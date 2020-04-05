from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase

from account.models import Account, AdminProfile, OpdProfile, UserProfile


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
        with self.assertRaises(IntegrityError):
            admin_profile.save()

    def test_create_user_pelamar_complete_default_value(self):
        user_profile = UserProfile(
            user=self.user_test_account,
        )
        user_profile.save()

        self.assertEqual(
            self.user_test_account.userprofile.user,
            self.user_test_account
        )

        self.assertEqual(
            user_profile.born_date,
            datetime(1945, 8, 17),
        )

        self.assertEqual(
            user_profile.born_city,
            'Not set',
        )

        self.assertEqual(
            user_profile.address,
            'Not set',
        )

        self.assertEqual(
            user_profile.sex,
            'n',
        )

        self.assertEqual(
            user_profile.education,
            'Not set'
        )

        self.assertEqual(
            user_profile.institution,
            'Not set'
        )

        self.assertEqual(
            user_profile.major,
            'Not set'
        )

        self.assertEqual(
            user_profile.cv,
            None
        )

        self.assertEqual(
            self.user_test_account.userprofile.__str__(),
            "<USER Profile> Account : test@mail.com",
        )

    def test_create_user_pelamar_complete_default_value_not_none(self):
        user_profile = UserProfile(
            user=self.user_test_account,
        )
        user_profile.save()

        self.assertNotEqual(
            self.user_test_account.userprofile.user,
            None,
        )

        self.assertNotEqual(
            user_profile.born_date,
            None,
        )

        self.assertNotEqual(
            user_profile.born_city,
            None,
        )

        self.assertNotEqual(
            user_profile.address,
            None,
        )

        self.assertNotEqual(
            user_profile.sex,
            None,
        )

        self.assertNotEqual(
            user_profile.education,
            None,
        )

        self.assertNotEqual(
            user_profile.institution,
            None,
        )

        self.assertNotEqual(
            user_profile.major,
            None,
        )

        self.assertNotEqual(
            self.user_test_account.userprofile.__str__(),
            None,
        )


    def test_create_user_pelamar_no_user(self):
        user_profile = UserProfile(user=None)
        with self.assertRaises(IntegrityError):
            user_profile.save()

    def test_user_profile_born_date_string_data_type_assert_string(self):
        user_profile = UserProfile(
            user=self.user_test_account,
            born_date="1945-08-17",
        )

        self.assertEqual(user_profile.born_date, "1945-08-17")

    def test_user_profile_born_date_string_data_type_assert_date(self):
        user_profile = UserProfile(
            user=self.user_test_account,
            born_date="1945-08-17",
        )

        self.assertNotEqual(user_profile.born_date, datetime(1945, 8, 17))

    def test_user_profile_born_date_datetime_data_type_assert_string(self):
        user_profile = UserProfile(
            user=self.user_test_account,
            born_date=datetime(1945, 8, 17),
        )

        self.assertNotEqual(user_profile.born_date, "1945-08-17")

    def test_call_userprofile_from_user(self):
        user_profile = UserProfile(
            user=self.user_test_account,
        )

        self.assertEqual(self.user_test_account, user_profile.user)
        self.assertEqual(self.user_test_account.userprofile.sex, 'n')
        self.assertEqual(self.user_test_account.userprofile.born_date, datetime(1945, 8, 17))
        self.assertEqual(self.user_test_account.userprofile.address, 'Not set')

    def test_call_user_from_userprofile(self):
        user_profile = UserProfile(
            user=self.user_test_account,
        )

        self.assertEqual(user_profile.user, self.user_test_account)
        self.assertEqual(user_profile.user.userprofile.user, self.user_test_account)
