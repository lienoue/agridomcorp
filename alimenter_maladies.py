# scripts/alimenter_maladies.py
# Exécution : python manage.py shell < alimenter_maladies.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriculture.settings')
django.setup()

from vegetables_fruits.models import MaladieCulture, Culture

MALADIES_DATA = [
    {
        'nom': 'Mildiou',
        'description': 'Maladie fongique due à l\'humidité excessive. Se manifeste par des taches jaunes sur les feuilles, puis brunes.',
        'emoji': '🦠',
        'cultures_cibles': ['Tomate', 'Pomme de terre', 'Vigne', 'Concombre', 'Courgette'],
        'temperature_min': 10,
        'temperature_max': 25,
        'humidite_min': 80,
        'humidite_max': 100,
        'precipitation_min': 5,
        'mois_debut': 5,
        'mois_fin': 9,
        'regions': ['tous'],
        'traitement_preventif': 'Bouillie bordelaise (cuivre) toutes les 2-3 semaines. Éviter l\'excès d\'humidité.',
        'traitement_curatif': 'Fongicide à base de cuivre ou de mancozèbe. Supprimer les parties atteintes.',
        'produits_recommandes': ['Bouillie bordelaise', 'Mancozèbe', 'Cuivre'],
        'delai_alerte_jours': 3,
        'gravite': 'elevee',
        'frequence_annuelle': 3,
    },
    {
        'nom': 'Oïdium (Blanc)',
        'description': 'Champignon blanc poudreux sur les feuilles. Se développe par temps sec et chaud.',
        'emoji': '🫧',
        'cultures_cibles': ['Courgette', 'Concombre', 'Fraise', 'Vigne', 'Tomate', 'Pommier'],
        'temperature_min': 15,
        'temperature_max': 30,
        'humidite_min': 60,
        'humidite_max': 80,
        'precipitation_min': 0,
        'precipitation_max': 5,
        'mois_debut': 5,
        'mois_fin': 8,
        'regions': ['tous'],
        'traitement_preventif': 'Soufre micronisé tous les 10-15 jours. Pulvérisation de purin d\'ortie.',
        'traitement_curatif': 'Soufre mouillable ou bicarbonate de soude + savon noir.',
        'produits_recommandes': ['Soufre', 'Bicarbonate de soude', 'Purin d\'ortie'],
        'delai_alerte_jours': 3,
        'gravite': 'moyenne',
        'frequence_annuelle': 2,
    },
    {
        'nom': 'Mildiou de la pomme de terre',
        'description': 'Maladie fongique spécifique à la pomme de terre. Taches brunes sur les feuilles.',
        'emoji': '🦠',
        'cultures_cibles': ['Pomme de terre'],
        'temperature_min': 12,
        'temperature_max': 20,
        'humidite_min': 85,
        'humidite_max': 100,
        'precipitation_min': 10,
        'mois_debut': 6,
        'mois_fin': 8,
        'regions': ['tous'],
        'traitement_preventif': 'Bouillie bordelaise avant la floraison. Buttage préventif.',
        'traitement_curatif': 'Fongicide anti-mildiou spécifique. Supprimer les plants atteints.',
        'produits_recommandes': ['Bouillie bordelaise', 'Fongicide spécifique'],
        'delai_alerte_jours': 2,
        'gravite': 'critique',
        'frequence_annuelle': 2,
    },
    {
        'nom': 'Rouille',
        'description': 'Maladie fongique avec des pustules orange sur les feuilles.',
        'emoji': '🍂',
        'cultures_cibles': ['Framboise', 'Mûre', 'Rosier', 'Ail', 'Poireau'],
        'temperature_min': 12,
        'temperature_max': 28,
        'humidite_min': 70,
        'humidite_max': 90,
        'precipitation_min': 5,
        'mois_debut': 4,
        'mois_fin': 10,
        'regions': ['tous'],
        'traitement_preventif': 'Soufre ou purin de prêle. Éviter l\'excès d\'azote.',
        'traitement_curatif': 'Fongicide spécifique anti-rouille. Supprimer les parties atteintes.',
        'produits_recommandes': ['Soufre', 'Purin de prêle', 'Fongicide anti-rouille'],
        'delai_alerte_jours': 4,
        'gravite': 'moyenne',
        'frequence_annuelle': 2,
    },
    {
        'nom': 'Pourriture grise (Botrytis)',
        'description': 'Pourriture grise sur les fruits et les tiges. Se développe par temps humide.',
        'emoji': '☁️',
        'cultures_cibles': ['Fraise', 'Tomate', 'Pommier', 'Framboise', 'Vigne'],
        'temperature_min': 15,
        'temperature_max': 25,
        'humidite_min': 75,
        'humidite_max': 100,
        'precipitation_min': 10,
        'mois_debut': 5,
        'mois_fin': 9,
        'regions': ['tous'],
        'traitement_preventif': 'Aération, éviter l\'excès d\'eau. Supprimer les fruits abîmés.',
        'traitement_curatif': 'Fongicide anti-botrytis. Éliminer les parties touchées.',
        'produits_recommandes': ['Fongicide anti-botrytis', 'Purins'],
        'delai_alerte_jours': 2,
        'gravite': 'elevee',
        'frequence_annuelle': 2,
    },
    {
        'nom': 'Alternariose',
        'description': 'Taches brunes concentriques sur les feuilles. Maladie de la chaleur.',
        'emoji': '🍂',
        'cultures_cibles': ['Tomate', 'Pomme de terre', 'Aubergine', 'Poivron'],
        'temperature_min': 20,
        'temperature_max': 35,
        'humidite_min': 50,
        'humidite_max': 70,
        'precipitation_min': 0,
        'precipitation_max': 10,
        'mois_debut': 6,
        'mois_fin': 9,
        'regions': ['provence', 'occitanie'],
        'traitement_preventif': 'Fongicide cuivre ou soufre. Rotation des cultures.',
        'traitement_curatif': 'Fongicide spécifique anti-alternaria.',
        'produits_recommandes': ['Cuivre', 'Soufre', 'Fongicide anti-alternaria'],
        'delai_alerte_jours': 4,
        'gravite': 'moyenne',
        'frequence_annuelle': 2,
    },
    {
        'nom': 'Cloque du pêcher',
        'description': 'Déformation et boursouflure des feuilles du pêcher.',
        'emoji': '🍑',
        'cultures_cibles': ['Pêche', 'Abricot', 'Amandier'],
        'temperature_min': 5,
        'temperature_max': 15,
        'humidite_min': 70,
        'humidite_max': 100,
        'precipitation_min': 10,
        'mois_debut': 2,
        'mois_fin': 4,
        'regions': ['tous'],
        'traitement_preventif': 'Bouillie bordelaise à la chute des feuilles et en fin d\'hiver.',
        'traitement_curatif': 'Supprimer les feuilles atteintes. Traitement fongicide spécifique.',
        'produits_recommandes': ['Bouillie bordelaise', 'Fongicide spécifique'],
        'delai_alerte_jours': 5,
        'gravite': 'moyenne',
        'frequence_annuelle': 1,
    },
    {
        'nom': 'Tavelure du pommier',
        'description': 'Taches olive sur les feuilles et les fruits du pommier.',
        'emoji': '🍎',
        'cultures_cibles': ['Pommier', 'Poire'],
        'temperature_min': 8,
        'temperature_max': 18,
        'humidite_min': 70,
        'humidite_max': 100,
        'precipitation_min': 5,
        'mois_debut': 3,
        'mois_fin': 6,
        'regions': ['tous'],
        'traitement_preventif': 'Soufre ou bouillie bordelaise en pré-floraison.',
        'traitement_curatif': 'Fongicide spécifique anti-tavelure.',
        'produits_recommandes': ['Soufre', 'Bouillie bordelaise', 'Fongicide anti-tavelure'],
        'delai_alerte_jours': 4,
        'gravite': 'moyenne',
        'frequence_annuelle': 2,
    },
]

