from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from .form import LowonganForm
from .models import Lowongan


@login_required
def show_form_lowongan(request):
    if request.user.is_opd == True:
        return render(request, 'lowongan/form_lowongan.html', {'form': LowonganForm(), 'type_form': 'post'})
    return redirect("/")
#

@login_required
def post_form_lowongan(request):
    if request.user.is_opd == False:
        return redirect('/')

    if request.method == 'POST':
        form = LowonganForm(request.POST or None)       
        if form.is_valid():

            data_lowongan = Lowongan.objects.create(
                judul=request.POST['judul'],
                penyedia=request.POST['penyedia'],
                jumlah_tersedia=request.POST['jumlah_tersedia'],
                durasi_magang=request.POST['durasi_magang'],
                jangka_waktu_lamaran=request.POST['jangka_waktu_lamaran'],
                berkas=request.POST['berkas'],
                deskripsi=request.POST['deskripsi'],
                requirement=request.POST['requirement'],
                opd_foreign_key_id=request.user.id
            )

            data_lowongan.save()
            return redirect("/opd/")

    return redirect('/lowongan/opd/form/')

@login_required
def update_form_lowongan(request, id_lowongan):
    if request.user.is_opd == False:
        return redirect('/lowongan/opd/form/')

    lowongan_data = get_object_or_404(Lowongan, pk=id_lowongan)
    form = LowonganForm(instance=lowongan_data)
    if request.method == 'POST':
        form = LowonganForm(request.POST or None, instance=lowongan_data)
        if form.is_valid():
            form.save()
            return redirect("/opd/")

    else:
        return render(request, 'lowongan/form_lowongan.html', {'form': form, 'type_form': 'update'})