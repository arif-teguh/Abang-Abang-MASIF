from django.http import HttpResponse
from django.shortcuts import render

def show_form_lowongan(request):
    return render(request, 'lowongan/form_lowongan.html')