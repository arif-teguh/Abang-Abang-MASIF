import time
import unittest

from django.http import HttpRequest
from django.test import TestCase
from django.test import Client
from django.urls import resolve
from . import views


# Create your tests here.

class Testing_landing(TestCase):

    def test_landing_page(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_landing_template(self):
        response = Client().get('/')
        self.assertTemplateUsed(response, 'landing_page.html')

    def test_landing_content(self):
        response = Client().get('/')
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Beranda</title>', html_response)

    def test_landing_func(self):
        found = resolve('/')
        self.assertEqual(found.func, views.landing)
