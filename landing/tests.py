import time
import unittest

from django.http import HttpRequest
from django.test import TestCase
from django.test import Client
from django.urls import resolve

from . import views
from account.models import Account

class testing_landing(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.request = HttpRequest()
        self.email = "a@a.com"
        self.password = "zxasqw12"
        self.user_test_account = Account.objects.create_user(
            email=self.email, password=self.password)
        self.user_test_account.save()

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_landing_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_landing_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'landing_page.html')

    def test_landing_content(self):
        response = self.client.get('/')
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Beranda</title>', html_response)

    def test_landing_func(self):
        found = resolve('/')
        self.assertEqual(found.func, views.landing)

    def test_logout_func_fail_if_not_logged_in(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_logout_func_success_if_logged_in_redirect(self):
        self.client.login(username=self.email, password=self.password)
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
