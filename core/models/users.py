from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from ..managers import CustomUserManager

from django.db.models.signals import post_migrate
from django.dispatch import receiver

# 1. MODEL: CustomUser
class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé avec email comme identifiant principal.
    """
    username = None  # Désactive le champ username
    email = models.EmailField(
        _('Adresse email'),
        unique=True,
        error_messages={
            'unique': _("Un utilisateur avec cette adresse email existe déjà."),
        }
    )
    first_name = models.CharField(_('Prénom'), max_length=150)
    last_name = models.CharField(_('Nom'), max_length=150)
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name=_("Photo de profil"),
        help_text=_("Format recommandé : 200x200px, max 2MB")
    )
    role = models.CharField(
        verbose_name=_("Rôle"),
        max_length=50, 
        choices=[
            ('superadmin', _('Super Administrateur')),
            ('admin', _('Administrateur')),
            ('finance', _('Responsable Financier')),
            ('communication', _('Responsable Communication')),
            ('moderator', _('Modérateur')),
            ('member', _('Membre Adhérent')),
            ('donor', _('Donateur')),
            ('visitor', _('Visiteur')),
        ],
        default='visitor'
    )
    
    # Add related_name to fix the clash
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groupes'),
        blank=True,
        related_name='custom_user_set',
        help_text=_('Les groupes auxquels appartient cet utilisateur.')
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions utilisateur'),
        blank=True,
        related_name='custom_user_set',
        help_text=_('Permissions spécifiques pour cet utilisateur.')
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.get_full_name() or self.email
    
    def get_full_name(self):
        """
        Retourne le nom complet de l'utilisateur.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """
        Retourne le prénom de l'utilisateur.
        """
        return self.first_name

    def get_avatar_url(self):
        """
        Retourne l'URL de l'avatar ou l'avatar par défaut
        """
        if self.avatar:
            return self.avatar.url
        return (
            '<div class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 '
            'flex items-center justify-center">'
            '<svg class="w-5 h-5 text-gray-500 dark:text-gray-400" '
            'aria-hidden="true" xmlns="http://www.w3.org/2000/svg" '
            'fill="currentColor" viewBox="0 0 20 20">'
            '<path d="M10 0a10 10 0 1 0 10 10A10.011 10.011 0 0 0 10 0Zm0 5a3 3 0 1 1 '
            '0 6 3 3 0 0 1 0-6Zm0 13a8.949 8.949 0 0 1-4.951-1.488A3.987 3.987 0 0 1 '
            '9 13h2a3.987 3.987 0 0 1 3.951 3.512A8.949 8.949 0 0 1 10 18Z"/>'
            '</svg></div>'
        )
    
    def can_change_role(self, user=None):
        """
        Vérifie si l'utilisateur peut modifier les rôles.
        Args:
            user: L'utilisateur qui tente de faire la modification
        Returns:
            bool: True si l'utilisateur peut modifier les rôles
        """
        # Si pas d'utilisateur spécifié, autoriser uniquement les superusers
        if user is None:
            return self.is_superuser
        
        # Les superusers peuvent toujours modifier
        if user.is_superuser:
            return True
            
        # L'utilisateur ne peut pas modifier son propre rôle
        if self.pk == user.pk and not user.is_superuser:
            return False
            
        return False

    def clean(self):
        """Validation personnalisée pour les modifications de rôle"""
        super().clean()
        
        if self.pk:
            original = CustomUser.objects.get(pk=self.pk)
            if original.role != self.role:
                # La validation sera faite au niveau de la vue/form
                self._role_changed = True
    
    class Meta:
        verbose_name = _("utilisateur")
        verbose_name_plural = _("utilisateurs")
        ordering = ['email']

# Création automatique des groupes avec permissions
def create_user_groups():
    """
    Création des groupes d’utilisateurs et assignation des permissions spécifiques.
    """
    roles = [
        ('Super Administrateur', []),
        ('Administrateur', []),
        ('Responsable Financier', []),
        ('Responsable Communication', []),
        ('Modérateur', []),
        ('Membre Adhérent', []),
        ('Donateur', []),
        ('Visiteur', []),
    ]
    
    for role_name, permissions in roles:
        group, created = Group.objects.get_or_create(name=role_name)
        if created:
            for perm in permissions:
                permission = Permission.objects.get(codename=perm)
                group.permissions.add(permission)

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    if sender.name == 'core':  # Changed from 'myapp' to 'core'
        create_user_groups()
