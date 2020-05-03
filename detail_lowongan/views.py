from django.shortcuts import render
from lowongan.models import Lowongan
from account.models import UserProfile

# Create your views here.

def detail_lowongan(request, id_lowongan):
    obj_lowongan = Lowongan.objects.filter(id=id_lowongan)
    kelengkapan = 'lengkap'
    if(request.user.is_authenticated):
        pelamar = request.user.userprofile
        if(pelamar.address ==  'Not set' or 
            pelamar.institution ==  'Not set' or 
            pelamar.education ==  'Not set'):
            kelengkapan = 'tidak_lengkap'
    else :
        kelengkapan = 'tidak_lengkap'
    response = {
        'data': obj_lowongan , 
        'status' : kelengkapan
    }
    return render(request, 'detail_lowongan.html', response)
