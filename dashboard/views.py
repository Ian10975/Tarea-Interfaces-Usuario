from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@login_required
def dashboard_view(request):
    return render(request, 'index.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    """
    Vista para obtener los datos del usuario actual
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        data = {
            'username': request.user.username,
            'email': request.user.email,
            'role': profile.role,
            'avatar': profile.avatar.url if profile.avatar else None,
            'bio': profile.bio
        }
        return Response(data)
    except UserProfile.DoesNotExist:
        return Response({'error': 'Perfil no encontrado'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    """
    Vista para obtener datos de todos los usuarios (solo para administradores)
    """
    if not request.user.is_staff:
        return Response({'error': 'No autorizado'}, status=403)
    
    users = User.objects.all()
    data = []
    for user in users:
        try:
            profile = user.userprofile
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': profile.role,
                'avatar': profile.avatar.url if profile.avatar else None,
                'is_active': user.is_active
            }
            data.append(user_data)
        except UserProfile.DoesNotExist:
            continue
    
    return Response(data) 