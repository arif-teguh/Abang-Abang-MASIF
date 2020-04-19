from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import logout


def landing(request):
    return render(request, 'landing_page.html')

def landing_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
