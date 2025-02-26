from pathlib import Path
import os
from .utils import dynamic_url


BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'  # URL to access media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Directory where media files are stored

# Build paths inside the project like this: BASE_DIR / 'subdir'.

SECRET_KEY = 'django-insecure-1!=^-)1^gj!pu6dxt6y5t48gw00o92vus5%n3hme2j8-ox83l*'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# Application definition
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'channels',
    'django.contrib.staticfiles',
    'compressor',
    'app.accounts',
    'app.dashboards',
    'app.clients',
    'django.contrib.sites',  # Required for allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # Include Google provider
    'django_extensions',
    'tailwind',
]


SITE_ID = 1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.accounts.middleware.RoleRequiredMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Add this line
    # "django_browser_reload.middleware.BrowserReloadMiddleware"
]
ROOT_URLCONF = 'inven.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [  
            BASE_DIR / "templates",         # Global templates directory
            BASE_DIR / 'inven/inven/inven/app/accounts/templates',
            BASE_DIR / "app/accounts/templates", # Accounts-specific templates (optional)
            BASE_DIR / "app/dashboards/templates", # Dashboards-specific templates (optional)
            BASE_DIR / "app/clients/templates", # Dashboards-specific templates (optional)
        ],
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
WSGI_APPLICATION = 'inven.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inven',
        'USER': 'lyndonabesamis',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'auth.User'  # This is Django's default user model
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


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # For custom login
    'allauth.account.auth_backends.AuthenticationBackend',  # For Django Allauth
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = 'static/'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
COMPRESS_ROOT = BASE_DIR / 'static'
COMPRESS_ENABLED = True
STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)
LOGIN_REDIRECT_URL = '/dashboards/'  # Redirect after successful login
LOGOUT_REDIRECT_URL = '/' 
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Change to 'mandatory' for email verification


APPEND_SLASH = False


ASGI_APPLICATION = 'inven.asgi.application'

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',  # Replace with Redis for production
#     },
# }

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # Redis server
        },
    },
}

# Google OAuth Settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "",
            "secret": "",
            "key": "",
        },
       'SCOPE': ['openid', 'profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'offline'},

    }
}


SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'http://localhost:8000/accounts/google/login/callback/'
SOCIALACCOUNT_LOGIN_ON_GET=True