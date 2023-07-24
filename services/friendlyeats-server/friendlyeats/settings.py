import os

from dynaconf import Dynaconf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings = Dynaconf(load_dotenv=True, envvar_prefix=False)

DEFAULT_TIMEZONE = "UTC"

# Application environment
APP_ENV = settings.APP_ENV

# JWT
SECRET_KEY = settings.SECRET_KEY

# Sentry
SENTRY_DSN = settings.SENTRY_DSN

# GCP
PROJECT_ID = "friendlyeats-eadaa"
