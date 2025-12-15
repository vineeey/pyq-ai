"""
AI-Powered Topic Clustering and Repetition Analysis Service.
Uses sentence transformers for semantic similarity to group questions by meaning.
"""
import logging
import re
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
from django.db import transaction

try:
    from sentence_transformers import SentenceTransformer, util
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logging.warning("sentence-transformers not available, using fallback clustering")

from apps.questions.models import Question
from apps.subjects.models import Subject, Module
from apps.analytics.models import TopicCluster

logger = logging.getLogger(__name__)


class TopicClusteringService:
    """
    AI-powered service to cluster questions by semantic meaning and analyze repetition patterns.
    Uses sentence-transformers for deep semantic understanding.
    """
    
    def __init__(
        self,
        subject: Subject,
        similarity_threshold: float = 0.75,  # Higher threshold for semantic similarity
        tier_1_threshold: int = 4,  # Top Priority: 4+ times
        tier_2_threshold: int = 3,  # High Priority: 3 times
        tier_3_threshold: int = 2   # Medium Priority: 2 times
    ):
        self.subject = subject
        self.similarity_threshold = similarity_threshold
        self.tier_1_threshold = tier_1_threshold
        self.tier_2_threshold = tier_2_threshold
        self.tier_3_threshold = tier_3_threshold
        
        # Initialize sentence transformer model if available
        self.model = None
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                logger.info("Loading sentence transformer model...")
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("✅ AI model loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load AI model: {e}, using fallback")
                self.model = None
        else:
            logger.info("Using enhanced keyword-based clustering (no AI model)")
    
    def analyze_subject(self) -> Dict[str, Any]:
        """
        Main entry point: analyze all questions using AI semantic similarity.
        
        Returns:
            Statistics about the clustering process
        """
        logger.info(f"Starting AI-powered topic analysis for subject: {self.subject}")
        
        # Get all questions for this subject
        questions = Question.objects.filter(
            paper__subject=self.subject
        ).select_related('paper', 'module').order_by('module__number', 'question_number')
        
        if not questions.exists():
            logger.warning(f"No questions found for subject {self.subject}")
            return {'clusters_created': 0, 'questions_clustered': 0}
        
        # Clear existing clusters for this subject
        with transaction.atomic():
            TopicCluster.objects.filter(subject=self.subject).delete()
        
        # Group questions by module and cluster using AI
        modules = self.subject.modules.all()
        total_clusters = 0
        total_questions_clustered = 0
        
        for module in modules:
            module_questions = list(questions.filter(module=module))
            if module_questions:
                clusters_count, questions_count = self._cluster_module_questions_ai(module, module_questions)
                total_clusters += clusters_count
                total_questions_clustered += questions_count
                logger.info(f"Module {module.number}: Created {clusters_count} clusters from {len(module_questions)} questions")
        
        # Handle unclassified questions
        unclassified = list(questions.filter(module__isnull=True))
        if unclassified:
            clusters_count, questions_count = self._cluster_module_questions_ai(None, unclassified)
            total_clusters += clusters_count
            total_questions_clustered += questions_count
            logger.info(f"Unclassified: Created {clusters_count} clusters")
        
        logger.info(f"✅ Total: {total_clusters} clusters created, {total_questions_clustered} questions clustered")
        
        return {
            'clusters_created': total_clusters,
            'questions_clustered': total_questions_clustered
        }
    
    def _cluster_module_questions_ai(self, module: Optional[Module], questions: List[Question]) -> Tuple[int, int]:
        """
        Cluster questions within a module using AI or enhanced keyword matching.
        
        Args:
            module: The module (or None for unclassified)
            questions: List of Question objects
            
        Returns:
            Tuple of (clusters_created, questions_clustered)
        """
        if not questions:
            return 0, 0
        
        logger.info(f"Clustering {len(questions)} questions...")
        
        # Use AI if available, otherwise use enhanced keyword matching
        if self.model:
            return self._cluster_with_ai(module, questions)
        else:
            return self._cluster_with_keywords(module, questions)
    
    def _cluster_with_ai(self, module: Optional[Module], questions: List[Question]) -> Tuple[int, int]:
        """Cluster using sentence transformers (AI semantic similarity)."""
        # Extract and clean question texts
        question_texts = [self._clean_question_text(q.text) for q in questions]
        
        # Generate embeddings
        logger.info("🤖 Generating AI embeddings...")
        embeddings = self.model.encode(question_texts, convert_to_tensor=False, show_progress_bar=False)
        
        # Calculate similarity and cluster
        clusters = []
        processed = set()
        
        for i, question in enumerate(questions):
            if i in processed:
                continue
            
            cluster_indices = [i]
            processed.add(i)
            
            # Find similar questions using cosine similarity
            for j in range(len(questions)):
                if j in processed or i == j:
                    continue
                
                # Manual cosine similarity (avoid numpy)
                similarity = self._cosine_similarity(embeddings[i], embeddings[j])
                
                if similarity >= self.similarity_threshold:
                    cluster_indices.append(j)
                    processed.add(j)
            
            cluster_questions = [questions[idx] for idx in cluster_indices]
            clusters.append({
                'representative': cluster_questions[0],
                'questions': cluster_questions
            })
        
        logger.info(f"✅ Created {len(clusters)} AI-powered clusters")
        
        # Save to database
        return self._save_clusters(module, clusters)
    
    def _cluster_with_keywords(self, module: Optional[Module], questions: List[Question]) -> Tuple[int, int]:
        """Enhanced keyword-based clustering (fallback when AI unavailable)."""
        logger.info("📊 Using enhanced keyword clustering...")
        
        clusters = []
        processed = set()
        
        for i, question in enumerate(questions):
            if i in processed:
                continue
            
            cluster_indices = [i]
            processed.add(i)
            
            # Get keywords for this question
            keywords1 = self._extract_keywords(question.text)
            
            # Find similar questions by keyword overlap
            for j in range(len(questions)):
                if j in processed or i == j:
                    continue
                
                keywords2 = self._extract_keywords(questions[j].text)
                similarity = self._keyword_similarity(keywords1, keywords2)
                
                if similarity >= self.similarity_threshold:
                    cluster_indices.append(j)
                    processed.add(j)
            
            cluster_questions = [questions[idx] for idx in cluster_indices]
            clusters.append({
                'representative': cluster_questions[0],
                'questions': cluster_questions
            })
        
        logger.info(f"✅ Created {len(clusters)} keyword-based clusters")
        
        return self._save_clusters(module, clusters)
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity without numpy."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _extract_keywords(self, text: str) -> set:
        """Extract meaningful keywords from question text."""
        text = self._clean_question_text(text).lower()
        
        # Remove common words
        stopwords = {
            'explain', 'describe', 'define', 'discuss', 'what', 'how', 'why', 
            'list', 'state', 'mention', 'briefly', 'detail', 'with', 'the', 
            'and', 'or', 'for', 'to', 'of', 'in', 'on', 'at', 'from'
        }
        
        words = text.split()
        keywords = {w for w in words if len(w) > 3 and w not in stopwords}
        
        return keywords
    
    def _keyword_similarity(self, keywords1: set, keywords2: set) -> float:
        """Calculate Jaccard similarity between keyword sets."""
        if not keywords1 or not keywords2:
            return 0.0
        
        intersection = keywords1.intersection(keywords2)
        union = keywords1.union(keywords2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _save_clusters(self, module: Optional[Module], clusters: List[Dict]) -> Tuple[int, int]:
        """Save clusters to database."""
        created_count = 0
        questions_clustered = 0
        
        with transaction.atomic():
            for cluster_data in clusters:
                if len(cluster_data['questions']) > 0:
                    self._create_topic_cluster(module, cluster_data)
                    created_count += 1
                    questions_clustered += len(cluster_data['questions'])
        
        return created_count, questions_clustered
    
    def _clean_question_text(self, text: str) -> str:
        """Clean question text for better semantic matching."""
        # Remove question numbers, marks, years
        text = re.sub(r'\(\d+\s*marks?\)', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(20\d{2})\b', '', text)  # Remove years
        text = re.sub(r'^[Qq]\s*\d+[a-z]?\s*[:.)\-]?\s*', '', text)  # Remove Q1, Q2, etc.
        text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
        return text
    
    def _are_similar(self, q1: Question, q2: Question) -> bool:
        """
        Determine if two questions are similar enough to be grouped.
        Uses text normalization and fuzzy matching.
        """
        # Normalize both texts
        norm1 = self._normalize_text(q1.text)
        norm2 = self._normalize_text(q2.text)
        
        # Check for very short texts (likely same topic)
        if len(norm1) < 30 or len(norm2) < 30:
            # Use simple substring matching for short questions
            return norm1 in norm2 or norm2 in norm1
        
        # Calculate simple similarity score
        similarity = self._calculate_text_similarity(norm1, norm2)
        
        return similarity >= self.similarity_threshold
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize question text for comparison.
        Removes marks, years, trivial words, and standardizes format.
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove common patterns
        text = re.sub(r'\(\s*\d+\s*marks?\s*\)', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\d{4}', '', text)  # Remove years
        text = re.sub(r'(dec|december|jun|june|nov|november|may|april|aug|august)\s*\d{4}', '', text, flags=re.IGNORECASE)
        
        # Remove question numbers and part indicators
        text = re.sub(r'^q\d+[a-z]?\s*[:\.\)]*\s*', '', text)
        text = re.sub(r'^question\s*\d+\s*[:\.\)]*\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^part\s*[ab]\s*[:\.\)]*\s*', '', text, flags=re.IGNORECASE)
        
        # Remove trivial words (but keep longer words even if in trivial list)
        trivial = ['the', 'a', 'an', 'and', 'or', 'but', 'with', 'for', 'to', 'of', 'in', 'on', 'at']
        words = text.split()
        words = [w for w in words if len(w) > 3 or w not in trivial]
        
        # Remove extra whitespace
        text = ' '.join(words)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two normalized texts.
        Uses token-based Jaccard similarity.
        """
        # Tokenize
        tokens1 = set(text1.split())
        tokens2 = set(text2.split())
        
        if not tokens1 or not tokens2:
            return 0.0
        
        # Jaccard similarity
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _extract_topic_name(self, question: Question) -> str:
        """
        Extract a meaningful topic name from a question using key phrases.
        """
        text = question.text
        
        # Remove action verbs at start
        text = re.sub(r'^(explain|define|describe|discuss|what|how|why|list|enumerate|state|elaborate|illustrate|classify|compare|differentiate|mention|identify|briefly)\s+', '', text, flags=re.IGNORECASE)
        
        # Remove marks notation
        text = re.sub(r'\(\s*\d+\s*marks?\s*\)', '', text, flags=re.IGNORECASE)
        
        # Take first meaningful part (up to 80 chars or first major punctuation)
        if '.' in text[:100]:
            text = text.split('.')[0]
        elif '?' in text[:100]:
            text = text.split('?')[0]
        
        text = text[:80].strip()
        
        # Capitalize properly
        text = ' '.join(word.capitalize() if len(word) > 3 else word.lower() for word in text.split())
        
        return text if text else question.text[:50]
        if '?' in text:
            text = text.split('?')[0]
        elif '.' in text:
            sentences = text.split('.')
            text = sentences[0] if len(sentences[0]) < 100 else sentences[0][:100]
        else:
            text = text[:100]
        
        # Capitalize first letter
        text = text.strip().capitalize()
        
        # If too long, truncate and add ellipsis
        if len(text) > 80:
            text = text[:77] + '...'
        
        return text
    
    def _create_topic_cluster(self, module: Optional[Module], cluster_data: Dict[str, Any]):
        """
        Create a TopicCluster object with proper priority calculation.
        """
        representative = cluster_data['representative']
        questions = cluster_data['questions']
        
        # Extract meaningful topic name
        topic_name = self._extract_topic_name(representative)
        
        # Calculate repetition statistics
        years = set()
        total_marks = 0
        
        for q in questions:
            # Get unique years
            if q.paper.year:
                years.add(str(q.paper.year))
            
            # Sum marks
            if q.marks:
                total_marks += q.marks
        
        # Frequency = number of unique years this topic appeared
        frequency_count = len(years)
        
        # Determine priority tier based on frequency
        if frequency_count >= self.tier_1_threshold:
            priority = TopicCluster.PriorityTier.TIER_1  # 🔥🔥🔥 TOP PRIORITY (4+ times)
        elif frequency_count >= self.tier_2_threshold:
            priority = TopicCluster.PriorityTier.TIER_2  # 🔥🔥 HIGH PRIORITY (3 times)
        elif frequency_count >= self.tier_3_threshold:
            priority = TopicCluster.PriorityTier.TIER_3  # 🔥 MEDIUM PRIORITY (2 times)
        else:
            priority = TopicCluster.PriorityTier.TIER_4  # ✓ LOW PRIORITY (1 time)
        
        # Create normalized key for deduplication
        normalized_key = self._clean_question_text(representative.text).lower()
        
        # Create TopicCluster
        cluster = TopicCluster.objects.create(
            subject=self.subject,
            module=module,
            topic_name=topic_name,
            normalized_key=normalized_key,
            representative_text=representative.text,
            frequency_count=frequency_count,
            years_appeared=sorted(list(years)),
            total_marks=total_marks,
            priority_tier=priority,
            question_count=len(questions)
        )
        
        logger.debug(f"Created cluster: {topic_name} ({frequency_count} times, {priority})")


def analyze_subject_topics(
    subject: Subject,
    similarity_threshold: float = 0.75,  # Higher for AI semantic matching
    tier_1_threshold: int = 4,  # TOP PRIORITY: 4+ times
    tier_2_threshold: int = 3,  # HIGH PRIORITY: 3 times
    tier_3_threshold: int = 2   # MEDIUM PRIORITY: 2 times
) -> Dict[str, Any]:
    """
    Convenience function to analyze topics for a subject.
    
    Args:
        subject: Subject instance
        similarity_threshold: Minimum similarity for clustering (0-1)
        tier_1_threshold: Minimum occurrences for Top Priority
        tier_2_threshold: Minimum occurrences for High Priority
        tier_3_threshold: Minimum occurrences for Medium Priority
    
    Returns:
        Statistics dictionary
    """
    service = TopicClusteringService(
        subject=subject,
        similarity_threshold=similarity_threshold,
        tier_1_threshold=tier_1_threshold,
        tier_2_threshold=tier_2_threshold,
        tier_3_threshold=tier_3_threshold
    )
    return service.analyze_subject()
