from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django import forms
from .models import CustomUser, Member, TeamMember, AboutSection, Partner, Achievement, Activity  # Import Activity model

# Create a ModelForm for TeamMember to customize the member field
class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the member field's queryset and display format
        self.fields['member'].queryset = Member.objects.filter(
            status='active'
        ).select_related('user')
        self.fields['member'].label_from_instance = lambda obj: f"{obj.get_full_name()} ({obj.get_member_type_display()})"

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    form = TeamMemberForm
    list_display = ('get_full_name', 'role', 'email', 'order', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('member__user__first_name', 'member__user__last_name', 'member__user__email', 'biography')
    ordering = ('order', 'member__user__last_name')
    list_per_page = 25

    fieldsets = (
        (_('Informations du membre'), {
            'fields': ('member', 'role')
        }),
        (_('Biographie'), {
            'fields': ('biography',)
        }),
        (_('Réseaux sociaux'), {
            'fields': ('facebook', 'twitter', 'linkedin'),
            'classes': ('collapse',)
        }),
        (_('Paramètres d\'affichage'), {
            'fields': ('order', 'is_active')
        }),
    )

    def get_full_name(self, obj):
        return obj.member.get_full_name()
    get_full_name.short_description = _('Nom complet')
    get_full_name.admin_order_field = 'member__user__last_name'

    def email(self, obj):
        return obj.member.user.email
    email.short_description = _('Email')
    email.admin_order_field = 'member__user__email'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "member":
            kwargs["queryset"] = Member.objects.filter(
                status='active'
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
    list_display = ('get_full_name', 'member_type', 'status', 'joined_at')
    list_filter = ('member_type', 'status')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    ordering = ('-joined_at',)

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = _('Nom complet')
    get_full_name.admin_order_field = 'user__last_name'

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ('get_section_type_display', 'title', 'order', 'is_active', 'updated_at')
    list_filter = ('section_type', 'is_active')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('section_type', 'title', 'subtitle')
        }),
        (_('Contenu'), {
            'fields': ('content', 'image_main', 'image_secondary')
        }),
        (_('Paramètres'), {
            'fields': ('order', 'is_active', 'created_at', 'updated_at')
        }),
    )

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partnership_type', 'is_active', 'order')
    list_filter = ('partnership_type', 'is_active')
    search_fields = ('name', 'description')
    fieldsets = (
        (_('Informations partenaire'), {
            'fields': ('name', 'logo', 'website', 'description')
        }),
        (_('Type et période'), {
            'fields': ('partnership_type', 'start_date')
        }),
        (_('Paramètres'), {
            'fields': ('order', 'is_active')
        }),
    )

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'metric_value', 'year', 'is_active', 'order')
    list_filter = ('is_active', 'year')
    search_fields = ('title', 'description', 'metric_label')
    fieldsets = (
        (_('Informations réalisation'), {
            'fields': ('title', 'description', 'year')
        }),
        (_('Métrique'), {
            'fields': ('metric_value', 'metric_label', 'icon')
        }),
        (_('Paramètres'), {
            'fields': ('order', 'is_active')
        }),
    )

class ActivityAdmin(admin.ModelAdmin):  # Update class name
    list_display = ('title', 'activity_code', 'status', 'start_date', 'end_date', 'is_featured')  # Update field name
    list_filter = ('status', 'thematic_area', 'start_date')
    search_fields = ('title', 'activity_code', 'description')  # Update field name
    prepopulated_fields = {'slug': ('title',)}  # Auto-generate slug from title
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    filter_horizontal = ('team_members',)  # For ManyToManyField

    fieldsets = (
        (_('Informations générales'), {
            'fields': ('title', 'slug', 'activity_code', 'status', 'is_featured')  # Update field name
        }),
        (_('Dates et Lieu'), {
            'fields': ('start_date', 'end_date', 'location')
        }),
        (_('Équipe'), {
            'fields': ('activity_manager', 'team_members')  # Update field name
        }),
        (_('Budget et Financement'), {
            'fields': ('budget', 'funding_sources')
        }),
        (_('Objectifs et Impact'), {
            'fields': ('goal', 'objectives', 'expected_impact', 'impact_indicators')
        }),
        (_('Domaine thématique'), {
            'fields': ('thematic_area',)
        }),
        (_('Visibilité et Reporting'), {
            'fields': ('image', 'description')
        }),
        (_('Suivi et Évaluation'), {
            'fields': ('monitoring_plan', 'evaluation_plan')
        }),
        (_('Gestion des risques'), {
            'fields': ('risk_assessment',)
        }),
        (_('Innovation & Technologie'), {
            'fields': ('tech_stack',)
        }),
        (_('Objectifs ODD'), {
            'fields': ('sdg_goals',)
        }),
    )

admin.site.register(Activity, ActivityAdmin)  # Update model name