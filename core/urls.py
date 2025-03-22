from django.urls import include, path

from .views.public import (
    index, about, contact, donate, blog,
)
from .views.projects import (
    projects, project_detail,
)
from .views.members import (
    MemberDashboardView, MemberProfileView,
    MemberSubscriptionView, MemberDocumentListView
)
from .views.accounts import profile

urlpatterns = [
    # Public URLs
    path('', index, name='index'),
    path('a-propos/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('faire-un-don/', donate, name='donate'),
    path('blog/', blog, name='blog'),
    
    # Project URLs
    path('projets/', projects, name='projects'),
    path('projets/<int:project_id>/', project_detail, name='project_detail'),
    
    # Member space URLs
    path('membre/tableau-de-bord/', MemberDashboardView.as_view(), name='member_dashboard'),
    path('membre/profil/', MemberProfileView.as_view(), name='member_profile'),
    path('membre/cotisation/', MemberSubscriptionView.as_view(), name='member_subscription'),
    path('membre/documents/', MemberDocumentListView.as_view(), name='member_documents'),
    
    # Account URLs
    path('compte/profil/', profile, name='account_profile'),

    # Allauth URLs
    path("accounts/", include("allauth.urls")),
]