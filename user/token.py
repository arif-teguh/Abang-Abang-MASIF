import secrets

def generate_user_token():
    return secrets.token_urlsafe(16)
