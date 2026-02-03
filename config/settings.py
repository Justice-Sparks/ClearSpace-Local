from pathlib import Path
import os

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env if present (local and EC2)
load_dotenv(BASE_DIR / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
# Local can still use a default, but production should provide DJANGO_SECRET_KEY in .env
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-local-dev-only-change-me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

# Allowed hosts
# Local example: DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
# Prod example:  DJANGO_ALLOWED_HOSTS=your-domain.com,EC2_PUBLIC_IP
ALLOWED_HOSTS = [h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom Apps
    'marketplace',
    'onboarding',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# Local defaults to sqlite unless DB_* env vars exist
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")

if all([DB_NAME, DB_USER, DB_PASSWORD, DB_HOST]):
    # Production / Postgres (RDS)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }
else:
    # Local fallback: sqlite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Where collectstatic outputs (needed for Nginx in prod)
STATIC_ROOT = BASE_DIR / "static"

# For local dev only (optional). In production, you can keep this, it won’t break anything.
STATICFILES_DIRS = [
    BASE_DIR / 'marketplace' / 'static',
]

# CSRF trusted origins (important once you're on HTTPS + domain)
# Example: CSRF_TRUSTED_ORIGINS=https://your-domain.com
_csrf = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf.split(",") if o.strip()] 


# EMAIL SETTINGS-------------------------------------------------------------------------------|

# Who the notification emails should go to
CONTRACTOR_SIGNUP_NOTIFY_EMAILS = [
    os.environ.get("CONTRACTOR_NOTIFY_EMAIL_1", ""),  # ! CHANGE EMAIL TO GOOGLE WORKSPACE EMAILS IN .ENV FILE 
    #os.environ.get("CONTRACTOR_NOTIFY_EMAIL_2", ""),
]
# Remove any blanks in case env vars weren't set
CONTRACTOR_SIGNUP_NOTIFY_EMAILS = [e for e in CONTRACTOR_SIGNUP_NOTIFY_EMAILS if e]

# Email config (Google Workspace SMTP)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# ! setup host email in google workspace and assign in (.env file for local) (systemd file on EC2)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")  
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")  # app password recommended

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER) 