# # import jwt
# # from django .shortcuts import  redirect
# # from django.conf import settings
# # from django.contrib.auth.models import User
# # from rest_framework_simplejwt.tokens import AccessToken

# # EXEMPT_URLS = [
# #     '/login/',
# #     '/register/',
# #     '/admin/',
# #     '/static/',
# #     '/media/',
# #     '/api/auth/login/',
# #     '/api/auth/register/',
# #     '/api/auth/logout/',
# #     '/api/auth/refresh/',
# # ]

# # class LoginRequiredMiddleware:
# #     def __init__(self, get_response):
# #         self.get_response = get_response

# #     def __call__(self, request):
# #         path = request.path_info

# #         access_token = request.session.get('access')

# #         if access_token:
# #             try:
# #                 token = AccessToken(access_token)
# #                 user_id = token['user_id']
# #                 user = User.objects.get(id=user_id)
# #                 request.user = user  # ✅ Django को user set करना जरूरी है
# #             except Exception as e:
# #                 request.user = None

# #         if not request.user or not request.user.is_authenticated:
# #             if not any(path.startswith(url) for url in EXEMPT_URLS):
# #                 return redirect(f"{settings.LOGIN_URL}?next={request.path}")

# #         return self.get_response(request)


# # photoapp/middleware.py

# from django.shortcuts import redirect
# from django.conf import settings
# from django.contrib.auth.models import User, AnonymousUser
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
#                 request.user = user
#             except Exception as e:
#                 request.user = AnonymousUser()  # ✅ instead of None
#         else:
#             request.user = AnonymousUser()  # ✅ instead of None

#         if not request.user.is_authenticated:
#             if not any(path.startswith(url) for url in EXEMPT_URLS):
#                 return redirect(f"{settings.LOGIN_URL}?next={request.path}")

#         return self.get_response(request)

# middlewares.py (photoapp ke andar)

from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User, AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

# जिन URLs पर login check नहीं करना है
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

        # DEBUG: Render logs me print hoga
        print(f"[Middleware] Request Path: {path}")

        access_token = request.session.get('access')

        # Token से user निकालना
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
            print("[Middleware] No access token in session")
            request.user = AnonymousUser()

        # अगर user authenticated नहीं है
        if not request.user.is_authenticated:
            # ✅ API calls को कभी redirect मत करो, JSON error दो
            if path.startswith('/api/'):
                return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)

            # ✅ बाकी pages पर login check
            if not any(path.startswith(url) for url in EXEMPT_URLS):
                print(f"[Middleware] Redirecting to login for path: {path}")
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        return self.get_response(request)
