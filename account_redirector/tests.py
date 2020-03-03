from django.http import HttpRequest
from django.test import TestCase, Client

from account.models import Account
from . import views


class AccountRedirectorUnitTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        self.created_mock_user = Account.objects.all()[0]

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_admin_redirector_url_exist_and_can_redirect(self):
        response = Client().get('/account-redirector')
        self.assertEqual(response.status_code, 302)

    def test_redirect_admin(self):
        self.request.user = self.created_mock_user
        self.request.user.is_admin = True
        self.request.user.is_opd = False
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.account_redirector(request=self.request)
        self.assertEqual(response.url, '/admin')

    def test_redirect_not_admin(self):
        self.request.user = self.created_mock_user
        self.request.user.is_admin = False
        self.request.user.is_opd = True
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.account_redirector(request=self.request)
        self.assertNotEqual(response.url, '/admin')

    def test_redirect_opd(self):
        self.request.user = self.created_mock_user
        self.request.user.is_admin = False
        self.request.user.is_opd = True
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.account_redirector(request=self.request)
        self.assertEqual(response.url, '/opd')

    def test_redirect_not_opd(self):
        self.request.user = self.created_mock_user
        self.request.user.is_admin = True
        self.request.user.is_opd = False
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.account_redirector(request=self.request)
        self.assertNotEqual(response.url, '/opd')

    def test_redirect_user(self):
        self.request.user = self.created_mock_user
        self.request.user.is_admin = False
        self.request.user.is_opd = False
        self.request.user.is_user = True
        self.request.user.is_superuser = False
        response = views.account_redirector(request=self.request)
        self.assertEqual(response.url, '/')

    def test_redirect_not_user(self):
        self.request.user = self.created_mock_user
        self.request.user.is_admin = True
        self.request.user.is_opd = False
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.account_redirector(request=self.request)
        self.assertNotEqual(response.url, '/')
