"""
Tests des dashboards (particulier / eleve / junior).
"""
import pytest
from datetime import date, timedelta
from django.urls import reverse

from vegetables_fruits.models import ChronologieCulture


# ============================================================
# Helper
# ============================================================
def url_dashboard_particulier():
    return reverse('vegetables_fruits:dashboard_particulier')


# ============================================================
# Accès et redirections
# ============================================================
@pytest.mark.integration
def test_dashboard_requiert_connexion(client_anon):
    """Non connecté → redirect vers login."""
    resp = client_anon.get(url_dashboard_particulier())
    assert resp.status_code in (301, 302)


@pytest.mark.integration
def test_dashboard_particulier_majeur(client_darkmaul):
    """Majeur → affiche dashboard_particulier."""
    resp = client_darkmaul.get(url_dashboard_particulier())
    assert resp.status_code == 200
    templates_utilises = [t.name for t in resp.templates if t.name]
    assert any('dashboard_particulier.html' in t for t in templates_utilises)


@pytest.mark.integration
def test_dashboard_particulier_mineur_redirige(client_loulou):
    """Mineur → redirigé vers junior ou élève."""
    resp = client_loulou.get(url_dashboard_particulier(), follow=False)
    assert resp.status_code == 302
    assert 'junior' in resp.url or 'eleve' in resp.url


# ============================================================
# État "non_planifiee"
# ============================================================
@pytest.mark.integration
def test_dashboard_culture_non_planifiee(client_darkmaul, figure_simple):
    """Crop sans chronologie → état 'non_planifiee'."""
    figure_simple.crops = [
        {'name': 'Tomate', 'emoji': '🍅', 'fruit_id': 999}
    ]
    figure_simple.save()

    resp = client_darkmaul.get(url_dashboard_particulier())
    assert resp.status_code == 200

    mes_cultures = resp.context['mes_cultures']
    assert len(mes_cultures) == 1
    assert mes_cultures[0]['etat'] == 'non_planifiee'
    assert mes_cultures[0]['progression'] == 0
    assert mes_cultures[0]['chrono_id'] is None


@pytest.mark.integration
def test_dashboard_compteur_non_planifiee(client_darkmaul, figure_simple):
    """Le compteur stats_mes_cultures compte bien les non planifiées."""
    figure_simple.crops = [
        {'name': 'Tomate', 'emoji': '🍅'},
        {'name': 'Salade', 'emoji': '🥬'},
    ]
    figure_simple.save()

    resp = client_darkmaul.get(url_dashboard_particulier())
    stats = resp.context['stats_mes_cultures']

    assert stats['total'] == 2
    assert stats['a_planifier'] == 2
    assert stats['en_cours'] == 0


# ============================================================
# État "en_cours"
# ============================================================
@pytest.mark.integration
def test_dashboard_culture_en_cours(client_darkmaul, figure_simple):
    """Chronologie active → état 'en_cours' avec progression."""
    figure_simple.crops = [{'name': 'Tomate', 'emoji': '🍅'}]
    figure_simple.save()

    ChronologieCulture.objects.create(
        figure=figure_simple,
        culture_nom='Tomate',
        culture_emoji='🍅',
        date_semis=date.today() - timedelta(days=30),
        date_recolte_prevue=date.today() + timedelta(days=60),
    )

    resp = client_darkmaul.get(url_dashboard_particulier())
    mes_cultures = resp.context['mes_cultures']

    assert mes_cultures[0]['etat'] == 'en_cours'
    assert 20 <= mes_cultures[0]['progression'] <= 40
    assert mes_cultures[0]['chrono_id'] is not None


# ============================================================
# État "recoltee"
# ============================================================
@pytest.mark.integration
def test_dashboard_culture_recoltee(client_darkmaul, figure_simple):
    """Chronologie récoltée → état 'recoltee'."""
    figure_simple.crops = [{'name': 'Tomate', 'emoji': '🍅'}]
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

    resp = client_darkmaul.get(url_dashboard_particulier())
    mes_cultures = resp.context['mes_cultures']

    assert mes_cultures[0]['etat'] == 'recoltee'
    assert mes_cultures[0]['progression'] == 100


# ============================================================
# MIXTE
# ============================================================
@pytest.mark.integration
def test_dashboard_mixte(client_darkmaul, figure_simple):
    """3 cultures aux 3 états différents → compteur exact."""
    figure_simple.crops = [
        {'name': 'Tomate', 'emoji': '🍅'},
        {'name': 'Salade', 'emoji': '🥬'},
        {'name': 'Carotte', 'emoji': '🥕'},
    ]
    figure_simple.save()

    ChronologieCulture.objects.create(
        figure=figure_simple,
        culture_nom='Tomate',
        culture_emoji='🍅',
        date_semis=date.today() - timedelta(days=30),
        date_recolte_prevue=date.today() + timedelta(days=60),
    )
    ChronologieCulture.objects.create(
        figure=figure_simple,
        culture_nom='Salade',
        culture_emoji='🥬',
        date_semis=date.today() - timedelta(days=60),
        date_recolte_prevue=date.today() - timedelta(days=10),
        date_recolte_effective=date.today(),
        statut='recolte',
    )

    resp = client_darkmaul.get(url_dashboard_particulier())
    stats = resp.context['stats_mes_cultures']

    assert stats['total'] == 3
    assert stats['en_cours'] == 1
    assert stats['a_planifier'] == 1
    assert stats['recoltees'] == 1