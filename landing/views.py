from django.contrib.auth import logout
from django.shortcuts import render, HttpResponseRedirect

from artikel.models import Artikel
from lowongan.models import Lowongan


def query_n_number_of_newest_lowongan(n):
    return Lowongan.objects.filter(is_lowongan_masih_berlaku=True).order_by('-id')[:n]
    
def landing(request):
    list_of_lowongan = query_n_number_of_newest_lowongan(7)
    context = {
        'lowongans': list_of_lowongan,
        'articles': Artikel.objects.all(),
    }
    return render(request, 'landing_page.html', context)


def landing_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
