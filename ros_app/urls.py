from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('roles/',views.roles,name='roles'),
    path('create_role/', views.create_role_view, name='create_role'),
    path('delete_role/<int:role_id>/', views.delete_role, name='delete_role'),
    path('permissions/', views.permissions_view, name='permissions'),
    path('create_permission/', views.create_permission_view, name='create_permission'),
    path('delete_permission/<int:permission_id>/', views.delete_permission, name='delete_permission'),
    path('users/', views.users_view, name='users'),
    path('forms/', views.forms, name='forms'),
    path('add_user/', views.add_user_view, name='add_user'),
    # ... other url patterns
]