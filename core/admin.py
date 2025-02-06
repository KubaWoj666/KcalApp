from django.contrib import admin

from .models import Product, Recipe, RecipeProduct

class ProductAdmin(admin.ModelAdmin):
    list_display = [ "id", "name", "kcal", "protein", "fat", "carbs"]

class RecipeAdmin(admin.ModelAdmin):
    list_display = ["name", "total_kcal"]

    def total_kcal(self, obj):
        totals = obj.calculate_total()
        return totals["kcal"]
    
    total_kcal.short_description = "Total Kcal"



admin.site.register(Product, ProductAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeProduct)
