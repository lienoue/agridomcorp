"""
Calculs économiques : valeur du jardin, économies réalisées, top cultures.
"""
import logging

from .models import (
    RendementCulture, GeometricFigure, ChronologieCulture,
    Fruit, Vegetable,
)

logger = logging.getLogger(__name__)

DEFAULT_RENDEMENT = 0.5 # 500g si aucune donnée trouvée


def _get_rendement(culture_nom, region='tous'):
    """Rendement kg/plant pour une culture, avec fallback."""
    nom = (culture_nom or '').strip().lower()
    if not nom:
        return DEFAULT_RENDEMENT

    # 1. Match exact sur la région climatique
    r = None
    if region and region != 'tous':
        r = RendementCulture.objects.filter(
            culture_nom=nom, region_climatique=region, est_actif=True
        ).first()

    # 2. Match exact sur 'tous'
    if not r:
        r = RendementCulture.objects.filter(
            culture_nom=nom, region_climatique='tous', est_actif=True
        ).first()

    # 3. Match partiel (le plus long match)
    if not r:
        candidats = RendementCulture.objects.filter(est_actif=True)
        nom_lower = nom.lower()
        meilleur = None
        meilleure_longueur = 0
        for c in candidats:
            culture_lower = c.culture_nom.lower()
            if culture_lower in nom_lower and len(culture_lower) > meilleure_longueur:
                meilleur = c
                meilleure_longueur = len(culture_lower)
        r = meilleur

    return r.rendement_kg_par_plant if r else DEFAULT_RENDEMENT


def _get_prix(culture_nom):
    """Prix €/kg depuis Fruit.prix ou Vegetable.prix."""
    nom = (culture_nom or '').strip()
    if not nom:
        return 0.0

    f = Fruit.objects.filter(nom__iexact=nom).first()
    if f and f.prix:
        return float(f.prix)

    v = Vegetable.objects.filter(nom__iexact=nom).first()
    if v and v.prix:
        return float(v.prix)

    return 0.0


def _compter_plants(user, figure_id=None):
    """Compte combien de fois chaque culture apparaît dans les figures."""
    compteur = {}
    figures = GeometricFigure.objects.filter(user=user)
    if figure_id:
        figures = figures.filter(id=figure_id)

    for fig in figures:
        for crop in (fig.crops or []):
            nom = crop.get('name', '').strip()
            if nom:
                compteur[nom] = compteur.get(nom, 0) + 1
    return compteur


def calculer_valeur_jardin(user, figure_id=None):
    """
    Retourne dict {
        'valeur_potentielle': float, # CONVERTIE dans la devise user
        'valeur_realisee': float, # CONVERTIE dans la devise user
        'pourcentage_realise': int,
        'devise': str, # ← NOUVEAU
        'top_cultures': [...], # prix et valeur CONVERTIS
        'details_par_culture': [...]
    }
    """
    from .services_devises import get_devise_user, get_devise_figure, convertir

    plants = _compter_plants(user, figure_id=figure_id)
    region = get_region_climatique(user)
    # ✅ Si une parcelle est sélectionnée, sa devise est prioritaire
    figure = None
    if figure_id:
        from .models import GeometricFigure
        figure = GeometricFigure.objects.filter(id=figure_id, user=user).first()

    devise = get_devise_figure(figure, user) if figure else get_devise_user(user)

    total_potentiel = 0.0
    details = []

    for nom, nb in plants.items():
        prix = _get_prix(nom)
        rendement = _get_rendement(nom, region=region)
        valeur = prix * rendement * nb
        total_potentiel += valeur

        if prix > 0:
            details.append({
                'nom': nom,
                'prix': round(prix, 2), # en EUR (pour calcul)
                'prix_local': convertir(prix, devise), # ← converti
                'rendement': rendement,
                'nb_plants': nb,
                'valeur_contribuee': round(valeur, 2), # en EUR
                'valeur_contribuee_local': convertir(valeur, devise), # ← converti
            })

    # Économies réalisées
    chronos_qs = ChronologieCulture.objects.filter(
        figure__user=user, statut='recolte'
    )
    if figure_id:
        chronos_qs = chronos_qs.filter(figure_id=figure_id)

    total_realise = 0.0
    for chrono in chronos_qs:
        prix = _get_prix(chrono.culture_nom)
        rendement = _get_rendement(chrono.culture_nom, region=region)
        total_realise += prix * rendement

    pourcentage = int((total_realise / total_potentiel) * 100) if total_potentiel > 0 else 0
    top3 = sorted(details, key=lambda x: x['valeur_contribuee'], reverse=True)[:3]

    from .views import get_culture_emoji
    for item in top3:
        item['emoji'] = get_culture_emoji(item['nom'])

    return {
        'valeur_potentielle': convertir(total_potentiel, devise), # ← converti
        'valeur_realisee': convertir(total_realise, devise), # ← converti
        'pourcentage_realise': min(pourcentage, 100),
        'devise': devise,
        'top_cultures': top3,
        'details_par_culture': sorted(details, key=lambda x: x['valeur_contribuee'], reverse=True),
        'region_climatique': region,
    }




def get_region_climatique(user, figure=None):
    """
    Retourne la région climatique de l'utilisateur (pour les rendements).
    Fallback : 'tous' si inconnu.
    """
    try:
        from .views import get_region_utilisateur
        from .models import GeometricFigure

        if not figure:
            figure = GeometricFigure.objects.filter(
                user=user,
                adresse_lat__isnull=False,
                adresse_lng__isnull=False,
            ).first()

        if figure and figure.adresse_lat and figure.adresse_lng:
            # Réutilise le helper de views pour la cohérence
            info = get_region_utilisateur(user, figure)
            pays = info.get('pays', '').lower()
            region = info.get('region', '').lower()

            # Mapping région → région climatique (à enrichir progressivement)
            MAPPING = {
                # Europe
                'iledefrance': 'tempere',
                'bretagne': 'tempere',
                'normandie': 'tempere',
                'alsace': 'continental',
                'provence': 'mediterraneen',
                'paca': 'mediterraneen',
                'corse': 'mediterraneen',
                'occitanie': 'mediterraneen',
                # Pays méditerranéens
                'espagne': 'mediterraneen', 'italie': 'mediterraneen',
                'grece': 'mediterraneen', 'portugal': 'mediterraneen',
                # Pays tropicaux
                'bresil': 'tropical', 'thailande': 'tropical',
                'vietnam': 'tropical', 'indonesie': 'tropical',
                # Désertiques
                'maroc': 'desertique', 'egypte': 'desertique',
                'arabie saoudite': 'desertique',
                # Montagneux
                'suisse': 'montagnard', 'autriche': 'montagnard',
                # Continental
                'allemagne': 'continental', 'pologne': 'continental',
                'russie': 'continental', 'canada': 'continental',
            }

            # Chercher dans le mapping
            for key, val in MAPPING.items():
                if key in region or key in pays:
                    return val

    except Exception as e:
        logger.warning(f"Impossible de déterminer la région climatique : {e}")

    return 'tous'

