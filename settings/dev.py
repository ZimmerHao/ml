from settings.common import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'news',
        'USER': 'postgres',
        'HOST': '192.168.50.20',
        'PORT': '5432',
    }
}
