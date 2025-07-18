import requests, time, os
from werkzeug.security import check_password_hash, generate_password_hash
import json

from app import app




def verify_recaptcha(token, RECAPTCHA_SECRET_KEY):
    #print(f"Using RECAPTCHA_SECRET_KEY: {RECAPTCHA_SECRET_KEY}"); time.sleep(300)
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


def load_users():
    try:
        users_path = os.path.join(app.root_path, 'data', 'users.json')
        with open(users_path, 'r', encoding='utf-8') as f:
            raw_users = json.load(f)
            # Hash passwords at runtime if not already hashed
            return [
                {
                    "username": u["username"],
                    "password_hash": generate_password_hash(u["password"]) if not u["password"].startswith("pbkdf2:") else u["password"]
                }
                for u in raw_users
            ]
    except Exception as e:
        print(f"Error loading users: {e}")
        return []

def load_applicants(applicant_email):
    try:
        applicants_path = os.path.join(app.root_path, 'data', 'submissions.json')
        with open(applicants_path, 'r', encoding='utf-8') as f:
            raw_applicants = json.load(f)
            
            # Search for the specific applicant by email
            for applicant in raw_applicants:
                if applicant.get("email") == applicant_email:
                    return {
                        "email": applicant["email"],
                        "first_name": applicant["first_name"],
                        "last_name": applicant["last_name"],
                        "whatsapp": applicant["whatsapp"],
                        "start_approval": applicant["start_approval"]
                    }
            
            # Return None if applicant not found
            return None
            
    except Exception as e:
        print(f"Error loading applicant: {e}")
        return None
    