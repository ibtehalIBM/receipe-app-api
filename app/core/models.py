"""
Database Models
"""

from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    """Manager for users."""
    def create_user(self,email,password=None,**extr_fields):
        """Create, Save, Return a new user."""
        user = self.model(email=email,**extr_fields)
        user.set_password(password)
        user.save()

class User(AbstractBaseUser, PermissionsMixin):
    """user in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME = email
