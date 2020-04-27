import datetime
from django.test import TestCase
from django.test import Client
from django.urls import resolve

from account.models import Account
from lowongan.models import Lowongan
from . import views

# Create your tests here.
mock_date = datetime.date(2012, 12, 12)


class TestingDetailLowongan(TestCase):
    URL_detail_lowongan = '/cari-lowongan/detail-lowongan/'

    def setUp(self):
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.client.force_login(self.account1)
        self.lowongan1 = Lowongan.objects.create(
            judul='judul1',
            kategori='kat1',
            kuota_peserta=10,
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
            berkas_persyaratan=['Kartu Keluarga'],
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.account1.id
        )

    def test_detail_lowongan_page_response_status(self):
        response = Client().get(self.URL_detail_lowongan + str(self.lowongan1.id))
        self.assertEqual(response.status_code, 200)

    def test_detail_lowongan_template(self):
        response = Client().get(self.URL_detail_lowongan + str(self.lowongan1.id))
        self.assertTemplateUsed(response, 'detail_lowongan.html')

    def test_detail_lowongan_content(self):
        response = Client().get(self.URL_detail_lowongan + str(self.lowongan1.id))
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Detail Lowongan</title>', html_response)

    def test_detail_lowongan_func(self):
        found = resolve(self.URL_detail_lowongan + str(self.lowongan1.id))
        self.assertEqual(found.func, views.detail_lowongan)
