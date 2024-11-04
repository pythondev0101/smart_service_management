from django.urls import path
from .views import *
from .datatables import *
from .api import get_project


urlpatterns = [
    path('ongoing-projects', ongoing_projects, name='ongoing_projects'),
    path('projects/create', project_create, name='project_create'),
    path('projects/<int:project_id>', project_edit, name='project_edit'),
    path('projects/<int:project_id>/set-as-complete', project_set_as_complete, name='project_set_as_complete'),
    path('projects/dt/ongoing-projects', dt_ongoing_projects, name='dt_ongoing_projects'),
    path('employees/dt/employees', dt_employees, name='dt_employees'),
    path('sites/dt/sites', dt_sites, name='dt_sites'),
    path('schedules/dt/schedules', dt_schedules, name='dt_schedules'),
    path('employees', employees, name='employees'),
    path('employees/create', employee_create, name='equipment_create'),
    path('employees/<int:equipment_id>', equipment_edit, name='equipment_id'),
    path('employees/upload-photo', equipment_upload_photo, name='equipment_upload_photo'),
    path('sites', sites, name='sites'),
    path('sites/create', site_create, name='site_create'),
    path('schedules', schedules, name='schedules'),
    path('schedules/create', schedule_create, name='schedule_create'),
    path('logs/dt/logs', dt_logs, name='dt_logs'),
    path('logs', logs, name='logs'),
    path('export-to-csv', export_to_csv, name='export_to_csv'),
    path('api/projects/<int:project_id>', get_project)
]
