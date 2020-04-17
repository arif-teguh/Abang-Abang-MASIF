from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from .kesbangpol_login_form import KesbangpolAuthenticationForm
# Create your views here.
def kesbangpol_login(request):
    err = []
    if request.method == 'POST':
        form = KesbangpolAuthenticationForm(request.POST)
        if form.is_valid():
            try:
                form.check()
                email = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/')
            except ValidationError as e:
                err = e
    else:
        form = KesbangpolAuthenticationForm()

    return render(request, 'kesbangpol_login.html', {'form': form, 'err': err})
