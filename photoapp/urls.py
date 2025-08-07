from django.urls import path
from . import views
from .views import blog_created

app_name = 'photoapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<int:pk>/', views.view_blog, name='view_blog'),
    path('blog/<int:pk>/like/', views.like_blog, name='like_blog'),
    path('blog/', blog_created, name='blog'),
    path('blog_list/', views.blog_list, name='blog_list'),
    path('blog/edit/<int:pk>/', views.edit_blog, name='edit_blog'),
    path('blog/delete/<int:pk>/', views.delete_blog, name='delete_blog'),

    path('image-list', views.image_list, name='image-list'),
    path('images/upload/', views.image_upload, name='image-upload'),
    path('videos/', views.video_list, name='video-list'),
    path('videos/upload/', views.video_upload, name='video-upload'),
    path('images/<int:pk>/edit/', views.image_update, name='image-update'),
    path('images/<int:pk>/delete/', views.image_delete, name='image-delete'),
    path('videos/<int:pk>/edit/', views.video_update, name='video-update'),
    path('videos/<int:pk>/delete/', views.video_delete, name='video-delete'),

    # API Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
