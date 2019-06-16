'''
Separated the settings for production and development environments.
'''

env = 'dev'

if env == 'dev':
    from .settings_dev import *
elif env == 'prod':
    from .settings_prod import *
else:
    print('Incorrect environment specified in settings.py. Specified env = {}'.format(env))
