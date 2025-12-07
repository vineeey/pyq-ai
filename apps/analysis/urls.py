"""URL patterns for analysis app."""
from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('job/<uuid:pk>/', views.AnalysisDetailView.as_view(), name='detail'),
    path('job/<uuid:pk>/status/', views.AnalysisStatusView.as_view(), name='status'),
]
