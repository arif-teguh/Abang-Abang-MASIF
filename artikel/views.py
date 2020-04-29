from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArtikelForm
from .models import Artikel

dir_form_artikel = 'artikel/form_artikel.html'
dir_form_debugger = 'artikel/debug.html'

@login_required
def show_form_artikel(request):
    if request.user.is_admin == False:
        return redirect('/')

    response = {
        "form" : ArtikelForm()
    }
    return render(request, dir_form_artikel, response)

@login_required
def post_form_artikel(request):
    if request.user.is_admin == False:
        return redirect('/')

    form = ArtikelForm(request.POST or None)
    if form.is_valid():
        data_artikel = Artikel.objects.create(
            judul=request.POST['judul'],
            deskripsi=request.POST['deskripsi'],
            foto_artikel=request.FILES.get('foto_artikel',
                                           False)
        )
        data_artikel.save()
        print("masuk gan")
        return redirect("/")
    return redirect("/")

@login_required
def update_form_artikel(request, id_artikel):
    if request.user.is_admin == False:
        return redirect('/')

    artikel_data = get_object_or_404(Artikel, pk=id_artikel)
    form = ArtikelForm(instance=artikel_data)
    if request.method == 'POST':
        form = ArtikelForm(request.POST or None,
                           request.FILES or None,
                           instance=artikel_data)
        if form.is_valid():
            form.save()
            return redirect("/")
    response = {
        'form': form
    }
    return render(request, dir_form_artikel, response)
