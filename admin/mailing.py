from django.core.mail import send_mail, BadHeaderError
from django.core.validators import validate_email
from django.core.validators import ValidationError

def send_verification_email(verification_url, recipient_email, recipient_type):
    subject = 'Verifikasi Akun'
    msg = 'Berikut link untuk verifikasi email untuk akun '+ recipient_type +': '\
        + verification_url
    from_mail = 'admin@masif.com'
    try:
        validate_email(recipient_email)
        send_mail(
            subject,
            msg,
            from_mail,
            [recipient_email]
        )
    except BadHeaderError:
        raise ValidationError('Header Error')
    except ValidationError:
        raise ValidationError("Email not valid")
