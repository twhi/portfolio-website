"""
DEV ENVIRONMENT SETTINGS
"""
import os
from .settings_common import *  # IMPORT COMMON SETTINGS

DEBUG = True

ALLOWED_HOSTS = []

# Dev database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DEV_DB_NAME'),      # DEV_DB_NAME
        'USER': os.environ.get('DEV_DB_USER'),         # DEV_DB_USER
        'PASSWORD': os.environ.get('DEV_DB_PASSWORD'),     # DEV_DB_PASSWORD
        'HOST': os.environ.get('DEV_DB_HOST'),        # DEV_DB_HOST
        'PORT': '5432',
    }
}

# email server details
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # only in dev environment
