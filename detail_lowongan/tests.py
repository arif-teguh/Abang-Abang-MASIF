from django.test import TestCase
from django.test import Client
from django.urls import resolve
from . import views


# Create your tests here.

class Testing_detail_lowongan(TestCase):
    URL_DETAIL_LOWONGAN = '/cari-lowongan/detail-lowongan/'

    def test_detail_lowongan_page_response_status(self):
        response = Client().get(self.URL_DETAIL_LOWONGAN)
        self.assertEqual(response.status_code, 200)

    def test_detail_lowongan_template(self):
        response = Client().get(self.URL_DETAIL_LOWONGAN)
        self.assertTemplateUsed(response, 'detail_lowongan.html')

    def test_detail_lowongan_content(self):
        response = Client().get(self.URL_DETAIL_LOWONGAN)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Detail Lowongan</title>', html_response)

    def test_detail_lowongan_func(self):
        found = resolve(self.URL_DETAIL_LOWONGAN)
        self.assertEqual(found.func, views.detail_lowongan)
