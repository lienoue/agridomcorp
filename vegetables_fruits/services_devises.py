"""
Gestion des devises : détection, conversion, formatage.
Optimisé : cache 24h, requêtes légères, fallback EUR.
"""
import logging
from django.core.cache import cache
from .models import TauxChange

logger = logging.getLogger(__name__)

DEFAULT_DEVISE = 'EUR'

# Mapping région/pays → devise
REGION_VERS_DEVISE = {
    # Europe
    'france': 'EUR', 'iledefrance': 'EUR', 'bretagne': 'EUR',
    'provence': 'EUR', 'alsace': 'EUR', 'normandie': 'EUR',
    'espagne': 'EUR', 'italie': 'EUR', 'allemagne': 'EUR',
    'portugal': 'EUR', 'grece': 'EUR', 'belgique': 'EUR',
    'pays-bas': 'EUR', 'autriche': 'EUR', 'irlande': 'EUR',
    'suisse': 'CHF',
    'royaume-uni': 'GBP', 'angleterre': 'GBP', 'uk': 'GBP',
    # Amérique du Nord
    'etats-unis': 'USD', 'usa': 'USD', 'canada': 'CAD',
    'mexique': 'MXN',
    # Amérique du Sud
    'bresil': 'BRL',
    # Afrique
    'senegal': 'XOF', 'mali': 'XOF', "cote d'ivoire": 'XOF',
    'burkina': 'XOF', 'benin': 'XOF', 'togo': 'XOF', 'niger': 'XOF',
    'cameroon': 'XAF', 'cameroun': 'XAF', 'gabon': 'XAF',
    'congo': 'XAF', 'tchad': 'XAF', 'centrafrique': 'XAF',
    'maroc': 'MAD', 'algerie': 'DZD', 'tunisie': 'TND',
    'afrique du sud': 'ZAR',
    # Asie
    'japon': 'JPY', 'chine': 'CNY', 'inde': 'INR',
    # Océanie
    'australie': 'AUD',
}


def detecter_devise(user):
    """Détecte la devise probable de l'utilisateur selon sa région."""
    # 1. Devise explicitement choisie
    if user.devise_preferee:
        return user.devise_preferee

    # 2. ✅ NOUVEAU : location explicite (mise dans le profil)
    if user.location:
        location_lower = user.location.lower().strip()
        for key, devise in REGION_VERS_DEVISE.items():
            if key in location_lower:
                return devise

    # 3. Fallback : région Mapbox basée sur les figures
    try:
        from .views import get_region_utilisateur
        info = get_region_utilisateur(user)
        pays = (info.get('pays') or '').lower()
        region = (info.get('region') or '').lower()

        for key, devise in REGION_VERS_DEVISE.items():
            if key in pays or key in region:
                return devise
    except Exception as e:
        logger.warning(f"Erreur détection devise : {e}")

    return DEFAULT_DEVISE


def get_taux(devise):
    """Retourne un objet TauxChange ou None (pour EUR/fallback)."""
    if not devise or devise == 'EUR':
        return None

    cache_key = f"taux_change_{devise}"
    taux = cache.get(cache_key)

    if taux is None:
        taux = TauxChange.objects.filter(devise=devise, est_actif=True).first()
        if taux:
            cache.set(cache_key, taux, 60 * 60 * 24)
        else:
            logger.warning(f"Taux {devise} introuvable, fallback EUR")

    return taux


def convertir(prix_eur, devise):
    """Convertit un prix en EUR vers la devise demandée."""
    taux = get_taux(devise)
    if not taux:
        return round(prix_eur, 2)
    return round(prix_eur * taux.taux_vs_eur, 2)


def formater(prix_eur, devise):
    """Retourne une chaîne formatée (ex: '10,50 €' ou 'CFA 6 559')."""
    taux = get_taux(devise)
    if not taux:
        return f"{prix_eur:,.2f} €".replace(',', ' ').replace('.', ',')
    return taux.formater(prix_eur)


def get_devise_user(user):
    """Retourne le code devise de l'utilisateur (avec fallback et auto-sauvegarde)."""
    if hasattr(user, 'devise_preferee') and user.devise_preferee:
        return user.devise_preferee

    devise = detecter_devise(user)

    if hasattr(user, 'devise_preferee'):
        try:
            # ✅ update_fields pour ne pas écraser d'autres champs
            user.devise_preferee = devise
            user.save(update_fields=['devise_preferee'])
        except Exception as e:
            logger.warning(f"Impossible de sauvegarder devise pour {user.username}: {e}")

    return devise

def get_devise_figure(figure, user):
    """
    Retourne la devise de la parcelle (prioritaire sur la devise user).
    """
    if figure and figure.adresse_lat and figure.adresse_lng:
        try:
            from .views import get_region_utilisateur
            info = get_region_utilisateur(user, figure)
            pays = (info.get('pays') or '').lower()
            region = (info.get('region') or '').lower()

            # Chercher la devise correspondante
            for key, devise in REGION_VERS_DEVISE.items():
                if key in pays or key in region:
                    return devise
        except Exception as e:
            logger.warning(f"Erreur détection devise parcelle : {e}")

    # Fallback : devise de l'utilisateur
    return get_devise_user(user)