import tempfile
import shutil
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Artikel

MEDIA_ROOT = tempfile.mkdtemp()
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
