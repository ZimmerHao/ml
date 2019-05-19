from settings.common import *

ALLOWED_HOSTS = ['news.k8s.internal']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yunti',
        'USER': 'hjm',
        'PASSWORD': 'hjm2016',
        'HOST': '192.168.31.103',
        'PORT': '5432',
    }
}

REDIS_HOST = "192.168.31.101"
REDIS_PORT = 6379