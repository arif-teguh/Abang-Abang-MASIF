from django.test import TestCase
from django.test import Client
from django.urls import resolve
from . import views


# Create your tests here.

class Testing_cari_lowongan(TestCase):
    URL_CARI_LOWONGAN = '/cari-lowongan/'

    def test_cari_lowongan_page_response_status(self):
        response = Client().get(self.URL_CARI_LOWONGAN)
        self.assertEqual(response.status_code, 200)

    def test_cari_lowongan_template(self):
        response = Client().get(self.URL_CARI_LOWONGAN)
        self.assertTemplateUsed(response, 'cari_lowongan.html')

    def test_cari_lowongan_content(self):
        response = Client().get(self.URL_CARI_LOWONGAN)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Cari Lowongan</title>', html_response)

    def test_cari_lowongan_func(self):
        found = resolve(self.URL_CARI_LOWONGAN)
        self.assertEqual(found.func, views.cari_lowongan)
