from django.http import HttpRequest
from django.test import TestCase, Client

from . import views
from .admin_login_form import AdminAuthenticationForm


class AdminUnitTest(TestCase):
    def test_admin_url_exist(self):
        response = Client().get('/admin/')
        self.assertEqual(response.status_code, 200)

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

    # Create your tests here.
