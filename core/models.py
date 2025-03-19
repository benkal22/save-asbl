from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .managers import CustomUserManager

from django.db.models.signals import post_migrate
from django.dispatch import receiver

# 1. MODEL: CustomUser
class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé avec email comme identifiant principal.
    """
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=50, 
        choices=[
            ('superadmin', 'Super Administrateur'),
            ('admin', 'Administrateur'),
            ('finance', 'Responsable Financier'),
            ('communication', 'Responsable Communication'),
            ('moderator', 'Modérateur'),
            ('member', 'Membre Adhérent'),
            ('donor', 'Donateur'),
            ('visitor', 'Visiteur'),
        ],
        default='visitor'
    )
    
    # Add related_name to fix the clash
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        help_text='Specific permissions for this user.'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

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

# 2. MODEL: Member
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils.timezone import now


class Member(models.Model):
    """
    Modèle représentant un membre de l'ASBL "SAVE Asbl".
    """

    # 🔹 Lien avec l'utilisateur Django
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="member_profile",
        verbose_name=_("Utilisateur associé")
    )

    # 🔹 Types de membres
    MEMBER_TYPE_CHOICES = [
        ('founder', _("Membre Fondateur")),
        ('active', _("Membre Effectif")),
        ('honorary', _("Membre d'Honneur")),
        ('supporter', _("Membre Sympathisant")),
    ]
    member_type = models.CharField(
        max_length=15,
        choices=MEMBER_TYPE_CHOICES,
        default='active',
        verbose_name=_("Type de membre")
    )

    # 🔹 Statut d'adhésion
    STATUS_CHOICES = [
        ('active', _("Actif")),
        ('inactive', _("Inactif")),
        ('pending', _("En attente")),
        ('suspended', _("Suspendu")),
        ('banned', _("Exclu")),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_("Statut")
    )

    # 🔹 Téléphone avec validation
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?\d{9,15}$', message=_("Numéro de téléphone invalide."))],
        blank=True,
        null=True,
        verbose_name=_("Téléphone")
    )

    # 🔹 Adresse complète
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Adresse")
    )

    # 🔹 Date d'adhésion
    joined_at = models.DateField(
        auto_now_add=True,
        verbose_name=_("Date d'adhésion")
    )

    # 🔹 Expiration de l'adhésion (uniquement pour les membres effectifs)
    membership_expiry = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Date d'expiration de l'adhésion")
    )

    # 🔹 Cotisation mensuelle (seulement pour les membres effectifs)
    monthly_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Cotisation mensuelle (USD)")
    )

    # 🔹 Justificatif de paiement (optionnel)
    payment_proof = models.FileField(
        upload_to="members/payments/",
        blank=True,
        null=True,
        verbose_name=_("Justificatif de paiement")
    )

    # 🔹 Document d'identité
    identity_document = models.FileField(
        upload_to="members/documents/",
        blank=True,
        null=True,
        verbose_name=_("Document d'identité")
    )

    # 🔹 Carte de membre (générée après validation)
    membership_card = models.FileField(
        upload_to="members/cards/",
        blank=True,
        null=True,
        verbose_name=_("Carte de membre")
    )

    class Meta:
        verbose_name = _("Membre")
        verbose_name_plural = _("Membres")
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_member_type_display()}"

    # ✅ Fonction : Vérifier si le membre est actif
    def is_active_member(self):
        """ Vérifie si le membre est actif et à jour dans ses cotisations. """
        if self.member_type == 'active':  # Seuls les membres effectifs doivent payer
            return self.status == 'active' and self.membership_expiry and self.membership_expiry >= now().date()
        return self.status == 'active'  # Les autres membres n'ont pas d'expiration

    # ✅ Fonction : Renouveler l'adhésion pour les membres effectifs
    def renew_membership(self, months=12):
        """ Renouvelle l'adhésion d'un membre effectif pour X mois (par défaut 12 mois). """
        if self.member_type == 'active':
            if not self.membership_expiry:
                self.membership_expiry = now().date()
            self.membership_expiry = self.membership_expiry.replace(year=self.membership_expiry.year + (months // 12))
            self.status = 'active'
            self.save()

    # ✅ Fonction : Ajouter un membre d'honneur sur décision du Président
    @classmethod
    def grant_honorary_status(cls, user):
        """ Attribue le statut de membre d'honneur sur décision du Président. """
        member, created = cls.objects.get_or_create(user=user)
        member.member_type = 'honorary'
        member.status = 'active'
        member.save()
        return member


# ✅ Manager personnalisé : récupérer uniquement les membres actifs
class ActiveMemberManager(models.Manager):
    """ Manager permettant de filtrer les membres actifs. """
    def get_queryset(self):
        return super().get_queryset().filter(status='active')


# ✅ Utilisation du manager personnalisé
Member.objects_active = ActiveMemberManager()
