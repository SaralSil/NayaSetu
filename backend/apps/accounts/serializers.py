from rest_framework import serializers
from .models import UserProfile, SavedScheme
from apps.schemes.serializers import SchemeListSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'supabase_uid', 'phone_number', 'district', 'block_or_municipality', 'preferred_language']


class SavedSchemeSerializer(serializers.ModelSerializer):
    scheme_detail = SchemeListSerializer(source='scheme', read_only=True)

    class Meta:
        model = SavedScheme
        fields = [
            'id', 'scheme', 'scheme_detail', 'tracking_status', 
            'application_ref_number', 'checked_documents', 'user_notes', 'updated_at'
        ]
