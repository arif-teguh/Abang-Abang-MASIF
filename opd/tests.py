from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest
from . import views
from account.models import Account
from lowongan.models import Lowongan
from .opd_login_form import OpdAuthenticationForm


class LoginOpdUnitTest(TestCase):
    #login
    def test_page_title_opd_login(self):
        request = HttpRequest()
        response = views.opd_login(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>OPD Login</title>', html_response)

    def test_opd_login_template(self):
        response = self.client.get('/opd/login/')
        self.assertTemplateUsed(response,'opd_login.html')
        

    def test_submit_button_exist(self):
        request = HttpRequest()
        response = views.opd_login(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button type="submit"', html_response)


    def test_opd_login_page_is_set_up_as_expected(self):
        response = Client().get('/opd/login/')
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertTrue(isinstance(form, OpdAuthenticationForm), type(form).__mro__)

    def test_displays_opd_login_form(self):
        response = Client().get('/opd/login/')
        self.assertIsInstance(response.context["form"], OpdAuthenticationForm)

    def test_opd_page_not_authenticated(self):
        response = Client().get('/opd/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/account-redirector', response.url)

class OpdRedirectUnitTest(TestCase):
    def test_opd_access_opd_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = False
        request.user.is_opd = True
        request.user.is_user = False
        request.user.is_superuser = False
        response = views.opd_index(request=request)
        self.assertEqual(response.status_code, 200)

    def test_admin_access_opd_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = True
        request.user.is_opd = False
        request.user.is_user = False
        request.user.is_superuser = False
        response = views.opd_index(request=request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/account-redirector', response.url)

    def test_user_access_opd_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = False
        request.user.is_opd = False
        request.user.is_user = True
        request.user.is_superuser = False
        response = views.opd_index(request=request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/account-redirector', response.url)

    def test_using_opd_index_func(self):
        found = resolve('/opd/')
        self.assertEqual(found.func, views.admin_index)






    def test_opd_lowongan_template(self):
        response = self.client.get('/opd/lowongan/')
        self.assertTemplateUsed(response,'opd_lowongan.html')

    def test_using_opd_index_func(self):
        found = resolve('/opd/lowongan/')
        self.assertEqual(found.func, views.opd_lowongan)

    
class LowonganOpdUnitTest(TestCase):
    def test_click_lowongan_button_exist(self):
        request = HttpRequest()
        response = views.opd_lowongan(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button ', html_response)

    def test_page_title_opd_lowongan(self):
        request = HttpRequest()
        response = views.opd_lowongan(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>lowongan</title>', html_response)

