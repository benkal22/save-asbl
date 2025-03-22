from django.shortcuts import render, get_object_or_404
from ..models import Activity  # Import Activity model

def activity_list(request):  # Update view name
    """
    Vue pour afficher la liste des activités.
    """
    activities = Activity.objects.filter(status='active').order_by('-start_date')  # Only active activities
    context = {'activities': activities}  # Update context variable
    return render(request, 'core/activities/activity_list.html', context)  # Update template path


def activity_detail(request, slug):  # Update view name
    """
    Vue pour afficher le détail d'une activité.
    """
    activity = get_object_or_404(Activity, slug=slug)  # Update model name
    context = {'activity': activity}  # Update context variable
    return render(request, 'core/activities/activity_detail.html', context)  # Update template path