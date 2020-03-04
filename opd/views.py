from django.shortcuts import render , redirect
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse

from lowongan.models import Lowongan
from admin.models import OpdVerificationList
from account.models import Account, OpdProfile
from .opd_confirmation_form import OpdConfirmationForm

def opd_login(request):
    return render(request, 'opd_login.html')

def opd_lowongan(request):
    if request.user.is_authenticated and request.user.is_opd:
        list_lowongan = Lowongan.objects.filter(opd_foreign_key = request.user.id)
        return render(request,'opd_lowongan.html', {'list_lowongan': list_lowongan})
    else:
        return redirect('/opd/login/')


def opd_detail_lowongan(request,id_lowongan):
    if request.user.is_authenticated and request.user.is_opd:
        list_lowongan = Lowongan.objects.filter(opd_foreign_key = request.user.id)
        lowongan = Lowongan.objects.get(id = id_lowongan)
        return render(request,'opd_detail_lowongan.html' , {'lowongan': lowongan})
    else:
        return redirect('/opd/login/')

def opd_verification(request, token):
    try:
        opd_from_verification_list = OpdVerificationList.objects.get(
            secret=token)
        opd_name = opd_from_verification_list.name
        email = opd_from_verification_list.email
        phone = opd_from_verification_list.phone
    except:
        return redirect('/opd/verification/404')
    if request.method == 'POST':
        form = OpdConfirmationForm(request.POST)
        if form.is_valid():
            password = form.clean_password()
            new_user = Account.objects.create_user(email, password)
            new_user.name = opd_name
            new_user.phone = phone
            new_user.save()
            create_opd = OpdProfile(user=new_user, unique_opd_attribute="opd")
            create_opd.save()
            opd_from_verification_list.delete()
            return redirect("/opd/login")
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
