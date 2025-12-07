"""URL patterns for reports app."""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('subject/<uuid:subject_pk>/module/', views.GenerateModuleReportView.as_view(), name='module_report'),
    path('subject/<uuid:subject_pk>/analytics/', views.GenerateAnalyticsReportView.as_view(), name='analytics_report'),
]
