from django.test import TestCase, Client, override_settings
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from account.models import Account
from user import views
from .models import UserVerificationList
from .user_registration_form import UserRegistrationForm
from .user_login_form import UserAuthenticationForm
from .token import generate_user_token
from unittest import mock
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from social_django.compat import reverse
from social_django.models import UserSocialAuth
from social_django.views import get_session_timeout



# Create your tests here.
class PelamarRegistrationTest(TestCase):
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
            response = self.client.get('/user/register')
            self.assertEqual(response.status_code, 200)

    def test_generate_token(self):
        secret = generate_user_token()
        secret_len = len(secret)
        self.assertEqual(secret_len, 22)

    def test_create_user(self):
        user_count = UserVerificationList.objects.count()
        response = self.client.post(
            "/user/register",
            {'user_name': self.user_name, 'email': self.email,
             'phone': self.phone, 'password': self.password,
             'confirm_password': self.password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserVerificationList.objects.count(), user_count + 1)


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
        response = self.client.get('/user/login/')
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
        response = Client().get('/user/login/')
        self.assertEqual(response.status_code, 200)

    def test_page_template(self):
        response = Client().get('/user/login/')
        self.assertTemplateUsed(response, 'user_login.html')
