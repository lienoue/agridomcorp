"""
Tests du modèle CustomUser.
"""
import pytest
from datetime import date, timedelta

from django.contrib.auth import get_user_model

User = get_user_model()


# ============================================================
# est_mineur()
# ============================================================
@pytest.mark.unit
def test_est_mineur_vrai(db, user_loulou):
    """Loulou (13 ans) est mineur."""
    assert user_loulou.est_mineur is True


@pytest.mark.unit
def test_est_mineur_faux(db, user_darkmaul):
    """Darkmaul (35 ans) n'est pas mineur."""
    assert user_darkmaul.est_mineur is False


@pytest.mark.unit
def test_est_mineur_sans_date(db):
    """Pas de birth_date → pas mineur."""
    u = User.objects.create_user(
        username='noage',
        email='noage@test.local',
        password='TestPass123!',
    )
    assert u.est_mineur is False


@pytest.mark.unit
def test_est_mineur_veille_18_ans(db):
    """17 ans et 364 jours → encore mineur."""
    birth = date.today() - timedelta(days=(18 * 365 - 1))
    u = User.objects.create_user(
        username='presque18',
        email='presque18@test.local',
        password='TestPass123!',
        birth_date=birth,
    )
    assert u.est_mineur is True


@pytest.mark.unit
def test_est_mineur_jour_18_ans(db):
    """Exactement 18 ans aujourd'hui → plus mineur."""
    birth = date(date.today().year - 18, date.today().month, date.today().day)
    u = User.objects.create_user(
        username='juste18',
        email='juste18@test.local',
        password='TestPass123!',
        birth_date=birth,
    )
    assert u.est_mineur is False


# ============================================================
# mode_junior auto (signal post_save)
# ============================================================
@pytest.mark.unit
def test_mode_junior_auto_active_pour_mineur(db, user_loulou):
    """Le signal active mode_junior pour un mineur."""
    assert user_loulou.mode_junior is True


@pytest.mark.unit
def test_mode_junior_pas_active_pour_majeur(db, user_darkmaul):
    """Le signal ne touche pas mode_junior d'un majeur."""
    assert user_darkmaul.mode_junior is False


# ============================================================
# est_suspendu_actif()
# ============================================================
@pytest.mark.unit
def test_suspendu_non_par_defaut(db, user_darkmaul):
    """Un nouvel utilisateur n'est pas suspendu."""
    assert user_darkmaul.est_suspendu is False
    assert user_darkmaul.est_suspendu_actif() is False


@pytest.mark.unit
def test_suspendu_actif_recent(db, user_darkmaul):
    """Suspendu il y a 2 jours → toujours actif."""
    from django.utils import timezone
    user_darkmaul.est_suspendu = True
    user_darkmaul.date_suspension = timezone.now() - timedelta(days=2)
    user_darkmaul.save()

    assert user_darkmaul.est_suspendu_actif() is True


@pytest.mark.unit
def test_suspendu_expire_apres_7_jours(db, user_darkmaul):
    """Suspendu il y a 8 jours → auto-désactivé."""
    from django.utils import timezone
    user_darkmaul.est_suspendu = True
    user_darkmaul.date_suspension = timezone.now() - timedelta(days=8)
    user_darkmaul.save()

    assert user_darkmaul.est_suspendu_actif() is False
    # Le signal doit avoir mis est_suspendu à False en DB
    user_darkmaul.refresh_from_db()
    assert user_darkmaul.est_suspendu is False


# ============================================================
# Admin
# ============================================================
@pytest.mark.unit
def test_superuser_flags(user_kamdem):
    """Kamdem est superuser + staff."""
    assert user_kamdem.is_superuser is True
    assert user_kamdem.is_staff is True
