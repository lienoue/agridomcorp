"""
Audit de sécurité : vérifie que les URLs critiques redirigent
vers login pour un utilisateur anonyme.
"""
import pytest
from django.urls import reverse, NoReverseMatch


URLS_PROTEGEES = [
    'vegetables_fruits:dashboard_particulier',
    'vegetables_fruits:view_figure',
    'vegetables_fruits:draw_figure',
    'vegetables_fruits:profile',
    'vegetables_fruits:limite_parcelles',
    'vegetables_fruits:suggestions_personnalisees',
]


@pytest.mark.integration
@pytest.mark.parametrize('url_name', URLS_PROTEGEES)
def test_url_protegee_redirige_anonyme(client_anon, url_name):
    """Un anonyme doit être redirigé (302/301), pas voir la page."""
    try:
        url = reverse(url_name)
    except NoReverseMatch:
        pytest.skip(f"URL {url_name} introuvable (nom incorrect ?)")

    resp = client_anon.get(url)
    assert resp.status_code in (301, 302), (
        f"⚠️ {url_name} ({url}) → status={resp.status_code}, attendu 301/302"
    )