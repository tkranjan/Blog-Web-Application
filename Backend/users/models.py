from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin','Admin'),
        ('user','User'),
    )

    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='user') 

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=30)
    
    last_name = models.CharField(max_length=30)

    bio = models.TextField(
        max_length= 500,
        blank= True
    )

    profile_picture = models.ImageField(
        upload_to='profile_picture/',
        null = True,
        blank = True
    )

    is_blocked = models.BooleanField(
        default = False
    )

    last_seen = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.username