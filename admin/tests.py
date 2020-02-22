from django.test import TestCase, Client


class AdminUnitTest(TestCase):
    def test_admin_url_exist(self):
        response = Client().get('/admin')
        self.assertEqual(response.status_code, 200)

# Create your tests here.
