from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from datetime import datetime


def user_directory_path(instance, filename):
    now = datetime.now()
    date_format = now.strftime("%d%m%y_%H%M")
    new_filename = f"{instance.username}_{date_format}.jpg"
    return f"user_pictures/{new_filename}"


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        super_admin_role, _ = CustomRoles.objects.get_or_create(name="Super Admin")
        return self._create_user(username, email, password, **extra_fields, role=super_admin_role)


class CustomRolesManager(models.Manager):
    def get_role_choices(self):
        return self.all().values_list("name", "name")


class CustomPermissions(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CustomRoles(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permission = models.ManyToManyField(
        CustomPermissions, through="RolePermissionAssociation", related_name="roles", blank=True
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CustomRolesManager()


class RolePermissionAssociation(models.Model):
    role = models.ForeignKey(CustomRoles, on_delete=models.CASCADE)
    permission = models.ForeignKey(CustomPermissions, on_delete=models.CASCADE)
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    role = models.ForeignKey(CustomRoles, on_delete=models.SET_NULL, related_name="users", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    projects = models.ManyToManyField("Projects", related_name="users", blank=True)
    vdml_documents = models.ManyToManyField("VDML_Document", related_name="users", blank=True)
    objects = CustomUserManager()


class ProjectManager(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="manager_projects")
    project = models.ForeignKey('Projects', on_delete=models.CASCADE)


class DocumentManager(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="document_manager_projects")
    project = models.ForeignKey('Projects', on_delete=models.CASCADE)


class Projects(models.Model):
    project_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    project_managers = models.ManyToManyField(CustomUser, through=ProjectManager, related_name="managed_projects_set")
    document_managers = models.ManyToManyField(CustomUser, through=DocumentManager, related_name="managed_documents_set")
    client_name = models.CharField(max_length=100)
    cpm_name = models.TextField()
    cpm_email = models.EmailField()
    cpm_phone = models.CharField(max_length=20)
    cdm_name = models.CharField(max_length=255)
    cdm_email = models.EmailField()
    cdm_phone = models.CharField(max_length=20)


class VDML_Document(models.Model):
    DOCUMENT_SIZES = [
        ('A4', 'A4'),
        ('A3', 'A3'),
        ('A2', 'A2'),
        ('A1', 'A1'),
        ('LEGAL', 'LEGAL'),
        ('LETTER', 'LETTER'),
    ]
    customer_doc_no = models.CharField(max_length=100, unique=True)
    ros_doc_no = models.CharField(max_length=100, unique=True)
    document_title = models.CharField(max_length=100, unique=True)
    document_type = models.CharField(max_length=100)
    document_size = models.CharField(max_length=100, choices=DOCUMENT_SIZES, default='A4') 


class VDMLDocumentDetail(models.Model):
    vdml_document = models.ForeignKey(VDML_Document, on_delete=models.CASCADE, null=False)
    ros_engineer = models.ManyToManyField(CustomUser, related_name="ros_engineer", blank=True)
    doc_revision_no = models.CharField(max_length=100, blank=True, null=True)
    document_code = models.CharField(max_length=100)
    planned_date = models.DateTimeField(blank=True, null=True,)
    forecast_date = models.DateTimeField(blank=True, null=True)
    actual_submission_date = models.DateTimeField(blank=True, null=True)
    ros_transmittal_no = models.CharField(max_length=100, blank=True, null=True)
    doc_duedate = models.CharField(max_length=100, blank=True, null=True)
    doc_returned_date = models.DateTimeField(blank=True, null=True)
    doc_return_code = models.CharField(max_length=100, blank=True, null=True)
    planned_return_date = models.DateTimeField(blank=True, null=True)
    actual_return_date = models.DateTimeField(blank=True, null=True)
    se_comment = models.CharField(max_length=100, blank=True, null=True)
    planned_return_date1 = models.DateTimeField(blank=True, null=True)
    actual_return_date1 = models.DateTimeField(blank=True, null=True)
    approval_code = models.CharField(max_length=100,blank=True, null=True)
    client_trasmittal_no = models.CharField(max_length=100,blank=True, null=True)
    bling_comment = models.CharField(max_length=100,blank=True, null=True)






 