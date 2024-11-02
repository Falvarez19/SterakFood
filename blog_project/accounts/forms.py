from .models import UserProfile
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nombre', 'apellido', 'imagen_perfil', 'birth_date']


class CustomUserCreationForm(UserCreationForm):
    birthdate = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class CustomPasswordChangeForm(PasswordChangeForm):
    pass
    

class CustomUserCreationForm(UserCreationForm):


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

