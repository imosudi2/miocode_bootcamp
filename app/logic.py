import requests

from app import RECAPTCHA_SECRET_KEY, app

def verify_recaptcha(token):
    # For development, return True to skip verification
    if app.config.get('TESTING', False):
        return True
    
    # Normal reCAPTCHA verification for production
    secret = RECAPTCHA_SECRET_KEY
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={'secret': secret, 'response': token}
    )
    return response.json().get('success', False)

def verify_recaptcha(token):
    """Verify the reCAPTCHA v2 token with Google."""
    if not token:
        return False

    url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': token
    }

    try:
        response = requests.post(url, data=payload)
        result = response.json()
        return result.get('success', False)
    except Exception as e:
        print("reCAPTCHA error:", e)
        return False

def verify_recaptcha_2(token):
    secret = RECAPTCHA_SECRET_KEY
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={'secret': secret, 'response': token}
    )
    return response.json().get('success', False)
