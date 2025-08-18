from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .form import ChildImageForm, ChildVideoForm, BlogPostForm
from .models import ChildImage, ChildVideo, BlogPost
from .utils import get_user_from_jwt_token  

import requests, json
from decouple import config


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
import json

# Load API base URL from .env
API_BASE_URL = config('API_BASE_URL')


# ================================
# IMAGE VIEWS with JWT Auth
# ================================

def image_upload(request):
    token = request.session.get('access')
    user = get_user_from_jwt_token(token)
    if user is None:
        messages.warning(request, "⚠ Please log in to upload an image.")
        return redirect('photoapp:login')

    if request.method == 'POST':
        form = ChildImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = user 
            image.save()
            messages.success(request, "✅ Image uploaded successfully!")
            return redirect('photoapp:image-list')
    else:
        form = ChildImageForm()
    return render(request, 'photoapp/image_form.html', {'form': form})


def image_update(request, pk):
    token = request.session.get('access')
    user = get_user_from_jwt_token(token)
    if user is None:
        return redirect('photoapp:login')

    image = get_object_or_404(ChildImage, pk=pk)
    if image.user != user:  
        messages.error(request, "🚫 You are not authorized to edit this image.")
        return redirect('photoapp:image-list')

    form = ChildImageForm(request.POST or None, request.FILES or None, instance=image)
    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Image updated successfully!")
        return redirect('photoapp:image-list')
    return render(request, 'photoapp/image_form.html', {'form': form})


def image_delete(request, pk):
    token = request.session.get('access')
    user = get_user_from_jwt_token(token)
    if user is None:
        return redirect('photoapp:login')

    image = get_object_or_404(ChildImage, pk=pk)
    if image.user != user:   
        messages.error(request, "🚫 You are not authorized to delete this image.")
        return redirect('photoapp:image-list')

    if request.method == 'POST':
        image.delete()
        messages.success(request, "🗑️ Image deleted successfully!")
        return redirect('photoapp:image-list')
    return render(request, 'photoapp/confirm_delete.html', {'object': image, 'type': 'Image'})

def image_list(request):
    images = ChildImage.objects.all().order_by('-uploaded_at')
    paginator = Paginator(images, 8)  # 8 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'photoapp/image_list.html', {'page_obj': page_obj})
# ================================
# VIDEO VIEWS with JWT Auth
# ================================

def video_upload(request):
    token = request.session.get('access')
    user = get_user_from_jwt_token(token)
    if user is None:
        messages.warning(request, "⚠ Please log in to upload a video.")
        return redirect('photoapp:login')

    if request.method == 'POST':
        form = ChildVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = user  
            video.save()
            messages.success(request, '🎥 Video uploaded successfully!')
            return redirect('photoapp:video-list')
    else:
        form = ChildVideoForm()
    return render(request, 'photoapp/video_form.html', {'form': form})


def video_update(request, pk):
    token = request.session.get('access')
    user = get_user_from_jwt_token(token)
    if user is None:
        return redirect('photoapp:login')

    video = get_object_or_404(ChildVideo, pk=pk)
    if video.user != user:   
        messages.error(request, "🚫 You are not authorized to edit this video.")
        return redirect('photoapp:video-list')

    form = ChildVideoForm(request.POST or None, request.FILES or None, instance=video)
    if form.is_valid():
        form.save()
        messages.success(request, '✏️ Video updated successfully!')
        return redirect('photoapp:video-list')
    return render(request, 'photoapp/video_form.html', {'form': form})


def video_delete(request, pk):
    token = request.session.get('access')
    user = get_user_from_jwt_token(token)
    if user is None:
        return redirect('photoapp:login')

    video = get_object_or_404(ChildVideo, pk=pk)
    if video.user != user:  
        messages.error(request, "🚫 You are not authorized to delete this video.")
        return redirect('photoapp:video-list')

    if request.method == 'POST':
        video.delete()
        messages.success(request, '🗑️ Video deleted successfully!')
        return redirect('photoapp:video-list')
    return render(request, 'photoapp/confirm_delete.html', {'object': video, 'type': 'Video'})

def video_list(request):
    videos = ChildVideo.objects.all().order_by('-uploaded_at')
    paginator = Paginator(videos, 6)  # 6 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'photoapp/video_list.html', {'page_obj': page_obj})
# ================================
# BLOG VIEWS with JWT Auth
# ================================

def blog_created(request):
    token = request.session.get('access')
    user = get_user_from_jwt_token(token)
    if user is None:
        return redirect('photoapp:login')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = user
            blog.save()
            messages.success(request, '✅ Blog created successfully!')
            return redirect('photoapp:home')
    else:
        form = BlogPostForm()
    
    return render(request, 'photoapp/blog_form.html', {'form': form})


def edit_blog(request, pk):
    token = request.session.get('access')
    user = get_user_from_jwt_token(token)
    if user is None:
        return redirect('photoapp:login')

    blog = get_object_or_404(BlogPost, pk=pk)
    if blog.user != user:
        messages.error(request, "🚫 You are not authorized to edit this blog.")
        return redirect('photoapp:blog_list')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Blog updated successfully!")
            return redirect('photoapp:blog_list')
    else:
        form = BlogPostForm(instance=blog)

    return render(request, 'photoapp/blog_form.html', {'form': form})


