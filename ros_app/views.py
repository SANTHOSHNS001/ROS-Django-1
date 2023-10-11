# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# import logging
# from django.db.models import Count
# from django.contrib.auth import get_user_model
# from django.contrib.auth.decorators import login_required
# from ros_app.forms import *
# from .models import *
# from .view_helper import *
# from django.forms import modelformset_factory

# from .decorators import login_required, user_has_role, user_has_permission


# # Set up logging
# logger = logging.getLogger(__name__)


# def user_login(request):
#     # If user is already authenticated, redirect to home
#     if request.user.is_authenticated:
#         return redirect("home")

#     # Handle POST request from the login form
#     if request.method == "POST":
#         username_or_email = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username_or_email, password=password)

#         # Check if user exists and is active
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect("home")
#             else:
#                 messages.error(
#                     request, "Account is inactive. Contact the admin for assistance."
#                 )
#         else:
#             messages.error(request, "Invalid login credentials.")

#     return render(request, "pages/login.html")

# @login_required
# def home(request):
#     if request.user.is_authenticated:
#         print(f"User Role: {request.user.role}")
#         logger.info(f"The user {request.user} accessed the dashboard.")
#         return render(request, "pages/home.html", {"user": request.user})
#     else:
#         return redirect("login")


# def user_logout(request):
#     logout(request)
#     return redirect("login")

# @login_required
# # @user_has_permission('read_roles')
# @user_has_role('Super Admin','Admin')
# def roles(request):
#     if request.user.is_authenticated:
#         roles = CustomRoles.objects.all()
#         permissions = CustomPermissions.objects.all()
#         form = CreateRoleForm(request.POST)
#         return render(
#             request,
#             "pages/roles.html",
#             {"user": request.user, "roles": roles, "permissions": permissions, "form": form},
#         )
#     else:
#         return redirect("login")

# @user_has_role('Super Admin','Admin')
# def create_role_view(request):
#     if not request.user.is_authenticated or not request.user.is_superuser:
#         return redirect("home")

#     if request.method == "POST":
#         form = CreateRoleForm(request.POST)
#         print(f"User initiated role creation: {request.POST}")
        
#         if form.is_valid():
#             role_name = form.cleaned_data.get("modalRoleName")

#             # Check if role already exists
#             if CustomRoles.objects.filter(name=role_name).exists():
#                 messages.error(request, "Role already exists.")
#             else:
#                 # Save the role with its permissions
#                 role = form.save(commit=False)  # Create the role instance but don't save it yet
#                 role.name = role_name  # Ensure we set the correct name field
#                 role.save()

#                 # Handle permissions
#                 all_permissions = form.cleaned_data.get("permission")
#                 for permission in all_permissions:
#                     selected_actions = request.POST.getlist(f'permission_{permission.name.lower()}')
#                     can_read = 'read' in selected_actions
#                     can_edit = 'edit' in selected_actions
#                     can_create = 'create' in selected_actions
#                     can_delete = 'delete' in selected_actions

#                     # Create or update RolePermissionAssociation
#                     role_permission, created = RolePermissionAssociation.objects.get_or_create(role=role, permission=permission)
#                     role_permission.can_read = can_read
#                     role_permission.can_edit = can_edit
#                     role_permission.can_write = can_create
#                     role_permission.can_delete = can_delete
#                     role_permission.save()

#                 messages.success(request, "Role created successfully.")
#                 return redirect("roles")
#         else:
#             for field in form:
#                 print(field.label)
#                 print(field.value())
#                 print(field.errors)
#                 print('-----------------')
#             messages.error(request, "There was an error creating the role. Please check the provided data.")

#     return redirect("roles")


# @user_has_role('Super Admin','Admin')
# def permissions_view(request):
#     if request.user.is_authenticated:
#         permissions = CustomPermissions.objects.all().prefetch_related(
#             "roles"
#         )  # Pre-fetch related roles for optimization

