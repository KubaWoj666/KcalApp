
from django import forms
from core.models import MealEntry, Meal, Product, SnackEntry

class MealForm(forms.ModelForm):
    meal = forms.ModelChoiceField(
        queryset=Meal.objects.none(),
        empty_label="Choose a meal",
        widget=forms.Select(attrs={"class": "form-control border-primary"}),
        label="Meal",
    )

    class Meta:
        model = MealEntry
        fields = ['meal', 'date', 'portions']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control border-primary'}),
            'portions': forms.NumberInput(attrs={'class': 'form-control border-primary', 'min': 1})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("creator", None)
        super(MealForm, self).__init__(*args, **kwargs)
        
        self.fields['meal'].queryset = Meal.objects.filter(creator=user)
        self.fields['meal'].label_from_instance = self.get_meal_label

    def get_meal_label(self, meal):
        """Formatowanie wyświetlanych opcji wyboru w polu meal"""
        if meal.infinite_portions == True:
                    return f"{meal.recipe.name}| {meal.kcal} kcal"

        return f"{meal.recipe.name} | Portions: {meal.available_portions}/{meal.total_portions} | {meal.kcal} kcal"

  

class SnackEntryForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        empty_label="Choose a product",
        widget=forms.Select(attrs={"class": "form-control border-primary"}),
        label="Product",
    )

    class Meta:
        model = SnackEntry
        fields = ['product', 'date', 'grams']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control border-primary'}),
            'portions': forms.NumberInput(attrs={'class': 'form-control border-primary', 'min': 1})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("creator", None)
        super(SnackEntryForm, self).__init__(*args, **kwargs)
        # Modyfikacja etykiet opcji w polu 'meal'
        self.fields['product'].queryset = Product.objects.filter(creator=user)
        # self.fields['product'].label_from_instance = self.get_meal_label

    # def get_meal_label(self, meal):
    #     """Formatowanie wyświetlanych opcji wyboru w polu meal"""
    #     if meal.infinite_portions == True:
    #                 return f"{meal.recipe.name}| {meal.kcal} kcal"

    #     return f"{meal.recipe.name} | Portions: {meal.available_portions}/{meal.total_portions} | {meal.kcal} kcal"

  
  

  

  
  
  