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
else:
    try:
        from .settings_prod import *
    except Exception as e:
        print(e)
    print('Using production environment settings.')
