import time
import os
import django

# Charger Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegetablesfruits.settings')
django.setup()

from vegetables_fruits.views import verifier_alertes_meteo

while True:
    print("⏰ Vérification météo automatique...")
    verifier_alertes_meteo()
    time.sleep(1800) # 30 minutes