from unittest import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

from django.test import TestCase, override_settings, Client

from social_django.compat import reverse
from social_django.models import UserSocialAuth
from social_django.views import get_session_timeout


@override_settings(SOCIAL_AUTH_GOOGLE_KEY='1',
                   SOCIAL_AUTH_GOOGLE_SECRET='2')
class TestViews(TestCase):

    def setUp(self):
        session = self.client.session
        session['google_state'] = '1'
        session.save()

    def test_begin_view(self):
        response = self.client.get(reverse('social:begin', kwargs={'backend': 'google-oauth2'}))
        self.assertEqual(response.status_code, 302)

        url = reverse('social:begin', kwargs={'backend': 'blabla'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_page_response_status(self):
        response = Client().get('/user/')
        self.assertEqual(response.status_code, 200)

    def test_page_template(self):
        response = Client().get('/user/')
        self.assertTemplateUsed(response, 'page_test.html')
