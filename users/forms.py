from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserAccount


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = [ "name", "height", "weight", ]

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
       
        self.fields['name'].widget.attrs['placeholder'] = self.fields['name'].label or 'Name'
        
        self.fields['height'].widget.attrs['placeholder'] = self.fields['height'].label or 'Height'
        self.fields['weight'].widget.attrs['placeholder'] = self.fields['weight'].label or 'Weight'



