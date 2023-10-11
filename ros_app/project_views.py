from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import user_has_role
from .models import Projects, CustomUser
from .forms import ProjectForm

@login_required
def project_view(request):
    print(request.user.role.name)
    if request.user.role.name in ['Super Admin', 'Admin']:
        projects = Projects.objects.all()
        for project in projects:
            print(project.project_managers.all())
    else:
        managed_projects = Projects.objects.filter(project_manager=request.user)
        print
        managed_documents = Projects.objects.filter(document_manager=request.user)
        projects = set(managed_projects) | set(managed_documents)

    return render(request, "pages/project_view.html", {"projects": projects})

@login_required
@user_has_role('Super Admin', 'Admin', 'Project Manager')
def create_project_view(request):
    document_managers = CustomUser.objects.filter(role__name="Document Manager")
    project_managers = CustomUser.objects.filter(role__name="Project Manager")
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_view')
    else:
        form = ProjectForm()
    for field in form.fields:
        if form[field].errors:
            print(f'The field {field} has the following errors: {form[field].errors}')
    context = {
        'form': form,
        'document_managers': document_managers,
        'project_managers': project_managers,

    }
    return render(request, 'pages/create_project.html', context)
