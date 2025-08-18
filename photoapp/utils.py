import logging
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

logger = logging.getLogger(__name__)


def get_user_from_jwt_token(token: str):
    """
    Decode a JWT access token and return the corresponding User instance.
    Returns None if token is invalid, expired, or user does not exist.
    """
    if not token:
        logger.debug("⚠️ No token provided to decode.")
        return None

    try:
        access_token = AccessToken(token)
        user_id = access_token.get("user_id") 

        if not user_id:
            logger.debug("⚠️ Token decoded but 'user_id' not found in payload.")
            return None

        user = User.objects.filter(id=user_id).first()
        if not user:
            logger.debug(f"⚠️ No user found with id {user_id}.")
            return None

        logger.debug(f"✅ Successfully authenticated user '{user.username}' from token.")
        return user

    except TokenError as e:
        logger.warning(f"⚠️ Invalid or expired token: {e}")
    except Exception as e:
        logger.error(f"❌ Unexpected error decoding token: {e}")

    return None


def get_user_from_request(request):
    """
    Extract JWT token from a request and return the corresponding User.
    Search order:
      1. 'Authorization: Bearer <token>' header
      2. Session key 'access'
    Returns None if no valid token found.
    """
    token = None

    # 1. Try Authorization header
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        logger.debug("🔑 Token found in Authorization header.")

    # 2. Fallback: session token
    if not token:
        token = request.session.get("access")  
        if token:
            logger.debug("🔑 Token found in session storage.")

    if not token:
        logger.debug("⚠️ No token found in request (header/session).")
        return None

    return get_user_from_jwt_token(token)
