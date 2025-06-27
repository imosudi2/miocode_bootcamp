from flask import Flask, render_template, request, redirect, flash, url_for
import os
import requests
from datetime import date
from dotenv import load_dotenv

app = Flask(__name__)
#app.secret_key = os.urandom(24)
print(os.environ.get('FLASK_SECRET_KEY'))
app.secret_key = os.environ.get('FLASK_SECRET_KEY')#, 'super-secret-key')
# reCAPTCHA keys
RECAPTCHA_SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")

# Make reCAPTCHA site key available in templates
app.jinja_env.globals.update(recaptcha_site_key=RECAPTCHA_SITE_KEY)



from .routes import *
