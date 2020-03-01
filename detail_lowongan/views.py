from django.shortcuts import render


# Create your views here.

def detail_lowongan(request):
    return render(request, 'detail_lowongan.html')
