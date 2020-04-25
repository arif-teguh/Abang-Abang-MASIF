from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Artikel

class ArtikelModelTest(TestCase):
    def setUp(self):
        self.artikel1 = Artikel.objects.create(
            judul='judul1',
            deskripsi='deskripsi1',
        )
        self.artikel2 = Artikel.objects.create(
            judul='judul2',
            deskripsi='deskripsi2',
        )
        self.artikel1.save()
        self.artikel2.save()

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

    def test_waktu_dibuat_not_none(self):
        self.assertIsNotNone(self.artikel1.waktu_dibuat)
