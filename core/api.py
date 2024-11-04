import json
from django.http import JsonResponse
from core.models import Project


def get_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    result = project.to_json()
    return JsonResponse(result)