#         # Print the roles associated with each permission
#         for perm in permissions:
#             roles = ", ".join([role.name for role in perm.roles.all()])
#             print(
#                 f"Permission: {perm.name} has roles: {roles if roles else 'No roles assigned'}"
#             )

#         return render(
#             request,
#             "pages/permissions.html",
#             {"user": request.user, "permissions": permissions},
#         )
#     else:
#         return redirect("login")

# @login_required
# @user_has_role('Super Admin','Admin')
# def create_permission_view(request):
#     if not request.user.is_authenticated or not request.user.is_superuser:
#         return redirect("home")

#     if request.method == "POST":
#         print("User initiated permission creation")
#         permission_name = request.POST.get("modalPermissionName")
#         is_core = request.POST.get("corePermission") == "on"
#         print(f"User initiated permission creation: {permission_name}")

#         # Check if permission exists
#         if CustomPermissions.objects.filter(name=permission_name).exists():
#             messages.error(request, "Permission already exists.")
#             return redirect("create_permission")
#         else:
#             # Create the permission
#             new_permission = CustomPermissions.objects.create(name=permission_name)
#             print(f"Permission created successfully: {new_permission.name}")

#             messages.success(request, "Permission created successfully.")
#             return redirect("create_permission")

#     return redirect("permissions")

# # @user_has_role('Super Admin','Admin')
# def users_view(request):
#     if request.user.is_authenticated:
#         users = CustomUser.objects.all()
#         roles = CustomRoles.objects.all()

#         print(f"Users: {users}")
#         print(f"Roles: {roles}")

#         return render(
#             request,
#             "pages/users.html",
#             {"user": request.user, "users": users, "roles": roles},
#         )
#     else:
#         return redirect("login")





# def delete_role(request, role_id):
#     if not request.user.is_authenticated or not request.user.is_superuser:
#         return redirect("home")

#     if request.method == "POST":
#         role = get_object_or_404(Role, id=role_id)
#         role.delete()
#         messages.success(request, f'Role "{role.name}" deleted successfully.')
#         return redirect("roles")
#     return render(request, "pages/confirm_delete.html", {"object": "Role"})


# def delete_permission(request, permission_id):
#     if not request.user.is_authenticated or not request.user.is_superuser:
#         return redirect("home")

#     if request.method == "POST":
#         permission = get_object_or_404(Permission, id=permission_id)
#         permission.delete()
#         messages.success(
#             request, f'Permission "{permission.name}" deleted successfully.'
#         )
#         return redirect("permissions")
#     return render(request, "pages/confirm_delete.html", {"object": "Permission"})

# @user_has_role('Super Admin','Admin')
# def add_user_view(request):
#     if not request.user.is_authenticated or not request.user.is_superuser:
#         return redirect("home")
#     else:
#         if request.method == "POST":
#             # Get user input from the request
#             username = request.POST["username"]
#             email = request.POST["email"]
#             first_name = request.POST.get(
#                 "first_name", ""
#             )  # using .get() to handle cases where the input might be optional
#             last_name = request.POST.get("last_name", "")
#             password = request.POST["password1"]
#             confirm_password = request.POST["password2"]
#             role_id = request.POST.get("role")
#             picture = request.FILES.get("picture")  # Handle uploaded picture

#             # Check if passwords match
#             if password != confirm_password:
#                 messages.error(request, "Passwords do not match")
#                 return redirect("users")

#             # Check if the username already exists
#             User = get_user_model()
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, "Username already exists")
#                 return redirect("users")

#             # Create the user and assign the selected role
#             user = User(
#                 username=username,
#                 email=email,
#                 first_name=first_name,
#                 last_name=last_name,
#             )
#             user.set_password(password)  # Set the password

#             # Handle the user's profile picture (if provided)
#             if picture:
#                 user.picture = picture

