"""
Tests de get_conseils_culture — validation du patch variété.
"""
import pytest

from vegetables_fruits.views import get_conseils_culture


# ============================================================
# RÉSOLUTION DU NOM (variété → parent)
# ============================================================
@pytest.mark.unit
def test_conseils_variete_remonte_au_parent(db, variete_cayenne):
    """get_conseils_culture('Cayenne') doit trouver via sa culture parente Ananas."""
    resultat = get_conseils_culture('Cayenne')

    assert resultat is not None
    assert resultat['est_generique'] is False
    assert resultat['nom'] == 'Ananas' # ← nom du parent, pas de la variété


@pytest.mark.unit
def test_conseils_variete_casse_insensible(db, variete_cayenne):
    """get_conseils_culture('cayenne') en minuscules doit aussi marcher."""
    resultat = get_conseils_culture('cayenne')
    assert resultat['est_generique'] is False
    assert resultat['nom'] == 'Ananas'


# ============================================================
# RECHERCHE DIRECTE
# ============================================================
@pytest.mark.unit
def test_conseils_culture_directe(db, culture_ananas):
    """get_conseils_culture('Ananas') — recherche directe dans Culture."""
    resultat = get_conseils_culture('Ananas')

    assert resultat is not None
    assert resultat['est_generique'] is False
    assert resultat['nom'] == 'Ananas'


@pytest.mark.unit
def test_conseils_fruit_direct(db, fruit_tomate):
    """get_conseils_culture('Tomate') — recherche dans Fruit."""
    resultat = get_conseils_culture('Tomate')

    assert resultat is not None
    assert resultat['est_generique'] is False
    assert resultat['nom'] == 'Tomate'


@pytest.mark.unit
def test_conseils_vegetable_direct(db, vegetable_salade):
    """get_conseils_culture('Salade') — recherche dans Vegetable."""
    resultat = get_conseils_culture('Salade')

    assert resultat is not None
    assert resultat['est_generique'] is False
    assert resultat['nom'] == 'Salade'


# ============================================================
# FALLBACK GÉNÉRIQUE
# ============================================================
@pytest.mark.unit
def test_conseils_culture_inconnue_fallback(db):
    """Culture bidon → conseils génériques."""
    resultat = get_conseils_culture('Plante Alien Zorglub')

    assert resultat is not None
    assert resultat['est_generique'] is True
    assert 'Plante Alien Zorglub' in resultat['nom']
    assert resultat['conseils_generaux'] is not None


@pytest.mark.unit
def test_conseils_nom_vide(db):
    """Culture vide → retourne None."""
    assert get_conseils_culture('') is None
    assert get_conseils_culture(None) is None
    assert get_conseils_culture(' ') is None # strip → vide


# ============================================================
# STRUCTURE DE LA RÉPONSE
# ============================================================
@pytest.mark.unit
def test_conseils_structure_complete(db, culture_ananas):
    """La réponse doit contenir tous les champs attendus."""
    resultat = get_conseils_culture('Ananas')

    champs_attendus = [
        'nom', 'famille', 'famille_emoji', 'est_generique',
        'temperature_min', 'temperature_optimale_min', 'temperature_optimale_max',
        'temperature_max', 'duree_culture_min_jours', 'duree_culture_max_jours',
        'methode_plantation', 'hivernage',
        'conseils_climat', 'conseils_plantation', 'conseils_arrosage',
        'conseils_fertilisation', 'conseils_protection',
        'conseils_recolte', 'conseils_conservation',
    ]
    for champ in champs_attendus:
        assert champ in resultat, f"Champ manquant : {champ}"
