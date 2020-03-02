from django.forms import forms
from django.http import HttpRequest
from django.test import TestCase, Client
from django.urls import resolve

from account.models import Account
from admin import views
from admin.admin_login_form import AdminAuthenticationForm


class AdminUnitTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.request = HttpRequest()
        Account.objects.create_user(email='test@mail.com', password='12345678')
        self.created_mock_user = Account.objects.all()[0]
        self.client.login(username='test@mail.com', password='12345678')
        self.request.user = self.created_mock_user

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_page_title_admin_login(self):
        response = views.admin_login(self.request)
        html_response = response.content.decode('utf8')
        self.assertIn('<title>Admin Login</title>', html_response)

    def test_using_admin_login_html(self):
        response = Client().get('/admin/login/')
        self.assertTemplateUsed(response, 'admin/admin_login.html')

    def test_submit_button_exist(self):
        request = HttpRequest()
        response = views.admin_login(request)
        html_response = response.content.decode('utf8')
        self.assertIn('<button type="submit"', html_response)

    def test_admin_login_page_is_set_up_as_expected(self):
        response = Client().get('/admin/login/')
        self.assertEqual(200, response.status_code)
        form = response.context['form']
        self.assertTrue(
            isinstance(form, AdminAuthenticationForm), type(form).__mro__)

    def test_displays_admin_login_form(self):
        response = Client().get('/admin/login/')
        self.assertIsInstance(response.context["form"], AdminAuthenticationForm)

    def test_admin_page_not_authenticated(self):
        response = Client().get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/admin/login/', response.url)

    def test_admin_access_admin_page(self):
        self.request.user.is_admin = True
        self.request.user.is_opd = False
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.admin_index(request=self.request)
        self.assertEqual(response.status_code, 200)

    def test_opd_access_admin_page(self):
        self.request.user.is_admin = False
        self.request.user.is_opd = True
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.admin_index(request=self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/admin/login/', response.url)

    def test_user_access_admin_page(self):
        self.request.user.is_admin = False
        self.request.user.is_opd = False
        self.request.user.is_user = True
        self.request.user.is_superuser = False
        response = views.admin_index(request=self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/admin/login/', response.url)

    def test_admin_access_admin_page_through_url(self):
        self.created_mock_user.is_admin = True
        self.created_mock_user.save()
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_opd_access_admin_page_through_url(self):
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_opd = True
        self.created_mock_user.save()
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/admin/login/', response.url)

    def test_user_access_admin_page_through_url(self):
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = True
        self.created_mock_user.save()
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/admin/login/', response.url)

    def test_using_admin_index_func(self):
        found = resolve('/admin/')
        self.assertEqual(found.func, views.admin_index)

    def test_admin_list_opd_not_authenticated_redirect_to_admin_login(self):
        response = Client().get('/admin/listopd/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/admin/login/', response.url)

    def test_using_admin_list_opd_func(self):
        found = resolve('/admin/listopd/')
        self.assertEqual(found.func, views.admin_list_opd)

    def test_admin_access_admin_opd_list_page(self):
        self.request.user.is_admin = True
        self.request.user.is_opd = False
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.admin_list_opd(request=self.request)
        self.assertEqual(response.status_code, 200)

    def test_opd_access_admin_opd_list_page(self):
        self.request.user.is_admin = False
        self.request.user.is_opd = True
        self.request.user.is_user = False
        self.request.user.is_superuser = False
        response = views.admin_list_opd(request=self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/admin/login/', response.url)

    def test_user_access_admin_opd_list_page(self):
        self.request.user.is_admin = False
        self.request.user.is_opd = False
        self.request.user.is_user = True
        self.request.user.is_superuser = False
        response = views.admin_list_opd(request=self.request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/admin/login/', response.url)

    def test_function_get_all_opd_database_has_opd(self):
        self.created_mock_user.is_opd = True
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.save()
        all_opd = views.get_all_opd()
        self.assertEqual([self.created_mock_user], all_opd)

    def test_function_get_all_opd_database_empty(self):
        all_opd = views.get_all_opd()
        self.assertEqual([], all_opd)

    def test_function_get_all_opd_database_has_admin(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.save()
        all_opd = views.get_all_opd()
        self.assertEqual([], all_opd)

    def test_function_get_all_opd_database_has_user(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = True
        self.created_mock_user.is_staff = False
        self.created_mock_user.save()
        all_opd = views.get_all_opd()
        self.assertEqual([], all_opd)

    def test_confirm_login_allowed_function_as_admin_is_active(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.save()
        admin_auth_form = AdminAuthenticationForm()
        result = admin_auth_form.confirm_login_allowed(
            user=self.created_mock_user
        )
        self.assertEqual(None, result)

    def test_confirm_login_allowed_function_as_opd_is_active(self):
        self.created_mock_user.is_opd = True
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        admin_auth_form = AdminAuthenticationForm()
        self.created_mock_user.save()
        with self.assertRaises(forms.ValidationError):
            admin_auth_form.confirm_login_allowed(user=self.created_mock_user)

    def test_confirm_login_allowed_function_as_user_is_active(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = True
        self.created_mock_user.is_staff = False
        self.created_mock_user.save()
        admin_auth_form = AdminAuthenticationForm()
        with self.assertRaises(forms.ValidationError):
            admin_auth_form.confirm_login_allowed(user=self.created_mock_user)

    def test_confirm_login_allowed_function_as_admin_is_not_active(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        admin_auth_form = AdminAuthenticationForm()
        with self.assertRaises(forms.ValidationError):
            admin_auth_form.confirm_login_allowed(user=self.created_mock_user)

    def test_confirm_login_allowed_function_as_opd_is_not_active(self):
        self.created_mock_user.is_opd = True
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        admin_auth_form = AdminAuthenticationForm()
        with self.assertRaises(forms.ValidationError):
            admin_auth_form.confirm_login_allowed(user=self.created_mock_user)

    def test_confirm_login_allowed_function_as_user_is_not_active(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = True
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        admin_auth_form = AdminAuthenticationForm()
        with self.assertRaises(forms.ValidationError):
            admin_auth_form.confirm_login_allowed(user=self.created_mock_user)

    def test_delete_opd_account_correct_pk(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        response = self.client.post(
            '/admin/listopd/deleteopd/',
            {'pk': self.created_mock_user.pk}
        )
        all_test_opd = list(Account.objects.all())
        self.assertEqual(
            'Delete OPD Success', response.content.decode('utf8')
        )
        self.assertEqual(all_test_opd, [])

    def test_delete_opd_account_wrong_pk(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        with self.assertRaises(IndexError):
            self.client.post(
                '/admin/listopd/deleteopd/',
                {'pk': int(self.created_mock_user.pk) + 1}
            )

    def test_delete_opd_account_string_pk(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        with self.assertRaises(ValueError):
            self.client.post(
                '/admin/listopd/deleteopd/',
                {'pk': 'abcdef'}
            )

    def test_delete_opd_account_mix_string_int_pk(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        with self.assertRaises(ValueError):
            self.client.post('/admin/listopd/deleteopd/', {'pk': 'g4bung'})

    def test_delete_opd_account_no_pk(self):
        self.created_mock_user.is_opd = False
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = True
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        with self.assertRaises(ValueError):
            self.client.post('/admin/listopd/deleteopd/', {'pk': ''})

    def test_delete_opd_account_correct_pk_not_admin(self):
        self.created_mock_user.is_opd = True
        self.created_mock_user.is_superuser = False
        self.created_mock_user.is_admin = False
        self.created_mock_user.is_user = False
        self.created_mock_user.is_staff = False
        self.created_mock_user.is_active = False
        self.created_mock_user.save()
        self.client.post(
            '/admin/listopd/deleteopd/',
            {'pk': self.created_mock_user.pk}
        )
        all_test_opd = list(Account.objects.all())
        self.assertEqual(
            [self.created_mock_user],
            all_test_opd
        )

    def test_get_method_in_delete_opd_for_admin(self):
        response = self.client.get('/admin/listopd/deleteopd/')
        html_response = response.content.decode('utf8')
        self.assertEqual("Forbidden", html_response)
