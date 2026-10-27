# scenario_test_complet.py
# Exécution : python manage.py shell
# Puis : exec(open('scenario_test_complet.py', encoding='utf-8').read())

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriculture.settings')
django.setup()

from vegetables_fruits.models import (
    CustomUser, GeometricFigure, Parcelle, ChronologieCulture,
    Classe, Eleve, Abonnement, PlanTarification
)
from django.utils import timezone
from datetime import timedelta, date


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def creer_utilisateur(username, email, password, birth_date=None, is_enseignant=False, is_active=True):
    """Crée un utilisateur avec les bonnes dates"""
    user, created = CustomUser.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'is_active': is_active,
            'is_enseignant': is_enseignant,
            'birth_date': birth_date,
        }
    )
    if created:
        user.set_password(password)
        user.save()
        print(f" ✅ Utilisateur créé : {username} (né le {birth_date})")
    else:
        print(f" ℹ️ Utilisateur existant : {username}")
    return user


def creer_parcelle(user, nom, adresse, lat, lng, pays, surface=0.05):
    """Crée une parcelle avec coordonnées précises"""

    # ✅ GeoJSON correct avec un Point
    geojson_data = {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [lng, lat]  # GeoJSON utilise [lng, lat]
            },
            'properties': {}
        }]
    }

    figure = GeometricFigure.objects.create(
        user=user,
        name=nom,
        figure_type='parcelle_agricole',
        geojson_data=geojson_data,
        adresse=f"{adresse}, {pays}",
        adresse_lat=lat,
        adresse_lng=lng,
        surface_hectares=surface
    )

    parcelle = Parcelle.objects.create(
        nom=nom,
        utilisateur=user,
        figure=figure,
        surface_m2=surface * 10000,
        type_sol='limoneux',
        exposition='plein_soleil'
    )

    return parcelle, figure


def creer_culture(figure, nom_culture, statut, jours_ecoules, emoji='🌱'):
    """Crée une culture à un stade spécifique et l'ajoute dans figure.crops"""

    # 1. Créer la chronologie
    date_semis = timezone.now() - timedelta(days=jours_ecoules)
    date_recolte_prevue = date_semis + timedelta(days=90)

    chrono = ChronologieCulture.objects.create(
        figure=figure,
        culture_nom=nom_culture,
        culture_emoji=emoji,
        date_semis=date_semis,
        date_recolte_prevue=date_recolte_prevue,
        statut=statut,
        progression=min(100, int((jours_ecoules / 90) * 100))
    )

    if statut == 'recolte':
        chrono.date_recolte_effective = timezone.now()
        chrono.points_gagnes = 10
        chrono.save()

    # 2. ✅ AJOUTER DANS figure.crops (le champ JSON)
    # Vérifier si figure.crops existe, sinon l'initialiser
    if not figure.crops:
        figure.crops = []

    # Ajouter la culture
    figure.crops.append({
        'name': nom_culture,
        'emoji': emoji,
        'type': 'vegetable',
        'date_placement': timezone.now().isoformat(),
        'lat': figure.adresse_lat or 0,
        'lng': figure.adresse_lng or 0,
        'statut': statut,
        'progression': chrono.progression,
    })
    figure.save()

    return chrono


def creer_abonnement(user, plan_nom):
    """Crée un abonnement pour un utilisateur"""
    plan = PlanTarification.objects.get(nom=plan_nom)
    abonnement, created = Abonnement.objects.get_or_create(
        utilisateur=user,
        defaults={
            'plan': plan,
            'statut': 'ACTIF',
            'frequence': 'MENSUEL',
            'date_debut': timezone.now(),
        }
    )
    if created:
        print(f" ✅ Abonnement {plan_nom} créé")
    else:
        abonnement.plan = plan
        abonnement.save()
        print(f" ✅ Abonnement mis à jour vers {plan_nom}")
    return abonnement


# ============================================================
# PROFIL 1 : PARTICULIER MAJEUR SANS ABONNEMENT
# ============================================================

def creer_particulier_sans_abo():
    print("\n" + "=" * 60)
    print("👤 PROFIL 1 : PARTICULIER MAJEUR SANS ABONNEMENT")
    print("=" * 60)

    # Âge : 35 ans
    birth_date = date(1991, 6, 15)

    user = creer_utilisateur(
        username='particulier_sans_abo',
        email='particulier.sansabo@test.com',
        password='test123',
        birth_date=birth_date,
        is_enseignant=False
    )

    # Pas d'abonnement
    print(f" ℹ️ Aucun abonnement (plan Gratuit)")

    # Parcelle en France (Paris)
    parcelle, figure = creer_parcelle(
        user=user,
        nom='Mon jardin parisien',
        adresse='12 rue de Rivoli',
        lat=48.8588,
        lng=2.3470,
        pays='France'
    )
    print(f" ✅ Parcelle créée : Paris, France")

    # Cultures
    cultures = [
        ('Tomate', 'croissance', 30, '🍅'),
        ('Carotte', 'levee', 10, '🥕'),
        ('Salade', 'pret', 70, '🥬'),
    ]
    for nom, statut, jours, emoji in cultures:
        creer_culture(figure, nom, statut, jours, emoji)

    print(f"\n 🔑 Identifiant : particulier_sans_abo")
    print(f" 🔐 Mot de passe : test123")
    return user


