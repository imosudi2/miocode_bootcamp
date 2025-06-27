from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
import os, time
import sys
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from datetime import date


from . import app
from .logic import verify_recaptcha


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# reCAPTCHA keys
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
recaptcha_site_key = os.environ.get("RECAPTCHA_SITE_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if this is an AJAX request (multiple ways to detect)
        is_ajax = (
            request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
            request.headers.get('Content-Type', '').startswith('multipart/form-data') and 
            'X-Requested-With' in request.headers or
            request.is_json or
            'ajax' in request.args
        )
        
        # Debug logging
        print(f"Request headers: {dict(request.headers)}")
        print(f"Is AJAX: {is_ajax}")
        
        form = request.form
        
        # reCAPTCHA token verification
        recaptcha_token = form.get('g-recaptcha-response')
        if not verify_recaptcha(recaptcha_token, RECAPTCHA_SECRET_KEY):
            error_message = "CAPTCHA verification failed. Please try again."
            print(f"reCAPTCHA failed for token: {recaptcha_token}")
            
            if is_ajax:
                response = jsonify({
                    'success': False,
                    'message': error_message
                })
                response.headers['Content-Type'] = 'application/json'
                return response, 400
            else:
                flash(error_message)
                return redirect(url_for('index'))

        # Retrieve and validate form data
        try:
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
                "agreed_to_terms": form.get("agreeTerms") == "on"

            }

            # Basic validation
            required_fields = [
                'first_name', 'last_name', 'email', 'phone', 'whatsapp',
                'contact_method', 'program', 'schedule', 'start_date',
                'experience', 'goals', 'payment_plan'
            ]
            data['agreed_to_terms'] = data['agreed_to_terms'] is True or data['agreed_to_terms'] == 'on'


            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                error_message = f"Missing required fields: {', '.join(missing_fields)}"
                if is_ajax:
                    response = jsonify({
                        'success': False,
                        'message': error_message
                    })
                    response.headers['Content-Type'] = 'application/json'
                    return response, 400
                else:
                    flash(error_message)
                    return redirect(url_for('index'))

            # Simulate backend processing (e.g., DB insert or email send)
            print("=== New Bootcamp Application ===")
            for key, value in data.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            print("================================")

            # Success response
            success_message = "Application submitted successfully! We will contact you shortly."
            
            if is_ajax:
                response = jsonify({
                    'success': True,
                    'message': success_message
                })
                response.headers['Content-Type'] = 'application/json'
                return response, 200
            else:
                flash(success_message)
                return redirect(url_for('index'))
                
        except Exception as e:
            # Handle unexpected errors
            error_message = "An error occurred while processing your application. Please try again."
            print(f"Error processing form: {str(e)}")  # Log the actual error
            
            if is_ajax:
                response = jsonify({
                    'success': False,
                    'message': error_message
                })
                response.headers['Content-Type'] = 'application/json'
                return response, 500
            else:
                flash(error_message)
                return redirect(url_for('index'))
    
    # GET request - render the form
    return render_template('index.html', today=date.today(), recaptcha_site_key=recaptcha_site_key)


@app.route('/registert', methods=['GET', 'POST'])
def registert():
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

    return render_template("register.html", today=date.today(), recaptcha_site_key=recaptcha_site_key)

