from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import CustomUser, Member

admin.site.register(Member)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # List view configuration
    list_display = ('email', 'get_full_name', 'role', 'is_active', 'is_staff', 'get_status')
    list_filter = ('is_active', 'is_staff', 'role', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_per_page = 25
    
    # Detail view configuration
    fieldsets = (
        (_('Authentication'), {
            'fields': ('email', 'password'),
            'classes': ('wide',)
        }),
        (_('Personal Information'), {
            'fields': (('first_name', 'last_name'), 'role'),
            'classes': ('wide',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    # Add view configuration
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        (_('Role and Status'), {
            'classes': ('wide',),
            'fields': ('role', 'is_active', 'is_staff'),
        }),
    )
    
    # Custom methods for list_display
    @admin.display(description=_('Full Name'))
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or "-"
    
    @admin.display(description=_('Status'))
    def get_status(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="color: green;">●</span> Active'
            )
        return format_html(
            '<span style="color: red;">●</span> Inactive'
        )
    
    # Custom actions
    actions = ['activate_users', 'deactivate_users']
    
    @admin.action(description=_('Activate selected users'))
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, _(
            f'{updated} users were successfully activated.'
        ))
    
    @admin.action(description=_('Deactivate selected users'))
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, _(
            f'{updated} users were successfully deactivated.'
        ))