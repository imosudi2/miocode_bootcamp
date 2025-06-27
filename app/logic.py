import requests, time

from app import app




def verify_recaptcha(token, RECAPTCHA_SECRET_KEY):
    print(f"Using RECAPTCHA_SECRET_KEY: {RECAPTCHA_SECRET_KEY}"); time.sleep(300)
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
        print("reCAPTCHA result:", result)  # ← debug
        return result.get('success', False)
    except Exception as e:
        print("reCAPTCHA error:", e)
        return False
