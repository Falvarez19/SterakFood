Proyecto de Blog
Descripción General del Proyecto
Este es un proyecto de blog basado en Django que incluye funcionalidades de gestión de usuarios y perfiles. El proyecto está organizado en dos aplicaciones principales:

accounts: Maneja el registro de usuarios, inicio de sesión, cierre de sesión, gestión de perfil y cambio de contraseña.
blog: Administra las publicaciones del blog, incluyendo la creación, lectura, edición, eliminación y categorización de los posts.
Funcionalidades
Autenticación de Usuarios (Registro, Inicio de Sesión, Cierre de Sesión)
Gestión de Perfil (Ver y Editar Perfil)
Cambio de Contraseña
CRUD de Publicaciones del Blog (Crear, Leer, Editar, Eliminar)
Categorización de Publicaciones del Blog
Cómo Usar el Proyecto
Configuración: Clona el repositorio y navega al directorio del proyecto.
Instalación de Dependencias: Usa pip install -r requirements.txt para instalar los paquetes necesarios.
Migraciones de Base de Datos: Ejecuta python manage.py migrate para configurar la base de datos.
Crear Superusuario: Ejecuta python manage.py createsuperuser para crear una cuenta de administrador.
Ejecutar el Servidor: Inicia el servidor con python manage.py runserver y accede al sitio en http://127.0.0.1:8000.
Acceso a la Página "About"
El proyecto incluye una página "About" (Acerca de) accesible desde la barra de navegación, donde se proporciona información general sobre la aplicación.
