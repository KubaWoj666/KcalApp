from django.contrib import admin

from .models import Product, Recipe, RecipeProduct, Meal, MealEntry, SnackEntry

class ProductAdmin(admin.ModelAdmin):
    list_display = [ "id",  "creator", "name", "kcal", "protein", "fat", "carbs"]

class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "creator", "name", "total_kcal"]

    def total_kcal(self, obj):
        totals = obj.calculate_total()
        return totals["kcal"]
    
    total_kcal.short_description = "Total Kcal"


class MealAdmin(admin.ModelAdmin):
    list_display = ["id", "creator", "recipe", "recipe_id", "kcal", "protein", "fat", "carbs", "total_portions", "available_portions", "infinite_portions"]

    def recipe_id(self, obj):
        return obj.recipe.id


class MealEntryAdmin(admin.ModelAdmin):
    list_display = ["id", "meal_creator", "meal", "meal_id", "date", "portions"]

    def meal_id(self, obj):
        return obj.meal.id
    def meal_creator(self, obj):
        return obj.meal.creator

class SnackEntryAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "product_creator", "product_id", "grams"]

    def product_id(self, obj):
        return obj.product.id
    def product_creator(self, obj):
        return obj.product.creator

admin.site.register(Product, ProductAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeProduct)
admin.site.register(Meal, MealAdmin)
admin.site.register(MealEntry, MealEntryAdmin)
admin.site.register(SnackEntry, SnackEntryAdmin)


