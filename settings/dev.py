from settings.common import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "data_service_dev",
        "USER": "automatic_review_replica_staging",
        "PASSWORD": "mypass",
        "HOST": "segment.cugtl68vtrxy.eu-central-1.rds.amazonaws.com",
        "PORT": "5432",
    }
}

ALLOWED_HOSTS = [
    "localhost",
    ".dp.com",
    ".deepvega.com",
    ".svc.cluster.local"
]

# DEBUG = False

os.environ['USE_S3'] = "TRUE"
# os.environ['USE_S3'] = "FALSE"
USE_S3 = os.getenv('USE_S3') == 'TRUE'

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = "data-k8s-public-staticfiles"
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'frontend'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# else:
#     STATIC_URL = '/frontend/'
#     STATIC_ROOT = os.path.join(BASE_DIR, 'frontend')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'frontend'),)


SESSION_COOKIE_DOMAIN="deepvega.com"
SESSION_COOKIE_NAME = 'deepvegasessionid'