#             # Assign the selected role (assuming you have a Role model)
#             if role_id:
#                 try:
#                     role = CustomRoles.objects.get(pk=role_id)
#                     user.role = role
#                 except CustomRoles.DoesNotExist:
#                     messages.error(request, "Selected role does not exist")
#                     return redirect("users")

#             user.save()

#             messages.success(request, "User created successfully!")
#             return redirect("users")

#         roles = CustomRoles.objects.all()  # Fetch roles for the select dropdown
#         context = {
#             "roles": roles,
#         }
#         return render(request, "pages/users.html", context)


# def edit_user_view(request, user_id):
#     User = get_user_model()
#     user_instance = get_object_or_404(User, pk=user_id)

#     if request.method == "POST":
#         # Get user input from the request
#         username = request.POST["username"]
#         email = request.POST["email"]
#         first_name = request.POST.get("first_name", "")
#         last_name = request.POST.get("last_name", "")
#         role_id = request.POST.get("role")
#         picture = request.FILES.get("picture")  # Handle uploaded picture

#         # Check if the username already exists for another user
#         if User.objects.filter(username=username).exclude(pk=user_id).exists():
#             messages.error(request, "Username already exists")
#             return redirect(f"edit-user/{user_id}/")

#         # Update the user details
#         user_instance.username = username
#         user_instance.email = email
#         user_instance.first_name = first_name
#         user_instance.last_name = last_name

#         # Handle the user's profile picture (if provided)
#         if picture:
#             user_instance.picture = picture

#         # Assign the selected role (assuming you have a Role model)
#         if role_id:
#             try:
#                 role = CustomRoles.objects.get(pk=role_id)
#                 user_instance.role = role
#             except CustomRoles.DoesNotExist:
#                 messages.error(request, "Selected role does not exist")
#                 return redirect(f"edit-user/{user_id}/")

#         user_instance.save()
#         messages.success(request, "User updated successfully!")
#         return redirect("success_page")  # Or some other page

#     roles = CustomRoles.objects.all()  # Fetch roles for the select dropdown
#     context = {
#         "user_instance": user_instance,
#         "roles": roles,
#     }
#     return render(request, "pages/edit_user.html", context)


# def document_title(request):
#     if request.user.is_authenticated:
#         return render(request, "pages/document_title..html")
#     else:
#         return redirect("login")

# def vdml_view(request):
#     if request.user.is_authenticated:
#             # Get VDML documents assigned to the logged-in user
#         if request.user.role.name in ['Super Admin','Admin']:
#             assigned_vdml_documents = VDML_Document.objects.all()
#         else:
#             assigned_vdml_documents = request.user.vdml_documents.all()
#         context = {
#             "vdml_documents": assigned_vdml_documents,
#         }
#         print(f"Assigned VDML Documents: {assigned_vdml_documents}")
#         return render(request, "pages/vdml_view.html", context)
#     else:
#         return redirect("login")



# def project_view(request):
    
#     if request.user.is_authenticated:
#         print(f"User role: {request.user.role.name}")
#         if request.user.role.name  in ['Super Admin','Admin']:
            
#             projects = Projects.objects.all()
#             print(f"Projects: {projects}")
            
#             for project in projects:
#                 print(f"Project: {project}")
 
#                 print(f"Project users: {project.users.all()}")
        

#             context = {
#                 "projects": projects,
#             }
#             return render(request, "pages/project_view.html", context)
#         else:
#             managed_projects = Projects.objects.filter(project_manager=request.user)
#             managed_documents = Projects.objects.filter(document_manager=request.user)
#             assigned_projects = set(managed_projects) | set(managed_documents)
#             #Filter the projects assigned to the user
#             print(f'The user {request.user} has the following projects assigned: {assigned_projects}')
#             print(f"Assigned Projects: {assigned_projects}")
#             context = {
#                 "projects": assigned_projects,
#             }
#             return render(request, "pages/project_view.html", context)

#     else:
#         return redirect("login")




# @login_required
# # @user_has_role('Super Admin','Admin','Project Manager',)
# def create_project_view(request):
#     # Get the user's role
#     user_role = request.user.role

