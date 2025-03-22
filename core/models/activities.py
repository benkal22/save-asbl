from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from .users import CustomUser  # Import CustomUser from users.py
from django.utils.text import slugify  # Import slugify

class Activity(models.Model):  # Rename the model to Activity
    """
    Modèle pour représenter une activité/action de l'ASBL SAVE.
    """

    # Activity Identification
    title = models.CharField(
        max_length=255,
        verbose_name=_("Titre de l'activité"),  # Update verbose_name
        help_text=_("Nom clair et concis de l'activité.")  # Update help_text
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text=_("Identifiant unique de l'activité (généré automatiquement).")  # Update help_text
    )
    activity_code = models.CharField(  # Update field name
        max_length=20,
        unique=True,
        verbose_name=_("Code de l'activité"),  # Update verbose_name
        help_text=_("Code unique pour identifier l'activité (ex: SAVE-SANTE-2025).")  # Update help_text
    )

    # Activity Dates
    start_date = models.DateField(
        verbose_name=_("Date de début"),
        default=timezone.now,
        help_text=_("Date de lancement effectif de l'activité.")  # Update help_text
    )
    end_date = models.DateField(
        verbose_name=_("Date de fin prévue"),
        null=True,
        blank=True,
        help_text=_("Date de fin estimée de l'activité.")  # Update help_text
    )

    # Activity Status
    STATUS_CHOICES = [
        ('planning', _('En planification')),
        ('active', _('En cours')),
        ('on_hold', _('En attente')),
        ('completed', _('Terminé')),
        ('cancelled', _('Annulé')),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planning',
        verbose_name=_("Statut"),
        help_text=_("État actuel de l'activité.")  # Update help_text
    )

   # Activity Location
    location = models.CharField(
        max_length=255,
        verbose_name=_("Lieu"),
        help_text=_("Zone géographique où se déroule l'activité.")  # Update help_text
    )

    # Activity Team
    activity_manager = models.ForeignKey(  # Update field name
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_activities',  # Update related_name
        verbose_name=_("Chef de l'activité"),  # Update verbose_name
        help_text=_("Responsable principal de l'activité.")  # Update help_text
    )
    team_members = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='participating_activities',  # Update related_name
        verbose_name=_("Membres de l'équipe"),
        help_text=_("Membres participant à l'activité.")  # Update help_text
    )

    # Activity Budget
    budget = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Budget total"),
        help_text=_("Budget total alloué à l'activité.")  # Update help_text
    )
    # Activity Funding Sources
    funding_sources = models.TextField(
        verbose_name=_("Sources de financement"),
        blank=True,
        help_text=_("Détail des sources de financement (donateurs, subventions, etc.).")  # Update help_text
    )

    # Activity Goals and Objectives
    goal = models.TextField(
        verbose_name=_("But de l'activité"),  # Update verbose_name
        help_text=_("Objectif global que l'activité vise à atteindre, en accord avec la mission de SAVE ASBL.")  # Update help_text
    )
    objectives = models.TextField(
        verbose_name=_("Objectifs spécifiques"),
        help_text=_("Résultats mesurables et concrets que l'activité doit atteindre.")  # Update help_text
    )

    # Impact Measurement
    expected_impact = models.TextField(
        verbose_name=_("Impact attendu"),
        help_text=_("Changements positifs que l'activité devrait générer (social, économique, environnemental).")  # Update help_text
    )
    impact_indicators = models.TextField(
        verbose_name=_("Indicateurs d'impact"),
        blank=True,
        help_text=_("Mesures utilisées pour évaluer l'impact de l'activité (ex: nombre de personnes touchées, réduction de la malnutrition, etc.).")  # Update help_text
    )

    # Thematic Area (aligning with SAVE ASBL's mission)
    THEMATIC_AREAS = [
        ('sante', _('Santé')),
        ('education', _('Éducation')),
        ('agriculture', _('Agriculture')),
        ('jeunesse', _('Jeunesse et Sports')),
        ('femme_famille', _('Femme, Enfant et Famille')),
        ('tic', _('Technologies de l\'Information et de la Communication')),
        ('infrastructures', _('Infrastructures')),
        ('autres', _('Autres')),
    ]
    thematic_area = models.CharField(
        max_length=50,
        choices=THEMATIC_AREAS,
        verbose_name=_("Domaine thématique"),
        help_text=_("Domaine principal auquel l'activité contribue.")  # Update help_text
    )

    # Activity Visibility and Reporting
    image = models.ImageField(
        upload_to='activities/',  # Update upload_to
        null=True,
        blank=True,
        verbose_name=_("Image de présentation"),
        help_text=_("Image attrayante pour présenter l'activité.")  # Update help_text
    )
    description = models.TextField(
        verbose_name=_("Description détaillée"),
        help_text=_("Description complète de l'activité, ses activités et son fonctionnement.")  # Update help_text
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Mis en avant"),
        help_text=_("Afficher cette activité sur la page d'accueil.")  # Update help_text
    )

    # Monitoring and Evaluation
    monitoring_plan = models.TextField(
        verbose_name=_("Plan de suivi"),
        blank=True,
        help_text=_("Méthodes et fréquences de suivi des activités de l'activité.")  # Update help_text
    )
    evaluation_plan = models.TextField(
        verbose_name=_("Plan d'évaluation"),
        blank=True,
        help_text=_("Comment l'efficacité et l'impact de l'activité seront évalués.")  # Update help_text
    )

    # Risk Management
    risk_assessment = models.TextField(
        verbose_name=_("Évaluation des risques"),
        blank=True,
        help_text=_("Identification des risques potentiels et mesures d'atténuation.")  # Update help_text
    )

    # Innovation & Technology
    tech_stack = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Technologies utilisées"),
        help_text=_("Liste des technologies innovantes utilisées dans l'activité (ex: applications mobiles, IoT, etc.).")  # Update help_text
    )

    # SDG Alignment (Optional, if applicable)
    sdg_goals = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Objectifs ODD"),
        help_text=_("Objectifs de développement durable des Nations Unies auxquels l'activité contribue (ex: ODD 3, ODD 4).")  # Update help_text
    )

    # Additional Fields (for future use)
    # Add any other fields that might be relevant to your specific activities

    class Meta:
        verbose_name = _("activité")  # Update verbose_name
        verbose_name_plural = _("activités")  # Update verbose_name_plural
        ordering = ['-start_date']  # Most recent activities first

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)