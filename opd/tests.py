import datetime
import secrets

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import resolve

from account.models import Account, UserProfile, OpdProfile
from admin.models import OpdVerificationList
from lowongan.models import Lowongan, UserLamarMagang
from opd import views
from .forms import EditOpdProfileForm
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
url_sort_asc = '/opd/sorting/batas-akhir/asc'
url_sort_asc2 = '/opd/sorting/waktu-magang/asc'
url_sort_desc = '/opd/sorting/batas-akhir/desc'
url_sort_desc2 = '/opd/sorting/waktu-magang/desc'
url_search = '/opd/searching/end'
class LoginOpdUnitTest(TestCase):
    # login
    def test_page_title_opd_login(self):
        request = HttpRequest()
        response = views.opd_login(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>OPD Login</title>', html_response)

    def test_opd_login_template(self):
        response = self.client.get(url_opd_login)
        self.assertTemplateUsed(response, 'opd_login.html')

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
        response = Client().get(url_opd_pelamar + '1')
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_opd_mendownload(self):
        response = Client().get(url_download_file + '1-1')
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_opd_page_list_pelamar(self):
        response = Client().get(url_download_cv + '1-1')
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
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
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
        self.assertTemplateUsed(response, 'opd_lowongan.html')

    def test_using_opd_lowongan_func(self):
        found = resolve(url_opd_index)
        self.assertEqual(found.func, views.opd_home)

    def test_response(self):
        response = self.client.get(url_opd_index)
        self.assertEqual(response.status_code, 200)

    def test_get_lowongan_item(self):
        response = self.client.get(url_opd_index)
        self.assertContains(response, self.lowongan1.judul)


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
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
            berkas_persyaratan=['Kartu Keluarga'],
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.account1.id
        )

    def test_opd_detail_lowongan_template(self):
        response = self.client.get(url_opd_lowongan_detail + str(self.lowongan1.id) + '/')
        self.assertTemplateUsed(response, 'opd_detail_lowongan.html')

    def test_using_opd_detail_lowongan_func(self):
        found = resolve(url_opd_lowongan_detail + str(self.lowongan1.id) + '/')
        self.assertEqual(found.func, views.opd_detail_lowongan)

    def test_click_detail_lowongan_button_exist(self):
        request = HttpRequest()
        request.user = self.account1
        response = views.opd_detail_lowongan(request, self.lowongan1.id)
        html_response = response.content.decode('utf8')
        self.assertIn('<button ', html_response)

    def test_page_title_opd_detail_lowngan_lowongan(self):
        request = HttpRequest()
        request.user = self.account1
        response = views.opd_detail_lowongan(request, self.lowongan1.id)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Detail Lowongan</title>', html_response)

    def test_get_lowongan_item(self):
        url = url_opd_lowongan_detail + str(self.lowongan1.id) + '/'
        response = self.client.get(url)
        self.assertContains(response, self.lowongan1.judul)
        self.assertContains(response, self.lowongan1.requirement)
        self.assertContains(response, self.lowongan1.deskripsi)

    def test_response(self):
        response = self.client.get(url_opd_lowongan_detail + str(self.lowongan1.id) + '/')
        self.assertEqual(response.status_code, 200)


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
            major='kosong',
            institution='kosong',
            education='kosong',
            address='kosong'
        )
        self.user2.save()
        self.opd1 = Account.objects.all()[0]
        self.opd2 = Account.objects.all()[1]
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
            opd_foreign_key_id=self.account1.id,

        )

        self.lowongan2 = Lowongan.objects.create(
            judul='judul2',
            kategori='kat2',
            kuota_peserta=10,
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
            berkas_persyaratan=['Kartu Keluarga'],
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.account2.id
        )
        self.lamaran = UserLamarMagang.objects.create(
            application_letter='test lamaran application',
            lowongan_foreign_key=self.lowongan1,
            user_foreign_key=self.account3,
        )
        self.lamaran.save()

    def test_opd_pendaftar_lowongan_template(self):
        response = self.client.get(url_opd_pelamar + str(self.lowongan1.id) + '/')
        self.assertTemplateUsed(response, 'opd_list_pendaftar.html')

    def test_using_opd_pendaftar_lowongan_func(self):
        found = resolve(url_opd_pelamar + str(self.lowongan1.id) + '/')
        self.assertEqual(found.func, views.opd_list_pendaftar)

    def test_response_jika_sudah_login_dan__list_pendaftar_yang_miliknya(self):
        response = self.client.get(url_opd_pelamar + str(self.lowongan1.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_response_jika_belum_login(self):
        response = Client().get(url_opd_pelamar + str(self.lowongan1.id) + '/')
        self.assertNotEqual(response.status_code, 200)

    def test_response_jika_melihat_list_pendaftar_yang_tidak_miliknya(self):
        response = self.client.get(url_opd_pelamar + str(self.lowongan2.id) + '/')
        self.assertNotEqual(response.status_code, 200)

    def test_html_render_jumlah_pelmar_dan_pendaftar(self):
        url = url_opd_pelamar + str(self.lowongan1.id) + '/'
        response = self.client.get(url)
        self.assertContains(response, self.lowongan1.judul)
        self.assertContains(response, '1')

    def test_page_title_opd_detail_lowngan_lowongan(self):
        request = HttpRequest()
        request.user = self.account1
        response = views.opd_list_pendaftar(request, self.lowongan1.id)
        html_response = response.content.decode('utf8')
        self.assertIn(self.user1.user.name, html_response)

    def test_melihat_application_letter_pelamar(self):
        url = url_opd_pelamar + str(self.lowongan1.id) + '/'
        response = self.client.get(url)
        self.assertContains(response, self.lamaran.application_letter)

    def test_melihat_detail_profil_pelamar(self):
        url = url_opd_pelamar + str(self.lowongan1.id) + '/'
        response = self.client.get(url)
        self.assertContains(response, self.account3.userprofile.major)
        self.assertContains(response, self.account3.email)
        self.assertContains(response, self.account3.phone)
        self.assertContains(response, self.account3.userprofile.institution)
        self.assertContains(response, self.account3.userprofile.education)
        self.assertContains(response, self.account3.userprofile.address)

    def test_melihat_tidak_ada_user_pelamar_yang_tidak_melamar(self):
        url = url_opd_pelamar + str(self.lowongan1.id) + '/'
        response = self.client.get(url)
        self.assertNotContains(response, self.account2.userprofile.major)
        self.assertNotContains(response, self.account2.email)
        self.assertNotContains(response, self.account2.phone)
        self.assertNotContains(response, self.account2.userprofile.institution)
        self.assertNotContains(response, self.account2.userprofile.education)
        self.assertNotContains(response, self.account2.userprofile.address)

    def test_approve_lamaran(self):
        response = self.client.get(url_update_lamaran +
                                   str(self.account3.id) + '-' + str(self.lowongan1.id)
                                   + '/Diterima/25 maret/')
        self.assertEqual(response.url, url_opd_pelamar + str(self.lowongan1.id) + '/')

    def test_error_jika_user_tidak_melamar(self):
        response = self.client.get(url_update_lamaran +
                                   str(self.account2.id) + '-' + str(self.lowongan1.id)
                                   + '/Diterima/25 maret/')
        self.assertNotEqual(response.status_code, 404)


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
            major='kosong',
            institution='kosong',
            education='kosong',
            address='kosong'
        )
        self.user2.save()
        self.opd1 = Account.objects.all()[0]
        self.opd2 = Account.objects.all()[1]
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
            opd_foreign_key_id=self.account1.id,
        )

        self.lowongan2 = Lowongan.objects.create(
            judul='judul2',
            kategori='kat2',
            kuota_peserta=10,
            waktu_awal_magang=mock_date,
            waktu_akhir_magang=mock_date,
            batas_akhir_pendaftaran=mock_date,
            berkas_persyaratan=['Kartu Keluarga'],
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=self.account2.id
        )
        self.lamaran = UserLamarMagang.objects.create(
            application_letter='test lamaran application',
            lowongan_foreign_key=self.lowongan1,
            user_foreign_key=self.account3,
            file_berkas_tambahan=SimpleUploadedFile("file.pdf", b"file_content")
        )
        self.lamaran.save()
        self.lamaran2 = UserLamarMagang.objects.create(
            application_letter='test lamaran application2',
            lowongan_foreign_key=self.lowongan2,
            user_foreign_key=self.account3,
        )
        self.lamaran2.save()
        self.lamaran3 = UserLamarMagang.objects.create(
            application_letter='test lamaran application2',
            lowongan_foreign_key=self.lowongan1,
            user_foreign_key=self.account4,
        )
        self.lamaran3.save()

    def test_download_file_sukses(self):
        response = self.client.get(url_download_file + str(self.account3.id) + '-' + str(self.lowongan1.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_download_file_gagal(self):
        response = self.client.get(url_download_file + str(self.account2.id) + '-' + str(self.lowongan1.id) + '/')
        self.assertNotEqual(response.status_code, 200)

    def test_download_cv_sukses(self):
        response = self.client.get(url_download_cv + str(self.account3.id) + '-' + str(self.lowongan1.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_download_cv_gagal(self):
        response = self.client.get(url_download_cv + str(self.account2.id) + '-' + str(self.lowongan1.id) + '/')
        self.assertNotEqual(response.status_code, 200)

    def test_redirect_download_cv_yang_bukan_miliknya(self):
        response = self.client.get(url_download_cv + str(self.account3.id) + '-' + str(self.lowongan2.id) + '/')
        self.assertNotEqual(response.status_code, 200)

    def test_download_file_yang_bukan_miliknya(self):
        response = self.client.get(url_download_file + str(self.account3.id) + '-' + str(self.lowongan2.id) + '/')
        self.assertNotEqual(response.status_code, 200)

    def test_downloading_file_name(self):
        response = self.client.get(url_download_file + str(self.account3.id) + '-' + str(self.lowongan1.id) + '/')
        filename = self.lamaran.file_berkas_tambahan.name.split('/')[-1]
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename=%s' % filename)

    def test_downloading_cv_file_name(self):
        response = self.client.get(url_download_cv + str(self.account3.id) + '-' + str(self.lowongan1.id) + '/')
        filename = self.account3.userprofile.cv.name.split('/')[-1]
        self.assertEquals(response.get('Content-Disposition'), 'attachment; filename=%s' % filename)

    def test_jika_file_tidak_ada(self):
        response = self.client.get(url_download_file + str(self.account4.id) + '-' + str(self.lowongan1.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_jika_cv_kosong(self):
        response = self.client.get(url_download_cv + str(self.account4.id) + '-' + str(self.lowongan1.id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_opd_tutup_lowongan(self):
        response = self.client.get(url_opd_tutup_buka_lowongan + str(self.lowongan1.id) + '/')
        self.assertNotEqual(response.status_code, 404)

    def test_fake_opd_tutup_lowongan(self):
        response = self.client.get(url_opd_tutup_buka_lowongan + str(self.lowongan1.id) + '/')
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(url_opd_index, response.url)

    def test_opd_tutup_lowongan_palsu(self):
        response = self.client.get(url_opd_tutup_buka_lowongan + '100/')
        self.assertNotEqual(response.status_code, 404)

    def test_approve_lamaran_yang_bukan_miliknya(self):
        response = self.client.get(url_update_lamaran +
                                   str(self.account3.id) + '-' + str(self.lowongan2.id)
                                   + '/Diterima/25 maret/')
        self.assertEqual(response.url, url_opd_index)

    def test_opd_akses_detail_lowongan_bukan_miliknya(self):
        response = self.client.get(url_opd_lowongan_detail + str(self.lowongan2.id) + '/')
        self.assertNotEqual(url_opd_lowongan_detail + str(self.lowongan2.id) + '/', response.url)
        self.assertEqual('/', response.url)

    def test_tutup_lowongan_yang_bukan_miliknya(self):
        response = self.client.get(url_opd_tutup_buka_lowongan + str(self.lowongan2.id)+'/')
        self.assertEqual('/' , response.url)


class OpdEditProfileTest(TestCase):
    def setUp(self):
        self.opd_coba_email = "opd@coba.com"
        self.opd2_coba_email = "opd2@coba.com"
        self.admin_coba_email = "admin@coba.com"
        self.opd_satu = Account.objects.create_user(self.opd_coba_email, '1234')
        self.opd_dua = Account.objects.create_user(self.opd2_coba_email, '1233')
        self.admin_satu = Account.objects.create_user(self.admin_coba_email, '1233')
        self.opd_satu.is_opd = True
        self.opd_satu.is_admin = False
        self.opd_satu.is_user = False
        self.admin_satu.is_opd = False
        self.admin_satu.is_admin = True
        self.admin_satu.is_user = False
        self.opd_dua.is_opd = True
        self.opd_dua.is_admin = False
        self.opd_dua.is_user = False
        self.opd_satu.opdprofile = OpdProfile()
        self.opd_dua.opdprofile = OpdProfile()
        self.opd_satu.save()
        self.opd_dua.save()
        self.opd_satu.opdprofile.save()
        self.opd_dua.opdprofile.save()
        self.admin_satu.save()
        self.client_login_opd = Client()
        self.client_login_admin = Client()
        self.client_login_opd.login(username=self.opd_coba_email, password='1234')
        self.client_login_admin.login(username=self.admin_coba_email, password='1233')
        self.edit_profile_page_url = '/opd/editprofile/'
        self.test_file_foto = SimpleUploadedFile("foto.jpg", b"file_content")
        self.test_address = 'test'
        self.phone = '12345'
        self.DEFAULT_NAME = "TESTNAME"

    def tearDown(self):
        pass

    def test_opd_can_access_its_own_edit_profile_page(self):
        response = self.client_login_opd.get(self.edit_profile_page_url + '{}/'.format(self.opd_satu.pk))
        self.assertTrue(response.context['permitted'])

    def test_opd_shouldnt_be_able_to_access_other_opd_edit_profile_page(self):
        response = self.client_login_opd.get(self.edit_profile_page_url + '{}/'.format(self.opd_dua.pk))
        self.assertFalse(response.context['permitted'])

    def test_edit_profile_page_should_always_return_correct_status_code(self):
        response1 = self.client.get(self.edit_profile_page_url + '999/')
        response2 = self.client.get(self.edit_profile_page_url + '998/post/')
        response3 = self.client.get(self.edit_profile_page_url + '997/post/upload_profile_picture/')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)

    def test_admin_should_be_able_to_edit_all_opd(self):
        response1 = self.client_login_admin.get(self.edit_profile_page_url + '{}/'.format(self.opd_satu.pk))
        response2 = self.client_login_admin.get(self.edit_profile_page_url + '{}/'.format(self.opd_dua.pk))
        self.assertTrue(response1.context['permitted'])
        self.assertTrue(response2.context['permitted'])

    def test_edit_profile_page_setup_correctly(self):
        response = self.client_login_admin.get(self.edit_profile_page_url + '{}/'.format(self.opd_satu.pk))
        form = response.context['form']
        self.assertTrue(
            isinstance(form, EditOpdProfileForm), type(form).__mro__)

    def test_opd_upload_profile_picture_with_mock_jpg_should_work(self):
        response = self.client_login_opd.post(
            self.edit_profile_page_url + '{}/post/upload_profile_picture/'.format(self.opd_satu.pk),
            {'profile_picture': self.test_file_foto}
        )

        self.assertEqual(response.status_code, 302)
        account = Account.objects.get(pk=self.opd_satu.pk)
        self.assertEqual(account.profile_picture.name, 'foto.jpg')
        account.profile_picture.delete()

    def test_opd_upload_shouldnt_be_able_to_upload_to_other_opd(self):
        response = self.client_login_opd.post(
            self.edit_profile_page_url + '{}/post/upload_profile_picture/'.format(self.opd_dua.pk),
            {'profile_picture': self.test_file_foto}
        )

        self.assertEqual(response.status_code, 200)
        account1 = Account.objects.get(pk=self.opd_satu.pk)
        account2 = Account.objects.get(pk=self.opd_dua.pk)
        self.assertEqual(account1.profile_picture.name, '')
        self.assertEqual(account2.profile_picture.name, '')

    def test_opd_should_be_able_to_edit_profile(self):
        response = self.client_login_opd.post(
            self.edit_profile_page_url + '{}/post/'.format(self.opd_satu.pk),
            {'phone': self.phone, 'address': self.test_address, 'name': self.DEFAULT_NAME}
        )

        account = Account.objects.get(pk=self.opd_satu.pk)
        self.assertEqual(account.opdprofile.address, 'test')
        self.assertEqual(account.phone, '12345')

    def test_opd_shouldnot_be_able_to_edit_other_opd_profile(self):
        response = self.client_login_opd.post(
            self.edit_profile_page_url + '{}/post/'.format(self.opd_dua.pk),
            {'phone': self.phone, 'address': self.test_address, 'name': self.DEFAULT_NAME}
        )

        account = Account.objects.get(pk=self.opd_dua.pk)
        self.assertNotEqual(account.opdprofile.address, self.test_address)
        self.assertNotEqual(account.phone, self.phone)
        self.assertNotEqual(account.name, self.DEFAULT_NAME)

    def test_admin_should_be_able_to_edit_any_opd(self):
        self.client_login_admin.post(
            self.edit_profile_page_url + '{}/post/'.format(self.opd_satu.pk),
            {'phone': self.phone, 'address': self.test_address, 'name': self.DEFAULT_NAME}
        )

        self.client_login_admin.post(
            self.edit_profile_page_url + '{}/post/'.format(self.opd_dua.pk),
            {'phone': self.phone, 'address': self.test_address, 'name': self.DEFAULT_NAME}
        )

        account1 = Account.objects.get(pk=self.opd_dua.pk)
        account2 = Account.objects.get(pk=self.opd_dua.pk)
        self.assertEqual(account1.opdprofile.address, self.test_address)
        self.assertEqual(account1.phone, self.phone)
        self.assertEqual(account1.name, self.DEFAULT_NAME)
        self.assertEqual(account2.opdprofile.address, self.test_address)
        self.assertEqual(account2.phone, self.phone)
        self.assertEqual(account2.name, self.DEFAULT_NAME)
        



class test_sort_by_deadline(TestCase):

    def test_sorting_asc_page_response_status(self):
        response = Client().get(url_sort_asc)
        self.assertEqual(response.status_code, 200)

    def test_sorting_desc_page_response_status(self):
        response = Client().get(url_sort_desc)
        self.assertEqual(response.status_code, 200)

    def test_sorting_other_param_response_status(self):
        response = Client().get('/opd/sorting/batas-akhir/dtogijt')
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)

    def test_sorting_page_response_status_post(self):
        response1 = Client().post(url_sort_asc)
        response2 = Client().post(url_sort_desc)
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)

class test_sort_by_waktu_magang(TestCase):

    def test_sorting_asc_page_response_status(self):
        response = Client().get(url_sort_asc2)
        self.assertEqual(response.status_code, 200)

    def test_sorting_desc_page_response_status(self):
        response = Client().get(url_sort_desc2)
        self.assertEqual(response.status_code, 200)

    def test_sorting_other_param_response_status(self):
        response = Client().get('/opd/sorting/waktu-magang/dtogijt')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.status_code, 200)

    def test_sorting_page_response_status_post(self):
        response1 = Client().post(url_sort_asc2)
        response2 = Client().post(url_sort_desc2)
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)

class test_search(TestCase):

    def test_search_page_response_status(self):
        response = Client().get(url_search)
        self.assertEqual(response.status_code, 200)

    def test_search_page_response_status_post(self):
        response = Client().post(url_search)
        self.assertEqual(response.status_code, 302)
