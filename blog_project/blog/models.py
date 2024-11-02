from django.db import models
from django.conf import settings
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

    #categorias
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    
    #comentarios 

class Comentario(models.Model):
    texto = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    birth_date = models.DateField
    avatar = models.CharField(max_length=255, default='avatar_1.png', null=True, blank=True)
    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.post.titulo}'

    

User = get_user_model()
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not UserProfile.objects.filter(user=instance).exists():
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

#modelo de mensajeria
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.sender} a {self.receiver} en {self.timestamp}"