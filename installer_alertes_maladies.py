# vegetables_fruits/management/commands/installer_alertes_maladies.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from vegetables_fruits.models import (
    MaladieCulture,
    ChronologieCulture,
    Culture
)

# ==================== DONNÉES DES MALADIES AVEC STADES ====================

MALADIES_DATA = [
    {
        'nom': 'Mildiou',
        'nom_scientifique': 'Phytophthora infestans',
        'description': 'Maladie fongique due à l\'humidité excessive. Se manifeste par des taches jaunes sur les feuilles, puis brunes.',
        'emoji': '🦠',
        'cultures_cibles': ['Tomate', 'Pomme de terre', 'Vigne', 'Concombre', 'Courgette', 'Aubergine'],
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
        'stades_sensibles': ['floraison', 'fructification', 'croissance'],
        'risque_par_stade': {
            'seme': 'faible',
            'levee': 'faible',
            'croissance': 'moyenne',
            'floraison': 'elevee',
            'fructification': 'elevee',
            'pret': 'moyenne',
            'recolte': 'faible',
        },
    },
    {
        'nom': 'Oïdium',
        'nom_scientifique': 'Erysiphe cichoracearum',
        'description': 'Champignon blanc poudreux sur les feuilles. Se développe par temps sec et chaud.',
        'emoji': '🫧',
        'cultures_cibles': ['Courgette', 'Concombre', 'Fraise', 'Vigne', 'Tomate', 'Pommier', 'Rosier'],
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
        'stades_sensibles': ['croissance', 'floraison', 'fructification'],
        'risque_par_stade': {
            'seme': 'faible',
            'levee': 'faible',
            'croissance': 'moyenne',
            'floraison': 'elevee',
            'fructification': 'moyenne',
            'pret': 'faible',
            'recolte': 'faible',
        },
    },
    {
        'nom': 'Mildiou de la pomme de terre',
        'nom_scientifique': 'Phytophthora infestans',
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
        'stades_sensibles': ['croissance', 'floraison', 'fructification'],
        'risque_par_stade': {
            'seme': 'faible',
            'levee': 'faible',
            'croissance': 'moyenne',
            'floraison': 'elevee',
            'fructification': 'critique',
            'pret': 'elevee',
            'recolte': 'faible',
        },
    },
    {
        'nom': 'Rouille',
        'nom_scientifique': 'Puccinia spp.',
        'description': 'Maladie fongique avec des pustules orange sur les feuilles.',
        'emoji': '🍂',
        'cultures_cibles': ['Framboise', 'Mûre', 'Rosier', 'Ail', 'Poireau', 'Haricot'],
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
        'stades_sensibles': ['croissance', 'floraison', 'fructification'],
        'risque_par_stade': {
            'seme': 'faible',
            'levee': 'faible',
            'croissance': 'moyenne',
            'floraison': 'moyenne',
            'fructification': 'moyenne',
            'pret': 'faible',
            'recolte': 'faible',
        },
    },
    {
        'nom': 'Pourriture grise (Botrytis)',
        'nom_scientifique': 'Botrytis cinerea',
        'description': 'Pourriture grise sur les fruits et les tiges. Se développe par temps humide.',
        'emoji': '☁️',
        'cultures_cibles': ['Fraise', 'Tomate', 'Pommier', 'Framboise', 'Vigne', 'Framboise'],
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
        'stades_sensibles': ['floraison', 'fructification', 'pret'],
        'risque_par_stade': {
            'seme': 'faible',
            'levee': 'faible',
            'croissance': 'faible',
            'floraison': 'moyenne',
            'fructification': 'elevee',
            'pret': 'elevee',
            'recolte': 'moyenne',
        },
    },
    {
        'nom': 'Alternariose',
        'nom_scientifique': 'Alternaria solani',
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
        'regions': ['provence', 'occitanie', 'corse'],
        'traitement_preventif': 'Fongicide cuivre ou soufre. Rotation des cultures.',
        'traitement_curatif': 'Fongicide spécifique anti-alternaria.',
        'produits_recommandes': ['Cuivre', 'Soufre', 'Fongicide anti-alternaria'],
        'delai_alerte_jours': 4,
        'gravite': 'moyenne',
        'frequence_annuelle': 2,
        'stades_sensibles': ['floraison', 'fructification', 'pret'],
        'risque_par_stade': {
            'seme': 'faible',
            'levee': 'faible',
            'croissance': 'faible',
            'floraison': 'moyenne',
            'fructification': 'moyenne',
            'pret': 'faible',
            'recolte': 'faible',
        },
    },
    {
        'nom': 'Cloque du pêcher',
        'nom_scientifique': 'Taphrina deformans',
        'description': 'Déformation et boursouflure des feuilles du pêcher.',
        'emoji': '🍑',
        'cultures_cibles': ['Pêche', 'Abricot', 'Amandier', 'Nectarine'],
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
        'stades_sensibles': ['seme', 'levee', 'croissance'],
        'risque_par_stade': {
            'seme': 'moyenne',
            'levee': 'elevee',
            'croissance': 'moyenne',
            'floraison': 'faible',
            'fructification': 'faible',
            'pret': 'faible',
            'recolte': 'faible',
        },
    },
    {
        'nom': 'Tavelure du pommier',
        'nom_scientifique': 'Venturia inaequalis',
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
        'stades_sensibles': ['croissance', 'floraison', 'fructification'],
        'risque_par_stade': {
            'seme': 'faible',
            'levee': 'faible',
            'croissance': 'moyenne',
            'floraison': 'elevee',
            'fructification': 'moyenne',
            'pret': 'faible',
            'recolte': 'faible',
        },
    },
    {
        'nom': 'Verticilliose',
        'nom_scientifique': 'Verticillium dahliae',
        'description': 'Flétrissement des feuilles et pourriture des racines.',
        'emoji': '🌿',
        'cultures_cibles': ['Tomate', 'Pomme de terre', 'Poivron', 'Aubergine', 'Fraise', 'Framboise'],
        'temperature_min': 18,
        'temperature_max': 30,
        'humidite_min': 40,
        'humidite_max': 70,
        'precipitation_min': 0,
        'precipitation_max': 5,
        'mois_debut': 6,
        'mois_fin': 9,
        'regions': ['tous'],
        'traitement_preventif': 'Solarisation du sol, rotation des cultures. Utiliser des plants résistants.',
        'traitement_curatif': 'Éliminer les plants atteints. Traitement fongicide spécifique.',
        'produits_recommandes': ['Solarisation', 'Plants résistants'],
        'delai_alerte_jours': 5,
        'gravite': 'elevee',
        'frequence_annuelle': 1,
        'stades_sensibles': ['croissance', 'floraison', 'fructification'],
        'risque_par_stade': {
            'seme': 'faible',
            'levee': 'faible',
            'croissance': 'moyenne',
            'floraison': 'elevee',
            'fructification': 'elevee',
            'pret': 'moyenne',
            'recolte': 'faible',
        },
    },
    {
        'nom': 'Anthracnose',
        'nom_scientifique': 'Colletotrichum spp.',
        'description': 'Taches brunes sur les fruits et les feuilles. Pourriture.',
        'emoji': '🟤',
        'cultures_cibles': ['Fraise', 'Framboise', 'Mûre', 'Tomate', 'Poivron'],
        'temperature_min': 18,
        'temperature_max': 30,
        'humidite_min': 70,
        'humidite_max': 95,
        'precipitation_min': 5,
        'mois_debut': 5,
        'mois_fin': 9,
        'regions': ['tous'],
        'traitement_preventif': 'Cuivre ou soufre. Éviter l\'excès d\'humidité.',
        'traitement_curatif': 'Fongicide spécifique anti-anthracnose.',
        'produits_recommandes': ['Cuivre', 'Soufre', 'Fongicide anti-anthracnose'],
        'delai_alerte_jours': 3,
        'gravite': 'elevee',
        'frequence_annuelle': 2,
        'stades_sensibles': ['floraison', 'fructification', 'pret'],
        'risque_par_stade': {
            'seme': 'faible',
            'levee': 'faible',
            'croissance': 'faible',
            'floraison': 'moyenne',
            'fructification': 'elevee',
            'pret': 'elevee',
            'recolte': 'moyenne',
        },
    },
    {
        'nom': 'Septoriose',
        'nom_scientifique': 'Septoria lycopersici',
        'description': 'Taches grises sur les feuilles de tomate.',
        'emoji': '⚪',
        'cultures_cibles': ['Tomate', 'Pomme de terre'],
        'temperature_min': 15,
        'temperature_max': 28,
        'humidite_min': 70,
        'humidite_max': 90,
        'precipitation_min': 5,
        'mois_debut': 5,
        'mois_fin': 9,
        'regions': ['tous'],
        'traitement_preventif': 'Cuivre ou soufre. Rotation des cultures.',
        'traitement_curatif': 'Fongicide spécifique anti-septoriose.',
        'produits_recommandes': ['Cuivre', 'Soufre', 'Fongicide anti-septoriose'],
        'delai_alerte_jours': 4,
        'gravite': 'moyenne',
        'frequence_annuelle': 2,
        'stades_sensibles': ['croissance', 'floraison', 'fructification'],
        'risque_par_stade': {
            'seme': 'faible',
            'levee': 'faible',
            'croissance': 'moyenne',
            'floraison': 'moyenne',
            'fructification': 'moyenne',
            'pret': 'faible',
            'recolte': 'faible',
        },
    },
    {
        'nom': 'Moniliose',
        'nom_scientifique': 'Monilinia spp.',
        'description': 'Pourriture brune des fruits à noyau.',
        'emoji': '🍑',
        'cultures_cibles': ['Pêche', 'Abricot', 'Cerise', 'Prune', 'Nectarine'],
        'temperature_min': 12,
        'temperature_max': 25,
        'humidite_min': 70,
        'humidite_max': 100,
        'precipitation_min': 5,
        'mois_debut': 4,
        'mois_fin': 8,
        'regions': ['tous'],
        'traitement_preventif': 'Soufre ou bouillie bordelaise en pré-floraison.',
        'traitement_curatif': 'Supprimer les fruits atteints. Fongicide spécifique.',
        'produits_recommandes': ['Soufre', 'Bouillie bordelaise', 'Fongicide anti-moniliose'],
        'delai_alerte_jours': 4,
        'gravite': 'elevee',
        'frequence_annuelle': 2,
        'stades_sensibles': ['floraison', 'fructification', 'pret'],
        'risque_par_stade': {
            'seme': 'faible',
            'levee': 'faible',
            'croissance': 'faible',
            'floraison': 'moyenne',
            'fructification': 'elevee',
            'pret': 'elevee',
            'recolte': 'moyenne',
        },
    },
]


