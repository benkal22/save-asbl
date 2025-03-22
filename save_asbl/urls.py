from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from allauth.account.decorators import secure_admin_login

admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    
    path('accounts/', include('allauth.urls')),  # Django Allauth
    
    path("accounts/profile/", TemplateView.as_view(template_name="core/profile.html"), name='account_profile'),
    path("i18n/", include("django.conf.urls.i18n")),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)