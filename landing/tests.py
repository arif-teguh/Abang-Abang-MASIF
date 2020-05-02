from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.test import TestCase
from django.urls import resolve

from account.models import Account
from artikel.models import Artikel
from lowongan.models import Lowongan
from . import views
from .views import query_n_number_of_newest_lowongan


class LandingPageUnitTest(TestCase):

    def setUp(self):
        self.mock_date = datetime(2012, 1, 1)
        self.email = 'a@a.com'
        self.password = '12345678'
        self.created_mock_user = Account.objects.create_user(
            email=self.email,
            password=self.password,
        )
        self.created_mock_user.name = 'TestName'
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.mock_opd = Account.objects.create_user(
            email='mockopd@mail.com',
            password='12341234',
        )
        self.mock_opd.is_opd = True
        self.mock_opd.name = 'MockOPDName'
        self.mock_opd.save()

        self.article_one = Artikel.objects.create(
            judul='MockJudul1',
            deskripsi='MockDeskripsiLanding1',
            foto_artikel=SimpleUploadedFile("mock1.jpg", b"file_content")
        )
        self.article_two = Artikel.objects.create(
            judul='MockJudul2',
            deskripsi='Mock Deskripsi Landing2',
            foto_artikel=SimpleUploadedFile("mock1.jpg", b"file_content")
        )
        self.article_one.save()
        self.article_two.save()
        self.client_get_landing = Client().get('/')

    def test_landing_page_should_return_code_200(self):
        self.assertEqual(self.client_get_landing.status_code, 200)

    def test_landing_template_should_use_landing_page_html(self):
        self.assertTemplateUsed(self.client_get_landing, 'landing_page.html')

    def test_landing_title_should_have_title_beranda(self):
        html_response = self.client_get_landing.content.decode('utf8')
        self.assertIn('<title>Beranda</title>', html_response)

    def test_landing_func_should_user_landing_function(self):
        found = resolve('/')
        self.assertEqual(found.func, views.landing)

    def test_logout_func_fail_if_not_logged_in(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_logout_func_success_if_logged_in_redirect(self):
        self.client.login(username=self.email, password=self.password)
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def add_10_lowongan_setup(self):
        test_lowongan = []
        for i in range(10):
            mock_lowongan = Lowongan(judul='judul' + str(i),
                                     kategori='kat1',
                                     kuota_peserta=10,
                                     waktu_awal_magang=self.mock_date,
                                     waktu_akhir_magang=self.mock_date,
                                     batas_akhir_pendaftaran=self.mock_date,
                                     berkas_persyaratan=['Kartu Keluarga'],
                                     deskripsi='deskripsi1',
                                     requirement='requirement1',
                                     opd_foreign_key_id=self.mock_opd.id)
            test_lowongan.append(mock_lowongan)
            mock_lowongan.save()
        return test_lowongan

    def test_query_5_lowongan_exist_10_lowongan_should_return_5(self):
        test_lowongan = self.add_10_lowongan_setup()
        test_lowongan.reverse()

        self.assertEqual(len(query_n_number_of_newest_lowongan(5)), 5)
        self.assertEqual(list(query_n_number_of_newest_lowongan(5)), test_lowongan[:5])

    def test_query_1_lowongan_exist_10_lowongan_should_return_1(self):
        test_lowongan = self.add_10_lowongan_setup()
        test_lowongan.reverse()

        self.assertEqual(len(query_n_number_of_newest_lowongan(1)), 1)
        self.assertEqual(list(query_n_number_of_newest_lowongan(1)), [test_lowongan[0]])

    def test_query_0_lowongan_exist_10_lowongan_should_return_0(self):
        self.add_10_lowongan_setup()

        self.assertEqual(len(query_n_number_of_newest_lowongan(0)), 0)
        self.assertEqual(list(query_n_number_of_newest_lowongan(0)), [])

    def test_query_12_lowongan_exist_10_lowongan_should_return_only_10_lowongan(self):
        test_lowongan = self.add_10_lowongan_setup()
        test_lowongan.reverse()
        self.assertEqual(len(query_n_number_of_newest_lowongan(12)), 10)
        self.assertEqual(list(query_n_number_of_newest_lowongan(12)), test_lowongan)

    def test_query_5_lowongan_exist_0_lowongan_should_return_0_lowongan(self):
        self.assertEqual(len(query_n_number_of_newest_lowongan(5)), 0)
        self.assertEqual(list(query_n_number_of_newest_lowongan(5)), [])

    def test_query_all_article_should_return_all_article(self):
        self.assertEqual(list(self.client_get_landing.context['articles']), list(Artikel.objects.all()))

    def test_query_all_article_should_not_return_empty_list(self):
        self.assertNotEqual(list(self.client_get_landing.context['articles']), [])
