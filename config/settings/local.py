from .base import *
import os
import environ

env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, "local.env")
env.read_env(env_file)
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.get_value("DEBUG",bool)

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
# sqliteを使う場合は以下をコメントアウトする。
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {"default": env.db()}
STATIC_URL = env("STATIC_URL")
LANGUAGE_CODE = env("LANGUAGE_CODE")
TIME_ZONE = env("TIME_ZONE")
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST")