from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,  Criteria

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

ACCESS_CHOICES = [
    (False, 'Désactivées'),
    (True, 'Activées')
]

class CriteriaForm(forms.ModelForm):
    class Meta:
        model = Criteria
        fields = ['public', 'budget', 'locality', 'minimum_surface', 'room_amount']
        widgets = {
            'public' : forms.Select(choices=ACCESS_CHOICES)
        }
        labels = {
            'public': 'Notifications',
            'locality': 'Localité',
            'minimum_surface': 'Surface minimale',
            'room_amount': 'Nombre de pièces'
        }
