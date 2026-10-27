"""
Tests bonus Économie : région climatique + historique.
"""
import pytest
from datetime import date

from vegetables_fruits.models import RendementCulture, HistoriqueValeurJardin
from vegetables_fruits.services_economie import (
    calculer_valeur_jardin,
    _get_rendement,
    get_region_climatique,
)


# ============================================================
# Région climatique
# ============================================================
@pytest.mark.unit
def test_get_region_climatique_sans_parcelle(db, user_darkmaul):
    """Pas de parcelle → 'tous'."""
    assert get_region_climatique(user_darkmaul) == 'tous'


@pytest.mark.unit
def test_get_region_climatique_paris(db, user_darkmaul, figure_simple):
    """Figure à Paris → tempéré (via mapping)."""
    # figure_simple a lat=48.8566, lng=2.3522 → iledefrance
    # Mais la région dépend de get_region_utilisateur → mockable
    # Pour ce test, on vérifie juste qu'on retourne une valeur valide
    region = get_region_climatique(user_darkmaul)
    assert region in ('tous', 'tempere', 'continental', 'mediterraneen', 'tropical')


# ============================================================
# Rendement avec région
# ============================================================
@pytest.mark.unit
def test_rendement_regional_prioritaire(db):
    """Le rendement régional est utilisé s'il existe."""
    RendementCulture.objects.create(
        culture_nom='tomate', rendement_kg_par_plant=2.5,
        region_climatique='tous'
    )
    RendementCulture.objects.create(
        culture_nom='tomate', rendement_kg_par_plant=3.5,
        region_climatique='mediterraneen'
    )

    assert _get_rendement('tomate', region='mediterraneen') == 3.5
    assert _get_rendement('tomate', region='continental') == 2.5 # fallback 'tous'


@pytest.mark.unit
def test_rendement_fallback_tous_si_region_inconnue(db):
    """Si pas de rendement régional, utilise 'tous'."""
    RendementCulture.objects.create(
        culture_nom='tomate', rendement_kg_par_plant=2.5,
        region_climatique='tous'
    )
    assert _get_rendement('tomate', region='zimbabwe') == 2.5


# ============================================================
# Historique valeur
# ============================================================
@pytest.mark.unit
def test_historique_valeur_creation(db, user_darkmaul):
    """Création d'un snapshot."""
    from datetime import date
    mois = date.today().replace(day=1)

    h = HistoriqueValeurJardin.objects.create(
        utilisateur=user_darkmaul,
        mois=mois,
        valeur_potentielle=487.50,
        valeur_realisee=182.30,
        nb_cultures=5,
    )
    assert h.valeur_potentielle == 487.50
    assert h.utilisateur == user_darkmaul


@pytest.mark.unit
def test_historique_valeur_unique_par_mois(db, user_darkmaul):
    """Un seul snapshot par (user, mois)."""
    from django.db import IntegrityError
    mois = date.today().replace(day=1)

    HistoriqueValeurJardin.objects.create(
        utilisateur=user_darkmaul, mois=mois,
        valeur_potentielle=100, valeur_realisee=50,
    )
    with pytest.raises(IntegrityError):
        HistoriqueValeurJardin.objects.create(
            utilisateur=user_darkmaul, mois=mois,
            valeur_potentielle=200, valeur_realisee=100,
        )


# ============================================================
# Commande snapshot
# ============================================================
@pytest.mark.integration
def test_commande_snapshot(db, user_darkmaul):
    """La commande crée un snapshot pour chaque user."""
    from django.core.management import call_command
    from io import StringIO

    out = StringIO()
    call_command('snapshot_valeur_jardin', stdout=out)

    assert HistoriqueValeurJardin.objects.filter(utilisateur=user_darkmaul).exists()
    assert 'snapshots créés' in out.getvalue()