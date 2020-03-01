from django.http import HttpResponse
from django.shortcuts import render, redirect


def admin_login(request):
    return render(request, 'admin/admin_login.html')


def admin_index(request):
    if request.user.is_authenticated and request.user.is_admin and not request.user.is_opd and not request.user.is_user:
        return render(request, 'admin/admin_index.html')
    else:
        return redirect('/account-redirector')
