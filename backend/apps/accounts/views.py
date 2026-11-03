import random
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate, login
from django.core.cache import cache
from .models import UserProfile, SavedScheme
from .serializers import UserProfileSerializer, SavedSchemeSerializer

User = get_user_model()

# In-memory OTP store for fast citizen verification (phone -> code)
# In production, this integrates with state SMS gateway (CDAC / NIC SMS)
OTP_STORE = {}

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


class CitizenRegisterAPIView(APIView):
    """Register a new citizen in NyayaSetu AI with West Bengal district & language preferences"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        phone = data.get('phone', '').strip().replace(' ', '').replace('+91', '')
        full_name = data.get('full_name', '').strip()
        password = data.get('password', '')
        district = data.get('district', '').strip()
        block_or_municipality = data.get('block_or_municipality', '').strip()
        preferred_language = data.get('preferred_language', 'bn').strip().lower()
        ration_card_type = data.get('ration_card_type', '').strip()

        if not phone or len(phone) < 10:
            return Response(
                {"error": "Please provide a valid 10-digit mobile number.", "code": "INVALID_PHONE"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not full_name:
            return Response(
                {"error": "Please provide your full name.", "code": "NAME_REQUIRED"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password or len(password) < 6:
            return Response(
                {"error": "Password must be at least 6 characters long.", "code": "WEAK_PASSWORD"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user already exists
        user = User.objects.filter(username=phone).first()
        if user:
            return Response(
                {"error": "An account with this mobile number already exists. Please log in.", "code": "USER_EXISTS"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User.objects.create_user(
            username=phone,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create or update profile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.phone_number = phone
        profile.district = district
        profile.block_or_municipality = block_or_municipality
        profile.preferred_language = preferred_language if preferred_language in ['bn', 'hi', 'en'] else 'bn'
        profile.save()

        return Response({
            "success": True,
            "message": "Citizen registration successful! Welcome to NyayaSetu AI.",
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": f"{user.first_name} {user.last_name}".strip() or full_name,
                "phone": profile.phone_number,
                "district": profile.district,
                "block": profile.block_or_municipality,
                "preferred_language": profile.preferred_language
            }
        }, status=status.HTTP_201_CREATED)


class CitizenLoginAPIView(APIView):
    """Citizen login using phone/username and password"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        identifier = request.data.get('identifier', '').strip().replace(' ', '').replace('+91', '')
        password = request.data.get('password', '')

        if not identifier or not password:
            return Response(
                {"error": "Please provide mobile number and password.", "code": "CREDENTIALS_MISSING"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try authenticating directly or by username
        user = authenticate(request, username=identifier, password=password)
        profile = None
        if not user:
            # Check if username exists by phone
            profile = UserProfile.objects.select_related('user').filter(phone_number=identifier).first()
            if profile and profile.user:
                user = authenticate(request, username=profile.user.username, password=password)

        if not user:
            return Response(
                {"error": "Invalid mobile number or password. Please verify and try again.", "code": "INVALID_CREDENTIALS"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not profile:
            profile = getattr(user, 'profile', None)
            if not profile:
                profile, _ = UserProfile.objects.get_or_create(user=user)

        return Response({
            "success": True,
            "message": "Login successful!",
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": f"{user.first_name} {user.last_name}".strip() or user.username,
                "phone": profile.phone_number or user.username,
                "district": profile.district,
                "block": profile.block_or_municipality,
                "preferred_language": profile.preferred_language
            }
        })


class SendOTPAPIView(APIView):
    """Generate and send a 6-digit OTP to citizen's mobile number"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get('phone', '').strip().replace(' ', '').replace('+91', '')
        if not phone or len(phone) < 10:
            return Response(
                {"error": "Please enter a valid 10-digit mobile number.", "code": "INVALID_PHONE"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Simulated OTP for instant testing, also accepts standard 123456
        otp = str(random.randint(100000, 999999))
        cache.set(f'otp:{phone}', otp, timeout=300)
        OTP_STORE[phone] = otp  # in-memory mirror

        return Response({
            "success": True,
            "message": f"OTP sent to +91 {phone[-10:]}. (Demo code: {otp} or standard demo 123456)",
            "demo_otp": otp,
            "expires_in_seconds": 300
        })


class VerifyOTPAPIView(APIView):
    """Verify citizen OTP and authenticate/create profile"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get('phone', '').strip().replace(' ', '').replace('+91', '')
        otp = request.data.get('otp', '').strip()

        if not phone or not otp:
            return Response(
                {"error": "Mobile number and OTP are required.", "code": "DATA_MISSING"},
                status=status.HTTP_400_BAD_REQUEST
            )

        stored_otp = cache.get(f'otp:{phone}') or OTP_STORE.get(phone)
        # Accept generated OTP or universal demo OTP 123456
        if otp != stored_otp and otp != "123456":
            return Response(
                {"error": "Incorrect OTP entered. Please try again or use demo code 123456.", "code": "INVALID_OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # OTP is valid! Find or create citizen user
        user, created = User.objects.get_or_create(username=phone)
        if created:
            user.set_unusable_password()
            user.first_name = f"Citizen"
            user.last_name = phone[-4:]
            user.save()

        profile, _ = UserProfile.objects.get_or_create(user=user)
        if not profile.phone_number:
            profile.phone_number = phone
            profile.save()

        # Clear OTP
        if phone in OTP_STORE:
            del OTP_STORE[phone]
        cache.delete(f'otp:{phone}')

        return Response({
            "success": True,
            "message": "OTP verification successful! Logged in.",
            "is_new_user": created,
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
                "phone": profile.phone_number or phone,
                "district": profile.district or "Kolkata",
                "block": profile.block_or_municipality or "",
                "preferred_language": profile.preferred_language or "bn"
            }
        })
