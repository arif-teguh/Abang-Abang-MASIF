from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import resolve

from .apps import LowonganConfig
from django.apps import apps
from account.models import Account, OpdProfile
from .models import Lowongan
from . import views

url_form_lowongan = '/lowongan/opd/form/'
'''
class LowonganFormTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user('test_user', password='test_user')
        self.client.login(username='test_user', password='test_user')

        self.lowongan_obj = Lowongan.objects.create(
            judul='judul1',
            penyedia='opd1',
            jumlah_tersedia=10,
            durasi_magang=10,
            jangka_waktu_lamaran=10,
            berkas='berkas1',
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.user.id
        )
    def test_form_lowongan_url_exist(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=True)
        response = self.client.get(url_form_lowongan)
        self.assertEqual(response.status_code, 200)

    def test_form_lowongan_url_for_non_opd(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=False)
        response = self.client.get(url_form_lowongan)
        self.assertEqual(response.status_code, 302)

    def test_form_lowongan_using_form_lowongan_function(self):
        function_used = resolve(url_form_lowongan)
        self.assertEqual(function_used.func, views.show_form_lowongan)

    def test_form_lowongan_using_template_form_lowongan(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=True)
        response = self.client.get(url_form_lowongan)
        self.assertTemplateUsed(response, 'lowongan/form_lowongan.html')
  
    def test_post_form_lowongan_failed_and_redirect(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=True)
        response = self.client.post(url_form_lowongan+"post/")
        self.assertEqual(response.status_code, 302)
    
    def test_post_form_lowongan_url_for_non_opd(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=False)
        response = self.client.get(url_form_lowongan+"post/")
        self.assertEqual(response.status_code, 302)

    def test_post_form_lowongan_url_for_opd_and_form_is_valid(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=True)
        data_form_lowongan = {
            "judul" :'judul1',
            "penyedia" :'opd1',
            "jumlah_tersedia":10,
            "durasi_magang":10,
            "jangka_waktu_lamaran":10,
            "berkas" :'berkas1',
            "deskripsi" :'deskripsi1',
            "requirement" :'requirement1',
            "opd_foreign_key_id" :self.user.id
        }    
        response = self.client.post(url_form_lowongan+"post/", data_form_lowongan)
        self.assertTrue(Lowongan.objects.filter(judul="judul1").exists())
        self.assertEqual(response.status_code, 302) 

    def test_update_form_lowongan_url_for_non_opd(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=False)
        response = self.client.get(url_form_lowongan+"edit/111/")
        self.assertEqual(response.status_code, 302)

    def test_update_form_lowongan_url_for_opd_and_form_not_is_valid(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=True)
        id_lowongan = str(self.lowongan_obj.id)
        response = self.client.get(url_form_lowongan+"edit/"+id_lowongan+"/")
        self.assertEqual(response.status_code, 200)
    
    def test_update_form_lowongan_url_for_opd_and_form_is_valid(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=True)
        id_lowongan = self.lowongan_obj.id
        data_form_lowongan = {
            "id":id_lowongan,
            "judul":'IniUpdate',
            "penyedia" :'opd1',
            "jumlah_tersedia":10,
            "durasi_magang":10,
            "jangka_waktu_lamaran":10,
            "berkas" :'berkas1',
            "deskripsi" :'deskripsi1',
            "requirement" :'requirement1',
            "opd_foreign_key_id" :self.user.id
        }   
        response = self.client.post(url_form_lowongan+"edit/"+str(id_lowongan)+"/", data_form_lowongan)
        self.assertTrue(Lowongan.objects.filter(judul="IniUpdate").exists()) 
        self.assertEqual(response.status_code, 302)

class LowonganModelTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.opd1 = Account.objects.all()[0]
        opd_profile = OpdProfile(user=self.opd1,
                                 unique_opd_attribute="opd")
        opd_profile.save()

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

    def test_object_opd_dibuat(self):
        self.assertTrue(type(self.opd1), Lowongan)

    def test_object_lowongan_is_created(self):
        self.assertTrue(type(self.lowongan1), Lowongan)

    def test_id_lowongan_is_generated(self):
        self.assertIsNotNone(self.lowongan1.id)

    def test_judul_is_judul1(self):
        self.assertEqual(self.lowongan1.judul, "judul1")

    def test_penyedia_is_opd1(self):
        self.assertEqual(self.lowongan1.penyedia, "opd1")

    def test_jumlah_tersedia_is_10(self):
        self.assertEqual(self.lowongan1.jumlah_tersedia, 10)

    def test_durasi_magang_is_10(self):
        self.assertEqual(self.lowongan1.durasi_magang, 10)
    
    def test_jangka_waktu_lamaran_is_10(self):
        self.assertEqual(self.lowongan1.jangka_waktu_lamaran, 10)

    def test_berkas_is_berkas1(self):
        self.assertEqual(self.lowongan1.berkas, "berkas1")

    def test_deskripsi_is_deskripsi1(self):
        self.assertEqual(self.lowongan1.deskripsi, "deskripsi1")

    def test_requirement_is_requirement1(self):
        self.assertEqual(self.lowongan1.requirement, "requirement1")

    def test_id_opd_is_foreign_key_from_Opd(self):
        self.assertEqual(self.lowongan1.opd_foreign_key_id, self.opd1.id)

    def test_func_str_in_lowongan1(self):
        self.assertEqual(self.lowongan1.__str__(), 'judul1')

class AppsTest(TestCase):
    def test_apps(self):
        self.assertEqual(LowonganConfig.name, 'lowongan')
        self.assertEqual(apps.get_app_config('lowongan').name, 'lowongan')