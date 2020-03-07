from django.test import TestCase
from django.test import Client
from django.urls import resolve

from account.models import Account
from lowongan.models import Lowongan
from . import views


# Create your tests here.

class TestingDetailLowongan(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.opd1 = Account.objects.all()[0]
        self.client.force_login(self.account1)
        self.lowongan1 = Lowongan.objects.create(
            judul='judul1',
            penyedia='opd1',
            jumlah_tersedia=10,
            durasi_magang=10,
            jangka_waktu_lamaran=10,
            berkas='berkas1',
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.opd1.id
        )

    def test_detail_lowongan_page_response_status(self):
        response = Client().get('/cari-lowongan/detail-lowongan/' + str(self.lowongan1.id))
        self.assertEqual(response.status_code, 200)

    def test_detail_lowongan_template(self):
        response = Client().get('/cari-lowongan/detail-lowongan/' + str(self.lowongan1.id))
        self.assertTemplateUsed(response, 'detail_lowongan.html')

    def test_detail_lowongan_content(self):
        response = Client().get('/cari-lowongan/detail-lowongan/' + str(self.lowongan1.id))
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Detail Lowongan</title>', html_response)

    def test_detail_lowongan_func(self):
        found = resolve('/cari-lowongan/detail-lowongan/' + str(self.lowongan1.id))
        self.assertEqual(found.func, views.detail_lowongan)
