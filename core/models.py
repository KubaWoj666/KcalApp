from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    kcal = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="kcal/100g")
    protein = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="protein/100g")
    fat = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="fat/100g")
    carbs = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="carbs/100g")
    
    def __str__(self):
        return self.name

