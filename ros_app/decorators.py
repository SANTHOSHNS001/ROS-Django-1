
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages

from ros_app.models import CustomPermissions, RolePermissionAssociation
def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page if not authenticated

    return _wrapped_view





def user_has_role(*required_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role.name in required_roles:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, f"Permission denied for {request.user.role.name}")
            return redirect('home')
        return _wrapped_view
    return decorator




def user_has_permission(*required_permissions):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user has the required permissions
            for permission_name in required_permissions:
                try:
                    permission = CustomPermissions.objects.get(name=permission_name)
                    
                    # Check if there is an association between the role and permission
                    association = RolePermissionAssociation.objects.filter(role=request.user.role, permission=permission).first()
                    
                    if not association:
                        raise CustomPermissions.DoesNotExist
                    
                    # Here, you can also check for specific actions like can_read, can_edit, etc.
                    # For simplicity, I'm just checking if the association exists

                except CustomPermissions.DoesNotExist:
                    return HttpResponseForbidden(f"You don't have the permission to access this page")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



