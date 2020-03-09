import mock
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

from django.test import TestCase, override_settings

from social_django.compat import reverse
from social_django.models import UserSocialAuth
from social_django.views import get_session_timeout
from .compat import base_url


@override_settings(SOCIAL_AUTH_GOOGLE_KEY='1',
                   SOCIAL_AUTH_GOOGLE_SECRET='2')
class TestViews(TestCase):
    def setUp(self):
        session = self.client.session
        session['google_state'] = '1'
        session.save()

    def test_begin_view(self):
        response = self.client.get(reverse('social:begin', kwargs={'backend': 'google'}))
        self.assertEqual(response.status_code, 302)

        url = reverse('social:begin', kwargs={'backend': 'blabla'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @mock.patch('social_core.backends.base.BaseAuth.request')
    def test_complete(self, mock_request):
        url = reverse('social:complete', kwargs={'backend': 'google'})
        url += '?code=2&state=1'
        mock_request.return_value.json.return_value = {'access_token': '123'}
        with mock.patch('django.contrib.sessions.backends.base.SessionBase'
                        '.set_expiry', side_effect=[OverflowError, None]):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, base_url + '/accounts/profile/')

    @mock.patch('social_core.backends.base.BaseAuth.request')
    def test_disconnect(self, mock_request):
        user_model = get_user_model()
        user = user_model.objects.create_user(username='test', password='pwd')
        UserSocialAuth.objects.create(user=user, provider='google')
        self.client.login(username='test', password='pwd')

        url = reverse('social:disconnect', kwargs={'backend': 'google'})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/accounts/profile/')

        url = reverse('social:disconnect_individual',
                      kwargs={'backend': 'google', 'association_id': '123'})
        hup = AbstractBaseUser.has_usable_password
        del AbstractBaseUser.has_usable_password
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/accounts/profile/')
        AbstractBaseUser.has_usable_password = hup
