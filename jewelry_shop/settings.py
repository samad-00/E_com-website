"""
Django settings for jewelry_shop project.

This file contains all the configuration settings for our Django website.
Each setting controls different aspects of how the website works.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This tells Django where our project files are located
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# This is like a password for your Django app - keep it secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-change-this')

# SECURITY WARNING: don't run with debug turned on in production!
# Debug = True shows detailed error pages (good for development)
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# List of allowed website addresses that can access this site
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []


# Application definition
# These are all the apps (features) that our website uses

INSTALLED_APPS = [
    # Built-in Django apps (these come with Django)
    'django.contrib.admin',        # Admin panel for managing data
    'django.contrib.auth',         # User authentication (login/logout)
    'django.contrib.contenttypes', # Content type framework
    'django.contrib.sessions',     # Session management
    'django.contrib.messages',     # Message framework for notifications
    'django.contrib.staticfiles',  # Static files (CSS, JS, images)
    
    # Our custom apps (features we built for our jewelry store)
    'store',                       # Main store functionality
    'users',                       # User registration and profiles
    
    # Third-party apps (external packages we installed)
    'crispy_forms',               # Makes forms look better
    'crispy_bootstrap5',          # Bootstrap 5 styling for forms
    'payments',                   # Payment processing
]

# Middleware - These run on every request to process data
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',         # Security features
    'django.contrib.sessions.middleware.SessionMiddleware',  # Handle user sessions
    'django.middleware.common.CommonMiddleware',             # Common web features
    'django.middleware.csrf.CsrfViewMiddleware',            # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Message handling
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Clickjacking protection
]

# URL configuration
ROOT_URLCONF = 'jewelry_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.cart_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'jewelry_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms settings
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Login URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Stripe Settings
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')  # set in environment for production

# Email Settings - Configuration for sending emails
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# Inventory
LOW_STOCK_THRESHOLD = int(os.environ.get('LOW_STOCK_THRESHOLD', 5))

# Twilio SMS settings
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_FROM_NUMBER = os.environ.get('TWILIO_FROM_NUMBER', '')

# Live chat widget id (Tawk.to) - Sign up at https://www.tawk.to
# Example ID: '5f7a6c8e1234567890abcdef/default'
TAWKTO_WIDGET_ID = os.environ.get('TAWKTO_WIDGET_ID', '5f7a6c8e1234567890abcdef')

