from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import error, success
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse
from accounts.services import sign_up_user


def login_user(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            context = {}
            return render(request, 'accounts/auth/login.html', context=context)
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is None:
            error(request, "Login failed, please try again")
            return redirect('login')

        login(request, user)
        return redirect('dashboard')


def logout_user(request):
    logout(request)
    return redirect('login')


def signup_user(request):
    if request.method == "GET":
        return render(request, 'accounts/auth/signup.html', context={})
    elif request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        business_name = request.POST['business_name']

        try:
            sign_up_user(
                fname=fname, 
                lname=lname,
                username=username,
                password=password,
                business_name=business_name
            )            
            success(request, 'Account created successfully!')
            return redirect('login')
        except IntegrityError:
            error(request, 'Username already exists')
            return redirect('signup')


@login_required
def reset_password(request):
    if request.method == "GET":
        return render(request, 'accounts/auth/reset_password.html', context={})
    elif request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if len(password) <= 5:
            error(request, "Password must be greater than to 5 characters!")
            return redirect('reset_password')

        if password != confirm_password:
            error(request, "Password does not match!")
            return redirect('reset_password')
        
        user = request.user
        user.set_password(password)
        user.save()

        logout(request)
        success(request, 'Password updated successfully!')
        return redirect('login')


@login_required
def users(request):
    if "Admin" not in [group.name for group in request.user.groups.all()]:
        return HttpResponse("You have no permission to view this page")

    context = {"breadcrumb":{"parent":"Account","child":"Users"}}
    return render(request, 'accounts/users/users.html', context=context)


@login_required
def user_create(request):
    if "Admin" not in [group.name for group in request.user.groups.all()]:
        return HttpResponse("You have no permission to view this page")

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']

        try:
            sign_up_user(
                fname=fname, 
                lname=lname,
                username=username,
                password=password
            )            
            success(request, 'Account created successfully!')
            return redirect('users')
        except IntegrityError:
            error(request, 'Username already exists')
            return redirect('user_create')

    context = {
        "breadcrumb":{"parent":"Account","child":"Create User"}
    }
    return render(request, 'accounts/users/create_new/usercreate.html', context=context)


@login_required
def user_edit(request, user_id):
    if "Admin" not in [group.name for group in request.user.groups.all()]:
        return HttpResponse("You have no permission to view this page")

    user = User.objects.get(pk=user_id)

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']

        try:
            user.first_name = fname
            user.last_name = lname
            user.username = username
            user.save()
            success(request, 'Account updated successfully!')
            return redirect('users')
        except IntegrityError:
            error(request, 'Username already exists')
            return redirect(request.META.get('HTTP_REFERER'))

    context = {
        "breadcrumb":{"parent":"Account","child":"Edit User"},
        "user": user
    }
    return render(request, 'accounts/users/edit/useredit.html', context=context)



# @login_required
# def profile_profile(request):
#     if request.method == "POST":
#         update_what = request.POST['update_what']
#         if update_what == "COMPANY":
#             profile_company_form = ProfileCompanyForm(request.POST)
#             profile_user_form = ProfileUserForm()

#             if profile_company_form.is_valid():
#                 account_edit(
#                     account_id=request.user.profile.account.id,
#                     name=profile_company_form.cleaned_data['name']
#                 )
#                 success(request, 'Company updated successfully!')
#                 return redirect('accounts:profile')
#         elif update_what == "USER":
#             profile_company_form = ProfileCompanyForm()
#             profile_user_form = ProfileUserForm(request.POST)

#             if profile_user_form.is_valid():
#                 user_edit(
#                     user_id=request.user.id,
#                     first_name=profile_user_form.cleaned_data['first_name'],
#                     last_name=profile_user_form.cleaned_data['last_name'],
#                     email=profile_user_form.cleaned_data['email'],
#                     username=profile_user_form.cleaned_data['username']
#                 )
#                 success(request, 'User updated successfully!')
#                 return redirect('accounts:profile')
#     else:
#         profile_company_form = ProfileCompanyForm()
#         profile_user_form = ProfileUserForm()

#     user = request.user
#     context={
#         "user": user,
#         "breadcrumb":{"parent":"Profile","child":"Profile Edit"},
#         "profile_company_form": profile_company_form,
#         "profile_user_form": profile_user_form
#     }
#     print(profile_company_form.errors)
#     return render(request, 'accounts/profile/profile.html', context=context)


# @require_http_methods(["POST"])
# @login_required
# def profile_user_edit(request):
#     pass


# @require_http_methods(["POST"])
# @login_required
# def profile_company_edit(request):

@login_required
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()

    success(request, 'Account deleted successfully!')
    return redirect('users')