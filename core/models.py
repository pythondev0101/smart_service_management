from datetime import datetime
from dateutil import tz
from django.db import models
from django.contrib.auth.models import User


UTC = tz.gettz('UTC')
MANILA = tz.gettz('Asia/Manila')


class Project(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    name = models.CharField(max_length=255)
    location_address1 = models.CharField(max_length=255, null=True)
    location_address2 = models.CharField(max_length=255, null=True)
    location_city = models.CharField(max_length=255, null=True)
    location_province = models.CharField(max_length=255, null=True)
    location_zip_code = models.CharField(max_length=255, null=True)
    borehole_quantity = models.IntegerField()
    borehole_depth_meters = models.DecimalField(decimal_places=2, max_digits=10)
    duration_days = models.IntegerField()
    pe_pm = models.ForeignKey(User, on_delete=models.RESTRICT)
    status = models.CharField(max_length=64, default="ONGOING")

    def __str__(self):
        return self.name

    @property    
    def location_full(self):
        return "{address1}, {address2}, {city}, {province} {zip}".format(
            address1=self.location_address1,
            address2=self.location_address2,
            city=self.location_city,
            province=self.location_province,
            zip=self.location_zip_code
        )

    def get_dt_json(self, page='ongoing_projects'):
        if page == "ongoing_projects":
            return [
                self.id,
                (self.name, self.location_full),
                self.borehole_quantity,
                self.borehole_depth_meters,
                self.duration_days,
                '',
                '',
                self.pe_pm.get_full_name(),
                self.status
            ]
        elif page == "dashboard":
            return [
                self.get_created_date_local(),
                (self.name, self.location_full),
                self.status
            ]
        else:
            return []        

    def get_created_date_local(self, format="%B %d %Y %I:%M %p"):
        utc = self.created_date.replace(tzinfo=UTC)
        return utc.astimezone(MANILA).strftime(format)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'equipments': [
                equipment.to_json() for equipment in self.equipments.all()
            ]
        }


class Employee(models.Model):
    employee_no = models.IntegerField(verbose_name="Employee No.")
    fname = models.CharField(max_length=255, verbose_name="First Name")
    lname = models.CharField(max_length=255, verbose_name="Last Name")
    position = models.CharField(max_length=255, verbose_name="Position", default="")
    # status = models.CharField(max_length=255, verbose_name="Capacity Code")
    
    @property
    def full_name(self):
        return f'{self.fname} {self.lname}'

    def get_dt_json(self, page="employees"):
        if page == "employees":
            return [
                self.id,
                self.employee_no,
                self.fname,
                self.lname,
                self.position,
                ''
            ]
        else:
            raise Exception("Project Error: page is not valid")

    def __str__(self):
        return self.full_name


class Site(models.Model):
    site_ea = models.IntegerField(verbose_name="Site EA")
    smart_site_id = models.CharField(max_length=255, verbose_name="Site ID")
    name = models.CharField(max_length=255, verbose_name="Site ID")
    address = models.CharField(max_length=255, verbose_name="Address")
    municipality = models.CharField(max_length=255, verbose_name="Municipality")
    province = models.CharField(max_length=255, verbose_name="Province")
    classification = models.CharField(max_length=255, verbose_name="Classification")
    location = models.CharField(max_length=255, verbose_name="Location")
    longitude = models.FloatField(verbose_name="Longitude")
    latitude = models.FloatField(verbose_name="Latitude")

    def get_dt_json(self, page="sites"):
        if page == "sites":
            return [
                self.id,
                self.site_ea,
                self.smart_site_id,
                self.name,
                self.municipality,
                self.province,
                self.classification,
                self.location,
                self.longitude,
                self.latitude,
                '',
                ''
            ]
        else:
            raise Exception("Project Error: page is not valid")

    def __str__(self):
        return f'{self.smart_site_id} - {self.name}'


class Schedule(models.Model):
    site = models.ForeignKey('Site', related_name='sites', null=True, on_delete=models.SET_NULL)
    employee = models.ForeignKey('Employee', related_name='employees', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=64, default="ACTIVE", verbose_name="Status")
    start_date = models.DateTimeField(auto_now_add=True)

    def get_start_date_local(self, format="%B %d %Y %I:%M %p"):
        utc = self.start_date.replace(tzinfo=UTC)
        return utc.astimezone(MANILA).strftime(format)

    def get_dt_json(self, page="schedules"):
        if page == "schedules":
            return [
                self.id,
                self.get_start_date_local(),
                self.site.name,
                self.employee.full_name,
                self.status,
                ''
            ]
        else:
            raise Exception("Project Error: page is not valid")


