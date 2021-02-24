from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager



class CustomUser(AbstractUser):
    username = models.CharField(_('username'), max_length=120, blank=True, default="")
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(_('user is active'), default=True)
    is_admin = models.BooleanField(_('user is admin'), default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email