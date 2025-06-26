from flask import Flask, render_template, request, jsonify
import os, requests
from datetime import date
from . import app
from .logic import verify_recaptcha

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = request.form
        token = form.get("g-recaptcha-response")

        if not verify_recaptcha(token):
            return jsonify(success=False, message="CAPTCHA verification failed.")

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

        # Simulated backend processing
        print("=== New Bootcamp Application ===")
        for k, v in data.items():
            print(f"{k}: {v}")
        print("================================")

        return jsonify(success=True)

    return render_template("index.html", today=date.today())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        token = form.get("g-recaptcha-response")

        if not verify_recaptcha(token):
            return jsonify(success=False, message="CAPTCHA verification failed.")

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

        # Simulated backend processing
        print("=== New Bootcamp Application ===")
        for k, v in data.items():
            print(f"{k}: {v}")
        print("================================")

        return jsonify(success=True)

    return render_template("register.html", today=date.today())
