# vegetables_fruits/tests/test_views_dates.py
"""
Tests de non-régression des vues qui créent des ChronologieCulture.
Vérifie que le bug 'cerisier récolté en 90 jours' est bien mort.
"""
import pytest
from datetime import date
from django.urls import reverse

from vegetables_fruits.models import ChronologieCulture, GeometricFigure


@pytest.mark.integration
def test_planifier_cerisier_creation_correcte(client, user_darkmaul):
    """
    POST planifier_culture avec un Cerisier → date_recolte en +4 ans,
    type_cycle='plantation'.
    """
    # Créer une figure avec un cerisier dans les crops
    figure = GeometricFigure.objects.create(
        user=user_darkmaul,
        name='Test verger',
        figure_type='jardin',
        geojson_data={'type': 'FeatureCollection', 'features': []},
        crops=[{'name': 'Cerisier', 'emoji': '🍒'}],
    )

    client.force_login(user_darkmaul)
    response = client.post(
        reverse('vegetables_fruits:planifier_culture', args=[figure.id]),
        {'crop_name': 'Cerisier', 'date_semis': '2026-11-02'},
    )

    assert response.status_code == 302

    chrono = ChronologieCulture.objects.filter(figure=figure).first()
    assert chrono is not None
    assert chrono.type_cycle == 'plantation'
    assert chrono.date_recolte_prevue == date(2030, 11, 2)
    assert chrono.date_recolte_prevue.year == 2030


@pytest.mark.integration
def test_planifier_tomate_creation_correcte(client, user_darkmaul):
    """POST planifier_culture avec une Tomate → date_recolte en +90 jours."""
    figure = GeometricFigure.objects.create(
        user=user_darkmaul,
        name='Test potager',
        figure_type='jardin',
        geojson_data={'type': 'FeatureCollection', 'features': []},
        crops=[{'name': 'Tomate', 'emoji': '🍅'}],
    )

    client.force_login(user_darkmaul)
    response = client.post(
        reverse('vegetables_fruits:planifier_culture', args=[figure.id]),
        {'crop_name': 'Tomate', 'date_semis': '2026-04-15'},
    )

    assert response.status_code == 302

    chrono = ChronologieCulture.objects.filter(figure=figure).first()
    assert chrono is not None
    assert chrono.type_cycle == 'semis'
    assert chrono.date_recolte_prevue == date(2026, 7, 14) # +90j


@pytest.mark.integration
def test_ajouter_chronologie_cerisier(client, user_darkmaul):
    """POST ajouter_chronologie avec un Cerisier → type_cycle='plantation'."""
    figure = GeometricFigure.objects.create(
        user=user_darkmaul,
        name='Test verger 2',
        figure_type='jardin',
        geojson_data={'type': 'FeatureCollection', 'features': []},
        crops=[{'name': 'Cerisier', 'emoji': '🍒'}],
    )

    client.force_login(user_darkmaul)
    response = client.post(
        reverse('vegetables_fruits:ajouter_chronologie'),
        {
            'figure_id': figure.id,
            'culture_nom': 'Cerisier',
            'culture_emoji': '🍒',
            'date_semis': '2026-11-02',
            # PAS de jours_recolte → on laisse le service calculer
        },
    )

    assert response.status_code == 302

    chrono = ChronologieCulture.objects.filter(figure=figure).first()
    assert chrono is not None
    assert chrono.type_cycle == 'plantation'
    assert chrono.date_recolte_prevue == date(2030, 11, 2)


@pytest.mark.integration
@pytest.mark.integration
def test_planification_semis_cerisier(client, user_darkmaul):
    """
    La vue planification_semis utilise calculer_date_recolte()
    → Cerisier = +4 ans, pas +60 jours.
    """
    from vegetables_fruits.models import (
        CalendrierUser, PlanTarification, Abonnement
    )

    # ✅ 1. CRÉER L'ABONNEMENT PREMIUM DANS LA BASE DE TEST
    plan_premium = PlanTarification.objects.create(
        nom='PREMIUM',
        prix_mensuel=14.99,
        prix_annuel=149.99,
        actif=True,
    )
    Abonnement.objects.create(
        utilisateur=user_darkmaul,
        plan=plan_premium,
        statut='ACTIF',
        frequence='MENSUEL',
        date_fin=None
    )

    # ✅ 2. CRÉER LES DONNÉES DU TEST
    figure = GeometricFigure.objects.create(
        user=user_darkmaul,
        name='Test',
        figure_type='jardin',
        geojson_data={'type': 'FeatureCollection', 'features': []},
    )
    CalendrierUser.objects.create(
        utilisateur=user_darkmaul,
        figure=figure,
        culture='Cerisier',
        date_semis=date(2026, 11, 2),
    )

    # ✅ 3. SE CONNECTER ET TESTER
    client.force_login(user_darkmaul)
    response = client.get(reverse('vegetables_fruits:planification_semis'))

    # On doit avoir un 200 (succès) et plus un 302 (redirection)
    assert response.status_code == 200

    semis = response.context['semis']
    assert len(semis) >= 1

    cerisier = next(s for s in semis if s.culture == 'Cerisier')
    assert cerisier.date_fin == date(2030, 11, 2)
