from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='home'),
    path('api/user/', views.get_user_data, name='user_data'),
    path('api/users/', views.get_all_users, name='all_users'),
] 