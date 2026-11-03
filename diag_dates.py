import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegetablesfruits.settings')
django.setup()

from vegetables_fruits.models import Fruit, Vegetable
from vegetables_fruits.management.commands.maj_dates_cultures import DATES_REFERENCE, normaliser

print("=== DIAGNOSTIC ===")
print(f"Nombre d'entrées dans DATES_REFERENCE : {len(DATES_REFERENCE)}")

# Test avec Abricot (Fruit)
f = Fruit.objects.filter(nom__iexact='Abricot').first()
if f:
    nom_norm = normaliser(f.nom)
    print(f"\nEn base (Fruit) : '{f.nom}'")
    print(f"Normalisé : '{nom_norm}'")
    print(f"Dans DATES_REFERENCE ? {nom_norm in DATES_REFERENCE}")
else:
    print("\nAbricot introuvable dans Fruit")

# Test avec Tomate (Vegetable ou Fruit)
v = Vegetable.objects.filter(nom__iexact='Tomate').first()
if v:
    nom_norm = normaliser(v.nom)
    print(f"\nEn base (Vegetable) : '{v.nom}'")
    print(f"Normalisé : '{nom_norm}'")
    print(f"Dans DATES_REFERENCE ? {nom_norm in DATES_REFERENCE}")

# Test avec Olivier
o = Fruit.objects.filter(nom__icontains='oliv').first()
if o:
    nom_norm = normaliser(o.nom)
    print(f"\nEn base (Olivier) : '{o.nom}'")
    print(f"Normalisé : '{nom_norm}'")
    print(f"Dans DATES_REFERENCE ? {nom_norm in DATES_REFERENCE}")
