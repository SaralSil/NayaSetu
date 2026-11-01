from django.urls import path
from .views import AnalyzeNoticeView

urlpatterns = [
    path('explain/', AnalyzeNoticeView.as_view(), name='explain-notice'),
]