class Command(BaseCommand):
    help = 'Installe les maladies des cultures avec leurs stades sensibles'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("\n" + "="*60))
        self.stdout.write(self.style.SUCCESS("🌱 INSTALLATION DES MALADIES DES CULTURES"))
        self.stdout.write(self.style.SUCCESS("="*60 + "\n"))

        # 1. Mettre à jour les modèles (les migrations doivent être faites avant)
        self.stdout.write("📌 Étape 1 : Vérification des champs stades...")
        self.stdout.write(" ℹ️ Assurez-vous que les migrations sont appliquées :")
        self.stdout.write(" python manage.py makemigrations")
        self.stdout.write(" python manage.py migrate\n")

        # 2. Alimenter les maladies
        self.stdout.write("📌 Étape 2 : Alimentation des maladies...")
        crees = 0
        existantes = 0

        for data in MALADIES_DATA:
            maladie, created = MaladieCulture.objects.get_or_create(
                nom=data['nom'],
                defaults={
                    'nom_scientifique': data.get('nom_scientifique', ''),
                    'description': data['description'],
                    'emoji': data['emoji'],
                    'cultures_cibles': data['cultures_cibles'],
                    'temperature_min': data.get('temperature_min'),
                    'temperature_max': data.get('temperature_max'),
                    'humidite_min': data.get('humidite_min'),
                    'humidite_max': data.get('humidite_max'),
                    'precipitation_min': data.get('precipitation_min'),
                    'precipitation_max': data.get('precipitation_max'),
                    'mois_debut': data.get('mois_debut'),
                    'mois_fin': data.get('mois_fin'),
                    'regions': data.get('regions', ['tous']),
                    'traitement_preventif': data.get('traitement_preventif', ''),
                    'traitement_curatif': data.get('traitement_curatif', ''),
                    'produits_recommandes': data.get('produits_recommandes', []),
                    'delai_alerte_jours': data.get('delai_alerte_jours', 3),
                    'gravite': data.get('gravite', 'moyenne'),
                    'frequence_annuelle': data.get('frequence_annuelle', 1),
                    'stades_sensibles': data.get('stades_sensibles', []),
                    'risque_par_stade': data.get('risque_par_stade', {}),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f" ✅ {maladie.emoji} {maladie.nom}"))
                crees += 1
            else:
                # Mettre à jour si besoin
                updated = False
                if maladie.stades_sensibles != data.get('stades_sensibles', []):
                    maladie.stades_sensibles = data.get('stades_sensibles', [])
                    updated = True
                if maladie.risque_par_stade != data.get('risque_par_stade', {}):
                    maladie.risque_par_stade = data.get('risque_par_stade', {})
                    updated = True
                if updated:
                    maladie.save()
                    self.stdout.write(self.style.WARNING(f" 🔄 {maladie.emoji} {maladie.nom} (mis à jour)"))
                    existantes += 1
                else:
                    self.stdout.write(f" ℹ️ {maladie.emoji} {maladie.nom} (déjà existante)")
                    existantes += 1

        # 3. Mettre à jour les chronologies avec le stade actuel
        self.stdout.write("\n📌 Étape 3 : Mise à jour des stades des cultures...")
        chronologies = ChronologieCulture.objects.all()
        mises_a_jour = 0

        for chrono in chronologies:
            # Récupérer le stade depuis la progression
            if not chrono.stade_actuel:
                # Définir le stade à partir du statut
                stade_map = {
                    'seme': 'seme',
                    'levee': 'levee',
                    'croissance': 'croissance',
                    'floraison': 'floraison',
                    'fructification': 'fructification',
                    'pret': 'pret',
                    'recolte': 'recolte',
                }
                chrono.stade_actuel = stade_map.get(chrono.statut, 'seme')
                chrono.save()
                mises_a_jour += 1

        self.stdout.write(self.style.SUCCESS(f" ✅ {mises_a_jour} chronologie(s) mises à jour"))

        # 4. Résumé
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS("📊 RÉSUMÉ"))
        self.stdout.write("="*60)
        self.stdout.write(f"✅ Maladies créées : {crees}")
        self.stdout.write(f"ℹ️ Maladies existantes : {existantes}")
        self.stdout.write(f"📊 Total maladies : {MaladieCulture.objects.count()}")
        self.stdout.write(f"📊 Chronologies mises à jour : {mises_a_jour}")
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS("✅ Installation terminée !"))
        self.stdout.write("="*60 + "\n")