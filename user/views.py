from django.http import HttpResponse
from django.shortcuts import render, redirect

from account.models import UserProfile
from user.forms import EditUserProfileForm


def account_is_user(request):
    try:
        return request.user.is_authenticated and request.user.is_user and request.user.userprofile is not None
    except UserProfile.DoesNotExist:
        return False


def user_dashboard(request):
    if account_is_user(request):
        return render(request, 'user/user-dashboard.html')
    return redirect('/user/login/')


def user_edit_profile(request):
    if account_is_user(request):
        if request.method == 'POST':
            form = EditUserProfileForm(request.POST)

            if form.is_valid():
                return HttpResponse('post success')
            return HttpResponse('post ERROR')
        else:
            return render(request, 'user/user-edit-profile.html', {'form': EditUserProfileForm(), 'request': request})

    return redirect('/user/login/')
