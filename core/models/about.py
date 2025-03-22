from django.db import models
from django.utils.translation import gettext_lazy as _
from .members import Member

class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('president', _('Président')),
        ('vice_president', _('Vice-Président')),
        ('secretary', _('Secrétaire')),
        ('treasurer', _('Trésorier')),
        ('project_manager', _('Chef de Projet')),
        ('communication', _('Responsable Communication')),
        ('member', _('Membre')),
    ]

    # Dictionnaire pour définir le poids hiérarchique de chaque rôle
    ROLE_WEIGHTS = {
        'president': 1,
        'vice_president': 2,
        'secretary': 3,
        'treasurer': 4,
        'project_manager': 5,
        'communication': 6,
        'member': 7,
    }

    # Relation avec Member
    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name='team_profile',
        verbose_name=_('Membre')
    )

    # Informations de rôle et biographie
    role = models.CharField(_('Rôle'), max_length=50, choices=ROLE_CHOICES)
    biography = models.TextField(_('Biographie'), blank=True)

    # Réseaux sociaux
    facebook = models.URLField(_('Facebook'), blank=True)
    twitter = models.URLField(_('Twitter'), blank=True)
    linkedin = models.URLField(_('LinkedIn'), blank=True)

    # Paramètres d'affichage
    order = models.PositiveIntegerField(_('Ordre d\'affichage'), default=0)
    is_active = models.BooleanField(_('Actif'), default=True)

    class Meta:
        verbose_name = _('Membre de l\'équipe')
        verbose_name_plural = _('Membres de l\'équipe')
        ordering = ['order', 'role', 'member__user__last_name']

    def __str__(self):
        return f"{self.member.get_full_name()} - {self.get_role_display()}"

    def get_full_name(self):
        return self.member.get_full_name()

    def get_avatar_url(self):
        """Retourne l'URL de l'avatar du membre"""
        if self.member.user.avatar:
            return self.member.user.avatar.url
        return None

    @property
    def email(self):
        """Retourne l'email du membre"""
        return self.member.user.email

    def get_social_links(self):
        """Retourne les liens des réseaux sociaux non vides"""
        links = {}
        if self.facebook:
            links['facebook'] = self.facebook
        if self.twitter:
            links['twitter'] = self.twitter
        if self.linkedin:
            links['linkedin'] = self.linkedin
        return links

    @property
    def role_weight(self):
        """Retourne le poids hiérarchique du rôle"""
        return self.ROLE_WEIGHTS.get(self.role, 999)

    def save(self, *args, **kwargs):
        """Définit l'ordre basé sur le poids du rôle si non spécifié"""
        if not self.order:
            self.order = self.role_weight
        super().save(*args, **kwargs)

class AboutSection(models.Model):
    """Modèle pour gérer les différentes sections de la page À propos"""
    SECTION_TYPES = [
        ('mission', _('Notre Mission')),
        ('impact', _('Notre Impact')),
        ('values', _('Nos Valeurs')),
        ('history', _('Notre Histoire')),
        ('partners', _('Nos Partenaires')),
    ]

    section_type = models.CharField(
        _('Type de section'),
        max_length=50,
        choices=SECTION_TYPES,
        unique=True
    )
    title = models.CharField(_('Titre'), max_length=200)
    subtitle = models.CharField(_('Sous-titre'), max_length=300, blank=True)
    content = models.TextField(_('Contenu'))
    image_main = models.ImageField(
        _('Image principale'),
        upload_to='about/sections/',
        help_text=_('Image principale de la section')
    )
    image_secondary = models.ImageField(
        _('Image secondaire'),
        upload_to='about/sections/',
        blank=True,
        help_text=_('Image secondaire optionnelle')
    )
    order = models.PositiveIntegerField(_('Ordre d\'affichage'), default=0)
    is_active = models.BooleanField(_('Actif'), default=True)
    created_at = models.DateTimeField(_('Créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Modifié le'), auto_now=True)

    class Meta:
        verbose_name = _('Section À propos')
        verbose_name_plural = _('Sections À propos')
        ordering = ['order']

    def __str__(self):
        return f"{self.get_section_type_display()}"

class Partner(models.Model):
    """Modèle pour gérer les partenaires"""
    name = models.CharField(_('Nom'), max_length=200)
    logo = models.ImageField(_('Logo'), upload_to='about/partners/')
    website = models.URLField(_('Site web'), blank=True)
    description = models.TextField(_('Description'), blank=True)
    partnership_type = models.CharField(
        _('Type de partenariat'),
        max_length=50,
        choices=[
            ('financial', _('Financier')),
            ('technical', _('Technique')),
            ('strategic', _('Stratégique')),
            ('academic', _('Académique')),
        ]
    )
    is_active = models.BooleanField(_('Actif'), default=True)
    order = models.PositiveIntegerField(_('Ordre d\'affichage'), default=0)
    start_date = models.DateField(_('Date de début'), null=True, blank=True)

    class Meta:
        verbose_name = _('Partenaire')
        verbose_name_plural = _('Partenaires')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Achievement(models.Model):
    """Modèle pour les réalisations et impact"""
    title = models.CharField(_('Titre'), max_length=200)
    description = models.TextField(_('Description'))
    metric_value = models.CharField(_('Valeur métrique'), max_length=50)
    metric_label = models.CharField(_('Label métrique'), max_length=100)
    icon = models.FileField(
        _('Icône'),
        upload_to='about/achievements/',
        help_text=_('SVG ou image pour l\'icône')
    )
    year = models.PositiveIntegerField(_('Année'), null=True, blank=True)
    is_active = models.BooleanField(_('Actif'), default=True)
    order = models.PositiveIntegerField(_('Ordre d\'affichage'), default=0)

    class Meta:
        verbose_name = _('Réalisation')
        verbose_name_plural = _('Réalisations')
        ordering = ['-year', 'order']

    def __str__(self):
        return self.title