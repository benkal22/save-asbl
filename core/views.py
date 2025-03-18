from django.shortcuts import render

def index(request):
    return render(request, 'core/index.html')

def about(request):
    return render(request, 'core/about/about.html')

def projects(request):
    return render(request, 'core/projects/projects.html')

def project_detail(request, project_id):
    return render(request, 'core/projects/project_detail.html', {'project_id': project_id})

def contact(request):
    return render(request, 'core/contacts/contact.html')

def donate(request):
    return render(request, 'core/donates/donate.html')

def blog(request):
    return render(request, 'core/blog/blog.html')