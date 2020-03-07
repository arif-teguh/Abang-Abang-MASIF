from django.shortcuts import render, redirect
from lowongan.models import Lowongan


# Create your views here.


def cari_lowongan(request):
    obj_lowongan = Lowongan.objects.all()
    response = {
        'data': obj_lowongan
    }
    return render(request, 'cari_lowongan.html', response)
