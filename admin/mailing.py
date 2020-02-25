import re

from django.core import mail



def send_verification_email(verification_url, recipient_email):
    email_validator = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(email_validator, recipient_email):
        mail.send_mail(
            'Verifikasi OPD',
            'Berikut link untuk verifikasi email untuk akun OPD: '
            + verification_url,
            'admin@masif.com',
            [recipient_email]
        )
    else:
        raise ValueError("Email not valid")
