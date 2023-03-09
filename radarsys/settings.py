"""
Django settings for radarsys project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xshb$k5fc-+j16)cvyffj&9u__0q3$l!hieh#+tbzqg)*f^km0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS=[
    "http://*.localhost:8030",
    "http://localhost:8030",
    "http://127.0.0.1:8030",
    "http://*.localhost:8086",
    "http://localhost:8086",
    "http://127.0.0.1:8086"
]
#Si se requiere que la aplicación salga de este entorno, para otros usuarios es necesario hacer una API request https://fractalideas.com/blog/making-react-and-django-play-well-together-single-page-app-model/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.main',
    'apps.misc',
    'apps.rc',
    'apps.dds',
    'apps.jars',
    'apps.usrp',
    'apps.abs',
    'apps.cgs',
    'apps.dds_rest',
    'apps.atrad',
    "django_bootstrap5",
    'polymorphic',
    'radarsys',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'radarsys.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.main.processors.radarsys_globals',
            ],
        },
    },
]

WSGI_APPLICATION = 'radarsys.wsgi.application'
ASGI_APPLICATION = 'radarsys.asgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': 'radarsys.sqlite',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'radarsys'),
        'USER': os.environ.get('DB_USER', 'docker'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'docker'),
        'HOST': os.environ.get('POSTGRES_PORT_5432_TCP_ADDR', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT_5432_TCP_PORT', '5432'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_TZ   = False #True

TIME_ZONE = os.environ.get('TZ', 'America/Lima')

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'radarsys/static/')
]   

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_URL = '/accounts/login' 
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/admin'
LOGOUT_REDIRECT_URL = '/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',  
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


import django
from django.utils.encoding import force_str
django.utils.encoding.force_text = force_str

# choose of auto-created primary keys
DEFAULT_AUTO_FIELD='django.db.models.AutoField'
