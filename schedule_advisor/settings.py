"""
Django settings for schedule_advisor project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import sys
from pathlib import Path

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!0)-+y%fukvkpdiq!q35)y9z@zg7f4d)&8x0wr%gzjdrl13r$%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 2
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'schedule-advisor-b-20.herokuapp.com',
    'schedule-advisor-b20.herokuapp.com'
]

# Application definition

INSTALLED_APPS = [
    'scheduling_app.apps.SchedulingAppConfig',
    'bootstrap5',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'future',
    'fixture_magic',
    # Google Authentication

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
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

ROOT_URLCONF = 'schedule_advisor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'schedule_advisor.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# if 'test' in sys.argv:
#     DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3'
#     }


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ACCOUNT SETUP:


# Google Authentication Settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
LOGIN_REDIRECT_URL = 'scheduling_app:accountRedirects'
LOGOUT_REDIRECT_URL = 'scheduling_app:login'
LOGIN_URL = 'scheduling_app:login'

# Additional configuration settings
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
AUTH_USER_MODEL = 'scheduling_app.User'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'django.project.b20@gmail.com'
EMAIL_HOST_PASSWORD = 'fyivwdcekmjuqfoe'
EMAIL_PORT = 587

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            "client_id": "46198671898-e4u3tjtru808tfp99vlnlv63m5dn04fu.apps.googleusercontent.com",
            "secret": "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",
            "key": "",
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}



# Client Id: 46198671898-e4u3tjtru808tfp99vlnlv63m5dn04fu.apps.googleusercontent.com
# Client Secret: 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



try:
    if 'HEROKU' in os.environ:
        import django_heroku
        django_heroku.settings(locals())
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_SECONDS = 180
        SECURE_SSL_REDIRECT = True

        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True
        DEBUG = False
except ImportError:
    found = False
