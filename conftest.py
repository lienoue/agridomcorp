"""
Fixtures partagées pour tous les tests d'Agriculture 2.0.

Convention : les fixtures sont nommées en snake_case, préfixées par leur
domaine quand utile (user_, figure_, culture_, calendrier_).
"""
import pytest
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.cache import cache


# ============================================================
# AUTO-USE : vide le cache avant chaque test
# ============================================================
@pytest.fixture(autouse=True)
def _clear_cache():
    """Vide le cache Django avant et après chaque test.

    Crucial car get_region_utilisateur, get_conseils_culture, etc.
    utilisent cache.set() avec des TTL longs (1h-24h).
    Sans ça, un test peut polluer le suivant.
    """
    cache.clear()
    yield
    cache.clear()


# ============================================================
# USERS
# ============================================================
User = get_user_model()


@pytest.fixture
def user_darkmaul(db):
    """Particulier majeur, abonnement Gratuit par défaut."""
    return User.objects.create_user(
        username='darkmaul',
        email='darkmaul@test.local',
        password='TestPass123!',
        birth_date=date(1990, 5, 15), # 35 ans
        location='France',
        tutoriel_termine=True,
    )


@pytest.fixture
def user_loulou(db):
    """Mineur (13 ans) — mode_junior auto-activé par signal post_save."""
    return User.objects.create_user(
        username='loulou',
        email='loulou@test.local',
        password='TestPass123!',
        birth_date=date.today() - timedelta(days=13 * 365 + 100),
        location='France',
        tutoriel_termine=True,
    )


@pytest.fixture
def user_kamdem(db):
    """Admin (staff)."""
    return User.objects.create_superuser(
        username='kamdem',
        email='kamdem@test.local',
        password='TestPass123!',
        birth_date=date(1985, 1, 1),
        location='France',
        tutoriel_termine=True,
    )


# ============================================================
# CLIENT HTTP
# ============================================================
@pytest.fixture
def client_anon(client):
    """Client Django anonyme (fourni par pytest-django)."""
    return client


@pytest.fixture
def client_darkmaul(client, user_darkmaul):
    """Client Django connecté en tant que Darkmaul."""
    client.force_login(user_darkmaul)
    return client


@pytest.fixture
def client_loulou(client, user_loulou):
    """Client Django connecté en tant que Loulou (mineur)."""
    client.force_login(user_loulou)
    return client


@pytest.fixture
def api_client_darkmaul(client_darkmaul):
    """Client prêt pour les endpoints JSON (CSRF désactivé pour les tests)."""
    from django.test import Client
    c = Client(enforce_csrf_checks=False)
    c.force_login(User.objects.get(username='darkmaul'))
    return c


# ============================================================
# FIGURES / PARCELLES
# ============================================================
@pytest.fixture
def figure_simple(db, user_darkmaul):
    """Une GeometricFigure avec un petit carré de 10m x 10m.

    Centre : Paris (48.8566, 2.3522).
    """
    from vegetables_fruits.models import GeometricFigure

    geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [2.3520, 48.8564],
                    [2.3524, 48.8564],
                    [2.3524, 48.8568],
                    [2.3520, 48.8568],
                    [2.3520, 48.8564],
                ]]
            },
            "properties": {"shape": "polygon"}
        }]
    }

    return GeometricFigure.objects.create(
        user=user_darkmaul,
        name='Parcelle Test',
        figure_type='maison',
        geojson_data=geojson,
        nb_points=4,
        adresse='Paris',
        adresse_lat=48.8566,
        adresse_lng=2.3522,
        adresse_formatted='Paris, France',
    )


# ============================================================
# CALENDRIER SEMIS (pour tester verifier_saison_culture)
# ============================================================
@pytest.fixture
def calendrier_tomate_iledefrance(db):
    """Tomate à iledefrance : fenêtre Mars-Mai (données réelles)."""
    from vegetables_fruits.models import CalendrierSemis
    return CalendrierSemis.objects.create(
        culture='Tomate',
        region='iledefrance',
        mois_debut_semis=3,
        mois_fin_semis=5,
        mois_debut_recolte=7,
        mois_fin_recolte=9,
        type_plantation='pleine_terre',
    )


@pytest.fixture
def calendrier_salade_iledefrance(db):
    """Salade à iledefrance : fenêtre Mars-Septembre."""
    from vegetables_fruits.models import CalendrierSemis
    return CalendrierSemis.objects.create(
        culture='Salade',
        region='iledefrance',
        mois_debut_semis=3,
        mois_fin_semis=9,
        mois_debut_recolte=5,
        mois_fin_recolte=11,
        type_plantation='pleine_terre',
    )


@pytest.fixture
def calendrier_tomate_tous(db):
    """Tomate fallback (region='tous') pour tester le lookup fallback."""
    from vegetables_fruits.models import CalendrierSemis
    return CalendrierSemis.objects.create(
        culture='Tomate',
        region='tous',
        mois_debut_semis=4,
        mois_fin_semis=6,
        mois_debut_recolte=7,
        mois_fin_recolte=9,
        type_plantation='pleine_terre',
    )


# ============================================================
# CULTURES / FRUITS / LÉGUMES / VARIÉTÉS
# ============================================================
@pytest.fixture
def culture_ananas(db):
    """Culture Ananas (parent) pour tester les variétés."""
    from vegetables_fruits.models import Culture
    return Culture.objects.create(
        nom='Ananas',
        type_culture='fruit',
        emoji='🍍',
        jours_pousse=365,
        besoin_eau_litres_jour=0.5,
    )


@pytest.fixture
def variete_cayenne(db, culture_ananas):
    """Variété Cayenne de l'Ananas (pour tester get_conseils_culture)."""
    from vegetables_fruits.models import Variete
    return Variete.objects.create(
        culture=culture_ananas,
        nom='Cayenne',
        emoji='🍍',
        description='Variété d\'ananas Cayenne',
    )


@pytest.fixture
def fruit_tomate(db):
    """Fruit Tomate simple pour les tests de crop."""
    from vegetables_fruits.models import Fruit
    return Fruit.objects.create(
        nom='Tomate',
        couleur='rouge',
        saison='ete',
        provenance='Amérique du Sud',
        prix=2.5,
        semis_interieur='Février-Mars',
        semis_exterieur='Avril-Mai',
        jours_levée=10,
        jours_recolte=90,
        temperature_min=15,
    )


@pytest.fixture
def vegetable_salade(db):
    """Légume Salade simple pour les tests de crop."""
    from vegetables_fruits.models import Vegetable
    return Vegetable.objects.create(
        nom='Salade',
        couleur='verte',
        saison='printemps',
        provenance='Europe',
        prix=1.5,
        semis_interieur='Février-Mars',
        semis_exterieur='Mars-Septembre',
        jours_levée=7,
        jours_recolte=45,
        temperature_min=10,
    )