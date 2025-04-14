from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'parent', 'capacity', 'capacity_unit', 'utilization')
    list_filter = ('level',)
    search_fields = ('name', 'address')
    readonly_fields = ('created_at', 'updated_at', 'utilization', 'total_value', 'full_path')
    fieldsets = (
        ('Location Information', {
            'fields': ('name', 'level', 'parent', 'address')
        }),
        ('Capacity Information', {
            'fields': ('capacity', 'capacity_unit', 'utilization')
        }),
        ('Value Information', {
            'fields': ('total_value',)
        }),
        ('Path', {
            'fields': ('full_path',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )