# copier_nom_vers_varietes.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegetablesfruits.settings')
django.setup()

from vegetables_fruits.models import Vegetable, Fruit


def copier_nom_vers_varietes():
    """Copie la valeur du champ 'nom' dans le champ 'varietes' pour tous les légumes et fruits"""

    print("=== MISE À JOUR DES VARIÉTÉS ===\n")

    # Pour les légumes
    legumes = Vegetable.objects.all()
    compteur_legumes = 0

    for legume in legumes:
        if not legume.varietes or legume.varietes == '-':
            legume.varietes = legume.nom
            legume.save()
            compteur_legumes += 1
            print(f"✅ Légume mis à jour: {legume.nom} → variétés: {legume.varietes}")

    # Pour les fruits
    fruits = Fruit.objects.all()
    compteur_fruits = 0

    for fruit in fruits:
        if not fruit.varietes or fruit.varietes == '':
            fruit.varietes = fruit.nom
            fruit.save()
            compteur_fruits += 1
            print(f"✅ Fruit mis à jour: {fruit.nom} → variétés: {fruit.varietes}")

    print(f"\n=== RÉSUMÉ ===")
    print(f"Légumes mis à jour: {compteur_legumes}")
    print(f"Fruits mis à jour: {compteur_fruits}")
    print(f"Total: {compteur_legumes + compteur_fruits}")


if __name__ == '__main__':
    copier_nom_vers_varietes()