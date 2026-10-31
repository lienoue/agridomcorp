import os
import sys
from pathlib import Path
from dotenv import load_dotenv


# Charge le fichier .env s'il existe
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ SECRET_KEY depuis l'environnement (fallback dev uniquement)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-key-change-me')

# ✅ DEBUG depuis l'environnement (False par défaut)
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# ✅ ALLOWED_HOSTS depuis l'environnement
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# --- CONFIGURATION GDAL VIA WHL (PIP) ---
# Avec le .whl, GDAL est dans ton environnement virtuel.
# On cherche dynamiquement le chemin de ton environnement.
VENV_BASE = sys.prefix 
GDAL_BIN = os.path.join(VENV_BASE, 'Lib', 'site-packages', 'osgeo')

if os.path.exists(GDAL_BIN):
    # On ajoute le dossier osgeo au PATH pour que Python trouve les DLL
    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(GDAL_BIN)
    os.environ['PATH'] = GDAL_BIN + os.pathsep + os.environ.get('PATH', '')

    # Chemins spécifiques pour Django
    # Le .whl installe généralement gdal308.dll ou gdal309.dll
    # Si le serveur ne trouve pas, vérifie le nom dans Lib/site-packages/osgeo/
    GDAL_LIBRARY_PATH = os.path.join(GDAL_BIN, 'gdal.dll')
    GEOS_LIBRARY_PATH = os.path.join(GDAL_BIN, 'geos_c.dll')

    # Les données PROJ et GDAL sont aussi dans le dossier osgeo du whl
    os.environ['PROJ_LIB'] = os.path.join(GDAL_BIN, 'data', 'proj')
    os.environ['GDAL_DATA'] = os.path.join(GDAL_BIN, 'data', 'gdal')

# --- FIN CONFIGURATION GDAL ---

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-*l(h)w5#)8j*ijdfa41n_v+rtifw1e1bt)74epbfs4uc#0(&+&'

DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.gis',
    'django.contrib.staticfiles',
    'vegetables_fruits.apps.VegetablesFruitsConfig',
    'background_task',
    'debug_toolbar',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'vegetables_fruits.CustomUser'
LOGIN_REDIRECT_URL = 'vegetables_fruits:profile'
LOGOUT_REDIRECT_URL = 'vegetables_fruits:index'

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
   # 'silk.middleware.SilkyMiddleware',
    'vegetables_fruits.middleware.ConnexionLogMiddleware',
]
SILKY_PYTHON_PROFILER = True
SILKY_ANALYZE_QUERIES = True
SILKY_QUERY_ANALYSE_IGNORE = True
ROOT_URLCONF = 'vegetablesfruits.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'vegetables_fruits' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'vegetables_fruits.context_processors.progression_junior',
            ],
        },
    },
]

WSGI_APPLICATION = 'vegetablesfruits.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'vegetables_fruits', 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ==================== LOGGING ====================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name}:{lineno} → {message}',
            'style': '{',
            'datefmt': '%d/%m/%Y %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'vegetables_fruits': {
            'handlers': ['console'],
            'level': 'DEBUG', # ← Affiche debug + info + warning + error
            'propagate': False,
        },
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'vegetables_fruits.validators.ComplexityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ('username', 'email', 'first_name', 'last_name'),
            'max_similarity': 0.7,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Whitenoise pour compression et cache
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Pour le développement (console) configuration email via Brevo
EMAIL_BACKEND = 'anymail.backends.sendinblue.EmailBackend'
ANYMAIL = {
    'SENDINBLUE_API_KEY': os.environ.get('SENDINBLUE_API_KEY', ''),
}
DEFAULT_FROM_EMAIL = 'lienouebrice@gmail.com'
# Pour la production (exemple avec Gmail)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'votre.email@gmail.com'
# EMAIL_HOST_PASSWORD = 'votre-mot-de-passe'


# Stripe
load_dotenv()
STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')
STRIPE_PRICE_IDS = {
    'GRATUIT': None,
    'BASIQUE_MENSUEL': os.environ.get('STRIPE_BASIQUE_MENSUEL', ''),
    'BASIQUE_ANNUEL': os.environ.get('STRIPE_BASIQUE_ANNUEL', ''),
    'PREMIUM_MENSUEL': os.environ.get('STRIPE_PREMIUM_MENSUEL', ''),
    'PREMIUM_ANNUEL': os.environ.get('STRIPE_PREMIUM_ANNUEL', ''),
    'ENSEIGNANT_MENSUEL': os.environ.get('STRIPE_ENSEIGNANT_MENSUEL', ''),
    'ENSEIGNANT_ANNUEL': os.environ.get('STRIPE_ENSEIGNANT_ANNUEL', ''),
}

# MAPBOX
MAPBOX_TOKEN = os.environ.get('MAPBOX_TOKEN', '')

# OPENWEATHER
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')

# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0' # Redis par défaut
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Celery Beat
INSTALLED_APPS += [
    'django_celery_beat',
    'silk',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'vegetables_fruits', 'media')

# Utilisation AWS S3 ou DigitalOcean Spaces pour le stockage
#INSTALLED_APPS += ['storages']

# settings.py
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
#AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
#AWS_STORAGE_BUCKET_NAME = 'agriculture-galerie'
#AWS_S3_REGION_NAME = 'eu-west-3'



# settings.py - Configuration PostgreSQL
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'agriculture_db',
#        'USER': 'agriculture_user',
#        'PASSWORD': 'mot_de_passe',
#        'HOST': 'localhost',
#        'PORT': '5432',
#        'CONN_MAX_AGE': 600, # Connexions persistantes
#        'OPTIONS': {
#            'options': '-c statement_timeout=30s', # Timeout 30 secondes
#        }
#    }
#}

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]





CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

