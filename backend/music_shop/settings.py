import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http(s)://your_domain.com').split(', ')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'you_need_to_set_the_secret_key_in_env')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1, localhost').split(', ')

INTERNAL_IPS = os.getenv('INTERNAL_IPS', '127.0.0.1, localhost').split(', ')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'tinymce',
    'debug_toolbar',
    'import_export',

    'item.apps.ItemConfig',
    'category.apps.CategoryConfig',
    'tags.apps.TagsConfig',
    'blog.apps.BlogConfig',
    'order.apps.OrderConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'music_shop.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'music_shop.wsgi.application'


# SQLite's settings (for local development):
##############################################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL's settings (for production or locally in containers):
###############################################################################

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.getenv('POSTGRES_DB', 'django'),
#        'USER': os.getenv('POSTGRES_USER', 'django'),
#        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'you_need_to_set_the_password_in_env'),
#        'HOST': os.getenv('DB_HOST', 'localhost'),
#        'PORT': os.getenv('DB_PORT', 5432)
#    }
# }

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'collected_static'

STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Viewing settings
###############################################################################

NAME_LENGHT = int(os.getenv('NAME_LENGHT', 30))
DESCRIPTION_LENGHT = int(os.getenv('DESCRIPTION_LENGHT', 50))
SHORT_DESCRIPTION_LENGHT = int(os.getenv('SHORT_DESCRIPTION_LENGHT', 50))
BLOG_TEXT_LENGHT = int(os.getenv('BLOG_TEXT_LENGHT', 150))
ORDER_NOTES_LENGHT = int(os.getenv('ORDER_NOTES_LENGHT', 50))
ADMIN_NOTES_LENGHT = int(os.getenv('ORDER_NOTES_LENGHT', 50))
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@email.xoxo')


# Import/Export settings
###############################################################################
IMPORT_EXPORT_USE_TRANSACTIONS = True


# Sending emails via Yandex mail (Don't work on pythonanywhere.com)
###############################################################################

RECIPIENT_ADDRESS = os.getenv('RECIPIENT_ADDRESS',
                              'your_email_on_yandex@yandex.ru')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.yandex.ru')
EMAIL_PORT = os.getenv('EMAIL_PORT', '465')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False') == 'True'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL',
                               'your_email_on_yandex@yandex.ru')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER',
                            'your_email_on_yandex@yandex.ru')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD',
                                'your_strong_email_password')
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND',
                          'django.core.mail.backends.smtp.EmailBackend')

# Celery settings
###############################################################################

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND',
                                  'redis://127.0.0.1:6379/0')

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = os.getenv(
    'CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP', 'True') == 'True'


# TinyMCE settings
###############################################################################

TINYMCE_JS_URL = os.path.join(STATIC_URL, "tinymce/tinymce.min.js")
TINYMCE_COMPRESSOR = False

TINYMCE_DEFAULT_CONFIG = {
    "height": "520px",
    "menubar": "file edit view insert format tools table help",
    "plugins": 'anchor autolink charmap codesample emoticons image link lists '
               'media searchreplace table visualblocks wordcount fullscreen '
               'pagebreak help',
    "toolbar": 'undo redo blocks fontfamily fontsize '
               'bold italic underline strikethrough blockquote '
               'link image media forecolor backcolor table align lineheight '
               'checklist numlist bullist indent outdent emoticons charmap '
               'removeformat ',
    "toolbar_mode": 'sliding',
    "custom_undo_redo_levels": 15,
}
