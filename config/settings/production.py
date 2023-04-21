from .base import *

import os
import io
import environ
import google.auth
from google.cloud import secretmanager
import json

# Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass
env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(env_file):
    # Use a local secret file, if provided

    env.read_env(env_file)
elif os.environ.get("TRAMPOLINE_CI", None):

    # Create local settings if running with CI, for unit testing
    placeholder = (
        f"SECRET_KEY=a\n"
        f"DATABASE_URL=sqlite://{os.path.join(BASE_DIR, 'db.sqlite3')}"
    )
    env.read_env(io.StringIO(placeholder))
# [END_EXCLUDE]
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
    d = json.loads(payload)
    # env.read_env(io.StringIO(payload))
else:
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")
# [END gaestd_py_django_secret_config]

SECRET_KEY = d["secrets"]["SECRET_KEY"]

DEBUG = os.environ.get("DEBUG") == "True"
# [START gaestd_py_django_csrf]
# SECURITY WARNING: It's recommended that you use this when
# running in production. The URL will be known once you first deploy
# to App Engine. This code takes the URL and converts it to both these settings formats.
CSRF_TRUSTED_ORIGINS =  [os.environ.get('CSRF_TRUSTED_ORIGINS')]
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "False") == "True"
# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]
# [END gaestd_py_django_csrf]
# Database
# [START db_setup]
# [START gaestd_py_django_database_config]
# Use django-environ to parse the connection string
DATABASES = {
    'default': {
        'ENGINE': d["secrets"]["DB"]["ENGINE"],
        'HOST': d["secrets"]["DB"]["HOST"],
        'NAME': d["secrets"]["DB"]["NAME"],
        'USER': d["secrets"]["DB"]["USER"],
        'PASSWORD': d["secrets"]["DB"]["PASSWORD"],
        'PORT': d["secrets"]["DB"]["PORT"],
    }
}

# If the flag as been set, configure to use proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = os.environ.get("DB_HOST")
    DATABASES["default"]["PORT"] = int(os.environ.get("DB_PORT"))

# [END gaestd_py_django_database_config]
# [END db_setup]

# Use a in-memory sqlite3 database when testing in CI systems
# TODO(glasnt) CHECK IF THIS IS REQUIRED because we're setting a val above
if os.getenv("TRAMPOLINE_CI", None):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "ja")
TIME_ZONE = os.environ.get("TIME_ZONE", "Asia/Tokyo")
CORS_ORIGIN_WHITELIST = [os.environ.get("CORS_ORIGIN_WHITELIST")]

# django < 4.2
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
# django >= 4.2
STORAGES = {"default": "storages.backends.gcloud.GoogleCloudStorage"}

GS_BUCKET_NAME = d["secrets"]["GS_BUCKET_NAME"]

# django < 4.2
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
# django >= 4.2
STORAGES = {"staticfiles": "storages.backends.gcloud.GoogleCloudStorage"}

STATIC_URL = "/static/"
GS_DEFAULT_ACL = "publicRead"