# create_pollinisation_data.py
# À exécuter une seule fois dans le shell Django


import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegetablesfruits.settings')
django.setup()


from vegetables_fruits.models import Fruit, Vegetable

# ===== DONNÉES DE POLLINISATION POUR LES FRUITS =====
fruits_data = {
    # Fruits à pépins
    'pomme': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': True,
        'pollinisateurs_conseilles': 'Golden, Gala, Fuji, Granny Smith',
        'distance_pollinisation': 50,
        'periode_floraison': 'Avril-Mai',
        'conseils_pollinisation': 'Planter au moins deux variétés différentes pour une bonne pollinisation'
    },
    'poire': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': True,
        'pollinisateurs_conseilles': 'Conférence, Williams, Comice',
        'distance_pollinisation': 40,
        'periode_floraison': 'Avril',
        'conseils_pollinisation': 'La plupart des poiriers ont besoin d\'un pollinisateur'
    },
    'coing': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 20,
        'periode_floraison': 'Mai',
        'conseils_pollinisation': 'Autofertile, mais la production est meilleure avec un autre pied'
    },

    # Fruits à noyau
    'pêche': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 20,
        'periode_floraison': 'Mars-Avril',
        'conseils_pollinisation': 'Généralement autofertile, mais favoriser les abeilles'
    },
    'nectarine': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 20,
        'periode_floraison': 'Mars-Avril',
        'conseils_pollinisation': 'Autofertile, sensible aux gelées printanières'
    },
    'abricot': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 30,
        'periode_floraison': 'Mars',
        'conseils_pollinisation': 'La plupart des variétés sont autofertiles'
    },
    'cerise': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': True,
        'pollinisateurs_conseilles': 'Burlat, Reverchon, Hedelfingen',
        'distance_pollinisation': 30,
        'periode_floraison': 'Avril',
        'conseils_pollinisation': 'La plupart des cerisiers ont besoin d\'un pollinisateur'
    },
    'prune': {
        'pollinisation_type': 'mixte',
        'besoin_pollinisateur': True,
        'pollinisateurs_conseilles': 'Reine Claude, Quetsche, Mirabelle',
        'distance_pollinisation': 40,
        'periode_floraison': 'Avril',
        'conseils_pollinisation': 'Certaines variétés sont autofertiles, d\'autres non'
    },

    # Fruits rouges
    'fraise': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 10,
        'periode_floraison': 'Avril à Septembre',
        'conseils_pollinisation': 'Favoriser la présence d\'abeilles pour de plus beaux fruits'
    },
    'framboise': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 10,
        'periode_floraison': 'Mai à Août',
        'conseils_pollinisation': 'Autofertile mais les insectes améliorent la production'
    },
    'cassis': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 10,
        'periode_floraison': 'Avril-Mai',
        'conseils_pollinisation': 'Autofertile'
    },
    'groseille': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 10,
        'periode_floraison': 'Avril',
        'conseils_pollinisation': 'Autofertile'
    },
    'myrtille': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': True,
        'pollinisateurs_conseilles': 'Planter plusieurs variétés',
        'distance_pollinisation': 15,
        'periode_floraison': 'Avril-Mai',
        'conseils_pollinisation': 'La plantation de plusieurs variétés améliore la pollinisation'
    },

    # Agrumes
    'orange': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 20,
        'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'citron': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 20,
        'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile, peut fleurir toute l\'année'
    },
    'pamplemousse': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 20,
        'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },

    # Fruits exotiques
    'banane': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 30,
        'periode_floraison': 'Toute l\'année',
        'conseils_pollinisation': 'Pollinisation naturelle par les oiseaux et chauves-souris'
    },
    'ananas': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 20,
        'periode_floraison': 'Variable',
        'conseils_pollinisation': 'Pollinisation par les colibris dans la nature'
    },
    'mangue': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 30,
        'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Pollinisation par les mouches et abeilles'
    },
    'kiwi': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': True,
        'pollinisateurs_conseilles': 'Planter un pied mâle pour 5-6 pieds femelles',
        'distance_pollinisation': 20,
        'periode_floraison': 'Mai-Juin',
        'conseils_pollinisation': 'Plante dioïque : nécessite un pied mâle et un pied femelle'
    },

    # Melons
    'pastèque': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 50,
        'periode_floraison': 'Juin-Juillet',
        'conseils_pollinisation': 'Nécessite des insectes, surtout les abeilles'
    },
    'melon': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 50,
        'periode_floraison': 'Juin-Juillet',
        'conseils_pollinisation': 'Fleurs mâles et femelles sur le même pied'
    },

    # Vigne
    'raisin': {
        'pollinisation_type': 'vent',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 100,
        'periode_floraison': 'Mai-Juin',
        'conseils_pollinisation': 'Pollinisation principalement par le vent'
    },
}

