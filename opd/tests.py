from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest
import secrets

from admin.models import OpdVerificationList
from opd import views
from account.models import Account
from lowongan.models import Lowongan
from .opd_login_form import OpdAuthenticationForm

url_opd_login = '/opd/login/'
url_opd_index = '/opd/'
url_opd_lowongan_detail = '/opd/lowongan/detail'
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
        response = Client().get('/opd/login/')
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertTrue(isinstance(form, OpdAuthenticationForm), type(form).__mro__)

    def test_displays_opd_login_form(self):
        response = Client().get('/opd/login/')
        self.assertIsInstance(response.context["form"], OpdAuthenticationForm)

    def test_opd_page_not_authenticated(self):
        response = Client().get('/opd/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/opd/login/', response.url)

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
        response = views.opd_lowongan(request=request)
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
        response = views.opd_lowongan(request=request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/opd/login/', response.url)

    def test_user_access_opd_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = False
        request.user.is_opd = False
        request.user.is_user = True
        request.user.is_superuser = False
        response = views.opd_lowongan(request=request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/opd/login/', response.url)
    
    def test_user_access_opd_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = False
        request.user.is_opd = False
        request.user.is_user = True
        request.user.is_superuser = False
        response = views.opd_lowongan(request=request)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual('/opd/lowongan/detail-3/', response.url)

    def test_using_opd_lowongan_func(self):
        found = resolve('/opd/')
        self.assertEqual(found.func, views.opd_lowongan)


class LowonganOpdUnitTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.opd1 = Account.objects.all()[0]
        '''
        opd_profile = OpdProfile(user=self.opd1,
                                 unique_opd_attribute="opd")
        opd_profile.save()
        '''
        self.account1.is_opd = True
        self.account1.save()
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

    def test_click_lowongan_button_exist(self):
        request = HttpRequest()
        request.user = self.account1
        response = views.opd_lowongan(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button ', html_response)

    def test_page_title_opd_lowongan(self):
        request = HttpRequest()
        request.user = self.account1
        response = views.opd_lowongan(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>OPD Dashboard</title>', html_response)

    
    def test_opd_lowongan_template(self):
        response = self.client.get('/opd/')
        self.assertTemplateUsed(response,'opd_lowongan.html')

    def test_using_opd_lowongan_func(self):
        found = resolve('/opd/')
        self.assertEqual(found.func, views.opd_lowongan)

    def test_response(self):
        response = self.client.get('/opd/')
        self.assertEqual(response.status_code,200)


    def test_get_lowongan_item(self):
         response = self.client.get('/opd/')
         self.assertContains(response,self.lowongan1.judul)
         self.assertContains(response,self.lowongan1.penyedia)
            


class DetailLowonganOpdUnitTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.opd1 = Account.objects.all()[0]
        '''
        opd_profile = OpdProfile(user=self.opd1,
                                 unique_opd_attribute="opd")
        opd_profile.save()
        '''
        self.account1.is_opd = True
        self.account1.save()
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



    def test_opd_detail_lowongan_template(self):
        response = self.client.get('/opd/lowongan/detail-' + str(self.lowongan1.id)+'/')
        self.assertTemplateUsed(response,'opd_detail_lowongan.html')

    def test_using_opd_detail_lowongan_func(self):
        found = resolve('/opd/lowongan/detail-' + str(self.lowongan1.id) +'/')
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
        url = '/opd/lowongan/detail-' + str(self.lowongan1.id)+'/'
        response = self.client.get(url)
        self.assertContains(response,self.lowongan1.judul)
        self.assertContains(response,self.lowongan1.penyedia)
        self.assertContains(response,self.lowongan1.requirement)
        self.assertContains(response,self.lowongan1.deskripsi)
        self.assertContains(response,self.lowongan1.durasi_magang)

    def test_response(self):
        response = self.client.get('/opd/lowongan/detail-' + str(self.lowongan1.id)+'/')
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
        self.opd1 = Account.objects.all()[0]
        self.account1.is_opd = True
        self.account1.save()
        self.account2 = Account.objects.create_superuser(email="test2@mail.com", password="1234")
        self.opd2 = Account.objects.all()[1]
        '''
        opd_profile = OpdProfile(user=self.opd1,
                                 unique_opd_attribute="opd")
        opd_profile.save()
        '''
        
        self.account2.is_opd = True
        self.account2.save()
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
        self.lowongan2 = Lowongan.objects.create(
            judul = 'judul1',
            penyedia = 'opd1',
            jumlah_tersedia = 10,
            durasi_magang = 10,
            jangka_waktu_lamaran = 10,
            berkas = 'berkas1',
            deskripsi = 'deskripsi1',
            requirement = 'requirement1',
            opd_foreign_key_id = self.opd2.id
        )


    def test_opd_pendaftar_lowongan_template(self):
        response = self.client.get('/opd/lowongan/list-pendaftar-' + str(self.lowongan1.id)+'/')
        self.assertTemplateUsed(response,'opd_list_pendaftar.html')

    def test_using_opd_pendaftar_lowongan_func(self):
        found = resolve('/opd/lowongan/list-pendaftar-' + str(self.lowongan1.id) +'/')
        self.assertEqual(found.func, views.opd_list_pendaftar)

    
    def test_response_jika_sudah_login_dan__list_pendaftar_yang_miliknya(self):
        response = self.client.get('/opd/lowongan/list-pendaftar-' + str(self.lowongan1.id) +'/')
        self.assertEqual(response.status_code,200)

    def test_response_jika_belum_login(self):
        response = Client().get('/opd/lowongan/list-pendaftar-' + str(self.lowongan1.id) +'/')
        self.assertNotEqual(response.status_code,200)
    

    def test_response_jika_melihat_list_pendaftar_yang_tidak_miliknya(self):
        response = self.client.get('/opd/lowongan/list-pendaftar-' + str(self.lowongan2.id) +'/')
        self.assertNotEqual(response.status_code,200)
 

    def test_isi_response(self):
        response = self.client.get('/opd/lowongan/list-pendaftar-' + str(self.lowongan2.id) +'/')
        self.assertEqual(response.content, self.lowongan1)