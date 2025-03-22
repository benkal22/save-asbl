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

    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name='team_profile',
        verbose_name=_('Membre')
    )
    role = models.CharField(_('Rôle'), max_length=50, choices=ROLE_CHOICES)
    biography = models.TextField(_('Biographie'), blank=True)
    order = models.PositiveIntegerField(_('Ordre d\'affichage'), default=0)
    is_active = models.BooleanField(_('Actif'), default=True)

    class Meta:
        verbose_name = _('Membre de l\'équipe')
        verbose_name_plural = _('Membres de l\'équipe')
        ordering = ['order', 'member__user__last_name']

    def __str__(self):
        return f"{self.member.get_full_name()} - {self.get_role_display()}"

    def get_full_name(self):
        return self.member.get_full_name()