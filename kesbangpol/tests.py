from django.test import TestCase, Client
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView

from account.models import Account, KesbangpolProfile
from .kesbangpol_login_form import KesbangpolAuthenticationForm
from . import views
class KesbangpolLoginTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.request = HttpRequest()
        self.email = "a@a.com"
        self.password = "zxasqw12"
        self.user_name = "abc"
        self.phone = 1234
        self.user_test_account = Account.objects.create_user(
            email=self.email, password=self.password)
        self.user_test_account.is_kesbangpol = True
        self.user_test_account.save()

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_page_title_login_kesbangpol_page(self):
        response = views.kesbangpol_login(self.request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Kesbangpol Login</title>', html_response)

    def test_submit_button_exist(self):
        response = views.kesbangpol_login(self.request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button type="submit"', html_response)

    def test_login_kesbangpol_html(self):
        with self.assertTemplateUsed('kesbangpol_login.html'):
            response = self.client.get('/kesbangpol/login/')
            self.assertEqual(response.status_code, 200)

    def test_login_kesbangpol_form_without_params(self):
        form = KesbangpolAuthenticationForm()
        self.assertFalse(form.is_valid())

    def test_login_kesbangpol_valid_data(self):
        form_data = {"username": self.email, "password": self.password}
        form = KesbangpolAuthenticationForm(data=form_data)
        if form.is_valid():
            form.check()
        self.assertTrue(form.is_valid())

    def test_login_kesbangpol_blank_data(self):
        form_data = {}
        form = KesbangpolAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])
        self.assertEqual(form.errors['password'], ['This field is required.'])

    def test_login_kesbangpol_form_user_not_registered(self):
        with self.assertRaises(ValidationError):
            form_data = {"username": "not_registered@email.com",
                         "password": self.password}
            form = KesbangpolAuthenticationForm(data=form_data)
            if form.is_valid():
                form.check()

    def test_login_kesbangpol_form_password_not_match(self):
        with self.assertRaises(ValidationError):
            form_data = {"username": self.email,
                         'password': "wrongpassword"}
            form = KesbangpolAuthenticationForm(data=form_data)
            if form.is_valid():
                form.check()

    def test_login_kesbangpol_form_user_not_kesbangpol(self):
        self.user_test_account.is_kesbangpol = False
        self.user_test_account.save()

        with self.assertRaises(ValidationError):
            form_data = {"username": self.email, "password": self.password}
            form = KesbangpolAuthenticationForm(data=form_data)
            if form.is_valid():
                form.check()

    def test_login_kesbangpol_success_will_redirect(self):
        user_kesbangpol = KesbangpolProfile(
            user=self.user_test_account,
            unique_kesbangpol_attribute="kesbangpol")
        user_kesbangpol.save()

        response = self.client.post(
            "/kesbangpol/login/",
            {
                'username': self.email,
                'password': self.password,
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")


    def test_login_kesbangpol_email_not_registered_not_redirect(self):
        response = self.client.post(
            "/kesbangpol/login/",
            {
                'username': 'new@email.com',
                'password': self.password
            }
        )
        self.assertEqual(response.status_code, 200)


class KesbangpolDashboardTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.request = HttpRequest()
        self.email = "a@a.com"
        self.password = "zxasqw12"
        self.user_name = "abc"
        self.phone = 1234
        self.user_test_account = Account.objects.create_user(
            email=self.email, password=self.password)
        self.user_test_account.is_kesbangpol = True
        self.user_test_account.save()

    def tearDown(self):
        # Clean up run after every test method.
        pass 
    
    def test_dashboard_kesbangpol_redirect_if_not_login(self):
        response = self.client.get('/kesbangpol/')
        self.assertEqual(response.status_code, 302)

    def test_dashboard_kesbangpol_200_if_login(self):
        self.client.login(username=self.email, password=self.password)
        response = self.client.get('/kesbangpol/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_kesbangpol_html_if_user_login(self):
        self.client.login(username=self.email, password=self.password) 
        with self.assertTemplateUsed('kesbangpol_dashboard.html'):
            response = self.client.get('/kesbangpol/')
            self.assertEqual(response.status_code, 200)
