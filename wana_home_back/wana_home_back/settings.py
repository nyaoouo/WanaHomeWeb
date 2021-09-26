from pathlib import Path

from charset_normalizer import assets

BASE_DIR = Path(__file__).resolve().parent.parent
from utils.Config import config
from utils import rand_char

SECRET_KEY = config.get('django', 'key', fallback=rand_char(32))

DEBUG = config.get('django', 'debug', fallback=None) is not None

ALLOWED_HOSTS = [s.strip() for s in config.get('django', 'allow_hosts', fallback='*').split('|')]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.Middleware.AjajPostMiddleware',
]

ROOT_URLCONF = 'wana_home_back.urls'

WSGI_APPLICATION = 'wana_home_back.wsgi.application'

if config.get('mysql', 'host', fallback=''):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config['mysql']['db_name'],
            'USER': config['mysql']['user'],
            'PASSWORD': config['mysql']['pass'],
            'HOST': config['mysql']['host'],
            'PORT': config['mysql']['port'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'OPTIONS': {
                'timeout': 30
            }
        }
    }

# if config['redis']['host']:
#     CACHES = {
#         "default": {
#             "BACKEND": "django_redis.cache.RedisCache",
#             "LOCATION": f"redis://{config['redis']['host']}:{config['redis']['port']}/{config['redis']['db']}",
#             "OPTIONS": {
#                 "CLIENT_CLASS": "django_redis.client.DefaultClient",
#                 "PASSWORD": config['redis']['pass'],
#             }
#         }
#     }
# else:
#     CACHES = {
#         'default': {
#             'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#             'LOCATION': BASE_DIR / 'cache',
#         }
#     }

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/assets/'

STATICFILES_DIRS = [
    BASE_DIR / "front" / "assets",
]