print("\n" + "="*60)
print("🌱 ALIMENTATION DES MALADIES DES CULTURES")
print("="*60)

crees = 0
ignores = 0

for data in MALADIES_DATA:
    # Vérifier si la maladie existe déjà
    existant = MaladieCulture.objects.filter(nom__iexact=data['nom']).first()
    if existant:
        print(f"ℹ️ Maladie déjà existante : {existant.nom}")
        ignores += 1
    else:
        # Créer la maladie
        maladie = MaladieCulture.objects.create(
            nom=data['nom'],
            description=data['description'],
            emoji=data['emoji'],
            cultures_cibles=data['cultures_cibles'],
            temperature_min=data.get('temperature_min'),
            temperature_max=data.get('temperature_max'),
            humidite_min=data.get('humidite_min'),
            humidite_max=data.get('humidite_max'),
            precipitation_min=data.get('precipitation_min'),
            precipitation_max=data.get('precipitation_max'),
            mois_debut=data.get('mois_debut'),
            mois_fin=data.get('mois_fin'),
            regions=data.get('regions', ['tous']),
            traitement_preventif=data.get('traitement_preventif', ''),
            traitement_curatif=data.get('traitement_curatif', ''),
            produits_recommandes=data.get('produits_recommandes', []),
            delai_alerte_jours=data.get('delai_alerte_jours', 3),
            gravite=data.get('gravite', 'moyenne'),
            frequence_annuelle=data.get('frequence_annuelle', 1),
        )
        print(f"✅ Maladie créée : {maladie.emoji} {maladie.nom}")
        crees += 1

print("\n" + "="*60)
print(f"✅ Maladies créées : {crees}")
print(f"ℹ️ Maladies existantes : {ignores}")
print(f"📊 Total : {MaladieCulture.objects.count()}")
print("\n✅ Terminé !")