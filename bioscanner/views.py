from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """
    Vista para la página principal
    El decorador @login_required asegura que solo usuarios autenticados puedan acceder
    """
    return render(request, 'index.html')

@login_required
def dashboard_view(request):
    return render(request, 'index.html', {}) 