"""Views for analysis app."""
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from .models import AnalysisJob


class AnalysisStatusView(LoginRequiredMixin, View):
    """Get analysis job status (for HTMX polling)."""
    
    def get(self, request, pk):
        try:
            job = AnalysisJob.objects.get(
                pk=pk,
                paper__subject__user=request.user
            )
            return JsonResponse({
                'status': job.status,
                'progress': job.progress,
                'questions_extracted': job.questions_extracted,
                'questions_classified': job.questions_classified,
                'duplicates_found': job.duplicates_found,
                'error_message': job.error_message,
            })
        except AnalysisJob.DoesNotExist:
            return JsonResponse({'error': 'Job not found'}, status=404)


class AnalysisDetailView(LoginRequiredMixin, DetailView):
    """View analysis job details."""
    
    model = AnalysisJob
    template_name = 'analysis/analysis_detail.html'
    context_object_name = 'job'
    
    def get_queryset(self):
        return AnalysisJob.objects.filter(paper__subject__user=self.request.user)
