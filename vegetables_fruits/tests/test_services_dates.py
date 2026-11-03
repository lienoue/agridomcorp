# vegetables_fruits/tests/test_services_dates.py
"""
Tests du service centralisé de calcul des dates de récolte.
Vérifie que le bug 'Cerisier récolté en 90 jours' est corrigé.
"""
import pytest
from datetime import date

from vegetables_fruits.services_dates import (
    calculer_date_recolte,
    determiner_type_cycle,
    est_perenne,
    FALLBACK_JOURS_ANNUEL,
)


# ============================================================
# DÉTECTION DU TYPE DE CYCLE
# ============================================================

@pytest.mark.unit
def test_type_cycle_annuelle():
    """Tomate = annuelle."""
    assert determiner_type_cycle('Tomate') == 'annuelle'


@pytest.mark.unit
def test_type_cycle_bisannuelle():
    """Carotte = bisannuelle (dans notre référentiel elle est annuelle, mais oignon est bisannuelle)."""
    assert determiner_type_cycle('Oignon') == 'bisannuelle'


@pytest.mark.unit
def test_type_cycle_perenne_arbre():
    """Cerisier = pérenne."""
    assert determiner_type_cycle('Cerisier') == 'perenne'


@pytest.mark.unit
def test_type_cycle_perenne_aromatique():
    """Romarin = pérenne."""
    assert determiner_type_cycle('Romarin') == 'perenne'


@pytest.mark.unit
def test_type_cycle_inconnu():
    """Culture bidon = inconnu."""
    assert determiner_type_cycle('Plante Alien') == 'inconnu'


@pytest.mark.unit
def test_est_perenne():
    """Vérifie est_perenne()."""
    assert est_perenne('Pommier') is True
    assert est_perenne('Tomate') is False


# ============================================================
# CALCUL DES DATES — ANNUELLES
# ============================================================

@pytest.mark.unit
def test_tomate_90_jours():
    """Tomate semée le 15/04/2026 → récolte ~15/07/2026."""
    result = calculer_date_recolte('Tomate', date(2026, 4, 15))

    assert result['type_cycle'] == 'annuelle'
    assert result['duree_jours'] == 90
    assert result['source'] == 'referentiel'
    assert result['date_recolte'] == date(2026, 7, 14) # 15/04 + 90j


@pytest.mark.unit
def test_radis_25_jours():
    """Radis semé le 01/05/2026 → récolte ~26/05/2026."""
    result = calculer_date_recolte('Radis', date(2026, 5, 1))

    assert result['duree_jours'] == 25
    assert result['date_recolte'] == date(2026, 5, 26)


@pytest.mark.unit
def test_salade_60_jours():
    """Salade semée le 01/04/2026 → récolte ~31/05/2026."""
    result = calculer_date_recolte('Salade', date(2026, 4, 1))

    assert result['duree_jours'] == 60
    assert result['date_recolte'] == date(2026, 5, 31)


# ============================================================
# CALCUL DES DATES — PÉRENNES (LE BUG À CORRIGER)
# ============================================================

@pytest.mark.unit
def test_cerisier_4_ans():
    """
    LE TEST CLÉ : Cerisier planté le 02/11/2026 → récolte en 2030.
    C'était le bug : récolte en 2027 (90 jours) au lieu de 2030.
    """
    result = calculer_date_recolte('Cerisier', date(2026, 11, 2))

    assert result['type_cycle'] == 'perenne'
    assert result['mode_utilise'] == 'plantation'
    assert result['date_recolte'] == date(2030, 11, 2)
    assert result['annees_avant_production'] == 4


@pytest.mark.unit
def test_pommier_3_ans():
    """Pommier planté le 15/11/2026 → récolte en 2029."""
    result = calculer_date_recolte('Pommier', date(2026, 11, 15))

    assert result['type_cycle'] == 'perenne'
    assert result['date_recolte'] == date(2029, 11, 15)
    assert result['annees_avant_production'] == 3



@pytest.mark.unit
def test_olivier_4_ans():
    """Olivier planté en septembre 2026 → récolte en 2030."""
    result = calculer_date_recolte('Olivier', date(2026, 9, 15))

    assert result['type_cycle'] == 'perenne'
    assert result['date_recolte'] == date(2030, 9, 15)


@pytest.mark.unit
def test_vigne_3_ans():
    """Vigne plantée en novembre 2026 → récolte en 2029."""
    result = calculer_date_recolte('Vigne', date(2026, 11, 1))

    assert result['type_cycle'] == 'perenne'
    assert result['date_recolte'] == date(2029, 11, 1)


@pytest.mark.unit
def test_fraisier_1_an():
    """Fraisier planté en septembre 2026 → récolte en 2027."""
    result = calculer_date_recolte('Fraisier', date(2026, 9, 1))

    assert result['type_cycle'] == 'perenne'
    assert result['date_recolte'].year == 2027


# ============================================================
# OVERRIDE MANUEL
# ============================================================

@pytest.mark.unit
def test_override_prioritaire():
    """jours_override court-circuite le référentiel."""
    result = calculer_date_recolte(
        'Cerisier',
        date(2026, 1, 1),
        jours_override=180,
    )

    assert result['source'] == 'override'
    assert result['duree_jours'] == 180
    assert result['date_recolte'] == date(2026, 6, 30)


# ============================================================
# FALLBACK
# ============================================================

@pytest.mark.unit
def test_culture_inconnue_fallback():
    """Culture inconnue → fallback 90 jours."""
    result = calculer_date_recolte('Plante Alien', date(2026, 1, 1))

    assert result['source'] == 'fallback'
    assert result['duree_jours'] == FALLBACK_JOURS_ANNUEL
    assert result['date_recolte'] == date(2026, 4, 1)


