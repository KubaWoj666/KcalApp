from django import forms
from .models import Product, RecipeProduct, Recipe
from decimal import Decimal
from django.core.validators import MinValueValidator

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "kcal", "protein", "carbs", "fat"]

    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("creator", None)     
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.creator = self.user
        if commit:
            instance.save()
        return instance
    
            


class RecipeProductForm(forms.ModelForm):
    name = forms.CharField(max_length=150)
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        empty_label="Wybierz produkt",  # Tekst placeholdera
        widget=forms.Select(attrs={"class": "form-control border-primary"})
    )
    class Meta:
        model = RecipeProduct
        fields = ["name", "product", "grams"]
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("creator", None)    
        super().__init__(*args, **kwargs)

        if user:
            self.fields["product"].queryset = Product.objects.filter(creator=user).order_by("name")
    


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

        if grams > 10000:
            print("DEBUG: Dodano błąd maksymalnej gramatury!")
            self.add_error("grams", "❌ Maksymalna gramatura to 10 000 g!")

        return cleaned_data

class AddProductToRecipeForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        empty_label="Wybierz produkt",  # Tekst placeholdera
        widget=forms.Select(attrs={"class": "form-control border-primary"})
    )
    class Meta:
        model = RecipeProduct
        fields = ["product", "grams"]
    
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("creator", None)
        print("useer", user)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["product"].queryset = Product.objects.filter(creator=user).order_by("name")
    