"""
PROD ENVIRONMENT SETTINGS
"""

from .settings_common import *  # IMPORT COMMON SETTINGS

DEBUG = False

ALLOWED_HOSTS = ['safe-woodland-45163.herokuapp.com']  # prod

# AWS S3 bucket credentials
AWS_STORAGE_BUCKET_NAME = 'django-portfolio-tom-1991'
AWS_S3_REGION_NAME = 'us-east-2'  # e.g. us-east-2
AWS_ACCESS_KEY_ID = '***REMOVED***'
AWS_SECRET_ACCESS_KEY = '***REMOVED***'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_DEFAULT_ACL = None
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

# Production Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '***REMOVED***',
        'USER': '***REMOVED***',
        'PASSWORD': '***REMOVED***',
        'HOST': '***REMOVED***',
        'PORT': '5432',
    }
}

# email server details
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_POST = 587
EMAIL_HOST_USER = '***REMOVED***'
EMAIL_HOST_PASSWORD = '***REMOVED***'
DEFAULT_FROM_EMAIL = 'webmaster@localhost'