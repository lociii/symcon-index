# -*- coding: UTF-8 -*-
import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from datetime import timedelta

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_NAME = os.path.basename(PROJECT_ROOT)
BASE_DIR = os.path.dirname(PROJECT_ROOT)

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "addSecretKeyToEnvironment"),
    DJANGO_LOG_LEVEL=(str, 'WARNING'),
    GITHUB_API_USER=(str, ''),
    GITHUB_API_TOKEN=(str, ''),
    REDIS_URL=(str, 'redis://'),
    RECAPTCHA_PUBLIC_KEY=(str, ''),
    RECAPTCHA_PRIVATE_KEY=(str, ''),
)
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

# Application definition

INSTALLED_APPS = [
    'heroku.apps.HerokuConfig',
    'symcon.apps.SymconConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django_extensions',
    'bootstrap_pagination',
    'django_celery_results',
    'django_celery_beat',
    'captcha',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'heroku.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'heroku.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'symcon', 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

LOGGING_DEFAULT_HANDLERS = ['console']
LOGGING_LOG_LEVEL = env('DJANGO_LOG_LEVEL')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': LOGGING_DEFAULT_HANDLERS,
            'level': LOGGING_LOG_LEVEL,
            'formatter': 'standard',
        },
        'django.db.backends': {
            'handlers': LOGGING_DEFAULT_HANDLERS,
            'level': LOGGING_LOG_LEVEL,
            'propagate': False,
        },
        'heroku': {
            'handlers': LOGGING_DEFAULT_HANDLERS,
            'level': LOGGING_LOG_LEVEL,
        },
        'celery': {
            'handlers': LOGGING_DEFAULT_HANDLERS,
            'level': LOGGING_LOG_LEVEL,
            'propagate': False,
        },
    },
}

# CELERY
CELERY_BROKER_URL = env('REDIS_URL')
CELERYD_HIJACK_ROOT_LOGGER = False
CELERY_QUEUE_HA_POLICY = 'all'
CELERY_WORKER_DIRECT = False
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_PERSISTENT = True
CELERY_IGNORE_RESULT = True
CELERY_TASK_RESULT_EXPIRES = timedelta(days=7)
CELERY_TIMEZONE = TIME_ZONE
CELERY_TRACK_STARTED = True
CELERY_SEND_EVENTS = False
CELERY_SEND_TASK_SENT_EVENT = False
CELERY_EVENT_QUEUE_TTL = 60
# END CELERY

SITE_ID = 1

LANGUAGES = (
    ('de', 'Deutsch'),
    ('en', 'English'),
)

GITHUB_API_USER = env('GITHUB_API_USER')
GITHUB_API_TOKEN = env('GITHUB_API_TOKEN')

FORMAT_MODULE_PATH = '%s.formats' % SITE_NAME

RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')
NOCAPTCHA = True
