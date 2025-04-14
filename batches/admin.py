from django.contrib import admin

from .filters import ExpiresSoonFilter, IsExpiredFilter
from .models import ProductBatch


@admin.register(ProductBatch)
class ProductBatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'expiration_date', 'location', 'is_expired', 'expires_soon')
    list_filter = ('product__category', IsExpiredFilter, ExpiresSoonFilter, 'location')
    search_fields = ('product__name', 'location__name')
    readonly_fields = ('created_at', 'updated_at', 'is_expired', 'expires_soon', 'effective_price', 'total_value')
    date_hierarchy = 'expiration_date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('product', 'quantity', 'expiration_date')
        }),
        ('Storage Information', {
            'fields': ('location', 'min_temperature', 'max_temperature')
        }),
        ('Price Information', {
            'fields': ('purchase_price', 'sale_price', 'discount', 'effective_price', 'total_value')
        }),
        ('Nutrition Override', {
            'fields': ('nutrition_data',),
            'classes': ('collapse',),
            'description': "Optional override for nutrition data specific to this batch."
        }),
        ('Status Information', {
            'fields': ('is_expired', 'expires_soon')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
