from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Scheme, Department, CommonRejectionReason
from .serializers import (
    SchemeListSerializer, SchemeDetailSerializer, 
    DepartmentSerializer, CommonRejectionReasonSerializer
)

class SchemeListView(generics.ListAPIView):
    """
    Search and filter West Bengal schemes.
    Supports query parameters: ?search=...&category=...&department=...
    """
    serializer_class = SchemeListSerializer

    def get_queryset(self):
        queryset = Scheme.objects.filter(is_active=True).select_related('department')
        search_query = self.request.query_params.get('search', '').strip()
        category = self.request.query_params.get('category', '').strip()
        department = self.request.query_params.get('department', '').strip()

        if search_query:
            queryset = queryset.filter(
                Q(name_en__icontains=search_query) |
                Q(name_bn__icontains=search_query) |
                Q(description_en__icontains=search_query) |
                Q(description_bn__icontains=search_query) |
                Q(tagline_en__icontains=search_query)
            )

        if category:
            queryset = queryset.filter(category=category)

        if department:
            queryset = queryset.filter(department__code=department)

        return queryset


class SchemeDetailView(generics.RetrieveAPIView):
    """Get complete details, document checklist, and common rejection remedies for a scheme"""
    queryset = Scheme.objects.filter(is_active=True).select_related('department', 'eligibility').prefetch_related('documents', 'rejection_reasons')
    serializer_class = SchemeDetailSerializer
    lookup_field = 'slug'


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EligibilityWizardView(APIView):
    """
    Evaluates citizen profile against all WB schemes.
    Input payload:
    {
      "age": 28,
      "gender": "female",
      "caste": "SC",
      "annual_family_income": 60000,
      "has_land": false,
      "is_student": false
    }
    """
    def post(self, request):
        data = request.data
        try:
            age = int(data.get('age', 0)) if data.get('age') is not None else None
        except (ValueError, TypeError):
            age = None
            
        gender = str(data.get('gender', '')).lower()
        caste = str(data.get('caste', 'General'))
        income = float(data.get('annual_family_income', 0)) if data.get('annual_family_income') else None
        has_land = bool(data.get('has_land', False))
        is_student = bool(data.get('is_student', False))

        schemes = Scheme.objects.filter(is_active=True).select_related('department', 'eligibility').prefetch_related('documents')
        
        matched_schemes = []

        for scheme in schemes:
            eligibility = getattr(scheme, 'eligibility', None)
            if not eligibility:
                continue

            match_score = 100
            reasons = []
            flags = []

            # 1. Gender check
            if eligibility.gender_allowed != 'all' and eligibility.gender_allowed != gender:
                continue  # Ineligible

            # 2. Age check
            if age is not None:
                if eligibility.min_age and age < eligibility.min_age:
                    continue
                if eligibility.max_age and age > eligibility.max_age:
                    continue

            # 3. Caste check
            if eligibility.caste_categories:
                # If scheme restricts to specific categories (e.g. Jai Johar ST, Taposhili Bandhu SC)
                if caste not in eligibility.caste_categories and 'All' not in eligibility.caste_categories:
                    continue

            # 4. Income check
            if eligibility.max_family_income and income is not None:
                if income > float(eligibility.max_family_income):
                    continue

            # 5. Land requirement (Krishak Bandhu)
            if eligibility.requires_land_record and not has_land:
                match_score -= 30
                flags.append("Requires cultivable land records (RoR/Porcha).")

            # Specific rules highlights
            if eligibility.requires_single_bank_account:
                flags.append("Requires a SINGLE bank account (joint account is strictly not accepted).")
            if eligibility.requires_swasthya_sathi:
                flags.append("Swasthya Sathi card is mandatory.")

            matched_schemes.append({
                "scheme": SchemeListSerializer(scheme).data,
                "match_score": match_score,
                "notes": flags,
                "mandatory_documents_count": scheme.documents.filter(is_mandatory=True).count(),
            })

        # Sort by match score
        matched_schemes.sort(key=lambda x: x['match_score'], reverse=True)

        return Response({
            "total_matches": len(matched_schemes),
            "profile_evaluated": {
                "age": age,
                "gender": gender,
                "caste": caste,
                "income": income,
                "has_land": has_land
            },
            "results": matched_schemes
        })
