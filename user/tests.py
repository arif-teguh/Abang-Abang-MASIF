from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest
from django.test import TestCase, Client, override_settings
from selenium import webdriver
from social_django.compat import reverse
from django.core.exceptions import ValidationError

from account.models import Account, UserProfile
from lowongan.models import UserLamarMagang, Lowongan
from user import views
from user.forms import EditUserProfileForm
from user.views import born_date_validator, sex_validator, phone_number_validator, is_data_valid, \
    list_of_lowongan_to_json_dict
from .models import UserVerificationList
from .token import generate_user_token
from .user_login_form import UserAuthenticationForm
from .user_registration_form import UserRegistrationForm

URL_USER_LOGIN = '/user/login/'

class PelamarRegistrationTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.request = HttpRequest()
        self.email = "a@a.com"
        self.password = "zxasqw12"
        self.user_name = "abc"
        self.phone = 1234
        self.DATA = {'user_name': self.user_name, 'email': self.email,
                     'phone': self.phone, 'password': self.password,
                     'confirm_password': self.password}

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_page_title_register_user_page(self):
        response = views.user_register(self.request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Daftar Pelamar</title>', html_response)

    def test_submit_button_exist(self):
        response = views.user_register(self.request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button type="submit"', html_response)

    def test_register_user_html(self):
        with self.assertTemplateUsed('user/user_register.html'):
            response = self.client.get('/user/register/')
            self.assertEqual(response.status_code, 200)

    def test_generate_token(self):
        secret = generate_user_token()
        secret_len = len(secret)
        self.assertEqual(secret_len, 22)

    def test_create_user_success(self):
        user_count = UserVerificationList.objects.count()
        response = self.client.post(
            "/user/register/",
            self.DATA)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserVerificationList.objects.count(), user_count + 1)
    
    def test_create_user_failed(self):
        user_count = UserVerificationList.objects.count()

        new_account = Account.objects.create_user(email=self.email,
                                                  password=self.password)
        new_account.is_user = True
        new_account.save()

        response = self.client.post(
            "/user/register/",
            self.DATA
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserVerificationList.objects.count(), user_count)

    def test_user_registration_form_fail_duplicate_user(self):
        new_account = Account.objects.create_user(email=self.email,
                                                  password=self.password)
        new_account.is_user = True
        new_account.save()

        with self.assertRaises(ValidationError):
            form = UserRegistrationForm(self.DATA)
            if form.is_valid():
                form.check()

    def test_user_registration_form_fail_user_on_verification_list(self):
        user_on_waitinglist = UserVerificationList(
            secret='1sdeja2sdfdf',
            name=self.user_name,
            email=self.email,
            phone=self.phone,
            password=self.password
        )
        user_on_waitinglist.save()

        with self.assertRaises(ValidationError):
            form = UserRegistrationForm(self.DATA)
            if form.is_valid():
                form.check()

class PelamarValidationTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.request = HttpRequest()
        self.email = "a@a.com"
        self.password = "zxasqw12"
        self.user_name = "abc"
        self.phone = 1234

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_verification_redirect(self):
        response = self.client.get('/user/verification', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_verification_not_found(self):
        with self.assertTemplateUsed('user/user_verification_404.html'):
            response = self.client.get('/user/verification/404')
            self.assertEqual(response.status_code, 200)

    def test_create_user_to_verification_list(self):
        secret = generate_user_token()
        new_user = UserVerificationList(name=self.user_name,
                                        email=self.email,
                                        phone=self.phone,
                                        password=self.password,
                                        secret=secret)
        new_user.save()
        response = self.client.get('/user/verification/' + secret)
        self.assertEqual(response.status_code, 302)

    def test_open_verification_code_not_exist(self):
        secret = "abcdefakfjalk"
        response = self.client.get('/user/verification/' + secret)
        self.assertEqual(response.status_code, 302)

    def test_pelamar_verified_login(self):
        response = self.client.get(URL_USER_LOGIN)
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertTrue(
            isinstance(form, UserAuthenticationForm), type(form).__mro__)


# GOOGLE OAUTH2 UNIT TEST
@override_settings(SOCIAL_AUTH_GOOGLE_KEY='1',
                   SOCIAL_AUTH_GOOGLE_SECRET='2')
class TestViews(TestCase):

    def setUp(self):
        session = self.client.session
        session['google_state'] = '1'
        session.save()

    def test_begin_view(self):
        response = self.client.get(reverse('social:begin', kwargs={'backend': 'google-oauth2'}))
        self.assertEqual(response.status_code, 302)

        url = reverse('social:begin', kwargs={'backend': 'blabla'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_page_response_status(self):
        response = Client().get(URL_USER_LOGIN)
        self.assertEqual(response.status_code, 200)

    def test_page_template(self):
        response = Client().get(URL_USER_LOGIN)
        self.assertTemplateUsed(response, 'user_login.html')


class UserUnitTest(TestCase):
    URL_USER_DASHBOARD = '/user/dashboard/'
    URL_USER_DASHBOARD_EDIT = '/user/dashboard/edit/'
    URL_USER_UPLOAD_CV = '/user/dashboard/edit/upload_cv/'
    URL_USER_DELETE_CV = '/user/dashboard/edit/delete_cv/'
    DEFAULT_CV = 'cv.pdf'
    DEFAULT_MAJOR = 'Computer Science'
    EMAIL_TEST = 'test@mail.com'
    PASSWORD_TEST = '12345678'

    def setUp(self):
        self.mock_date = datetime(2012, 1, 1)
        self.client = Client()
        self.request = HttpRequest()
        self.created_mock_user = Account.objects.create_user(
            email=self.EMAIL_TEST,
            password=self.PASSWORD_TEST,
        )
        self.created_mock_user.name = 'MockName'
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.mock_opd = Account.objects.create_user(
            email='mockopd@mail.com',
            password='12345678',
        )
        self.mock_opd.is_opd = True
        self.mock_opd.name = 'MockName'
        self.mock_opd.save()
        self.request.user = self.created_mock_user
        self.mock_user_profile = UserProfile(user=self.created_mock_user)
        self.mock_user_profile.save()
        self.test_file_cv = SimpleUploadedFile(self.DEFAULT_CV, b"file_content")
        self.test_file_jpg = SimpleUploadedFile("pp.jpg", b"file_content")
        self.mock_lowongan = Lowongan(judul='MockJudulLowongan',
                                      kategori='kat1',
                                      kuota_peserta=10,
                                      waktu_awal_magang=self.mock_date,
                                      waktu_akhir_magang=self.mock_date,
                                      batas_akhir_pendaftaran=self.mock_date,
                                      berkas_persyaratan=['Kartu Keluarga'],
                                      deskripsi='deskripsi1',
                                      requirement='requirement1',
                                      opd_foreign_key_id=self.mock_opd.id)
        self.mock_lowongan.save()
        self.mock_user_lamar_magang = UserLamarMagang(
            lowongan_foreign_key=self.mock_lowongan,
            user_foreign_key=self.created_mock_user,
            status_lamaran='MockStatus')
        self.mock_user_lamar_magang.save()

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_access_user_dashboard_url_logged_in_should_return_200(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        response = self.client.get(self.URL_USER_DASHBOARD)
        self.assertEqual(response.status_code, 200)

    def test_access_user_dashboard_url_not_logged_in_should_return_302(self):
        response = self.client.get(
            self.URL_USER_DASHBOARD
        )
        self.assertEqual(response.status_code, 302)

    def test_access_user_dashboard_url_logged_in_not_user_should_return_302(self):
        self.created_mock_user.is_user = False
        self.created_mock_user.save()
        response = self.client.get(self.URL_USER_DASHBOARD)
        self.assertEqual(response.status_code, 302)

    def test_user_has_no_user_dashboard_profile_should_redirect(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.userprofile.delete()
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        response = self.client.get(self.URL_USER_DASHBOARD)
        self.assertEqual(response.status_code, 302)

    def test_access_user_dashboard_edit_url_logged_in_should_return_200(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(
            username=self.EMAIL_TEST,
            password=self.PASSWORD_TEST,
        )
        response = self.client.get(self.URL_USER_DASHBOARD_EDIT)
        self.assertEqual(response.status_code, 200)

    def test_access_user_dashboard_edit_url_not_logged_in_should_return_302(self):
        response = self.client.get(self.URL_USER_DASHBOARD_EDIT)
        self.assertEqual(response.status_code, 302)

    def test_access_user_dashboard_edit_url_logged_in_not_user_should_return_302(self):
        self.created_mock_user.is_user = False
        self.created_mock_user.save()
        response = self.client.get(self.URL_USER_DASHBOARD_EDIT)
        self.assertEqual(response.status_code, 302)

    def test_user_edit_has_user_dashboard_edit_profile_no_redirect(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        response = self.client.get(self.URL_USER_DASHBOARD_EDIT)
        self.assertEqual(response.status_code, 200)

    def test_user_has_no_user_dashboard_edit_profile_should_redirect(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.userprofile.delete()
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        response = self.client.get(self.URL_USER_DASHBOARD_EDIT)
        self.assertEqual(response.status_code, 302)

    def test_user_edit_profile_page_is_set_up_as_expected(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        response = self.client.get(self.URL_USER_DASHBOARD_EDIT)
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertTrue(
            isinstance(form, EditUserProfileForm), type(form).__mro__)

    def test_date_validator_correct_date_should_return_true(self):
        result = born_date_validator({'born_date': '17/08/1945'})
        self.assertEqual(True, result['result'])

    def test_date_validator_empty_string_date_should_return_false(self):
        result = born_date_validator({'born_date': ''})
        self.assertEqual(False, result['result'])

    def test_date_validator_integer_date_should_return_false(self):
        result = born_date_validator({'born_date': 17081945})
        self.assertEqual(False, result['result'])

    def test_date_validator_no_year_date_should_return_false(self):
        result = born_date_validator({'born_date': '17/08/'})
        self.assertEqual(False, result['result'])

    def test_date_validator_no_month_date_should_return_false(self):
        result = born_date_validator({'born_date': '17//1945'})
        self.assertEqual(False, result['result'])

    def test_date_validator_no_day_date_should_return_false(self):
        result = born_date_validator({'born_date': '/08/1945'})
        self.assertEqual(False, result['result'])

    def test_date_validator_no_day_month_year_date_should_return_false(self):
        result = born_date_validator({'born_date': '//'})
        self.assertEqual(False, result['result'])

    def test_date_validator_mmddyyyy_date_should_return_false(self):
        result = born_date_validator({'born_date': '12/30/1945'})
        self.assertEqual(False, result['result'])

    def test_date_validator_yyyymmdd_date_should_return_false(self):
        result = born_date_validator({'born_date': '1945/08/1945'})
        self.assertEqual(False, result['result'])

    def test_sex_validator_f_should_return_true(self):
        validation_result = sex_validator({'sex': 'f'})['result']
        self.assertEqual(True, validation_result)

    def test_sex_validator_m_should_return_true(self):
        validation_result = sex_validator({'sex': 'm'})['result']
        self.assertEqual(True, validation_result)

    def test_sex_validator_lainlain_should_return_false(self):
        validation_result = sex_validator({'sex': 'lainlain'})['result']
        self.assertEqual(False, validation_result)

    def test_phone_number_correct_should_return_true(self):
        validation_result = phone_number_validator({'phone': '0812345678'})['result']
        self.assertEqual(True, validation_result)

    def test_phone_number_one_digit_should_return_false(self):
        validation_result = phone_number_validator({'phone': '1'})['result']
        self.assertEqual(False, validation_result)

    def test_phone_number_sixteen_should_return_false(self):
        validation_result = phone_number_validator({'phone': '16'})['result']
        self.assertEqual(False, validation_result)

    def test_is_data_valid_correct_data_should_return_true(self):
        validation_result = is_data_valid({'phone': '0812345678', 'sex': 'm', 'born_date': '17/08/1945'})['result']
        self.assertEqual(True, validation_result)

    def test_is_data_valid_wrong_born_date_data_should_return_false(self):
        validation_result = is_data_valid({'phone': '0812345678', 'sex': 'm', 'born_date': '/08/1945'})['result']
        self.assertEqual(False, validation_result)

    def test_is_data_valid_wrong_phone_data_should_return_false(self):
        validation_result = is_data_valid({'phone': '1', 'sex': 'm', 'born_date': '17/08/1945'})['result']
        self.assertEqual(False, validation_result)

    def test_is_data_valid_wrong_sex_data_should_return_false(self):
        validation_result = is_data_valid({'phone': '0812345678', 'sex': 'lainlain', 'born_date': '17/08/1945'})[
            'result']
        self.assertEqual(False, validation_result)

    def test_logged_in_post_to_edit_profile_url_correct_data_should_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': self.DEFAULT_MAJOR
        }
        result = self.client.post(self.URL_USER_DASHBOARD_EDIT, data=form_data)
        self.assertEqual(302, result.status_code)
        self.assertEqual(self.URL_USER_DASHBOARD, result.url)

    def test_logged_in_post_to_edit_profile_url_no_name_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        form_data = {

            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': self.DEFAULT_MAJOR
        }
        result = self.client.post(self.URL_USER_DASHBOARD_EDIT, data=form_data)
        self.assertEqual('name', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_address_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        form_data = {
            'name': 'test',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': self.DEFAULT_MAJOR
        }
        result = self.client.post(self.URL_USER_DASHBOARD_EDIT, data=form_data)
        self.assertEqual('address', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_born_date_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': self.DEFAULT_MAJOR
        }
        result = self.client.post(self.URL_USER_DASHBOARD_EDIT, data=form_data)
        self.assertEqual('born_date', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_born_city_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': self.DEFAULT_MAJOR
        }
        result = self.client.post(self.URL_USER_DASHBOARD_EDIT, data=form_data)
        self.assertEqual('born_city', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_phone_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': self.DEFAULT_MAJOR
        }
        result = self.client.post(self.URL_USER_DASHBOARD_EDIT, data=form_data)
        self.assertEqual('phone', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_sex_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'institution': 'uwiw',
            'education': 'smk',
            'major': self.DEFAULT_MAJOR
        }
        result = self.client.post(self.URL_USER_DASHBOARD_EDIT, data=form_data)
        self.assertEqual('sex', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_institution_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'education': 'smk',
            'major': self.DEFAULT_MAJOR
        }
        result = self.client.post(self.URL_USER_DASHBOARD_EDIT, data=form_data)
        self.assertEqual('institution', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_education_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'major': self.DEFAULT_MAJOR
        }
        result = self.client.post(self.URL_USER_DASHBOARD_EDIT, data=form_data)
        self.assertEqual('education', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_major_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
        }
        result = self.client.post(self.URL_USER_DASHBOARD_EDIT, data=form_data)
        self.assertEqual('major', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_wrong_born_date_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '1708/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': 'CS',
        }
        result = self.client.post(self.URL_USER_DASHBOARD_EDIT, data=form_data)
        self.assertEqual('Tanggal lahir salah', result.content.decode('utf-8'))

    def test_not_logged_in_post_to_edit_profile_url_should_redirect(self):
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': self.DEFAULT_MAJOR
        }
        result = self.client.post(self.URL_USER_DASHBOARD_EDIT, data=form_data)
        self.assertEqual(result.status_code, 302)

    def test_access_user_dashboard_upload_cv_page_should_be_accessible(self):
        response = self.client.get(self.URL_USER_UPLOAD_CV)
        self.assertEqual(response.status_code, 200)

    def test_user_upload_cv_with_pdf_should_work(self):
        self.assertEqual(self.created_mock_user.userprofile.cv, None)
        self.created_mock_user.is_user = True
        self.created_mock_user.save()

        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)

        response = self.client.post(self.URL_USER_UPLOAD_CV, {'cv': self.test_file_cv})

        self.assertEqual(response.status_code, 302)
        test_user = Account.objects.get(email=self.EMAIL_TEST)
        self.assertEqual(test_user.userprofile.cv.name, self.DEFAULT_CV)
        test_user.userprofile.cv.delete()

    def test_user_upload_cv_with_pdf_should_not_change_other_userprofile_data(self):
        self.assertEqual(self.created_mock_user.userprofile.cv, None)
        self.created_mock_user.is_user = True
        self.created_mock_user.name = "test_name"
        self.created_mock_user.userprofile.sex = "m"
        self.created_mock_user.userprofile.address = "test_address"
        self.created_mock_user.userprofile.institution = "test_institution"
        self.created_mock_user.userprofile.education = "test_education"
        self.created_mock_user.userprofile.born_city = "test_borncity"
        self.created_mock_user.userprofile.born_date = datetime(2000, 1, 1)
        self.created_mock_user.userprofile.major = "test_major"
        self.created_mock_user.save()
        self.created_mock_user.userprofile.save()

        self.client.login(username='test@mail.com', password='12345678')
        self.assertEqual(self.created_mock_user.name, 'test_name')
        self.assertEqual(self.created_mock_user.userprofile.sex, 'm')
        self.assertEqual(self.created_mock_user.userprofile.address, 'test_address')
        self.assertEqual(self.created_mock_user.userprofile.institution, 'test_institution')
        self.assertEqual(self.created_mock_user.userprofile.education, 'test_education')
        self.assertEqual(self.created_mock_user.userprofile.born_city, 'test_borncity')
        self.assertEqual(self.created_mock_user.userprofile.born_date, datetime(2000, 1, 1))
        self.assertEqual(self.created_mock_user.userprofile.major, 'test_major')
        response = self.client.post(self.URL_USER_UPLOAD_CV, {'cv': self.test_file_cv})
        self.assertEqual(response.status_code, 302)
        test_user = Account.objects.get(email=self.EMAIL_TEST)
        self.assertEqual(test_user.userprofile.cv.name, self.DEFAULT_CV)
        self.assertEqual(test_user.name, 'test_name')
        self.assertEqual(test_user.userprofile.sex, 'm')
        self.assertEqual(test_user.userprofile.address, 'test_address')
        self.assertEqual(test_user.userprofile.institution, 'test_institution')
        self.assertEqual(test_user.userprofile.education, 'test_education')
        self.assertEqual(test_user.userprofile.born_city, 'test_borncity')
        self.assertEqual(test_user.userprofile.born_date, datetime(2000, 1, 1).date())
        self.assertEqual(test_user.userprofile.major, 'test_major')
        test_user.userprofile.cv.delete()

    def test_user_upload_cv_no_file_shouldnt_work(self):
        self.assertEqual(self.created_mock_user.userprofile.cv, None)
        self.created_mock_user.is_user = True
        self.created_mock_user.save()

        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)

        response = self.client.post(self.URL_USER_UPLOAD_CV, {'cv': ''})

        self.assertEqual(response.status_code, 200)
        test_user = Account.objects.get(email=self.EMAIL_TEST)
        self.assertEqual(test_user.userprofile.cv.name, '')

    def test_access_user_dashboard_delete_cv_should_be_accessible(self):
        response = self.client.get(self.URL_USER_DELETE_CV)
        self.assertEqual(response.status_code, 200)

    def test_user_upload_profile_picture_with_jpg_should_work(self):
        self.assertEqual(self.created_mock_user.profile_picture, None)
        self.created_mock_user.is_user = True
        self.created_mock_user.save()

        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)

        response = self.client.post('/user/dashboard/edit/upload_profile_picture/',
                                    {'profile_picture': self.test_file_jpg})

        self.assertEqual(response.status_code, 302)
        test_user = Account.objects.get(email=self.EMAIL_TEST)
        self.assertEqual(test_user.profile_picture.name, 'pp.jpg')
        test_user.profile_picture.delete()

    def test_user_upload_profile_picture_no_file_shouldnt_work(self):
        self.assertEqual(self.created_mock_user.profile_picture, None)
        self.created_mock_user.is_user = True
        self.created_mock_user.save()

        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)

        response = self.client.post(self.URL_USER_UPLOAD_CV, {'profile_picture': ''})

        self.assertEqual(response.status_code, 200)
        test_user = Account.objects.get(email=self.EMAIL_TEST)
        self.assertEqual(test_user.profile_picture.name, '')

    def test_access_user_dashboard_upload_profile_pic_should_be_accessible(self):
        response = self.client.get('/user/dashboard/edit/upload_profile_picture/')
        self.assertEqual(response.status_code, 200)

    def test_delete_cv_user_has_cv_should_work(self):
        self.created_mock_user.is_user = True
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        self.created_mock_user.save()
        self.client.post(self.URL_USER_UPLOAD_CV, {'cv': self.test_file_cv})
        self.assertEqual(Account.objects.get(email=self.EMAIL_TEST).userprofile.cv.name, self.DEFAULT_CV)

        self.client.post(self.URL_USER_DELETE_CV)
        self.assertEqual(Account.objects.get(email=self.EMAIL_TEST).userprofile.cv, '')
        Account.objects.get(email=self.EMAIL_TEST).userprofile.cv.delete()

    def test_delete_cv_user_no_cv_should_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.assertEqual(self.created_mock_user.userprofile.cv.name, None)

        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        self.client.post(self.URL_USER_DELETE_CV)
        self.assertEqual(self.created_mock_user.userprofile.cv.name, None)

    def test_access_user_dashboard_api_get_table_url_logged_in_should_return_200(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username=self.EMAIL_TEST, password=self.PASSWORD_TEST)
        response = self.client.get('/user/dashboard/api/get-all-lamaran-for-dashboard-table/')
        self.assertEqual(response.status_code, 200)

    def test_access_user_dashboard_api_get_table_url_not_logged_in_should_return_200(self):
        response = self.client.get('/user/dashboard/api/get-all-lamaran-for-dashboard-table/')
        self.assertEqual(response.status_code, 200)

    def test_list_of_lowongan_to_json_has_data_should_return_mock_status(self):
        data = list_of_lowongan_to_json_dict(
            [self.mock_user_lamar_magang]
        )['data'][0][0]
        self.assertEqual(data, 'MockStatus')

    def test_list_of_lowongan_to_json_has_data_should_return_mock_html_a_tag(self):
        data = list_of_lowongan_to_json_dict(
            [self.mock_user_lamar_magang]
        )['data'][0][1]
        self.assertEqual(data, '<a href="/user/dashboard/status-lamaran/{}/">MockJudulLowongan</a>'.format(
            self.mock_user_lamar_magang.pk))

    def test_list_of_lowongan_to_json_has_data_should_return_username(self):
        data = list_of_lowongan_to_json_dict(
            [self.mock_user_lamar_magang]
        )['data'][0][2]
        self.assertEqual(data, 'MockName')

    def test_list_of_lowongan_to_json_no_data_should_return_empty_list(self):
        data = list_of_lowongan_to_json_dict(
            []
        )['data']
        self.assertEqual(data, [])

    def test_status_lamaran_page_no_login_should_return_error_permission_denied(self):
        response = self.client.get('/user/dashboard/status-lamaran/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '[ERROR] Permission Denied')

    def test_status_lamaran_page_logged_in_access_lamaran_wrong_id_should_return_error_lamaran_not_found(self):
        self.client.login(username='test@mail.com', password='12345678')
        response = self.client.get('/user/dashboard/status-lamaran/999/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '[ERROR] Lamaran Not Found')

    def test_status_lamaran_page_logged_in_has_lamaran_correct_lamaran_id_should_not_return_error_not_found(self):
        self.mock_user_lamar_magang.pk = 1
        self.mock_user_lamar_magang.save()
        self.client.login(username='test@mail.com', password='12345678')
        response = self.client.get('/user/dashboard/status-lamaran/1/')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content.decode('utf-8'), '[ERROR] Lamaran Not Found')

    def test_status_lamaran_page_logged_in_has_no_lamaran_access_other_user_lamaran_should_be_error_denied(self):
        self.mock_user_lamar_magang.pk = 2
        self.mock_user_lamar_magang.user_foreign_key = self.mock_opd
        self.mock_user_lamar_magang.save()
        self.client.login(username='test@mail.com', password='12345678')
        response = self.client.get('/user/dashboard/status-lamaran/2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), '[ERROR] Permission Denied')


class UserFunctionalTest(TestCase):
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(
            chrome_options=chrome_options,
            executable_path='./chromedriver',
        )

    def tearDown(self):
        self.driver.quit()
        super(UserFunctionalTest, self).tearDown()

    # This function is just to make sure that chromedriver is properly installed on gitlab pipeline
    def test_input_status_selenium(self):
        self.driver.get(url='http://localhost:8000/')
