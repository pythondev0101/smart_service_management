from django.urls import path
from .views import reset_password


app_name = 'accounts'

urlpatterns = [
    # path('profile', profile_profile, name='profile'),
    path('reset-password', reset_password, 'reset_password')
]