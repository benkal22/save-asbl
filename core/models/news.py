from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model

class News(models.Model):
    """
    Modèle pour représenter une actualité, un article de blog ou une annonce.
    """
    title = models.CharField(
        max_length=255,
        verbose_name=_("Titre"),
        help_text=_("Titre de l'actualité.")
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text=_("Identifiant unique de l'actualité (généré automatiquement).")
    )
    content = models.TextField(
        verbose_name=_("Contenu"),
        help_text=_("Contenu de l'actualité.")
    )
    publication_date = models.DateTimeField(
        verbose_name=_("Date de publication"),
        default=timezone.now,
        help_text=_("Date de publication de l'actualité.")
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Auteur"),
        help_text=_("Auteur de l'actualité.")
    )
    image = models.ImageField(
        upload_to='news/',
        null=True,
        blank=True,
        verbose_name=_("Image"),
        help_text=_("Image illustrant l'actualité.")
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('evenement', _('Événement')),
            ('annonce', _('Annonce')),
            ('article', _('Article de blog')),
            ('autre', _('Autre')),
        ],
        default='article',
        verbose_name=_("Catégorie"),
        help_text=_("Catégorie de l'actualité.")
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name=_("Mis en avant"),
        help_text=_("Afficher cette actualité sur la page d'accueil.")
    )

    class Meta:
        verbose_name = _("actualité")
        verbose_name_plural = _("actualités")
        ordering = ['-publication_date']  # Most recent news first

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)