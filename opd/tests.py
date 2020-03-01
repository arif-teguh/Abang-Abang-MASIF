from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest
from . import views
from account.models import Account
from lowongan.models import Lowongan
from .opd_login_form import OpdAuthenticationForm


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
        self.assertEqual('/account-redirector', response.url)

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
        response = views.opd_index(request=request)
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
        response = views.opd_index(request=request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/account-redirector', response.url)

    def test_user_access_opd_page(self):
        request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        created_mock_user = Account.objects.all()[0]
        request.user = created_mock_user
        request.user.is_admin = False
        request.user.is_opd = False
        request.user.is_user = True
        request.user.is_superuser = False
        response = views.opd_index(request=request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/account-redirector', response.url)

    def test_using_opd_index_func(self):
        found = resolve('/opd/')
        self.assertEqual(found.func, views.opd_index)


class LowonganOpdUnitTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.opd1 = Account.objects.all()[0]
        '''
        opd_profile = OpdProfile(user=self.opd1,
                                 unique_opd_attribute="opd")
        opd_profile.save()
        '''

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
        response = views.opd_lowongan(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button ', html_response)

    def test_page_title_opd_lowongan(self):
        request = HttpRequest()
        response = views.opd_lowongan(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>lowongan</title>', html_response)

    
    def test_opd_lowongan_template(self):
        response = self.client.get('/opd/lowongan/')
        self.assertTemplateUsed(response,'opd_lowongan.html')

    def test_using_opd_index_func(self):
        found = resolve('/opd/lowongan/')
        self.assertEqual(found.func, views.opd_lowongan)

    def test_get_lowongan_item(self):
        response = self.client.get('/opd/lowongan/')
        self.assertContains(response,self.lowongan1.judul)
        self.assertContains(response,self.lowongan1.penyedia)

    def test_response(self):
        response = self.client.get('/opd/lowongan/')
        self.assertEqual(response.status_code,200)

            


class DetailLowonganOpdUnitTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create_superuser(email="test@mail.com", password="1234")
        self.opd1 = Account.objects.all()[0]
        '''
        opd_profile = OpdProfile(user=self.opd1,
                                 unique_opd_attribute="opd")
        opd_profile.save()
        '''

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
        response = views.opd_detail_lowongan(request,self.lowongan1.id)
        html_response = response.content.decode('utf8')
        self.assertIn('<button ', html_response)

    def test_page_title_opd_detail_lowngan_lowongan(self):
        request = HttpRequest()
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



    
