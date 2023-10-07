from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import logging
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from ros_app.forms import ProjectForm

from .models import *


# Set up logging
logger = logging.getLogger(__name__)


def user_login(request):
    # If user is already authenticated, redirect to home
    if request.user.is_authenticated:
        return redirect("home")

    # Handle POST request from the login form
    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username_or_email, password=password)

        # Check if user exists and is active
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("home")
            else:
                messages.error(
                    request, "Account is inactive. Contact the admin for assistance."
                )
        else:
            messages.error(request, "Invalid login credentials.")

    return render(request, "pages/login.html")


def home(request):
    if request.user.is_authenticated:
        logger.info(f"The user {request.user} accessed the dashboard.")
        return render(request, "pages/home.html", {"user": request.user})
    else:
        return redirect("login")


def user_logout(request):
    logout(request)
    return redirect("login")


def roles(request):
    if request.user.is_authenticated:
        roles = CustomRoles.objects.all()
        permissions = CustomPermissions.objects.all()
        return render(
            request,
            "pages/roles.html",
            {"user": request.user, "roles": roles, "permissions": permissions},
        )
    else:
        return redirect("login")


def create_role_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("home")

    if request.method == "POST":
        role_name = request.POST.get("modalRoleName")

        # Check if role exists
        if not role_name:
            messages.error(request, "Role name cannot be empty.")
            return redirect("roles")
        elif CustomRoles.objects.filter(name=role_name).exists():
            messages.error(request, "Role already exists.")
            return redirect("roles")
        else:
            # Create the role first
            role = CustomRoles.objects.create(name=role_name)
            checkbox_names = [name for name in request.POST.keys()]
            print(checkbox_names)
            # Gather selected permissions and assign to the role
            for permission in CustomPermissions.objects.all():
                # Construct the expected checkbox name for each action
                for action in ["Read", "Write", "Create"]:
                    checkbox_name = f"permission-{permission.id}-{action}"
                    print(f"Checkbox name: {checkbox_name}")
                    if request.POST.get(checkbox_name):
                        print(
                            f"Adding permission: {permission.name} with action: {action}"
                        )
                        role.permission.add(permission)

            messages.success(request, "Role created successfully.")
            return redirect("roles")

    return redirect("roles")


def permissions_view(request):
    if request.user.is_authenticated:
        permissions = CustomPermissions.objects.all().prefetch_related(
            "roles"
        )  # Pre-fetch related roles for optimization

        # Print the roles associated with each permission
        for perm in permissions:
            roles = ", ".join([role.name for role in perm.roles.all()])
            print(
                f"Permission: {perm.name} has roles: {roles if roles else 'No roles assigned'}"
            )

        return render(
            request,
            "pages/permissions.html",
            {"user": request.user, "permissions": permissions},
        )
    else:
        return redirect("login")


@login_required
def create_permission_view(request):
    # Check if the user is a Super Admin or Admin
    if request.user.role not in ["Super Admin", "Admin"]:
        messages.error(request, "You do not have permission to create permissions.")
        return redirect("home")  # Redirect to the homepage or an appropriate URL

    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        description = request.POST.get("description")

        # Create the new permission
        new_permission = CustomPermissions(name=name, description=description)
        new_permission.save()

        messages.success(request, f"Permission '{name}' created successfully!")
        return redirect("create_permission")

    return render(request, "create_permission.html")


@login_required
def users_view(request):
    if request.user.is_authenticated:
        users = CustomUser.objects.all()
        roles = CustomRoles.objects.all()

        print(f"Users: {users}")
        print(f"Roles: {roles}")

        return render(
            request,
            "pages/users.html",
            {"user": request.user, "users": users, "roles": roles},
        )
    else:
        return redirect("login")





