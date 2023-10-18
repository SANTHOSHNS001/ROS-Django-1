import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
from .decorators import user_has_role
from .models import VDML_Document, VDMLDocumentDetail, CustomUser, Projects, ProjectAttribute
# from .forms import VDMLDocumentDetailForm, VDMLDocumentForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def vdml_view(request):
    if request.user.role.name in ['Super Admin', 'Admin']:
        assigned_vdml_documents = VDML_Document.objects.all()
    else:
        assigned_vdml_documents = request.user.vdml_documents.all()
    
    # Get ROS engineers for each VDML_Document
    document_engineers = {}
    for doc in assigned_vdml_documents:
        details = VDMLDocumentDetail.objects.filter(vdml_document=doc)
        all_engineers = []
        for detail in details:
            all_engineers.extend(list(detail.ros_engineer.all()))
        unique_engineers = set(all_engineers)
        document_engineers[doc.id] = unique_engineers
    print(document_engineers)
    context = {
        "vdml_documents": assigned_vdml_documents,
        "document_engineers": document_engineers
    }
    return render(request, "pages/vdml_view.html", context)

def vdml_form_view(request):
    ros_engineers = CustomUser.objects.filter(role__name='Engineer')
    context = { 'ros_engineers': ros_engineers }
    if request.method == "POST":
        # Extract data for VDML_Document
        customer_doc_no = request.POST.get('customer_doc_no')
        ros_doc_no = request.POST.get('ros_doc_no')
        ses_doc_no = request.POST.get('ses_doc_no')
        document_title = request.POST.get('document_title')
        document_type = request.POST.get('document_type')
        document_size = request.POST.get('document_size')

        # Save VDML_Document
        vdml_document = VDML_Document(
            customer_doc_no=customer_doc_no,
            ros_doc_no=ros_doc_no,
            ses_doc_no=ses_doc_no,
            document_title=document_title,
            document_type=document_type,
            document_size=document_size,
        )
        vdml_document.save()

        # Extract details for VDMLDocumentDetail
        # Assuming you'll send data in a structured format like JSON or similar
        # For simplicity, let's assume each detail field is an array, e.g., request.POST.getlist('ros_engineer[]')
        ros_engineers = request.POST.getlist('ros_engineer[]')
        doc_revisions = request.POST.getlist('doc_revision_no[]')
        issue_of_code = request.POST.getlist('issue_of_code[]')
        planned_date = [date if date else None for date in request.POST.getlist('planned_date[]')]
        forecast_date = [date if date else None for date in request.POST.getlist('forecast_date[]')]
        actual_date = [date if date else None for date in request.POST.getlist('actual_date[]')]
        ros_transmittal = request.POST.getlist('ros_transmittal[]')
        approval_rev = request.POST.getlist('approval_rev[]')
        approval_date = [date if date else None for date in request.POST.getlist('approval_date[]')]
        actual_returned_date = [date if date else None for date in request.POST.getlist('actual_returned_date[]')]
        se_comment = request.POST.getlist('se_comment[]')
        planned_return_date = [date if date else None for date in request.POST.getlist('planned_return_date[]')]
        actual_return_date = [date if date else None for date in request.POST.getlist('actual_return_date[]')]
        client_transmittal = request.POST.getlist('client_transmittal[]')
        blng_comment = request.POST.getlist('blng_comment[]')

        print(f'''
            ros_engineers: {ros_engineers}
            doc_revisions: {doc_revisions}
            issue_of_code: {issue_of_code}
            planned_date: {planned_date}
            forecast_date: {forecast_date}
            actual_date: {actual_date}
            ros_transmittal: {ros_transmittal}
            approval_rev: {approval_rev}
            approval_date: {approval_date}
            actual_returned_date: {actual_returned_date}
            se_comment: {se_comment}
            planned_return_date: {planned_return_date}
            actual_return_date: {actual_return_date}
            client_transmittal: {client_transmittal}
            blng_comment: {blng_comment}
''')

        # ... extract other details similarly ...

        for i in range(len(ros_engineers)):
            vdml_document_detail = VDMLDocumentDetail(
                vdml_document=vdml_document,
                doc_revision_no=doc_revisions[i] if i < len(doc_revisions) else None,
                issue_of_code=issue_of_code[i] if i < len(issue_of_code) else None,
                planned_date=planned_date[i] if i < len(planned_date) else None,
                forecast_date=forecast_date[i] if i < len(forecast_date) else None,
                actual_date=actual_date[i] if i < len(actual_date) else None,
                ros_transmittal=ros_transmittal[i] if i < len(ros_transmittal) else None,
                approval_rev=approval_rev[i] if i < len(approval_rev) else None,
                approval_date=approval_date[i] if i < len(approval_date) else None,
                actual_returned_date=actual_returned_date[i] if i < len(actual_returned_date) else None,
                se_comment=se_comment[i] if i < len(se_comment) else None,
                planned_return_date=planned_return_date[i] if i < len(planned_return_date) else None,
                actual_return_date=actual_return_date[i] if i < len(actual_return_date) else None,
                client_transmittal= client_transmittal[i] if i < len(client_transmittal) else None,
                blng_comment=blng_comment[i] if i < len(blng_comment) else None,
            )
            vdml_document_detail.save()
            # Now add ros_engineer separately
            engineer = CustomUser.objects.get(pk=ros_engineers[i])
            vdml_document_detail.ros_engineer.add(engineer)


        return redirect('vdml_view')  # Redirect to a success page or another relevant page

    return render(request, 'pages/create_vdml_doc.html', context)



