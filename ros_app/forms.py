from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser, Projects, CustomPermissions, CustomRoles, VDMLDocumentDetail,VDML_Document

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'picture', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password and confirm_password and password != confirm_password:
            self.add_error('password2', "Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'picture', 'role']

    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['username'].initial = self.instance.username
            self.fields['email'].initial = self.instance.email
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
            self.fields['picture'].initial = self.instance.picture
            self.fields['role'].initial = self.instance.role

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.picture = self.cleaned_data["picture"]
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = [
            'project_name', 'description', 'start_date', 'end_date', 'project_managers',
            'document_managers', 'client_name', 'cpm_name', 'cpm_email', 'cpm_phone',
            'cdm_name', 'cdm_email', 'cdm_phone'
        ]
        widgets = {
            'project_managers': forms.SelectMultiple(attrs={'type': 'text'}),
            'document_managers': forms.SelectMultiple(attrs={'type': 'text'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'cpm_phone': forms.TextInput(attrs={'type': 'tel'}),
            'cdm_phone': forms.TextInput(attrs={'type': 'tel'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'cpm_email': forms.EmailInput(attrs={'type': 'email'}),
            'cdm_email': forms.EmailInput(attrs={'type': 'email'}),
            'cpm_name': forms.TextInput(attrs={'type': 'text'}),
            'cdm_name': forms.TextInput(attrs={'type': 'text'}),
            'client_name': forms.TextInput(attrs={'type': 'text'}),
            'project_name': forms.TextInput(attrs={'type': 'text'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date <= start_date:
                self.add_error('end_date', "End date should be after the start date.")

        return cleaned_data

class CreateRoleForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    permission = forms.ModelMultipleChoiceField(
        label='Role Permissions',
        queryset=CustomPermissions.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    class Meta:
        model = CustomRoles
        fields = ['name']

    def clean(self):
        cleaned_data = super().clean()
        permissions = []
        for permission in CustomPermissions.objects.all():
            selected_actions = self.data.getlist(f'permission_{permission.name.lower()}')
            if selected_actions:
                permissions.append(permission)

        cleaned_data['permission'] = permissions
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if CustomRoles.objects.filter(name=name).exists():
            raise forms.ValidationError("A role with this name already exists.")
        return name
    

class VDMLDocumentForm(forms.ModelForm):
    class Meta:
        model = VDML_Document
        fields = [
            'customer_doc_no', 'ros_doc_no', 'document_title', 'document_type', 'document_size'
        ]
        widgets = {
            'customer_doc_no': forms.TextInput(attrs={'type': 'text'}),
            'ros_doc_no': forms.TextInput(attrs={'type': 'text'}),
            'document_title': forms.TextInput(attrs={'type': 'text'}),
            'document_type': forms.TextInput(attrs={'type': 'text'}),
            'document_size': forms.Select(choices=VDML_Document.DOCUMENT_SIZES, attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Select a size'})
        }


# class VDMLDocumentDetailForm(forms.ModelForm):
#     class Meta:
#         model = VDMLDocumentDetail
#         fields = [
#             'ros_engineer', 'doc_revision_no', 
#             'document_code', 'planned_date', 'forecast_date', 'actual_submission_date', 
#             'ros_transmittal_no', 'doc_duedate', 'doc_returned_date', 'doc_return_code', 
#             'planned_return_date', 'actual_return_date','planned_return_date1', 'actual_return_date1', 'approval_code', 'client_trasmittal_no',
#         ]
#         widgets = {
#             'planned_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select a date'}),
#             'forecast_date': forms.DateInput(attrs={'type': 'date'}),
#             'actual_submission_date': forms.DateInput(attrs={'type': 'date'}),
#             'doc_duedate': forms.TextInput(attrs={'type': 'date'}),
#             'doc_returned_date': forms.DateInput(attrs={'type': 'date'}),
#             'planned_return_date': forms.DateInput(attrs={'type': 'date'}),
#             'actual_return_date': forms.DateInput(attrs={'type': 'date'}),
#             'planned_return_date1': forms.DateInput(attrs={'type': 'date'}),
#             'actual_return_date1': forms.DateInput(attrs={'type': 'date'}),
#             'ros_engineer': forms.SelectMultiple(attrs={'type': 'text'}),
#             'doc_revision_no': forms.TextInput(attrs={'type': 'text'}),
#             'document_code': forms.TextInput(attrs={'type': 'text'}),
#             'ros_transmittal_no': forms.TextInput(attrs={'type': 'text'}),
#             'doc_return_code': forms.TextInput(attrs={'type': 'text'}),
#             'approval_code': forms.TextInput(attrs={'type': 'text'}),
#             'client_trasmittal_no': forms.TextInput(attrs={'type': 'text'}),
#             'se_comment': forms.TextInput(attrs={'type': 'text'}),
#             'bling_comment': forms.TextInput(attrs={'type': 'text'}),
#         }
