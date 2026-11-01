from django.db import models
from django.contrib.auth import get_user_model
from apps.schemes.models import Scheme

User = get_user_model()

class UserProfile(models.Model):
    """Profile synced with Supabase Auth"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    supabase_uid = models.CharField(max_length=128, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    district = models.CharField(max_length=100, blank=True)
    block_or_municipality = models.CharField(max_length=100, blank=True)
    preferred_language = models.CharField(
        max_length=10, 
        choices=[('bn', 'Bengali'), ('en', 'English'), ('hi', 'Hindi')], 
        default='bn'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class SavedScheme(models.Model):
    """Citizen's bookmarked schemes & application tracking"""
    STATUS_CHOICES = [
        ('exploring', 'Exploring / Checking Eligibility'),
        ('collecting_docs', 'Gathering Documents'),
        ('applied', 'Applied at Duare Sarkar / BDO'),
        ('on_hold', 'Notice Received / Action Required'),
        ('approved', 'Sanctioned / Receiving Benefits'),
        ('rejected', 'Application Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_schemes')
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    tracking_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='exploring')
    application_ref_number = models.CharField(max_length=100, blank=True)
    checked_documents = models.JSONField(default=list, help_text="IDs of documents applicant already has")
    user_notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'scheme')

    def __str__(self):
        return f"{self.user.username} -> {self.scheme.name_en}"
