from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.contrib.contenttypes.models import ContentType
from datetime import datetime


# add name to the img
def user_directory_path(instance, filename):
    # Get the current date and time
    now = datetime.now()

    # Format date and time
    date_format = now.strftime("%d%m%y_%H%M")

    # Construct the new filename
    new_filename = (
        f"{instance.username}_{date_format}.jpg"  # Assuming the image is in jpg format
    )
    return f"user_pictures/{new_filename}"


from datetime import datetime


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Retrieve the 'Super Admin' role
        super_admin_role = CustomRoles.objects.get_or_create(name="Super Admin")
        # Create the superuser with the provided details
        superuser = self._create_user(
            username, email, password, **extra_fields, role=super_admin_role[0]
        )

        superuser.save(using=self._db)

        return superuser


class CustomRolesManager(models.Manager):
    def get_role_choices(self):
        return self.all().values_list("name", "name")


class CustomPermissions(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CustomRoles(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permission = models.ManyToManyField(
        CustomPermissions,
        through="RolePermissionAssociation",
        related_name="roles",
        blank=True,
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CustomRolesManager()  # Assuming you've defined this manager elsewhere

    def __str__(self):
        return self.name


class RolePermissionAssociation(models.Model):
    role = models.ForeignKey(CustomRoles, on_delete=models.CASCADE)
    permission = models.ForeignKey(CustomPermissions, on_delete=models.CASCADE)
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name="Email Address",
        help_text="Enter a unique email address.",
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name="First Name",
        help_text="Enter the user's first name.",
    )
    last_name = models.CharField(
        max_length=30, verbose_name="Last Name", help_text="Enter the user's last name."
    )
    picture = models.ImageField(
        upload_to=user_directory_path,
        null=True,
        blank=True,
        verbose_name="Profile Picture",
        help_text="Upload a profile picture for the user.",
    )
    role = models.ForeignKey(
        CustomRoles,
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        blank=True,
        verbose_name="Role",
        help_text="Assign a role to the user.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    projects = models.ManyToManyField(
        "Projects",
        related_name="users",
        blank=True,
        verbose_name="Projects",
        help_text="Assign a project to the user.",
    )
    vdml_documents = models.ManyToManyField(
        "VDML_Document",
        related_name="users",
        blank=True,
        verbose_name="VDML Documents",
        help_text="Assign a VDML Document to the user.",
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"


class Projects(models.Model):
    # Add the project name
    project_name = models.CharField(max_length=100, unique=True)
    # Add the project description
    description = models.TextField(blank=True, null=True)
    # Add the project Start and End Date
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # Add the project manager
    project_manager = models.ManyToManyField(
        CustomUser,
        related_name="managed_projects",
        blank=True,
        verbose_name="Project Manager",
        help_text="Assign a project manager to the project.",
    )
    # Add Document manager
    document_manager = models.ManyToManyField(
        CustomUser,
        related_name="managed_documents",
        blank=True,
        verbose_name="Document Manager",
        help_text="Assign a document manager to the project.",
    )
    # Add the Client Details
    client_name = models.CharField(max_length=100, unique=False)
    # CPM - Client Project Manager
    cpm_name = models.TextField(blank=False, null=False)
    cpm_email = models.EmailField()
    cpm_phone = models.CharField(max_length=20)

    # CDM - Client Document Manager
    cdm_name = models.CharField(max_length=255)
    cdm_email = models.EmailField()
    cdm_phone = models.CharField(max_length=20)

    @property
    def duration(self):
        # Get the current date and time
        now = datetime.now(self.end_date.tzinfo)  # Using the timezone of end_date

        # If the project has already ended, return 0
        if now > self.end_date:
            return 0

        # Subtract the current date from end_date to get a timedelta object
        remaining_timedelta = self.end_date - now

        # Return the number of days left
        return remaining_timedelta.days


class VDML_Document(models.Model):
    A4 = "A4"
    A3 = "A3"
    A2 = "A2"
    A1 = "A1"
    LEGAL = "LEGAL"
    LETTER = "LETTER"

    DOCUMENT_SIZES = [
        (A4, "A4"),
        (A3, "A3"),
        (A2, "A2"),
        (A1, "A1"),
        (LEGAL, "LEGAL"),
        (LETTER, "LETTER"),
    ]

    customer_doc_no = models.CharField(max_length=100, unique=True)
    ros_doc_no = models.CharField(max_length=100, unique=True)
    document_title = models.CharField(max_length=100, unique=True)
    document_type = models.CharField(max_length=100, unique=False)
    document_size = models.CharField(max_length=100, choices=DOCUMENT_SIZES, default=A4)
    schedule_submission_date = models.DateTimeField()
    ros_engineer = models.ManyToManyField(
        CustomUser,
        related_name="ros_engineer",
        blank=True,
        verbose_name="ROS Engineer",
        help_text="Assign a ROS Engineer to the project.",
    )
    doc_revision_no = models.CharField(
        max_length=100, unique=True, blank=True, null=True
    )
    document_code = models.CharField(max_length=100, unique=True)
    planned_date = models.DateTimeField(blank=True, null=True)
    forecast_date = models.DateTimeField(blank=True, null=True)
    actual_submission_date = models.DateTimeField(blank=True, null=True)
    ros_transmittal_no = models.CharField(
        max_length=100, unique=True, blank=True, null=True
    )
    doc_duedate = models.DateTimeField(blank=True, null=True)
    doc_returned_date = models.DateTimeField(blank=True, null=True)
    doc_return_code = models.CharField(
        max_length=100, unique=True, blank=True, null=True
    )
    planned_return_date = models.DateTimeField(blank=True, null=True)
    actual_return_date = models.DateTimeField(blank=True, null=True)
    approval_code = models.CharField(max_length=100, unique=True)
    trasmittal_no = models.CharField(max_length=100, unique=True)

    @property
    def duration(self):
        # Get the current date and time
        now = datetime.now(self.planned_date.tzinfo)  # Using the timezone of end_date

        # If the project has already ended, return 0
        if now > self.planned_date:
            return 0

        # Subtract the current date from end_date to get a timedelta object
        remaining_timedelta = self.planned_date - now

        # Return the number of days left
        return remaining_timedelta.days
