from django.db import models
from products.models import Product

class NutritionData(models.Model):
    product = models.OneToOneField(
        Product, 
        on_delete=models.CASCADE, 
        related_name='nutrition'
    )
    
    # Serving information
    serving_size = models.CharField(max_length=50)
    
    # Per serving values
    calories_per_serving = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    protein_per_serving = models.CharField(max_length=20, null=True, blank=True)
    fat_per_serving = models.CharField(max_length=20, null=True, blank=True)
    carbs_per_serving = models.CharField(max_length=20, null=True, blank=True)
    
    # Total values
    calories_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    protein_total = models.CharField(max_length=20, null=True, blank=True)
    fat_total = models.CharField(max_length=20, null=True, blank=True)
    carbs_total = models.CharField(max_length=20, null=True, blank=True)
    
    # Additional nutritional information
    ingredients = models.TextField(null=True, blank=True)
    allergens = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Nutrition data for {self.product.name}"
    
    def save(self, *args, **kwargs):
        # Ensure this only applies to edible products
        if not self.product.is_edible:
            self.product.is_edible = True
            self.product.save()
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Nutrition Data"
        verbose_name_plural = "Nutrition Data"