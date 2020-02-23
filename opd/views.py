from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def opd_login(request):
    return render(request, 'opdLogin.html')

