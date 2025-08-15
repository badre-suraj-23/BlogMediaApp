import logging
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

logger = logging.getLogger(__name__)

def get_user_from_jwt_token(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        logger.debug(f"Decoded user_id from token: {user_id}")
        user = User.objects.get(id=user_id)
        return user
    except TokenError as e:
        logger.warning(f"Invalid token: {e}")
    except User.DoesNotExist:
        logger.warning(f"User not found for token")
    return None
