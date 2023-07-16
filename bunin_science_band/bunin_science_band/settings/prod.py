from .base import *
import os
from dotenv import find_dotenv
from dotenv import load_dotenv

env_file = find_dotenv(".env.prod")
load_dotenv(env_file)

DEBUG = int(os.getenv("DEBUG"))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(" ")

ADMINS = (("admin", os.getenv("ADMIN_EMAIL")),)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}

REDIS_URL = os.getenv("REDIS_URL")
CACHE_LOCATION = REDIS_URL
CACHES["default"]["LOCATION"] = REDIS_URL

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
