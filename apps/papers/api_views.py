"""API views for paper processing and status."""
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from apps.papers.models import Paper
from apps.subjects.models import Subject


class StartProcessingView(View):
    """Manually trigger processing for a paper or all papers in a subject."""
    
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        paper_id = request.POST.get('paper_id')
        subject_id = request.POST.get('subject_id')
        
        if paper_id:
            # Process single paper
            paper = get_object_or_404(Paper, id=paper_id)
            
            if paper.status == Paper.ProcessingStatus.PROCESSING:
                return JsonResponse({
                    'success': False,
                    'message': 'Paper is already being processed'
                })
            
            # Queue for processing
            from apps.analysis.tasks import analyze_paper_task
            from django_q.tasks import async_task
            
            paper.status = Paper.ProcessingStatus.PROCESSING
            paper.status_detail = 'Queued for processing...'
            paper.progress_percent = 0
            paper.save()
            
            async_task(analyze_paper_task, paper.id)
            
            return JsonResponse({
                'success': True,
                'message': f'Started processing: {paper.title}',
                'paper_id': str(paper.id)
            })
            
        elif subject_id:
            # Process all pending papers in subject
            subject = get_object_or_404(Subject, id=subject_id)
            pending_papers = subject.papers.filter(status=Paper.ProcessingStatus.PENDING)
            
            if not pending_papers.exists():
                return JsonResponse({
                    'success': False,
                    'message': 'No pending papers to process'
                })
            
            from apps.analysis.tasks import analyze_paper_task
            from django_q.tasks import async_task
            
            count = 0
            for paper in pending_papers:
                paper.status = Paper.ProcessingStatus.PROCESSING
                paper.status_detail = 'Queued for processing...'
                paper.progress_percent = 0
                paper.save()
                
                async_task(analyze_paper_task, paper.id)
                count += 1
            
            return JsonResponse({
                'success': True,
                'message': f'Started processing {count} papers',
                'count': count
            })
        
        return JsonResponse({
            'success': False,
            'message': 'Missing paper_id or subject_id'
        }, status=400)


class PaperStatusView(View):
    """Get real-time status of paper processing."""
    
    def get(self, request, paper_id):
        paper = get_object_or_404(Paper, id=paper_id)
        
        return JsonResponse({
            'id': str(paper.id),
            'title': paper.title,
            'status': paper.status,
            'status_detail': paper.status_detail,
            'progress_percent': paper.progress_percent,
            'questions_extracted': paper.questions_extracted,
            'questions_classified': paper.questions_classified,
            'error': paper.processing_error if paper.status == Paper.ProcessingStatus.FAILED else None
        })


class SubjectStatusView(View):
    """Get status of all papers in a subject."""
    
    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        papers = subject.papers.all()
        
        papers_data = []
        for paper in papers:
            papers_data.append({
                'id': str(paper.id),
                'title': paper.title,
                'status': paper.status,
                'status_detail': paper.status_detail,
                'progress_percent': paper.progress_percent,
                'questions_extracted': paper.questions_extracted,
                'questions_classified': paper.questions_classified,
            })
        
        # Calculate overall stats
        total = papers.count()
        completed = papers.filter(status=Paper.ProcessingStatus.COMPLETED).count()
        processing = papers.filter(status=Paper.ProcessingStatus.PROCESSING).count()
        pending = papers.filter(status=Paper.ProcessingStatus.PENDING).count()
        failed = papers.filter(status=Paper.ProcessingStatus.FAILED).count()
        
        return JsonResponse({
            'subject_id': str(subject.id),
            'subject_name': subject.name,
            'papers': papers_data,
            'stats': {
                'total': total,
                'completed': completed,
                'processing': processing,
                'pending': pending,
                'failed': failed
            }
        })
