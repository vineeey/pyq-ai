"""
Enhanced analysis pipeline with dual classification system.
"""
import logging
from typing import Optional
from django.utils import timezone
from django.conf import settings

from apps.papers.models import Paper
from apps.questions.models import Question
from .models import AnalysisJob
from .services.pymupdf_extractor import PyMuPDFExtractor
from .services.extractor import QuestionExtractor
from .services.classifier import ModuleClassifier
from .services.bloom import BloomClassifier
from .services.difficulty import DifficultyEstimator

# Services with optional numpy dependency
try:
    from .services.ai_classifier import AIClassifier
    from .services.embedder import EmbeddingService
    from .services.similarity import SimilarityService
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    AIClassifier = None
    EmbeddingService = None
    SimilarityService = None

logger = logging.getLogger(__name__)


class AnalysisPipeline:
    """
    Enhanced orchestration of analysis workflow with dual classification.
    - KTU: Rule-based mapping (strict)
    - Other: AI-based classification (LLM + embeddings + clustering)
    """
    
    def __init__(self, llm_client=None):
        # Extractors
        self.pymupdf_extractor = PyMuPDFExtractor()  # Primary extractor
        self.fallback_extractor = QuestionExtractor()  # Fallback
        
        # Services (with numpy fallback handling)
        if NUMPY_AVAILABLE:
            self.embedder = EmbeddingService()
            self.similarity = SimilarityService()
            self.ai_classifier = AIClassifier(llm_client, self.embedder)
        else:
            self.embedder = None
            self.similarity = None
            self.ai_classifier = None
            logger.warning("NumPy not available - AI features disabled")
        
        self.bloom_classifier = BloomClassifier(llm_client)
        self.difficulty_estimator = DifficultyEstimator(llm_client)
        
        # Classifiers
        self.module_classifier = ModuleClassifier(llm_client)  # For KTU
        
        self.llm_client = llm_client
    
    def analyze_paper(self, paper: Paper) -> AnalysisJob:
        """
        Run complete analysis on a paper with dual classification support.
        
        Args:
            paper: Paper instance to analyze
            
        Returns:
            AnalysisJob with results
        """
        # Create analysis job
        job = AnalysisJob.objects.create(paper=paper)
        job.started_at = timezone.now()
        job.save()
        
        try:
            subject = paper.subject
            is_ktu = subject.university_type == 'KTU' if hasattr(subject, 'university_type') else True
            
            logger.info(f"Starting analysis for {paper.title} - University: {subject.university_type if hasattr(subject, 'university_type') else 'KTU'}")
            
            # Step 1: Extract text, images, and questions using PyMuPDF
            job.status = AnalysisJob.Status.EXTRACTING
            job.progress = 5
            job.status_detail = 'Reading PDF file...'
            job.save()
            
            try:
                questions_data, images = self.pymupdf_extractor.extract_questions_with_images(
                    paper.file.path
                )
                
                # Store extracted text
                paper.raw_text = self.pymupdf_extractor.extract_text(paper.file.path)
                paper.page_count = self.pymupdf_extractor.get_page_count(paper.file.path)
                paper.save()
                
                logger.info(f"PyMuPDF: Extracted {len(questions_data)} questions and {len(images)} images")
                
            except Exception as e:
                logger.error(f"PyMuPDF extraction failed, using fallback: {e}")
                
                # Fallback to pdfplumber
                text = self.fallback_extractor.extract_text(paper.file.path)
                paper.raw_text = text
                paper.page_count = self.fallback_extractor.get_page_count(paper.file.path)
                paper.save()
                
                questions_data = self.fallback_extractor.extract_questions(text)
                images = []
            
            job.questions_extracted = len(questions_data)
            job.progress = 30
            job.status_detail = f'Found {len(questions_data)} questions from {paper.page_count} pages'
            job.save()
            
            # Step 2: Classify questions based on university type
            job.status = AnalysisJob.Status.CLASSIFYING
            job.progress = 40
            job.status_detail = 'Creating question records...'
            job.save()
            
            modules = list(subject.modules.all())
            
            if is_ktu:
                # KTU: Use strict rule-based classification
                classified_questions = self._classify_ktu_questions(
                    questions_data, subject, modules
                )
            else:
                # Other Universities: Use AI-based classification
                if self.ai_classifier:
                    syllabus_text = subject.syllabus_text if hasattr(subject, 'syllabus_text') else None
                    classified_questions = self.ai_classifier.classify_questions_semantic(
                        questions_data, subject, syllabus_text
                    )
                else:
                    # Fallback to KTU classification if AI not available
                    logger.warning("AI classifier not available, using KTU classification")
                    classified_questions = self._classify_ktu_questions(
                        questions_data, subject, modules
                    )
            
            job.progress = 60
            job.status_detail = f'Classified {len(classified_questions)} questions'
            job.save()
            
            # Step 3: Create question objects in database
            job.status = AnalysisJob.Status.ANALYZING
            job.save()
            
            created_questions = []
            for i, q_data in enumerate(classified_questions):
                # Update progress every 5 questions
                if i > 0 and i % 5 == 0:
                    progress = 60 + int((i / len(classified_questions)) * 20)
                    job.progress = progress
                    job.status_detail = f'Saving question {i}/{len(classified_questions)}...'
                    job.save()
                
                # Find module
                module = None
                if 'module_number' in q_data:
                    module = next(
                        (m for m in modules if m.number == q_data['module_number']), 
                        None
                    )
                
                # Create question
                question = Question.objects.create(
                    paper=paper,
                    question_number=q_data.get('question_number', ''),
                    text=q_data['text'],
                    marks=q_data.get('marks'),
                    part=q_data.get('part', ''),
                    module=module,
                    images=q_data.get('images', []),
                    question_type=q_data.get('question_type', ''),
                    difficulty=q_data.get('difficulty', ''),
                    bloom_level=q_data.get('bloom_level', ''),
                    embedding=q_data.get('embedding')
                )
                
                created_questions.append(question)
            
            job.progress = 90
            job.status_detail = 'Finalizing analysis...'
            job.save()
            
            # Step 4: Mark paper as completed
            paper.status = Paper.ProcessingStatus.COMPLETED
            paper.processed_at = timezone.now()
            paper.save()
            
            # Complete job
            job.status = AnalysisJob.Status.COMPLETED
            job.progress = 100
            job.status_detail = 'Analysis completed successfully'
            job.completed_at = timezone.now()
            job.save()
            
            logger.info(f"Analysis completed: {len(created_questions)} questions created")
            return job
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            
            # Mark as failed
            job.status = AnalysisJob.Status.FAILED
            job.error_message = str(e)
            job.completed_at = timezone.now()
            job.save()
            
            paper.status = Paper.ProcessingStatus.FAILED
            paper.processing_error = str(e)
            paper.save()
            
            raise
    
    def _classify_ktu_questions(
        self,
        questions_data: list,
        subject,
        modules: list
    ) -> list:
        """
        KTU-specific rule-based classification.
        Uses strict question number to module mapping.
        """
        logger.info("Using KTU rule-based classification")
        
        exam_pattern = None
        if hasattr(subject, 'exam_pattern'):
            exam_pattern = subject.exam_pattern
        
        classified = []
        
        for q_data in questions_data:
            # Get module assignment from pattern
            module_num = None
            part = q_data.get('part', '')
            
            if exam_pattern and part:
                module_num = exam_pattern.get_module_for_question(
                    q_data['question_number'], part
                )
            
            # Add module_number to data
            q_data['module_number'] = module_num if module_num else 1
            
            # Use rule-based Bloom and difficulty
            q_data['bloom_level'] = self.bloom_classifier.classify(q_data['text'])
            q_data['difficulty'] = self.difficulty_estimator.estimate(
                q_data['text'], q_data.get('marks')
            )
            
            # Simple question type classification
            q_data['question_type'] = self._simple_question_type(q_data['text'])
            
            classified.append(q_data)
        
        return classified
    
    def _simple_question_type(self, text: str) -> str:
        """Simple rule-based question type classification."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['define', 'what is']):
            return 'definition'
        elif any(word in text_lower for word in ['derive', 'proof']):
            return 'derivation'
        elif any(word in text_lower for word in ['calculate', 'compute']):
            return 'numerical'
        elif any(word in text_lower for word in ['draw', 'diagram']):
            return 'diagram'
        elif any(word in text_lower for word in ['compare', 'differentiate']):
            return 'comparison'
        else:
            return 'theory'
