from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import *
from .decorators import *
from .models import CustomUser, CustomRoles
from .forms import CustomUserEditForm, CustomUserCreationForm

@login_required
def users_view(request):
    if request.user.is_authenticated:
        users = CustomUser.objects.all()
        roles = CustomRoles.objects.all()
        return render(
            request,
            "pages/users.html",
            {"user": request.user, "users": users, "roles": roles},
        )
    else:
        return redirect("login")

@login_required
@user_has_role('Super Admin', 'Admin')
def add_user_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            if request.user.role.name == "Super Admin":
                return redirect("users")
            else:
                return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "pages/users.html", {"form": form})

@login_required
@user_has_role('Super Admin', 'Admin')
def edit_user_view(request, user_id):
    user_instance = get_object_or_404(CustomUser, pk=user_id)
    if request.method == "POST":
        form = CustomUserEditForm(request.POST, instance=user_instance)
        if form.is_valid():
            form.save() 
            messages.success(request, "User updated successfully!")
            return redirect("users_view")
    else:
        form = CustomUserEditForm(instance=user_instance)
    return render(request, "pages/edit_user.html", {"form": form, "user_id": user_id})

@login_required
def document_title(request):
    if request.user.is_authenticated:
        return render(request, "pages/document_title.html")
    else:
        return redirect("login")
