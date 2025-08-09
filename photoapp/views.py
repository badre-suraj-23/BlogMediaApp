from django.shortcuts import render, redirect
from.form import ChildImageForm, ChildVideoForm,BlogPostForm
from .models import ChildImage, ChildVideo,BlogPost
from django.contrib import messages
import json,requests
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
import json
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .utils import get_user_from_jwt_token  



# IMAGE LIST with Pagination
def image_list(request):
    images = ChildImage.objects.all().order_by('-uploaded_at')
    paginator = Paginator(images, 8)  # Show 8 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'photoapp/image_list.html', {'page_obj': page_obj})

# IMAGE UPLOAD
def image_upload(request):
    if request.method == 'POST':
        form = ChildImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Image uploaded successfully!")
            return redirect('photoapp:image-list')
    else:
        form = ChildImageForm()
    return render(request, 'photoapp/image_form.html', {'form': form})

# VIDEO LIST with Pagination
def video_list(request):
    videos = ChildVideo.objects.all().order_by('-uploaded_at')
    paginator = Paginator(videos, 6)  # Show 6 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'photoapp/video_list.html', {'page_obj': page_obj})

# VIDEO UPLOAD
def video_upload(request):
    if request.method == 'POST':
        form = ChildVideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video uploaded successfully!')
            return redirect('photoapp:video-list')
    else:
        form = ChildVideoForm()
    return render(request, 'photoapp/video_form.html', {'form': form})

# IMAGE UPDATE
def image_update(request, pk):
    image = get_object_or_404(ChildImage, pk=pk)
    form = ChildImageForm(request.POST or None, request.FILES or None, instance=image)
    if form.is_valid():
        form.save()
        messages.success(request, "✏️ Image updated successfully!")
        return redirect('photoapp:image-list')
    return render(request, 'photoapp/image_form.html', {'form': form})

# IMAGE DELETE
def image_delete(request, pk):
    image = get_object_or_404(ChildImage, pk=pk)
    if request.method == 'POST':
        image.delete()
        messages.success(request, "🗑️ Image deleted successfully!")
        return redirect('photoapp:image-list')
    return render(request, 'photoapp/confirm_delete.html', {'object': image, 'type': 'Image'})

# VIDEO UPDATE
def video_update(request, pk):
    video = get_object_or_404(ChildVideo, pk=pk)
    form = ChildVideoForm(request.POST or None, request.FILES or None, instance=video)
    if form.is_valid():
        form.save()
        messages.success(request, 'Video updated successfully!')
        return redirect('photoapp:video-list')
    return render(request, 'photoapp/video_form.html', {'form': form})

# VIDEO DELETE
def video_delete(request, pk):
    video = get_object_or_404(ChildVideo, pk=pk)
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video deleted successfully!')
        return redirect('photoapp:video-list')
    return render(request, 'photoapp/confirm_delete.html', {'object': video, 'type': 'Video'})

# Blog 

def blog_created(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            token = request.session.get('access')
            user = get_user_from_jwt_token(token)  # ✅ Get user from token
            if user is None:
                return redirect('photoapp:login')

            blog = form.save(commit=False)
            blog.user = user  # ✅ set user manually
            blog.save()
            messages.success(request, '✅ Blog created successfully!')
            return redirect('photoapp:blog_list')
    else:
        form = BlogPostForm()
    
    return render(request, 'photoapp/blog_form.html', {'form': form})

        
def blog_list(request):
    blogs = BlogPost.objects.all().order_by('-created_at')  # Latest first
    paginator = Paginator(blogs, 5)  # 5 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'photoapp/blog_list.html', {'page_obj': page_obj})



# @login_required
def edit_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    #  Check if current user is the owner
    if blog.user != request.user:
        messages.error(request, "You are not authorized to edit this blog.")
        return redirect('photoapp:blog_list')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('photoapp:blog_list')
    else:
        form = BlogPostForm(instance=blog)

    return render(request, 'photoapp/blog_form.html', {'form': form})


# @login_required
def delete_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    #  Only the creator can delete
    if blog.user != request.user:
        messages.error(request, "You are not authorized to delete this blog.")
        return redirect('blog_list')

    blog.delete()
    messages.success(request, "Blog deleted successfully.")
    return redirect('blog_list')



def home(request):
    blogs = BlogPost.objects.order_by('-created_at')  # Show newest first
    return render(request, 'photoapp/home.html', {'blogs': blogs})

def view_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    blog.view_count += 1
    blog.save()
    return render(request, 'photoapp/blog_detail.html', {'blog': blog})



# @login_required
def like_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    if request.user in blog.likes.all():
        blog.likes.remove(request.user)  # Unlike
    else:
        blog.likes.add(request.user)     # Like

    return HttpResponseRedirect(reverse('photoapp:view_blog', args=[pk]))

import requests
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from decouple import config

# Load API base URL from .env
API_BASE_URL = config('API_BASE_URL')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'photoapp/login.html', {'error': 'Username and password are required.'})

        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(
                f'{API_BASE_URL}/login/',
                data=json.dumps({'username': username, 'password': password}),
                headers=headers
            )
        except requests.RequestException as e:
            return render(request, 'photoapp/login.html', {'error': f'⚠ Server not reachable: {e}'})

        print("DEBUG LOGIN:", response.status_code, response.text)  # Debugging

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
                error_msg = response.json().get('detail') or 'Invalid credentials'
            except ValueError:
                error_msg = 'Login failed. Invalid server response.'
            return render(request, 'photoapp/login.html', {'error': error_msg})

    return render(request, 'photoapp/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'photoapp/register.html', {'error': 'Username and password are required.'})

        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(
                f'{API_BASE_URL}/register/',
                data=json.dumps({'username': username, 'password': password}),
                headers=headers
            )
        except requests.RequestException as e:
            return render(request, 'photoapp/register.html', {'error': f'⚠ Server not reachable: {e}'})

        print("DEBUG REGISTER:", response.status_code, response.text)  # Debugging

        if response.status_code == 201:
            messages.success(request, '✅ Account created successfully! Please log in.')
            return redirect('photoapp:login')
        else:
            try:
                data = response.json()
                error_msg = data.get('error') or data.get('detail') or '❌ Registration failed.'
            except ValueError:
                error_msg = '❌ Invalid server response.'
            return render(request, 'photoapp/register.html', {'error': error_msg})

    return render(request, 'photoapp/register.html')


def logout_view(request):
    refresh = request.session.get('refresh')
    headers = {'Content-Type': 'application/json'}

    if refresh:
        try:
            requests.post(
                f'{API_BASE_URL}/logout/',
                data=json.dumps({'refresh': refresh}),
                headers=headers
            )
        except requests.RequestException:
            pass  # Ignore errors during logout

    request.session.flush()
    messages.success(request, '👋 Logged out successfully.')
    return redirect('photoapp:login')
