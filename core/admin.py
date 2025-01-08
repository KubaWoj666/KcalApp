from django.contrib import admin

from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "kcal", "protein", "fat", "carbs"]

admin.site.register(Product, ProductAdmin)
