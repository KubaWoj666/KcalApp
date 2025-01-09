from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=150, unique=True)
    kcal = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="kcal/100g")
    protein = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="protein/100g")
    fat = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="fat/100g")
    carbs = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="carbs/100g")
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=150)
    products = models.ManyToManyField(Product, through="RecipeProduct", related_name="recipes")

    def __str__(self):
        return self.name

    def calculate_total(self):
        total_kcal = 0
        total_protein = 0
        total_fat = 0
        total_carbs = 0

        for recipe_product in self.recipeproduct_set.all():
            grams = recipe_product.grams
            product = recipe_product.product

            total_kcal += (product.kcal * grams/100)
            total_protein += (product.protein * grams/100)
            total_fat += (product.fat * grams/100)
            total_carbs += (product.carbs * grams/100)

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