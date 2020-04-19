from django.shortcuts import render
from lowongan.models import Lowongan


# Create your views here.

def detail_lowongan(request, id_lowongan):
    obj_lowongan = Lowongan.objects.filter(id=id_lowongan)
    response = {
        'data': obj_lowongan
    }
    return render(request, 'detail_lowongan.html', response)