# ============================================================
# PROFIL 2 : PARTICULIER MAJEUR AVEC ABONNEMENT PREMIUM
# ============================================================

def creer_particulier_premium():
    print("\n" + "=" * 60)
    print("👤 PROFIL 2 : PARTICULIER MAJEUR AVEC ABONNEMENT PREMIUM")
    print("=" * 60)

    # Âge : 42 ans
    birth_date = date(1984, 3, 10)

    user = creer_utilisateur(
        username='particulier_premium',
        email='particulier.premium@test.com',
        password='test123',
        birth_date=birth_date,
        is_enseignant=False
    )

    # Abonnement Premium
    creer_abonnement(user, 'PREMIUM')

    # Parcelle au Japon (Tokyo)
    parcelle, figure = creer_parcelle(
        user=user,
        nom='Jardin tokyoïte',
        adresse='1-1-1 Shibuya',
        lat=35.6595,
        lng=139.7004,
        pays='Japon'
    )
    print(f" ✅ Parcelle créée : Tokyo, Japon")

    # Cultures
    cultures = [
        ('Tomate', 'floraison', 45, '🍅'),
        ('Poivron', 'croissance', 25, '🫑'),
        ('Aubergine', 'floraison', 40, '🍆'),
        ('Fraise', 'recolte', 85, '🍓'),
        ('Cerise', 'fructification', 55, '🍒'),
    ]
    for nom, statut, jours, emoji in cultures:
        creer_culture(figure, nom, statut, jours, emoji)

    print(f"\n 🔑 Identifiant : particulier_premium")
    print(f" 🔐 Mot de passe : test123")
    return user


# ============================================================
# PROFIL 3 : ENSEIGNANT AVEC CLASSE
# ============================================================

def creer_enseignant():
    print("\n" + "=" * 60)
    print("👨‍🏫 PROFIL 3 : ENSEIGNANT AVEC CLASSE")
    print("=" * 60)

    # Âge : 45 ans
    birth_date = date(1981, 9, 5)

    user = creer_utilisateur(
        username='enseignant_test',
        email='enseignant@test.com',
        password='test123',
        birth_date=birth_date,
        is_enseignant=True
    )

    # Abonnement Enseignant
    creer_abonnement(user, 'ENSEIGNANT')

    # Créer une classe
    classe, created = Classe.objects.get_or_create(
        nom='Classe de SVT - 4ème',
        enseignant=user
    )
    if created:
        print(f" ✅ Classe créée : {classe.nom} (code: {classe.code})")
    else:
        print(f" ℹ️ Classe existante : {classe.nom}")

    # Parcelle aux États-Unis (New York)
    parcelle, figure = creer_parcelle(
        user=user,
        nom='Jardin pédagogique de Brooklyn',
        adresse='100 Bedford Ave',
        lat=40.7128,
        lng=-74.0060,
        pays='USA'
    )
    print(f" ✅ Parcelle créée : New York, USA")

    # Cultures
    cultures = [
        ('Tomate', 'floraison', 45, '🍅'),
        ('Courgette', 'croissance', 30, '🥒'),
        ('Poivron', 'floraison', 40, '🫑'),
        ('Haricot', 'recolte', 90, '🫘'),
        ('Pommier', 'fructification', 60, '🍎'),
    ]
    for nom, statut, jours, emoji in cultures:
        creer_culture(figure, nom, statut, jours, emoji)

    print(f"\n 🔑 Identifiant : enseignant_test")
    print(f" 🔐 Mot de passe : test123")
    print(f" 🏫 Code classe : {classe.code}")
    return user, classe


# ============================================================
# PROFIL 4 : MINEUR DANS LA CLASSE DE L'ENSEIGNANT
# ============================================================

def creer_mineur(enseignant_classe):
    print("\n" + "=" * 60)
    print("🧒 PROFIL 4 : MINEUR (élève dans la classe)")
    print("=" * 60)

    # Âge : 13 ans
    birth_date = date(2013, 11, 20)

    user = creer_utilisateur(
        username='eleve_mineur',
        email='eleve.mineur@test.com',
        password='test123',
        birth_date=birth_date,
        is_enseignant=False
    )

    # Créer le profil élève et l'associer à la classe
    eleve, created = Eleve.objects.get_or_create(
        user=user,
        defaults={
            'classe': enseignant_classe,
            'points': 0,
            'niveau': 1
        }
    )
    if not created:
        eleve.classe = enseignant_classe
        eleve.save()

    if created:
        print(f" ✅ Élève créé et associé à la classe : {enseignant_classe.nom}")
    else:
        print(f" ℹ️ Élève existant : {user.username}")

    # Pas d'abonnement (le profil élève est automatiquement Junior)
    print(f" ℹ️ Mode Junior activé automatiquement")

    # Parcelle en Afrique (Sénégal - Dakar)
    parcelle, figure = creer_parcelle(
        user=user,
        nom='Mon jardin africain',
        adresse='Route de l\'Ouest',
        lat=14.7167,
        lng=-17.4677,
        pays='Sénégal'
    )
    print(f" ✅ Parcelle créée : Dakar, Sénégal")

    # Cultures (simples pour un enfant)
    cultures = [
        ('Radis', 'recolte', 30, '🌱'),
        ('Carotte', 'croissance', 20, '🥕'),
        ('Tomate', 'seme', 3, '🍅'),
        ('Salade', 'pret', 70, '🥬'),
        ('Fraise', 'levee', 8, '🍓'),
    ]
    for nom, statut, jours, emoji in cultures:
        creer_culture(figure, nom, statut, jours, emoji)

    # Ajouter des points pour le mode junior
    eleve.points = 150
    eleve.niveau = 2
    eleve.save()
    print(f" ✅ Points ajoutés : 150 (niveau 2)")

    print(f"\n 🔑 Identifiant : eleve_mineur")
    print(f" 🔐 Mot de passe : test123")
    return user, eleve


