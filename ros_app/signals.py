
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Permission, Group

from ros_app.models import CustomUserPermissions

@receiver(post_delete, sender=CustomUserPermissions)
def revoke_permission_from_role(sender, instance, **kwargs):
    permission = instance.permission
    groups_with_permission = Group.objects.filter(permissions=permission)
    for group in groups_with_permission:
        group.permissions.remove(permission)