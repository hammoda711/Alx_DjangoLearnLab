from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Like, Post,Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)