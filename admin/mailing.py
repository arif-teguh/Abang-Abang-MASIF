from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.validators import ValidationError

def send_verification_email(verification_url, recipient_email):
    try:
        validate_email(recipient_email)
        send_mail(
            'Verifikasi OPD',
            'Berikut link untuk verifikasi email untuk akun OPD: '
            + verification_url,
            'admin@masif.com',
            [recipient_email]
        )
    except ValidationError:
        raise ValueError("Email not valid")
