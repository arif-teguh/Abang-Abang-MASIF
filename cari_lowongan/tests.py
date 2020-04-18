from django.test import TestCase
from django.test import Client
from django.urls import resolve
from . import views

class TestingCariLowongan(TestCase):
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

    def test_cari_lowongan_post(self):
        response = Client().post('/cari-lowongan/')
        self.assertEqual(response.status_code, 302)



class test_sort_by_deadline(TestCase):

    def test_sorting_asc_page_response_status(self):
        response = Client().get('/cari-lowongan/sorting/batas-akhir/asc')
        self.assertEqual(response.status_code, 200)

    def test_sorting_desc_page_response_status(self):
        response = Client().get('/cari-lowongan/sorting/batas-akhir/desc')
        self.assertEqual(response.status_code, 200)

    def test_sorting_other_param_response_status(self):
        response = Client().get('/cari-lowongan/sorting/batas-akhir/dtogijt')
        self.assertEqual(response.status_code, 302)

    def test_sorting_page_response_status_post(self):
        response1 = Client().post('/cari-lowongan/sorting/batas-akhir/asc')
        response2 = Client().post('/cari-lowongan/sorting/batas-akhir/desc')
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)

class test_sort_by_waktu_magang(TestCase):

    def test_sorting_asc_page_response_status(self):
        response = Client().get('/cari-lowongan/sorting/waktu-magang/asc')
        self.assertEqual(response.status_code, 200)

    def test_sorting_desc_page_response_status(self):
        response = Client().get('/cari-lowongan/sorting/waktu-magang/desc')
        self.assertEqual(response.status_code, 200)

    def test_sorting_other_param_response_status(self):
        response = Client().get('/cari-lowongan/sorting/waktu-magang/dtogijt')
        self.assertEqual(response.status_code, 302)

    def test_sorting_page_response_status_post(self):
        response1 = Client().post('/cari-lowongan/sorting/waktu-magang/asc')
        response2 = Client().post('/cari-lowongan/sorting/waktu-magang/desc')
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)

class test_search(TestCase):

    def test_search_page_response_status(self):
        response = Client().get('/cari-lowongan/searching/end')
        self.assertEqual(response.status_code, 200)

    def test_search_page_response_status_post(self):
        response = Client().post('/cari-lowongan/searching/end')
        self.assertEqual(response.status_code, 302)