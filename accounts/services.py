from accounts.models import Profile
from django.contrib.auth.models import User
from django.db import transaction


def sign_up_user(**kwargs):
    fname = kwargs.get('fname')
    lname = kwargs.get('lname')
    username = kwargs.get('username')
    password = kwargs.get('password')

    with transaction.atomic():
        user = User.objects.create(
            first_name=fname,
            last_name=lname,
            username=username
        )
        user.set_password(password)
        user.save()
    return user


# def user_edit(user_id, **kwargs):
#     user = User.objects.get(pk=user_id)
#     user.first_name = kwargs.get('first_name')
#     user.last_name = kwargs.get('last_name')
#     user.username = kwargs.get('username')
#     user.email = kwargs.get('email')
#     user.save()
#     return user
