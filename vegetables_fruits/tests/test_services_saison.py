"""
Tests du Chantier 27 — verifier_saison_culture.
"""
import pytest
from datetime import date

from vegetables_fruits.services import (
    verifier_saison_culture,
    verifier_saison_cultures,
    _resoudre_nom_culture,
)


# ============================================================
# _resoudre_nom_culture
# ============================================================
@pytest.mark.unit
def test_resoudre_nom_avec_fruit_id(db, fruit_tomate):
    """Résout le nom via fruit_id."""
    crop = {'fruit_id': fruit_tomate.id, 'name': 'Ignoré'}
    assert _resoudre_nom_culture(crop) == 'Tomate'


@pytest.mark.unit
def test_resoudre_nom_avec_vegetable_id(db, vegetable_salade):
    """Résout le nom via vegetable_id."""
    crop = {'vegetable_id': vegetable_salade.id, 'name': 'Ignoré'}
    assert _resoudre_nom_culture(crop) == 'Salade'


@pytest.mark.unit
def test_resoudre_nom_avec_variete(db, variete_cayenne):
    """Résout le nom via variete_id → remonte au parent."""
    crop = {'variete_id': variete_cayenne.id, 'name': 'Cayenne'}
    assert _resoudre_nom_culture(crop) == 'Ananas'


@pytest.mark.unit
def test_resoudre_nom_fallback_sur_name(db):
    """Fallback sur crop['name'] si aucun ID ne correspond."""
    crop = {'name': 'Culture Bidon'}
    assert _resoudre_nom_culture(crop) == 'Culture Bidon'


# ============================================================
# verifier_saison_culture
# ============================================================
@pytest.mark.saison
def test_culture_en_saison(db, fruit_tomate, calendrier_tomate_iledefrance):
    """Tomate en Avril → OK."""
    crop = {'fruit_id': fruit_tomate.id, 'name': 'Tomate'}
    resultat = verifier_saison_culture(crop, 'iledefrance', date(2026, 4, 15))

    assert resultat['ok'] is True
    assert resultat['raison'] == 'ok'
    assert resultat['fenetre'] == 'Mars - Mai'


@pytest.mark.saison
def test_culture_hors_saison(db, fruit_tomate, calendrier_tomate_iledefrance):
    """Tomate en Décembre → hors saison."""
    crop = {'fruit_id': fruit_tomate.id, 'name': 'Tomate'}
    resultat = verifier_saison_culture(crop, 'iledefrance', date(2026, 12, 15))

    assert resultat['ok'] is False
    assert resultat['raison'] == 'hors_saison'
    assert 'Mars - Mai' in resultat['fenetre']


@pytest.mark.saison
def test_culture_inconnue_pas_de_blocage(db):
    """Culture absente de CalendrierSemis → on ne bloque pas."""
    crop = {'name': 'Plante Alien'}
    resultat = verifier_saison_culture(crop, 'iledefrance', date(2026, 6, 1))

    assert resultat['ok'] is True
    assert resultat['raison'] == 'culture_inconnue'


@pytest.mark.saison
def test_fallback_region_tous(db, fruit_tomate, calendrier_tomate_tous):
    """Pas de Tomate à 'zimbabwe' → fallback sur region='tous'."""
    crop = {'fruit_id': fruit_tomate.id, 'name': 'Tomate'}
    resultat = verifier_saison_culture(crop, 'zimbabwe', date(2026, 5, 1))

    assert resultat['ok'] is True
    assert resultat['fenetre'] == 'Avril - Juin'


@pytest.mark.saison
def test_fenetre_a_cheval(db, fruit_tomate):
    """Test fenêtre qui wrap (Nov → Mars)."""
    from vegetables_fruits.models import CalendrierSemis
    CalendrierSemis.objects.create(
        culture='Tomate',
        region='iledefrance',
        mois_debut_semis=11,
        mois_fin_semis=3,
        mois_debut_recolte=6,
        mois_fin_recolte=8,
        type_plantation='pleine_terre',
    )

    crop = {'fruit_id': fruit_tomate.id, 'name': 'Tomate'}

    # Janvier → dans la fenêtre (11-3 wrap)
    r1 = verifier_saison_culture(crop, 'iledefrance', date(2026, 1, 15))
    assert r1['ok'] is True

    # Juin → hors fenêtre
    r2 = verifier_saison_culture(crop, 'iledefrance', date(2026, 6, 15))
    assert r2['ok'] is False


# ============================================================
# verifier_saison_cultures (batch)
# ============================================================
@pytest.mark.integration
def test_batch_mixte(db, user_darkmaul, fruit_tomate, vegetable_salade,
                     calendrier_tomate_iledefrance, calendrier_salade_iledefrance):
    """Batch : Tomate en Décembre (KO) + Salade en Juin (OK)."""
    crops = [
        {'fruit_id': fruit_tomate.id, 'name': 'Tomate', 'emoji': '🍅'},
        {'vegetable_id': vegetable_salade.id, 'name': 'Salade', 'emoji': '🥬'},
    ]

    # Astuce : on force la date via monkeypatch plus tard si besoin
    resultat = verifier_saison_cultures(
        crops, user_darkmaul, figure=None
    )

    # On vérifie juste la structure
    assert 'hors_saison' in resultat
    assert 'region' in resultat
    assert resultat['total_verifiees'] == 2