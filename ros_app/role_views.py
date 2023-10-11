from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import user_has_role
from .models import CustomRoles, CustomPermissions, RolePermissionAssociation
from .forms import CreateRoleForm

@login_required
@user_has_role('Super Admin', 'Admin')
def roles(request):
    roles = CustomRoles.objects.all()
    permissions = CustomPermissions.objects.all()
    form = CreateRoleForm(request.POST)
    return render(
        request,
        "pages/roles.html",
        {"user": request.user, "roles": roles, "permissions": permissions, "form": form},
    )

@login_required
@user_has_role('Super Admin', 'Admin')
def create_role_view(request):
    if request.method == "POST":
        form = CreateRoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Role created successfully.")
            return redirect("roles")
        else:
            messages.error(request, "There was an error creating the role. Please check the provided data.")
    return redirect("roles")

@login_required
@user_has_role('Super Admin', 'Admin')
def permissions_view(request):
    permissions = CustomPermissions.objects.all().prefetch_related("roles")
    return render(
        request,
        "pages/permissions.html",
        {"user": request.user, "permissions": permissions},
    )

@login_required
@user_has_role('Super Admin', 'Admin')
def create_permission_view(request):
    if request.method == "POST":
        permission_name = request.POST.get("modalPermissionName")
        is_core = request.POST.get("corePermission") == "on"
        if CustomPermissions.objects.filter(name=permission_name).exists():
            messages.error(request, "Permission already exists.")
            return redirect("create_permission")
        else:
            CustomPermissions.objects.create(name=permission_name)
            messages.success(request, "Permission created successfully.")
            return redirect("create_permission")
    return redirect("permissions")

@login_required
@user_has_role('Super Admin', 'Admin')
def delete_role(request, role_id):
    if request.method == "POST":
        role = get_object_or_404(CustomRoles, id=role_id)
        role.delete()
        messages.success(request, f'Role "{role.name}" deleted successfully.')
        return redirect("roles")
    return render(request, "pages/confirm_delete.html", {"object": "Role"})

@login_required
@user_has_role('Super Admin', 'Admin')
def delete_permission(request, permission_id):
    if request.method == "POST":
        permission = get_object_or_404(CustomPermissions, id=permission_id)
        permission.delete()
        messages.success(request, f'Permission "{permission.name}" deleted successfully.')
        return redirect("permissions")
    return render(request, "pages/confirm_delete.html", {"object": "Permission"})
