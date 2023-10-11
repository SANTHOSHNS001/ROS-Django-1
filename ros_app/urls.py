from django.urls import path
from .auth_views import *
from .role_views import *
from .project_views import *
from .vdml_view import *
from .user_views import *


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', home, name='home'),
    path('roles/',roles,name='roles'),
    path('create_role/', create_role_view, name='create_role'),
    path('delete_role/<int:role_id>/', delete_role, name='delete_role'),
    path('permissions/', permissions_view, name='permissions'),
    path('create_permission/', create_permission_view, name='create_permission'),
    path('delete_permission/<int:permission_id>/', delete_permission, name='delete_permission'),
    path('users/', users_view, name='users'),
    path('add_user/', add_user_view, name='add_user'),
    path('edit-user/<int:user_id>/', edit_user_view, name='edit_user'),
    path('document_title/', document_title, name='document_title'),
    path('project_view/', project_view, name='project_view'),
    path('create_project/', create_project_view, name='create_project'),
    path('create_vdml_document/', create_vdml_view, name='create_vdml_document'),
    path('vdml_view/', vdml_view, name='vdml_view'),
]