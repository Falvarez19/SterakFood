from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import Post, Comentario, Categoria
from .forms import ComentarioForm, CustomUserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

#para que solo los admin o miembros del staff puedan eliminar archivos
@staff_member_required

def eliminar_post(request, pk):
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

# Registro de usuario
def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/registro.html', {'form': form})

# Inicio de sesión
def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('post_list')

# Filtro de posts por categoría
def posts_por_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    posts = Post.objects.filter(categoria=categoria)
    return render(request, 'blog/post_list.html', {'posts': posts, 'categoria': categoria})


def post_list(request):
    posts = Post.objects.all()
    categorias = Categoria.objects.all()  # Obteniendo todas las categorías
    return render(request, 'blog/post_list.html', {'posts': posts, 'categorias': categorias})
