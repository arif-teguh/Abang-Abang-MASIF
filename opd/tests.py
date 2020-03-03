from django.test import TestCase, Client
from django.urls import resolve
from django.http import HttpRequest
import secrets

from admin.models import OpdVerificationList
from opd import views

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
