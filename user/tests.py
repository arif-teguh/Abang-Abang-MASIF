from django.http import HttpRequest
from django.test import TestCase, Client
from selenium import webdriver

from account.models import Account, UserProfile
from user.forms import EditUserProfileForm


class UserUnitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.request = HttpRequest()
        self.created_mock_user = Account.objects.create_user(
            email='test@mail.com',
            password='12345678',
        )
        self.request.user = self.created_mock_user
        self.mock_user_profile = UserProfile(user=self.created_mock_user)
        self.mock_user_profile.save()

    def tearDown(self):
        pass

    def test_access_user_dashboard_url_logged_in_should_return_200(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        response = self.client.get('/user/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_access_user_dashboard_url_not_logged_in_should_return_302(self):
        response = self.client.get(
            '/user/dashboard/'
        )
        self.assertEqual(response.status_code, 302)

    def test_access_user_dashboard_url_logged_in_not_user_should_return_302(self):
        self.created_mock_user.is_user = False
        self.created_mock_user.save()
        response = self.client.get('/user/dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_user_has_user_dashboard_profile_no_redirect(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        response = self.client.get('/user/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_user_has_no_user_dashboard_profile_should_redirect(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.userprofile.delete()
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        response = self.client.get('/user/dashboard/')
        self.assertEqual(response.status_code, 302)

    #
    def test_access_user_dashboard_edit_url_logged_in_should_return_200(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(
            username='test@mail.com',
            password='12345678',
        )
        response = self.client.get('/user/dashboard/edit/')
        self.assertEqual(response.status_code, 200)

    def test_access_user_dashboard_edit_url_not_logged_in_should_return_302(self):
        response = self.client.get('/user/dashboard/edit/')
        self.assertEqual(response.status_code, 302)

    def test_access_user_dashboard_edit_url_logged_in_not_user_should_return_302(self):
        self.created_mock_user.is_user = False
        self.created_mock_user.save()
        response = self.client.get('/user/dashboard/edit/')
        self.assertEqual(response.status_code, 302)

    def test_user_edit_has_user_dashboard_edit_profile_no_redirect(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        response = self.client.get('/user/dashboard/edit/')
        self.assertEqual(response.status_code, 200)

    def test_user_has_no_user_dashboard_edit_profile_should_redirect(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.userprofile.delete()
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        response = self.client.get('/user/dashboard/edit/')
        self.assertEqual(response.status_code, 302)

    def test_user_edit_profile_page_is_set_up_as_expected(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        response = self.client.get('/user/dashboard/edit/')
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertTrue(
            isinstance(form, EditUserProfileForm), type(form).__mro__)


class UserFunctionalTest(TestCase):
    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(
            chrome_options=chrome_options,
            executable_path='./chromedriver',
        )

    def tearDown(self):
        self.driver.quit()
        super(UserFunctionalTest, self).tearDown()

    # This function is just to make sure that chromedriver is properly installed on gitlab pipeline
    def test_input_status_selenium(self):
        self.driver.get(url='http://localhost:8000/')
