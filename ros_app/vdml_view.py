from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
from .decorators import user_has_role
from .models import VDML_Document, VDMLDocumentDetail, CustomUser
from .forms import VDMLDocumentDetailForm, VDMLDocumentForm

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

# @login_required
# def create_vdml_view(request):
#     # Define the formset for VDMLDocumentDetail
#     VDMLDocumentDetailFormSet = modelformset_factory(VDMLDocumentDetail, form=VDMLDocumentDetailForm, extra=1)

#     if request.user.is_authenticated:
#         engineers = CustomUser.objects.filter(role__name="Engineer")
#         if request.method == "POST":
#             form = VDMLDocumentForm(request.POST)
#             detail_formset = VDMLDocumentDetailFormSet(request.POST, prefix='details')

#             # Check if both form and formset are valid without saving them
#             if form.is_valid() and detail_formset.is_valid():
#                 # Save the main VDML Document
#                 vdml_doc = form.save()

#                 # Save each detail form
#                 for detail_form in detail_formset:
#                     detail = detail_form.save(commit=False)
#                     detail.vdml_document = vdml_doc
#                     detail.save()

#                 messages.success(request, "VDML created successfully!")
#                 return redirect("vdml_view")
            
#             # Print form errors to terminal
#             for field, errors in form.errors.items():
#                 print(f"VDMLDocument form errors for {field}:", errors)
#             for detail_form in detail_formset:
#                 for field, errors in detail_form.errors.items():
#                     print(f"VDMLDocumentDetail formset errors for {field}:", errors)
#         else:
#             form = VDMLDocumentForm()
#             detail_formset = VDMLDocumentDetailFormSet(queryset=VDMLDocumentDetail.objects.none(), prefix='details')
#     else:
#         return redirect("login")
    
#     context = {
#         "form": form,
#         "detail_formset": detail_formset,
#         "engineers": engineers
#     }
#     return render(request, "pages/create_vdml_doc.html", context)
@login_required
def create_vdml_view(request):
    # Define the formset for VDMLDocumentDetail
    VDMLDocumentDetailFormSet = modelformset_factory(VDMLDocumentDetail, form=VDMLDocumentDetailForm, extra=1)

    
    engineers = CustomUser.objects.filter(role__name="Engineer")
    if request.method == "POST":
        form = VDMLDocumentForm(request.POST)
        formset = VDMLDocumentDetailFormSet(request.POST, prefix='detail')


        if form.is_valid() and formset.is_valid():
            vdml_document = form.save()
            for detail_form in formset:
                vdml_detail = detail_form.save(commit=False)
                vdml_detail.vdml_document = vdml_document
                vdml_detail.save()
            return redirect('vdml_view')  # Replace 'some_view_name' with the name of the view you want to redirect to after a successful submission.
        for field, errors in form.errors.items():
            print(f"VDMLDocument form errors for {field}:", errors)
        for form in formset:
            for field, errors in form.errors.items():
                print(f"VDMLDocumentDetail formset errors for {field}:", errors)

    else:
        form = VDMLDocumentForm()
        formset = VDMLDocumentDetailFormSet(queryset=VDMLDocumentDetail.objects.none(), prefix='detail')

    context = {
        'form': form,
        'formset': formset,
        'engineers': engineers,
    }
    return render(request, 'pages/vdml_test.html', context)  # Replace 'path_to_template.html' with the path to your template.

                