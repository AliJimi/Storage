from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_fa', 'barcode', 'category', 'is_edible', 'total_quantity', 'created_at')
    list_filter = ('category', 'is_edible')
    search_fields = ('name_en', 'name_fa', 'barcode', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name_en', 'name_fa', 'barcode', 'category', 'is_edible', 'description')
        }),
        ('Images', {
            'fields': ('image',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )