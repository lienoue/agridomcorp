"""
Tests de planifier_culture.
"""
import pytest
from datetime import date

from vegetables_fruits.models import ChronologieCulture, Culture


@pytest.mark.integration
def test_planifier_culture_cree_chrono(client_darkmaul, user_darkmaul, figure_simple):
    """POST valide → une ChronologieCulture est créée."""
    figure_simple.crops = [
        {'name': 'Tomate', 'emoji': '🍅', 'fruit_id': 999}
    ]
    figure_simple.save()

    resp = client_darkmaul.post(
        f'/planifier-culture/{figure_simple.id}/',
        {'crop_name': 'Tomate', 'date_semis': '2026-04-15'},
        follow=False,
    )

    assert resp.status_code == 302
    assert ChronologieCulture.objects.filter(
        figure=figure_simple,
        culture_nom__icontains='Tomate'
    ).count() == 1

    chrono = ChronologieCulture.objects.get(figure=figure_simple)
    assert chrono.date_semis == date(2026, 4, 15)


@pytest.mark.integration
def test_planifier_culture_utilise_jours_pousse(client_darkmaul, figure_simple, db):
    """Si Culture.jours_pousse existe, il est utilisé."""
    Culture.objects.create(
        nom='Tomate',
        type_culture='legume',
        emoji='🍅',
        jours_pousse=80,
    )
    figure_simple.crops = [{'name': 'Tomate', 'emoji': '🍅'}]
    figure_simple.save()

    client_darkmaul.post(
        f'/planifier-culture/{figure_simple.id}/',
        {'crop_name': 'Tomate', 'date_semis': '2026-04-01'},
    )

    chrono = ChronologieCulture.objects.get(figure=figure_simple)
    # 1er avril + 80 jours = 20 juin
    assert chrono.date_recolte_prevue == date(2026, 6, 20)


@pytest.mark.integration
def test_planifier_culture_refuse_double(client_darkmaul, figure_simple, db):
    """Ne crée pas 2 chronologies actives pour la même culture."""
    figure_simple.crops = [{'name': 'Tomate', 'emoji': '🍅'}]
    figure_simple.save()

    client_darkmaul.post(
        f'/planifier-culture/{figure_simple.id}/',
        {'crop_name': 'Tomate', 'date_semis': '2026-04-01'},
    )
    client_darkmaul.post(
        f'/planifier-culture/{figure_simple.id}/',
        {'crop_name': 'Tomate', 'date_semis': '2026-05-01'},
    )

    assert ChronologieCulture.objects.filter(figure=figure_simple).count() == 1


@pytest.mark.integration
def test_planifier_culture_refuse_crop_absent(client_darkmaul, figure_simple):
    """Refuse si le crop n'est pas dans la figure."""
    figure_simple.crops = [{'name': 'Salade', 'emoji': '🥬'}]
    figure_simple.save()

    client_darkmaul.post(
        f'/planifier-culture/{figure_simple.id}/',
        {'crop_name': 'Tomate', 'date_semis': '2026-04-01'},
    )

    assert ChronologieCulture.objects.filter(figure=figure_simple).count() == 0