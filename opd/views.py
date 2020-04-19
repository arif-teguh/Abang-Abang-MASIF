from django.shortcuts import render , redirect
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist 
from lowongan.models import Lowongan , UserLamarMagang
from django.shortcuts import render, redirect

from lowongan.models import Lowongan
from admin.models import OpdVerificationList
from account.models import Account, OpdProfile
from .opd_confirmation_form import OpdConfirmationForm

opd_home = '/opd/'
URL_OPD_LOGIN = '/opd/login/'

def opd_login(request):
    return render(request, 'opd_login.html')

def opd_update_lamaran(request , id_lowongan , id_user , status , catatan):
    try :
        userlamarmagang = UserLamarMagang.objects.get(user_foreign_key = id_user , lowongan_foreign_key = id_lowongan)
        if(cek_id_lowongan_dan_opd(request , id_lowongan)):
            userlamarmagang.status_lamaran = status
            userlamarmagang.notes_status_lamaran = catatan
            userlamarmagang.save()
            return redirect('/opd/lowongan/list-pendaftar-'+id_lowongan+'/')
        else :
            return redirect(opd_home)
    except ObjectDoesNotExist :
        return redirect(opd_home)


def opd_list_pendaftar(request, id_lowongan):
    #cek apakah user sudah login dan user harus opd
    if request.user.is_authenticated and request.user.is_opd:
        if(cek_id_lowongan_dan_opd(request, id_lowongan)):
            lowongan = Lowongan.objects.get(id = id_lowongan)
            lamaran = UserLamarMagang.objects.filter(lowongan_foreign_key = id_lowongan)
            return render(request,'opd_list_pendaftar.html',
            {'lowongan': lowongan ,
              'lamaran' : lamaran
               } )
        else:
            return redirect(opd_home)
    else:
        return redirect('/opd/login/')


def opd_download_file(request ,id_user , id_lowongan):
    try:
        userlamarmagang = UserLamarMagang.objects.get(user_foreign_key = id_user , lowongan_foreign_key = id_lowongan)
        if(cek_id_lowongan_dan_opd(request , id_lowongan)):
            filename = userlamarmagang.file_berkas_tambahan.name.split('/')[-1]
            if(userlamarmagang.file_berkas_tambahan):
                #filename = os.path.basename(userlamarmagang.file_berkas_tambahan.name)
                response = HttpResponse(userlamarmagang.file_berkas_tambahan, content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename=%s' % filename
                return response
            else :
                return HttpResponse('tidak ada file')
        else :
            return redirect(opd_home)
    except ObjectDoesNotExist :
        return redirect(opd_home)
    
    

def opd_download_cv(request ,id_user, id_lowongan ):
    try :
        userlamarmagang = UserLamarMagang.objects.get(user_foreign_key = id_user , lowongan_foreign_key = id_lowongan)
        if(cek_id_lowongan_dan_opd(request , id_lowongan)):
            pelamar = Account.objects.get(id = id_user)
            if(pelamar.userprofile.cv):
                filename = pelamar.userprofile.cv.name.split('/')[-1]
                #filename = os.path.basename(userlamarmagang.file_berkas_tambahan.name)
                response = HttpResponse(pelamar.userprofile.cv, content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename=%s' % filename
                return response
            else :
                return HttpResponse('tidak ada file')
        else :
            return redirect(opd_home)
    except ObjectDoesNotExist :
        return redirect(opd_home)

        
#Fungsi untuk mengecek apakah opd yang 
# mengakses data lowongan adalah opd terkait
def cek_id_lowongan_dan_opd(request, id_lowongan):
    lowongan = Lowongan.objects.get(id=id_lowongan)
    if lowongan.opd_foreign_key_id == request.user.id:
        return True
    else:
        return False

def opd_lowongan(request):
    if request.user.is_authenticated and request.user.is_opd:
        list_lowongan = Lowongan.objects.filter(opd_foreign_key=request.user.id)

        return render(request, 'opd_lowongan.html',
                      {'list_lowongan': list_lowongan})
    return redirect(URL_OPD_LOGIN)


def opd_detail_lowongan(request, id_lowongan):
    if request.user.is_authenticated and request.user.is_opd:
        lowongan = Lowongan.objects.get(id=id_lowongan)
        return render(request, 'opd_detail_lowongan.html',
                      {'lowongan': lowongan})
    return redirect(URL_OPD_LOGIN)

def opd_verification(request, token):
    try:
        opd_from_verification_list = OpdVerificationList.objects.get(
            secret=token)
        opd_name = opd_from_verification_list.name
        email = opd_from_verification_list.email
        phone = opd_from_verification_list.phone
    except OpdVerificationList.DoesNotExist:
        return redirect('/opd/verification/404')
    if request.method == 'POST':
        form = OpdConfirmationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            new_user = Account.objects.create_user(email, password)
            new_user.name = opd_name
            new_user.phone = phone
            new_user.is_opd = True
            new_user.save()
            create_opd = OpdProfile(user=new_user, unique_opd_attribute="opd")
            create_opd.save()
            opd_from_verification_list.delete()
            return redirect(URL_OPD_LOGIN)
    else:
        form = OpdConfirmationForm()
    return render(
        request,
        'opd/opd_verification.html',
        {
            'token': token,
            'form': form,
            'opd_name': opd_name
        }
    )

def opd_verification_not_found(request):
    return render(
        request,
        'opd/opd_verification_404.html'
    )
def opd_verification_redirect(request):
    return redirect("/")
