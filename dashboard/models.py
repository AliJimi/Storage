from django.db import models
from django.utils import timezone
from products.models import Product
from batches.models import ProductBatch
from locations.models import Location
from nutrition.models import NutritionData

# The dashboard doesn't need its own models as it will use data from other apps
# This file is kept for Django convention