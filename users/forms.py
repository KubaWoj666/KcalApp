from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import UserAccount


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = [ "name", "email", "height", "weight", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label or 'email@address.com'
        self.fields['name'].widget.attrs['placeholder'] = self.fields['name'].label or 'Name'
        self.fields['password1'].widget.attrs['placeholder'] = self.fields['password1'].label or 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = self.fields['password2'].label or 'Password confirmation'        
        self.fields['height'].widget.attrs['placeholder'] = self.fields['height'].label or 'Height'
        self.fields['weight'].widget.attrs['placeholder'] = self.fields['weight'].label or 'Weight'

    def signup(self, request, user):
        
        user.save()
        