def delete_blog(request, pk):
    token = request.session.get('access')
    user = get_user_from_jwt_token(token)
    if user is None:
        return redirect('photoapp:login')

    blog = get_object_or_404(BlogPost, pk=pk)
    if blog.user != user:
        messages.error(request, "🚫 You are not authorized to delete this blog.")
        return redirect('photoapp:blog_list')

    blog.delete()
    messages.success(request, "🗑️ Blog deleted successfully.")
    return redirect('photoapp:blog_list')

def blog_list(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    paginator = Paginator(blogs, 5)  # 5 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'photoapp/blog_list.html', {'page_obj': page_obj})



def home_view(request):
    access_token = request.session.get('access')  
    if not access_token:
        messages.warning(request, '⚠ Please log in to continue.')
        return redirect('photoapp:login')

    blogs = BlogPost.objects.order_by('-created_at')
    return render(request, 'photoapp/home.html', {'blogs': blogs})



def view_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    blog.view_count += 1
    blog.save()
    return render(request, 'photoapp/blog_detail.html', {'blog': blog})


def like_blog(request, pk):
    token = request.session.get('access')
    user = get_user_from_jwt_token(token)
    if user is None:
        return redirect('photoapp:login')

    blog = get_object_or_404(BlogPost, pk=pk)

    if user in blog.likes.all():
        blog.likes.remove(user)  # Unlike
    else:
        blog.likes.add(user)     # Like

    return HttpResponseRedirect(reverse('photoapp:view_blog', args=[pk]))


# API_BASE_URL = "http://127.0.0.1:8000/api"

# API_BASE_URL = "http://127.0.0.1:8000/api" 
# API_BASE_URL="https://blogmedia.onrender.com/api"

# ========================
# Register View (Email-based)
# ========================
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')      
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'photoapp/register.html', {'error': 'Email and password are required.'})

        headers = {'Content-Type': 'application/json'}
        payload = {'email': email, 'password': password}

        try:
            response = requests.post(f'{API_BASE_URL}/register/', data=json.dumps(payload), headers=headers)
        except requests.RequestException as e:
            return render(request, 'photoapp/register.html', {'error': f'⚠ Server not reachable: {e}'})

        if response.status_code == 201:
            messages.success(request, '✅ Account created successfully! Please log in.')
            return redirect('photoapp:login')
        else:
            try:
                error_msg = response.json().get('error', '❌ Registration failed.')
            except ValueError:
                error_msg = '❌ Invalid server response.'
            return render(request, 'photoapp/register.html', {'error': error_msg})

    return render(request, 'photoapp/register.html')


# ========================
# Login View (Email-based)
# ========================
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'photoapp/login.html', {'error': 'Email and password are required.'})

        headers = {'Content-Type': 'application/json'}
        payload = {'email': email, 'password': password}

        try:
            response = requests.post(f'{API_BASE_URL}/login/', data=json.dumps(payload), headers=headers)
        except requests.RequestException as e:
            return render(request, 'photoapp/login.html', {'error': f'⚠ Server not reachable: {e}'})

        if response.status_code == 200:
            try:
                tokens = response.json()
                request.session['access'] = tokens.get('access')
                request.session['refresh'] = tokens.get('refresh')
                
                messages.success(request, '🎉 Login successful!')
                return redirect('photoapp:home')
            except ValueError:
                return render(request, 'photoapp/login.html', {'error': 'Invalid JSON from server.'})
        else:
            try:
                error_msg = response.json().get('error', 'Invalid credentials')
            except ValueError:
                error_msg = 'Login failed. Invalid server response.'
            return render(request, 'photoapp/login.html', {'error': error_msg})

    return render(request, 'photoapp/login.html')


# ========================
# Logout View (Blacklist Refresh Token)
# ========================
def logout_view(request):
    refresh_token = request.session.get('refresh')
    if refresh_token:
        try:
            response = requests.post(
                f'{API_BASE_URL}/logout/',
                data=json.dumps({'refresh': refresh_token}),
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 205:
                messages.success(request, '✅ Logged out successfully.')
            else:
                messages.warning(request, '⚠ Logout failed on server, but session cleared.')
        except requests.RequestException:
            messages.warning(request, '⚠ Server not reachable during logout.')

    request.session.flush()  # Clear session
    return redirect('photoapp:login')


# photoapp/views.py


@csrf_exempt
def login_session_save(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            access_token = data.get("access")
            refresh_token = data.get("refresh")

            if not access_token:
                return JsonResponse({"error": "Access token missing"}, status=400)

            # JWT decode
            token = AccessToken(access_token)
            user_id = token["user_id"]
            user = User.objects.get(id=user_id)
            

            # Django session login
            login(request, user)

            #  FIX: save tokens in correct session keys
            request.session["access"] = access_token
            request.session["refresh"] = refresh_token

            return JsonResponse(
                {"status": "success", "user": user.username}, status=200
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)
