from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def account_redirector(request):
    if request.user.is_authenticated:
        if request.user.is_opd:
            return redirect('/opd')
        elif request.user.is_admin:
            return redirect('/admin')

    return redirect('/')