def add_project_fields_view(request, project_id):
    project = get_object_or_404(Projects, id=project_id)
    
    if request.method == 'POST':
        field_names = request.POST.getlist('field_name[]')
        field_types = request.POST.getlist('field_type[]')
        choices_values = request.POST.getlist('choice_value[]')
        choices_labels = request.POST.getlist('choice_label[]')
        
        # Assuming every field group will have a required checkbox:
        required_values = ['on' for _ in field_names]
        required_booleans = [val in request.POST.getlist('required[]') for val in required_values]

        for i in range(len(field_names)):
            # Convert choice values and labels to JSON format if field type is Dropdown
            choices_json = None
            if field_types[i] == 'DropDown':
                choices = [{"value": choices_values[j], "label": choices_labels[j]} 
                           for j in range(len(choices_values))]
                choices_json = json.dumps(choices)
            
            ProjectAttribute.objects.create(
                project=project,
                field_name=field_names[i],
                field_type=field_types[i],
                choices=choices_json,
                required=required_booleans[i]
            )
        
        # Redirect to the same page to add more fields or to another page as needed
        return redirect('add_required_fields', project_id=project.id)
    
    context = {
        'project': project
    }
    return render(request, 'pages/add_project_fields.html', context)

def edit_project_fields_view(request, project_id):
    project = get_object_or_404(Projects, id=project_id)
    attributes = ProjectAttribute.objects.filter(project=project)
    
    if request.method == 'POST':
        # Get the updated data from the form
        updated_field_names = request.POST.getlist('field_name[]')
        updated_field_types = request.POST.getlist('field_type[]')
        updated_choices_values = request.POST.getlist('choice_value[]')
        updated_choices_labels = request.POST.getlist('choice_label[]')
        
        # Update the existing attributes
        for i, attribute in enumerate(attributes):
            attribute.field_name = updated_field_names[i]
            attribute.field_type = updated_field_types[i]
            
            if attribute.field_type == 'DropDown':
                choices = [{"value": updated_choices_values[j], "label": updated_choices_labels[j]} 
                           for j in range(len(updated_choices_values))]
                attribute.choices = json.dumps(choices)
            
            attribute.save()

        return redirect('edit_project_fields', project_id=project.id)
    
    context = {
        'project': project,
        'attributes': attributes
    }
    return render(request, 'pages/edit_project_fields.html', context)
