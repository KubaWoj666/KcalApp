from django import forms
from .models import Product, RecipeProduct, Recipe
from decimal import Decimal
from django.core.validators import MinValueValidator

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["id"]


class RecipeProductForm(forms.ModelForm):
    name = forms.CharField(max_length=150)
    product = forms.ModelChoiceField(
        queryset=Product.objects.all().order_by("name"),
        empty_label="Wybierz produkt",  # Tekst placeholdera
        widget=forms.Select(attrs={"class": "form-control border-primary"})
    )
    class Meta:
        model = RecipeProduct
        fields = ["name", "product", "grams"]


class RecipeNameForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name"]

class RecipeGramsEditForm(forms.Form):
    grams = forms.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal(0.01))],
                               error_messages={'min_value': "❌ Gramatura musi być większa niż 0!"},
                               widget=forms.NumberInput(attrs={'placeholder': 'Grams'}))
    
    
    def clean(self):
        cleaned_data = super().clean()
        grams = cleaned_data.get("grams")

        print("DEBUG: `clean()` jest wykonywane")
        print("DEBUG: `grams` =", grams)

        if grams is None:
            print("DEBUG: Pole grams jest puste, więc walidacja Django zablokowała dalszą walidację")
            return cleaned_data  

        if grams > 1000:
            print("DEBUG: Dodano błąd maksymalnej gramatury!")
            self.add_error("grams", "❌ Maksymalna gramatura to 10 000 g!")

        return cleaned_data

class AddProductToRecipeForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all().order_by("name"),
        empty_label="Wybierz produkt",  # Tekst placeholdera
        widget=forms.Select(attrs={"class": "form-control border-primary"})
    )
    class Meta:
        model = RecipeProduct
        fields = ["product", "grams"]