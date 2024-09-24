from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=200)
    profile_picture = models.ImageField(blank=True,null=True)
    followers = models.ManyToManyField("self", symmetrical=False,related_name='following',blank=True)
    