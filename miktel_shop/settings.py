"""
Django settings for miktel_shop project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import socket

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['127.0.0.1', 'serwiswrybnej.pl', 'www.serwiswrybnej.pl'
                 '51.75.64.242', 'e372-185-172-87-165.ngrok.io']

print(socket.gethostname())
if socket.gethostname() in ["Asus", "michalp", "DESKTOP-HDDTT8P", "michal-asus"]:
    SECURE_SSL_REDIRECT = False
    DEBUG = True
    DOMAIN = "127.0.0.1:8000"
    DOMAIN_URL = "http://" + DOMAIN
    DatabaseName = "miktel_shop_v1"
    SECURE_SSL_REDIRECT = False
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY_TEST')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY_TEST')
else:
    DOMAIN = "serwiswrybnej.pl"
    DOMAIN_URL = "https://" + DOMAIN
    DatabaseName = "miktel_shop_v1"
    DEBUG = False
    SECURE_SSL_REDIRECT = True
    SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
    SESSION_COOKIE_DOMAIN = f".{DOMAIN}"
    SESSION_COOKIE_AGE = 10 * 60
    SESSION_SAVE_EVERY_REQUEST = True
    CSRF_COOKIE_DOMAIN = f".{DOMAIN}"
    CSRF_COOKIE_HTTPONLY = True
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Application definition


# Application definition

INSTALLED_APPS = [
    'web.accounts.apps.AccountConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'rest_framework',
    'crispy_forms',
    'captcha',
    'sorl.thumbnail',
    'web',
    # 'django_minify_html'
    'compressor',

]

STRIPE_ENDPOINT_SECRET = os.environ.get('STRIPE_ENDPOINT_SECRET')

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAP_PUBKEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAP_PRIVKEY')

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'web.middleware.WwwRedirectMiddleware',
    # 'django_minify_html.middleware.MinifyHtmlMiddleware',
]

ROOT_URLCONF = 'miktel_shop.urls'

CART_SESSION_ID = 'cart'

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
                'django.template.context_processors.media',
                "web.cart.my_context_processor.cart",
                "web.front.my_context_processor.logo",
                "web.front.my_context_processor.get_domain",
                "web.products.my_context_processor.menu_category",
            ],
        },
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

WSGI_APPLICATION = 'miktel_shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "NAME": DatabaseName,
        "ENGINE": "django.db.backends.postgresql",
        "USER": os.environ.get('DB_USER'),
        "PASSWORD": os.environ.get('DB_PASSWORD'),
        "HOST": "localhost",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'pl'
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_L10N = True
USE_TZ = False
DATETIME_FORMAT = "Y-m-d H:M:S"
DATE_INPUT_FORMATS = "Y-m-d H:M:S"

STATIC_URL = '/static/'
STATIC_ROOT = "static"
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATICFILES_DIRS = (os.path.join(SITE_ROOT, "static/"), )
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = "front_page"
LOGOUT_REDIRECT_URL = "login"

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
SERVER_EMAIL = os.environ.get('EMAIL_HOST')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_USER')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')

DJANGORESIZED_DEFAULT_SIZE = [1280, 960]
DJANGORESIZED_DEFAULT_QUALITY = 100
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'WEBP'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'WEBP': ".webp"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES
}
