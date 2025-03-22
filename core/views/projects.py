from django.shortcuts import render

def projects(request):
    return render(request, 'core/projects/projects.html')

def project_detail(request, project_id):
    return render(request, 'core/projects/project_detail.html', {'project_id': project_id})