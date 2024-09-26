from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post,Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)