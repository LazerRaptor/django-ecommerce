from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import IntegrityError



class UserManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        if not email and password:
            raise ValidationError(_(f'Fields "email" and "password" cannot be empty'))
        email = self.normalize_email(email)
        try:
            user = self.model(email=email, **other_fields)
            user.set_password(password)
            user.save()
        except IntegrityError:
            raise IntegrityError(_(f'User with email {email} already exists'))

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_superuser') is not True:
            raise ValidationError(_('Superuser must have is_superuser set to True'))
        
        self.create_user(email, password, **other_fields)


