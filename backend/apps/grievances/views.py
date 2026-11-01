from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import OfficialDirectory, GrievanceDraft
from .services.letter_generator import generate_representation_letter

class OfficialDirectoryListView(generics.ListAPIView):
    """List administrative offices (BDO, SDO, Duare Sarkar nodal desks) by district"""
    def get(self, request):
        district = request.query_params.get('district', '').strip()
        office_type = request.query_params.get('office_type', '').strip()
        
        queryset = OfficialDirectory.objects.all()
        if district:
            queryset = queryset.filter(district__iexact=district)
        if office_type:
            queryset = queryset.filter(office_type=office_type)
            
        data = [
            {
                "id": o.id,
                "office_type": o.office_type,
                "district": o.district,
                "designation": o.designation,
                "address": o.office_address,
                "phone": o.contact_phone,
                "portal_url": o.grievance_portal_url
            } for o in queryset
        ]
        return Response(data)


class GenerateGrievanceDraftView(APIView):
    """
    Generates a formal representation letter to a BDO, SDO, or Portal.
    """
    def post(self, request):
        data = request.data
        applicant_name = data.get('applicant_name', '').strip()
        scheme_name = data.get('scheme_name', '').strip()
        
        if not applicant_name or not scheme_name:
            return Response(
                {"error": "'applicant_name' and 'scheme_name' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        contact_phone = data.get('contact_phone', '')
        residence_address = data.get('residence_address', '')
        application_ref_no = data.get('application_ref_no', '')
        original_application_date = data.get('original_application_date', '')
        grievance_type = data.get('grievance_type', 'delay')
        addressed_to = data.get('addressed_to', '')
        facts_statement = data.get('facts_statement', '')
        language = data.get('language', 'bn')

        letter_text = generate_representation_letter(
            applicant_name=applicant_name,
            contact_phone=contact_phone,
            residence_address=residence_address,
            scheme_name=scheme_name,
            application_ref_no=application_ref_no,
            original_application_date=original_application_date,
            grievance_type=grievance_type,
            addressed_to=addressed_to,
            facts_statement=facts_statement,
            language=language
        )

        # Save record if user wishes to keep track
        draft = GrievanceDraft.objects.create(
            applicant_name=applicant_name,
            contact_phone=contact_phone,
            residence_address=residence_address,
            scheme_name=scheme_name,
            application_reference_no=application_ref_no,
            original_application_date=original_application_date,
            grievance_type=grievance_type,
            language=language,
            facts_statement=facts_statement,
            generated_letter_text=letter_text
        )

        return Response({
            "draft_id": draft.id,
            "language": language,
            "generated_letter": letter_text,
            "official_submission_advice": {
                "step_1": "Print 2 copies of this letter.",
                "step_2": "Sign both copies and attach self-attested photocopies of your Aadhaar card, bank passbook, and acknowledgment receipt.",
                "step_3": "Submit one copy at the Receiving Counter of your BDO/SDO office or Duare Sarkar Camp, and take a 'Received' rubber stamp with date on the second copy as proof."
            },
            "disclaimer": "NyayaSetu AI is an independent preparation assistant and does not submit complaints directly to government databases without personal verification."
        }, status=status.HTTP_201_CREATED)