#     # If the user has a role, fetch its permissions and actions
#     if user_role:
#         permissions_associations = RolePermissionAssociation.objects.filter(role=user_role)
#     else:
#         permissions_associations = []
#     print(f'Permissions associations: {permissions_associations}')
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         print(f'Selected project manager: {request.POST.get("project_manager")}')
#         print(f'Selected document manager: {request.POST.get("document_manager")}')
#         if form.is_valid():
#             form.save()
#             # Redirect to a success page or the project listing page
#             return redirect('project_view')  # assuming 'project_view' is a named URL pattern
#         else:
#             # This will only execute when form is invalid after a POST request
#             print('Form is not valid')
#             for field in form:
#                 print(field.label)
#                 print(field.value())
#                 print(field.errors)
#                 print('-----------------')
#                 pass
#     else:
#         form = ProjectForm()

#     # Fetch users with the role "Project Manager"
#     project_managers = CustomUser.objects.filter(role__name="Project Manager")
#     # Fetch users with the role "Document Manager"
#     document_managers = CustomUser.objects.filter(role__name="Document Manager")

#     print(f'Project managers: {project_managers}')
#     print(f'Document managers: {document_managers}')

#     context = {
#         'project_managers': project_managers,
#         'document_managers': document_managers,
#         'form': form
#     }
    
#     return render(request, 'pages/create_project.html', context)


# # def create_vdml_view(request):
# #     form = VDMLDocumentForm()

# #     if request.user.is_authenticated:
# #         engineers = CustomUser.objects.filter(role__name="Engineer")
# #         if request.method == "POST":
# #             # Get user input from the request
# #             form = VDMLDocumentForm(request.POST)
# #             print(f"User initiated VDML creation: {request.POST}")
# #             if form.is_valid():
# #                 form.save()
# #                 messages.success(request, "VDML created successfully!")
# #                 return redirect("vdml_view")
# #             for field in form:
# #                 print(field.label)
# #                 print(field.value())
# #                 print(field.errors)
# #                 print('-----------------')
            
# #     else:
# #         return redirect("login")
# #     return render(request, "pages/create_document.html", {"form": form, "engineers": engineers})


# def create_vdml_view(request):
#     # Define the formset for VDMLDocumentDetail
#     VDMLDocumentDetailFormSet = modelformset_factory(VDMLDocumentDetail, form=VDMLDocumentDetailForm, extra=1)

#     if request.user.is_authenticated:
#         engineers = CustomUser.objects.filter(role__name="Engineer")
#         if request.method == "POST":
#             form = VDMLDocumentDetailForm(request.POST)
#             detail_formset = VDMLDocumentDetailFormSet(request.POST, prefix='details')

#             if form.is_valid() and detail_formset.is_valid():
#                 # Save the main VDML Document
#                 vdml_doc = form.save()

#                 # Save each detail form
#                 for detail_form in detail_formset:
#                     detail = detail_form.save(commit=False)
#                     detail.vdml_document = vdml_doc
#                     detail.save()

#                 messages.success(request, "VDML created successfully!")
#                 return redirect("vdml_view")
            
#             # Error handling and debugging
#             for field in form:
#                 if field.errors:
#                     print(field.label)
#                     print(field.value())
#                     print(field.errors)
#                     print('-----------------')
#             for detail_form in detail_formset:
#                 for field in detail_form:
#                     if field.errors:
#                         print(field.label)
#                         print(field.value())
#                         print(field.errors)
#                         print('-----------------')
#         else:
#             form = VDMLDocumentDetailForm()
#             detail_formset = VDMLDocumentDetailFormSet(queryset=VDMLDocumentDetail.objects.none(), prefix='details')

#     else:
#         return redirect("login")
    
#     context = {
#         "form": form,
#         "detail_formset": detail_formset,
#         "engineers": engineers
#     }
#     return render(request, "pages/create_vdml_doc.html", context)

