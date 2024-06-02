from django.contrib import admin
from .models import Message, Blog, BlogImage

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ("name", "email", "subject", "text", "datetime_created")
    

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    model = Blog
    list_display = ("title", "text", "author", "datetime_modified")
    

@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    model = BlogImage
    list_display = ("blog", "image")

    

    