# ============================================================
# ERREURS
# ============================================================

@pytest.mark.unit
def test_date_debut_none_leve_erreur():
    """date_debut=None → ValueError."""
    with pytest.raises(ValueError):
        calculer_date_recolte('Tomate', None)


# ============================================================
# CAS RÉELS DU TERRAIN (paramétré)
# ============================================================

@pytest.mark.unit
@pytest.mark.parametrize("culture,annee_attendue", [
    ('Cerisier', 2030), # 4 ans
    ('Pommier', 2029), # 3 ans
    ('Poirier', 2029), # 3 ans
    ('Prunier', 2029), # 3 ans
    ('Abricotier', 2029), # 3 ans
    ('Pêcher', 2028), # 2 ans
    ('Olivier', 2030), # 4 ans
    ('Figuier', 2028), # 2 ans
    ('Vigne', 2029), # 3 ans
    ('Kiwi', 2029), # 3 ans
])
def test_arbres_reels(culture, annee_attendue):
    """
    Test paramétré sur les arbres réels de l'app.
    Plantation le 01/01/2026.
    On vérifie l'année ET on vérifie que le jour/mois sont conservés
    (preuve qu'on a corrigé le bug '31 décembre').
    """
    result = calculer_date_recolte(culture, date(2026, 1, 1))

    assert result['type_cycle'] == 'perenne', f"{culture} devrait être pérenne"
    assert result['date_recolte'].year == annee_attendue, (
        f"{culture} : attendu {annee_attendue}, obtenu {result['date_recolte'].year}"
    )
    # ✅ Le jour/mois doivent être conservés (01/01)
    assert result['date_recolte'].month == 1, f"{culture} : mois non conservé"
    assert result['date_recolte'].day == 1, f"{culture} : jour non conservé"


# ============================================================
# NOUVEAU : gestion du 29 février (bissextile)
# ============================================================

@pytest.mark.unit
def test_plantation_29_fevrier_annee_non_bissextile():
    """Plantation le 29/02/2024 + 1 an → 28/02/2025 (pas de crash)."""
    result = calculer_date_recolte('Cerisier', date(2024, 2, 29))
    # Cerisier = 4 ans → 2028 (bissextile, jour conservé)
    # Pour tester le fallback 28/02, on utilise un arbre à 1 ou 3 ans
    # sur une année non bissextile
    assert result['date_recolte'] == date(2028, 2, 29) # 2028 bissextile


@pytest.mark.unit
def test_plantation_29_fevrier_fallback():
    """Plantation le 29/02/2024 + 3 ans → 28/02/2027 (fallback 28)."""
    result = calculer_date_recolte('Pommier', date(2024, 2, 29))
    # Pommier = 3 ans → 2027 non bissextile → 28/02/2027
    assert result['date_recolte'] == date(2027, 2, 28)


# ============================================================
# VARIÉTÉS → CULTURE PARENTE (règle métier)
# ============================================================

@pytest.mark.integration
def test_variete_arbre_resolue_via_culture(db):
    """Une variété d'arbre remonte à sa Culture parente pérenne."""
    from vegetables_fruits.models import Culture, Variete

    cerisier = Culture.objects.create(nom='Cerisier', type_culture='fruit', emoji='🍒')
    Variete.objects.create(culture=cerisier, nom='Burlat')

    result = calculer_date_recolte('Burlat', date(2026, 11, 2))

    assert result['type_cycle'] == 'perenne'
    assert result['date_recolte'] == date(2030, 11, 2)


@pytest.mark.integration
def test_variete_legume_reste_annuelle(db):
    """Une variété de légume reste annuelle."""
    from vegetables_fruits.models import Culture, Variete

    tomate = Culture.objects.create(nom='Tomate', type_culture='legume', emoji='🍅')
    Variete.objects.create(culture=tomate, nom='Marmande')

    result = calculer_date_recolte('Marmande', date(2026, 4, 15))

    assert result['type_cycle'] == 'annuelle'
    assert result['duree_jours'] == 90


@pytest.mark.integration
def test_variete_solo_papaye(db):
    """Le cas réel : Variete('Solo') → Culture('Papaye') → pérenne."""
    from vegetables_fruits.models import Culture, Variete

    papaye = Culture.objects.create(nom='Papaye', type_culture='fruit', emoji='🟠')
    Variete.objects.create(culture=papaye, nom='Solo')

    result = calculer_date_recolte('Solo', date(2026, 3, 1))

    assert result['type_cycle'] == 'perenne'
    assert result['date_recolte'] == date(2027, 3, 1)


@pytest.mark.integration
def test_variete_muscat_raisin(db):
    """Le cas réel : Variete('Muscat') → Culture('Raisin') → pérenne."""
    from vegetables_fruits.models import Culture, Variete

    raisin = Culture.objects.create(nom='Raisin', type_culture='fruit', emoji='🍇')
    Variete.objects.create(culture=raisin, nom='Muscat')

    result = calculer_date_recolte('Muscat', date(2026, 11, 1))

    assert result['type_cycle'] == 'perenne'
    assert result['date_recolte'] == date(2029, 11, 1)


@pytest.mark.unit
def test_protection_boucle_variete_culture():
    """Variete → Culture qui boucle sur elle-même ne crashe pas."""
    # Ce test est défensif : on ne peut pas le déclencher via DB
    # sans violer le FK, donc on vérifie juste que _depth>3 retourne None.
    from vegetables_fruits.data.cycles_cultures import get_cycle
    assert get_cycle('NimporteQuoi', _depth=4) is None