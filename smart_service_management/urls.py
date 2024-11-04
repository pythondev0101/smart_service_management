"""
URL configuration for smart_service_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import index, dashboard
from accounts.views import (
    login_user, logout_user, signup_user, reset_password,
    users, user_create, user_edit, delete_user
)
from accounts.datatables import (
    dt_users
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('adminsite/', admin.site.urls),
    path('', index, name='root'),
    path('dashboard', dashboard, name='dashboard'),
    path('', include('core.urls')),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('signup/', signup_user, name='signup'),
    path('reset-password/', reset_password, name='reset_password'),
    path('users/', users, name='users'),
    path('users/create', user_create, name='user_create'),
    path('users/<int:user_id>', user_edit, name='user_edit'),
    path('users/<int:user_id>/delete', delete_user, name='user_delete'),
    path('accounts/dt/users', dt_users, name='dt_users'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
