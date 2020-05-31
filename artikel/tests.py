import tempfile
import shutil
from django.test import TestCase, override_settings, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from account.models import Account
from .models import Artikel

MEDIA_ROOT = tempfile.mkdtemp()
url_form_artikel = "/artikel/form/"
url_post_form_artikel = url_form_artikel+"post/"
url_update_form_artikel = url_form_artikel+"edit/"

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ArtikelModelTest(TestCase):
    def setUp(self):
        self.test_file_jpg1 = SimpleUploadedFile("foto1.jpg", b"file_content")
        self.test_file_jpg2 = SimpleUploadedFile("foto2.jpg", b"file_content")
        self.artikel1 = Artikel.objects.create(
            judul='judul1',
            deskripsi='deskripsi1',
            foto_artikel=self.test_file_jpg1
        )
        self.artikel2 = Artikel.objects.create(
            judul='judul2',
            deskripsi='deskripsi2',
            foto_artikel=self.test_file_jpg2
        )
        self.artikel1.save()
        self.artikel2.save()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_object_artikel_is_created(self):
        self.assertTrue(type(self.artikel1), Artikel)
        self.assertTrue(type(self.artikel2), Artikel)

    def test_id_artikel_is_generated(self):
        self.assertIsNotNone(self.artikel1.id)
        self.assertIsNotNone(self.artikel2.id)

    def test_judul_is_judul1(self):
        self.assertEqual(self.artikel1.judul, "judul1")

    def test_judul_artikel1_artikel2_not_equal(self):
        self.assertNotEqual(self.artikel1.judul, self.artikel2.judul)

    def test_deskripsi_is_deskripsi1(self):
        self.assertEqual(self.artikel1.deskripsi, "deskripsi1")

    def test_deskripsi_artikel1_artikel2_not_equal(self):
        self.assertNotEqual(self.artikel1.deskripsi, self.artikel2.deskripsi)

    def test_foto_artikel_is_not_none(self):
        self.assertIsNotNone(self.artikel1.foto_artikel)

    def test_artikel_artikel1_artikel2_not_equal(self):
        self.assertNotEqual(self.artikel1.foto_artikel,
                            self.artikel2.foto_artikel)

    def test_waktu_dibuat_not_none(self):
        self.assertIsNotNone(self.artikel1.waktu_dibuat)

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ArtikelFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user('test_user',
                                                password='test_user')
        self.client.login(username='test_user', password='test_user')
        self.test_file_jpg_a = SimpleUploadedFile("fotoa.jpg", b"file_content")
        self.test_file_jpg_b = SimpleUploadedFile("fotob.jpg", b"file_content")
        self.artikel_obj = Artikel.objects.create(
            judul="judul1",
            deskripsi="desk1",
            foto_artikel=self.test_file_jpg_a
        )
        self.artikel_obj.save()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_form_artikel_url_exist(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=True)
        response = self.client.get(url_form_artikel)
        self.assertEqual(response.status_code, 200)

    def test_form_arikel_url_for_non_opd(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=False)
        response = self.client.get(url_form_artikel)
        self.assertEqual(response.status_code, 302)

    def test_post_form_artikel_open_raw_url_redirect(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=True)
        response = self.client.get(url_post_form_artikel)
        self.assertEqual(response.status_code, 302)

    def test_post_form_lowongan_url_for_non_opd(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=False)
        response = self.client.get(url_post_form_artikel)
        self.assertEqual(response.status_code, 302)

    def test_post_form_artikel_url_for_admin_and_form_is_valid(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=True)
        data_artikel = {
            "judul":"judul_admin",
            "deskripsi":"desk1",
            "foto_artikel":self.test_file_jpg_a
        }
        response = self.client.post(url_post_form_artikel, data_artikel)
        self.assertTrue(Artikel.objects.filter(judul="judul_admin").exists())
        self.assertEqual(response.status_code, 302)

    def test_post_form_artikel_url_not_admin_and_form_is_valid(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=False)
        data_artikel = {
            "judul":"judul_admin",
            "deskripsi":"desk1",
            "foto_artikel":self.test_file_jpg_a
        }
        response = self.client.post(url_post_form_artikel, data_artikel)
        self.assertFalse(Artikel.objects.filter(judul="judul_admin").exists())
        self.assertEqual(response.status_code, 302)

    def test_update_form_artikel_url_for_non_opd(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=False)
        response = self.client.get(url_update_form_artikel+"111/")
        self.assertEqual(response.status_code, 302)

    def test_update_form_artikel_url_for_admin_and_form_not_is_valid(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=True)
        id_artikel = str(self.artikel_obj.id)
        response = self.client.get(url_update_form_artikel+id_artikel+"/")
        self.assertEqual(response.status_code, 200)

    def test_update_form_artikel_url_for_admin_and_form_is_valid(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=True)
        id_artikel = self.artikel_obj.id
        data_artikel = {
            "id":id_artikel,
            "judul":"judul_update",
            "deskripsi":"desk1",
            "foto_artikel":self.test_file_jpg_b
        }
        url_update = url_update_form_artikel+str(id_artikel)+"/"
        response = self.client.post(url_update, data_artikel)
        self.assertTrue(Artikel.objects.filter(judul="judul_update").exists())
        self.assertEqual(response.status_code, 302)
    
    def test_url_update_is_not_exist(self):
        Account.objects.filter(pk=self.user.id).update(is_admin=True)
        id_artikel = 123456
        data_artikel = {
            "id":id_artikel,
            "judul":"test_error",
            "deskripsi":"desk1",
            "foto_artikel":self.test_file_jpg_b
        }
        url_update = url_update_form_artikel+str(id_artikel)+"/"
        response = self.client.post(url_update, data_artikel)
        self.assertFalse(Artikel.objects.filter(judul="test_error").exists())
        self.assertEqual(response.status_code, 302)

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ArtikelReadTest(TestCase):
    def setUp(self):
        self.test_file_jpg1 = SimpleUploadedFile("fotosatu.jpg", b"file_content")
        self.test_file_jpg2 = SimpleUploadedFile("fotodua.jpg", b"file_content")
        self.artikel1 = Artikel.objects.create(
            judul='judulsatu',
            deskripsi='deskripsisatu',
            foto_artikel=self.test_file_jpg1
        )
        self.artikel2 = Artikel.objects.create(
            judul='juduldua',
            deskripsi='deskripsidua',
            foto_artikel=self.test_file_jpg2
        )
        self.artikel1.save()
        self.artikel2.save()
        self.all_other_article_test = Artikel.objects.all().exclude(pk=self.artikel1.pk)
        self.client = Client()
        self.article_one_url = '/artikel/{}/'.format(self.artikel1.pk)
        self.article_two_url = '/artikel/{}/'.format(self.artikel2.pk)
        self.response_read_article = self.client.get(self.article_one_url)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_get_all_other_article_query_in_article_read_should_return_all_articles_except_article_being_read(self):
        self.assertEqual(list(self.all_other_article_test),
                         list(self.response_read_article.context['all_other_article'])
                         )

    def test_get_all_other_article_query_in_article_read_has_article_should_not_return_empty_list(self):
        self.assertNotEqual([], list(self.response_read_article.context['all_other_article']))

    def test_get_all_other_article_query_no_article_in_db_in_article_read_should_not_return_empty_list(self):
        Artikel.objects.all().delete()

        self.assertEqual([], list(self.client.get(self.article_one_url).context['all_other_article']))

    def test_get_article_by_pk_in_article_read_should_return_correct_article(self):
        self.assertEqual(self.artikel1, self.response_read_article.context['artikel'])

    def test_get_article_by_pk_in_article_read_should_not_return_wrong_article(self):
        self.assertNotEqual(self.artikel2, self.response_read_article.context['artikel'])

    def test_access_correct_article_should_not_return_error_true(self):
        self.assertFalse(self.response_read_article.context['error'])

    def test_access_wrong_article_should_return_error_true(self):
        self.assertTrue(self.client.get('/artikel/999/').context['error'])

    def test_access_article_page_should_return_200(self):
        self.assertEqual(200, self.response_read_article.status_code)

    def test_access_wrong_article_should_return_200(self):
        self.assertEqual(200, self.client.get('/artikel/12345/').status_code)
