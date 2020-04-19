import datetime
from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest
import secrets
from django.core.files.uploadedfile import SimpleUploadedFile
from admin.models import OpdVerificationList
from opd import views
from account.models import Account , UserProfile
from lowongan.models import Lowongan , UserLamarMagang
from .opd_login_form import OpdAuthenticationForm
home = '/'
url_opd_login = '/opd/login/'
url_opd_index = '/opd/'
url_opd_lowongan_detail = '/opd/lowongan/detail-'
url_opd_pelamar = '/opd/lowongan/list-pendaftar-'
url_download_file = '/opd/lowongan/file_tambahan-'
url_download_cv = '/opd/lowongan/cv_pendaftar-'
url_update_lamaran = '/opd/proses-'
test_email_addr = 'test@mail.com'
kartu_keluarga = 'Kartu Keluarga'
url_opd_tutup_buka_lowongan = '/opd/lowongan/buka-tutup/'
mock_date = datetime.date(2012, 12, 12)

class LoginOpdUnitTest(TestCase):
    #login
    def test_page_title_opd_login(self):
        request = HttpRequest()
        response = views.opd_login(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>OPD Login</title>', html_response)

    def test_opd_login_template(self):
        response = self.client.get(url_opd_login)
        self.assertTemplateUsed(response,'opd_login.html')
        

    def test_submit_button_exist(self):
        request = HttpRequest()
        response = views.opd_login(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button type="submit"', html_response)


    def test_opd_login_page_is_set_up_as_expected(self):
        response = Client().get(url_opd_login)
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertTrue(isinstance(form, OpdAuthenticationForm), type(form).__mro__)

    def test_displays_opd_login_form(self):
        response = Client().get(url_opd_login)
        self.assertIsInstance(response.context["form"], OpdAuthenticationForm)

    def test_opd_page_not_authenticated(self):
        response = Client().get(url_opd_index)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(home, response.url)

class RedirectJikaBelumLogin(TestCase):
    def test_redirect_detail_lowongan(self):
        response = Client().get(url_opd_lowongan_detail + '1')
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_opd_page_list_pelamar(self):
        response = Client().get(url_opd_pelamar +'1')
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_opd_mendownload(self):
        response = Client().get(url_download_file +'1-1')
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_opd_page_list_pelamar(self):
        response = Client().get(url_download_cv +'1-1')
        self.assertNotEqual(response.status_code, 200)

class OpdRedirectUnitTest(TestCase):
    def test_opd_access_opd_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = False
        request.user.is_opd = True
        request.user.is_user = False
        request.user.is_superuser = False
        response = views.opd_home(request=request)
        self.assertEqual(response.status_code, 200)

    def test_admin_access_opd_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = True
        request.user.is_opd = False
        request.user.is_user = False
        request.user.is_superuser = False
        response = views.opd_home(request=request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/', response.url)

    def test_user_access_opd_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = False
        request.user.is_opd = False
        request.user.is_user = True
        request.user.is_superuser = False
        response = views.opd_home(request=request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/', response.url)
    
    def test_user_access_opd_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = False
        request.user.is_opd = False
        request.user.is_user = True
        request.user.is_superuser = False
        response = views.opd_home(request=request)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual('/opd/lowongan/detail-3/', response.url)

    def test_using_opd_lowongan_func(self):
        found = resolve('/opd/')
        self.assertEqual(found.func, views.opd_home)


class LowonganOpdUnitTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.opd1 = Account.objects.all()[0]
   
         
        self.account1.is_opd = True
        self.account1.save()
        self.client.force_login(self.account1)
        self.lowongan1 = Lowongan.objects.create(
            judul='judul1',
            kategori='kat1',
            kuota_peserta=10,
            waktu_awal_magang = mock_date,
            waktu_akhir_magang = mock_date,
            batas_akhir_pendaftaran = mock_date,
            berkas_persyaratan=['Kartu Keluarga'],
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.account1.id
        )

    def test_click_lowongan_button_exist(self):
        request = HttpRequest()
        request.user = self.account1
        response = views.opd_home(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button ', html_response)

    def test_page_title_opd_lowongan(self):
        request = HttpRequest()
        request.user = self.account1
        response = views.opd_home(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>OPD Dashboard</title>', html_response)

    
    def test_opd_lowongan_template(self):
        response = self.client.get(url_opd_index)
        self.assertTemplateUsed(response,'opd_lowongan.html')

    def test_using_opd_lowongan_func(self):
        found = resolve(url_opd_index)
        self.assertEqual(found.func, views.opd_home)

    def test_response(self):
        response = self.client.get(url_opd_index)
        self.assertEqual(response.status_code,200)


    def test_get_lowongan_item(self):
         response = self.client.get(url_opd_index)
         self.assertContains(response,self.lowongan1.judul)
            


class DetailLowonganOpdUnitTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.opd1 = Account.objects.all()[0]
        
        self.account1.is_opd = True
        self.account1.save()
        self.client.force_login(self.account1)
        self.lowongan1 = Lowongan.objects.create(
            judul='judul1',
            kategori='kat1',
            kuota_peserta=10,
            waktu_awal_magang = mock_date,
            waktu_akhir_magang = mock_date,
            batas_akhir_pendaftaran = mock_date,
            berkas_persyaratan=['Kartu Keluarga'],
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.account1.id
        )


    
    def test_opd_detail_lowongan_template(self):
        response = self.client.get(url_opd_lowongan_detail + str(self.lowongan1.id)+'/')
        self.assertTemplateUsed(response,'opd_detail_lowongan.html')

    def test_using_opd_detail_lowongan_func(self):
        found = resolve(url_opd_lowongan_detail + str(self.lowongan1.id) +'/')
        self.assertEqual(found.func, views.opd_detail_lowongan)

    def test_click_detail_lowongan_button_exist(self):
        request = HttpRequest()
        request.user = self.account1
        response = views.opd_detail_lowongan(request,self.lowongan1.id)
        html_response = response.content.decode('utf8')
        self.assertIn('<button ', html_response)

    def test_page_title_opd_detail_lowngan_lowongan(self):
        request = HttpRequest()
        request.user = self.account1
        response = views.opd_detail_lowongan(request, self.lowongan1.id)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Detail Lowongan</title>', html_response)
    
    def test_get_lowongan_item(self):
        url = url_opd_lowongan_detail + str(self.lowongan1.id)+'/'
        response = self.client.get(url)
        self.assertContains(response,self.lowongan1.judul)
        self.assertContains(response,self.lowongan1.requirement)
        self.assertContains(response,self.lowongan1.deskripsi)

    def test_response(self):
        response = self.client.get(url_opd_lowongan_detail+ str(self.lowongan1.id)+'/')
        self.assertEqual(response.status_code,200)


class OpdConfirmationTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.request = HttpRequest()
        self.secret = secrets.token_urlsafe(16)
        opd_verif = OpdVerificationList(secret=self.secret,
             name="AbangAbang",
             email="abang@abang.com", 
             phone="081312213")
        opd_verif.save()

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_verification_without_token_redirect(self):
        response = self.client.get('/opd/verification/')
        self.assertEqual('/', response.url)


class TestCekListPelamar(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.account1.is_opd = True
        self.account1.save()
        self.account2 = Account.objects.create_superuser(email="test2@mail.com", password="xyz")
        self.account2.is_opd = True
        self.account2.save()
        self.account3 = Account.objects.create_user(email="user3@mail.com", password="dqwqfas")
        self.account3.name = "testtest"
        self.account3.is_user = True
        self.account3.save()
        self.user1 = UserProfile(user=self.account3)
        self.user1.save()
        self.user2 = UserProfile(
            user=self.account2,
            major = 'kosong',
            institution = 'kosong',
            education = 'kosong',
            address = 'kosong'
            )
        self.user2.save()
        self.opd1 = Account.objects.all()[0]
        self.opd2 = Account.objects.all()[1]
        self.client.force_login(self.account1)
        self.lowongan1 = Lowongan.objects.create(
            judul='judul1',
            kategori='kat1',
            kuota_peserta=10,
            waktu_awal_magang = mock_date,
            waktu_akhir_magang = mock_date,
            batas_akhir_pendaftaran = mock_date,
            berkas_persyaratan=['Kartu Keluarga'],
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.account1.id,
            
            
        )

        self.lowongan2 = Lowongan.objects.create(
            judul='judul2',
            kategori='kat2',
            kuota_peserta=10,
            waktu_awal_magang = mock_date,
            waktu_akhir_magang = mock_date,
            batas_akhir_pendaftaran = mock_date,
            berkas_persyaratan=['Kartu Keluarga'],
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id = self.account2.id
        )
        self.lamaran = UserLamarMagang.objects.create(
            application_letter = 'test lamaran application',
            lowongan_foreign_key = self.lowongan1,
            user_foreign_key = self.account3,
        )
        self.lamaran.save()

    
    def test_opd_pendaftar_lowongan_template(self):
        response = self.client.get(url_opd_pelamar + str(self.lowongan1.id)+'/')
        self.assertTemplateUsed(response,'opd_list_pendaftar.html')

    def test_using_opd_pendaftar_lowongan_func(self):
        found = resolve(url_opd_pelamar + str(self.lowongan1.id) +'/')
        self.assertEqual(found.func, views.opd_list_pendaftar)

    
    def test_response_jika_sudah_login_dan__list_pendaftar_yang_miliknya(self):
        response = self.client.get(url_opd_pelamar + str(self.lowongan1.id) +'/')
        self.assertEqual(response.status_code,200)

    def test_response_jika_belum_login(self):
        response = Client().get(url_opd_pelamar + str(self.lowongan1.id) +'/')
        self.assertNotEqual(response.status_code,200)
    

    def test_response_jika_melihat_list_pendaftar_yang_tidak_miliknya(self):
        response = self.client.get(url_opd_pelamar + str(self.lowongan2.id) +'/')
        self.assertNotEqual(response.status_code,200)
 

    def test_html_render_jumlah_pelmar_dan_pendaftar(self):
        url = url_opd_pelamar + str(self.lowongan1.id)+'/'
        response = self.client.get(url)
        self.assertContains(response,self.lowongan1.judul)
        self.assertContains(response,'1')


    
    def test_page_title_opd_detail_lowngan_lowongan(self):
        request = HttpRequest()
        request.user = self.account1
        response = views.opd_list_pendaftar(request, self.lowongan1.id)
        html_response = response.content.decode('utf8')
        self.assertIn(self.user1.user.name, html_response)

    def test_melihat_application_letter_pelamar(self):
        url = url_opd_pelamar + str(self.lowongan1.id)+'/'
        response = self.client.get(url)
        self.assertContains(response,self.lamaran.application_letter)

    def test_melihat_detail_profil_pelamar(self):
        url = url_opd_pelamar + str(self.lowongan1.id)+'/'
        response = self.client.get(url)
        self.assertContains(response,self.account3.userprofile.major)
        self.assertContains(response,self.account3.email)
        self.assertContains(response,self.account3.phone)
        self.assertContains(response,self.account3.userprofile.institution)
        self.assertContains(response,self.account3.userprofile.education)
        self.assertContains(response,self.account3.userprofile.address)

    
    def test_melihat_tidak_ada_user_pelamar_yang_tidak_melamar(self):
        url = url_opd_pelamar + str(self.lowongan1.id)+'/'
        response = self.client.get(url)
        self.assertNotContains(response,self.account2.userprofile.major)
        self.assertNotContains(response,self.account2.email)
        self.assertNotContains(response,self.account2.phone)
        self.assertNotContains(response,self.account2.userprofile.institution)
        self.assertNotContains(response,self.account2.userprofile.education)
        self.assertNotContains(response,self.account2.userprofile.address)

    def test_approve_lamaran(self):
        response = self.client.get(url_update_lamaran  +
        str(self.account3.id)+'-'+str(self.lowongan1.id)
        +'/Diterima/25 maret/')
        self.assertEqual(response.url , url_opd_pelamar+str(self.lowongan1.id)+'/')

    def test_error_jika_user_tidak_melamar(self):
        response = self.client.get(url_update_lamaran  +
        str(self.account2.id)+'-'+str(self.lowongan1.id)
        +'/Diterima/25 maret/')
        self.assertNotEqual(response.status_code,404)


class TestOpdDownload(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.account1.is_opd = True
        self.account1.save()
        self.account2 = Account.objects.create_superuser(email="test2@mail.com", password="xyz")
        self.account2.is_opd = True
        self.account2.save()
        self.account3 = Account.objects.create_user(email="user3@mail.com", password="dqwqfas")
        self.account3.name = "testtest"
        self.account3.is_user = True
        self.account3.save()
        self.account4 = Account.objects.create_user(email="user4@mail.com", password="fadfads")
        self.account4.name = "fsafas"
        self.account4.is_user = True
        self.account4.save()
        self.user1 = UserProfile(user=self.account3)
        self.user1.cv = SimpleUploadedFile("file.pdf", b"file_content")
        self.user1.save()
        self.user2 = UserProfile(
            user=self.account4,
            major = 'kosong',
            institution = 'kosong',
            education = 'kosong',
            address = 'kosong'
            )
        self.user2.save()
        self.opd1 = Account.objects.all()[0]
        self.opd2 = Account.objects.all()[1]
        self.client.force_login(self.account1)
        self.lowongan1 = Lowongan.objects.create(
            judul='judul1',
            kategori='kat1',
            kuota_peserta=10,
            waktu_awal_magang = mock_date,
            waktu_akhir_magang = mock_date,
            batas_akhir_pendaftaran = mock_date,
            berkas_persyaratan=['Kartu Keluarga'],
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.account1.id,
        )

        self.lowongan2 = Lowongan.objects.create(
            judul='judul2',
            kategori='kat2',
            kuota_peserta=10,
            waktu_awal_magang = mock_date,
            waktu_akhir_magang = mock_date,
            batas_akhir_pendaftaran = mock_date,
            berkas_persyaratan=['Kartu Keluarga'],
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id = self.account2.id
        )
        self.lamaran = UserLamarMagang.objects.create(
            application_letter = 'test lamaran application',
            lowongan_foreign_key = self.lowongan1,
            user_foreign_key = self.account3,
            file_berkas_tambahan = SimpleUploadedFile("file.pdf", b"file_content")
        )
        self.lamaran.save()
        self.lamaran2 = UserLamarMagang.objects.create(
            application_letter = 'test lamaran application2',
            lowongan_foreign_key = self.lowongan2,
            user_foreign_key = self.account3,
        )
        self.lamaran2.save()
        self.lamaran3 = UserLamarMagang.objects.create(
            application_letter = 'test lamaran application2',
            lowongan_foreign_key = self.lowongan1,
            user_foreign_key = self.account4,
        )
        self.lamaran3.save()

    def test_download_file_sukses(self):
        response = self.client.get(url_download_file + str(self.account3.id)+'-'+str(self.lowongan1.id)+'/')
        self.assertEqual(response.status_code,200)

    def test_download_file_gagal(self):
        response = self.client.get(url_download_file + str(self.account2.id)+'-'+str(self.lowongan1.id)+'/')
        self.assertNotEqual(response.status_code,200)

    def test_download_cv_sukses(self):
        response = self.client.get(url_download_cv + str(self.account3.id)+'-'+str(self.lowongan1.id)+'/')
        self.assertEqual(response.status_code,200)

    def test_download_cv_gagal(self):
        response = self.client.get(url_download_cv + str(self.account2.id)+'-'+str(self.lowongan1.id)+'/')
        self.assertNotEqual(response.status_code,200)

    def test_redirect_download_cv_yang_bukan_miliknya(self):
        response = self.client.get(url_download_cv + str(self.account3.id)+'-'+str(self.lowongan2.id)+'/')
        self.assertNotEqual(response.status_code,200)


    def test_download_file_yang_bukan_miliknya(self):
        response = self.client.get(url_download_file + str(self.account3.id)+'-'+str(self.lowongan2.id)+'/')
        self.assertNotEqual(response.status_code,200)

    def test_downloading_file_name(self):
        response = self.client.get(url_download_file + str(self.account3.id)+'-'+str(self.lowongan1.id)+'/')
        filename = self.lamaran.file_berkas_tambahan.name.split('/')[-1]
        self.assertEquals(response.get('Content-Disposition'),'attachment; filename=%s' % filename )

    def test_downloading_cv_file_name(self):
        response = self.client.get(url_download_cv + str(self.account3.id)+'-'+str(self.lowongan1.id)+'/')
        filename = self.account3.userprofile.cv.name.split('/')[-1]
        self.assertEquals(response.get('Content-Disposition'),'attachment; filename=%s' % filename )

    def test_jika_file_tidak_ada(self):
        response = self.client.get(url_download_file + str(self.account4.id)+'-'+str(self.lowongan1.id)+'/')
        self.assertEqual(response.status_code,200)

    def test_jika_cv_kosong(self):
        response = self.client.get(url_download_cv + str(self.account4.id)+'-'+str(self.lowongan1.id)+'/')
        self.assertEqual(response.status_code,200)
 

    def test_opd_tutup_lowongan(self):
        response = self.client.get(url_opd_tutup_buka_lowongan + str(self.lowongan1.id)+'/')
        self.assertNotEqual(response.status_code,404)
    
    def test_fake_opd_tutup_lowongan(self):
        response = self.client.get(url_opd_tutup_buka_lowongan + str(self.lowongan1.id)+'/')
        self.assertNotEqual(response.status_code,404)
        self.assertEqual(url_opd_index , response.url)
        

    def test_opd_tutup_lowongan_palsu(self):
        response = self.client.get(url_opd_tutup_buka_lowongan + '100/')
        self.assertNotEqual(response.status_code,404)

    def test_approve_lamaran_yang_bukan_miliknya(self):
        response = self.client.get(url_update_lamaran  +
        str(self.account3.id)+'-'+str(self.lowongan2.id)
        +'/Diterima/25 maret/')
        self.assertEqual(response.url , url_opd_index)

    def test_opd_akses_detail_lowongan_bukan_miliknya(self):
        response = self.client.get(url_opd_lowongan_detail +str(self.lowongan2.id) +'/' )
        self.assertNotEqual(url_opd_lowongan_detail +str(self.lowongan2.id) +'/' , response.url)
        self.assertEqual('/' , response.url)

    def test_tutup_lowongan_yang_bukan_miliknya(self):
        response = self.client.get(url_opd_tutup_buka_lowongan + str(self.lowongan2.id)+'/')
        self.assertEqual('/' , response.url)