"""
Django settings for PyRestPdf project.

For more information on this file, see https://docs.djangoproject.com/en/3.2/topics/settings/
For the full list of settings and their values, see https://docs.djangoproject.com/en/3.2/ref/settings/
"""


from pathlib import Path
from os import getenv

from samurai.settings import get_env_databases, get_env_email, get_env_debug_secret_hosts


BASE_DIR = Path(__file__).resolve().parent.parent  # Build paths inside the project like this: BASE_DIR / 'subdir'

# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/
DEBUG, SECRET_KEY, ALLOWED_HOSTS = get_env_debug_secret_hosts()
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Custom, dirty, and specific to this project
WRITE_TOKEN = getenv("WRITE_TOKEN", "k660ax^ktfg(c2#%-d#r%(*9h_p=s$2!puz4zoiyw6wi*ympxs")
READ_TOKEN = getenv("READ_TOKEN", "zko=pb*=5jiba1#2rqj0x$l$!y-%u&@jc%xki-rep5&#(=$#)i")

# Application definition
# _contrib_apps = ["admin", "auth", "contenttypes", "sessions", "messages", "staticfiles"]
_contrib_apps = ["contenttypes"]
_project_apps = ["generated_pdf", "pdf_template"]
INSTALLED_APPS = [*[f"django.contrib.{a}" for a in _contrib_apps], *[f"apps.{a}" for a in _project_apps]]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "middlewares.TokenMiddleware",
]

ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "wsgi.application"

DATABASES = get_env_databases(BASE_DIR)  # Database: https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Password validation - https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
_pass_checks = ["UserAttributeSimilarity", "MinimumLength", "CommonPassword", "NumericPassword"]
AUTH_PASSWORD_VALIDATORS = [{"NAME": f"django.contrib.auth.password_validation.{v}Validator"} for v in _pass_checks]

# Internationalization: https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_L10N, USE_TZ = "en-us", "UTC", True, True, True
