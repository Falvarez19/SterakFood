from django import forms
from .models import Comentario, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

from django import forms

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo', 'subtitulo', 'cuerpo', 'imagen', 'categoria')