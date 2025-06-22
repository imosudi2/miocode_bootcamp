from flask import Flask, render_template, request, redirect, flash, url_for
import os
import requests
from datetime import date

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Replace with your actual reCAPTCHA keys
RECAPTCHA_SECRET_KEY = "6LeFlWkrAAAAAC2DmNRzjQqD_9hJ3Y4s84SYHRkF"
RECAPTCHA_SITE_KEY = "6LeFlWkrAAAAAGWAysVIcK9ZhvksD--q_hNW1BrO"

# Make reCAPTCHA site key available in templates
app.jinja_env.globals.update(recaptcha_site_key=RECAPTCHA_SITE_KEY)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = request.form

        # reCAPTCHA token
        recaptcha_token = form.get('g-recaptcha-response')
        if not verify_recaptcha(recaptcha_token):
            flash("CAPTCHA verification failed. Please try again.")
            return redirect(url_for('index'))

        # Retrieve form data
        data = {
            "first_name": form.get("firstName"),
            "last_name": form.get("lastName"),
            "email": form.get("email"),
            "phone": form.get("phone"),
            "whatsapp": form.get("whatsapp"),
            "contact_method": form.get("contactMethod"),
            "address": form.get("address"),
            "program": form.get("program"),
            "schedule": form.get("schedule"),
            "start_date": form.get("startDate"),
            "education": form.get("education"),
            "experience": form.get("experience"),
            "goals": form.get("goals"),
            "payment_plan": form.get("payment"),
            "agreed_to_terms": form.get("agreeTerms")
        }

        # Simulate backend processing (e.g., DB insert or email send)
        print("=== New Bootcamp Application ===")
        for key, value in data.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        print("================================")

        flash("Application submitted successfully! We will contact you shortly.")
        return redirect(url_for('index'))

    return render_template('index.html', today=date.today())


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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

