from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from account.models import Account
from admin.opd_registration_form import OpdRegistrationForm
from artikel.models import Artikel
from .mailing import send_verification_email
from .models import OpdVerificationList
from .token import generate_opd_token


def get_all_opd():
    return list(
        Account.objects.filter(
            is_opd=True,
            is_admin=False,
            is_staff=False,
            is_superuser=False,
            is_user=False
        )
    )


def user_is_admin(request):
    return request.user.is_authenticated and \
           request.user.is_admin


def admin_login(request):
    return render(request, 'admin/admin_login.html')


def admin_index(request):
    if user_is_admin(request):
        return render(request, 'admin/admin_index.html')
    else:
        return redirect('/admin/login/')


def admin_list_opd(request):
    if user_is_admin(request):
        return render(
            request,
            'admin/admin_list_opd.html',
            {'list_opd': get_all_opd()}
        )

    else:
        return redirect('/admin/login/')


def admin_register_opd(request):
    if user_is_admin(request):
        err = []
        if request.method == 'POST':
            form = OpdRegistrationForm(request.POST)
            if form.is_valid():
                try:
                    form.check()
                    name = form.cleaned_data['opd_name']
                    email = form.cleaned_data['email']
                    phone = form.cleaned_data['phone']
                    secret = generate_opd_token()
                    new_account = OpdVerificationList(
                        secret=secret,
                        name=name,
                        email=email,
                        phone=phone
                    )
                    new_account.save()
                    base_url = get_current_site(request).domain
                    verif_url = base_url + '/opd/verification/' + secret
                    send_verification_email(verif_url, email)
                    return render(
                        request,
                        'activation_link.html'
                    )
                except ValidationError as e:
                    err = e
        else:
            form = OpdRegistrationForm()
        return render(
            request,
            'admin/admin_register_opd.html',
            {'form': form, 'err': err}
        )
    else:
        return redirect('/admin/login')


@csrf_exempt
def admin_delete_opd(request):
    if request.method == "POST" and user_is_admin(request):
        pk = int(request.POST['pk'])
        Account.objects.filter(pk=pk)[0].delete()
        return HttpResponse('Delete OPD Success')
    return HttpResponse('Forbidden')


def information_page(request):
    if user_is_admin(request):
        context = {
            "articles": list(Artikel.objects.all()),
        }
        return render(request, 'admin/admin-info-page.html', context)
    else:
        return redirect('/admin/login')
