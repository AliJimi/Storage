from django.db import models
from django.utils import timezone
from decimal import Decimal
from products.models import Product
from locations.models import Location
from nutrition.models import NutritionData


class ProductBatch(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='batches'
    )
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField(null=True, blank=True)

    # Storage details
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='batches'
    )
    min_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    max_temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Price information
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Discount percentage (0-100)")

    # Optional nutrition data override for this specific batch
    nutrition_data = models.ForeignKey(
        NutritionData,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='batches'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Batch #{self.id} - {self.product.name}"

    @property
    def is_expired(self):
        """Check if batch is expired"""
        if not self.expiration_date:
            return False
        return self.expiration_date < timezone.now().date()

    @property
    def expires_soon(self):
        """Check if batch expires within 7 days"""
        if not self.expiration_date:
            return False

        today = timezone.now().date()
        delta = self.expiration_date - today

        return 0 <= delta.days <= 7

    @property
    def effective_price(self):
        """Calculate the effective price after discount"""
        if not self.sale_price:
            return None

        if not self.discount:
            return self.sale_price

        discount_multiplier = Decimal(1) - (self.discount / Decimal(100))
        return self.sale_price * discount_multiplier

    @property
    def total_value(self):
        """Calculate the total value of this batch"""
        if not self.effective_price:
            return Decimal('0.00')

        return self.effective_price * self.quantity

    class Meta:
        verbose_name_plural = "Product Batches"
        ordering = ['-created_at']
