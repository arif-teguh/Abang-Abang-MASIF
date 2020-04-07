from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase
from account.models import Account, AdminProfile, OpdProfile, PelamarProfile


# Create your tests here.
class AccountUnitTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.user_test_account = Account.objects.create_user(email="test@mail.com", password="1234")
        self.superuser_test_account = Account.objects.create_superuser(email="super@mail.com", password="1234")

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_create_user_using_create_user_function_complete(self):
        self.assertEqual(self.user_test_account.name, "")
        self.assertEqual(self.user_test_account.email, "test@mail.com")

    def test_create_user_using_create_user_function_no_email(self):
        with self.assertRaises(ValueError):
            Account.objects.create_user(email="", password="1234")

    def test_create_user_using_create_user_function_empty_string_password(self):
        self.assertEqual(self.user_test_account.name, "")
        self.assertEqual(self.user_test_account.email, "test@mail.com")

    def test_create_superuser_using_create_superuser_function_complete(self):
        self.assertEqual(self.superuser_test_account.profile_picture, None)
        self.assertEqual(self.superuser_test_account.name, "SuperUser")
        self.assertEqual(self.superuser_test_account.phone, "000")
        self.assertEqual(self.superuser_test_account.is_superuser, True)
        self.assertEqual(self.superuser_test_account.is_staff, True)
        self.assertEqual(self.superuser_test_account.is_admin, True)
        self.assertEqual(self.superuser_test_account.email, "super@mail.com")
        self.assertEqual(self.superuser_test_account.__str__(), "super@mail.com")
        self.assertEqual(self.superuser_test_account.has_module_perms("module"), True)
        self.assertEqual(self.superuser_test_account.has_perm("perm"), True)

    def test_create_superuser_using_create_superuser_function_no_email(self):
        with self.assertRaises(ValueError):
            Account.objects.create_superuser(email="", password="1234")

    def test_create_user_opd_complete(self):
        opd_profile = OpdProfile(user=self.user_test_account,
                                 unique_opd_attribute="opd")
        opd_profile.save()
        self.assertEqual(self.user_test_account
                         .opdprofile
                         .unique_opd_attribute,
                         "opd")

        self.assertEqual(
            self.user_test_account.opdprofile.__str__(),
            "<OPD Profile> opd")

        self.assertEqual(
            self.user_test_account.opdprofile.user.email,
            "test@mail.com")

    def test_create_user_opd_no_user(self):
        opd_profile = OpdProfile(user=None, unique_opd_attribute="opd")
        with self.assertRaises(IntegrityError):
            opd_profile.save()

    def test_create_user_admin_complete(self):
        admin_profile = AdminProfile(
            user=self.user_test_account,
            unique_admin_attribute="admin")
        admin_profile.save()
        self.assertEqual(
            self.user_test_account.adminprofile.unique_admin_attribute,
            "admin")
        self.assertEqual(
            self.user_test_account.adminprofile.__str__(),
            "<ADMIN Profile> admin")

        self.assertEqual(
            self.user_test_account.adminprofile.user.email,
            "test@mail.com")

    def test_create_user_admin_no_user(self):
        admin_profile = AdminProfile(user=None, unique_admin_attribute="admin")
        try:
            admin_profile.save()
        except:
            self.assertTrue(True)


    def test_create_user_pelamar_complete(self):
        Account.objects.create_user(email="test@mail.com", password="1234")
        newly_created_user = Account.objects.all()[0]
        pelamar_profile = PelamarProfile(user=newly_created_user,
                                 unique_pelamar_attribute="user")
        pelamar_profile.save()
        self.assertEqual(newly_created_user
                         .pelamarprofile
                         .unique_pelamar_attribute,
                         "user")

        self.assertEqual(
            newly_created_user.pelamarprofile.__str__(),
            "<PELAMAR Profile> user")

        self.assertEqual(
            newly_created_user.pelamarprofile.user.email,
            "test@mail.com")

    def test_create_user_pelamar_no_user(self):
        pelamar_profile = OpdProfile(user=None, unique_opd_attribute="user")
        try:
            pelamar_profile.save()
        except:
            self.assertTrue(True)


