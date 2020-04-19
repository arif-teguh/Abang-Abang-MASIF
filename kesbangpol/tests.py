import datetime

from django.test import TestCase, Client
from django.http import HttpRequest
from django.core.exceptions import ValidationError


from account.models import Account, KesbangpolProfile, UserProfile
from lowongan.models import Lowongan, UserLamarMagang
from .kesbangpol_login_form import KesbangpolAuthenticationForm
from . import views
class KesbangpolLoginTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.request = HttpRequest()
        self.email = "a@a.com"
        self.password = "zxasqw12"
        self.user_name = "abc"
        self.phone = 1234
        self.user_test_account = Account.objects.create_user(
            email=self.email, password=self.password)
        self.user_test_account.is_kesbangpol = True
        self.user_test_account.save()

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_page_title_login_kesbangpol_page(self):
        response = views.kesbangpol_login(self.request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Kesbangpol Login</title>', html_response)

    def test_submit_button_exist(self):
        response = views.kesbangpol_login(self.request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button type="submit"', html_response)

    def test_login_kesbangpol_html(self):
        with self.assertTemplateUsed('kesbangpol_login.html'):
            response = self.client.get('/kesbangpol/login/')
            self.assertEqual(response.status_code, 200)

    def test_login_kesbangpol_form_without_params(self):
        form = KesbangpolAuthenticationForm()
        self.assertFalse(form.is_valid())

    def test_login_kesbangpol_valid_data(self):
        form_data = {"username": self.email, "password": self.password}
        form = KesbangpolAuthenticationForm(data=form_data)
        if form.is_valid():
            form.check()
        self.assertTrue(form.is_valid())

    def test_login_kesbangpol_blank_data(self):
        form_data = {}
        form = KesbangpolAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])
        self.assertEqual(form.errors['password'], ['This field is required.'])

    def test_login_kesbangpol_form_user_not_registered(self):
        with self.assertRaises(ValidationError):
            form_data = {"username": "not_registered@email.com",
                         "password": self.password}
            form = KesbangpolAuthenticationForm(data=form_data)
            if form.is_valid():
                form.check()

    def test_login_kesbangpol_form_password_not_match(self):
        with self.assertRaises(ValidationError):
            form_data = {"username": self.email,
                         'password': "wrongpassword"}
            form = KesbangpolAuthenticationForm(data=form_data)
            if form.is_valid():
                form.check()

    def test_login_kesbangpol_form_user_not_kesbangpol(self):
        self.user_test_account.is_kesbangpol = False
        self.user_test_account.save()

        with self.assertRaises(ValidationError):
            form_data = {"username": self.email, "password": self.password}
            form = KesbangpolAuthenticationForm(data=form_data)
            if form.is_valid():
                form.check()

    def test_login_kesbangpol_success_will_redirect(self):
        user_kesbangpol = KesbangpolProfile(
            user=self.user_test_account,
            unique_kesbangpol_attribute="kesbangpol")
        user_kesbangpol.save()

        response = self.client.post(
            "/kesbangpol/login/",
            {
                'username': self.email,
                'password': self.password,
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/kesbangpol/")


    def test_login_kesbangpol_email_not_registered_not_redirect(self):
        response = self.client.post(
            "/kesbangpol/login/",
            {
                'username': 'new@email.com',
                'password': self.password
            }
        )
        self.assertEqual(response.status_code, 200)


class KesbangpolDashboardTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.request = HttpRequest()
        self.email = "a@a.com"
        self.password = "zxasqw12"
        self.user_name = "abc"
        self.phone = 1234
        self.user_test_account = Account.objects.create_user(
            email=self.email, password=self.password)
        self.user_test_account.is_kesbangpol = True
        self.user_test_account.save()

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_dashboard_kesbangpol_redirect_if_not_login(self):
        response = self.client.get('/kesbangpol/')
        self.assertEqual(response.status_code, 302)

    def test_dashboard_kesbangpol_200_if_login(self):
        self.client.login(username=self.email, password=self.password)
        response = self.client.get('/kesbangpol/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_kesbangpol_html_if_user_login(self):
        self.client.login(username=self.email, password=self.password)
        with self.assertTemplateUsed('kesbangpol_dashboard.html'):
            response = self.client.get('/kesbangpol/')
            self.assertEqual(response.status_code, 200)

    def test_kesbangpol_get_lamaran_details_fail(self):
        response = self.client.get('/kesbangpol/lamaran/1/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'err': 'User Not Exist'}
        )

    def test_kesbangpol_get_lamaran_details_success(self):
        secret_password = '12345678'
        opd = Account.objects.create_user(email='opd@mail.com',
                                          password=secret_password)
        opd.is_opd = True
        opd.name = "OPD Name"
        opd.save()

        user = Account.objects.create_user(email='user@mail.com',
                                           password=secret_password)
        user.is_user = True
        user.name = "Test Name"
        user.save()

        user_profile = UserProfile(user=user)
        user_profile.institution = "UI"
        user_profile.save()

        akhir = datetime.date(2012, 12, 12)
        awal = datetime.date(2011, 11, 11)
        lowongan = Lowongan.objects.create(
            judul='judul1',
            kategori='kat1',
            kuota_peserta=10,
            waktu_awal_magang=awal,
            waktu_akhir_magang=akhir,
            batas_akhir_pendaftaran=akhir,
            berkas_persyaratan=['Kartu Keluarga'],
            deskripsi='deskripsi1',
            requirement='requirement1',
            opd_foreign_key_id=opd.id
        )
        lowongan.save()

        lamar = UserLamarMagang(application_letter='a',
                                lowongan_foreign_key=lowongan,
                                user_foreign_key=user,
                                status_lamaran='Diterima')
        lamar.save()

        response = self.client.get('/kesbangpol/lamaran/'+str(lamar.id)+'/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'bagian': 'kat1', 'durasi': 397, 'institution': 'UI',
             'judul': 'judul1', 'name': 'Test Name', 'opd': 'OPD Name'}
        )
