from django.shortcuts import render, redirect
from lowongan.models import Lowongan

URL_CARI_LOWONGAN = '/cari-lowongan/'
TEMPLATE_CARI_LOWONGAN = 'cari_lowongan.html'

filter_obj = Lowongan.objects.filter()
template = 'cari_lowongan.html'
redirect_url = '/cari-lowongan/'

def cari_lowongan(request):
    if request.method == 'GET':
        obj_lowongan = filter_obj.order_by('-id')
        response = {
            'data': obj_lowongan
        }
        return render(request, TEMPLATE_CARI_LOWONGAN, response)
    else:
        return redirect(URL_CARI_LOWONGAN)


def sort_by_waktu_magang(request, param):
    if request.method == 'GET':
        response = {}
        if param == 'asc':
            obj_lowongan = filter_obj.order_by('waktu_awal_magang')
            response['data'] = obj_lowongan
            return render(request, TEMPLATE_CARI_LOWONGAN, response)
        elif param == 'desc':
            obj_lowongan = filter_obj.order_by('-waktu_awal_magang')
            response['data'] = obj_lowongan
            return render(request, TEMPLATE_CARI_LOWONGAN, response)
        else:
            return redirect(URL_CARI_LOWONGAN)
    else:
        return redirect(URL_CARI_LOWONGAN)


def sort_by_batas_akhir(request, param):
    if request.method == 'GET':
        response = {}
        if param == 'asc':
            obj_lowongan = filter_obj.order_by('batas_akhir_pendaftaran')
            response['data'] = obj_lowongan
            return render(request, TEMPLATE_CARI_LOWONGAN, response)
        elif param == 'desc':
            obj_lowongan = filter_obj.order_by('-batas_akhir_pendaftaran')
            response['data'] = obj_lowongan
            return render(request, TEMPLATE_CARI_LOWONGAN, response)
        else:
            return redirect(URL_CARI_LOWONGAN)
    else:
        return redirect(URL_CARI_LOWONGAN)


def search_by_judul(request, param):
    if request.method == 'GET':
        response = {}
        obj_lowongan = Lowongan.objects.filter(
            judul__contains=param).order_by('judul')
        response['data'] = obj_lowongan
        return render(request, TEMPLATE_CARI_LOWONGAN, response)
    else:
        return redirect(URL_CARI_LOWONGAN)
