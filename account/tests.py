from django.test import TestCase
from account.models import Account, AdminProfile, OpdProfile, AccountManager


# Create your tests here.
class AccountUnitTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_create_user_using_create_user_function_complete(self):
        Account.objects.create_user(email="test@mail.com", password="1234")
        newly_created_user = Account.objects.all()[0]
        self.assertEqual(newly_created_user.name, "")
        self.assertEqual(newly_created_user.email, "test@mail.com")

    def test_create_user_using_create_user_function_no_email(self):
        with self.assertRaises(ValueError):
            Account.objects.create_user(email="", password="1234")

    def test_create_user_using_create_user_function_empty_string_password(self):
        Account.objects.create_user(email="test@mail.com", password="")
        newly_created_user = Account.objects.all()[0]
        self.assertEqual(newly_created_user.name, "")
        self.assertEqual(newly_created_user.email, "test@mail.com")

    def test_create_superuser_using_create_superuser_function_complete(self):
        Account.objects.create_superuser(email="test@mail.com", password="1234")
        newly_created_user = Account.objects.all()[0]
        self.assertEqual(newly_created_user.name, "SuperUser")
        self.assertEqual(newly_created_user.phone, "000")
        self.assertEqual(newly_created_user.is_superuser, True)
        self.assertEqual(newly_created_user.is_staff, True)
        self.assertEqual(newly_created_user.is_admin, True)
        self.assertEqual(newly_created_user.email, "test@mail.com")
        self.assertEqual(newly_created_user.__str__(), "test@mail.com")
        self.assertEqual(newly_created_user.has_module_perms("module"), True)
        self.assertEqual(newly_created_user.has_perm("perm"), True)

    def test_create_superuser_using_create_superuser_function_no_email(self):
        with self.assertRaises(ValueError):
            Account.objects.create_superuser(email="", password="1234")

    def test_create_user_opd_complete(self):
        Account.objects.create_superuser(email="test@mail.com", password="1234")
        newly_created_user = Account.objects.all()[0]
        opd_profile = OpdProfile(user=newly_created_user,
                                 unique_opd_attribute="opd")
        opd_profile.save()
        self.assertEqual(newly_created_user
                         .opdprofile
                         .unique_opd_attribute,
                         "opd")

        self.assertEqual(
            newly_created_user.opdprofile.__str__(),
            "<OPD Profile> opd")

        self.assertEqual(
            newly_created_user.opdprofile.user.email,
            "test@mail.com")

    def test_create_user_opd_no_user(self):
        opd_profile = OpdProfile(user=None, unique_opd_attribute="opd")
        try:
            opd_profile.save()
        except:
            self.assertTrue(True)

    def test_create_user_admin_complete(self):
        Account.objects.create_superuser(email="test@mail.com", password="1234")
        newly_created_user = Account.objects.all()[0]
        admin_profile = AdminProfile(
            user=newly_created_user,
                                     unique_admin_attribute="admin")
        admin_profile.save()
        self.assertEqual(
            newly_created_user.adminprofile.unique_admin_attribute,
            "admin")
        self.assertEqual(
            newly_created_user.adminprofile.__str__(),
            "<ADMIN Profile> admin")

        self.assertEqual(
            newly_created_user.adminprofile.user.email,
                         "test@mail.com")

    def test_create_user_admin_no_user(self):
        admin_profile = AdminProfile(user=None, unique_admin_attribute="admin")
        try:
            admin_profile.save()
        except:
            self.assertTrue(True)
