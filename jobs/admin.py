from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """Admin interface for Job model"""
    list_display = ('title', 'employer', 'daily_wage', 'required_workers', 
                   'filled_slots', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'employer__full_name', 'employer__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Job Details', {
            'fields': ('employer', 'title', 'description', 'daily_wage')
        }),
        ('Capacity', {
            'fields': ('required_workers', 'filled_slots', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin interface for Application model"""
    list_display = ('worker', 'job', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('worker__full_name', 'worker__email', 'job__title')
    ordering = ('-applied_at',)
    readonly_fields = ('applied_at', 'updated_at')
    
    fieldsets = (
        ('Application Details', {
            'fields': ('job', 'worker', 'status')
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
