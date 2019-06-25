from settings.common import *
from libs.aws.get_secrets import get_db_details

db_details = get_db_details("ar_replica")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "news",
        "USER": db_details["username"],
        "PASSWORD": db_details["password"],
        "HOST": "automatic-review-staging-replica.cugtl68vtrxy.eu-central-1.rds.amazonaws.com",
        "PORT": "5432",
    }
}

ALLOWED_HOSTS = [
    "a2c55cadd8c1f11e9860a0215658c8a6-6be0eabc0a5ca0fa.elb.eu-central-1.amazonaws.com",
    "localhost",
    "3.121.157.212"
]

DEBUG = False