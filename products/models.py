from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

CATEGORY_CHOICES = [
    ('food', _('Food')),
    ('beverage', _('Beverage')),
    ('cleaning', _('Cleaning')),
    ('electronics', _('Electronics')),
    ('clothing', _('Clothing')),
    ('furniture', _('Furniture')),
    ('equipment', _('Equipment')),
    ('other', _('Other')),
]

BARCODE_TYPE_CHOICES = [
    ('EAN13', _('EAN-13')),
    ('EAN8', _('EAN-8')),
    ('UPC', _('UPC')),
    ('CODE39', _('Code 39')),
    ('CODE128', _('Code 128')),
    ('QR', _('QR Code')),
    ('OTHER', _('Other')),
]


class Barcode(models.Model):
    code = models.CharField(max_length=50, unique=True)

    type = models.CharField(
        max_length=10,
        choices=BARCODE_TYPE_CHOICES,
        default='OTHER',
    )

    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} ({self.type})"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name_en = models.CharField(max_length=100)
    name_fa = models.CharField(max_length=100)
    barcode = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_edible = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)

    quantity = models.IntegerField(default=0)

    # Image handling
    def product_image_path(self, filename):
        # Generate a unique filename using UUID
        ext = filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        return f'products/{self.id}/{filename}'

    image = models.ImageField(upload_to=product_image_path, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_en

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
        ordering = ['name_en']
