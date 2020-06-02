from django.shortcuts import render
from lowongan.models import Lowongan
from account.models import UserProfile

# Create your views here.

def detail_lowongan(request, id_lowongan):
    obj_lowongan = Lowongan.objects.filter(id=id_lowongan)
    kelengkapan = 'tidak_lengkap'
    if(request.user.is_authenticated):
        user_is_user = request.user.is_user 
        if(user_is_user) :
            pelamar = request.user.userprofile
            not_set = 'Not set'
            if( (Lowongan.objects.get(pk=id_lowongan).is_lowongan_masih_berlaku) == True and
                pelamar.address !=  not_set and
                pelamar.institution !=  not_set and
                pelamar.education !=  not_set and
                pelamar.sex !=  'n'  ):
                kelengkapan = 'lengkap'
    response = {
        'data': obj_lowongan , 
        'status' : kelengkapan
    }
    return render(request, 'detail_lowongan.html', response)
