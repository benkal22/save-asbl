from django.urls import include, path
from .views import public, members, accounts, activities  # Update import

urlpatterns = [
    # Public URLs
    path('', public.index, name='index'),
    path('a-propos/', public.about, name='about'),
    path('contact/', public.contact, name='contact'),
    path('faire-un-don/', public.donate, name='donate'),
    path('blog/', public.blog, name='blog'),
    
    # Activity URLs
    path('activites/', activities.activity_list, name='activity_list'),  # Update URL and view name
    path('activites/<slug:slug>/', activities.activity_detail, name='activity_detail'),  # Update URL and view name
    
    # Member space URLs
    path('membre/tableau-de-bord/', members.MemberDashboardView.as_view(), name='member_dashboard'),
    path('membre/profil/', members.MemberProfileView.as_view(), name='member_profile'),
    path('membre/cotisation/', members.MemberSubscriptionView.as_view(), name='member_subscription'),
    path('membre/documents/', members.MemberDocumentListView.as_view(), name='member_documents'),
    
    # Account URLs
    path('compte/profil/', accounts.profile, name='account_profile'),

    # Allauth URLs
    path("accounts/", include("allauth.urls")),
]