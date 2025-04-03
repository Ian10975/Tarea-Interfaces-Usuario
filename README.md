# Bioscanner - Panel de Control de Usuarios

## Descripción
Bioscanner es una aplicación web desarrollada con Django que proporciona un panel de control para la gestión de usuarios. La aplicación incluye autenticación de usuarios, un panel de administración interactivo y funcionalidades CRUD para la gestión de usuarios.

## Características
-  Sistema de autenticación (login/logout)
-  Gestión de usuarios (agregar/eliminar)
-  Diseño responsive con Tailwind CSS
-  Interfaz moderna e intuitiva
-  Accesibilidad ARIA implementada
-  Actualizaciones dinámicas sin recargar la página

## Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone [url-del-repositorio]
cd bioscanner
```

2. Crear un entorno virtual:
```bash
python -m venv venv
```

3. Activar el entorno virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Realizar migraciones:
```bash
python manage.py migrate
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

## Uso

1. Iniciar el servidor:
```bash
python manage.py runserver
```

2. Acceder a:
- Panel de control: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Funcionalidades

### Panel de Control
- Barra lateral responsive
- Botón de agregar usuario (+)
- Modo de eliminación en configuración
- Tarjetas de usuario interactivas

### Gestión de Usuarios
- Formulario de registro con validación
- Eliminación con confirmación
- Avatares automáticos
- Notificaciones de acciones

### Seguridad
- Autenticación requerida
- Protección CSRF
- Sesiones seguras
- Validación de formularios

## Tecnologías Utilizadas
- Django 5.0.1
- Tailwind CSS
- Font Awesome
- JavaScript ES6+

## Dependencias Principales
```text
Django==5.0.1
asgiref==3.7.2
sqlparse==0.4.4
tzdata==2023.3
```

## Configuración
El proyecto utiliza las siguientes configuraciones clave en `settings.py`:
- DEBUG = True (desarrollo)
- ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
- LOGIN_REDIRECT_URL = 'home'
- LOGOUT_REDIRECT_URL = 'login'

## Desarrollo
1. El proyecto sigue la estructura estándar de Django
2. Las vistas requieren autenticación (@login_required)
3. Utiliza templates para la interfaz de usuario
4. Implementa JavaScript para interacciones dinámicas

## Contribuir
1. Fork del repositorio
2. Crear rama para nueva función
3. Commit cambios
4. Push a la rama
5. Crear Pull Request

## Autor
Ian Iker Del Valle Zarate
Gerardo Giovanni Marrufo Palomino


## Estructura del Proyecto 
