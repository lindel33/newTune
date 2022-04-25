# -*- coding: utf-8 -*-
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ljw@!#$uwio5u43u45u35u@#q4utiuopi34io5uodas231123@!#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['tuneapple.xyz', 'https://tuneapple.xyz/', '127.0.0.1', 'https://tuneapple.xyz/panel/homelogin/?next=/panel/home', 'https://tuneapple.xyz/']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'tune_admin',
    'bot_telegram',
    'price',
    'provider',
    'cost_models',
#     'corsheaders',
]

MIDDLEWARE = [
#     "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#     "corsheaders.middleware.CorsPostCsrfMiddleware" ,
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tune.urls'

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

WSGI_APPLICATION = 'tune.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TuneApple$TuneProd',
        'USER': 'TuneApple',
        'PASSWORD': 'tune',
        'OPTIONS': {'charset': 'utf8mb4', },
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/apple/code/project1/tune/static/'
STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'TuneApple_cache')
    }
}


CSRF_TRUSTED_ORIGINS = [
    'https://tuneapple.xyz/',
    'https://tuneapple.xyz',
    'https://www.tuneapple.xyz/',
    'https://www.tuneapple.xyz/',
    'tuneapple.xyz/',
    'tuneapple.xyz'
]

CORS_ALLOWED_ORIGINS = ['https://tuneapple.xyz',
                        'https://tuneapple.xyz/',
                        'https://www.tuneapple.xyz',
                        'https://www.tuneapple.xyz/',
                        'tuneapple.xyz'
                        'https://tuneapple.xyz/',
                       ]
CORS_ALLOWED_ORIGIN_REGEXES  = [
     r"^https://\w+\.tuneapple\.xyz$" , 
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOWED_ORIGINS  = [
    "http://tuneapple.xyz" ,
    "http://www.tuneapple.xyz" ,
    "https://www.tuneapple.xyz" , 
    "https://www.tuneapple.xyz" ,
    'https://tuneapple.xyz/panel/homelogin/?next=/panel/home',
    'https://tuneapple.xyz/',
] 

