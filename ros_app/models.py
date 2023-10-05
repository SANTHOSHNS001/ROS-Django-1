from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
#add name to the img
def user_directory_path(instance, filename):
    # Get the current date and time
    now = datetime.now()
    
    # Format date and time
    date_format = now.strftime('%d%m%y_%H%M')
    
    # Construct the new filename
    new_filename = f"{instance.username}_{date_format}.jpg"  # Assuming the image is in jpg format
    return f"user_pictures/{new_filename}"
from datetime import datetime

def user_directory_path(instance, filename):
    # Get the current date and time
    now = datetime.now()
    
    # Format date and time
    date_format = now.strftime('%d%m%y_%H%M')
    
    # Construct the new filename
    new_filename = f"{instance.username}_{date_format}.jpg"  # Assuming the image is in jpg format
    return f"user_pictures/{new_filename}"



class CustomPermissions(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class CustomRolesManager(models.Manager):
    def get_role_choices(self):
        return self.all().values_list('name', 'name')


class CustomRoles(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permission = models.ManyToManyField(CustomPermissions, related_name="roles")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CustomRolesManager()
    def __str__(self):
        return self.name
    


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email Address", help_text="Enter a unique email address.")
    first_name = models.CharField(max_length=30, verbose_name="First Name", help_text="Enter the user's first name.")
    last_name = models.CharField(max_length=30, verbose_name="Last Name", help_text="Enter the user's last name.")
    picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True, verbose_name="Profile Picture", help_text="Upload a profile picture for the user.")
    role = models.ForeignKey(CustomRoles, on_delete=models.SET_NULL, related_name='users', null=True, blank=True, verbose_name="Role", help_text="Assign a role to the user.")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

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
