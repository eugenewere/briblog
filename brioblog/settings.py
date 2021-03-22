"""
Django settings for brioblog project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# import export as export
import sweetify

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!fw8sv*nk7$qro7s$xuo7)*e-1hc3(oru4vzpw2zm@eq61*!9*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'blogfrontapp.apps.BlogfrontappConfig',
    'blogbackapp.apps.BlogbackappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'hitcount',
    'ckeditor',
    'djrichtextfield',
    'social_django',
    'sweetify',
    'crispy_forms',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'brioblog.urls'

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

                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect',  # <--
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
]

WSGI_APPLICATION = 'brioblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL ='/media/'

# SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'
#
# sweetify.DEFAULT_OPTS = {
#     'showConfirmButton': False,
#     'timer': 2500,
#     'allowOutsideClick': True,
#     'confirmButtonText': 'OK',
#     'customClass': {
#         'popup': 'animated tada',
#     }
# }


LOGIN_REDIRECT_URL = 'BLOG:home'
LOGIN_URL = "BLOG:home"
LOGOUT_URL = 'BLOG:home'


SOCIAL_AUTH_FACEBOOK_KEY = '746649342720717'
SOCIAL_AUTH_FACEBOOK_SECRET = 'd889a66c0b7110761da974da5fbd4c42'
# SOCIAL_AUTH_FACEBOOK_SECRET = 'd1afad05f5f093ccecea0586d92ade93'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'eugenecodedev@gmail.com'
# EMAIL_HOST_USER = 'Climatechangebasicske@gmail.com'
# EMAIL_HOST_PASSWORD = 'Brandoxvilla7123'
EMAIL_HOST_PASSWORD = '123$insecure'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL: False
# OPENEXCHANGERATES_API_KEY = '71501b20f84c42cfa79667487398fd93'
# PAYPAL_RECEIVER_EMAIL = "sb-mobfb2963036@business.example.com"
# PAYPAL_TEST = True

SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'

sweetify.DEFAULT_OPTS = {
    'showConfirmButton': False,
    'timer': 2500,
    'allowOutsideClick': True,
    'confirmButtonText': 'OK',
    'customClass': {
        'popup': 'animated tada',
    }
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# CELERY_BROKER_URL = 'amqp://localhost'
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_CACHE_BACKEND = 'django-cache'



# export DJANGO_SETTINGS_MODULE=brioblog.settings