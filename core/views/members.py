from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, ListView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from ..models import Member

__all__ = [
    'MemberDashboardView',
    'MemberProfileView',
    'MemberSubscriptionView',
    'MemberDocumentListView',
]

class MemberRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur a un profil membre"""
    def test_func(self):
        return hasattr(self.request.user, 'member_profile')

class MemberDashboardView(MemberRequiredMixin, TemplateView):
    """Vue du tableau de bord membre avec statistiques"""
    template_name = 'core/members/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.request.user.member_profile
        
        try:
            context.update({
                'title': _('Tableau de bord'),
                'member': member,
                'is_active': member.is_active_member(),
                'days_left': (member.membership_expiry - now().date()).days if member.membership_expiry else 0,
                'documents_count': member.get_documents_count(),
            })
        except (AttributeError, ValueError):
            context.update({
                'title': _('Tableau de bord'),
                'error': True,
                'error_message': _("Une erreur s'est produite lors du chargement de votre profil membre.")
            })
        
        return context

    def dispatch(self, request, *args, **kwargs):
        """Handle errors before rendering the template"""
        try:
            if not hasattr(request.user, 'member_profile'):
                messages.error(
                    request,
                    _("Vous devez avoir un profil membre pour accéder à cette page.")
                )
                return redirect('index')
        except AttributeError:
            messages.error(
                request,
                _("Une erreur s'est produite avec votre session. Veuillez vous reconnecter.")
            )
            return redirect('account_login')
            
        return super().dispatch(request, *args, **kwargs)

class MemberProfileView(MemberRequiredMixin, UpdateView):
    """Vue pour mettre à jour le profil membre"""
    model = Member
    template_name = 'core/members/profile.html'
    fields = ['phone_number', 'address']
    success_url = reverse_lazy('member_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            member = self.get_object()
            context.update({
                'title': _('Mon profil'),
                'member': member,
                'is_active': member.is_active_member(),
                'documents': member.get_documents(),
                'documents_count': member.get_documents_count(),
                'has_missing_documents': member.get_documents_count() < 3
            })
        except AttributeError as e:
            messages.error(self.request, _("Une erreur s'est produite lors du chargement de votre profil."))
            return redirect('member_dashboard')
        return context

    def get_object(self, queryset=None):
        return self.request.user.member_profile

    def form_valid(self, form):
        messages.success(self.request, _('Profil mis à jour avec succès.'))
        return super().form_valid(form)

class MemberSubscriptionView(MemberRequiredMixin, DetailView):
    """Vue pour gérer la cotisation du membre"""
    model = Member
    template_name = 'core/members/subscription.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.get_object()
        
        # Calcul du montant dû
        months_due = 1
        if member.membership_expiry and member.membership_expiry < now().date():
            months_due = (now().date() - member.membership_expiry).days // 30 + 1

        context.update({
            'payment_history': member.get_payment_history(),
            'total_contributions': member.get_total_contributions(),
            'min_monthly_fee': member.MIN_MONTHLY_FEE,
            'months_due': months_due,
            'total_due': member.monthly_fee * months_due,
            'payment_methods': [
                {
                    'name': 'mobile_money',
                    'display_name': _('Mobile Money'),
                    'number': '+243 123 456 789',
                    'icon': 'mobile'
                },
                {
                    'name': 'bank_transfer',
                    'display_name': _('Virement bancaire'),
                    'account': 'SAVE ASBL - BE12 3456 7890 1234',
                    'icon': 'bank'
                }
            ]
        })
        return context

    def get_object(self, queryset=None):
        return self.request.user.member_profile

    def post(self, request, *args, **kwargs):
        """Gérer le renouvellement d'adhésion"""
        member = self.get_object()
        
        if 'renew' in request.POST:
            try:
                # Valider le montant personnalisé
                amount = Decimal(request.POST.get('monthly_fee', member.monthly_fee))
                if amount < member.MIN_MONTHLY_FEE:
                    raise ValidationError(
                        _(f"Le montant minimum est de {member.MIN_MONTHLY_FEE} USD")
                    )
                
                # Valider le justificatif
                if not request.FILES.get('payment_proof'):
                    raise ValidationError(_("Le justificatif de paiement est requis"))

                # Mettre à jour le montant si changé
                if amount != member.monthly_fee:
                    member.set_monthly_fee(amount)

                # Sauvegarder le justificatif
                member.payment_proof = request.FILES['payment_proof']
                member.save()

                # Nombre de mois
                months = int(request.POST.get('months', 1))
                if not 1 <= months <= 12:
                    raise ValidationError(_("Le nombre de mois doit être entre 1 et 12"))

                # Renouveler l'adhésion
                member.renew_membership(months=months)
                messages.success(request, _('Demande de renouvellement envoyée.'))

            except (ValidationError, ValueError, decimal.InvalidOperation) as e:
                messages.error(request, str(e))

        return redirect('member_subscription')

class MemberDocumentListView(MemberRequiredMixin, ListView):
    """Vue pour lister et gérer les documents du membre"""
    template_name = 'core/members/documents.html'
    context_object_name = 'documents'

    def get_queryset(self):
        return self.request.user.member_profile.get_documents()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.request.user.member_profile
        context.update({
            'title': _('Mes documents'),
            'member': member,
            'documents_count': member.get_documents_count(),
            'has_missing_documents': member.get_documents_count() < 3
        })
        return context

    def post(self, request, *args, **kwargs):
        """Gérer l'upload de documents"""
        member = request.user.member_profile
        if 'identity_document' in request.FILES:
            member.identity_document = request.FILES['identity_document']
            member.save()
            messages.success(request, _('Document d\'identité téléchargé.'))
        return redirect('member_documents')