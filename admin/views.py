from django.http import HttpResponse
from django.shortcuts import render


def admin_login(request):
    return render(request, 'admin/admin_login.html')


def admin_index(request):
    return HttpResponse("<h1>Hello</h1>")
