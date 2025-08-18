from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .api_views import RegisterView, LoginView, LogoutView

app_name = 'photoapp'

urlpatterns = [
    # Home + Blogs
    path('', views.home_view, name='home'),
    path('blog/<int:pk>/', views.view_blog, name='view_blog'),
    path('blog/<int:pk>/like/', views.like_blog, name='like_blog'),
    path('blog/', views.blog_created, name='blog'),
    path('blog_list/', views.blog_list, name='blog_list'),
    path('blog/edit/<int:pk>/', views.edit_blog, name='edit_blog'),
    path('blog/delete/<int:pk>/', views.delete_blog, name='delete_blog'),

    # Images + Videos
    path('image-list/', views.image_list, name='image-list'),
    path('images/upload/', views.image_upload, name='image-upload'),
    path('videos/', views.video_list, name='video-list'),
    path('videos/upload/', views.video_upload, name='video-upload'),
    path('images/<int:pk>/edit/', views.image_update, name='image-update'),
    path('images/<int:pk>/delete/', views.image_delete, name='image-delete'),
    path('videos/<int:pk>/edit/', views.video_update, name='video-update'),
    path('videos/<int:pk>/delete/', views.video_delete, name='video-delete'),

    # Session-based Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # JWT Auth
    path('api/register/', RegisterView.as_view(), name='jwt_register'),
    path('api/login/', LoginView.as_view(), name='jwt_login'),
    path('api/logout/', LogoutView.as_view(), name='jwt_logout'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('login_session_save/', views.login_session_save, name='save_token_session'),
]
