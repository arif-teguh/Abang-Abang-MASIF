import datetime
import json
import shutil
from django.test import TestCase, Client
from django.urls import resolve
from django.apps import apps
from account.models import Account, OpdProfile, UserProfile
from .apps import LowonganConfig
from .models import Lowongan, UserLamarMagang
from . import views
from .form import LowonganForm
from django.core.files.uploadedfile import SimpleUploadedFile

url_form_lowongan = '/lowongan/opd/form/'
url_form_lamar = "/lowongan/user/lamar/"
url_post_lowongan = url_form_lowongan + "post/"
str_kartu_keluarga = "Kartu Keluarga"
str_surat_izin_sekolah = 'Surat Izin Sekolah'
list_berkas = [str_kartu_keluarga]
mock_date = datetime.date(2012, 12, 12)
mock_date2 = datetime.date(2011, 11, 11)
encypte_multipart = "multipart/form-data"
kategori_json_dir = 'templates/lowongan/kategori.json'
edit_kategori_url = "/lowongan/admin/edit-kategori/"
url_form_edit_kategori = "/lowongan/admin/form/edit-kategori/"
templates_dir = "templates/"
template_lowongan_dir = templates_dir+"lowongan/"
template_json_dir = templates_dir+"kategori.json"

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

    def test_edit_kategori_oleh_admin(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=True)
        with open(kategori_json_dir) as kategori_json:
            backup_kategori_json = json.load(kategori_json)
        print(backup_kategori_json)

        data_form_lowongan = {
            "kategori" : ["Test"]
        }

        self.client.post(edit_kategori_url, data_form_lowongan)
        with open(kategori_json_dir) as kategori_json:
            test_kategori_json = json.load(kategori_json)
        print(test_kategori_json)

        self.assertNotEqual(backup_kategori_json, test_kategori_json)

        with open(kategori_json_dir, 'w') as kategori_json:
            json.dump(backup_kategori_json, kategori_json)

    def test_edit_kategori_not_admin(self):
        data_form_lowongan = {
            "kategori" : ["Test"]
        }
        response = self.client.post(edit_kategori_url, data_form_lowongan)
        self.assertEqual(response.status_code, 302)

    def test_redirect_when_get_edit_kategori(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=True)
        response = self.client.get(edit_kategori_url, {"Pass":"Error"})
        self.assertEqual(response.status_code, 302)

    def test_redirect_when_file_kategori_json_not_found(self):
        shutil.move(kategori_json_dir, templates_dir)
        Account.objects.filter(pk=self.user.id).update(is_admin=True)
        data_form_lowongan = {
            "kategori" : ["Test"]
        }
        response = self.client.post(edit_kategori_url, data_form_lowongan)
        self.assertEqual(response.status_code, 302)
        shutil.move(template_json_dir, template_lowongan_dir)

    def test_form_lamaran_success_made_when_file_not_found(self):
        shutil.move(kategori_json_dir, templates_dir)
        mock_form_lowongan = LowonganForm()
        self.assertIsInstance(mock_form_lowongan, LowonganForm)
        shutil.move(template_json_dir, template_lowongan_dir)

    def test_show_form_edit_lowongan_not_admin(self):
        response = self.client.get(url_form_edit_kategori)
        self.assertNotEqual(response.status_code, 200)

    def test_show_form_edit_lowongan_admin(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=True)
        response = self.client.get(url_form_edit_kategori)
        self.assertEqual(response.status_code, 200)

    def test_show_form_edit_lowongan_file_not_found(self):
        shutil.move(kategori_json_dir, templates_dir)
        Account.objects.filter(pk=self.user.id).update(is_admin=True)
        response = self.client.get(url_form_edit_kategori)
        self.assertNotEqual(response.status_code, 200)
        shutil.move(template_json_dir, template_lowongan_dir)

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

class UserLamarMagangModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.user1 = Account.objects.all()[0]
        user_profile = UserProfile(user=self.user1)
        user_profile.save()
        self.test_file_cv = SimpleUploadedFile("testcv.pdf", b"file_content")
        self.test_file_cv_2 = SimpleUploadedFile("testcv2.pdf", b"file_content")

        self.account2 = Account.objects.create_superuser(email="test2@mail.com", password="1234")
        self.opd1 = Account.objects.all()[1]
        opd_profile = OpdProfile(user=self.opd1,
                                 unique_opd_attribute="opd")
        opd_profile.save()

        self.lowongan3 = Lowongan.objects.create(
            judul='judul1',
            kategori='kat1',
            kuota_peserta=3,
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
            berkas_persyaratan=list_berkas,
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.opd1.id
        )

        self.lowongan4 = Lowongan.objects.create(
            judul='judul2',
            kategori='kat2',
            kuota_peserta=3,
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
            berkas_persyaratan=list_berkas,
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.opd1.id
        )

        self.lowongan5 = Lowongan.objects.create(
            judul='judul3',
            kategori='kat2',
            kuota_peserta=3,
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
            berkas_persyaratan=list_berkas,
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.opd1.id
        )

        self.lowongan6 = Lowongan.objects.create(
            judul='judul3',
            kategori='kat2',
            kuota_peserta=3,
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
            berkas_persyaratan=list_berkas,
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.opd1.id
        )

        self.lowongan7 = Lowongan.objects.create(
            judul='judul7',
            kategori='kat2',
            kuota_peserta=3,
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
            berkas_persyaratan=list_berkas,
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.opd1.id
        )

        self.lowongan8 = Lowongan.objects.create(
            judul='judul8',
            kategori='kat2',
            kuota_peserta=3,
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
            berkas_persyaratan=list_berkas,
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.opd1.id
        )

        self.client.force_login(self.account1)

        self.lamar1 = UserLamarMagang.objects.create(
            application_letter="test",
            lowongan_foreign_key_id=self.lowongan3.id,
            user_foreign_key_id=self.user1.id,
            status_lamaran="pending",
            notes_status_lamaran="Test"
        )
        self.lamar2 = UserLamarMagang.objects.create(
            lowongan_foreign_key_id=self.lowongan4.id,
            user_foreign_key_id=self.user1.id
        )
        self.lamar3 = UserLamarMagang.objects.create(
            application_letter="test",
            lowongan_foreign_key_id=self.lowongan8.id,
            user_foreign_key_id=self.user1.id,
            status_lamaran="wawancara",
            notes_status_lamaran="Test"
        )

    def test_object_user_lamar_magang_is_created(self):
        self.assertTrue(type(self.lamar1), UserLamarMagang)

    def test_lamar1_not_lamar2(self):
        self.assertNotEqual(str(self.lamar1.id), str(self.lamar2.id))

    def test_lamar1_user_is_lamar2_user(self):
        self.assertEqual(str(self.lamar1.user_foreign_key_id),
                         str(self.lamar2.user_foreign_key_id))

    def test_form_lamar_lowongan_url_exist(self):
        id_user = self.user1.id
        self.client.force_login(self.account1)
        Account.objects.filter(pk=id_user).update(is_user=True)
        response = self.client.get(url_form_lamar+str(self.lowongan5.id)+"/")
        self.assertEqual(response.status_code, 200)

    def test_status_lamaran_default_pending(self):
        self.assertEqual(self.lamar2.status_lamaran, "pending")
    
    def test_notes_status_lamaran_default_tidak_ada_catatan(self):
        self.assertEqual(self.lamar2.notes_status_lamaran, "Tidak Ada Catatan")
        
    def test_status_lamaran_not_default_pending(self):
        self.assertNotEqual(self.lamar3.status_lamaran, "pending")
    
    def test_notes_status_lamaran_not_default_tidak_ada_catatan(self):
        self.assertNotEqual(self.lamar1.notes_status_lamaran, "Tidak Ada Catatan")

    def test_first_post_lamaran(self):
        id_user = self.user1.id
        self.client.force_login(self.account1)
        Account.objects.filter(pk=id_user).update(is_user=True)
        data_form_lamar = {
            "application_letter":"first",
            "lowongan_foreign_key_id":self.lowongan6.id,
            "user_foreign_key_id":self.user1.id,
            "file_berkas_tambahan":self.test_file_cv
        }
        self.client.post(url_form_lamar+str(self.lowongan6.id)+"/", enctype=encypte_multipart, data=data_form_lamar)
        self.assertTrue(UserLamarMagang.objects.filter(application_letter="first").exists())

    def test_first_post_lamaran_with_cv(self):
        id_user = self.user1.id
        self.client.force_login(self.account1)
        Account.objects.filter(pk=id_user).update(is_user=True)
        data_form_lamar = {
            "file_cv":self.test_file_cv_2,
            "application_letter":"first",
            "lowongan_foreign_key_id":self.lowongan7.id,
            "user_foreign_key_id":self.user1.id,
            "file_berkas_tambahan":self.test_file_cv
        }
        self.client.post(url_form_lamar+str(self.lowongan7.id)+"/", enctype=encypte_multipart, data=data_form_lamar)
        self.assertTrue(UserLamarMagang.objects.filter(application_letter="first").exists())

    def test_post_lamar(self):
        id_user = self.user1.id
        self.client.force_login(self.account1)
        Account.objects.filter(pk=id_user).update(is_user=True)
        data_form_lamar = {
            "application_letter":"hei",
            "lowongan_foreign_key_id":self.lowongan3.id,
            "user_foreign_key_id":self.user1.id,
            "file_berkas_tambahan":self.test_file_cv
        }
        self.client.post(url_form_lamar+str(self.lowongan3.id)+"/", enctype=encypte_multipart, data=data_form_lamar)
        self.assertTrue(UserLamarMagang.objects.filter(application_letter="hei").exists())
    
    def test_update_lamar(self):
        id_user = self.user1.id
        self.client.force_login(self.account1)
        Account.objects.filter(pk=id_user).update(is_user=True)
        data_form_lamar = {
            "application_letter":"aaaa",
            "lowongan_foreign_key_id":self.lowongan3.id,
            "user_foreign_key_id":self.user1.id,
            "file_berkas_tambahan":self.test_file_cv
        }
        self.client.post(url_form_lamar+str(self.lowongan3.id)+"/", enctype=encypte_multipart, data=data_form_lamar)
        self.assertTrue(UserLamarMagang.objects.filter(application_letter="aaaa").exists())
    
    def test_update_lamar_status_wawancara(self):
        id_user = self.user1.id
        self.client.force_login(self.account1)
        Account.objects.filter(pk=id_user).update(is_user=True)
        data_form_lamar = {
            "application_letter":"wawancara",
            "lowongan_foreign_key_id":self.lowongan8.id,
            "user_foreign_key_id":self.user1.id,
            "file_berkas_tambahan":self.test_file_cv
        }
        self.client.post(url_form_lamar+str(self.lowongan8.id)+"/", enctype=encypte_multipart, data=data_form_lamar)
        self.assertFalse(UserLamarMagang.objects.filter(application_letter="wawancara").exists())

    def test_update_url_lamar(self):
        id_user = self.user1.id
        self.client.force_login(self.account1)
        Account.objects.filter(pk=id_user).update(is_user=True)
        response = self.client.get(url_form_lamar+str(self.lowongan3.id)+"/")
        self.assertTrue(response.status_code, 200)
    
    def test_post_lamar_with_cv(self):
        id_user = self.user1.id
        self.client.force_login(self.account1)
        Account.objects.filter(pk=id_user).update(is_user=True)
        data_form_lamar = {
            "file_cv":self.test_file_cv_2,
            "application_letter":"cvcv",
            "lowongan_foreign_key_id":self.lowongan4.id,
            "user_foreign_key_id":self.user1.id,
            "file_berkas_tambahan":self.test_file_cv
        }
        self.client.post(url_form_lamar+str(self.lowongan4.id)+"/", enctype=encypte_multipart, data=data_form_lamar)
        self.assertTrue(UserLamarMagang.objects.filter(application_letter="cvcv").exists())
    
    def test_redirect_post_lamar_field_missing(self):
        id_user = self.user1.id
        self.client.force_login(self.account1)
        Account.objects.filter(pk=id_user).update(is_user=True)
        data_form_lamar = {
            "application_letter":"nofiletest",
            "lowongan_foreign_key_id":self.lowongan5.id,
            "user_foreign_key_id":self.user1.id,
        }
        self.client.post(url_form_lamar+str(self.lowongan5.id)+"/", enctype=encypte_multipart, data=data_form_lamar)
        self.assertFalse(UserLamarMagang.objects.filter(application_letter="nofiletest").exists())

    def test_is_not_user_to_lamar(self):
        response = self.client.get(url_form_lamar+str(self.lowongan3.id)+"/")
        self.assertEqual(response.status_code, 302)

    def test_redirect_is_lowongan_is_none(self):
        id_user = self.user1.id
        self.client.force_login(self.account1)
        Account.objects.filter(pk=id_user).update(is_user=True)
        data_form_lamar = {
            "application_letter":"hei",
            "lowongan_foreign_key_id":self.lowongan3.id,
            "user_foreign_key_id":self.user1.id,
            "file_berkas_tambahan":self.test_file_cv
        }
        response = self.client.post(url_form_lamar+"12800/", enctype=encypte_multipart, data=data_form_lamar)
        self.assertEqual(response.status_code, 302)
