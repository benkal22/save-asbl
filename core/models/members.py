from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from ..managers import CustomUserManager

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from calendar import monthrange
from decimal import Decimal
from django.core.validators import MinValueValidator

# 2. MODEL: Member
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.timezone import now
from .users import CustomUser


class Member(models.Model):
    """
    Modèle représentant un membre de l'ASBL "SAVE Asbl".
    """

    # 🔹 Lien avec l'utilisateur Django
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="member_profile",
        verbose_name=_("Utilisateur")
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

    # Ajout du montant minimum de cotisation
    MIN_MONTHLY_FEE = Decimal('10.00')  # 10 USD minimum

    # Cotisation mensuelle personnalisée
    monthly_fee = models.DecimalField(
        _("Cotisation mensuelle (USD)"),
        max_digits=10,
        decimal_places=2,
        default=MIN_MONTHLY_FEE,
        validators=[MinValueValidator(MIN_MONTHLY_FEE)]
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

    birth_date = models.DateField(_('Date de naissance'), null=True, blank=True)
    phone = models.CharField(_('Téléphone'), max_length=20, blank=True)
    address = models.TextField(_('Adresse'), blank=True)
    membership_date = models.DateField(_('Date d\'adhésion'), auto_now_add=True)
    membership_expiry = models.DateField(_('Date d\'expiration'), null=True, blank=True)
    membership_status = models.CharField(
        _('Statut d\'adhésion'),
        max_length=20,
        choices=[
            ('active', _('Actif')),
            ('pending', _('En attente')),
            ('expired', _('Expiré')),
            ('cancelled', _('Annulé')),
        ],
        default='pending'
    )

    class Meta:
        verbose_name = _("Membre")
        verbose_name_plural = _("Membres")
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_member_type_display()})"

    def get_full_name(self):
        return self.user.get_full_name()

    # ✅ Fonction : Vérifier si le membre est actif
    def is_active_member(self):
        """ Vérifie si le membre est actif et à jour dans ses cotisations. """
        if self.member_type == 'active':  # Seuls les membres effectifs doivent payer
            return self.status == 'active' and self.membership_expiry and self.membership_expiry >= now().date()
        return self.status == 'active'  # Les autres membres n'ont pas d'expiration

    # ✅ Fonction : Renouveler l'adhésion pour les membres effectifs
    def renew_membership(self, months=1, payment_proof=None):
        """Renouvelle l'adhésion pour X mois"""
        if self.member_type != 'active':
            return False

        today = now().date()
        
        # Si pas d'expiration ou expirée, commencer à partir de ce mois
        if not self.membership_expiry or self.membership_expiry < today:
            current_month = today.replace(day=1)
            self.membership_expiry = current_month
        
        # Calculer la nouvelle date d'expiration
        current_date = self.membership_expiry
        for _ in range(months):
            _, last_day = monthrange(current_date.year, current_date.month)
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1, day=1)
        
        # Définir l'expiration au dernier jour du dernier mois
        _, last_day = monthrange(current_date.year, current_date.month)
        self.membership_expiry = current_date.replace(day=last_day)
        self.status = 'active'
        self.save()

        # Créer l'historique de paiement
        PaymentHistory.objects.create(
            member=self,
            amount=self.monthly_fee * months,
            period_start=today,
            period_end=self.membership_expiry,
            payment_proof=payment_proof,
            status='pending'
        )

        return True

    # ✅ Fonction : Ajouter un membre d'honneur sur décision du Président
    @classmethod
    def grant_honorary_status(cls, user):
        """ Attribue le statut de membre d'honneur sur décision du Président. """
        member, created = cls.objects.get_or_create(user=user)
        member.member_type = 'honorary'
        member.status = 'active'
        member.save()
        return member

    def get_documents_count(self):
        """Retourne le nombre total de documents téléchargés."""
        count = 0
        if self.identity_document:
            count += 1
        if self.membership_card:
            count += 1
        if self.payment_proof:
            count += 1
        return count

    def get_documents(self):
        """Retourne une liste des documents disponibles."""
        documents = []
        if self.identity_document:
            documents.append({
                'type': 'identity',
                'name': _('Document d\'identité'),
                'file': self.identity_document,
                'uploaded_at': getattr(self.identity_document, 'uploaded_at', None)
            })
        if self.membership_card:
            documents.append({
                'type': 'card',
                'name': _('Carte de membre'),
                'file': self.membership_card,
                'uploaded_at': getattr(self.membership_card, 'uploaded_at', None)
            })
        if self.payment_proof:
            documents.append({
                'type': 'payment',
                'name': _('Justificatif de paiement'),
                'file': self.payment_proof,
                'uploaded_at': getattr(self.payment_proof, 'uploaded_at', None)
            })
        return documents

    def get_payment_history(self):
        """Retourne l'historique des paiements"""
        return self.payments.all()

    def get_total_contributions(self):
        """Retourne le total des cotisations validées"""
        return self.payments.filter(status='validated').aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')

    def set_monthly_fee(self, amount):
        """Définit le montant de la cotisation mensuelle."""
        if amount < self.MIN_MONTHLY_FEE:
            raise ValueError(_(
                f"Le montant minimum de la cotisation est de {self.MIN_MONTHLY_FEE} USD"
            ))
        self.monthly_fee = amount
        self.save()


class PaymentHistory(models.Model):
    """Modèle pour l'historique des paiements de cotisation"""
    member = models.ForeignKey(
        'Member', 
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_("Membre")
    )
    amount = models.DecimalField(
        _("Montant"),
        max_digits=10,
        decimal_places=2
    )
    payment_date = models.DateField(
        _("Date de paiement"),
        auto_now_add=True
    )
    payment_proof = models.FileField(
        _("Justificatif"),
        upload_to='members/payments/%Y/%m/',
        null=True,
        blank=True
    )
    period_start = models.DateField(_("Début de période"))
    period_end = models.DateField(_("Fin de période"))
    status = models.CharField(
        _("Statut"),
        max_length=10,
        choices=[
            ('pending', _('En attente')),
            ('validated', _('Validé')),
            ('rejected', _('Rejeté')),
        ],
        default='pending'
    )
    notes = models.TextField(_("Notes"), blank=True)

    class Meta:
        verbose_name = _("Historique de paiement")
        verbose_name_plural = _("Historiques de paiement")
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.member} - {self.payment_date}"


# ✅ Manager personnalisé : récupérer uniquement les membres actifs
class ActiveMemberManager(models.Manager):
    """ Manager permettant de filtrer les membres actifs. """
    def get_queryset(self):
        return super().get_queryset().filter(status='active')


# ✅ Utilisation du manager personnalisé
Member.objects_active = ActiveMemberManager()
