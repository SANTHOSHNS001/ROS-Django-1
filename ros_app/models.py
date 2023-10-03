from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class CustomUserRoles(models.Model):
    role_name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission, blank=True)

class CustomUserPermissions(models.Model):
    permission_name = models.CharField(max_length=100)
    


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('SUPER_ADMIN', 'Super Admin'),
        ('ADMIN', 'Admin'),
        ('SECRETARY', 'Secretary'),
        ('MANAGER', 'Manager'),
        ('SUPERVISOR', 'Supervisor'),
        ('ENGINEER', 'Engineer'),
    )
    
    user_type = models.CharField(max_length=15, choices=USER_TYPES, default='ENGINEER')
    user_role = models.ForeignKey(CustomUserRoles, on_delete=models.CASCADE, related_name='users')



def create_default_groups():
    """
    Utility function to create default user groups.
    Can be run once to initialize groups.
    """
    group_names = ["Super Admin", "Admin", "Secretary", "Manager", "Supervisor", "Engineer"]

    for name in group_names:
        group, created = Group.objects.get_or_create(name=name)
        if created:
            print(f"Group '{name}' created.")
        else:
            print(f"Group '{name}' already exists.")
