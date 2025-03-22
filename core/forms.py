from django import forms
from allauth.account.forms import SignupForm
from django.utils.translation import gettext_lazy as _

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label=_('Prénom'),
        widget=forms.TextInput(
            attrs={'placeholder': _('Votre prénom')}
        )
    )
    last_name = forms.CharField(
        max_length=30,
        label=_('Nom'),
        widget=forms.TextInput(
            attrs={'placeholder': _('Votre nom')}
        )
    )

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user