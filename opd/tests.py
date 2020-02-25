from django.test import TestCase
from django.test import Client
from django.urls import resolve
from .views import *
from django.http import HttpRequest

class opd_page(TestCase):
	def test_opd_login_url_exist(self):
		response = self.client.get('/opd/login/')
		self.assertEqual(response.status_code,200)
		
	def test_opd_login_template(self):
		response = self.client.get('/opd/login/')
		self.assertTemplateUsed(response,'opdLogin.html')
				




  
		
		
	
		