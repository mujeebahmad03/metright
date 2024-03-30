"""
Django settings for metright project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*4&#me*v8dscg807-yl^@)xy5ra8m4xs@_-kf(4_7w4_*2#4#d'


# SECRET_KEY = os.environ.get('SECRET_KEY')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'metapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'metapp.LoginCheckMiddleware.LoginCheckMiddleWare',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'metright.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'metright.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     # 'default': {
#     #     'ENGINE': 'django.db.backends.mysql',
#     #     'NAME': 'metright',
#     #     'USER': 'root',
#     #     #'PASSWORD': 'Born?1996',
#     #     'PASSWORD': '',
#     #     'HOST': 'localhost',
#     #     'PORT': '3306'
#     # }
#     'default': dj_database_url.config(
#         default="sqlite:///"+ os.path.join(BASE_DIR, "db.sqlite3")
#     )
# }


# DATABASES = {
# 	"default": dj_database_url.parse("postgres://metright_user:pNWO1XPrjVUGuUAWQepKN0qW9RHBo41B@dpg-cm2v73mn7f5s73eku420-a.oregon-postgres.render.com/metright")
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'URL': 'postgresql://postgres:F1af354EeA525b56EDB4d45G4cB2e-4a@monorail.proxy.rlwy.net:47964/railway',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'F1af354EeA525b56EDB4d45G4cB2e-4a',
        'HOST': 'monorail.proxy.rlwy.net',
        'PORT': 47964,
         'OPTIONS': {
            'options': '-c timezone=UTC'  # Set timezone to UTC
        },
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'metright/static')]



# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# AWS Configuration

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'brint-media-files-24'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_REGION_NAME = 'eu-north-1'
AWS_FILE_OVERWRITE = False

# Storage Configuration for Amazon S3
AWS_LOCATION = 'static'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/' 
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# AWS_DEFAULT_ACL = 'public-read'

# MEDIA_ROOT = '/media/'
MEDIA_URL =  f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Add custom locations for different types of media files
# NOTES_FILES_LOCATION = f'{MEDIA_URL}notes/'
# RECEIPT_FILES_LOCATION = f'{MEDIA_URL}receipt/'
# ASSIGNMENTS_FILES_LOCATION = f'{MEDIA_URL}assignments/'
# ASSIGNMENTS_SUBMISSION_FILES_LOCATION = f'{MEDIA_URL}assignment_submission/'
# REPORTS_FILES_LOCATION = f'{MEDIA_URL}reports/'
# INVOICE_FILES_LOCATION = f'{MEDIA_URL}invoice/'
# PROFILE_PIC_LOCATION = f'{MEDIA_URL}/profile-pic/'


AUTH_USER_MODEL = 'metapp.CustomUser'
AUTHENTICATION_BACKEND = 'metapp.EmailBackEnd.EmailBackEnd'
