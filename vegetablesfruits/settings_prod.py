"""
Settings de PRODUCTION pour Agriculture 2.0.
À utiliser via DJANGO_SETTINGS_MODULE=vegetablesfruits.settings_prod
"""
from .settings import *

# ✅ Sécurité stricte
DEBUG = False
SECRET_KEY = os.environ['DJANGO_SECRET_KEY'] # Obligatoire, pas de fallback

# ✅ Hôtes autorisés (à adapter avec ton domaine)
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ValueError("DJANGO_ALLOWED_HOSTS doit être défini en prod")

# ✅ Base de données PostgreSQL (si tu l'utilises)
# Sinon, commente ce bloc pour rester sur SQLite en attendant
import dj_database_url # à installer : pip install dj-database-url
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ✅ Fichiers statiques avec WhiteNoise (pas besoin de Nginx pour les servir)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ✅ Sécurité HTTPS (activer une fois le SSL en place)
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000 # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ✅ Email (à configurer avec Brevo/SendGrid en prod)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp-relay.brevo.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'contact@agriculture20.fr')
