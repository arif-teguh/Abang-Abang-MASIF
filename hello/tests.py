from django.test import TestCase
from django.test import Client


class ViewTest(TestCase):
    def test_index_view(self):
        client = Client()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello")
