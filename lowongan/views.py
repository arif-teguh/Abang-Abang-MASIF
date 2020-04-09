from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from account.models import Account
from .form import LowonganForm, UserLamarMagangForm
from .models import Lowongan, UserLamarMagang

@login_required
def show_form_lowongan(request, response=None):
    if request.user.is_opd is True:
        if response is None:
            return render(request, 'lowongan/form_lowongan.html',
                          {'form': LowonganForm(), 'type_form': 'post'})
        elif response is not None:
            return render(request, 'lowongan/form_lowongan.html',
                          response)
    return redirect("/")
#

@login_required
def post_form_lowongan(request):
    if request.user.is_opd == False:
        return redirect('/')

    if request.method == 'POST':
        form = LowonganForm(request.POST or None, request.user.id)
        if form.is_valid():
            data_lowongan = Lowongan.objects.create(
                judul=request.POST['judul'],
                kategori=request.POST['kategori'],
                kuota_peserta=request.POST['kuota_peserta'],
                waktu_awal_magang=request.POST['waktu_awal_magang'],
                waktu_akhir_magang=request.POST['waktu_akhir_magang'],
                batas_akhir_pendaftaran=request.POST['batas_akhir_pendaftaran'],
                berkas_persyaratan=request.POST.getlist("berkas_persyaratan"),
                deskripsi=request.POST['deskripsi'],
                requirement=request.POST['requirement'],
                opd_foreign_key_id=request.user.id
            )
            data_lowongan.save()
            id_lowongan = str(data_lowongan.id)
            return redirect("/opd/lowongan/detail-"+id_lowongan+"/")
        berkas_persyaratan = request.POST.getlist("berkas_persyaratan")
        if berkas_persyaratan != []:
            form = LowonganForm(request.POST or None, request.user.id,
                                list_choice=berkas_persyaratan)
        return show_form_lowongan(request,
                                  {'form': form, 'type_form': 'post',
                                   'choice_select_field': berkas_persyaratan})
    return redirect('/lowongan/opd/form/')

@login_required
def update_form_lowongan(request, id_lowongan):
    if request.user.is_opd == False:
        return redirect('/lowongan/opd/form/')

    lowongan_data = get_object_or_404(Lowongan, pk=id_lowongan)
    form = LowonganForm(instance=lowongan_data, id=id_lowongan)
    if request.method == 'POST':
        form = LowonganForm(request.POST or None,
                            instance=lowongan_data, id=id_lowongan)
        if form.is_valid():
            form.save()
            return redirect("/")
    response = {
        'form': form, 'type_form': 'update',
        'choice_select_field': lowongan_data.berkas_persyaratan
    }
    return render(request, 'lowongan/form_lowongan.html', response)

@login_required
def form_lamar_lowongan(request, id_lowongan):
    if request.user.is_user == False:
        return redirect('/')

    try:
        user = request.user
        lowongan = Lowongan.objects.get(pk=id_lowongan)
        user_profile = user.userprofile
        opd = lowongan.opd_foreign_key
    except ObjectDoesNotExist:
        return redirect("/")

    if request.method == 'POST':
        form = UserLamarMagangForm(request.POST or None)
        if form.is_valid():
            file_cv = request.FILES.get('file_cv', False)
            data_lamaran = UserLamarMagang.objects.create(
                application_letter=request.POST['application_letter'],
                file_berkas_tambahan=request.FILES.get('file_berkas_tambahan', False),
                lowongan_foreign_key=lowongan,
                user_foreign_key=user
            )
            lowongan.list_pendaftar_key.add(user_profile)
            data_lamaran.save()
            if user_profile.cv != "" and file_cv is False:
                pass
            else:
                user_profile.cv = file_cv
                user_profile.save()
            return redirect("/user/dashboard/")

    response = {
        'form': UserLamarMagangForm(),
        'lowongan':lowongan,
        'opd':opd
    }
    print(opd.name)

    return render(request, 'lowongan/form_lamar.html', response)
