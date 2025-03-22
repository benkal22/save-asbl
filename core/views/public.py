from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from ..models import TeamMember

def index(request):
    """Vue pour la page d'accueil"""
    context = {
        'title': _('Accueil'),
    }
    return render(request, 'core/index.html', context)

def about(request):
    team_members = TeamMember.objects.filter(is_active=True)
    context = {
        'team_members': team_members,
        'page_title': _('À propos de SAVE ASBL'),
        'page_description': _('Découvrez notre mission et notre équipe dédiée au développement durable en RDC.')
    }
    return render(request, 'core/about/about.html', context)

def contact(request):
    """Vue pour la page Contact"""
    context = {
        'title': _('Contact'),
    }
    return render(request, 'core/contacts/contact.html', context)

def donate(request):
    """Vue pour la page Faire un don"""
    context = {
        'title': _('Faire un don'),
    }
    return render(request, 'core/donates/donate.html', context)

def blog(request):
    """Vue pour la page Blog"""
    context = {
        'title': _('Blog'),
    }
    return render(request, 'core/blog/blog.html', context)