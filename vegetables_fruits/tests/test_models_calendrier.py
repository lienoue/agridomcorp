"""
Tests de ChronologieCulture + CalendrierSemis.
"""
import pytest
from datetime import date, timedelta

from vegetables_fruits.models import ChronologieCulture, CalendrierSemis


# ============================================================
# calculer_progression() — cas normaux
# ============================================================
@pytest.mark.unit
def test_progression_juste_seme(db, figure_simple):
    """Semé aujourd'hui → progression ~0%, statut 'seme'."""
    chrono = ChronologieCulture.objects.create(
        figure=figure_simple,
        culture_nom='Tomate',
        culture_emoji='🍅',
        date_semis=date.today(),
        date_recolte_prevue=date.today() + timedelta(days=100),
    )
    progress = chrono.calculer_progression()

    assert progress == 0
    assert chrono.statut == 'seme'


@pytest.mark.unit
def test_progression_mi_parcours(db, figure_simple):
    """Semé il y a 50 jours sur 100 → ~50%."""
    chrono = ChronologieCulture.objects.create(
        figure=figure_simple,
        culture_nom='Tomate',
        culture_emoji='🍅',
        date_semis=date.today() - timedelta(days=50),
        date_recolte_prevue=date.today() + timedelta(days=50),
    )
    progress = chrono.calculer_progression()

    assert 40 <= progress <= 60 # tolérance
    assert chrono.statut in ('levee', 'croissance', 'floraison')


@pytest.mark.unit
def test_progression_pret_recolter(db, figure_simple):
    """Date de récolte passée → statut 'pret' (100%)."""
    chrono = ChronologieCulture.objects.create(
        figure=figure_simple,
        culture_nom='Tomate',
        culture_emoji='🍅',
        date_semis=date.today() - timedelta(days=100),
        date_recolte_prevue=date.today() - timedelta(days=1),
    )
    progress = chrono.calculer_progression()

    assert progress == 100
    assert chrono.statut == 'pret'


@pytest.mark.unit
def test_progression_recolte_effective(db, figure_simple):
    """Récolte effective → statut 'recolte'."""
    chrono = ChronologieCulture.objects.create(
        figure=figure_simple,
        culture_nom='Tomate',
        culture_emoji='🍅',
        date_semis=date.today() - timedelta(days=100),
        date_recolte_prevue=date.today() - timedelta(days=10),
        date_recolte_effective=date.today(),
    )
    chrono.calculer_progression()

    assert chrono.progression == 100
    assert chrono.statut == 'recolte'


# ============================================================
# Dates prévues intermédiaires
# ============================================================
@pytest.mark.unit
def test_dates_prevues_calculees(db, figure_simple):
    """calculer_progression() remplit date_levee_prevue, etc."""
    chrono = ChronologieCulture.objects.create(
        figure=figure_simple,
        culture_nom='Tomate',
        culture_emoji='🍅',
        date_semis=date.today(),
        date_recolte_prevue=date.today() + timedelta(days=100),
    )
    chrono.calculer_progression()
    chrono.refresh_from_db()

    assert chrono.date_levee_prevue is not None
    assert chrono.date_croissance_prevue is not None
    assert chrono.date_floraison_prevue is not None
    assert chrono.date_fructification_prevue is not None

    # Vérifier l'ordre chronologique
    assert chrono.date_semis < chrono.date_levee_prevue < chrono.date_recolte_prevue


# ============================================================
# CalendrierSemis — contraintes
# ============================================================
@pytest.mark.unit
def test_calendrier_unique_together(db, calendrier_tomate_iledefrance):
    """Impossible de créer 2 calendriers pour la même culture+région."""
    from django.db import IntegrityError
    with pytest.raises(IntegrityError):
        CalendrierSemis.objects.create(
            culture='Tomate',
            region='iledefrance',
            mois_debut_semis=4,
            mois_fin_semis=6,
            mois_debut_recolte=7,
            mois_fin_recolte=9,
        )


@pytest.mark.unit
def test_calendrier_peut_avoir_plusieurs_regions(db, calendrier_tomate_iledefrance):
    """Tomate à iledefrance ET Tomate à provence → 2 lignes distinctes."""
    cal2 = CalendrierSemis.objects.create(
        culture='Tomate',
        region='provence',
        mois_debut_semis=2,
        mois_fin_semis=5,
        mois_debut_recolte=6,
        mois_fin_recolte=9,
    )
    assert CalendrierSemis.objects.filter(culture='Tomate').count() == 2


# ============================================================
# Relation Figure ↔ ChronologieCulture
# ============================================================
@pytest.mark.unit
def test_relation_figure_chrono(db, figure_simple):
    """Une chronologie est bien liée à sa figure."""
    chrono = ChronologieCulture.objects.create(
        figure=figure_simple,
        culture_nom='Salade',
        culture_emoji='🥬',
        date_semis=date.today(),
        date_recolte_prevue=date.today() + timedelta(days=45),
    )

    assert chrono in figure_simple.chronologies.all()
    assert chrono.figure == figure_simple


@pytest.mark.unit
def test_suppression_figure_supprime_chrono(db, figure_simple):
    """CASCADE : supprimer la figure supprime ses chronologies."""
    ChronologieCulture.objects.create(
        figure=figure_simple,
        culture_nom='Salade',
        culture_emoji='🥬',
        date_semis=date.today(),
        date_recolte_prevue=date.today() + timedelta(days=45),
    )

    figure_simple.delete()
    assert ChronologieCulture.objects.count() == 0