from django.http import HttpResponse
from django.shortcuts import render, redirect

def user_is_admin(request):
    return request.user.is_authenticated and request.user.is_admin and not request.user.is_opd and not request.user.is_user

def admin_login(request):
    return render(request, 'admin/admin_login.html')


def admin_index(request):
    if user_is_admin(request):
        return render(request, 'admin/admin_index.html')
    else:
        return redirect('/account-redirector')

def admin_list_opd(request):
    if user_is_admin(request):
        return render(request, 'admin/admin_list_opd.html')
    else:
        return redirect('/account-redirector')