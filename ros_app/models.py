from django.contrib.auth.models import AbstractUser, UserManager
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



class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Create the superuser with the provided details
        superuser = self._create_user(username, email, password, **extra_fields)

        # Assign the "Super Admin" role to the superuser
        superuser.role = 'Super Admin'
        superuser.save(using=self._db)

        return superuser



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
    objects = CustomUserManager()
    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"


class Projects(models.Model):
    #Add the project name
    project_name = models.CharField(max_length=100, unique=True)
    #Add the project description
    description = models.TextField(blank=True, null=True)
    #Add the project Start and End Date
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    #Add the project manager
    project_manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='managed_projects', null=True, blank=True, verbose_name="Project Manager", help_text="Assign a project manager to the project.")
    #Add Document manager
    document_manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='managed_documents', null=True, blank=True, verbose_name="Document Manager", help_text="Assign a document manager to the project.")
    #Add the Client Details
    client_name = models.CharField(max_length=100, unique=True)
    #CPM - Client Project Manager
    cpm_name = models.TextField(blank=False, null=False)
    cpm_email = models.EmailField()
    cpm_phone = models.CharField(max_length=20)

    #CDM - Client Document Manager
    cdm_name = models.CharField(max_length=255)
    cdm_email = models.EmailField()
    cdm_phone = models.CharField(max_length=20) 
