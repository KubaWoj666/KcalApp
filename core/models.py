from django.db import models
from django.urls import reverse
from users.models import UserAccount

class Product(models.Model):
    creator = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150)
    kcal = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="kcal/100g")
    protein = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="protein/100g")
    fat = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="fat/100g")
    carbs = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="carbs/100g")
    
    def __str__(self):
        return self.name
    class Meta:
        unique_together = (('name', 'creator'),)

class Recipe(models.Model):
    creator = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150)
    products = models.ManyToManyField(Product, through="RecipeProduct", related_name="recipes")

    def __str__(self):
        return self.name

    def calculate_total(self):
        total_kcal = 0
        total_protein = 0
        total_fat = 0
        total_carbs = 0

        try:
            for recipe_product in self.recipeproduct_set.all():
                grams = recipe_product.grams
                product = recipe_product.product

                total_kcal += (product.kcal * grams/100)
                total_protein += (product.protein * grams/100)
                total_fat += (product.fat * grams/100)
                total_carbs += (product.carbs * grams/100)
        except:
            total_kcal = 0
            total_protein = 0
            total_fat = 0
            total_carbs = 0

        return {
            "kcal" : round(total_kcal, 2),
            "protein": round(total_protein, 2),
            "fat": round(total_fat, 2),
            "carbs": round(total_carbs, 2)

        }


class RecipeProduct(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    grams = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="grams")

    def __str__(self):
        return f"{self.product.name} ({self.grams}g in {self.recipe.name})"
    


class Meal(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    kcal = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="kcal/100g")
    protein = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="protein/100g")
    fat = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="fat/100g")
    carbs = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="carbs/100g")
    total_portions = models.PositiveIntegerField(default=0, null=True)
    available_portions =  models.PositiveIntegerField(default=0, null=True)
    infinite_portions = models.BooleanField(default=False)

    
    def __str__(self):
        return self.recipe.name
    

class MealEntry(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    date = models.DateField()
    portions = models.PositiveBigIntegerField(default=1)

    class Meta:
        verbose_name = "Meal entry"
        verbose_name_plural = "Meal entry"

    def __str__(self):
        return self.meal.recipe.name
    
    def get_year(self):
        if self.date_field:
            return self.date.year  # To działa poprawnie
        return None 
    
    def get_month(self):
        if self.date_field:
            return self.date.month  # To działa poprawnie
        return None 
    
    @property
    def get_html_url(self):
        url = reverse('meal_entry_detail', args=(self.id,))
        return f'<a href="{url}"> {self.meal.recipe.name} </a>'
