# import jwt
# from django .shortcuts import  redirect
# from django.conf import settings
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import AccessToken

# EXEMPT_URLS = [
#     '/login/',
#     '/register/',
#     '/admin/',
#     '/static/',
#     '/media/',
#     '/api/auth/login/',
#     '/api/auth/register/',
#     '/api/auth/logout/',
#     '/api/auth/refresh/',
# ]

# class LoginRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         path = request.path_info

#         access_token = request.session.get('access')

#         if access_token:
#             try:
#                 token = AccessToken(access_token)
#                 user_id = token['user_id']
#                 user = User.objects.get(id=user_id)
#                 request.user = user  # ✅ Django को user set करना जरूरी है
#             except Exception as e:
#                 request.user = None

#         if not request.user or not request.user.is_authenticated:
#             if not any(path.startswith(url) for url in EXEMPT_URLS):
#                 return redirect(f"{settings.LOGIN_URL}?next={request.path}")

#         return self.get_response(request)


# photoapp/middleware.py

from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

EXEMPT_URLS = [
    '/login/',
    '/register/',
    '/admin/',
    '/static/',
    '/media/',
    '/api/auth/login/',
    '/api/auth/register/',
    '/api/auth/logout/',
    '/api/auth/refresh/',
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        access_token = request.session.get('access')

        if access_token:
            try:
                token = AccessToken(access_token)
                user_id = token['user_id']
                user = User.objects.get(id=user_id)
                request.user = user
            except Exception as e:
                request.user = AnonymousUser()  # ✅ instead of None
        else:
            request.user = AnonymousUser()  # ✅ instead of None

        if not request.user.is_authenticated:
            if not any(path.startswith(url) for url in EXEMPT_URLS):
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        return self.get_response(request)
