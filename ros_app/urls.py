from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('roles/',views.roles,name='roles'),
    path('create_role/', views.create_role_view, name='create_role'),
    path('permissions/', views.permissions_view, name='permissions'),
    path('create_permission/', views.create_permission_view, name='create_permission'),
    # ... other url patterns
]
