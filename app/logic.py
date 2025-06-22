import requests

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

