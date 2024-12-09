from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('active', 'Active User'),
        ('passive', 'Passive User'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='passive',  # Default role is 'passive user'
    )
