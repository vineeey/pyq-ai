"""Views for question management."""
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Question
from .forms import QuestionEditForm


class QuestionListView(LoginRequiredMixin, ListView):
    """List all questions for a paper."""
    
    model = Question
    template_name = 'questions/question_list.html'
    context_object_name = 'questions'
    
    def get_queryset(self):
        return Question.objects.filter(
            paper__subject__user=self.request.user
        ).select_related('paper', 'module')


class QuestionDetailView(LoginRequiredMixin, DetailView):
    """View question details."""
    
    model = Question
    template_name = 'questions/question_detail.html'
    context_object_name = 'question'
    
    def get_queryset(self):
        return Question.objects.filter(
            paper__subject__user=self.request.user
        ).select_related('paper', 'module', 'duplicate_of')


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    """Update question classification."""
    
    model = Question
    form_class = QuestionEditForm
    template_name = 'questions/question_edit.html'
    
    def get_queryset(self):
        return Question.objects.filter(paper__subject__user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('questions:detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        # Set manual override flags
        if 'module' in form.changed_data:
            form.instance.module_manually_set = True
        if 'difficulty' in form.changed_data:
            form.instance.difficulty_manually_set = True
        messages.success(self.request, 'Question updated successfully!')
        return super().form_valid(form)
