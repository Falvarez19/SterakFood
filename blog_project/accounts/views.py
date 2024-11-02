from django.shortcuts import render, redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from blog.models import Post, UserProfile
from .forms import  CustomUserCreationForm, ProfileUpdateForm, CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def perfil(request):
    # Obtiene el perfil del usuario o crea uno si no existe
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Obtener los posts del usuario
    posts = Post.objects.filter(autor=request.user)  # Asegúrate de que el campo autor existe en el modelo Post
    
    return render(request, 'accounts/perfil.html', {
        'profile': profile,
        'user': request.user,
        'posts': posts,
    })

@login_required

def perfil_editar_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirige a la vista de perfil después de guardar los cambios
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'accounts/edit_perfil.html', {'form': form})  # Usa el nuevo nombre de la plantilla
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('perfil')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/cambiar_contraseña.html', {'form': form})

# Registro de usuario
def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Verificar si el perfil ya existe
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('post_list')
    else:
        form = CustomUserCreationForm()

           # Depuración para ver errores en el formulario
        if not form.is_valid():
               print('Errores en el formulario:', form.errors)
    return render(request, 'accounts/registro.html', {'form': form})


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
    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login') 



