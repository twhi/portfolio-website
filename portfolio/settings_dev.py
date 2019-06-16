"""
DEV ENVIRONMENT SETTINGS
"""

from .settings_common import *  # IMPORT COMMON SETTINGS

DEBUG = True

ALLOWED_HOSTS = []

# Dev database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'portfoliodb',
        'USER': 'postgres',
        'PASSWORD': '***REMOVED***',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# email server details
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # only in dev environment
