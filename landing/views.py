from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import logout

from lowongan.models import Lowongan


def query_n_number_of_newest_lowongan(n):
    return Lowongan.objects.all().order_by('-id')[:n]
    
def landing(request):
    list_of_lowongan = query_n_number_of_newest_lowongan(7)
    context = {
        'lowongans': list_of_lowongan
    }
    return render(request, 'landing_page.html', context)

def landing_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
