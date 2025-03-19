from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('a-propos/', views.about, name='about'),
    path('projets/', views.projects, name='projects'),
    path('projets/<int:project_id>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
    path('faire-un-don/', views.donate, name='donate'),
    path('blog/', views.blog, name='blog'),
    
    
]