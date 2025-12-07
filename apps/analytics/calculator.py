"""
Statistics calculator for analytics dashboard.
"""
from typing import Dict, Any, List
from collections import Counter
from django.db.models import Count, Avg

from apps.questions.models import Question
from apps.subjects.models import Subject


class StatsCalculator:
    """Calculates statistics for a subject."""
    
    def __init__(self, subject: Subject):
        self.subject = subject
        self.questions = Question.objects.filter(paper__subject=subject)
    
    def get_overview(self) -> Dict[str, Any]:
        """Get overview statistics."""
        total_questions = self.questions.count()
        unique_questions = self.questions.filter(is_duplicate=False).count()
        duplicates = total_questions - unique_questions
        
        return {
            'total_questions': total_questions,
            'unique_questions': unique_questions,
            'duplicates': duplicates,
            'duplicate_percentage': round(duplicates / total_questions * 100, 1) if total_questions else 0,
            'papers_count': self.subject.papers.count(),
            'modules_count': self.subject.modules.count(),
        }
    
    def get_module_distribution(self) -> List[Dict[str, Any]]:
        """Get question distribution across modules."""
        modules = self.subject.modules.all()
        distribution = []
        
        for module in modules:
            count = self.questions.filter(module=module).count()
            distribution.append({
                'module': module.name,
                'module_number': module.number,
                'count': count,
                'expected_weightage': float(module.weightage),
            })
        
        # Add unclassified
        unclassified = self.questions.filter(module__isnull=True).count()
        if unclassified:
            distribution.append({
                'module': 'Unclassified',
                'module_number': 0,
                'count': unclassified,
                'expected_weightage': 0,
            })
        
        return distribution
    
    def get_difficulty_distribution(self) -> Dict[str, int]:
        """Get question distribution by difficulty."""
        return dict(
            self.questions
            .exclude(difficulty='')
            .values('difficulty')
            .annotate(count=Count('id'))
            .values_list('difficulty', 'count')
        )
    
    def get_bloom_distribution(self) -> Dict[str, int]:
        """Get question distribution by Bloom's level."""
        return dict(
            self.questions
            .exclude(bloom_level='')
            .values('bloom_level')
            .annotate(count=Count('id'))
            .values_list('bloom_level', 'count')
        )
    
    def get_year_trend(self) -> List[Dict[str, Any]]:
        """Get question count trend by year."""
        papers = self.subject.papers.exclude(year='').order_by('year')
        trend = []
        
        for paper in papers:
            count = paper.questions.count()
            trend.append({
                'year': paper.year,
                'paper': paper.title,
                'question_count': count,
            })
        
        return trend
    
    def get_topic_frequency(self, top_n: int = 10) -> List[Dict[str, int]]:
        """Get most frequent topics."""
        all_topics = []
        for question in self.questions.exclude(topics=[]):
            all_topics.extend(question.topics)
        
        counter = Counter(all_topics)
        return [{'topic': t, 'count': c} for t, c in counter.most_common(top_n)]
    
    def get_complete_stats(self) -> Dict[str, Any]:
        """Get all statistics."""
        return {
            'overview': self.get_overview(),
            'module_distribution': self.get_module_distribution(),
            'difficulty_distribution': self.get_difficulty_distribution(),
            'bloom_distribution': self.get_bloom_distribution(),
            'year_trend': self.get_year_trend(),
            'top_topics': self.get_topic_frequency(),
        }
