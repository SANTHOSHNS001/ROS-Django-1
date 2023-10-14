from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
from .decorators import user_has_role
from .models import VDML_Document, VDMLDocumentDetail, CustomUser
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
