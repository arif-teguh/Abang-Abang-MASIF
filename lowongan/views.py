import os
from json import dump, load
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .form import LowonganForm, UserLamarMagangForm, AdminMenambahKategoriForm
from .models import Lowongan, UserLamarMagang

dir_form_lowongan = 'lowongan/form_lowongan.html'
@login_required
def show_form_lowongan(request, response=None):
    if request.user.is_opd is True:
        if response is None:
            return render(request, dir_form_lowongan,
                          {'form': LowonganForm(), 'type_form': 'post'})
        elif response is not None:
            return render(request, dir_form_lowongan,
                          response)
    return redirect("/")

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
            return redirect("/opd/lowongan/detail-"+str(id_lowongan)+"/")
    response = {
        'form': form, 'type_form': 'update',
        'choice_select_field': lowongan_data.berkas_persyaratan
    }
    return render(request, dir_form_lowongan, response)

def update_lamar_lowongan(request, id_lowongan, lamaran):
    user = request.user
    lowongan = Lowongan.objects.get(pk=id_lowongan)
    user_profile = user.userprofile
    opd = lowongan.opd_foreign_key
    if request.method == 'POST':
        file_cv = request.FILES.get('file_cv', False)
        form = UserLamarMagangForm(request.POST or None,
                                       request.FILES or None,
                                       instance=lamaran)
        if form.is_valid():
            form.save()
            if file_cv is not False:
                user_profile.cv = file_cv
                user_profile.save()
            return redirect("/user/dashboard/")
    form = UserLamarMagangForm(instance=lamaran)
    respons = {
        'form': form,
        'lowongan':lowongan,
        'opd':opd,
        'is_update':True,
        'file_berkas':lamaran.file_berkas_tambahan,
        'application_letter': lamaran.application_letter
    }

    return render(request, 'lowongan/form_lamar.html', respons)

@login_required
def form_lamar_lowongan(request, id_lowongan):
    url_dashboard_user = "/user/dashboard/"
    if request.user.is_user == False:
        return redirect('/')

    try:
        user = request.user
        lowongan = Lowongan.objects.get(pk=id_lowongan)
        user_profile = user.userprofile
        opd = lowongan.opd_foreign_key
    except ObjectDoesNotExist:
        return redirect("/")

    try:
        lamaran = UserLamarMagang.objects.get(
            user_foreign_key=user,
            lowongan_foreign_key=lowongan
        )
        return update_lamar_lowongan(request, id_lowongan, lamaran)
    except ObjectDoesNotExist:
        lamaran = False

    if request.method == 'POST':
        file_cv = request.FILES.get('file_cv', False)
        form = UserLamarMagangForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            data_lamaran = UserLamarMagang.objects.create(
                application_letter=request.POST['application_letter'],
                file_berkas_tambahan=request.FILES.get('file_berkas_tambahan',
                                                       False),
                lowongan_foreign_key=lowongan,
                user_foreign_key=user
            )
            lowongan.list_pendaftar_key.add(user_profile)
            data_lamaran.save()
            if file_cv is False:
                return redirect(url_dashboard_user)
            else:
                user_profile.cv = file_cv
                user_profile.save()
                return redirect(url_dashboard_user)
    
    form = UserLamarMagangForm()
    response = {
        'form': form,
        'lowongan':lowongan,
        'opd':opd,
        'is_update':False
    }

    return render(request, 'lowongan/form_lamar.html', response)

@login_required
def edit_pilihan_kategori_lowongan(request):
    json_kategori_dir = 'templates/lowongan/kategori.json'
    if request.user.is_admin == False:
        return redirect('/')

    if request.method == "POST":
        kategori = request.POST.getlist('kategori')
        kategori_first = kategori[0]
        empty_str = " "
        if isinstance(kategori, list) and isinstance(kategori_first, str):
            if kategori_first != empty_str:
                kategori.insert(0, empty_str)
            temp = {"kategori" : kategori}
            if os.path.exists(json_kategori_dir):
                with open(json_kategori_dir, 'w') as kategori_json:
                    dump(temp, kategori_json)
                return redirect("/admin/")
            else:
                print("File Error Detected!")
                return redirect('/')

    return redirect('/')

@login_required
def show_edit_kategori_lowongan(request):
    json_kategori_dir = 'templates/lowongan/kategori.json'
    dir_form_edit_kategori = 'admin/admin_add_kategori_lowongan.html'
    if request.user.is_admin == False:
        return redirect('/')
    if os.path.exists(json_kategori_dir):
        with open(json_kategori_dir) as kategori_json:
            kategori_dict = load(kategori_json)
        return render(request, dir_form_edit_kategori,
                      {'form': AdminMenambahKategoriForm(),
                       'choice_select_field': kategori_dict["kategori"]})
    else:
        print("File Error Detected!")
        return redirect('/')
