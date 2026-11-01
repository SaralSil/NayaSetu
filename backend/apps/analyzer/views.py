from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .services.gemini_service import GeminiAnalyzerService

class AnalyzeNoticeView(APIView):
    """
    Accepts text or uploaded photo of a West Bengal scheme notice/rejection/SMS
    and returns a plain-language explanation and action plan.
    """
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        service = GeminiAnalyzerService()
        
        # Check if an image was uploaded
        image_file = request.FILES.get('image')
        notice_text = request.data.get('text', '').strip()

        if image_file:
            analysis = service.analyze_image(image_file)
            return Response(analysis, status=status.HTTP_200_OK)
        elif notice_text:
            analysis = service.analyze_text(notice_text)
            return Response(analysis, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Please provide either 'text' (notice/SMS content) or upload an 'image' file."},
                status=status.HTTP_400_BAD_REQUEST
            )
