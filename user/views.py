import datetime

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from account.models import UserProfile, Account
from admin.mailing import send_verification_email
from lowongan.models import UserLamarMagang
from user.forms import EditUserProfileForm, CVForm, ProfilePictureForm
from user.models import UserVerificationList
from .token import generate_user_token
from .user_registration_form import UserRegistrationForm

URL_USER_DASHBOARD = '/user/dashboard/'
ERROR_PAGE_NOT_FOUND = 'ERROR 404 Page not found'


def account_is_user(request):
    try:
        return (request.user.is_authenticated
                and request.user.is_user
                and request.user.userprofile is not None)
    except UserProfile.DoesNotExist:
        return False


def upload_profile_picture(request):
    if account_is_user(request) and request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.profile_picture = request.FILES['profile_picture']
            request.user.save()
        return redirect(URL_USER_DASHBOARD)
    return HttpResponse(ERROR_PAGE_NOT_FOUND)


def upload_cv(request):
    if account_is_user(request) and request.method == 'POST':
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                request.user.userprofile.cv = request.FILES['cv']
                request.user.userprofile.save()
            except MultiValueDictKeyError:
                return HttpResponse('ERROR no file sent')
        return redirect(URL_USER_DASHBOARD)
    return HttpResponse(ERROR_PAGE_NOT_FOUND)


def delete_cv(request):
    if account_is_user(request) and request.method == 'POST':
        request.user.userprofile.cv.delete()
    return HttpResponse(ERROR_PAGE_NOT_FOUND)


def user_dashboard(request):
    if account_is_user(request):
        return render(request, 'user/user-dashboard.html',
                      {'form_pp': ProfilePictureForm(),
                       'user': request.user, 'form_cv': CVForm()})
    return redirect('/user/login/')


def born_date_validator(post):
    date = str(post['born_date'])
    date_format = '%d/%m/%Y'
    try:
        date_obj = datetime.datetime.strptime(date, date_format)
        print(date_obj)
        return {'result': True, 'message': 'success'}
    except (ValueError, TypeError):
        return {'result': False, 'message': 'Tanggal lahir salah'}


def sex_validator(post):
    sex = post['sex']
    if sex == 'm' or sex == 'f':
        return {'result': True, 'message': 'success'}
    return {'result': False, 'message': 'Jenis kelamin salah'}


def phone_number_validator(post):
    phone_number = post['phone']
    if 3 <= len(phone_number) < 15:
        return {'result': True, 'message': 'success'}
    return {'result': False, 'message': 'Nomor telepon salah'}


# Asumsi form sudah valid, tidak ada missing key dictionary
def is_data_valid(post):
    validators = [
        born_date_validator,
        sex_validator,
        phone_number_validator,
    ]
    for function in validators:
        validation_result = function(post)
        if not validation_result['result']:
            return validation_result

    return {'result': True, 'message': 'success'}


def user_edit_profile(request):
    if account_is_user(request):
        if request.method == 'POST':
            form = EditUserProfileForm(request.POST)

            if form.is_valid():
                data_valid = is_data_valid(request.POST)
                if data_valid['result']:
                    profile = request.user.userprofile
                    request.user.name = request.POST['name']
                    request.user.phone = request.POST['phone']
                    profile.born_city = request.POST['born_city']

                    date_obj = datetime.datetime.strptime(
                        request.POST['born_date'],
                        '%d/%m/%Y')
                    profile.born_date = date_obj
                    profile.address = request.POST['address']
                    profile.sex = request.POST['sex']
                    profile.education = request.POST['education']
                    profile.institution = request.POST['institution']
                    profile.major = request.POST['major']

                    request.user.save()
                    profile.save()
                    return redirect('/user/dashboard/')
                return HttpResponse(data_valid['message'])
            return HttpResponse(form.errors)
        else:
            born_date_in_database = str(
                request.user.userprofile.born_date
            ).split('-')
            shown_born_date = '{}/{}/{}'.format(born_date_in_database[2],
                                                born_date_in_database[1],
                                                born_date_in_database[0])

            current_user_data = {
                'phone': request.user.phone,
                'name': request.user.name,
                'born_city': request.user.userprofile.born_city,
                'born_date': shown_born_date,
                'address': request.user.userprofile.address,
                'institution': request.user.userprofile.institution,
                'major': request.user.userprofile.major,
            }

            return render(request, 'user/user-edit-profile.html',
                          {'form': EditUserProfileForm(current_user_data),
                           'request': request})
    return redirect('/user/login/')


def list_of_lowongan_to_json_dict(data):
    result = {
        'data': []
    }

    for item in data:
        lowongan_object = item.lowongan_foreign_key
        result['data'].append(
            [item.status_lamaran,
             '<a href="/user/dashboard/status-lamaran/{}/">{}</a>'.format(item.pk, lowongan_object.judul),
             lowongan_object.opd_foreign_key.name])
    return result


def get_all_lamaran_for_dashboard_table(request):
    if request.user.is_authenticated:
        response = list_of_lowongan_to_json_dict(request.user.RelasiLowonganAndUser.all())
        return JsonResponse(response)
    else:
        return HttpResponse('[ERROR] permission denied')


def user_register(request):
    err = []
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.check()
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
                base_url = get_current_site(request).domain
                verif_url = base_url + '/user/verification/' + secret
                send_verification_email(verif_url, email)
                return render(
                    request,
                    'activation_link.html',
                )
            except ValidationError as e:
                err = e
    else:
        form = UserRegistrationForm()
    return render(request,
                  'user/user_register.html',
                  {'form': form, 'err': err})


def user_verification(request, token):
    if token == 'google-oauth2':
        google_user = Account.objects.get(email=request.user.email)
        google_is_user = google_user.is_user
        if google_user.name == "" and google_user.phone == "" and not google_is_user:
            google_user.name = "Pelamar"
            google_user.phone = "081122232222"
            google_user.is_user = True
            google_user.save()
            create_user = UserProfile(user=google_user, unique_pelamar_attribute='user')
            create_user.save()
            messages.success(request, 'User Verified')
            return redirect("/")
        else:
            return redirect("/")
    else:
        try:
            user_from_verification_list = UserVerificationList.objects.get(
                secret=token)
            user_name = user_from_verification_list.name
            email = user_from_verification_list.email
            phone = user_from_verification_list.phone
            password = user_from_verification_list.password
        except UserVerificationList.DoesNotExist:
            return redirect('/user/verification/404')
        new_user = Account.objects.create_user(email, password)
        new_user.name = user_name
        new_user.phone = phone
        new_user.is_user = True
        new_user.save()
        create_user = UserProfile(user=new_user, unique_pelamar_attribute='user')
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


def user_see_status_lamaran(request, id_user_lamar_magang):
    if request.user.is_authenticated:
        try:
            lamaran_obj = UserLamarMagang.objects.get(pk=id_user_lamar_magang)
        except UserLamarMagang.DoesNotExist:
            return HttpResponse('[ERROR] Lamaran Not Found')

        if lamaran_obj.user_foreign_key.email == request.user.email:
            context = {
                'lamaran_obj': lamaran_obj
            }
            return render(request, 'user/user-lamaran-state.html', context=context)

    return HttpResponse('[ERROR] Permission Denied')
