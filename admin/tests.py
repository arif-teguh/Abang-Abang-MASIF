from django.core import mail
from django.core.exceptions import ValidationError
from django.forms import forms
from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import resolve

from account.models import Account
from admin import views
from admin.admin_login_form import AdminAuthenticationForm
from admin.opd_registration_form import OpdRegistrationForm
from artikel.models import Artikel
from . import mailing, token
from .models import OpdVerificationList

TEST_EMAIL = 'test@mail.com'
TEST_PASSWORD = '12345678'
URL_ADMIN_LOGIN = '/admin/login/'
URL_ADMIN_BASE = '/admin/'
URL_ADMIN_DELETE_OPD = '/admin/listopd/deleteopd/'


class AdminUnitTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.request = HttpRequest()
        Account.objects.create_user(email=TEST_EMAIL, password=TEST_PASSWORD)
        self.created_mock_user = Account.objects.all()[0]
        self.client.login(username=TEST_EMAIL, password=TEST_PASSWORD)
        self.request.user = self.created_mock_user

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_page_title_admin_login(self):
        response = views.admin_login(self.request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Admin Login</title>', html_response)

    def test_using_admin_login_html(self):
        response = Client().get(URL_ADMIN_LOGIN)
        self.assertTemplateUsed(response, 'admin/admin_login.html')

    def test_submit_button_exist(self):
        request = HttpRequest()
        response = views.admin_login(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button type="submit"', html_response)

    def test_admin_login_page_is_set_up_as_expected(self):
        response = Client().get(URL_ADMIN_LOGIN)
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertTrue(
            isinstance(form, AdminAuthenticationForm), type(form).__mro__)

    def test_displays_admin_login_form(self):
        response = Client().get(URL_ADMIN_LOGIN)
        self.assertIsInstance(response.context["form"], AdminAuthenticationForm)

    def test_admin_page_not_authenticated(self):
        response = Client().get(URL_ADMIN_BASE)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(URL_ADMIN_LOGIN, response.url)

    def test_admin_access_admin_page(self):
        self.request.user.is_admin = True
        self.request.user.is_opd = False
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.admin_index(request=self.request)
        self.assertEqual(response.status_code, 200)

    def test_opd_access_admin_page(self):
        self.request.user.is_admin = False
        self.request.user.is_opd = True
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.admin_index(request=self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(URL_ADMIN_LOGIN, response.url)

    def test_user_access_admin_page(self):
        self.request.user.is_admin = False
        self.request.user.is_opd = False
        self.request.user.is_user = True
        self.request.user.is_superuser = False
        response = views.admin_index(request=self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(URL_ADMIN_LOGIN, response.url)

    def test_admin_access_admin_page_through_url(self):
        self.created_mock_user.is_admin = True
        self.created_mock_user.save()
        response = self.client.get(URL_ADMIN_BASE)
        self.assertEqual(response.status_code, 200)

    def test_opd_access_admin_page_through_url(self):
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_opd = True
        self.created_mock_user.save()
        response = self.client.get(URL_ADMIN_BASE)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(URL_ADMIN_LOGIN, response.url)

    def test_user_access_admin_page_through_url(self):
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        response = self.client.get(URL_ADMIN_BASE)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(URL_ADMIN_LOGIN, response.url)

    def test_using_admin_index_func(self):
        found = resolve(URL_ADMIN_BASE)
        self.assertEqual(found.func, views.admin_index)

    def test_admin_list_opd_not_authenticated_redirect_to_admin_login(self):
        response = Client().get('/admin/listopd/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(URL_ADMIN_LOGIN, response.url)

    def test_using_admin_list_opd_func(self):
        found = resolve('/admin/listopd/')
        self.assertEqual(found.func, views.admin_list_opd)

    def test_admin_access_admin_opd_list_page(self):
        self.request.user.is_admin = True
        self.request.user.is_opd = False
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.admin_list_opd(request=self.request)
        self.assertEqual(response.status_code, 200)

    def test_opd_access_admin_opd_list_page(self):
        self.request.user.is_admin = False
        self.request.user.is_opd = True
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.admin_list_opd(request=self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(URL_ADMIN_LOGIN, response.url)

    def test_user_access_admin_opd_list_page(self):
        self.request.user.is_admin = False
        self.request.user.is_opd = False
        self.request.user.is_user = True
        self.request.user.is_superuser = False
        response = views.admin_list_opd(request=self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(URL_ADMIN_LOGIN, response.url)

    def test_function_get_all_opd_database_has_opd(self):
        self.created_mock_user.is_opd = True
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.save()
        all_opd = views.get_all_opd()
        self.assertEqual([self.created_mock_user], all_opd)

    def test_function_get_all_opd_database_empty(self):
        all_opd = views.get_all_opd()
        self.assertEqual([], all_opd)

    def test_function_get_all_opd_database_has_admin(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.save()
        all_opd = views.get_all_opd()
        self.assertEqual([], all_opd)

    def test_function_get_all_opd_database_has_user(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = True
        self.created_mock_user.is_staff = False
        self.created_mock_user.save()
        all_opd = views.get_all_opd()
        self.assertEqual([], all_opd)

    def test_confirm_login_allowed_function_as_admin_is_active(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.save()
        admin_auth_form = AdminAuthenticationForm()
        result = admin_auth_form.confirm_login_allowed(
            user=self.created_mock_user
        )
        self.assertEqual(None, result)

    def test_confirm_login_allowed_function_as_opd_is_active(self):
        self.created_mock_user.is_opd = True
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        admin_auth_form = AdminAuthenticationForm()
        self.created_mock_user.save()
        with self.assertRaises(forms.ValidationError):
            admin_auth_form.confirm_login_allowed(user=self.created_mock_user)

    def test_confirm_login_allowed_function_as_user_is_active(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = True
        self.created_mock_user.is_staff = False
        self.created_mock_user.save()
        admin_auth_form = AdminAuthenticationForm()
        with self.assertRaises(forms.ValidationError):
            admin_auth_form.confirm_login_allowed(user=self.created_mock_user)

    def test_confirm_login_allowed_function_as_admin_is_not_active(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        admin_auth_form = AdminAuthenticationForm()
        with self.assertRaises(forms.ValidationError):
            admin_auth_form.confirm_login_allowed(user=self.created_mock_user)

    def test_confirm_login_allowed_function_as_opd_is_not_active(self):
        self.created_mock_user.is_opd = True
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        admin_auth_form = AdminAuthenticationForm()
        with self.assertRaises(forms.ValidationError):
            admin_auth_form.confirm_login_allowed(user=self.created_mock_user)

    def test_confirm_login_allowed_function_as_user_is_not_active(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = True
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        admin_auth_form = AdminAuthenticationForm()
        with self.assertRaises(forms.ValidationError):
            admin_auth_form.confirm_login_allowed(user=self.created_mock_user)

    def test_delete_opd_account_correct_pk(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        response = self.client.post(
            URL_ADMIN_DELETE_OPD,
            {'pk': self.created_mock_user.pk}
        )
        all_test_opd = list(Account.objects.all())
        self.assertEqual(
            'Delete OPD Success', response.content.decode('utf8')
        )
        self.assertEqual(all_test_opd, [])

    def test_delete_opd_account_wrong_pk(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        with self.assertRaises(IndexError):
            self.client.post(
                URL_ADMIN_DELETE_OPD,
                {'pk': int(self.created_mock_user.pk) + 1}
            )

    def test_delete_opd_account_string_pk(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        with self.assertRaises(ValueError):
            self.client.post(
                URL_ADMIN_DELETE_OPD,
                {'pk': 'abcdef'}
            )

    def test_delete_opd_account_mix_string_int_pk(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        with self.assertRaises(ValueError):
            self.client.post(URL_ADMIN_DELETE_OPD, {'pk': 'g4bung'})

    def test_delete_opd_account_no_pk(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        with self.assertRaises(ValueError):
            self.client.post(URL_ADMIN_DELETE_OPD, {'pk': ''})

    def test_delete_opd_account_correct_pk_not_admin(self):
        self.created_mock_user.is_opd = True
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        self.client.post(
            URL_ADMIN_DELETE_OPD,
            {'pk': self.created_mock_user.pk}
        )
        all_test_opd = list(Account.objects.all())
        self.assertEqual(
            [self.created_mock_user],
            all_test_opd
        )

    def test_get_method_in_delete_opd_for_admin(self):
        response = self.client.get(URL_ADMIN_DELETE_OPD)
        html_response = response.content.decode('utf8')
        self.assertEqual("Forbidden", html_response)

    def information_test_setUp(self):
        self.artikel1 = Artikel.objects.create(
            judul='judulsatu',
            deskripsi='deskripsisatu',
            foto_artikel='mockfotosatu',
        )
        self.artikel2 = Artikel.objects.create(
            judul='juduldua',
            deskripsi='deskripsidua',
            foto_artikel='mockfotodua',
        )
        self.artikel1.save()
        self.artikel2.save()
        self.admin_information_url = '/admin/information/'
        self.test_mail_admin = 'admin@mail.com'
        self.test_mail_password = '332211'
        self.admin_obj_test = Account.objects.create_user(email=self.test_mail_admin,
                                                          password=self.test_mail_password)
        self.admin_obj_test.is_admin = True
        self.admin_obj_test.save()
        self.client_admin_loggedin = Client()
        self.client_admin_loggedin.login(username=self.test_mail_admin, password=self.test_mail_password)
        self.response_logged_in_info_page = self.client_admin_loggedin.get(self.admin_information_url)

    def test_admin_information_logged_in_should_return_200(self):
        self.information_test_setUp()
        self.assertEqual(self.response_logged_in_info_page.status_code, 200)

    def test_admin_information_not_logged_in_should_return_302(self):
        self.information_test_setUp()
        response = Client().get(self.admin_information_url)
        self.assertEqual(response.status_code, 302)

    def test_information_page_query_all_artikel_should_return_all_article(self):
        self.information_test_setUp()
        self.assertEqual(self.response_logged_in_info_page.context['articles'], [self.artikel1, self.artikel2])

    def test_information_page_should_not_return_empty_list(self):
        self.information_test_setUp()
        self.assertNotEqual(self.response_logged_in_info_page.context['articles'], [])

    def test_information_page_no_article_should_return_empty_list(self):
        self.information_test_setUp()
        self.artikel1.delete()
        self.artikel2.delete()
        self.assertEqual(
            self.client_admin_loggedin.get(self.admin_information_url).context.get('articles', None), [])
        self.assertNotEqual(self.response_logged_in_info_page.context['articles'], [self.artikel1, self.artikel2])


class EmailTest(TestCase):
    verification_url = '/user/verification/token'
    recipient_email = 'test@test.com'

    def test_send_email_sent(self):
        mailing.send_verification_email(
            self.verification_url,
            self.recipient_email,
            "OPD"
        )
        self.assertEqual(len(mail.outbox), 1)
        mail.outbox = []

    def test_email_subject(self):
        mailing.send_verification_email(
            self.verification_url,
            self.recipient_email,
            "OPD"
        )
        self.assertEqual(mail.outbox[0].subject, 'Verifikasi Akun')
        mail.outbox = []

    def test_email_body(self):
        mailing.send_verification_email(
            self.verification_url,
            self.recipient_email,
            "OPD"
        )
        self.assertIn(self.verification_url, mail.outbox[0].body)
        mail.outbox = []

    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            mailing.send_verification_email(self.verification_url,
                                            "test.com",
                                            "OPD")

    def test_generate_token(self):
        secret = token.generate_opd_token()
        secret_length = len(secret)
        self.assertEqual(secret_length, 22)


class OpdRegistrationTest(TestCase):
    SECOND_EMAIL = 'a@a.com'

    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.request = HttpRequest()
        self.SECRET = 'qdawedcvdswe1'
        self.PHONE = '1234567'
        self.DATA = {'opd_name': "test", 'email': TEST_EMAIL,
                     'phone': self.PHONE,
                     'secret': self.SECRET}
        Account.objects.create_superuser(email=TEST_EMAIL, password=TEST_PASSWORD)
        self.created_mock_user = Account.objects.all()[0]
        self.client.login(username=TEST_EMAIL, password=TEST_PASSWORD)
        self.request.user = self.created_mock_user

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_page_title_register_opd_page(self):
        response = views.admin_register_opd(self.request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Daftar OPD</title>', html_response)

    def test_submit_button_exist(self):
        response = views.admin_register_opd(self.request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button type="submit"', html_response)

    def test_using_admin_register_opd_html(self):
        with self.assertTemplateUsed('admin/admin_register_opd.html'):
            response = self.client.get('/admin/listopd/register/')
            self.assertEqual(response.status_code, 200)

    def test_register_opd_page_not_authenticated(self):
        response = Client().get('/admin/listopd/register/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/admin/login', response.url)

    def test_create_opd_duplicated(self):
        with self.assertRaises(ValidationError):
            form = OpdRegistrationForm(self.DATA)
            if form.is_valid():
                form.check()

    def test_create_opd_form_failed_already_on_verification_list(self):
        verification_list = OpdVerificationList(
            secret=self.SECRET,
            name="Test",
            email=self.SECOND_EMAIL,
            phone=self.PHONE
        )
        verification_list.save()

        self.DATA['email'] = self.SECOND_EMAIL

        with self.assertRaises(ValidationError):
            form = OpdRegistrationForm(self.DATA)
            if form.is_valid():
                form.check()

    def test_create_opd_form_success(self):
        self.DATA['email'] = self.SECOND_EMAIL
        form = OpdRegistrationForm(self.DATA)
        if form.is_valid():
            checked_form = form.check()
        self.assertTrue(form.is_valid())
        self.assertIsNotNone(checked_form)

    def test_register_opd_failed_user_already_registered(self):
        user_count = OpdVerificationList.objects.count()
        response = self.client.post(
            "/admin/listopd/register/",
            self.DATA)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OpdVerificationList.objects.count(), user_count)

    def test_register_opd_success(self):
        user_count = OpdVerificationList.objects.count()
        self.DATA['email'] = self.SECOND_EMAIL
        response = self.client.post(
            "/admin/listopd/register/",
            self.DATA)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OpdVerificationList.objects.count(), user_count + 1)
