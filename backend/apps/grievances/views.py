import math
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import OfficialDirectory, GrievanceDraft
from .services.letter_generator import generate_representation_letter

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in kilometers between two GPS coordinates using Haversine formula"""
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

class OfficialDirectoryListView(generics.ListAPIView):
    """List administrative offices (BDO, SDO, Seva Shivir desks) by district and compute nearest office via GPS"""
    def get(self, request):
        district = request.query_params.get('district', '').strip()
        office_type = request.query_params.get('office_type', '').strip()
        user_lat = request.query_params.get('lat', '').strip()
        user_lng = request.query_params.get('lng', '').strip()
        
        queryset = OfficialDirectory.objects.all()
        if district:
            queryset = queryset.filter(district__iexact=district)
        if office_type:
            queryset = queryset.filter(office_type=office_type)

        u_lat = None
        u_lng = None
        if user_lat and user_lng:
            try:
                u_lat = float(user_lat)
                u_lng = float(user_lng)
            except ValueError:
                pass
            
        data = []
        for o in queryset:
            item = {
                "id": o.id,
                "office_type": o.office_type,
                "district": o.district,
                "block_or_subdivision": o.block_or_subdivision,
                "designation": o.designation,
                "address": o.office_address,
                "phone": o.contact_phone,
                "email": o.official_email,
                "portal_url": o.grievance_portal_url,
                "latitude": o.latitude,
                "longitude": o.longitude,
                "distance_km": None
            }
            if u_lat is not None and u_lng is not None and o.latitude is not None and o.longitude is not None:
                item["distance_km"] = haversine_distance(u_lat, u_lng, o.latitude, o.longitude)
            data.append(item)

        if u_lat is not None and u_lng is not None:
            # Sort with valid distance first
            data.sort(key=lambda x: (x["distance_km"] is None, x["distance_km"] if x["distance_km"] is not None else float('inf')))
            if data and data[0]["distance_km"] is not None:
                data[0]["is_nearest"] = True

        return Response(data)


class GenerateGrievanceDraftView(APIView):
    """
    Generates a formal representation letter to a BDO, SDO, or Portal.
    """
    def post(self, request):
        data = request.data
        raw_name = data.get('applicant_name', '').strip()
        scheme_name = data.get('scheme_name', '').strip()
        
        if not raw_name or not scheme_name:
            return Response(
                {"error": "'applicant_name' and 'scheme_name' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Strict validation: Only alphabets (English, Bengali, Hindi) and spaces allowed
        import re
        applicant_name = re.sub(r'[^a-zA-Z\sঀ-৿ऀ-ॿ]', '', raw_name)
        applicant_name = re.sub(r'\s+', ' ', applicant_name).strip()
        if not applicant_name:
            return Response(
                {"error": "Applicant name must contain only alphabetic letters (no numbers or special characters).", "code": "INVALID_NAME"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Strict validation: Contact phone must contain only numbers (0-9), max 10 digits
        raw_phone = data.get('contact_phone', '')
        contact_phone = re.sub(r'\D', '', str(raw_phone))[:10] if raw_phone else ''
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
