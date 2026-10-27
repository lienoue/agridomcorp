"""
Tests des devises.
"""
import pytest
from vegetables_fruits.models import TauxChange
from vegetables_fruits.services_devises import (
    detecter_devise, convertir, formater, get_devise_user, get_taux,
)


# ============================================================
# Modèle TauxChange
# ============================================================
@pytest.mark.unit
def test_taux_change_conversion(db):
    """10€ = 6559.57 CFA (taux 655.957)."""
    taux = TauxChange.objects.create(
        devise='XOF', taux_vs_eur=655.957, symbole='CFA'
    )
    assert taux.convertir_depuis_eur(10) == 6559.57


@pytest.mark.unit
def test_taux_change_format_apres(db):
    """Format CFA après."""
    taux = TauxChange.objects.create(
        devise='XOF', taux_vs_eur=655.957, symbole='CFA', position_symbole='apres'
    )
    result = taux.formater(10)
    assert 'CFA' in result
    assert result.index('CFA') > result.index('6')


@pytest.mark.unit
def test_taux_change_format_avant(db):
    """Format $ avant."""
    taux = TauxChange.objects.create(
        devise='USD', taux_vs_eur=1.08, symbole='$', position_symbole='avant'
    )
    result = taux.formater(10)
    assert result.startswith('$')


# ============================================================
# Détection
# ============================================================
@pytest.mark.unit
def test_detecter_devise_senegal(db, user_darkmaul):
    """Utilisateur sénégalais → XOF."""
    user_darkmaul.location = 'Senegal'
    user_darkmaul.devise_preferee = None
    user_darkmaul.save()
    assert detecter_devise(user_darkmaul) == 'XOF'


@pytest.mark.unit
def test_devise_preferee_prioritaire(db, user_darkmaul):
    """Si devise_preferee définie, elle est prioritaire."""
    user_darkmaul.devise_preferee = 'USD'
    user_darkmaul.location = 'France'
    user_darkmaul.save()
    assert detecter_devise(user_darkmaul) == 'USD'


# ============================================================
# get_taux + cache
# ============================================================
@pytest.mark.unit
def test_get_taux_eur_none(db):
    """EUR n'a pas de taux (pivot)."""
    assert get_taux('EUR') is None


@pytest.mark.unit
def test_get_taux_mis_en_cache(db):
    """Le taux est mis en cache."""
    from django.core.cache import cache
    cache.clear()

    taux = TauxChange.objects.create(
        devise='USD', taux_vs_eur=1.08, symbole='$'
    )
    t1 = get_taux('USD')
    t2 = get_taux('USD')
    assert t1.id == t2.id
    assert t1.id == taux.id


# ============================================================
# Conversion
# ============================================================
@pytest.mark.unit
def test_convertir_xof(db):
    """10€ → 6559.57 CFA."""
    TauxChange.objects.create(devise='XOF', taux_vs_eur=655.957, symbole='CFA')
    assert convertir(10, 'XOF') == 6559.57


@pytest.mark.unit
def test_convertir_eur_pas_de_conversion(db):
    """EUR → pas de conversion."""
    assert convertir(10, 'EUR') == 10


@pytest.mark.unit
def test_convertir_devise_inconnue_fallback(db):
    """Devise inconnue → retourne EUR."""
    assert convertir(10, 'XYZ') == 10


# ============================================================
# Formater
# ============================================================
@pytest.mark.unit
def test_formater_eur(db):
    """10€ → contient '€'."""
    assert '€' in formater(10, 'EUR')


@pytest.mark.unit
def test_formater_usd(db):
    """10€ → contient '$'."""
    TauxChange.objects.create(devise='USD', taux_vs_eur=1.08, symbole='$', position_symbole='avant')
    result = formater(10, 'USD')
    assert '$' in result


# ============================================================
# get_devise_user
# ============================================================
@pytest.mark.unit
def test_get_devise_user_sauvegarde(db, user_darkmaul):
    """La détection auto sauvegarde la devise."""
    user_darkmaul.devise_preferee = None
    user_darkmaul.save()

    devise = get_devise_user(user_darkmaul)
    user_darkmaul.refresh_from_db()
    assert user_darkmaul.devise_preferee == devise


# ============================================================
# Intégration calculer_valeur_jardin
# ============================================================
@pytest.mark.integration
def test_valeur_jardin_convertie(db, user_darkmaul, figure_simple, fruit_tomate):
    """La valeur est convertie dans la devise de l'utilisateur."""
    from vegetables_fruits.models import RendementCulture
    from vegetables_fruits.services_economie import calculer_valeur_jardin

    # Configurer XOF
    TauxChange.objects.create(devise='XOF', taux_vs_eur=655.957, symbole='CFA')
    user_darkmaul.devise_preferee = 'XOF'
    user_darkmaul.save()

    RendementCulture.objects.create(
        culture_nom='tomate', rendement_kg_par_plant=2.5, region_climatique='tous'
    )
    figure_simple.crops = [{'name': 'Tomate'}]
    figure_simple.save()

    data = calculer_valeur_jardin(user_darkmaul)

    # 1 plant tomate * 2.5 kg * 2.5€ = 6.25 EUR
    # → 6.25 * 655.957 = 4099.73 XOF
    assert data['devise'] == 'XOF'
    assert abs(data['valeur_potentielle'] - 4099.73) < 0.01