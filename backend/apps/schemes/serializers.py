from rest_framework import serializers
from .models import Department, Scheme, SchemeEligibility, SchemeDocument, CommonRejectionReason

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name_en', 'name_bn', 'name_hi', 'code', 'portal_url', 'helpline']


class SchemeEligibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeEligibility
        fields = [
            'min_age', 'max_age', 'gender_allowed', 'caste_categories', 
            'max_family_income', 'requires_single_bank_account', 
            'requires_aadhaar_dbt_linking', 'requires_swasthya_sathi', 
            'requires_land_record', 'rules_summary_en', 'rules_summary_bn', 'custom_rules'
        ]


class SchemeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeDocument
        fields = [
            'id', 'name_en', 'name_bn', 'name_hi', 'is_mandatory', 
            'clarification_en', 'clarification_bn', 'how_to_obtain_en', 'how_to_obtain_bn'
        ]


class CommonRejectionReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonRejectionReason
        fields = [
            'id', 'code_or_phrase', 'title_en', 'title_bn', 
            'explanation_en', 'explanation_bn', 'explanation_hi',
            'remedy_steps_en', 'remedy_steps_bn', 'responsible_authority'
        ]


class SchemeListSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Scheme
        fields = [
            'id', 'slug', 'category', 'name_en', 'name_bn', 'name_hi',
            'tagline_en', 'tagline_bn', 'tagline_hi', 'benefit_type',
            'benefit_amount_text_en', 'benefit_amount_text_bn',
            'department', 'is_active'
        ]


class SchemeDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    eligibility = SchemeEligibilitySerializer(read_only=True)
    documents = SchemeDocumentSerializer(many=True, read_only=True)
    rejection_reasons = CommonRejectionReasonSerializer(many=True, read_only=True)

    class Meta:
        model = Scheme
        fields = [
            'id', 'slug', 'category', 'name_en', 'name_bn', 'name_hi',
            'tagline_en', 'tagline_bn', 'tagline_hi',
            'description_en', 'description_bn', 'description_hi',
            'benefit_type', 'benefit_amount_text_en', 'benefit_amount_text_bn',
            'application_channels', 'official_portal_url', 'department',
            'eligibility', 'documents', 'rejection_reasons', 'is_active'
        ]
