from .base import *
import os
from dotenv import find_dotenv
from dotenv import load_dotenv

env_file = find_dotenv(".env.local")
load_dotenv(env_file)

DEBUG = int(os.getenv("DEBUG"))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(" ")

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DATABASE_ENGINE"),
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "PORT": os.getenv("DATABASE_PORT"),
        # "ATOMIC_REQUESTS": True
    }
}
