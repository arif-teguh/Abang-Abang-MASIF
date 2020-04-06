import datetime
from django.test import TestCase, Client
from django.urls import resolve
from django.apps import apps
from account.models import Account, OpdProfile
from .apps import LowonganConfig
from .models import Lowongan
from . import views
from .form import LowonganForm

url_form_lowongan = '/lowongan/opd/form/'
url_post_lowongan = url_form_lowongan + "post/"
str_kartu_keluarga = "Kartu Keluarga"
str_surat_izin_sekolah = 'Surat Izin Sekolah'
list_berkas = [str_kartu_keluarga]
mock_date = datetime.date(2012, 12, 12)
mock_date2 = datetime.date(2011, 11, 11)
'''
class LowonganFormTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user('test_user',
                                                password='test_user')
        self.client.login(username='test_user', password='test_user')

        self.lowongan_obj = Lowongan.objects.create(
            judul='judul1',
            kategori='kat1',
            kuota_peserta=10,
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
            berkas_persyaratan=['Kartu Keluarga'],
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
    
    def test_form_init_form_to_create_choice_update_form(self):
        choice = (
                (str_kartu_keluarga, str_kartu_keluarga),
                ('Kartu Tanda Penduduk', 'Kartu Tanda Penduduk'),
                (str_surat_izin_sekolah, str_surat_izin_sekolah),
            )
        mock_id_lowongan = self.lowongan_obj.id
        form = LowonganForm(instance=self.lowongan_obj, id=mock_id_lowongan)
        self.assertNotEqual(form.choice, choice)
        self.assertEqual(form.id_lowongan, mock_id_lowongan)

    def test_form_lowongan_using_form_lowongan_function(self):
        function_used = resolve(url_form_lowongan)
        self.assertEqual(function_used.func, views.show_form_lowongan)

    def test_form_lowongan_using_template_form_lowongan(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=True)
        response = self.client.get(url_form_lowongan)
        self.assertTemplateUsed(response, 'lowongan/form_lowongan.html')

    def test_post_form_lowongan_failed_and_reload(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=True)
        response = self.client.post(url_post_lowongan)
        self.assertEqual(response.status_code, 200)

    def test_post_form_lowongan_open_raw_url_redirect(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=True)
        response = self.client.get(url_post_lowongan)
        self.assertEqual(response.status_code, 302)

    def test_post_form_lowongan_url_for_non_opd(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=False)
        response = self.client.get(url_post_lowongan)
        self.assertEqual(response.status_code, 302)

    def test_post_form_lowongan_url_for_opd_and_form_is_valid(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=True)
        data_form_lowongan = {
            "judul" :'judul1',
            "kategori" :'kat1',
            "kuota_peserta":10,
            "waktu_awal_magang" : mock_date,
            "waktu_akhir_magang" : mock_date,
            "batas_akhir_pendaftaran" : mock_date,
            "berkas_persyaratan" :list_berkas,
            "deskripsi" :'deskripsi1',
            "requirement" :'requirement1',
            "opd_foreign_key_id" :self.user.id
        }
        response = self.client.post(url_post_lowongan, data_form_lowongan)
        self.assertTrue(Lowongan.objects.filter(judul="judul1").exists())
        self.assertEqual(response.status_code, 302)

    def test_post_form_is_not_valid_because_waktu_awal_greater_akhir(self):
        Account.objects.filter(pk=self.user.id).update(is_opd=True)
        data_form_lowongan = {
            "judul" :'judul1',
            "kategori" :'kat1',
            "kuota_peserta":10,
            "waktu_awal_magang" : mock_date,
            "waktu_akhir_magang" : mock_date2,
            "batas_akhir_pendaftaran" : mock_date,
            "berkas_persyaratan" :list_berkas,
            "deskripsi" :'deskripsi1',
            "requirement" :'requirement1',
            "opd_foreign_key_id" :self.user.id
        }
        response = self.client.post(url_post_lowongan, data_form_lowongan)
        self.assertEqual(response.status_code, 200)

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
            "kategori" :'kat1',
            "kuota_peserta":10,
            "waktu_awal_magang" : mock_date,
            "waktu_akhir_magang" : mock_date,
            "batas_akhir_pendaftaran" : mock_date,
            "berkas_persyaratan" :list_berkas,
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
            kategori='kat1',
            kuota_peserta=10,
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
            berkas_persyaratan=list_berkas,
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.opd1.id
        )

        self.lowongan2 = Lowongan.objects.create(
            judul='judul2',
            kategori='kat2',
            kuota_peserta=20,
            waktu_awal_magang=mock_date2,
            waktu_akhir_magang=mock_date2,
            batas_akhir_pendaftaran=mock_date2,
            berkas_persyaratan=[str_surat_izin_sekolah],
            deskripsi='deskripsi2',
            requirement='requirement2',
            opd_foreign_key_id=self.opd1.id
        )

    def test_object_opd_dibuat(self):
        self.assertTrue(type(self.opd1), Lowongan)

    def test_object_lowongan_is_created(self):
        self.assertTrue(type(self.lowongan1), Lowongan)
        self.assertTrue(type(self.lowongan2), Lowongan)

    def test_id_lowongan_is_generated(self):
        self.assertIsNotNone(self.lowongan1.id)
        self.assertIsNotNone(self.lowongan2.id)

    def test_judul_is_judul1(self):
        self.assertEqual(self.lowongan1.judul, "judul1")

    def test_kategori_is_kat1(self):
        self.assertEqual(self.lowongan1.kategori, "kat1")

    def test_kuota_peserta_is_10(self):
        self.assertEqual(self.lowongan1.kuota_peserta, 10)

    def test_berkas_persyaratan_is_berkas_persyaratan1(self):
        self.assertEqual(self.lowongan1.berkas_persyaratan, list_berkas)

    def test_deskripsi_is_deskripsi1(self):
        self.assertEqual(self.lowongan1.deskripsi, "deskripsi1")

    def test_requirement_is_requirement1(self):
        self.assertEqual(self.lowongan1.requirement, "requirement1")

    def test_id_opd_is_foreign_key_from_Opd(self):
        self.assertEqual(self.lowongan1.opd_foreign_key_id, self.opd1.id)

    def test_func_str_in_lowongan1(self):
        self.assertEqual(self.lowongan1.__str__(), 'judul1')

    def test_waktu_awal_magang_is_2012_12_12(self):
        self.assertEqual(self.lowongan1.waktu_awal_magang, mock_date)

    def test_waktu_akhir_magang_is_2012_12_12(self):
        self.assertEqual(self.lowongan1.waktu_akhir_magang, mock_date)

    def test_batas_akhir_pendaftaran_is_2012_12_12(self):
        self.assertEqual(self.lowongan1.batas_akhir_pendaftaran, mock_date)

    def test_is_lowongan_masih_berlaku_is_true(self):
        self.assertTrue(self.lowongan1.is_lowongan_masih_berlaku, True)

    def test_judul_lowongan1_and_lowongan2_is_not_equal(self):
        self.assertNotEqual(self.lowongan1.judul, self.lowongan2.judul)

    def test_kategori_lowongan1_and_lowongan2_is_not_equal(self):
        self.assertNotEqual(self.lowongan1.kategori, self.lowongan2.kategori)

    def test_kuota_peserta_lowongan1_and_lowongan2_is_not_equal(self):
        self.assertNotEqual(self.lowongan1.kuota_peserta,
                            self.lowongan2.kuota_peserta)

    def test_waktu_awal_magang_lowongan1_and_lowongan2_is_not_equal(self):
        self.assertNotEqual(self.lowongan1.waktu_awal_magang,
                            self.lowongan2.waktu_awal_magang)

    def test_waktu_akhir_magang_lowongan1_and_lowongan2_is_not_equal(self):
        self.assertNotEqual(self.lowongan1.waktu_akhir_magang,
                            self.lowongan2.waktu_akhir_magang)

    def test_batas_akhir_pendaftaran_lowongan1_and_lowongan2_is_not_equal(self):
        self.assertNotEqual(self.lowongan1.batas_akhir_pendaftaran,
                            self.lowongan2.batas_akhir_pendaftaran)

    def test_berkas_persyaratan_lowongan1_and_lowongan2_is_not_equal(self):
        self.assertNotEqual(self.lowongan1.berkas_persyaratan,
                            self.lowongan2.berkas_persyaratan)

    def test_deskripsi_lowongan1_and_lowongan2_is_not_equal(self):
        self.assertNotEqual(self.lowongan1.deskripsi,
                            self.lowongan2.deskripsi)

    def test_requirement_lowongan1_and_lowongan2_is_not_equal(self):
        self.assertNotEqual(self.lowongan1.requirement,
                            self.lowongan2.requirement)

class AppsTest(TestCase):
    def test_apps(self):
        self.assertEqual(LowonganConfig.name, 'lowongan')
        self.assertEqual(apps.get_app_config('lowongan').name, 'lowongan')
'''