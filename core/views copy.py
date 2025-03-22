from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

def profile(request):
    return render(request, 'account/login.html')

@login_required
def member_dashboard(request):
    return render(request, 'core/members/dashboard.html')

@login_required
def member_profile(request):
    return render(request, 'core/members/profile.html')

@login_required
def member_subscription(request):
    return render(request, 'core/members/subscription.html')

@login_required
def member_documents(request):
    return render(request, 'core/members/documents.html')