from flask import Flask, render_template, request, redirect, flash, url_for
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Replace this with your actual reCAPTCHA secret key from Google
RECAPTCHA_SECRET_KEY = 'YOUR_SECRET_KEY_HERE'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form fields
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        course = request.form.get('course')
        level = request.form.get('level')
        location = request.form.get('location')
        how_did_you_hear = request.form.get('how_did_you_hear')
        motivation = request.form.get('motivation')
        recaptcha_token = request.form.get('g-recaptcha-response')

        # reCAPTCHA verification
        if not verify_recaptcha(recaptcha_token):
            flash('CAPTCHA verification failed. Please try again.')
            return redirect(url_for('index'))

        # Simulated data processing (e.g., save to DB or CSV)
        print("New Registration:")
        print(f"Full Name: {fullname}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Course: {course}")
        print(f"Level: {level}")
        print(f"Location: {location}")
        print(f"Heard About Us: {how_did_you_hear}")
        print(f"Motivation: {motivation}")
        print("------")

        flash('Application submitted successfully! We will contact you shortly.')
        return redirect(url_for('index'))

    return render_template('index.html')


def verify_recaptcha(token):
    """Verify reCAPTCHA token with Google."""
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

