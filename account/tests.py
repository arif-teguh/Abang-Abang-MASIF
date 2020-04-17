from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase
from account.models import Account, AdminProfile, OpdProfile, PelamarProfile, UserProfile


# Create your tests here.
class AccountUnitTest(TestCase):
    def setUp(self):
        self.DEFAULT_BLANK = ""
        self.DEFAULT_NOT_SET = "Not set"
        self.DEFAULT_BORN_DATE_STRING = "1945-08-17"
        self.DEFAULT_BORN_DATE_DATETIME = datetime(1945, 8, 17)

        self.test_mail = "test@mail.com"
        self.test_supermail = "super@mail.com"
        self.test_password = "1234"

        self.user_test_account = Account.objects.create_user(
            email=self.test_mail, password=self.test_password)
        self.superuser_test_account = Account.objects.create_superuser(
            email=self.test_supermail, password=self.test_password)

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_create_user_using_create_user_function_complete(self):
        self.assertEqual(self.user_test_account.name, self.DEFAULT_BLANK)
        self.assertEqual(self.user_test_account.email, self.test_mail)

    def test_create_user_using_create_user_function_no_email(self):
        with self.assertRaises(ValueError):
            Account.objects.create_user(email=self.DEFAULT_BLANK, password=self.test_password)

    def test_create_superuser_using_create_superuser_function_complete(self):
        self.assertEqual(self.superuser_test_account.profile_picture, None)
        self.assertEqual(self.superuser_test_account.name, "SuperUser")
        self.assertEqual(self.superuser_test_account.phone, "000")
        self.assertEqual(self.superuser_test_account.is_superuser, True)
        self.assertEqual(self.superuser_test_account.is_staff, True)
        self.assertEqual(self.superuser_test_account.is_admin, True)
        self.assertEqual(self.superuser_test_account.email, self.test_supermail)
        self.assertEqual(
            self.superuser_test_account.__str__(), self.test_supermail)
        self.assertEqual(
            self.superuser_test_account.has_module_perms("module"), True)
        self.assertEqual(self.superuser_test_account.has_perm("perm"), True)

    def test_create_superuser_using_create_superuser_function_no_email(self):
        with self.assertRaises(ValueError):
            Account.objects.create_superuser(email=self.DEFAULT_BLANK, 
                                             password=self.test_password)

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
            self.test_mail)

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
            self.test_mail)

    def test_create_user_admin_no_user(self):
        admin_profile = AdminProfile(user=None, unique_admin_attribute="admin")
        with self.assertRaises(IntegrityError):
            admin_profile.save()

    def test_create_user_pelamar_complete_default_value(self):
        user_profile = UserProfile(user=self.user_test_account,)
        user_profile.save()

        self.assertEqual(
            self.user_test_account.userprofile.user,
            self.user_test_account
        )

        self.assertEqual(
            user_profile.born_date,
            self.DEFAULT_BORN_DATE_DATETIME,
        )

        self.assertEqual(
            user_profile.born_city,
            self.DEFAULT_NOT_SET,
        )

        self.assertEqual(
            user_profile.address,
            self.DEFAULT_NOT_SET,
        )

        self.assertEqual(
            user_profile.sex,
            'n',
        )

        self.assertEqual(
            user_profile.education,
            self.DEFAULT_NOT_SET
        )

        self.assertEqual(
            user_profile.institution,
            self.DEFAULT_NOT_SET
        )

        self.assertEqual(
            user_profile.major,
            self.DEFAULT_NOT_SET
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

    def test_create_user_profile_no_user(self):
        user_profile = UserProfile(user=None)
        with self.assertRaises(IntegrityError):
            user_profile.save()

    def test_user_profile_born_date_string_data_type_assert_string(self):
        user_profile = UserProfile(
            user=self.user_test_account,
            born_date=self.DEFAULT_BORN_DATE_STRING,
        )

        self.assertEqual(user_profile.born_date, self.DEFAULT_BORN_DATE_STRING)

    def test_user_profile_born_date_string_data_type_assert_date(self):
        user_profile = UserProfile(
            user=self.user_test_account,
            born_date=self.DEFAULT_BORN_DATE_STRING,
        )

        self.assertNotEqual(user_profile.born_date, self.DEFAULT_BORN_DATE_DATETIME)

    def test_user_profile_born_date_datetime_data_type_assert_string(self):
        user_profile = UserProfile(
            user=self.user_test_account,
            born_date=self.DEFAULT_BORN_DATE_DATETIME,
        )

        self.assertNotEqual(user_profile.born_date, self.DEFAULT_BORN_DATE_STRING)

    def test_call_userprofile_from_user(self):
        user_profile = UserProfile(
            user=self.user_test_account,
        )

        self.assertEqual(self.user_test_account, user_profile.user)
        self.assertEqual(self.user_test_account.userprofile.sex, 'n')
        self.assertEqual(
            self.user_test_account.userprofile.born_date, self.DEFAULT_BORN_DATE_DATETIME)
        self.assertEqual(self.user_test_account.userprofile.address, self.DEFAULT_NOT_SET)

    def test_call_user_from_userprofile(self):
        user_profile = UserProfile(
            user=self.user_test_account,
        )

        self.assertEqual(user_profile.user, self.user_test_account)
        self.assertEqual(user_profile.user.userprofile.user,
                         self.user_test_account)

    def test_create_user_pelamar_complete(self):
        newly_created_user = Account.objects.all()[0]
        pelamar_profile = PelamarProfile(
            user=newly_created_user, unique_pelamar_attribute="user")
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
            self.test_mail)

    def test_create_user_pelamar_no_user(self):
        pelamar_profile = OpdProfile(user=None, unique_opd_attribute="user")
        try:
            pelamar_profile.save()
        except:
            self.assertTrue(True)
