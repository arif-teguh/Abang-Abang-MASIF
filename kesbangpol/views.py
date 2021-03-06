from datetime import datetime
import tempfile

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from account.models import UserProfile
from lowongan.models import UserLamarMagang
from .kesbangpol_login_form import KesbangpolAuthenticationForm
# Create your views here.
def kesbangpol_login(request):
    err = []
    if request.method == 'POST':
        form = KesbangpolAuthenticationForm(request.POST)
        if form.is_valid():
            try:
                form.check()
                email = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/kesbangpol/')
            except ValidationError as e:
                err = e
    else:
        form = KesbangpolAuthenticationForm()

    return render(request, 'kesbangpol_login.html', {'form': form, 'err': err})

def kesbangpol_dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/kesbangpol/login')
    
    if not request.user.is_kesbangpol:
        return HttpResponseRedirect('/')

    user_diterima_opd = UserLamarMagang.objects.filter(
        status_lamaran="DITERIMA")
    return render(request, 'kesbangpol_dashboard.html',
                  {'user_diterima': user_diterima_opd,
                   'kesbangpol': request.user})

@csrf_exempt
def get_user_lamaran_detail(request, user_lamar_id):
    try:
        user_lamar = UserLamarMagang.objects.get(id=user_lamar_id)
        user_account = user_lamar.user_foreign_key
        user_profile = UserProfile.objects.get(user=user_account)
        lowongan = user_lamar.lowongan_foreign_key
        durations = lowongan.waktu_akhir_magang - lowongan.waktu_awal_magang
        data = {
            'name': user_account.name,
            'institution': user_profile.institution,
            'opd': lowongan.opd_foreign_key.name,
            'judul': lowongan.judul,
            'bagian': lowongan.kategori,
            'durasi': durations.days,
        }
        return JsonResponse(data)

    except UserLamarMagang.DoesNotExist:
        err = {'err': 'User Not Exist'}
        return JsonResponse(err)

@csrf_exempt
def post_jadwal_lamaran_kesbangpol(request, user_lamar_id):
    try:
        user_lamar = UserLamarMagang.objects.get(id=user_lamar_id)
        request_data = request.POST.get('tanggal_kesbangpol', None)
        request_data = request_data.strip()
        date_object = datetime.strptime(request_data, '%d/%m/%Y').date()
        user_lamar.tanggal_kesbangpol = date_object
        user_lamar.status_kesbangpol = "DITERIMA"
        user_lamar.save()
        data = {
            'success': "Success update date"
        }
        return JsonResponse(data)

    except UserLamarMagang.DoesNotExist:
        err = {'err': 'User Not Exist'}
        return JsonResponse(err)
    except ValueError:
        err = {'err': 'Invalid date format'}
        return JsonResponse(err)

def get_rekomendasi_pdf(request, user_lamar_id):
    data = {}
    try:
        user_lamar = UserLamarMagang.objects.get(id=user_lamar_id)
        user_lamar.status_kesbangpol = "DITERIMA"
        user_lamar.save()
        user_account = user_lamar.user_foreign_key
        user_profile = UserProfile.objects.get(user=user_account)
        lowongan = user_lamar.lowongan_foreign_key
        name = user_account.name
        institution = user_profile.institution
        address = user_profile.address
        contact = user_account.phone
        title = lowongan.judul
        location = lowongan.opd_foreign_key.name
        magang_start = lowongan.waktu_awal_magang
        magang_end = lowongan.waktu_akhir_magang
        duration = magang_start.strftime("%d/%m/%Y") + ' s.d. '+ magang_end.strftime("%d/%m/%Y")
        category = lowongan.kategori
        data = {
            "name": name,
            "institution": institution,
            "address": address,
            "contact": contact,
            "title": title,
            "location": location,
            "duration": duration,
            "category": category
        }
        html_template = render_to_string('kesbangpol_pdf.html', data)
        pdf_file = HTML(string=html_template).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="rekomendasi.pdf"'
    except UserLamarMagang.DoesNotExist:
        response = HttpResponseRedirect('/kesbangpol/')
    return response
