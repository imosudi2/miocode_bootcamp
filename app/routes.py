from flask import Flask, render_template, request, redirect, flash, url_for, jsonify,  session
from werkzeug.security import check_password_hash, generate_password_hash


import os, time
import sys
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from datetime import date, datetime
from pathlib import Path
import json

from . import app
from .logic import load_users, verify_recaptcha

DATA_PATH = os.path.join(app.root_path, 'data')
os.makedirs(DATA_PATH, exist_ok=True)

file_path = os.path.join(DATA_PATH, 'submissions.json')
#sudo chown -R $USER:$USER /home/mosud/Downloads/miocode/miocode_bootcamp/app/data/
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# reCAPTCHA keys
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
recaptcha_site_key = os.environ.get("RECAPTCHA_SITE_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if this is an AJAX request
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
                return jsonify({
                    'success': False,
                    'message': error_message
                }), 400
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
                "education_sublevel": form.get("undergradSublevel"),
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

            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                error_message = f"Missing required fields: {', '.join(missing_fields)}"
                if is_ajax:
                    return jsonify({
                        'success': False,
                        'message': error_message
                    }), 400
                else:
                    flash(error_message)
                    return redirect(url_for('index'))

            # Check terms agreement
            if not data['agreed_to_terms']:
                error_message = "You must agree to the terms and conditions."
                if is_ajax:
                    return jsonify({
                        'success': False,
                        'message': error_message
                    }), 400
                else:
                    flash(error_message)
                    return redirect(url_for('index'))

            # Simulate backend processing (e.g., DB insert or email send)
            print("=== New Bootcamp Application ===")
            for key, value in data.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            print("================================")

            # Save to JSON file with proper error handling
            data["submitted_at"] = datetime.now().isoformat()
            
            try:
                # Ensure the directory exists and has proper permissions
                os.makedirs(DATA_PATH, mode=0o755, exist_ok=True)
                
                # Load existing submissions
                submissions = []
                if os.path.exists(file_path):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            submissions = json.load(f)
                    except (json.JSONDecodeError, FileNotFoundError):
                        submissions = []

                # Add new submission
                submissions.append(data)

                # Write back to file with proper error handling
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(submissions, f, indent=2, ensure_ascii=False)
                
                print(f"Successfully saved submission to {file_path}")
                
            except PermissionError as e:
                print(f"Permission error saving submission: {e}")
                # You might want to save to a different location or handle this differently
                error_message = "Unable to save your application due to server permissions. Please contact support."
                if is_ajax:
                    return jsonify({
                        'success': False,
                        'message': error_message
                    }), 500
                else:
                    flash(error_message)
                    return redirect(url_for('index'))
            except Exception as e:
                print(f"Unexpected error saving submission: {e}")
                error_message = "An error occurred while saving your application. Please try again."
                if is_ajax:
                    return jsonify({
                        'success': False,
                        'message': error_message
                    }), 500
                else:
                    flash(error_message)
                    return redirect(url_for('index'))

            # Success response
            success_message = "Application submitted successfully! We will contact you shortly."
            
            if is_ajax:
                return jsonify({
                    'success': True,
                    'message': success_message
                }), 200
            else:
                flash(success_message)
                return redirect(url_for('index'))
                
        except Exception as e:
            # Handle unexpected errors
            error_message = "An error occurred while processing your application. Please try again."
            print(f"Error processing form: {str(e)}")
            
            if is_ajax:
                return jsonify({
                    'success': False,
                    'message': error_message
                }), 500
            else:
                flash(error_message)
                return redirect(url_for('index'))
    
    # GET request - render the form
    return render_template('index.html', today=date.today(), recaptcha_site_key=recaptcha_site_key)


@app.route('/admin')
def admin_dashboard():
    if 'admin_user' not in session:
        flash("You must be logged in to access the admin dashboard.")
        return redirect(url_for('admin_login'))

    submissions = []
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                submissions = json.load(f)
    except Exception as e:
        flash(f"Error loading submissions: {e}")
        print(f"Error loading submissions: {e}")

    return render_template("admin.html", submissions=submissions, admin_user=session.get('admin_user'))

@app.route('/admin/student/<email>')
def view_student_by_email(email):
    submissions = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            submissions = json.load(f)

    student = next((s for s in submissions if s["email"] == email), None)
    if not student:
        abort(404)

    return render_template("student_detail.html", student=student)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    users = load_users()

    if request.method == 'POST':
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '').strip()

        user = next((u for u in users if u['username'] == username), None)

        if user and check_password_hash(user['password_hash'], password):
            session['admin_user'] = username
            flash(f"Welcome, {username}!")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid username or password.")

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_user', None)
    flash("You have been logged out.")
    return redirect(url_for('admin_login'))


