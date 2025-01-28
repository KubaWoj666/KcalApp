from django import forms
from .models import Product, RecipeProduct, Recipe

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["id"]



class RecipeProductForm(forms.ModelForm):
    name = forms.CharField(max_length=150)
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        empty_label="Wybierz produkt",  # Tekst placeholdera
        widget=forms.Select(attrs={"class": "form-control border-primary"})
    )
    class Meta:
        model = RecipeProduct
        fields = ["name", "product", "grams"]

        