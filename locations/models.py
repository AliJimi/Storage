from django.db import models

class Location(models.Model):
    # Location levels
    LEVEL_CHOICES = [
        ('world', 'World'),
        ('country', 'Country'),
        ('region', 'Region'),
        ('city', 'City'),
        ('warehouse', 'Warehouse'),
        ('section', 'Section'),
        ('shelf', 'Shelf'),
        ('cabinet', 'Cabinet'),
    ]
    
    name = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    capacity = models.IntegerField(null=True, blank=True)
    capacity_unit = models.CharField(max_length=20, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def full_path(self):
        """Returns the full location path from the root to this location"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name
    
    @property
    def utilization(self):
        """Calculate utilization as a percentage of capacity"""
        if not self.capacity or self.capacity <= 0:
            return 0
            
        # Count batches in this location
        batch_count = self.batches.aggregate(
            total_quantity=models.Sum('quantity')
        )['total_quantity'] or 0
            
        return min(100, round((batch_count / self.capacity) * 100))
    
    @property
    def total_value(self):
        """Calculate the total value of products in this location"""
        from batches.models import ProductBatch
        
        batches = ProductBatch.objects.filter(location=self)
        total = 0
        
        for batch in batches:
            if batch.effective_price:
                total += batch.effective_price * batch.quantity
                
        return total
    
    class Meta:
        ordering = ['level', 'name']