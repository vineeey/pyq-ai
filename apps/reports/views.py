"""Views for report generation and download."""
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from pathlib import Path

from apps.subjects.models import Subject
from .generator import ReportGenerator


class GenerateModuleReportView(LoginRequiredMixin, View):
    """Generate and download module report."""
    
    def get(self, request, subject_pk):
        subject = get_object_or_404(
            Subject, pk=subject_pk, user=request.user
        )
        
        generator = ReportGenerator(subject)
        pdf_path = generator.generate_module_report()
        
        if pdf_path and Path(pdf_path).exists():
            return FileResponse(
                open(pdf_path, 'rb'),
                content_type='application/pdf',
                as_attachment=True,
                filename=f'{subject.name}_module_report.pdf'
            )
        
        raise Http404("Report generation failed")


class GenerateAnalyticsReportView(LoginRequiredMixin, View):
    """Generate and download analytics report."""
    
    def get(self, request, subject_pk):
        subject = get_object_or_404(
            Subject, pk=subject_pk, user=request.user
        )
        
        generator = ReportGenerator(subject)
        pdf_path = generator.generate_analytics_report()
        
        if pdf_path and Path(pdf_path).exists():
            return FileResponse(
                open(pdf_path, 'rb'),
                content_type='application/pdf',
                as_attachment=True,
                filename=f'{subject.name}_analytics_report.pdf'
            )
        
        raise Http404("Report generation failed")
