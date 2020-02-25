from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import resolve

from . import views

class LowonganFormTest(TestCase):
    def test_form_lowongan_url_exist(self):
        response = Client().get('/lowongan/opd/form/')
        self.assertEqual(response.status_code, 200)

    def test_form_lowongan_using_form_lowongan_function(self):
        function_used = resolve('/lowongan/opd/form/')
        self.assertEqual(function_used.func, views.show_form_lowongan)

    def test_form_lowongan_using_template_form_lowongan(self):
        response = Client().get('/lowongan/opd/form/')
        self.assertTemplateUsed(response, 'lowongan/form_lowongan.html')