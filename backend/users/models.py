from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and returns a passive user by default.
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role="passive_user")
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and returns a user with the admin role.
        """
        user = self.create_user(username, email, password)
        user.role = "admin"
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    ROLES = (
        ('admin', 'Admin'),
        ('active_user', 'Active User'),
        ('passive_user', 'Passive User'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLES, default='passive_user')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    last_login = None
