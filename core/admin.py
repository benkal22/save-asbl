from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import CustomUser, Member, TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'role', 'get_email', 'order', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('member__user__first_name', 'member__user__last_name', 'member__user__email')
    ordering = ('order', 'member__user__last_name')
    list_per_page = 25

    fieldsets = (
        (_('Member Information'), {
            'fields': ('member',)
        }),
        (_('Team Role'), {
            'fields': ('role', 'biography')
        }),
        (_('Settings'), {
            'fields': ('order', 'is_active')
        }),
    )

    def get_full_name(self, obj):
        return obj.member.get_full_name()
    get_full_name.short_description = _('Name')
    get_full_name.admin_order_field = 'member__user__last_name'

    def get_email(self, obj):
        return obj.member.user.email
    get_email.short_description = _('Email')
    get_email.admin_order_field = 'member__user__email'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "member":
            kwargs["queryset"] = Member.objects.filter(
                membership_status='active'
            ).select_related('user')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # List view configuration
    list_display = ('get_avatar_display', 'email', 'get_full_name', 'role', 'is_active', 'is_staff', 'get_status')
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
            'fields': ('avatar', ('first_name', 'last_name'), 'role'),
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
            'fields': ('email', 'password1', 'password2', 'avatar'),
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
    
    @admin.display(description='')
    def get_avatar_display(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="32" height="32" style="border-radius: 50%;" />',
                obj.avatar.url
            )
        return format_html(
            '<img src="/static/images/default-avatar.png" width="32" height="32" style="border-radius: 50%;" />'
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

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    # Add your Member model admin configuration here
    pass