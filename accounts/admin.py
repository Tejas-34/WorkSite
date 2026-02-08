from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ('email', 'full_name', 'role', 'city', 'is_oauth_complete', 'created_at')
    list_filter = ('role', 'is_oauth_complete', 'oauth_provider', 'created_at')
    search_fields = ('email', 'full_name', 'city')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'google_id', 'oauth_provider')
    
    fieldsets = (
        ('Account Information', {
            'fields': ('email', 'password', 'full_name', 'role', 'city')
        }),
        ('OAuth Information', {
            'fields': ('google_id', 'oauth_provider', 'is_oauth_complete', 'profile_photo'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_login'),
            'classes': ('collapse',)
        }),
    )
