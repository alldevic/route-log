import os
from os import environ


def get_env(key, default=None):
    val = environ.get(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = get_env('SECRET_KEY',
                     '(pt#3^)gwk)!7t@*=6132#k8zl(cj4$1x%7n!jcmd#821^8evr')

DEBUG = get_env('DEBUG', True)

ALLOWED_HOSTS = ["*"]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'import_export',
    'django_q',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'djoser',
    'django_filters',
]

LOCAL_APPS = [
    'user_profile.apps.UserProfileConfig',
    'nav_client',
    'reports',
]

if DEBUG:
    THIRD_PARTY_APPS = ['silk', ] + THIRD_PARTY_APPS

    # Silk settings
    SILKY_PYTHON_PROFILER = True
    SILKY_PYTHON_PROFILER_BINARY = True
    SILKY_PYTHON_PROFILER_RESULT_PATH = os.path.join(BASE_DIR, 'profiles')
    SILKY_MAX_REQUEST_BODY_SIZE = -1  # Silk takes anything <0 as no limit
    SILKY_MAX_RESPONSE_BODY_SIZE = -1
    SILKY_META = True

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE = ['silk.middleware.SilkyMiddleware', ] + MIDDLEWARE

ROOT_URLCONF = 'route_log_prj.urls'

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

WSGI_APPLICATION = 'route_log_prj.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env('POSTGRES_DB', 'postgres_db'),
        'USER': get_env('POSTGRES_USER', 'postgresuser'),
        'PASSWORD': get_env('POSTGRES_PASSWORD', 'mysecretpass'),
        'HOST': get_env('POSTGRES_HOST', 'localhost'),
        'PORT': 5432
    }
}

AUTH_USER_MODEL = 'user_profile.UserProfile'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Novokuznetsk'

USE_I18N = True

USE_L10N = True

USE_TZ = True

NAV_HOST = get_env('SOAP_WSDL', 'http://test/test?wsdl')
NAV_USER = get_env('SOAP_USER', 'username')
NAV_PASS = get_env('SOAP_PASS', 'pass')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 2,
    'retry': 3600,
    'timeout': 3000,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}
