"""
Tests du service économie.
"""
import pytest
from datetime import date, timedelta

from vegetables_fruits.models import RendementCulture, ChronologieCulture
from vegetables_fruits.services_economie import (
    calculer_valeur_jardin,
    _get_prix,
    _get_rendement,
)


# ============================================================
# _get_prix
# ============================================================
@pytest.mark.unit
def test_get_prix_fruit(db, fruit_tomate):
    """Prix via Fruit."""
    assert _get_prix('Tomate') == 2.5


@pytest.mark.unit
def test_get_prix_vegetable(db, vegetable_salade):
    """Prix via Vegetable."""
    assert _get_prix('Salade') == 1.5


@pytest.mark.unit
def test_get_prix_inconnu(db):
    """Culture inconnue → 0."""
    assert _get_prix('Plante Alien') == 0.0


# ============================================================
# _get_rendement
# ============================================================
@pytest.mark.unit
def test_get_rendement_trouve(db):
    """Rendement trouvé pour 'tomate'."""
    RendementCulture.objects.create(
        culture_nom='tomate', rendement_kg_par_plant=2.5,
        region_climatique='tous', source='fao'
    )
    assert _get_rendement('tomate') == 2.5


@pytest.mark.unit
def test_get_rendement_fallback(db):
    """Culture absente → fallback 0.5."""
    assert _get_rendement('plante inconnue') == 0.5


@pytest.mark.unit
def test_get_rendement_match_partiel(db):
    """'tomate cerise' remonte à 'tomate'."""
    RendementCulture.objects.create(
        culture_nom='tomate', rendement_kg_par_plant=2.5,
        region_climatique='tous', source='fao'
    )
    assert _get_rendement('tomate cerise') == 2.5


# ============================================================
# calculer_valeur_jardin
# ============================================================
@pytest.mark.integration
def test_valeur_jardin_simple(db, user_darkmaul, figure_simple, fruit_tomate):
    """3 plants de tomate = 3 * 2.5 kg * 2.5€ = 18.75€."""
    RendementCulture.objects.create(
        culture_nom='tomate', rendement_kg_par_plant=2.5,
        region_climatique='tous', source='fao'
    )
    figure_simple.crops = [
        {'name': 'Tomate'},
        {'name': 'Tomate'},
        {'name': 'Tomate'},
    ]
    figure_simple.save()

    result = calculer_valeur_jardin(user_darkmaul)

    assert result['valeur_potentielle'] == 18.75
    assert result['valeur_realisee'] == 0
    assert result['pourcentage_realise'] == 0
    assert len(result['top_cultures']) == 1
    assert result['top_cultures'][0]['nom'] == 'Tomate'


@pytest.mark.integration
def test_valeur_jardin_avec_recolte(db, user_darkmaul, figure_simple, fruit_tomate):
    """Ajoute une récolte → valeur réalisée > 0."""
    RendementCulture.objects.create(
        culture_nom='tomate', rendement_kg_par_plant=2.5,
        region_climatique='tous', source='fao'
    )
    figure_simple.crops = [{'name': 'Tomate'}]
    figure_simple.save()

    ChronologieCulture.objects.create(
        figure=figure_simple,
        culture_nom='Tomate',
        culture_emoji='🍅',
        date_semis=date.today() - timedelta(days=100),
        date_recolte_prevue=date.today() - timedelta(days=10),
        date_recolte_effective=date.today(),
        statut='recolte',
    )

    result = calculer_valeur_jardin(user_darkmaul)

    assert result['valeur_potentielle'] == 6.25 # 1 * 2.5 * 2.5
    assert result['valeur_realisee'] == 6.25 # 1 récolte
    assert result['pourcentage_realise'] == 100


@pytest.mark.integration
def test_valeur_jardin_vide(db, user_darkmaul):
    """Aucune culture → tout à 0."""
    result = calculer_valeur_jardin(user_darkmaul)
    assert result['valeur_potentielle'] == 0
    assert result['valeur_realisee'] == 0
    assert result['top_cultures'] == []


@pytest.mark.integration
def test_top3_tri_par_valeur_contribuee(db, user_darkmaul, figure_simple):
    """Top 3 trié par valeur contribuée."""
    from vegetables_fruits.models import Fruit

    # Framboise très chère mais 1 plant
    Fruit.objects.create(nom='Framboise', prix=8.90, couleur='rouge', saison='ete')
    # Tomate moins chère mais 5 plants
    Fruit.objects.create(nom='Tomate', prix=2.5, couleur='rouge', saison='ete')

    RendementCulture.objects.create(culture_nom='framboise', rendement_kg_par_plant=0.5, region_climatique='tous')
    RendementCulture.objects.create(culture_nom='tomate', rendement_kg_par_plant=2.5, region_climatique='tous')

    figure_simple.crops = [
        {'name': 'Framboise'},
        {'name': 'Tomate'}, {'name': 'Tomate'}, {'name': 'Tomate'},
        {'name': 'Tomate'}, {'name': 'Tomate'},
    ]
    figure_simple.save()

    result = calculer_valeur_jardin(user_darkmaul)
    top3 = result['top_cultures']

    # Tomate = 5 * 2.5 * 2.5 = 31.25€
    # Framboise = 1 * 0.5 * 8.9 = 4.45€
    assert top3[0]['nom'] == 'Tomate'
    assert top3[1]['nom'] == 'Framboise'