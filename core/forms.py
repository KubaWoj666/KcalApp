from django import forms
from .models import Product, RecipeProduct

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["id"]

class RecipeProductForm(forms.ModelForm):
    class Meta:
        model = RecipeProduct
        exclude = ["id"]
