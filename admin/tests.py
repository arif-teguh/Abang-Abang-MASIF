from django.test import TestCase
from django.core import mail
from . import mailing


class EmailTest(TestCase):
    verification_url = 'masif.com/abcdefg'
    recipient_email = 'test@test.com'

    def test_send_email_sent(self):
        mailing.send_verification_email(
            self.verification_url,
            self.recipient_email)
        self.assertEqual(len(mail.outbox), 1)
        mail.outbox = []

    def test_email_subject(self):
        mailing.send_verification_email(
            self.verification_url,
            self.recipient_email)
        self.assertEqual(mail.outbox[0].subject, 'Verifikasi OPD')
        mail.outbox = []

    def test_email_body(self):
        mailing.send_verification_email(
            self.verification_url,
            self.recipient_email)
        self.assertIn(self.verification_url, mail.outbox[0].body)
        mail.outbox = []

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            mailing.send_verification_email(self.verification_url, "test.com")
            