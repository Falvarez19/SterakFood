"""
URL configuration for blog_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from blog import views
from django.contrib.auth import views as auth_views
from .views import PostCreateView, PostUpdateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('categoria/<int:pk>/', views.posts_por_categoria, name='posts_por_categoria'), 
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('contacto/', views.contacto, name='contacto'),
    path('form_exito/', views.form_exito, name='form_exito'),
    path('post/new/', PostCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('categoria/<int:categoria_id>/', views.categoria_posts, name='categoria_posts'),
    path('messaging/', views.messaging_home, name='messaging_home'),
    path('messaging/<str:username>/', views.conversation, name='conversation'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.views.generic import TemplateView

urlpatterns += [
    path('about/', TemplateView.as_view(template_name='blog/about.html'), name='about'),
]