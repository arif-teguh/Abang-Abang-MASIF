from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import resolve

from django.contrib.auth.models import User
from account.models import Account, AdminProfile, OpdProfile, AccountManager
from .models import Lowongan
from . import views

url_form_lowongan = '/lowongan/opd/form/'
'''
class LowonganFormTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test_user', password='test_user')
        self.client.login(username='test_user', password='test_user')

    def test_form_lowongan_url_exist(self):
        response = self.client.get(url_form_lowongan)
        self.assertEqual(response.status_code, 200)

    def test_form_lowongan_using_form_lowongan_function(self):
        function_used = resolve(url_form_lowongan)
        self.assertEqual(function_used.func, views.show_form_lowongan)

    def test_form_lowongan_using_template_form_lowongan(self):
        response = self.client.get(url_form_lowongan)
        self.assertTemplateUsed(response, 'lowongan/form_lowongan.html')
'''
class LowonganModelTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.opd1 = Account.objects.all()[0]
        opd_profile = OpdProfile(user=self.opd1,
                                 unique_opd_attribute="opd")
        opd_profile.save()

        self.client.force_login(self.account1)
        self.lowongan1 = Lowongan.objects.create(
            judul = 'judul1',
            penyedia = 'opd1',
            jumlah_tersedia = 10,
            durasi_magang = 10,
            jangka_waktu_lamaran = 10,
            berkas = 'berkas1',
            deskripsi = 'deskripsi1',
            requirement = 'requirement1',
            opd_foreign_key_id = self.opd1.id
        )

    def test_object_opd_dibuat(self):
        self.assertTrue(type(self.opd1), Lowongan)

    def test_object_lowongan_is_created(self):
        self.assertTrue(type(self.lowongan1), Lowongan)

    def test_id_lowongan_is_generated(self):
        self.assertIsNotNone(self.lowongan1.id)

    def test_judul_is_judul1(self):
        self.assertEquals(self.lowongan1.judul, "judul1")

    def test_penyedia_is_opd1(self):
        self.assertEquals(self.lowongan1.penyedia, "opd1")

    def test_jumlah_tersedia_is_10(self):
        self.assertEquals(self.lowongan1.jumlah_tersedia, 10)

    def test_durasi_magang_is_10(self):
        self.assertEquals(self.lowongan1.durasi_magang, 10)
    
    def test_jangka_waktu_lamaran_is_10(self):
        self.assertEquals(self.lowongan1.jangka_waktu_lamaran, 10)

    def test_berkas_is_berkas1(self):
        self.assertEquals(self.lowongan1.berkas, "berkas1")

    def test_deskripsi_is_deskripsi1(self):
        self.assertEquals(self.lowongan1.deskripsi, "deskripsi1")

    def test_requirement_is_requirement1(self):
        self.assertEquals(self.lowongan1.requirement, "requirement1")

    def test_id_opd_is_foreign_key_from_Opd(self):
        self.assertEquals(self.lowongan1.opd_foreign_key_id, self.opd1.id)

    def test_func_str_in_lowongan1(self):
        self.assertEquals(self.lowongan1.__str__(), 'judul1')