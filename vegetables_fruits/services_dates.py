# vegetables_fruits/services_dates.py
"""
Service centralisé de calcul des dates de récolte.

Règle métier :
- Culture annuelle → date_semis + duree_jours
- Culture bisannuelle → date_semis + duree_jours (souvent 2 saisons)
- Culture pérenne → date_plantation + debut_production_annees (année civile)

Fallback (culture inconnue du référentiel) :
- Si le modèle Fruit/Vegetable/Culture fournit une durée → l'utiliser
- Sinon → 90 jours (durée safe pour un légume)
"""
from datetime import date, timedelta

from .data.cycles_cultures import get_cycle

# Durée de secours si aucune info n'est trouvée nulle part
FALLBACK_JOURS_ANNUEL = 90


def _ajouter_annees(date_debut, nb_annees):
    """
    Ajoute N années à une date en conservant le jour/mois exacts.

    Gère le cas du 29 février :
    - Si la date cible n'existe pas (ex: 29/02 sur année non bissextile),
      on retombe sur le 28/02.

    Exemples :
        _ajouter_annees(date(2026, 11, 2), 4) → date(2030, 11, 2)
        _ajouter_annees(date(2026, 1, 1), 3) → date(2029, 1, 1)
        _ajouter_annees(date(2024, 2, 29), 1) → date(2025, 2, 28) # bissextile ratée
        _ajouter_annees(date(2024, 2, 29), 4) → date(2028, 2, 29) # bissextile OK
    """
    if nb_annees < 0:
        raise ValueError("nb_annees doit être >= 0")

    annee_cible = date_debut.year + nb_annees
    try:
        return date_debut.replace(year=annee_cible)
    except ValueError:
        # Cas du 29 février sur année non bissextile
        return date_debut.replace(year=annee_cible, day=28)


def calculer_date_recolte(culture_nom, date_debut, mode='auto', jours_override=None):
    """
    Calcule la date de récolte prévue pour une culture.

    Args:
        culture_nom (str): nom de la culture (ex: 'Cerisier', 'Tomate')
        date_debut (date): date de semis OU de plantation
        mode (str):
            - 'auto' → détecte via CYCLES_CULTURES
            - 'semis' → force le calcul "annuelle"
            - 'plantation' → force le calcul "pérenne"
        jours_override (int|None): si fourni, court-circuite le référentiel
                                   (utile pour forcer une valeur en admin)

    Returns:
        dict {
            'date_recolte': date,
            'type_cycle': 'annuelle' | 'bisannuelle' | 'perenne',
            'duree_jours': int,
            'source': 'override' | 'referentiel' | 'modele' | 'fallback',
            'mode_utilise': 'semis' | 'plantation',
        }
    """
    if date_debut is None:
        raise ValueError("date_debut est obligatoire")

    # 1. Override prioritaire
    if jours_override is not None and jours_override > 0:
        return {
            'date_recolte': date_debut + timedelta(days=jours_override),
            'type_cycle': 'annuelle',
            'duree_jours': jours_override,
            'source': 'override',
            'mode_utilise': 'semis',
        }

    # 2. Référentiel CYCLES_CULTURES
    cycle = get_cycle(culture_nom) if mode == 'auto' or mode is None else None

    if cycle:
        type_cycle = cycle.get('type', 'annuelle')

        # ---- Pérenne ----
        if type_cycle == 'perenne':
            annees = cycle.get('debut_production_annees', 3)
            date_cible = _ajouter_annees(date_debut, annees)
            return {
                'date_recolte': date_cible,
                'type_cycle': 'perenne',
                # duree_jours purement indicative (pour l'affichage)
                'duree_jours': (date_cible - date_debut).days,
                'source': 'referentiel',
                'mode_utilise': 'plantation',
                'annees_avant_production': annees,
            }

        # ---- Annuelle / bisannuelle ----
        duree_jours = cycle.get('duree_jours')
        if duree_jours:
            return {
                'date_recolte': date_debut + timedelta(days=duree_jours),
                'type_cycle': type_cycle,
                'duree_jours': duree_jours,
                'source': 'referentiel',
                'mode_utilise': 'semis',
            }

    # 3. Fallback sur le modèle (Fruit/Vegetable/Culture)
    duree_modele = _duree_depuis_modele(culture_nom)
    if duree_modele and duree_modele > 0:
        return {
            'date_recolte': date_debut + timedelta(days=duree_modele),
            'type_cycle': 'annuelle',
            'duree_jours': duree_modele,
            'source': 'modele',
            'mode_utilise': 'semis',
        }

    # 4. Fallback ultime (durée safe)
    return {
        'date_recolte': date_debut + timedelta(days=FALLBACK_JOURS_ANNUEL),
        'type_cycle': 'annuelle',
        'duree_jours': FALLBACK_JOURS_ANNUEL,
        'source': 'fallback',
        'mode_utilise': 'semis',
    }


def _duree_depuis_modele(culture_nom):
    """
    Cherche une durée de récolte dans les modèles Django.
    Ordre : Fruit → Vegetable → Culture.

    Returns:
        int | None: durée en jours ou None si rien trouvé
    """
    # Import local pour éviter les imports circulaires
    from .models import Fruit, Vegetable, Culture

    # 1. Fruit
    try:
        fruit = Fruit.objects.filter(nom__iexact=culture_nom).first()
        if fruit and fruit.jours_recolte and fruit.jours_recolte > 0:
            return fruit.jours_recolte
    except Exception:
        pass

    # 2. Vegetable
    try:
        veg = Vegetable.objects.filter(nom__iexact=culture_nom).first()
        if veg and veg.jours_recolte and veg.jours_recolte > 0:
            return veg.jours_recolte
    except Exception:
        pass

    # 3. Culture (jours_pousse en priorité, puis duree_culture_max_jours)
    try:
        culture = Culture.objects.filter(nom__iexact=culture_nom).first()
        if culture:
            if culture.jours_pousse and culture.jours_pousse > 0:
                return culture.jours_pousse
            if culture.duree_culture_max_jours and culture.duree_culture_max_jours > 0:
                return culture.duree_culture_max_jours
    except Exception:
        pass

    return None


def determiner_type_cycle(culture_nom):
    """
    Retourne le type de cycle d'une culture (sans calculer de date).

    Returns:
        str: 'annuelle' | 'bisannuelle' | 'perenne' | 'inconnu'
    """
    cycle = get_cycle(culture_nom)
    if cycle:
        return cycle.get('type', 'annuelle')
    return 'inconnu'


def est_perenne(culture_nom):
    """
    Retourne True si la culture doit être affichée comme un arbre/arbuste (Plantation)
    dans l'interface utilisateur.

    Logique :
    1. Si le dictionnaire force 'est_arbre_ui': True → True (ex: bananier)
    2. Si c'est de type 'annuelle' → False
    3. Si c'est de type 'perenne' ET que ça met >= 2 ans à produire → True
    4. Sinon → False (ex: thym, fraise)
    """
    from .data.cycles_cultures import get_cycle

    cycle = get_cycle(culture_nom)
    if not cycle:
        return False

    # 1. Force l'affichage en arbre (pour les arbres tropicaux rapides comme la banane)
    if cycle.get('est_arbre_ui') is True:
        return True

    # 2. Si c'est explicitement annuel, c'est un semis
    if cycle.get('type') == 'annuelle':
        return False

    # 3. Pérenne "classique" (arbres fruitiers, vignes)
    if cycle.get('type') == 'perenne':
        annees = cycle.get('debut_production_annees', 3)
        return annees >= 2

    return False
