from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import resolve

from account.models import Account
from . import views
from .admin_login_form import AdminAuthenticationForm


class AdminUnitTest(TestCase):
    def test_page_title_admin_login(self):
        request = HttpRequest()
        response = views.admin_login(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Admin Login</title>', html_response)

    def test_using_admin_login_html(self):
        response = Client().get('/admin/login/')
        self.assertTemplateUsed(response, 'admin/admin_login.html')

    def test_submit_button_exist(self):
        request = HttpRequest()
        response = views.admin_login(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button type="submit"', html_response)

    def test_admin_login_page_is_set_up_as_expected(self):
        response = Client().get('/admin/login/')
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertTrue(
            isinstance(form, AdminAuthenticationForm), type(form).__mro__)

    def test_displays_admin_login_form(self):
        response = Client().get('/admin/login/')
        self.assertIsInstance(response.context["form"], AdminAuthenticationForm)

    def test_admin_page_not_authenticated(self):
        response = Client().get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/account-redirector', response.url)

    def test_admin_access_admin_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = True
        request.user.is_opd = False
        request.user.is_user = False
        request.user.is_superuser = False
        response = views.admin_index(request=request)
        self.assertEqual(response.status_code, 200)

    def test_opd_access_admin_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = False
        request.user.is_opd = True
        request.user.is_user = False
        request.user.is_superuser = False
        response = views.admin_index(request=request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/account-redirector', response.url)

    def test_user_access_admin_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = False
        request.user.is_opd = False
        request.user.is_user = True
        request.user.is_superuser = False
        response = views.admin_index(request=request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/account-redirector', response.url)

    def test_using_admin_index_func(self):
        found = resolve('/admin/')
        self.assertEqual(found.func, views.admin_index)
