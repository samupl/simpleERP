"""
Django settings for simpleERP project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import configparser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_db = configparser.ConfigParser()
config_db.read(os.path.join(BASE_DIR, 'conf', 'database.conf'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'da44gn_oa86s)6l0v7mc9(z_)y2&vb&&%i1$5+6$ya+4-ou38k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'True':
    DEBUG = True

if DEBUG:
    SSLIFY_DISABLE = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party apps
    'django_countries',
    # Local project apps
    'apps.contacts',
    'apps.invoices',
    'apps.download',
    'apps.ledger',
    'apps.costs',
)

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'simpleERP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'simpleERP.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config_db.get('database', 'engine', fallback='django.db.backends.mysql'),
        'NAME': config_db.get('database', 'name'),
        'USER': config_db.get('database', 'user'),
        'PASSWORD': config_db.get('database', 'password'),
        'HOST': config_db.get('database', 'host'),
        'PORT': config_db.get('database', 'port'),
        'TEST': {
            'CHARSET': "utf8",
            'COLLATION': "utf8_general_ci",
        }
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'pl'
LANGUAGES = [
    ('pl', 'Polski'),
    ('en', 'English'),
]
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'media')
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'upload/')
MEDIA_URL = '/download/'

STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
