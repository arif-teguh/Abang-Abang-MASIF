from django.shortcuts import render , redirect
from django.http import HttpResponse
from lowongan.models import Lowongan
# Create your views here.
def opd_login(request):
    return render(request,'opd_login.html')

def opd_index(request):
    if request.user.is_authenticated and not request.user.is_admin and request.user.is_opd and not request.user.is_user:
        return HttpResponse("<h1>opd PAGE, Under Construction</h1>")
    else:
        return redirect('/account-redirector')

def opd_lowongan(request):
    list_lowongan = Lowongan.objects.all()
    return render(request,'opd_lowongan.html', {'list_lowongan': list_lowongan})

def opd_detail_lowongan(request,id_lowongan):
    lowongan = Lowongan.objects.get(id = id_lowongan)
    return render(request,'opd_detail_lowongan.html' , {'lowongan': lowongan})