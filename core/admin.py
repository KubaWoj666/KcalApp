from django.contrib import admin

from .models import Product, Recipe, RecipeProduct, Meal, MealEntry

class ProductAdmin(admin.ModelAdmin):
    list_display = [ "id", "name", "kcal", "protein", "fat", "carbs"]

class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "total_kcal"]

    def total_kcal(self, obj):
        totals = obj.calculate_total()
        return totals["kcal"]
    
    total_kcal.short_description = "Total Kcal"


class MealAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe", "recipe_id", "kcal", "protein", "fat", "carbs", "total_portions", "available_portions"]

    def recipe_id(self, obj):
        return obj.recipe.id


class MealEntryAdmin(admin.ModelAdmin):
    list_display = ["id", "meal", "meal_id", "date", "portions"]

    def meal_id(self, obj):
        return obj.meal.id



admin.site.register(Product, ProductAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeProduct)
admin.site.register(Meal, MealAdmin)
admin.site.register(MealEntry, MealEntryAdmin)

