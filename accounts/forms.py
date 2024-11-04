from django import forms


class ProfileCompanyForm(forms.Form):
    name = forms.CharField(required=True, max_length=255)


class ProfileUserForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=255)
    last_name = forms.CharField(required=True, max_length=255)
    email = forms.EmailField(required=False)
    username = forms.CharField(required=True, max_length=255)


