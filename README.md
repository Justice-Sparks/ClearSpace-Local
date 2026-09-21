ClearSpace Local

A lead-generation marketplace connecting Colorado Springs contractors and tradespeople with local customers. Contractors apply through an onboarding flow, an admin reviews and approves them, and approved contractors receive an emailed link to set their password and access their dashboard.

Status: Not currently deployed. It previously ran in production on AWS (architecture below).

Tech stack
Backend: Python, Django 6.0
Database: PostgreSQL on AWS RDS/Aurora in production; SQLite for local development
Serving: Gunicorn as a systemd service behind Nginx
Hosting: AWS EC2
Libraries: django-recaptcha, django-ratelimit, python-dotenv, Pillow, psycopg2
Project structure
App	Responsibility
marketplace	Public site: homepage, service pages, cities, service categories, clients, and customer service requests
onboarding	Contractor signup requests and the admin approval workflow
contractorportal	Custom user model, contractor profiles, and the login-protected contractor dashboard
config	Project settings, URL routing, WSGI/ASGI entry points
Contractor onboarding flow
A contractor submits a signup request (business details, service categories, service area, licensing).
The site notifies the admin team by email.
An admin approves the request from the Django admin with a custom action, which creates the contractor's account with an unusable password.
The contractor is emailed a one-time link, built with Django's token generator, to set their password.
After logging in, the contractor is routed to their dashboard.
Security
Bot protection on the public signup form, layered:
reCAPTCHA v3
Per-IP rate limiting with django-ratelimit
A hidden honeypot field; submissions that fill it are silently discarded
Nginx limit_req_zone rate limiting at the proxy layer
CSRF protection on all forms
No secrets in code. Every credential and environment-specific value is read from environment variables, so the same settings.py runs in every environment.
Configuration

Settings load from a .env file in the project root (via python-dotenv) or from the process environment. With no database variables set, the app falls back to SQLite.

Variable	Purpose
DJANGO_SECRET_KEY	Django secret key (required in production)
DJANGO_DEBUG	True or False
DJANGO_ALLOWED_HOSTS	Comma-separated hostnames
CSRF_TRUSTED_ORIGINS	Comma-separated origins, e.g. https://example.com
DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT	PostgreSQL connection; all but port must be set to use Postgres
RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY	Google reCAPTCHA v3 keys
EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL	Outgoing mail (Gmail SMTP)
CONTRACTOR_NOTIFY_EMAIL_1	Address notified of new signup requests
RATELIMIT_IP_META_KEY	Request header holding the client IP when behind a proxy
Running locally

Requires Python 3.12+.

bash
git clone https://github.com/Justice-Sparks/ClearSpace-Local.git
cd ClearSpace-Local
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Then open http://127.0.0.1:8000. The admin is at /admin/.

Production architecture
Browser ──> Nginx (TLS, rate limiting, static files)
              └──> Gunicorn (systemd service) ──> Django
                                                    └──> PostgreSQL (AWS RDS/Aurora)

In production, systemd loads credentials into Gunicorn through an EnvironmentFile. Management commands must be run with the same database variables exported; otherwise Django silently falls back to SQLite and writes to the wrong database.
