from django.shortcuts import render, redirect


# Create your views here.
def opd_login(request):
    return render(request, 'opd_login.html')


def opd_index(request):
    if request.user.is_authenticated and not request.user.is_admin and request.user.is_opd and not request.user.is_user:
        return render(request, 'opddashboard.html', {'user': request.user})
    else:
        return redirect('/account-redirector')


def opd_lowongan(request):
    return render(request, 'opd_lowongan.html')
