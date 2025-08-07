# utils.py (photoapp ke andar banao)

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

def get_user_from_jwt_token(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)
        return user
    except (TokenError, User.DoesNotExist):
        return None
