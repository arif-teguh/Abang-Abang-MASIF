from django.shortcuts import render , redirect
from django.http import HttpResponse
# Create your views here.
def opd_login(request):
    return render(request,'opd_login.html')
