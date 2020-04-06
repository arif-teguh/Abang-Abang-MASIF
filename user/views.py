from django.shortcuts import render

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
