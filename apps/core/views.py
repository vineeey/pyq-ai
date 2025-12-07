"""
Core views - Home and Dashboard.
"""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count

from apps.papers.models import Paper
from apps.questions.models import Question


class HomeView(TemplateView):
    """Landing page view."""
    template_name = 'pages/home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view after login."""
    template_name = 'pages/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user's statistics
        context['total_subjects'] = user.subjects.count() if hasattr(user, 'subjects') else 0
        context['total_papers'] = Paper.objects.filter(subject__user=user).count()
        context['total_questions'] = Question.objects.filter(paper__subject__user=user).count()
        
        # Get recent subjects
        context['recent_subjects'] = user.subjects.all()[:5] if hasattr(user, 'subjects') else []
        
        return context
