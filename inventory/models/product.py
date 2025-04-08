from django.db import models

from inventory.models.location import Location
from inventory.models.edible import NutritionData


class Product(models.Model):
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, blank=True)
    is_edible = models.BooleanField(default=False)
    default_image = models.ImageField(upload_to="products/images/", null=True, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return f"Image of {self.product.name}"


class ProductBatch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="batches")
    expiration_date = models.DateField(null=True, blank=True)
    size_volume = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()

    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    wholeprice = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Discount in %")

    income_date = models.DateField()
    outgoing_date = models.DateField(null=True, blank=True)

    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="batches")
    nutrition = models.OneToOneField(NutritionData, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def accumulated_price(self):
        price_after_discount = self.sale_price_per_item * (1 - self.discount / 100)
        return round(price_after_discount * self.quantity, 2)

    def __str__(self):
        return f"{self.product.name} | Expires: {self.expiration_date} | Qty: {self.quantity}"
