from django import forms
from core.models import *
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    equipments = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects, required=True
    )

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['pe_pm'].empty_label = None
        self.fields['status'].required = False
        self.fields['pe_pm'].queryset = User.objects.filter(is_active=True).all()

    class Meta:
        model = Project
        fields = "__all__"


class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Employee
        fields = "__all__"


class SiteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SiteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Site
        fields = "__all__"


class ScheduleForm(forms.ModelForm):
    # equipments = forms.ModelMultipleChoiceField(
    #     queryset=Equipment.objects, required=True
    # )

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        # self.fields['pe_pm'].empty_label = None
        self.fields['status'].required = False
        # self.fields['site'].queryset = Site.objects.filter(is_active=True).all()
        # self.fields['employee'].queryset = Employee.objects.filter(is_active=True).all()

    class Meta:
        model = Schedule
        fields = "__all__"


class EquipmentPhotoForm(forms.ModelForm):
    class Meta:
        model = EquipmentPhoto
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super(EquipmentPhotoForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False

