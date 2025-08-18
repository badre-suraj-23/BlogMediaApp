from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse

from .utils import get_user_from_request  # ✅ JWT decode helper


# ✅ Frontend URLs exempt from login
EXEMPT_URLS = (
    '/login/',
    '/register/',
    '/admin/',
    '/static/',
    '/media/',
    '/favicon.ico',
    '/login_session_save/',
)

# ✅ API URLs exempt from JWT check
API_EXEMPT_URLS = (
    '/api/login/',
    '/api/register/',
    '/api/logout/',
    '/api/refresh/',
)


class LoginRequiredMiddleware:
    """Custom middleware to protect API + frontend routes with JWT"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        #  JWT decode user
        user = get_user_from_request(request)
        request.user = user if user else AnonymousUser()

        #  API request authentication
        if path.startswith('/api/'):
            if not any(path.startswith(url) for url in API_EXEMPT_URLS):
                if not request.user.is_authenticated:
                    return JsonResponse({'error': 'Authentication required'}, status=401)

        #  Frontend request authentication
        else:
            if not any(path.startswith(url) for url in EXEMPT_URLS):
                if not request.user.is_authenticated:
                    return redirect(f"{settings.LOGIN_URL}?next={path}")

        return self.get_response(request)
