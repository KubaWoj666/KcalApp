from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserAccount, WeightEntry


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = [ "name", "height", "weight", ]

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
       
        self.fields['name'].widget.attrs['placeholder'] = self.fields['name'].label or 'Name'
        
        self.fields['height'].widget.attrs['placeholder'] = self.fields['height'].label or 'Height'
        self.fields['weight'].widget.attrs['placeholder'] = self.fields['weight'].label or 'Weight'



class WeighEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ["weight"]
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(WeighEntryForm, self).__init__(*args, **kwargs)
       
        self.fields['weight'].widget.attrs['placeholder'] =  self.user.weight
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance