from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
import logging
from django.db.models import Count
from .forms import CustomUserCreationForm
from .models import *
from django.contrib.auth.models import Group, Permission
# Set up logging
logger = logging.getLogger(__name__)

def user_login(request):

    # If user is already authenticated, redirect to home
    if request.user.is_authenticated:
        return redirect('home')

    # Handle POST request from the login form
    if request.method == "POST":
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username_or_email, password=password)

        # Check if user exists and is active
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Account is inactive. Contact the admin for assistance.')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'login.html')

def home(request):
    if request.user.is_authenticated:
        logger.info(f'The user {request.user} accessed the dashboard.')
        return render(request, 'home.html', {'user': request.user})
    else:
        return redirect('login')
    


def user_logout(request):
    logout(request)
    return redirect('login')


def create_user_view(request):
    if not request.user.is_authenticated or request.user.user_type != 'ADMIN':
        return redirect('home')  # or some other response indicating they don't have permission

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Redirect to a success page or back to the form with a success message
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'create_user.html', {'form': form})


def roles(request):
    if request.user.is_authenticated:
        roles_with_counts = CustomUserRoles.objects.annotate(num_users=Count('users'))

        return render(request, 'roles.html', {'user': request.user, 'roles': roles_with_counts})
    else:
        return redirect('login')
    

def create_role_view(request):

    print('User initiated role creation')
    if not request.user.is_authenticated or not request.user.is_superuser:  # Only allow superusers to create roles
        return redirect('home')

    if request.method == 'POST':
        role_name = request.POST.get('modalRoleName')
        #Check if role exists
        if CustomUserRoles.objects.filter(role_name=role_name):
            print('Role already exists')
            messages.error(request, 'Role already exists.')
            return render(request, 'roles.html', {'user': request.user})
        else:
            CustomUserRoles.objects.create(role_name=role_name)
            messages.success(request, 'Role created successfully.')
            
            return redirect('create_role')


    return redirect('roles')


def permissions_view(request):
    if request.user.is_authenticated:
        permissions = CustomUserPermissions.objects.all()
        return render(request, 'permissions.html', {'user': request.user, 'permissions': permissions})
    else:
        return redirect('login')
    

def create_permission_view(request):

    if not request.user.is_authenticated or not request.user.is_superuser: 
        return redirect('home')
    
    if request.method == 'POST':
        print('User initiated permission creation')
        permission_name = request.POST.get('modalPermissionName')
        print(f'User initiated permission creation: {permission_name}')
        
        # Check if permission exists
        if CustomUserPermissions.objects.filter(permission_name=permission_name):
            messages.error(request, 'Permission already exists.')
            return redirect('create_permission')
        else:
            CustomUserPermissions.objects.create(permission_name=permission_name)
            
            messages.success(request, 'Permission created successfully.')
            print('Permission created successfully')
            return redirect('create_permission')
        
    return redirect('permissions')


