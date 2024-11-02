from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comentario, Categoria, Message
from .forms import ComentarioForm, ContactForm, PostForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User


#home
def home_view(request):
    return render(request, 'blog/home.html')

#para que solo los admin o miembros del staff puedan eliminar archivos
@staff_member_required

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'El post ha sido eliminado con éxito.')
        return redirect('post_list')
    return render(request, 'blog/eliminar_post_confirmacion.html', {'post': post})


# Vista para la lista de publicaciones
def post_list(request):
    posts = Post.objects.all()
    categorias = Categoria.objects.all()  # Traer todas las categorías
    return render(request, 'blog/post_list.html', {'posts': posts, 'categorias': categorias})

# Vista para el detalle de una publicación

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comentarios = Comentario.objects.filter(post=post)
    
    if request.method == "POST":
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            nuevo_comentario = comentario_form.save(commit=False)
            nuevo_comentario.post = post  # Asigna el post al comentario
            nuevo_comentario.autor = request.user  # Asigna el autor al comentario
            nuevo_comentario.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comentario_form = ComentarioForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comentarios': comentarios,
        'comentario_form': comentario_form
    })


# Filtro de posts por categoría
def posts_por_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    posts = Post.objects.filter(categoria=categoria)
    return render(request, 'blog/post_list.html', {'posts': posts, 'categoria': categoria})


def post_list(request):
    posts = Post.objects.all()
    categorias = Categoria.objects.all()  # Obteniendo todas las categorías
    return render(request, 'blog/post_list.html', {'posts': posts, 'categorias': categorias})



def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            try:
                send_mail(
                    'Mensaje de {}'.format(nombre),
                    mensaje,
                    email,
                    ['thereyalxx@gmail.com'], 
                    fail_silently=False,
                )
                messages.success(request, 'Tu mensaje ha sido enviado exitosamente.')
            except Exception as e:
                messages.error(request, 'Hubo un error al enviar tu mensaje.')

            return redirect('form_exito')  # Redirige a la vista de éxito
    else:
        form = ContactForm()
    return render(request, 'blog/contacto.html', {'form': form})

def form_exito(request):
    return render(request, 'blog/form_exito.html')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['titulo', 'subtitulo', 'descripcion', 'imagen', 'categoria']
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()  # Asegúrate de que la consulta es correcta
        return context
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    success_url = reverse_lazy('post_list')  # Redirige a la lista de posts tras editar

    # Este método define la condición para permitir acceso
    def test_func(self):
        post = self.get_object()  # Obtiene el objeto Post que se está editando
        return self.request.user == post.author or self.request.user.is_superuser

    def handle_no_permission(self):
        # Opcional: redirige a la lista de posts o muestra un mensaje si no tiene permisos
        return redirect('post_list')  # Redirige si el usuario no tiene permisos

def categorias_context(request):
    categorias = Categoria.objects.all()
    return {'categorias': categorias}

def categoria_posts(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    posts = Post.objects.filter(categoria=categoria)
    return render(request, 'blog/categoria_posts.html', {'categoria': categoria, 'posts': posts})

@login_required
def messaging_home(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'blog/home_mensajeria.html', {'users': users})

@login_required
def conversation(request, username):
    # Obtiene el usuario con el que el usuario actual está conversando
    other_user = get_object_or_404(User, username=username)

    # Filtra los mensajes entre el usuario actual y el otro usuario
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    # Si se envía un mensaje nuevo
    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('conversation', username=other_user.username)

    return render(request, 'blog/conversacion.html', {'messages': messages, 'other_user': other_user})