# ===== DONNÉES DE POLLINISATION POUR LES LÉGUMES =====
legumes_data = {
    # Solanacées
    'tomate': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 10,
        'periode_floraison': 'Juin à Septembre',
        'conseils_pollinisation': 'Secouer légèrement les plants pour favoriser la pollinisation'
    },
    'aubergine': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 10,
        'periode_floraison': 'Juillet à Septembre',
        'conseils_pollinisation': 'Autofertile, les abeilles améliorent la production'
    },
    'poivron': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 10,
        'periode_floraison': 'Juillet à Septembre',
        'conseils_pollinisation': 'Autofertile'
    },
    'piment': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 10,
        'periode_floraison': 'Juillet à Septembre',
        'conseils_pollinisation': 'Autofertile'
    },

    # Cucurbitacées
    'concombre': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': True,
        'distance_pollinisation': 50,
        'periode_floraison': 'Juin à Août',
        'conseils_pollinisation': 'Nécessite des insectes, surtout les abeilles'
    },
    'cornichon': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': True,
        'distance_pollinisation': 50,
        'periode_floraison': 'Juin à Août',
        'conseils_pollinisation': 'Comme le concombre'
    },
    'courgette': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': True,
        'distance_pollinisation': 100,
        'periode_floraison': 'Juin à Août',
        'conseils_pollinisation': 'Fleurs mâles et femelles, nécessite des insectes'
    },
    'potiron': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': True,
        'distance_pollinisation': 100,
        'periode_floraison': 'Juillet à Septembre',
        'conseils_pollinisation': 'Pollinisation manuelle possible en l\'absence d\'insectes'
    },
    'citrouille': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': True,
        'distance_pollinisation': 100,
        'periode_floraison': 'Juillet à Septembre',
        'conseils_pollinisation': 'Comme le potiron'
    },

    # Légumineuses
    'haricot': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 5,
        'periode_floraison': 'Juin à Août',
        'conseils_pollinisation': 'Autofertile, fleurs fermées'
    },
    'petit pois': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 5,
        'periode_floraison': 'Mai à Juillet',
        'conseils_pollinisation': 'Autofertile'
    },
    'fève': {
        'pollinisation_type': 'mixte',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 20,
        'periode_floraison': 'Avril à Juin',
        'conseils_pollinisation': 'Autofertile mais les bourdons améliorent la production'
    },

    # Brassicacées
    'chou': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 500,
        'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'La floraison a lieu la deuxième année'
    },
    'brocoli': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 500,
        'periode_floraison': 'Été',
        'conseils_pollinisation': 'Comme le chou'
    },
    'chou-fleur': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 500,
        'periode_floraison': 'Été',
        'conseils_pollinisation': 'Comme le chou'
    },

    # Apiacées
    'carotte': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 500,
        'periode_floraison': 'Été (2ème année)',
        'conseils_pollinisation': 'Floraison la deuxième année'
    },
    'céleri': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 500,
        'periode_floraison': 'Été',
        'conseils_pollinisation': 'Comme la carotte'
    },
    'fenouil': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 500,
        'periode_floraison': 'Été',
        'conseils_pollinisation': 'Comme la carotte'
    },

    # Liliacées
    'oignon': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 500,
        'periode_floraison': 'Été (2ème année)',
        'conseils_pollinisation': 'Floraison la deuxième année'
    },
    'ail': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 5,
        'periode_floraison': 'Été',
        'conseils_pollinisation': 'Se multiplie principalement par bulbes'
    },
    'poireau': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 500,
        'periode_floraison': 'Été (2ème année)',
        'conseils_pollinisation': 'Floraison la deuxième année'
    },

    # Astéracées
    'laitue': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 10,
        'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile'
    },
    'endive': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 10,
        'periode_floraison': 'Été',
        'conseils_pollinisation': 'Comme la laitue'
    },
    'artichaut': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 100,
        'periode_floraison': 'Été',
        'conseils_pollinisation': 'Pollinisation par les abeilles'
    },

    # Céréales
    'blé': {
        'pollinisation_type': 'auto',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 10,
        'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile, pollinisation par le vent'
    },
    'maïs': {
        'pollinisation_type': 'vent',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 100,
        'periode_floraison': 'Été',
        'conseils_pollinisation': 'Pollinisation par le vent, planter en blocs'
    },

    # Autres
    'épinard': {
        'pollinisation_type': 'vent',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 100,
        'periode_floraison': 'Été',
        'conseils_pollinisation': 'Pollinisation par le vent'
    },
    'rhubarbe': {
        'pollinisation_type': 'insectes',
        'besoin_pollinisateur': False,
        'distance_pollinisation': 50,
        'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Pollinisation par les insectes'
    },
}


# Script de mise à jour
def update_pollinisation_data():
    print("=== MISE À JOUR DES DONNÉES DE POLLINISATION ===\n")

    # Mise à jour des fruits
    fruits_updated = 0
    for nom, data in fruits_data.items():
        fruits = Fruit.objects.filter(nom__icontains=nom)
        for fruit in fruits:
            for key, value in data.items():
                setattr(fruit, key, value)
            fruit.save()
            fruits_updated += 1
            print(f"✅ Fruit mis à jour: {fruit.nom}")

    # Mise à jour des légumes
    legumes_updated = 0
    for nom, data in legumes_data.items():
        legumes = Vegetable.objects.filter(nom__icontains=nom)
        for legume in legumes:
            for key, value in data.items():
                setattr(legume, key, value)
            legume.save()
            legumes_updated += 1
            print(f"✅ Légume mis à jour: {legume.nom}")

    print(f"\n=== RÉSUMÉ ===")
    print(f"Fruits mis à jour: {fruits_updated}")
    print(f"Légumes mis à jour: {legumes_updated}")

if __name__ == '__main__':
    update_pollinisation_data()