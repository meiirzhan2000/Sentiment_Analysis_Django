from django.urls import path
from . import views

app_name = 'sentiment_analyzer'

urlpatterns = [
    path('', views.analyze_text_view, name='analyze'),
    path('history/', views.AnalysisHistoryView.as_view(), name='history'),
    path('analysis/<int:pk>/', views.AnalysisDetailView.as_view(), name='detail'),
]