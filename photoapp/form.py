from django import forms
from .models import ChildImage, ChildVideo,BlogPost

class ChildImageForm(forms.ModelForm):
    class Meta:
        model = ChildImage
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter image title',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

class ChildVideoForm(forms.ModelForm):
    class Meta:
        model = ChildVideo
        fields = ['title', 'video']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter video title',
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }



class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        exclude = ['user', 'created_at', 'likes', 'view_count'] 
        widgets = {
            'blog_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blog title'
            }),
            'state': forms.Select(attrs={
                'class': 'form-select'
            }),
            'blog_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'blog_content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your blog content here...',
                'rows': 10
            }),
        }

