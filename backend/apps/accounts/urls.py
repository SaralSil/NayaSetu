from django.urls import path
from .views import (
    UserProfileView,
    SavedSchemeListCreateView,
    SavedSchemeDetailView,
    CitizenRegisterAPIView,
    CitizenLoginAPIView,
    SendOTPAPIView,
    VerifyOTPAPIView
)

urlpatterns = [
    # Citizen Authentication Endpoints
    path('register/', CitizenRegisterAPIView.as_view(), name='citizen-register'),
    path('login/', CitizenLoginAPIView.as_view(), name='citizen-login'),
    path('send-otp/', SendOTPAPIView.as_view(), name='citizen-send-otp'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='citizen-verify-otp'),

    # Profile & Saved Schemes
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('saved-schemes/', SavedSchemeListCreateView.as_view(), name='saved-schemes-list'),
    path('saved-schemes/<int:pk>/', SavedSchemeDetailView.as_view(), name='saved-scheme-detail'),
]