class Equipment(models.Model):
    line_no = models.IntegerField(verbose_name="Line No.")
    machine_id = models.CharField(max_length=255, verbose_name="Machine ID")
    model = models.CharField(max_length=255, verbose_name="Model")
    capacity_code = models.CharField(max_length=255, verbose_name="Capacity Code")
    year = models.IntegerField(null=True, verbose_name="Year")
    tripod = models.IntegerField(null=True, verbose_name="Tripod")
    water_pump = models.IntegerField(null=True, verbose_name="Water Pump")
    toolbox = models.IntegerField(null=True, verbose_name="Toolbox")
    pipe_wrench_pair = models.IntegerField(null=True, verbose_name="Pipe Wrench Pair")
    casing = models.IntegerField(null=True, verbose_name="Casing")
    rod = models.IntegerField(null=True, verbose_name="Rod")
    reamer = models.IntegerField(null=True, verbose_name="Reamer")
    diamond_bit = models.IntegerField(null=True, verbose_name="Diamond Bit")
    spt_hammer = models.IntegerField(null=True, verbose_name="SPT Hammer")
    spt_sampler = models.IntegerField(null=True, verbose_name="SPT Sampler")
    fire_ext = models.IntegerField(null=True, verbose_name="Fire Ext")
    cm_tank = models.IntegerField(null=True, verbose_name="CM Tank")
    l_tank = models.IntegerField(null=True, verbose_name="L Tank")
    fuel_tank = models.IntegerField(null=True, verbose_name="Fuel Tank")
    maintenance_date = models.DateField(verbose_name="Maintenance Date")
    maintenance_due_date = models.DateField(null=True, verbose_name="Maintenance Due Date")
    last_assignment_date = models.DateField(null=True, verbose_name="Last Assignment Date")
    mobilization_date = models.DateField(null=True, verbose_name="Date of Mobilization")
    demobilization_date = models.DateField(null=True, verbose_name="Date of Demobilization")
    delivered_by_fname = models.CharField(max_length=255, null=True, default='')
    delivered_by_lname = models.CharField(max_length=255, null=True, default='')
    received_by_fname = models.CharField(max_length=255, null=True, default='')
    received_by_lname = models.CharField(max_length=255, null=True, default='')
    operator_fname = models.CharField(max_length=255, null=True, default='')
    operator_lname = models.CharField(max_length=255, null=True, default='')
    project = models.ForeignKey('Project', related_name='equipments', null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=64, default="AVAILABLE", verbose_name="Status")

    def __str__(self):
        return self.machine_id

    def get_dt_json(self, page="equipments"):
        if page == "equipments":
            return [
                self.id,
                self.line_no,
                self.machine_id,
                self.model,
                self.capacity_code,
                self.year,
                self.maintenance_date,
                self.maintenance_due_date,
                self.last_assignment_date,
                self.status
            ]
        elif page == "search-rig-line-modal":
            return [
                self.id,
                self.line_no,
                self.machine_id,
                self.maintenance_date,
                self.maintenance_due_date,
                self.last_assignment_date,
                self.status,
                ''
            ]
        else:
            raise Exception("Project Error: page is not valid")
        
    def to_json(self):
        return {
            'id': self.id,
            'line_no': self.line_no,
            'machine_id': self.machine_id,
            'status': self.status
        }


class Log(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=64) # Ex. project, equipment
    model_id = models.IntegerField() # Ex. projectA.id
    name = models.CharField(max_length=255) # Ex. ProjectName
    updates = models.CharField(max_length=1064)
    updated_by = models.CharField(max_length=255)

    def get_dt_json(self):
        return [
            self.model_id,
            self.get_created_date_local(),
            self.model,
            self.updates,
            self.updated_by
        ]

    def get_csv_data(self):
        return [
            self.get_created_date_local(),
            self.model,
            self.updates,
            self.updated_by
        ]

    def get_created_date_local(self, format="%B %d %Y %I:%M %p"):
        utc = self.created_date.replace(tzinfo=UTC)
        return utc.astimezone(MANILA).strftime(format)


class EquipmentPhoto(models.Model):
    equipment = models.ForeignKey('Equipment', related_name='photos', null=True, on_delete=models.SET_NULL)
    path = models.ImageField(upload_to='uploads/')
    name = models.CharField(max_length=255, null=True, default='')
