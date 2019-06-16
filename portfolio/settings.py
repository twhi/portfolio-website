'''
Separated the settings for production and development environments.
'''

env = 'prod'

if env == 'dev':
    try:
        from .settings_dev import *
    except Exception as e:
        print(e)
    print('Using development environment settings.')
elif env == 'prod':
    try:
        from .settings_prod import *
    except Exception as e:
        print(e)
    print('Using production environment settings.')
else:
    print('Incorrect environment specified in settings.py. Specified env = {}'.format(env))
