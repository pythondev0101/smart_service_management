from django.shortcuts import render, redirect
from django.contrib.messages import success, error
from django.contrib.auth.decorators import login_required
from django.db import transaction
from core.forms import EmployeeForm, EquipmentPhotoForm
from core.models import Equipment, Log


@login_required
def employees(request):
    context = {"breadcrumb":{"parent":"Employee","child":"Employees"}}
    return render(request, 'core/employee/employees/employees.html', context=context)


@login_required
def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                employee = form.save()
                updates = f'New employee'
                user_full_name = request.user.get_full_name()
                log = Log.objects.create(
                    model=employee.employee_no,
                    model_id=employee.id,
                    updates=updates,
                    updated_by=user_full_name
                )
                log.save()                        
            success(request, 'Employee was created successfully!')
            return redirect('employees')
    else:
        form = EmployeeForm()

    context = {
        "breadcrumb":{"parent":"Employee","child":"Create Employee"},
        "form": form
    }
    return render(request, 'core/employee/create_new/create.html', context=context)


@login_required
def equipment_edit(request, equipment_id):
    equipment = Equipment.objects.get(id=equipment_id)
    form = EquipmentForm(instance=equipment)
    for photo in equipment.photos.all():
        print(photo.path.url)

    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)

        if form.is_valid():
            print("The following fields changed: %s" % ", ".join(form.changed_data))
            with transaction.atomic():
                user_full_name = request.user.get_full_name()

                for changed_field in form.changed_data:
                    if changed_field == "status":
                        continue

                    updates = "{field} updated to {new_value}".format(
                        field=changed_field.replace('_', ' ').capitalize(),
                        new_value=getattr(equipment, changed_field)
                    )

                    log = Log.objects.create(
                        model=equipment.machine_id,
                        model_id=equipment.id,
                        updates=updates,
                        updated_by=user_full_name
                    )
                    log.save()                        
                equipment = form.save()
            success(request, 'Rig Line updated successfully!')
            return redirect('equipments')

    context = {
        "breadcrumb":{"parent":"Equipment","child":"Edit Equipment"},
        "form": form,
        "equipment_photo_form": EquipmentPhotoForm()
    }
    return render(request, 'core/equipment/edit/equipment_edit.html', context=context)


def equipment_upload_photo(request):
    if request.method == 'POST':
        form = EquipmentPhotoForm(request.POST, request.FILES)
  
        if form.is_valid():
            form.save()
            success(request, 'Photo uploaded successfully!')
            return redirect(request.META.get('HTTP_REFERER'))
    print(form.errors)
    error(request, 'Failed to upload!')
    return redirect(request.META.get('HTTP_REFERER'))
