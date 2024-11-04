import csv
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from core.models import Log


@login_required
def logs(request):
    context = {"breadcrumb":{"parent":"Project","child":"Logs"}}
    return render(request, 'core/logs/logs.html', context=context)


@login_required
def export_to_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    current_date = datetime.now().strftime('%Y%m%d')
    file_name = f'report_logs_{current_date}.csv'

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="{}"'.format(file_name)},
    )

    writer = csv.writer(response)
    writer.writerow(["Date", "Project/Equipment", "Updates", "Updated By"])

    logs = Log.objects.all()
    for log in logs:
        writer.writerow(log.get_csv_data()) 
    return response
