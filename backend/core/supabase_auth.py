"""
Supabase JWT Authentication for Django REST Framework.
Validates the Bearer token issued by Supabase Auth and binds it to a Django user.
"""
import jwt
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

logger = logging.getLogger(__name__)
User = get_user_model()


class SupabaseAuthentication(authentication.BaseAuthentication):
    """
    Authenticates requests using Supabase JWT Access Tokens.
    Expects header: Authorization: Bearer <supabase_jwt_token>
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        token = parts[1]
        jwt_secret = getattr(settings, "SUPABASE_JWT_SECRET", None)

        try:
            # If JWT secret is configured, verify HMAC signature
            if jwt_secret and jwt_secret.strip():
                payload = jwt.decode(
                    token,
                    jwt_secret,
                    algorithms=["HS256"],
                    audience="authenticated"
                )
            else:
                # In early development if secret is not set, decode without verify
                logger.warning("SUPABASE_JWT_SECRET not set. Decoding JWT without signature verification.")
                payload = jwt.decode(token, options={"verify_signature": False})

            user_id = payload.get("sub")
            if not user_id:
                raise exceptions.AuthenticationFailed("Invalid token payload: missing sub (user ID)")

            email = payload.get("email", f"{user_id}@supabase.user")
            
            # Sync or create local Django User for this Supabase user
            username = email.split("@")[0] + "_" + user_id[:6]
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={"email": email}
            )

            # Attach Supabase metadata to request
            request.supabase_user = payload
            return (user, payload)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Supabase token has expired.")
        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f"Invalid Supabase token: {str(e)}")
        except Exception as e:
            logger.error(f"Supabase auth error: {str(e)}")
            raise exceptions.AuthenticationFailed(f"Authentication failed: {str(e)}")
