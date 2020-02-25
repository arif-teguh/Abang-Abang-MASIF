from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import resolve

from . import views


class AdminUnitTest(TestCase):
    def test_admin_url_exist(self):
        response = Client().get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_login_using_admin_login_function(self):
        function_used = resolve('/admin/login/')
        self.assertEqual(function_used.func, views.admin_login)

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

# Create your tests here.
