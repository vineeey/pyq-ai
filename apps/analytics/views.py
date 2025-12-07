"""Views for analytics dashboard."""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from apps.subjects.models import Subject
from .calculator import StatsCalculator


class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    """Analytics dashboard for a subject."""
    
    template_name = 'analytics/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = get_object_or_404(
            Subject, pk=self.kwargs['subject_pk'], user=self.request.user
        )
        
        calculator = StatsCalculator(subject)
        
        context['subject'] = subject
        context['stats'] = calculator.get_complete_stats()
        
        return context


class AnalyticsAPIView(LoginRequiredMixin, TemplateView):
    """API endpoint for analytics data (for Chart.js)."""
    
    def get(self, request, subject_pk):
        subject = get_object_or_404(
            Subject, pk=subject_pk, user=request.user
        )
        
        calculator = StatsCalculator(subject)
        return JsonResponse(calculator.get_complete_stats())
