"""
Background tasks for analysis using Django-Q2.
"""
from django_q.tasks import async_task
from apps.papers.models import Paper


def analyze_paper_task(paper_id: str):
    """
    Background task to analyze a paper.
    Called via Django-Q2.
    """
    from .pipeline import AnalysisPipeline
    
    try:
        paper = Paper.objects.get(id=paper_id)
        paper.status = Paper.ProcessingStatus.PROCESSING
        paper.save()
        
        # Run analysis without LLM for speed (use keyword-based classification)
        # LLM is too slow for real-time processing
        pipeline = AnalysisPipeline(llm_client=None)
        pipeline.analyze_paper(paper)
        
    except Paper.DoesNotExist:
        pass
    except Exception as e:
        paper.status = Paper.ProcessingStatus.FAILED
        paper.processing_error = str(e)
        paper.save()


def queue_paper_analysis(paper: Paper):
    """Queue a paper for background analysis."""
    async_task(
        'apps.analysis.tasks.analyze_paper_task',
        str(paper.id),
        task_name=f'analyze_paper_{paper.id}'
    )
