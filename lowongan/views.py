from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def show_form_lowongan(request):
    return HttpResponse("<h1>test<h1>")