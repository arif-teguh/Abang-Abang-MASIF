from django.test import TestCase
from django.test import Client
from django.urls import resolve
from . import views


# Create your tests here.

class testing_detail_lowongan(TestCase):

    def test_detail_lowongan_page_response_status(self):
        response = Client().get('/cari-lowongan/detail-lowongan/')
        self.assertEqual(response.status_code, 200)

    def test_detail_lowongan_template(self):
        response = Client().get('/cari-lowongan/detail-lowongan/')
        self.assertTemplateUsed(response, 'detail_lowongan.html')

    def test_detail_lowongan_content(self):
        response = Client().get('/cari-lowongan/detail-lowongan/')
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Detail Lowongan</title>', html_response)

    def test_detail_lowongan_func(self):
        found = resolve('/cari-lowongan/detail-lowongan/')
        self.assertEqual(found.func, views.detail_lowongan)
