"""
Service de vérification des saisons de culture.
"""
import logging
from datetime import date

from django.utils import timezone

from .models import CalendrierSemis, Variete, Culture, Fruit, Vegetable

logger = logging.getLogger(__name__)


# ============================================================
# HELPERS MOIS (déplacés AVANT les fonctions qui les utilisent)
# ============================================================

_MOIS_FR = [
    '', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre',
]


def _nom_mois(numero):
    """Retourne le nom français d'un mois (1-12)."""
    if 1 <= numero <= 12:
        return _MOIS_FR[numero]
    return str(numero)


def _mois_intervalle(debut, fin):
    """
    Retourne la liste des mois (1-12) couverts par l'intervalle [debut, fin].
    Gère le wrap d'année : 11→2 = [11, 12, 1, 2].

    >>> _mois_intervalle(3, 6)
    [3, 4, 5, 6]
    >>> _mois_intervalle(11, 2)
    [11, 12, 1, 2]
    >>> _mois_intervalle(12, 1)
    [12, 1]
    >>> _mois_intervalle(5, 5)
    [5]
    """
    if not (1 <= debut <= 12 and 1 <= fin <= 12):
        return []
    if debut <= fin:
        return list(range(debut, fin + 1))
    return list(range(debut, 13)) + list(range(1, fin + 1))


# ============================================================
# RÉSOLUTION DU NOM DE CULTURE
# ============================================================

def _resoudre_nom_culture(crop):
    """
    À partir d'un item de crops_data, retourne le nom de la culture parente.
    Retourne None si introuvable.
    """
    # 1. Variété → remonter à la culture parente
    if crop.get('variete_id'):
        try:
            variete = Variete.objects.select_related('culture').get(id=crop['variete_id'])
            if variete.culture:
                return variete.culture.nom
            return variete.nom
        except Variete.DoesNotExist:
            logger.warning(f"Variete {crop['variete_id']} introuvable")

    # 2. Fruit → nom direct
    if crop.get('fruit_id'):
        try:
            fruit = Fruit.objects.get(id=crop['fruit_id'])
            return fruit.nom
        except Fruit.DoesNotExist:
            logger.warning(f"Fruit {crop['fruit_id']} introuvable")

    # 3. Vegetable → nom direct
    if crop.get('vegetable_id'):
        try:
            veg = Vegetable.objects.get(id=crop['vegetable_id'])
            return veg.nom
        except Vegetable.DoesNotExist:
            logger.warning(f"Vegetable {crop['vegetable_id']} introuvable")

    # 4. Fallback : le nom directement
    return crop.get('name')


# ============================================================
# VÉRIFICATION SAISON (unitaire)
# ============================================================

def verifier_saison_culture(crop, region, date_ref=None):
    """
    Vérifie si une culture est dans sa fenêtre de semis/plantation pour la région.
    """
    if date_ref is None:
        date_ref = date.today()

    nom_culture = _resoudre_nom_culture(crop)
    emoji = crop.get('emoji', '🌱')

    resultat = {
        'ok': True,
        'name': nom_culture or crop.get('name', 'Culture inconnue'),
        'emoji': emoji,
        'fenetre': '',
        'mois_actuel': _nom_mois(date_ref.month),
        'message': '',
        'raison': 'ok',
    }

    if not nom_culture:
        resultat['raison'] = 'culture_inconnue'
        return resultat

    # ✅ NOUVEAU : On utilise notre service centralisé au lieu des mots-clés
    from .services_dates import est_perenne

    if est_perenne(nom_culture):
        resultat['raison'] = 'arbre_pas_de_verif'
        resultat['message'] = (
            f"🌳 {nom_culture} est un arbre/arbuste. "
            f"Vous pouvez le planter en dehors de la période de semis classique."
        )
        return resultat

    # Recherche du calendrier : d'abord la région exacte, puis 'tous'
    calendrier = (
            CalendrierSemis.objects.filter(culture__iexact=nom_culture, region=region).first()
            or CalendrierSemis.objects.filter(culture__iexact=nom_culture, region='tous').first()
    )

    # Recherche floue si pas trouvé (ex: "Tomate cerise" → "Tomate")
    if not calendrier:
        calendrier = (
                CalendrierSemis.objects.filter(culture__icontains=nom_culture, region=region).first()
                or CalendrierSemis.objects.filter(culture__icontains=nom_culture, region='tous').first()
                or CalendrierSemis.objects.filter(
            culture__icontains=nom_culture.split()[0], region=region
        ).first()
        )

    if not calendrier:
        # Pas de données : on ne bloque pas
        resultat['raison'] = 'culture_inconnue'
        return resultat

    # Vérification de la fenêtre
    mois = date_ref.month
    mois_debut = calendrier.mois_debut_semis
    mois_fin = calendrier.mois_fin_semis

    # Gestion des fenêtres à cheval (ex: nov-fév)
    if mois_debut <= mois_fin:
        dans_fenetre = mois_debut <= mois <= mois_fin
    else:
        dans_fenetre = mois >= mois_debut or mois <= mois_fin

    resultat['fenetre'] = f"{_nom_mois(mois_debut)} - {_nom_mois(mois_fin)}"

    if not dans_fenetre:
        resultat['ok'] = False
        resultat['raison'] = 'hors_saison'
        resultat['message'] = (
            f"La période recommandée pour planter {nom_culture} "
            f"dans ta région est : {resultat['fenetre']}."
        )
    else:
        resultat['message'] = f"✅ {nom_culture} est dans sa période de plantation."

    return resultat


