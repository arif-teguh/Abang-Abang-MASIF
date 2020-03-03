from django.shortcuts import redirect


def account_redirector(request):
    if request.user.is_authenticated:
        if request.user.is_opd:
            return redirect('/opd')
        elif request.user.is_admin:
            return redirect('/admin')

    return redirect('/')
