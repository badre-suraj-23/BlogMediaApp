from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, LogoutView

app_name = 'photoapp'

urlpatterns = [
    # ✅ Register via Email
    path('api/register/', RegisterView.as_view(), name='jwt_register'),

    # ✅ Login via Email
    path('api/login/', LoginView.as_view(), name='jwt_login'),

    # ✅ Refresh JWT Token
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Logout (Blacklist Refresh Token)
    path('api/logout/', LogoutView.as_view(), name='jwt_logout'),
]
