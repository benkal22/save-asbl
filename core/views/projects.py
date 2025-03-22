from django.shortcuts import render, get_object_or_404
from ..models.projects import Project  # Import Project model from projects.py

def project_list(request):
    """
    Vue pour afficher la liste des projets.
    """
    projects = Project.objects.filter(status='active').order_by('-start_date')  # Only active projects
    context = {'projects': projects}
    return render(request, 'core/projects/project_list.html', context)


def project_detail(request, slug):
    """
    Vue pour afficher le détail d'un projet.
    """
    project = get_object_or_404(Project, slug=slug)
    context = {'project': project}
    return render(request, 'core/projects/project_detail.html', context)