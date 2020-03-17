from django.http import HttpRequest
from django.test import TestCase, Client

from account.models import Account, UserProfile
from user.forms import EditUserProfileForm
from user.views import born_date_validator, sex_validator, phone_number_validator, is_data_valid


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

    def test_date_validator_correct_date_should_return_true(self):
        result = born_date_validator({'born_date': '17/08/1945'})
        self.assertEqual(True, result['result'])

    def test_date_validator_empty_string_date_should_return_false(self):
        result = born_date_validator({'born_date': ''})
        self.assertEqual(False, result['result'])

    def test_date_validator_integer_date_should_return_false(self):
        result = born_date_validator({'born_date': 17081945})
        self.assertEqual(False, result['result'])

    def test_date_validator_no_year_date_should_return_false(self):
        result = born_date_validator({'born_date': '17/08/'})
        self.assertEqual(False, result['result'])

    def test_date_validator_no_month_date_should_return_false(self):
        result = born_date_validator({'born_date': '17//1945'})
        self.assertEqual(False, result['result'])

    def test_date_validator_no_day_date_should_return_false(self):
        result = born_date_validator({'born_date': '/08/1945'})
        self.assertEqual(False, result['result'])

    def test_date_validator_no_day_month_year_date_should_return_false(self):
        result = born_date_validator({'born_date': '//'})
        self.assertEqual(False, result['result'])

    def test_date_validator_mmddyyyy_date_should_return_false(self):
        result = born_date_validator({'born_date': '12/30/1945'})
        self.assertEqual(False, result['result'])

    def test_date_validator_yyyymmdd_date_should_return_false(self):
        result = born_date_validator({'born_date': '1945/08/1945'})
        self.assertEqual(False, result['result'])

    def test_sex_validator_f_should_return_true(self):
        validation_result = sex_validator({'sex': 'f'})['result']
        self.assertEqual(True, validation_result)

    def test_sex_validator_m_should_return_true(self):
        validation_result = sex_validator({'sex': 'm'})['result']
        self.assertEqual(True, validation_result)

    def test_sex_validator_lainlain_should_return_false(self):
        validation_result = sex_validator({'sex': 'lainlain'})['result']
        self.assertEqual(False, validation_result)

    def test_phone_number_correct_should_return_true(self):
        validation_result = phone_number_validator({'phone': '0812345678'})['result']
        self.assertEqual(True, validation_result)

    def test_phone_number_one_digit_should_return_false(self):
        validation_result = phone_number_validator({'phone': '1'})['result']
        self.assertEqual(False, validation_result)

    def test_phone_number_sixteen_should_return_false(self):
        validation_result = phone_number_validator({'phone': '16'})['result']
        self.assertEqual(False, validation_result)

    def test_is_data_valid_correct_data_should_return_true(self):
        validation_result = is_data_valid({'phone': '0812345678', 'sex': 'm', 'born_date': '17/08/1945'})['result']
        self.assertEqual(True, validation_result)

    def test_is_data_valid_wrong_born_date_data_should_return_false(self):
        validation_result = is_data_valid({'phone': '0812345678', 'sex': 'm', 'born_date': '/08/1945'})['result']
        self.assertEqual(False, validation_result)

    def test_is_data_valid_wrong_phone_data_should_return_false(self):
        validation_result = is_data_valid({'phone': '1', 'sex': 'm', 'born_date': '17/08/1945'})['result']
        self.assertEqual(False, validation_result)

    def test_is_data_valid_wrong_sex_data_should_return_false(self):
        validation_result = is_data_valid({'phone': '0812345678', 'sex': 'lainlain', 'born_date': '17/08/1945'})[
            'result']
        self.assertEqual(False, validation_result)

    def test_logged_in_post_to_edit_profile_url_correct_data_should_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': 'Computer Science'
        }
        result = self.client.post('/user/dashboard/edit/', data=form_data)
        self.assertEqual('17/08/1945', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_name_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        form_data = {

            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': 'Computer Science'
        }
        result = self.client.post('/user/dashboard/edit/', data=form_data)
        self.assertEqual('name', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_address_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        form_data = {
            'name': 'test',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': 'Computer Science'
        }
        result = self.client.post('/user/dashboard/edit/', data=form_data)
        self.assertEqual('address', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_born_date_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': 'Computer Science'
        }
        result = self.client.post('/user/dashboard/edit/', data=form_data)
        self.assertEqual('born_date', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_born_city_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': 'Computer Science'
        }
        result = self.client.post('/user/dashboard/edit/', data=form_data)
        self.assertEqual('born_city', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_phone_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': 'Computer Science'
        }
        result = self.client.post('/user/dashboard/edit/', data=form_data)
        self.assertEqual('phone', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_sex_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'institution': 'uwiw',
            'education': 'smk',
            'major': 'Computer Science'
        }
        result = self.client.post('/user/dashboard/edit/', data=form_data)
        self.assertEqual('sex', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_institution_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'education': 'smk',
            'major': 'Computer Science'
        }
        result = self.client.post('/user/dashboard/edit/', data=form_data)
        self.assertEqual('institution', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_education_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'major': 'Computer Science'
        }
        result = self.client.post('/user/dashboard/edit/', data=form_data)
        self.assertEqual('education', result.content.decode('utf-8'))

    def test_logged_in_post_to_edit_profile_url_no_major_data_shouldnt_work(self):
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        self.client.login(username='test@mail.com', password='12345678')
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
        }
        result = self.client.post('/user/dashboard/edit/', data=form_data)
        self.assertEqual('major', result.content.decode('utf-8'))

    def test_not_logged_in_post_to_edit_profile_url_should_redirect(self):
        form_data = {
            'name': 'test',
            'address': 'rumah',
            'born_date': '17/08/1945',
            'born_city': 'Depok',
            'phone': '0812345678',
            'sex': 'm',
            'institution': 'uwiw',
            'education': 'smk',
            'major': 'Computer Science'
        }
        result = self.client.post('/user/dashboard/edit/', data=form_data)
        self.assertEqual(result.status_code, 302)

# class UserFunctionalTest(TestCase):
#     def setUp(self):
#         chrome_options = webdriver.ChromeOptions()
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--window-size=1420,1080')
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--disable-gpu')
#         self.driver = webdriver.Chrome(
#             chrome_options=chrome_options,
#             executable_path='./chromedriver',
#         )
#
#     def tearDown(self):
#         self.driver.quit()
#         super(UserFunctionalTest, self).tearDown()
#
#     # This function is just to make sure that chromedriver is properly installed on gitlab pipeline
#     def test_input_status_selenium(self):
#         self.driver.get(url='http://localhost:8000/')
