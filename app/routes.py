from flask import Flask, render_template, request, redirect, flash, url_for, jsonify,  session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import HTTPException

import os, time
import sys
from os.path import join, dirname
from dotenv import load_dotenv
import requests
from datetime import date, datetime
from pathlib import Path
import json

from . import app
from .logic import load_applicants, load_users, verify_recaptcha

DATA_PATH = os.path.join(app.root_path, 'data')
os.makedirs(DATA_PATH, exist_ok=True)

file_path = os.path.join(DATA_PATH, 'submissions.json')
questionnaire_file_path = os.path.join(DATA_PATH, 'questionnaire.json')
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
                "agreed_to_terms": form.get("agreeTerms") == "on",
                "start_approval": False
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

                # Check for duplicate email or WhatsApp number
                for existing in submissions:
                    if existing.get("email") == data["email"]:
                        error_message = "An application with this email address already exists."
                        if is_ajax:
                            return jsonify({'success': False, 'message': error_message}), 400
                        else:
                            flash(error_message, "danger")
                            return redirect(url_for('index'))
                    
                    if existing.get("whatsapp") == data["whatsapp"]:
                        error_message = "An application with this WhatsApp number already exists."
                        if is_ajax:
                            return jsonify({'success': False, 'message': error_message}), 400
                        else:
                            flash(error_message, "danger")
                            return redirect(url_for('index'))

                
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

@app.route('/admin/questionnaire')
def admin_questionnaire():
    if 'admin_user' not in session:
        flash("You must be logged in to access the admin questionnaire.")
        return redirect(url_for('admin_login'))
    
    questionnaire_responses = []
    #questionnaire_file_path = questionnaire_file_path #"questionnaire.json"
    
    try:
        if os.path.exists(questionnaire_file_path):
            with open(questionnaire_file_path, "r", encoding="utf-8") as f:
                questionnaire_responses = json.load(f)
    except Exception as e:
        flash(f"Error loading questionnaire responses: {e}")
        print(f"Error loading questionnaire responses: {e}")
    
    return render_template("admin_questionnaire.html", 
                         questionnaire_responses=questionnaire_responses, 
                         admin_user=session.get('admin_user'))
    
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

@app.route('/admin/questionnaire/<email>')
def view_questionnaire_by_email(email):
    if 'admin_user' not in session:
        flash("You must be logged in to access questionnaire details.")
        return redirect(url_for('admin_login'))
    
    questionnaire_responses = []
    #questionnaire_file_path = "questionnaire.json"
    
    if os.path.exists(questionnaire_file_path):
        with open(questionnaire_file_path, "r", encoding="utf-8") as f:
            questionnaire_responses = json.load(f)

    questionnaire = next((q for q in questionnaire_responses if q["email"] == email), None)
    if not questionnaire:
        abort(404)

    return render_template("questionnaire_detail.html", questionnaire=questionnaire)

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

@app.after_request
def apply_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=()'
    return response

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    applicant_details = None
    
    if request.method == 'POST':
        # Check if this is an email lookup request
        if 'lookup_email' in request.form:
            applicant_email = request.form.get('lookup_email')
            if applicant_email:
                applicant_details = load_applicants(applicant_email)
                if not applicant_details:
                    flash('No applicant found with this email address.', 'danger')
                elif applicant_details.get("start_approval") != True:
                    flash('You are not approved to commence the training! Make the initial deposit payment.', 'warning')
                    applicant_details = None  # Reset to show email form again
            else:
                flash('Please enter an email address.', 'warning')
        
        # Check if this is a questionnaire submission
        elif 'full_name' in request.form:
            # Check if this email/whatsapp already exists in questionnaire submissions
            email = request.form.get('email')
            phone = request.form.get('phone')
            
            # Load existing questionnaire submissions
            file_path = questionnaire_file_path  # 'data/questionnaire.json'
            existing = []
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        existing = json.load(f)
                except:
                    existing = []
            
            # Check for duplicate email or phone/whatsapp
            for submission in existing:
                if (submission.get('email') == email or 
                    submission.get('phone') == phone):
                    # Check if the existing submission has start_approval = true
                    if submission.get('start_approval') == True:
                        flash('Your information has been submitted earlier, contact the administrator for a request to update earlier submission.', 'info')
                        return redirect(url_for('questionnaire'))
            
            # Extract data for new submission
            data = {
                "full_name": request.form.get('full_name'),
                "email": email,
                "phone": phone,
                "program": request.form.get('program'),
                "os": request.form.get('os'),
                "python_installed": request.form.get('python_installed'),
                "cli_familiarity": request.form.get('cli_familiarity'),
                "tools_used": request.form.getlist('tools_used'),  # Handle multiple checkboxes
                "specs": request.form.get('specs'),
                "goals": request.form.get('goals'),
                "project_interest": request.form.get('project_interest'),
                "challenges": request.form.get('challenges'),
                "submitted_at": datetime.utcnow().isoformat(),
                "start_approval": True
            }

            # Save to JSON (append)
            existing.append(data)
            with open(file_path, 'w') as f:
                json.dump(existing, f, indent=2)

            flash('Questionnaire submitted successfully!', 'success')
            return redirect(url_for('questionnaire'))

    return render_template('questionnaire.html', applicant_details=applicant_details)

"""
# 400 - Bad Request
@app.errorhandler(400)
def bad_request(error):
    flash("Bad request. Please check your input and try again.", "danger")
    return redirect(request.referrer or url_for('index'))

# 401 - Unauthorized
@app.errorhandler(401)
def unauthorized(error):
    flash("You must be logged in to access this page.", "warning")
    return redirect(url_for('admin_login'))

# 403 - Forbidden
@app.errorhandler(403)
def forbidden(error):
    flash("You do not have permission to access this page.", "warning")
    return redirect(url_for('index'))

# 404 - Not Found
@app.errorhandler(404)
def not_found(error):
    flash("The page you’re looking for doesn’t exist.", "warning")
    return redirect(url_for('index'))

# 405 - Method Not Allowed
@app.errorhandler(405)
def method_not_allowed(error):
    flash("Invalid request method.", "danger")
    return redirect(url_for('index'))

# 408 - Request Timeout
@app.errorhandler(408)
def request_timeout(error):
    flash("Request timed out. Please try again.", "warning")
    return redirect(url_for('index'))

# 413 - Payload Too Large
@app.errorhandler(413)
def payload_too_large(error):
    flash("Uploaded file is too large.", "danger")
    return redirect(request.referrer or url_for('index'))

# 429 - Too Many Requests
@app.errorhandler(429)
def too_many_requests(error):
    flash("Too many requests. Please slow down.", "warning")
    return redirect(url_for('index'))

# 500 - Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    flash("An unexpected error occurred. Our team has been notified.", "danger")
    return redirect(url_for('index'))

# 502 - Bad Gateway
@app.errorhandler(502)
def bad_gateway(error):
    flash("Bad gateway error. Please try again later.", "danger")
    return redirect(url_for('index'))

# 503 - Service Unavailable
@app.errorhandler(503)
def service_unavailable(error):
    flash("Service temporarily unavailable. Please check back soon.", "warning")
    return redirect(url_for('index'))

# Catch-all handler for unhandled exceptions (fallback)
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    flash("A system error occurred. Please try again or contact support.", "danger")
    return redirect(url_for('index'))"""
