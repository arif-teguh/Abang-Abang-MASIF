import secrets

def generate_opd_token():
    return secrets.token_urlsafe(16)
