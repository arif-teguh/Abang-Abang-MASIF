from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from admin.views import user_is_admin
from .forms import ArtikelForm
from .models import Artikel

dir_form_artikel = 'artikel/form_artikel.html'
dir_form_debugger = 'artikel/debug.html'
url_artikel = "/artikel/"

@login_required
def show_form_artikel(request):
    if request.user.is_admin == False:
        return redirect('/')

    response = {
        "form": ArtikelForm()
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
        return redirect(url_artikel+str(data_artikel.id))
    return redirect("/")


@login_required
def update_form_artikel(request, id_artikel):
    if request.user.is_admin == False:
        return redirect('/')

    try:
        artikel_data = Artikel.objects.get(pk=id_artikel)
    except Artikel.DoesNotExist:
        return redirect("/")

    form = ArtikelForm(instance=artikel_data)
    if request.method == 'POST':
        form = ArtikelForm(request.POST or None,
                           request.FILES or None,
                           instance=artikel_data)
        if form.is_valid():
            form.save()
            return redirect(url_artikel+str(id_artikel))
    response = {
        'form': form,
        'type':'update',
        'pk' : id_artikel,
    }
    return render(request, dir_form_artikel, response)


def view_read_artikel(request, artikel_id):
    error = False
    try:
        artikel_obj = Artikel.objects.get(pk=artikel_id)
    except Artikel.DoesNotExist:
        artikel_obj = None
        error = True

    all_other_article = Artikel.objects.all().exclude(pk=artikel_id)
    context = {
        'artikel': artikel_obj,
        'all_other_article': all_other_article,
        'error': error
    }
    return render(request, 'artikel/artikel-read.html', context)

@csrf_exempt
def admin_delete_artikel(request, id_artikel):
    if request.method == "POST" and user_is_admin(request):
        Artikel.objects.filter(pk=id_artikel)[0].delete()
        return HttpResponse('Article Successfully Deleted')
    return HttpResponse('Forbidden')