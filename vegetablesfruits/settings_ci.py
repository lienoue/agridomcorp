from .settings import *

# On retire les applications qui posent problème sur la CI (Linux)
# ou qui ne sont pas nécessaires pour faire tourner les tests.
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in ['django_cron', 'silk', 'debug_toolbar', 'background_task']]

# On retire aussi les middlewares associés s'il y en a
MIDDLEWARE = [mw for mw in MIDDLEWARE if mw not in ['debug_toolbar.middleware.DebugToolbarMiddleware', 'silk.middleware.SilkyMiddleware']]

# ✅ Pour que les tests ne plantent pas à cause des fichiers statiques
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage", # <-- Sans Whitenoise
    },
}