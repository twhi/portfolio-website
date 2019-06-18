"""
Django settings for portfolio project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

env = 'prod'

if env == 'dev':
    try:
        from .settings_dev import *
    except Exception as e:
        print(e)
    print('Using development environment settings.')
else:
    try:
        from .settings_prod import *
    except Exception as e:
        print(e)
    print('Using production environment settings.')