def delete_role(request, role_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("home")

    if request.method == "POST":
        role = get_object_or_404(Role, id=role_id)
        role.delete()
        messages.success(request, f'Role "{role.name}" deleted successfully.')
        return redirect("roles")
    return render(request, "pages/confirm_delete.html", {"object": "Role"})


def delete_permission(request, permission_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("home")

    if request.method == "POST":
        permission = get_object_or_404(Permission, id=permission_id)
        permission.delete()
        messages.success(
            request, f'Permission "{permission.name}" deleted successfully.'
        )
        return redirect("permissions")
    return render(request, "pages/confirm_delete.html", {"object": "Permission"})


def add_user_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("home")
    else:
        if request.method == "POST":
            # Get user input from the request
            username = request.POST["username"]
            email = request.POST["email"]
            first_name = request.POST.get(
                "first_name", ""
            )  # using .get() to handle cases where the input might be optional
            last_name = request.POST.get("last_name", "")
            password = request.POST["password1"]
            confirm_password = request.POST["password2"]
            role_id = request.POST.get("role")
            picture = request.FILES.get("picture")  # Handle uploaded picture

            # Check if passwords match
            if password != confirm_password:
                messages.error(request, "Passwords do not match")
                return redirect("users")

            # Check if the username already exists
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("users")

            # Create the user and assign the selected role
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)  # Set the password

            # Handle the user's profile picture (if provided)
            if picture:
                user.picture = picture

            # Assign the selected role (assuming you have a Role model)
            if role_id:
                try:
                    role = CustomRoles.objects.get(pk=role_id)
                    user.role = role
                except CustomRoles.DoesNotExist:
                    messages.error(request, "Selected role does not exist")
                    return redirect("users")

            user.save()

            messages.success(request, "User created successfully!")
            return redirect("users")

        roles = CustomRoles.objects.all()  # Fetch roles for the select dropdown
        context = {
            "roles": roles,
        }
        return render(request, "pages/users.html", context)


def edit_user_view(request, user_id):
    User = get_user_model()
    user_instance = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        # Get user input from the request
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        role_id = request.POST.get("role")
        picture = request.FILES.get("picture")  # Handle uploaded picture

        # Check if the username already exists for another user
        if User.objects.filter(username=username).exclude(pk=user_id).exists():
            messages.error(request, "Username already exists")
            return redirect(f"edit-user/{user_id}/")

        # Update the user details
        user_instance.username = username
        user_instance.email = email
        user_instance.first_name = first_name
        user_instance.last_name = last_name

        # Handle the user's profile picture (if provided)
        if picture:
            user_instance.picture = picture

        # Assign the selected role (assuming you have a Role model)
        if role_id:
            try:
                role = CustomRoles.objects.get(pk=role_id)
                user_instance.role = role
            except CustomRoles.DoesNotExist:
                messages.error(request, "Selected role does not exist")
                return redirect(f"edit-user/{user_id}/")

        user_instance.save()
        messages.success(request, "User updated successfully!")
        return redirect("success_page")  # Or some other page

    roles = CustomRoles.objects.all()  # Fetch roles for the select dropdown
    context = {
        "user_instance": user_instance,
        "roles": roles,
    }
    return render(request, "pages/edit_user.html", context)


def document_title(request):
    if request.user.is_authenticated:
        return render(request, "pages/document_title..html")
    else:
        return redirect("login")


def project_view(request):
    if request.user.is_authenticated:
        return render(request, "pages/project_view.html")
    else:
        return redirect("login")




@login_required
def create_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        print(f'Selected project manager: {request.POST.get("project_manager")}')
        print(f'Selected document manager: {request.POST.get("document_manager")}')
        if form.is_valid():
            form.save()
            # Redirect to a success page or the project listing page
            return redirect('project_view')  # assuming 'project_view' is a named URL pattern
        else:
            # This will only execute when form is invalid after a POST request
            print('Form is not valid')
            for field in form:
                print(field.label)
                print(field.value())
                print(field.errors)
                print('-----------------')
                pass
    else:
        form = ProjectForm()

    # Fetch users with the role "Project Manager"
    project_managers = CustomUser.objects.filter(role__name="Project Manager")
    # Fetch users with the role "Document Manager"
    document_managers = CustomUser.objects.filter(role__name="Document Manager")

    print(f'Project managers: {project_managers}')
    print(f'Document managers: {document_managers}')

    context = {
        'project_managers': project_managers,
        'document_managers': document_managers,
        'form': form
    }
    
    return render(request, 'pages/create_project.html', context)
