# photoapp/middleware.py

from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User, AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

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

        print(f"[Middleware] Request Path: {path}")

        # 1️⃣ Try session token first
        access_token = request.session.get('access')

        # 2️⃣ Fallback: Try Authorization header
        if not access_token:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                access_token = auth_header.split(' ')[1]

        # 3️⃣ Decode JWT token if available
        if access_token:
            try:
                token = AccessToken(access_token)
                user_id = token['user_id']
                user = User.objects.get(id=user_id)
                request.user = user
                print(f"[Middleware] Authenticated user: {user.username}")
            except TokenError as e:
                print(f"[Middleware] Token error: {e}")
                request.user = AnonymousUser()
            except User.DoesNotExist:
                print("[Middleware] User not found for token")
                request.user = AnonymousUser()
            except Exception as e:
                print(f"[Middleware] Unknown error: {e}")
                request.user = AnonymousUser()
        else:
            print("[Middleware] No access token found")
            request.user = AnonymousUser()

        # 4️⃣ Handle unauthenticated users
        if not request.user.is_authenticated:
            if path.startswith('/api/'):
                return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

            if not any(path.startswith(url) for url in EXEMPT_URLS):
                print(f"[Middleware] Redirecting to login for path: {path}")
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        return self.get_response(request)
