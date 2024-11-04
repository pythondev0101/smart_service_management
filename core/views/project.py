from django.shortcuts import render, redirect
from django.contrib.messages import success
from django.contrib.auth.decorators import login_required
from django.db import transaction
from core.models import Project, Log, Equipment
from core.forms import ProjectForm


@login_required
def ongoing_projects(request):
    context = {"breadcrumb":{"parent":"Project","child":"Ongoing Projects"}}
    return render(request, 'core/project/ongoing_projects/ongoing_projects.html', context=context)


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                project = form.save()

                # Update equipment's project and status
                for equipment in form.cleaned_data['equipments']:
                    equipment.project = project
                    equipment.status = "ACTIVE"
                    equipment.save()

                # Create log
                updates = f'New project created'
                user_full_name = request.user.get_full_name()
                log = Log.objects.create(
                    model=project.name,
                    model_id=project.id,
                    updates=updates,
                    updated_by=user_full_name
                )
                log.save()                      
            success(request, 'Project created successfully!')
            return redirect('ongoing_projects')
    else:
        form = ProjectForm()

    context = {
        "breadcrumb":{"parent":"Project","child":"Create Project"},
        "form": form
    }
    return render(request, 'core/project/create_new/projectcreate.html', context=context)


@login_required
def project_edit(request, project_id):
    project = Project.objects.get(id=project_id)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            with transaction.atomic():
                user_full_name = request.user.get_full_name()

                # Update equipment's project and status
                project_equipments = Equipment.objects.filter(project=project).all()
                print("project_equipments", project_equipments)
                for old_equipment in project_equipments:
                    old_equipment.status = "AVAILABLE"
                    old_equipment.project = None
                    old_equipment.save()

                for new_equipment in form.cleaned_data['equipments']:
                    new_equipment.project = project
                    new_equipment.status = "ACTIVE"
                    new_equipment.save()

                # Create logs
                for changed_field in form.changed_data:
                    if changed_field == "status":
                        continue

                    updates = "{field} updated to {new_value}".format(
                        field=changed_field.replace('_', ' ').capitalize(),
                        new_value=getattr(project, changed_field)
                    )

                    log = Log.objects.create(
                        model=project.name,
                        model_id=project.id,
                        updates=updates,
                        updated_by=user_full_name
                    )
                    log.save()   
                project = form.save()
            success(request, 'Project updated successfully!')
            return redirect('ongoing_projects')

    context = {
        "breadcrumb":{"parent":"Project","child":"Edit Project"},
        "form": form
    }
    return render(request, 'core/project/edit/projectedit.html', context=context)


@login_required
def project_set_as_complete(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method == "POST":
        with transaction.atomic():
            if project.status == "ONGOING":
                project.status = "COMPLETED"
                updates = "Project completed"
            elif project.status == "COMPLETED":
                project.status = "ONGOING"
                updates = "Project undo complete"
            project.save()

            # Create logs
            user_full_name = request.user.get_full_name()
            log = Log.objects.create(
                model=project.name,
                model_id=project.id,
                updates=updates,
                updated_by=user_full_name
            )
            log.save()   
        success(request, 'Project updated successfully!')
        return redirect('ongoing_projects')