# ============================================================
# PROFIL 5 : PARTICULIER AUSTRALIE (sans abonnement)
# ============================================================

def creer_particulier_australie():
    print("\n" + "=" * 60)
    print("🌏 PROFIL 5 : PARTICULIER - AUSTRALIE (sans abonnement)")
    print("=" * 60)

    # Âge : 28 ans
    birth_date = date(1998, 2, 14)

    user = creer_utilisateur(
        username='particulier_australie',
        email='australie@test.com',
        password='test123',
        birth_date=birth_date,
        is_enseignant=False
    )

    # Pas d'abonnement (Gratuit)
    print(f" ℹ️ Aucun abonnement (plan Gratuit)")

    # Parcelle en Australie (Sydney)
    parcelle, figure = creer_parcelle(
        user=user,
        nom='Mon jardin australien',
        adresse='1 George Street',
        lat=-33.8688,
        lng=151.2093,
        pays='Australie'
    )
    print(f" ✅ Parcelle créée : Sydney, Australie")

    # Cultures
    cultures = [
        ('Tomate', 'croissance', 25, '🍅'),
        ('Carotte', 'levee', 10, '🥕'),
        ('Basilic', 'croissance', 15, '🌿'),
    ]
    for nom, statut, jours, emoji in cultures:
        creer_culture(figure, nom, statut, jours, emoji)

    print(f"\n 🔑 Identifiant : particulier_australie")
    print(f" 🔐 Mot de passe : test123")
    return user


# ============================================================
# EXÉCUTION PRINCIPALE
# ============================================================

print("\n" + "=" * 60)
print("🌍 CRÉATION DES 5 PROFILS DE TEST (MONDE ENTIER)")
print("=" * 60)

# 1. Particulier sans abonnement (Paris, France)
particulier_sans_abo = creer_particulier_sans_abo()

# 2. Particulier Premium (Tokyo, Japon)
particulier_premium = creer_particulier_premium()

# 3. Enseignant avec classe (New York, USA)
enseignant_user, enseignant_classe = creer_enseignant()

# 4. Mineur dans la classe (Dakar, Sénégal)
mineur_user, mineur_eleve = creer_mineur(enseignant_classe)

# 5. Particulier Australie (Sydney, Australie)
particulier_australie = creer_particulier_australie()

# ============================================================
# RÉSUMÉ FINAL
# ============================================================

print("\n" + "=" * 60)
print("📊 RÉSUMÉ DES 5 PROFILS")
print("=" * 60)

profils = [
    ("👤 Particulier sans abonnement", "particulier_sans_abo", "test123", "Paris, France", "Gratuit", "Majeur (35 ans)"),
    ("👤 Particulier Premium", "particulier_premium", "test123", "Tokyo, Japon", "Premium", "Majeur (42 ans)"),
    ("👨‍🏫 Enseignant", "enseignant_test", "test123", "New York, USA", "Enseignant", "Majeur (45 ans)"),
    ("🧒 Élève mineur", "eleve_mineur", "test123", "Dakar, Sénégal", "Junior", "Mineur (13 ans)"),
    ("🌏 Particulier Australie", "particulier_australie", "test123", "Sydney, Australie", "Gratuit", "Majeur (28 ans)"),
]

for profil, username, password, ville, abonnement, age in profils:
    print(f"\n{profil}")
    print(f" 🔑 Identifiant : {username}")
    print(f" 🔐 Mot de passe : {password}")
    print(f" 📍 Ville : {ville}")
    print(f" 💰 Abonnement : {abonnement}")
    print(f" 🎂 {age}")

print("\n" + "=" * 60)
print("✅ Scénario de test complet prêt !")
print("=" * 60)
print("\n🌍 Parcelles réparties sur 4 continents :")
print(" - Europe : Paris 🇫🇷")
print(" - Asie : Tokyo 🇯🇵")
print(" - Amérique : New York 🇺🇸")
print(" - Afrique : Dakar 🇸🇳")
print(" - Océanie : Sydney 🇦🇺")