from django.db import models


class NutritionData(models.Model):
    serving_size = models.CharField(max_length=50, blank=True)
    per_serving_calories = models.FloatField(null=True, blank=True)
    per_serving_fat = models.FloatField(null=True, blank=True)
    per_serving_carbs = models.FloatField(null=True, blank=True)
    per_serving_protein = models.FloatField(null=True, blank=True)

    per_whole_calories = models.FloatField(null=True, blank=True)
    per_whole_fat = models.FloatField(null=True, blank=True)
    per_whole_carbs = models.FloatField(null=True, blank=True)
    per_whole_protein = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Nutrition (Serving: {self.serving_size})"
