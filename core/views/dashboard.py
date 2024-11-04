from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')


@login_required
def dashboard(request):
    context = {
        "breadcrumb":{"parent":"Dashboard","child":"Dashboard"},
    }
    return render(request, 'core/dashboard/dashboard.html', context=context)
