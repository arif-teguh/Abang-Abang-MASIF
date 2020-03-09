import datetime
from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest
import secrets

from admin.models import OpdVerificationList
from opd import views
from account.models import Account
from lowongan.models import Lowongan
from .opd_login_form import OpdAuthenticationForm

mock_date = datetime.date(2012, 12, 12)
class LoginOpdUnitTest(TestCase):
    #login
    def test_page_title_opd_login(self):
        request = HttpRequest()
        response = views.opd_login(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>OPD Login</title>', html_response)

    def test_opd_login_template(self):
        response = self.client.get('/opd/login/')
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
        self.assertContains(response,self.lowongan1.requirement)
        self.assertContains(response,self.lowongan1.deskripsi)

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
