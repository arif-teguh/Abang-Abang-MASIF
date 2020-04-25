from django.shortcuts import render

from artikel.models import Artikel


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
