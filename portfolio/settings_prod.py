"""
PROD ENVIRONMENT SETTINGS
"""

from .settings_common import *  # IMPORT COMMON SETTINGS

DEBUG = False

ALLOWED_HOSTS = ['safe-woodland-45163.herokuapp.com']  # prod

# AWS S3 bucket credentials
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_BUCKET_REGION')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_BUCKET_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_BUCKET_SECRET_ACCESS_KEY')

# AWS S3 bucket settings
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
        'NAME': os.environ.get('PROD_DB_NAME'),
        'USER': os.environ.get('PROD_DB_USER'),
        'PASSWORD': os.environ.get('PROD_DB_PASSWORD'),
        'HOST': os.environ.get('PROD_DB_HOST'),
        'PORT': 5432,
    }
}

# email server details
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('PROD_EMAIL_HOST')
EMAIL_POST = os.environ.get('PROD_EMAIL_POST')
EMAIL_HOST_USER = os.environ.get('PROD_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('PROD_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('PROD_DEFAULT_FROM_EMAIL')
