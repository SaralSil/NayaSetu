from django.urls import path
from .views import AnalyzeNoticeView, ChatbotAssistantView

urlpatterns = [
    path('explain/', AnalyzeNoticeView.as_view(), name='explain-notice'),
    path('chat/', ChatbotAssistantView.as_view(), name='chatbot-assistant'),
]
