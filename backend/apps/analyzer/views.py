from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .services.gemini_service import GeminiAnalyzerService
from .services.chatbot_service import ChatbotAssistantService

class AnalyzeNoticeView(APIView):
    """
    Accepts text or uploaded photo of a West Bengal scheme notice/rejection/SMS
    and returns a plain-language explanation and action plan.
    """
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        service = GeminiAnalyzerService()
        
        # Check language preference ('bn', 'hi', 'en')
        lang = (request.data.get('lang') or request.data.get('language') or 'bn').strip().lower()
        if lang not in ['bn', 'hi', 'en']:
            lang = 'bn'

        # Check if an image was uploaded
        image_file = request.FILES.get('image')
        notice_text = request.data.get('text', '').strip()

        if image_file:
            analysis = service.analyze_image(image_file, lang=lang)
            return Response(analysis, status=status.HTTP_200_OK)
        elif notice_text:
            analysis = service.analyze_text(notice_text, lang=lang)
            return Response(analysis, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Please provide either 'text' (notice/SMS content) or upload an 'image' file."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChatbotAssistantView(APIView):
    """
    Accepts user questions about schemes, scholarships, documents, or website navigation.
    Returns response strictly as 'नया सेतु AI' with required documents, links, and action buttons.
    Supports multi-lingual queries (English, Bengali, Hindi) and dynamic Gemini LLM generation.
    """
    parser_classes = [JSONParser, FormParser]

    def post(self, request):
        service = ChatbotAssistantService()
        message = request.data.get('message', '').strip()
        history = request.data.get('history', [])
        api_key = request.data.get('api_key', '').strip() or request.headers.get('X-Gemini-Api-Key', '').strip()
        preferred_lang = request.data.get('language', '').strip()
        
        result = service.get_reply(
            user_message=message,
            history=history,
            api_key_override=api_key,
            preferred_language=preferred_lang
        )
        return Response(result, status=status.HTTP_200_OK)

