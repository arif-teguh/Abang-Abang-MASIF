from django.shortcuts import render, redirect
from django.contrib import messages

from account.models import Account, PelamarProfile
from user.models import UserVerificationList
from .user_registration_form import UserRegistrationForm
from .token import generate_user_token


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            secret = generate_user_token()
            password = form.cleaned_data['password']
            new_account = UserVerificationList(
                secret=secret,
                name=name,
                email=email,
                phone=phone,
                password=password
            )
            new_account.save()
            return render(
                request,
                'user/user_activation_link.html',
                {'secret': secret}
            )
    else:
        form = UserRegistrationForm()
    return render(request, 'user/user_register.html', {'form': form})


def user_verification(request, token):
    try:
        user_from_verification_list = UserVerificationList.objects.get(
            secret=token)
        user_name = user_from_verification_list.name
        email = user_from_verification_list.email
        phone = user_from_verification_list.phone
        password = user_from_verification_list.password
    except:
        return redirect('/user/verification/404')
    new_user = Account.objects.create_user(email, password)
    new_user.name = user_name
    new_user.phone = phone
    new_user.is_user = True
    new_user.save()
    create_user = PelamarProfile(user=new_user, unique_pelamar_attribute='user')
    create_user.save()
    user_from_verification_list.delete()
    messages.success(request, 'User Verified')
    return redirect("/user/login")


def user_verification_redirect(request):
    return redirect("/")


def user_verification_not_found(request):
    return render(
        request,
        'user/user_verification_404.html'
    )
