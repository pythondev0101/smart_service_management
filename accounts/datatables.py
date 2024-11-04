from django.http import JsonResponse
from django.db.models import Q
from .models import User


def dt_users(request):
    draw = request.GET['draw']
    start, length = int(request.GET['start']), int(request.GET['length'])
    users = User.objects.filter(is_active=True).all()[start:length]
    data = []

    for user in users:
        data.append([
            user.id,
            user.username,
            user.first_name,
            user.last_name,
            ''
        ])

    filtered_records = len(data)
    total_records = User.objects.count()
    response = {
        'draw': draw,
        'recordsTotal': filtered_records,
        'recordsFiltered': total_records,
        'data': data,
    }
    return JsonResponse(response)

