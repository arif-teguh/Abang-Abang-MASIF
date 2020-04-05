import datetime
import re

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from account.models import UserProfile
from user.forms import EditUserProfileForm, CVForm, ProfilePictureForm


def account_is_user(request):
    try:
        return request.user.is_authenticated and request.user.is_user and request.user.userprofile is not None
    except UserProfile.DoesNotExist:
        return False


def upload_profile_picture(request):
    if account_is_user(request):
        if request.method == 'POST':
            form = ProfilePictureForm(request.POST, request.FILES)
            if form.is_valid():
                request.user.profile_picture = request.FILES['profile_picture']
                request.user.save()
            return redirect('/user/dashboard/')
    return HttpResponse('ERROR 404 Page not found')


def upload_cv(request):
    if account_is_user(request):

        if request.method == 'POST':
            form = CVForm(request.POST, request.FILES)
            # form.instance.user = request.user
            if form.is_valid():
                try:
                    request.user.userprofile.cv = request.FILES['cv']
                    request.user.userprofile.save()
                except MultiValueDictKeyError:
                    return HttpResponse('ERROR no file sent')
            return redirect('/user/dashboard/')
    return HttpResponse('ERROR 404 Page not found')


def delete_cv(request):
    if account_is_user(request):
        if request.method == 'POST':
            request.user.userprofile.cv.delete()
    return HttpResponse('ERROR 404 Page not found')


def user_dashboard(request):
    if account_is_user(request):

        return render(request, 'user/user-dashboard.html',
                      {'form_pp': ProfilePictureForm(), 'user': request.user, 'form_cv': CVForm()})
    else:
        return redirect('/user/login/')


def born_date_validator(post):
    # date_format = '%Y-%m-%d'
    date = str(post['born_date'])
    date_format = '%d/%m/%Y'
    try:
        date_obj = datetime.datetime.strptime(date, date_format)
        print(date_obj)
        return {'result': True, 'message': 'success'}
    except (ValueError, TypeError) as e:
        return {'result': False, 'message': 'Tanggal lahir salah'}


def sex_validator(post):
    sex = post['sex']
    if sex == 'm' or sex == 'f':
        return {'result': True, 'message': 'success'}
    return {'result': False, 'message': 'Jenis kelamin salah'}


def phone_number_validator(post):
    phone_number = post['phone']
    if re.match(r'^\+?1?\d{3,15}$', phone_number):
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

    return validation_result


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

                    date_obj = datetime.datetime.strptime(request.POST['born_date'], '%d/%m/%Y')
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
            born_date_in_database = str(request.user.userprofile.born_date).split('-')
            shown_born_date = '{}/{}/{}'.format(born_date_in_database[2], born_date_in_database[1],
                                                born_date_in_database[0])

            current_user_data = {
                'phone': request.user.phone,
                'name': request.user.name,
                'born_city': request.user.userprofile.born_city,
                'born_date': shown_born_date,
                'address': request.user.userprofile.address,
                'institution': request.user.userprofile.institution,
                'major': request.user.userprofile.major,
                'phone': request.user.phone,

            }

            return render(request, 'user/user-edit-profile.html',
                          {'form': EditUserProfileForm(current_user_data), 'request': request})
    return redirect('/user/login/')
