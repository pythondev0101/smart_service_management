from django.http import JsonResponse
from django.db.models import Q
from .models import *


def dt_ongoing_projects(request):
    draw = request.GET['draw']
    start, length = int(request.GET['start']), int(request.GET['length'])
    projects = Project.objects.order_by('-created_date').all()[start:length]
    page = request.GET.get('page', 'ongoing_projects')
    data = []

    for project in projects:
        data.append(project.get_dt_json(page=page))

    filtered_records = len(data)
    total_records = Project.objects.count()
    response = {
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': total_records,
        'data': data,
    }
    return JsonResponse(response)


def dt_employees(request):
    draw = request.GET['draw']
    start, length = int(request.GET['start']), int(request.GET['length'])
    page = request.GET.get('page', 'employees')

    if page not in ['employees']:
        raise Exception("Project Error: page is not valid")

    data = []
    if page == 'employees':
        employees = Employee.objects.all()[start:length]

    for employee in employees:
        data.append(employee.get_dt_json(page=page))

    print(data)
    filtered_records = len(data)
    total_records = Employee.objects.count()
    response = {
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': total_records,
        'data': data,
    }
    return JsonResponse(response)


def dt_sites(request):
    draw = request.GET['draw']
    start, length = int(request.GET['start']), int(request.GET['length'])
    page = request.GET.get('page', 'sites')

    if page not in ['sites']:
        raise Exception("Project Error: page is not valid")

    data = []
    if page == 'sites':
        sites = Site.objects.all()[start:length]

    for site in sites:
        data.append(site.get_dt_json(page=page))

    filtered_records = len(data)
    total_records = Site.objects.count()
    response = {
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': total_records,
        'data': data,
    }
    return JsonResponse(response)


def dt_schedules(request):
    draw = request.GET['draw']
    start, length = int(request.GET['start']), int(request.GET['length'])
    page = request.GET.get('page', 'schedules')

    if page not in ['schedules']:
        raise Exception("Project Error: page is not valid")

    data = []
    if page == 'schedules':
        schedules = Schedule.objects.all()[start:length]

    for site in schedules:
        data.append(site.get_dt_json(page=page))

    filtered_records = len(data)
    total_records = Schedule.objects.count()
    response = {
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': total_records,
        'data': data,
    }
    return JsonResponse(response)


def dt_logs(request):
    draw = request.GET['draw']
    start, length = int(request.GET['start']), int(request.GET['length'])
    logs = Log.objects.order_by('-created_date').all()[start:length]
    data = []

    for log in logs:
        data.append(log.get_dt_json())

    filtered_records = len(data)
    total_records = Log.objects.count()
    response = {
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': total_records,
        'data': data,
    }
    return JsonResponse(response)

