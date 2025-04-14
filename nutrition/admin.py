from django.contrib import admin
from .models import NutritionData

@admin.register(NutritionData)
class NutritionDataAdmin(admin.ModelAdmin):
    list_display = ('product', 'serving_size', 'calories_per_serving')
    search_fields = ('product__name', 'ingredients', 'allergens')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Product Information', {
            'fields': ('product',)
        }),
        ('Serving Information', {
            'fields': ('serving_size',)
        }),
        ('Nutritional Values Per Serving', {
            'fields': ('calories_per_serving', 'protein_per_serving', 'fat_per_serving', 'carbs_per_serving')
        }),
        ('Nutritional Values Total', {
            'fields': ('calories_total', 'protein_total', 'fat_total', 'carbs_total')
        }),
        ('Additional Information', {
            'fields': ('ingredients', 'allergens')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )