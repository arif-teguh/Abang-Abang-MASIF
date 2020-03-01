from django.shortcuts import render


# Create your views here.

def cari_lowongan(request):
    return render(request, 'cari_lowongan.html')
