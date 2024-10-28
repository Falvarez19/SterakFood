from django import forms
from .models import Comentario, Post
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

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

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['titulo', 'subtitulo', 'cuerpo', 'imagen', 'categoria']
    success_url = reverse_lazy('post_list')  # Asegúrate de definir a dónde redirigir después de crear el post

    def form_valid(self, form):
        form.instance.autor = self.request.user  # Asigna el autor al post
        return super().form_valid(form)
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

