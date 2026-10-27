import os
import sys
import django

# 1. On indique à Python où trouver le dossier 'agriculture'
# (On récupère le chemin du dossier où se trouve ce script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# 2. On configure Django (en utilisant le bon nom de projet)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegetablesfruits.settings')
django.setup()

# 3. Maintenant on peut importer les modèles
from django.contrib.auth import get_user_model
from vegetables_fruits.views import get_region_utilisateur
from vegetables_fruits.models import GeometricFigure

User = get_user_model()
user = User.objects.get(username='kamdem')

try:
    fig = GeometricFigure.objects.get(user=user, name='parcelle_japon')
except GeometricFigure.DoesNotExist:
    print("❌ Parcelle 'parcelle_japon' introuvable. Voici les tiennes :")
    for f in GeometricFigure.objects.filter(user=user):
        print(f" - {f.name}")
    raise SystemExit(1)

print("=== DIAGNOSTIC PARCELLE JAPON ===")
print(f"Nom : {fig.name}")
print(f"Latitude : {fig.adresse_lat}")
print(f"Longitude : {fig.adresse_lng}")

info = get_region_utilisateur(user, fig)
print()
print("--- Résultat get_region_utilisateur ---")
print(f"continent = {info.get('continent')}")
print(f"pays = {info.get('pays')}")
print(f"region = {info.get('region')}")
print(f"saison = {info.get('saison')}")