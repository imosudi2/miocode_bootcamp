from flask import Flask, render_template, request, redirect, flash, url_for
import os
import requests
from datetime import date


from . import app
from .logic import verify_recaptcha


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



