from django import forms
from .models import Comentario, Post, Categoria, Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
#formulario comentario
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']

#formulario contacto
class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea)

    #para poder crear posts
class PostForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), empty_label="Seleccione una categoría")

    class Meta:
        model = Post
        fields = ['titulo', 'subtitulo', 'descripcion', 'imagen', 'categoria']  
        
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['titulo', 'subtitulo', 'descripcion', 'imagen', 'categoria']
    success_url = reverse_lazy('post_list') 

    def form_valid(self, form):
        form.instance.autor = self.request.user  # Asigna el autor al post
        return super().form_valid(form)
#mensajeria
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']

