from django.contrib import admin
from.models import ChildImage,ChildVideo,BlogPost

# Register your models here.

@admin.register(ChildImage)
class ChildImageAdmin(admin.ModelAdmin):
    list_display = ['id','title','image','uploaded_at']


@admin.register(ChildVideo)
class ChildVideoAdmin(admin.ModelAdmin):
    list_display =  ['id','title','video','uploaded_at']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['blog_title', 'user', 'created_at','blog_content']
