from django.db import models
from django.utils import timezone
import uuid

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('beverage', 'Beverage'),
        ('cleaning', 'Cleaning'),
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('furniture', 'Furniture'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_edible = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    
    # Image handling
    def product_image_path(instance, filename):
        # Generate a unique filename using UUID
        ext = filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return f'products/{instance.id}/{filename}'
        
    image = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def total_quantity(self):
        """Returns the total quantity of this product across all batches"""
        return self.batches.aggregate(total=models.Sum('quantity'))['total'] or 0
    
    @property
    def is_low_stock(self):
        """Returns True if the product is running low on stock"""
        # This is a simple example. In a real app, you might want to define
        # low stock thresholds for each product individually
        return self.total_quantity < 10
    
    @property
    def has_expiring_soon(self):
        """Check if any batches are expiring soon (within 7 days)"""
        today = timezone.now().date()
        seven_days_later = today + timezone.timedelta(days=7)
        
        expiring_count = self.batches.filter(
            expiration_date__isnull=False,
            expiration_date__lte=seven_days_later,
            expiration_date__gte=today
        ).count()
        
        return expiring_count > 0
    
    class Meta:
        ordering = ['name']