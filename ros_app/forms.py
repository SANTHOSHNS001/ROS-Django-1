from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=True
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        required=True
    )
    
    class Meta:
        model = get_user_model()
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

from django import forms
from .models import Projects

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = [
            'project_name', 'description', 'start_date', 'end_date', 'project_manager', 
            'document_manager', 'client_name', 'cpm_name', 'cpm_email', 'cpm_phone',
            'cdm_name', 'cdm_email', 'cdm_phone'
        ]

        widgets = {
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
                raise ValidationError("End date should be after the start date.")

        return cleaned_data
