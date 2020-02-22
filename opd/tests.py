from django.test import TestCase
from django.test import Client
from django.urls import resolve
from .views import *
from django.http import HttpRequest

class opdPage(TestCase):
	def test_url_exist(self):
		response = self.client.get('/opd/login')
		self.assertEqual(response.status_code,200)
		
	def test_main_template(self):
		response = self.client.get('/opd/login')
		self.assertTemplateUsed(response,'opdLogin.html')
				




  
		
		
	
		