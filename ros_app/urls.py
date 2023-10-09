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
    path('add_user/', views.add_user_view, name='add_user'),
    path('edit-user/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('document_title/', views.document_title, name='document_title'),
    path('project_view/', views.project_view, name='project_view'),
    path('create_project/', views.create_project_view, name='create_project'),
    path('create_vdml_document/', views.create_vdml_view, name='create_vdml_document'),
    path('vdml_view/', views.vdml_view, name='vdml_view'),
]