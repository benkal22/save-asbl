from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Manager personnalisé pour le modèle CustomUser, permettant la création d'utilisateurs et de super-utilisateurs.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('L\'adresse email est obligatoire'))
        
        # Force le rôle 'visitor' pour tous les nouveaux utilisateurs
        extra_fields.setdefault('role', 'visitor')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'superadmin')  # Force le rôle 'superadmin' pour les superusers

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Le superuser doit avoir is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Le superuser doit avoir is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)
