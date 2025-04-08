from django.db import models
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    class LocationType(models.TextChoices):
        WORLD = "WORLD", _("World")
        COUNTRY = "COUNTRY", _("Country")
        REGION = "REGION", _("Region")
        CITY = "CITY", _("City")
        WAREHOUSE = "WAREHOUSE", _("Warehouse")
        CABINET = "CABINET", _("Cabinet")

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=LocationType.choices)
    description = models.TextField(blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")

    def __str__(self):
        return f"{self.name} ({self.type})"