# ============================================================
# VÉRIFICATION SAISON (batch — utilisée par api_verifier_saison)
# ============================================================

def verifier_saison_cultures(crops, user, figure=None):
    """
    Vérifie en batch la saison de toutes les cultures d'une parcelle.

    Args:
        crops (list[dict]): liste des items crops_data (figure.crops)
        user (CustomUser): utilisateur (pour résoudre la région)
        figure (GeometricFigure|None): parcelle d'où viennent les crops

    Returns:
        dict {
            'hors_saison': list[dict], # cultures en alerte
            'region': str, # région utilisée
            'total_verifiees': int,
        }
    """
    # Import local pour éviter un import circulaire (views importe services)
    from .views import get_region_utilisateur

    region_info = get_region_utilisateur(user, figure)
    region = region_info.get('region', 'iledefrance')

    hors_saison = []
    for crop in crops or []:
        resultat = verifier_saison_culture(crop, region)
        if not resultat['ok']:
            hors_saison.append(resultat)

    return {
        'hors_saison': hors_saison,
        'region': region,
        'total_verifiees': len(crops or []),
    }


# ============================================================
# ORGANISATION DU CALENDRIER PAR MOIS
# ============================================================

def organiser_calendrier_par_mois(entries):
    """
    Organise une liste d'entrées CalendrierSemis par mois (1-12).
    Gère correctement les intervalles qui wrappent l'année.

    Retourne un dict {mois_int: [entry, ...]}.
    """
    mois_data = {i: [] for i in range(1, 13)}
    for entry in entries:
        for m in _mois_intervalle(entry.mois_debut_semis, entry.mois_fin_semis):
            mois_data[m].append(entry)
    return mois_data


# ============================================================
# RÉSOLUTION DE LA RÉGION POUR LE CALENDRIER
# ============================================================

def resoudre_calendrier_semis(user, figure=None):
    """
    Cascade de résolution de la région pour le calendrier :
    Région exacte → Pays (via REGION_MAPPING) → Continent → Tous.
    Retourne (queryset, region_finale, source_debug).
    """
    # Import local pour éviter un import circulaire
    from .views import get_region_utilisateur, REGION_MAPPING

    region_info = get_region_utilisateur(user, figure)
    region = region_info.get('region')
    pays = (region_info.get('pays') or '').lower()
    continent = region_info.get('continent')

    regions_dispo = set(CalendrierSemis.objects.values_list('region', flat=True).distinct())

    # Correspondance Continent → Région pivot (pour le fallback)
    CONTINENT_TO_REGION = {
        'europe': 'iledefrance',
        'afrique': 'afrique_ouest',
        'asie': 'japon',
        'amerique': 'usa_nord_est',
        'oceanie': 'australie_sud_est',
    }

    region_finale = None
    source = None

    # 1. Région exacte
    if region and region in regions_dispo:
        region_finale, source = region, 'region_exacte'

    # 2. Pays → Région (via le mapping)
    if not region_finale and pays:
        mappee = REGION_MAPPING.get(pays)
        if mappee and mappee in regions_dispo:
            region_finale, source = mappee, f'pays→region ({pays}→{mappee})'

    # 3. Continent → Région pivot
    if not region_finale and continent:
        pivot = CONTINENT_TO_REGION.get(continent)
        if pivot and pivot in regions_dispo:
            region_finale, source = pivot, f'continent→region ({continent}→{pivot})'

    # 4. Fallback global
    if not region_finale:
        region_finale, source = 'tous', 'fallback_tous'

    qs = CalendrierSemis.objects.filter(region=region_finale).order_by('mois_debut_semis')
    return qs, region_finale, source