from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from ..models import AboutSection, TeamMember, Partner, Achievement, Activity  # Import Activity model
from django.db.models import Case, When, Value, IntegerField

def index(request):
    """
    Vue pour la page d'accueil.
    """
    about_sections = AboutSection.objects.filter(is_active=True).order_by('order')
    partners = Partner.objects.filter(is_active=True).order_by('order')
    achievements = Achievement.objects.filter(is_active=True).order_by('order')
    activities = Activity.objects.filter(is_featured=True, status='active').order_by('-start_date')[:6]  # Get featured activities
    context = {
        'about_sections': about_sections,
        'partners': partners,
        'achievements': achievements,
        'activities': activities,  # Add activities to the context
    }
    return render(request, 'core/public/index.html', context)

def about(request):
    # Create ordering based on role weights
    role_order = Case(
        *[When(role=role, then=Value(weight)) 
          for role, weight in TeamMember.ROLE_WEIGHTS.items()],
        default=Value(999),
        output_field=IntegerField(),
    )

    # Get team members with custom ordering
    team_members = TeamMember.objects.filter(
        is_active=True
    ).select_related(
        'member',
        'member__user'
    ).annotate(
        role_order=role_order
    ).order_by(
        'role_order',
        'member__user__last_name'
    )

    context = {
        'about_sections': AboutSection.objects.filter(is_active=True),
        'team_members': team_members,
        'partners': Partner.objects.filter(is_active=True).order_by('order', 'name'),
        'achievements': Achievement.objects.filter(is_active=True),
        'page_title': _('À propos de SAVE ASBL'),
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