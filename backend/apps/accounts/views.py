from rest_framework import generics, permissions
from .models import UserProfile, SavedScheme
from .serializers import UserProfileSerializer, SavedSchemeSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class SavedSchemeListCreateView(generics.ListCreateAPIView):
    serializer_class = SavedSchemeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedScheme.objects.filter(user=self.request.user).select_related('scheme', 'scheme__department')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavedSchemeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavedSchemeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedScheme.objects.filter(user=self.request.user)
