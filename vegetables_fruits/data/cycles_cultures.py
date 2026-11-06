# vegetables_fruits/data/cycles_cultures.py
"""
Référentiel des cycles culturaux.

Clé = nom normalisé (sans accent, minuscule, sans article).
Valeurs :
  - type : 'annuelle' | 'bisannuelle' | 'perenne'
  - duree_jours : (annuelles/bisannuelles) durée semis→récolte (fourchette)
  - duree_jours_min/max : (annuelles) fourchette affichable
  - debut_production_annees : (pérennes) nb d'années avant 1ère récolte
  - pleine_production_annees: (pérennes) nb d'années avant pleine production
  - mois_plantation : (optionnel) tuple (début, fin) recommandé (1-12)
  - emoji : (optionnel)
"""

CYCLES_CULTURES = {
    # ============================================================
    # 🍎 ARBRES FRUITIERS À PÉPINS (PÉRENNES)
    # ============================================================
    'pommier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 8, 'emoji': '🍎', 'mois_plantation': (10, 3)},
    'poirier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 8, 'emoji': '🍐', 'mois_plantation': (10, 3)},
    'cognassier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟡', 'mois_plantation': (10, 3)},
    'coing': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟡', 'mois_plantation': (10, 3)},
    'nashi': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍐', 'mois_plantation': (10, 3)},
    'pommier sauvage': {'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 10, 'emoji': '🍎', 'mois_plantation': (10, 3)},

    # ============================================================
    # 🍑 ARBRES FRUITIERS À NOYAU (PÉRENNES)
    # ============================================================
    'cerisier': {'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🍒', 'mois_plantation': (10, 3)},
    'prunier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟣', 'mois_plantation': (10, 3)},
    'mirabellier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟡', 'mois_plantation': (10, 3)},
    'quetschier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟣', 'mois_plantation': (10, 3)},
    'abricotier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍑', 'mois_plantation': (10, 3)},
    'pêcher': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 5, 'emoji': '🍑', 'mois_plantation': (10, 3)},
    'pecher': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 5, 'emoji': '🍑', 'mois_plantation': (10, 3)},
    'nectarinier': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 5, 'emoji': '🍑', 'mois_plantation': (10, 3)},
    'amandier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 8, 'emoji': '🌰', 'mois_plantation': (10, 2)},

    # ============================================================
    # 🌰 ARBRES À COQUE (PÉRENNES)
    # ============================================================
    'noyer': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 15, 'emoji': '🌰', 'mois_plantation': (10, 2)},
    'noisetier': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 5, 'emoji': '🌰', 'mois_plantation': (10, 2)},
    'châtaignier': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 15, 'emoji': '🌰', 'mois_plantation': (10, 2)},
    'chataignier': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 15, 'emoji': '🌰', 'mois_plantation': (10, 2)},
    'pistachier': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '🟢', 'mois_plantation': (10, 2)},
    'cajou': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🌰', 'mois_plantation': (3, 6)},
    'macadamia': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '🌰', 'mois_plantation': (3, 6)},
    'pacanier': {'type': 'perenne', 'debut_production_annees': 6, 'pleine_production_annees': 12, 'emoji': '🌰', 'mois_plantation': (10, 2)},

    # ============================================================
    # 🫒 ARBRES MÉDITERRANÉENS (PÉRENNES)
    # ============================================================
    'olivier': {'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 10, 'emoji': '🫒', 'mois_plantation': (9, 11)},
    'figuier': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 5, 'emoji': '🟣', 'mois_plantation': (10, 3)},
    'grenadier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🔴', 'mois_plantation': (10, 3)},
    'kaki': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🟠', 'mois_plantation': (10, 3)},
    'plaqueminier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🟠', 'mois_plantation': (10, 3)},
    'caroubier': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '🟤', 'mois_plantation': (10, 3)},
    'jujubier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🔴', 'mois_plantation': (10, 3)},

    # ============================================================
    # 🍋 AGRUMES (PÉRENNES, sensibles au gel)
    # ============================================================
    'oranger': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍊', 'mois_plantation': (3, 5)},
    'citronnier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍋', 'mois_plantation': (3, 5)},
    'pamplemoussier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍊', 'mois_plantation': (3, 5)},
    'mandarinier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍊', 'mois_plantation': (3, 5)},
    'clémentinier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍊', 'mois_plantation': (3, 5)},
    'clementinier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍊', 'mois_plantation': (3, 5)},
    'kumquat': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 5, 'emoji': '🍊', 'mois_plantation': (3, 5)},
    'calamondin': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 5, 'emoji': '🍊', 'mois_plantation': (3, 5)},
    'yuzu': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍋', 'mois_plantation': (3, 5)},
    'cédratier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍋', 'mois_plantation': (3, 5)},
    'cedratier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍋', 'mois_plantation': (3, 5)},
    'bergamotier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍋', 'mois_plantation': (3, 5)},
    'lime': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍋', 'mois_plantation': (3, 5)},
    'tangelo': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍊', 'mois_plantation': (3, 5)},
    'tangerinier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍊', 'mois_plantation': (3, 5)},

    # ============================================================
    # 🍇 VIGNE & PETITS FRUITS (PÉRENNES)
    # ============================================================
    'vigne': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 5, 'emoji': '🍇', 'mois_plantation': (11, 3)},
    'raisin': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 5, 'emoji': '🍇', 'mois_plantation': (11, 3)},
    'kiwi': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 5, 'emoji': '🥝', 'mois_plantation': (11, 3)},
    'actinidia': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 5, 'emoji': '🥝', 'mois_plantation': (11, 3)},
    'fraisier': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🍓', 'mois_plantation': (8, 10)},
    'framboisier': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🔴', 'mois_plantation': (11, 3)},
    'groseillier': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '🔴', 'mois_plantation': (11, 3)},
    'cassisier': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '⚫', 'mois_plantation': (11, 3)},
    'cassis': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '⚫', 'mois_plantation': (11, 3)},
    'myrtillier': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🔵', 'mois_plantation': (11, 3)},
    'airellier': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🔴', 'mois_plantation': (11, 3)},
    'mûrier': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '⚫', 'mois_plantation': (11, 3)},
    'murier': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '⚫', 'mois_plantation': (11, 3)},
    'ronce': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '⚫', 'mois_plantation': (11, 3)},
    'physalis': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🟠', 'mois_plantation': (4, 5)},
    'goji': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '🔴', 'mois_plantation': (11, 3)},
    'argousier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 5, 'emoji': '🟠', 'mois_plantation': (10, 3)},

    # ============================================================
    # 🌴 FRUITS TROPICAUX / SUBTROPICAUX (PÉRENNES)
    # ============================================================
    'bananier': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🍌', 'mois_plantation': (3, 6)},
    'manguier': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🥭', 'mois_plantation': (3, 6)},
    'avocatier': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🥑', 'mois_plantation': (3, 6)},
    'papayer': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🟠', 'mois_plantation': (3, 6)},
    'ananas': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🍍', 'mois_plantation': (4, 8)},
    'litchi': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🔴', 'mois_plantation': (3, 6)},
    'longanier': {'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🟤', 'mois_plantation': (3, 6)},
    'ramboutanier': {'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🔴', 'mois_plantation': (3, 6)},
    'durianier': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '🟡', 'mois_plantation': (3, 6)},
    'mangoustanier': {'type': 'perenne', 'debut_production_annees': 6, 'pleine_production_annees': 10, 'emoji': '🟣', 'mois_plantation': (3, 6)},
    'goyavier': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🟢', 'mois_plantation': (3, 6)},
    'fruit de la passion': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🟣', 'mois_plantation': (3, 6)},
    'passiflore': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🟣', 'mois_plantation': (3, 6)},
    'fruit du dragon': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 3, 'emoji': '🩷', 'mois_plantation': (3, 6)},
    'pitaya': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 3, 'emoji': '🩷', 'mois_plantation': (3, 6)},
    'cacaoyer': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 8, 'emoji': '🍫', 'mois_plantation': (3, 6)},
    'caféier': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '☕', 'mois_plantation': (3, 6)},
    'cafeier': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '☕', 'mois_plantation': (3, 6)},
    'cocotier': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '🥥', 'mois_plantation': (3, 6)},
    'dattier': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '🌴', 'mois_plantation': (3, 6)},
    'vanillier': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🌿', 'mois_plantation': (3, 6)},
    'sapotillier': {'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🟤', 'mois_plantation': (3, 6)},
    'cherimolier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟢', 'mois_plantation': (3, 6)},
    'carambolier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟡', 'mois_plantation': (3, 6)},
    'jaboticaba': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '⚫', 'mois_plantation': (3, 6)},
    'cupuaçu': {'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🟤', 'mois_plantation': (3, 6)},
    'acérola': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🔴', 'mois_plantation': (3, 6)},
    'acerola': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🔴', 'mois_plantation': (3, 6)},
    'açaï': {'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🟣', 'mois_plantation': (3, 6)},
    'acai': {'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🟣', 'mois_plantation': (3, 6)},
    'aguaje': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 8, 'emoji': '🟤', 'mois_plantation': (3, 6)},
    'achacha': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟡', 'mois_plantation': (3, 6)},
    'canistel': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟠', 'mois_plantation': (3, 6)},
    'bilimbi': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🟢', 'mois_plantation': (3, 6)},
    'tamarinier': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '🟤', 'mois_plantation': (3, 6)},
    'safou': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '🫐', 'mois_plantation': (3, 6)},
    'safoutier': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '🫐', 'mois_plantation': (3, 6)},
    'prunier d afrique': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '🫐', 'mois_plantation': (3, 6)},
    # --- ALIAS FRUITS TROPICAUX (Culture peut porter le nom du fruit) ---
    'papaye': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🟠', 'mois_plantation': (3, 6)},
    'mangue': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🥭', 'mois_plantation': (3, 6)},
    'avocat': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🥑', 'mois_plantation': (3, 6)},
    'banane': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🍌', 'mois_plantation': (3, 6)},
    'ananas': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🍍', 'mois_plantation': (4, 8)},
    'litchi': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🔴', 'mois_plantation': (3, 6)},
    'goyave': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🟢', 'mois_plantation': (3, 6)},
    'cacao': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 8, 'emoji': '🍫', 'mois_plantation': (3, 6)},
    'café': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '☕', 'mois_plantation': (3, 6)},
    'cafe': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '☕', 'mois_plantation': (3, 6)},
    'noix de coco': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '🥥', 'mois_plantation': (3, 6)},
    'datte': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 10, 'emoji': '🌴', 'mois_plantation': (3, 6)},
    'vanille': {'est_arbre_ui': True, 'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🌿', 'mois_plantation': (3, 6)},

    # --- ALIAS FRUITS À NOYAU / À PÉPINS (Culture peut porter le nom du fruit) ---
    'cerise': {'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 8, 'emoji': '🍒', 'mois_plantation': (10, 3)},
    'pomme': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 8, 'emoji': '🍎', 'mois_plantation': (10, 3)},
    'poire': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 8, 'emoji': '🍐', 'mois_plantation': (10, 3)},
    'prune': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟣', 'mois_plantation': (10, 3)},
    'mirabelle': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟡', 'mois_plantation': (10, 3)},
    'quetsche': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟣', 'mois_plantation': (10, 3)},
    'abricot': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍑', 'mois_plantation': (10, 3)},
    'pêche': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 5, 'emoji': '🍑', 'mois_plantation': (10, 3)},
    'peche': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 5, 'emoji': '🍑', 'mois_plantation': (10, 3)},
    'nectarine': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 5, 'emoji': '🍑', 'mois_plantation': (10, 3)},
    'amande': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 8, 'emoji': '🌰', 'mois_plantation': (10, 2)},
    'noix': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 15, 'emoji': '🌰', 'mois_plantation': (10, 2)},
    'noisette': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 5, 'emoji': '🌰', 'mois_plantation': (10, 2)},
    'châtaigne': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 15, 'emoji': '🌰', 'mois_plantation': (10, 2)},
    'chataigne': {'type': 'perenne', 'debut_production_annees': 5, 'pleine_production_annees': 15, 'emoji': '🌰', 'mois_plantation': (10, 2)},
    'figue': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 5, 'emoji': '🟣', 'mois_plantation': (10, 3)},
    'grenade': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🔴', 'mois_plantation': (10, 3)},
    'olive': {'type': 'perenne', 'debut_production_annees': 4, 'pleine_production_annees': 10, 'emoji': '🫒', 'mois_plantation': (9, 11)},
    'kaki': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🟠', 'mois_plantation': (10, 3)},
    'coing': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 6, 'emoji': '🟡', 'mois_plantation': (10, 3)},
    'nashi': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍐', 'mois_plantation': (10, 3)},

    # --- ALIAS AGRUMES ---
    'orange': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍊', 'mois_plantation': (3, 5)},
    'citron': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍋', 'mois_plantation': (3, 5)},
    'pamplemousse': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍊', 'mois_plantation': (3, 5)},
    'mandarine': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍊', 'mois_plantation': (3, 5)},
    'clémentine': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍊', 'mois_plantation': (3, 5)},
    'clementine': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 7, 'emoji': '🍊', 'mois_plantation': (3, 5)},

    # --- ALIAS BAIES ---
    'fraise': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🍓', 'mois_plantation': (8, 10)},
    'framboise': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🔴', 'mois_plantation': (11, 3)},
    'groseille': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '🔴', 'mois_plantation': (11, 3)},
    'groseille à maquereau': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '🟢', 'mois_plantation': (11, 3)},
    'groseille a maquereau': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '🟢', 'mois_plantation': (11, 3)},
    'cassis': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '⚫', 'mois_plantation': (11, 3)},
    'myrtille': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🔵', 'mois_plantation': (11, 3)},
    'mûre': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '⚫', 'mois_plantation': (11, 3)},
    'mure': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '⚫', 'mois_plantation': (11, 3)},
    'airelle': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🔴', 'mois_plantation': (11, 3)},
    'goji': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 3, 'emoji': '🔴', 'mois_plantation': (11, 3)},
    'argousier': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 5, 'emoji': '🟠', 'mois_plantation': (10, 3)},

    # ============================================================
    # 🌿 AROMATIQUES VIVACES (PÉRENNES)
    # ============================================================
    'romarin': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'thym': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'sauge': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'lavande': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 3, 'emoji': '💜', 'mois_plantation': (3, 5)},
    'origan': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'marjolaine': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'estragon': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'ciboulette': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'menthe': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'mélisse': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'melisse': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'verveine': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'laurier': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'sarriette': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'hysope': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},

    # ============================================================
    # 🌸 FLEURS VIVACES (PÉRENNES)
    # ============================================================
    'rose': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌹', 'mois_plantation': (11, 3)},
    'rosier': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌹', 'mois_plantation': (11, 3)},
    'pivoine': {'type': 'perenne', 'debut_production_annees': 2, 'pleine_production_annees': 4, 'emoji': '🌺', 'mois_plantation': (9, 11)},
    'iris': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌸', 'mois_plantation': (7, 9)},
    'hortensia': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 3, 'emoji': '💐', 'mois_plantation': (10, 11)},
    'jasmin': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 3, 'emoji': '🌸', 'mois_plantation': (3, 5)},
    'chèvrefeuille': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌸', 'mois_plantation': (10, 3)},
    'chevrefeuille': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌸', 'mois_plantation': (10, 3)},
    'glycine': {'type': 'perenne', 'debut_production_annees': 3, 'pleine_production_annees': 5, 'emoji': '💜', 'mois_plantation': (10, 3)},
    'clématite': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '💜', 'mois_plantation': (10, 3)},
    'clematite': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '💜', 'mois_plantation': (10, 3)},
    'buddleia': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '💜', 'mois_plantation': (10, 3)},
    'plumeria': {'type': 'perenne', 'est_arbre_ui': True, 'debut_production_annees': 3, 'pleine_production_annees': 5, 'emoji': '🌸', 'mois_plantation': (3, 6)},
    'frangipanier': {'type': 'perenne', 'est_arbre_ui': True, 'debut_production_annees': 3, 'pleine_production_annees': 5, 'emoji': '🌸', 'mois_plantation': (3, 6)},

    # ============================================================
    # 🥬 LÉGUMES-FRUITS (ANNUELLES)
    # ============================================================
    'tomate': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 80, 'duree_jours_max': 110, 'emoji': '🍅', 'mois_plantation': (4, 5)},
    'tomate cerise': {'type': 'annuelle', 'duree_jours': 80, 'duree_jours_min': 70, 'duree_jours_max': 90, 'emoji': '🍅', 'mois_plantation': (4, 5)},
    'tomate ancienne': {'type': 'annuelle', 'duree_jours': 95, 'duree_jours_min': 85, 'duree_jours_max': 110, 'emoji': '🍅', 'mois_plantation': (4, 5)},
    'aubergine': {'type': 'annuelle', 'duree_jours': 110, 'duree_jours_min': 100, 'duree_jours_max': 130, 'emoji': '🍆', 'mois_plantation': (4, 5)},
    'poivron': {'type': 'annuelle', 'duree_jours': 100, 'duree_jours_min': 90, 'duree_jours_max': 120, 'emoji': '🫑', 'mois_plantation': (4, 5)},
    'piment': {'type': 'annuelle', 'duree_jours': 100, 'duree_jours_min': 90, 'duree_jours_max': 120, 'emoji': '🌶️', 'mois_plantation': (4, 5)},
    'piment fort': {'type': 'annuelle', 'duree_jours': 110, 'duree_jours_min': 100, 'duree_jours_max': 130, 'emoji': '🌶️', 'mois_plantation': (4, 5)},
    'concombre': {'type': 'annuelle', 'duree_jours': 65, 'duree_jours_min': 55, 'duree_jours_max': 75, 'emoji': '🥒', 'mois_plantation': (4, 6)},
    'cornichon': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 70, 'emoji': '🥒', 'mois_plantation': (4, 6)},
    'courgette': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 70, 'emoji': '🥒', 'mois_plantation': (4, 6)},
    'potiron': {'type': 'annuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 140, 'emoji': '🎃', 'mois_plantation': (4, 6)},
    'citrouille': {'type': 'annuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 140, 'emoji': '🎃', 'mois_plantation': (4, 6)},
    'courge': {'type': 'annuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 140, 'emoji': '🎃', 'mois_plantation': (4, 6)},
    'butternut': {'type': 'annuelle', 'duree_jours': 110, 'duree_jours_min': 100, 'duree_jours_max': 120, 'emoji': '🎃', 'mois_plantation': (4, 6)},
    'melon': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 80, 'duree_jours_max': 110, 'emoji': '🍈', 'mois_plantation': (4, 6)},
    'pastèque': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 80, 'duree_jours_max': 110, 'emoji': '🍉', 'mois_plantation': (4, 6)},
    'pasteque': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 80, 'duree_jours_max': 110, 'emoji': '🍉', 'mois_plantation': (4, 6)},
    'kiwano': {'type': 'annuelle', 'duree_jours': 80, 'duree_jours_min': 70, 'duree_jours_max': 90, 'emoji': '🟠', 'mois_plantation': (4, 6)},

    # ============================================================
    # 🥕 LÉGUMES-RACINES (ANNUELLES / BISANNUELLES)
    # ============================================================
    'carotte': {'type': 'annuelle', 'duree_jours': 70, 'duree_jours_min': 60, 'duree_jours_max': 90, 'emoji': '🥕', 'mois_plantation': (3, 7)},
    'radis': {'type': 'annuelle', 'duree_jours': 25, 'duree_jours_min': 18, 'duree_jours_max': 30, 'emoji': '🔴', 'mois_plantation': (3, 9)},
    'radis noir': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 70, 'emoji': '⚫', 'mois_plantation': (7, 9)},
    'betterave': {'type': 'bisannuelle', 'duree_jours': 90, 'duree_jours_min': 80, 'duree_jours_max': 110, 'emoji': '🔴', 'mois_plantation': (4, 7)},
    'navet': {'type': 'bisannuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 80, 'emoji': '⚪', 'mois_plantation': (3, 9)},
    'rutabaga': {'type': 'bisannuelle', 'duree_jours': 90, 'duree_jours_min': 80, 'duree_jours_max': 110, 'emoji': '🟡', 'mois_plantation': (6, 8)},
    'panais': {'type': 'bisannuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 150, 'emoji': '⚪', 'mois_plantation': (3, 6)},
    'salsifis': {'type': 'bisannuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 150, 'emoji': '⚫', 'mois_plantation': (3, 5)},
    'scorsonère': {'type': 'bisannuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 150, 'emoji': '⚫', 'mois_plantation': (3, 5)},
    'céleri-rave': {'type': 'bisannuelle', 'duree_jours': 140, 'duree_jours_min': 120, 'duree_jours_max': 160, 'emoji': '⚪', 'mois_plantation': (4, 6)},
    'celeri-rave': {'type': 'bisannuelle', 'duree_jours': 140, 'duree_jours_min': 120, 'duree_jours_max': 160, 'emoji': '⚪', 'mois_plantation': (4, 6)},
    'raifort': {'type': 'bisannuelle', 'duree_jours': 150, 'duree_jours_min': 120, 'duree_jours_max': 180, 'emoji': '⚪', 'mois_plantation': (3, 5)},
    'topinambour': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌻', 'mois_plantation': (2, 4)},
    'patate douce': {'type': 'annuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 140, 'emoji': '🍠', 'mois_plantation': (5, 6)},

    # ============================================================
    # 🥔 TUBERCULES (ANNUELLES)
    # ============================================================
    'pomme de terre': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 70, 'duree_jours_max': 120, 'emoji': '🥔', 'mois_plantation': (3, 5)},
    'patate': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 70, 'duree_jours_max': 120, 'emoji': '🥔', 'mois_plantation': (3, 5)},

    # ============================================================
    # 🧄 BULBES (ANNUELLES / BISANNUELLES)
    # ============================================================
    'oignon': {'type': 'bisannuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 150, 'emoji': '🧅', 'mois_plantation': (2, 4)},
    'oignon rouge': {'type': 'bisannuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 150, 'emoji': '🧅', 'mois_plantation': (2, 4)},
    'oignon blanc': {'type': 'bisannuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 150, 'emoji': '🧅', 'mois_plantation': (2, 4)},
    'échalote': {'type': 'bisannuelle', 'duree_jours': 150, 'duree_jours_min': 120, 'duree_jours_max': 180, 'emoji': '🧅', 'mois_plantation': (2, 3)},
    'echalote': {'type': 'bisannuelle', 'duree_jours': 150, 'duree_jours_min': 120, 'duree_jours_max': 180, 'emoji': '🧅', 'mois_plantation': (2, 3)},
    'ail': {'type': 'bisannuelle', 'duree_jours': 240, 'duree_jours_min': 210, 'duree_jours_max': 270, 'emoji': '🧄', 'mois_plantation': (10, 12)},
    'ail rose': {'type': 'bisannuelle', 'duree_jours': 240, 'duree_jours_min': 210, 'duree_jours_max': 270, 'emoji': '🧄', 'mois_plantation': (10, 12)},
    'poireau': {'type': 'bisannuelle', 'duree_jours': 150, 'duree_jours_min': 120, 'duree_jours_max': 180, 'emoji': '🌿', 'mois_plantation': (2, 5)},

    # ============================================================
    # 🥬 LÉGUMES-FEUILLES (ANNUELLES)
    # ============================================================
    'salade': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 45, 'duree_jours_max': 75, 'emoji': '🥬', 'mois_plantation': (3, 8)},
    'laitue': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 45, 'duree_jours_max': 75, 'emoji': '🥬', 'mois_plantation': (3, 8)},
    'batavia': {'type': 'annuelle', 'duree_jours': 55, 'duree_jours_min': 45, 'duree_jours_max': 70, 'emoji': '🥬', 'mois_plantation': (3, 8)},
    'roquette': {'type': 'annuelle', 'duree_jours': 35, 'duree_jours_min': 25, 'duree_jours_max': 45, 'emoji': '🥬', 'mois_plantation': (3, 9)},
    'mâche': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 75, 'emoji': '🥬', 'mois_plantation': (8, 10)},
    'mache': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 75, 'emoji': '🥬', 'mois_plantation': (8, 10)},
    'épinard': {'type': 'annuelle', 'duree_jours': 50, 'duree_jours_min': 40, 'duree_jours_max': 60, 'emoji': '🥬', 'mois_plantation': (3, 9)},
    'epinard': {'type': 'annuelle', 'duree_jours': 50, 'duree_jours_min': 40, 'duree_jours_max': 60, 'emoji': '🥬', 'mois_plantation': (3, 9)},
    'blette': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 80, 'emoji': '🥬', 'mois_plantation': (4, 7)},
    'oseille': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌿', 'mois_plantation': (3, 5)},
    'cresson': {'type': 'annuelle', 'duree_jours': 30, 'duree_jours_min': 20, 'duree_jours_max': 40, 'emoji': '🌿', 'mois_plantation': (3, 9)},
    'pourpier': {'type': 'annuelle', 'duree_jours': 40, 'duree_jours_min': 30, 'duree_jours_max': 50, 'emoji': '🌿', 'mois_plantation': (5, 8)},

    # ============================================================
    # 🥬 CHOUX (BISANNUELLES)
    # ============================================================
    'chou': {'type': 'bisannuelle', 'duree_jours': 120, 'duree_jours_min': 90, 'duree_jours_max': 150, 'emoji': '🥬', 'mois_plantation': (3, 7)},
    'chou vert': {'type': 'bisannuelle', 'duree_jours': 120, 'duree_jours_min': 90, 'duree_jours_max': 150, 'emoji': '🥬', 'mois_plantation': (3, 7)},
    'chou rouge': {'type': 'bisannuelle', 'duree_jours': 120, 'duree_jours_min': 90, 'duree_jours_max': 150, 'emoji': '🥬', 'mois_plantation': (3, 7)},
    'chou blanc': {'type': 'bisannuelle', 'duree_jours': 120, 'duree_jours_min': 90, 'duree_jours_max': 150, 'emoji': '🥬', 'mois_plantation': (3, 7)},
    'chou frisé': {'type': 'bisannuelle', 'duree_jours': 110, 'duree_jours_min': 90, 'duree_jours_max': 140, 'emoji': '🥬', 'mois_plantation': (5, 7)},
    'chou pommé': {'type': 'bisannuelle', 'duree_jours': 120, 'duree_jours_min': 90, 'duree_jours_max': 150, 'emoji': '🥬', 'mois_plantation': (3, 7)},
    'chou de bruxelles': {'type': 'bisannuelle', 'duree_jours': 150, 'duree_jours_min': 120, 'duree_jours_max': 180, 'emoji': '🥬', 'mois_plantation': (4, 6)},
    'chou-fleur': {'type': 'bisannuelle', 'duree_jours': 150, 'duree_jours_min': 90, 'duree_jours_max': 200, 'emoji': '🥦', 'mois_plantation': (3, 7)},
    'chou fleur': {'type': 'bisannuelle', 'duree_jours': 150, 'duree_jours_min': 90, 'duree_jours_max': 200, 'emoji': '🥦', 'mois_plantation': (3, 7)},
    'brocoli': {'type': 'annuelle', 'duree_jours': 100, 'duree_jours_min': 80, 'duree_jours_max': 130, 'emoji': '🥦', 'mois_plantation': (3, 7)},
    'chou-rave': {'type': 'bisannuelle', 'duree_jours': 80, 'duree_jours_min': 60, 'duree_jours_max': 100, 'emoji': '🥬', 'mois_plantation': (3, 7)},
    'chou rave': {'type': 'bisannuelle', 'duree_jours': 80, 'duree_jours_min': 60, 'duree_jours_max': 100, 'emoji': '🥬', 'mois_plantation': (3, 7)},
    'chou chinois': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 80, 'emoji': '🥬', 'mois_plantation': (7, 9)},
    'endive': {'type': 'bisannuelle', 'duree_jours': 180, 'duree_jours_min': 150, 'duree_jours_max': 210, 'emoji': '🥬', 'mois_plantation': (5, 6)},

    # ============================================================
    # 🫘 LÉGUMINEUSES (ANNUELLES)
    # ============================================================
    'haricot': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 80, 'emoji': '🫘', 'mois_plantation': (5, 7)},
    'haricot vert': {'type': 'annuelle', 'duree_jours': 55, 'duree_jours_min': 45, 'duree_jours_max': 70, 'emoji': '🫘', 'mois_plantation': (5, 7)},
    'haricot nain': {'type': 'annuelle', 'duree_jours': 55, 'duree_jours_min': 45, 'duree_jours_max': 70, 'emoji': '🫘', 'mois_plantation': (5, 7)},
    'haricot grimpant': {'type': 'annuelle', 'duree_jours': 75, 'duree_jours_min': 60, 'duree_jours_max': 90, 'emoji': '🫘', 'mois_plantation': (5, 7)},
    'haricot rouge': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 80, 'duree_jours_max': 110, 'emoji': '🫘', 'mois_plantation': (5, 6)},
    'haricot blanc': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 80, 'duree_jours_max': 110, 'emoji': '🫘', 'mois_plantation': (5, 6)},
    'petit pois': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 70, 'duree_jours_max': 110, 'emoji': '🫛', 'mois_plantation': (2, 5)},
    'pois': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 70, 'duree_jours_max': 110, 'emoji': '🫛', 'mois_plantation': (2, 5)},
    'pois chiche': {'type': 'annuelle', 'duree_jours': 100, 'duree_jours_min': 90, 'duree_jours_max': 120, 'emoji': '🫘', 'mois_plantation': (3, 5)},
    'fève': {'type': 'annuelle', 'duree_jours': 100, 'duree_jours_min': 80, 'duree_jours_max': 120, 'emoji': '🫘', 'mois_plantation': (2, 4)},
    'feve': {'type': 'annuelle', 'duree_jours': 100, 'duree_jours_min': 80, 'duree_jours_max': 120, 'emoji': '🫘', 'mois_plantation': (2, 4)},
    'lentille': {'type': 'annuelle', 'duree_jours': 100, 'duree_jours_min': 90, 'duree_jours_max': 120, 'emoji': '🫘', 'mois_plantation': (3, 4)},
    'soja': {'type': 'annuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 140, 'emoji': '🫘', 'mois_plantation': (5, 6)},
    'edamame': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 80, 'duree_jours_max': 100, 'emoji': '🫛', 'mois_plantation': (5, 6)},
    'arachide': {'type': 'annuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 140, 'emoji': '🥜', 'mois_plantation': (5, 6)},

    # ============================================================
    # 🌾 CÉRÉALES (ANNUELLES)
    # ============================================================
    'blé': {'type': 'annuelle', 'duree_jours': 240, 'duree_jours_min': 200, 'duree_jours_max': 280, 'emoji': '🌾', 'mois_plantation': (10, 11)},
    'ble': {'type': 'annuelle', 'duree_jours': 240, 'duree_jours_min': 200, 'duree_jours_max': 280, 'emoji': '🌾', 'mois_plantation': (10, 11)},
    'orge': {'type': 'annuelle', 'duree_jours': 210, 'duree_jours_min': 180, 'duree_jours_max': 240, 'emoji': '🌾', 'mois_plantation': (10, 11)},
    'avoine': {'type': 'annuelle', 'duree_jours': 150, 'duree_jours_min': 130, 'duree_jours_max': 180, 'emoji': '🌾', 'mois_plantation': (3, 4)},
    'seigle': {'type': 'annuelle', 'duree_jours': 260, 'duree_jours_min': 230, 'duree_jours_max': 300, 'emoji': '🌾', 'mois_plantation': (10, 11)},
    'maïs': {'type': 'annuelle', 'duree_jours': 100, 'duree_jours_min': 85, 'duree_jours_max': 130, 'emoji': '🌽', 'mois_plantation': (4, 6)},
    'mais': {'type': 'annuelle', 'duree_jours': 100, 'duree_jours_min': 85, 'duree_jours_max': 130, 'emoji': '🌽', 'mois_plantation': (4, 6)},
    'riz': {'type': 'annuelle', 'duree_jours': 150, 'duree_jours_min': 120, 'duree_jours_max': 180, 'emoji': '🍚', 'mois_plantation': (4, 6)},
    'millet': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 70, 'duree_jours_max': 120, 'emoji': '🌾', 'mois_plantation': (5, 6)},
    'sorgho': {'type': 'annuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 140, 'emoji': '🌾', 'mois_plantation': (5, 6)},
    'quinoa': {'type': 'annuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 140, 'emoji': '🌾', 'mois_plantation': (4, 5)},
    'sarrasin': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 70, 'duree_jours_max': 110, 'emoji': '🌾', 'mois_plantation': (5, 6)},

    # ============================================================
    # 🌿 AROMATIQUES ANNUELLES (ANNUELLES)
    # ============================================================
    'basilic': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 80, 'emoji': '🌿', 'mois_plantation': (5, 6)},
    'persil': {'type': 'bisannuelle', 'duree_jours': 90, 'duree_jours_min': 75, 'duree_jours_max': 110, 'emoji': '🌿', 'mois_plantation': (3, 7)},
    'coriandre': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 80, 'emoji': '🌿', 'mois_plantation': (4, 8)},
    'aneth': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 45, 'duree_jours_max': 75, 'emoji': '🌿', 'mois_plantation': (4, 7)},
    'fenouil': {'type': 'bisannuelle', 'duree_jours': 100, 'duree_jours_min': 80, 'duree_jours_max': 130, 'emoji': '🌿', 'mois_plantation': (5, 7)},
    'cumin': {'type': 'annuelle', 'duree_jours': 120, 'duree_jours_min': 100, 'duree_jours_max': 140, 'emoji': '🌿', 'mois_plantation': (4, 5)},
    'curcuma': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🧡', 'mois_plantation': (4, 5)},
    'gingembre': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🫚', 'mois_plantation': (4, 5)},

    # ============================================================
    # 🌸 FLEURS ANNUELLES (ANNUELLES)
    # ============================================================
    'tournesol': {'type': 'annuelle', 'duree_jours': 100, 'duree_jours_min': 80, 'duree_jours_max': 120, 'emoji': '🌻', 'mois_plantation': (4, 6)},
    'souci': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 80, 'emoji': '🌼', 'mois_plantation': (4, 6)},
    'œillet d\'inde': {'type': 'annuelle', 'duree_jours': 70, 'duree_jours_min': 60, 'duree_jours_max': 90, 'emoji': '🌼', 'mois_plantation': (4, 6)},
    'oeillet d inde': {'type': 'annuelle', 'duree_jours': 70, 'duree_jours_min': 60, 'duree_jours_max': 90, 'emoji': '🌼', 'mois_plantation': (4, 6)},
    'capucine': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 80, 'emoji': '🌺', 'mois_plantation': (4, 6)},
    'cosmos': {'type': 'annuelle', 'duree_jours': 80, 'duree_jours_min': 70, 'duree_jours_max': 100, 'emoji': '🌸', 'mois_plantation': (4, 6)},
    'zinnia': {'type': 'annuelle', 'duree_jours': 70, 'duree_jours_min': 60, 'duree_jours_max': 90, 'emoji': '🌸', 'mois_plantation': (4, 6)},
    'bourrache': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 80, 'emoji': '💙', 'mois_plantation': (4, 6)},
    'phacélie': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 80, 'emoji': '💜', 'mois_plantation': (4, 7)},
    'phacelie': {'type': 'annuelle', 'duree_jours': 60, 'duree_jours_min': 50, 'duree_jours_max': 80, 'emoji': '💜', 'mois_plantation': (4, 7)},
    'nigelle': {'type': 'annuelle', 'duree_jours': 80, 'duree_jours_min': 70, 'duree_jours_max': 100, 'emoji': '💙', 'mois_plantation': (4, 5)},
    'coquelicot': {'type': 'annuelle', 'duree_jours': 80, 'duree_jours_min': 70, 'duree_jours_max': 100, 'emoji': '🌺', 'mois_plantation': (3, 5)},
    'bleuet': {'type': 'annuelle', 'duree_jours': 80, 'duree_jours_min': 70, 'duree_jours_max': 100, 'emoji': '💙', 'mois_plantation': (3, 5)},
    'marguerite': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌼', 'mois_plantation': (3, 5)},
    'tulipe': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌷', 'mois_plantation': (9, 11)},
    'jonquille': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '💛', 'mois_plantation': (9, 11)},
    'narcisse': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '💛', 'mois_plantation': (9, 11)},
    'dahlia': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌸', 'mois_plantation': (4, 5)},
    'glaïeul': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌸', 'mois_plantation': (3, 5)},
    'glaieul': {'type': 'perenne', 'debut_production_annees': 1, 'pleine_production_annees': 2, 'emoji': '🌸', 'mois_plantation': (3, 5)},

    # ============================================================
    # 🍄 CHAMPIGNONS (quelques cycles — cas particuliers)
    # ============================================================
    'champignon': {'type': 'annuelle', 'duree_jours': 30, 'duree_jours_min': 20, 'duree_jours_max': 45, 'emoji': '🍄'},
    'pleurote': {'type': 'annuelle', 'duree_jours': 30, 'duree_jours_min': 20, 'duree_jours_max': 45, 'emoji': '🍄'},
    'shiitake': {'type': 'annuelle', 'duree_jours': 90, 'duree_jours_min': 60, 'duree_jours_max': 120, 'emoji': '🍄'},


    # ============================================================
    # 🍅 VARIÉTÉS SPÉCIFIQUES (Surcharge du parent pour précision)
    # ============================================================

    # --- TOMATES ---
    'tomate cerise': {'type': 'annuelle', 'duree_jours': 75, 'emoji': '🍅'},
    'cherry': {'type': 'annuelle', 'duree_jours': 75, 'emoji': '🍅'},
    'roma': {'type': 'annuelle', 'duree_jours': 85, 'emoji': '🍅'},
    'san marzano': {'type': 'annuelle', 'duree_jours': 85, 'emoji': '🍅'},
    'andine cornue': {'type': 'annuelle', 'duree_jours': 95, 'emoji': '🍅'},
    'coeur de boeuf': {'type': 'annuelle', 'duree_jours': 100, 'emoji': '🍅'},
    'green zebra': {'type': 'annuelle', 'duree_jours': 90, 'emoji': '🍅'},
    'noire de crimee': {'type': 'annuelle', 'duree_jours': 90, 'emoji': '🍅'},

    # --- PIMENTS & POIVRONS ---
    'poivron': {'type': 'annuelle', 'duree_jours': 100, 'emoji': '🫑'},
    'bell pepper': {'type': 'annuelle', 'duree_jours': 90, 'emoji': '🫑'},
    'poblano': {'type': 'annuelle', 'duree_jours': 90, 'emoji': '🫑'},
    'shishito': {'type': 'annuelle', 'duree_jours': 80, 'emoji': '🫑'},
    'jalapeno': {'type': 'annuelle', 'duree_jours': 80, 'emoji': '🌶️'},
    'habanero': {'type': 'annuelle', 'duree_jours': 110, 'emoji': '🌶️'},

    # --- SALADES ---
    'batavia': {'type': 'annuelle', 'duree_jours': 50, 'emoji': '🥬'},
    'iceberg': {'type': 'annuelle', 'duree_jours': 75, 'emoji': '🥬'},
    'romaine': {'type': 'annuelle', 'duree_jours': 65, 'emoji': '🥬'},
    'feuille de chene': {'type': 'annuelle', 'duree_jours': 50, 'emoji': '🥬'},

    # --- POMMES DE TERRE ---
    'charlotte': {'type': 'annuelle', 'duree_jours': 75, 'emoji': '🥔'},
    'charlott': {'type': 'annuelle', 'duree_jours': 75, 'emoji': '🥔'},
    'ratte': {'type': 'annuelle', 'duree_jours': 110, 'emoji': '🥔'},
    'bintje': {'type': 'annuelle', 'duree_jours': 100, 'emoji': '🥔'},
    'yukon gold': {'type': 'annuelle', 'duree_jours': 90, 'emoji': '🥔'},
    'russet': {'type': 'annuelle', 'duree_jours': 110, 'emoji': '🥔'},

    # --- FRAISES ---
    'gariguette': {'type': 'perenne', 'debut_production_annees': 1, 'emoji': '🍓'},
    'ciflorette': {'type': 'perenne', 'debut_production_annees': 1, 'emoji': '🍓'},
    'mara des bois': {'type': 'perenne', 'debut_production_annees': 1, 'emoji': '🍓'},
    'albion': {'type': 'perenne', 'debut_production_annees': 1, 'emoji': '🍓'},
    'chandler': {'type': 'perenne', 'debut_production_annees': 1, 'emoji': '🍓'},

    # --- MAÏS ---
    'sweet corn': {'type': 'annuelle', 'duree_jours': 80, 'emoji': '🌽'},
    'silver queen': {'type': 'annuelle', 'duree_jours': 85, 'emoji': '🌽'},

    # --- SOJA / EDAMAME ---
    'edamame': {'type': 'annuelle', 'duree_jours': 80, 'emoji': '🫛'},
    'enrei': {'type': 'annuelle', 'duree_jours': 90, 'emoji': '🫛'},

    # --- AGRUMES ---
    'eureka': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍋'},
    'meyer': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍋'},
    'lisbon': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍋'},
    'hamlin': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍊'},
    'valencia': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍊'},
    'washington navel': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍊'},
    'pineapple': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍊'},

    # --- POMMES ---
    'golden delicious': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍎'},
    'granny smith': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍎'},
    'gala': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍎'},
    'fuji': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍎'},
    'pink lady': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍎'},
    'reinette': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍎'},
    'cox orange': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍎'},
    'jonagold': {'type': 'perenne', 'debut_production_annees': 3, 'emoji': '🍎'},



}


# ============================================================
# HELPER DE RÉSOLUTION
# ============================================================

import unicodedata

def _nettoyer_nom(nom):
    """Retire les accents, les caractères spéciaux (œ, æ) et met en minuscule."""
    if not nom:
        return ""
    # Remplace les ligatures manuelles
    nom = nom.replace('œ', 'oe').replace('Œ', 'OE').replace('æ', 'ae').replace('Æ', 'AE')
    # Normalise et retire les accents
    nom = ''.join(c for c in unicodedata.normalize('NFD', nom) if unicodedata.category(c) != 'Mn')
    return nom.lower().strip()

def get_cycle(culture_nom, _depth=0):
    """
    Retourne le dict de cycle pour une culture (recherche exacte, variété, floue).
    """
    if not culture_nom or _depth > 3:
        return None

    cle = _nettoyer_nom(culture_nom)

    # 1. Correspondance exacte (nettoyée)
    for k, v in CYCLES_CULTURES.items():
        if _nettoyer_nom(k) == cle:
            return v

    # 2. Résolution via Variete → Culture
    if _depth == 0:
        try:
            from vegetables_fruits.models import Variete
            # On utilise __iexact qui est en général insensible à la casse dans SQLite
            variete = Variete.objects.select_related('culture').filter(nom__iexact=culture_nom.strip()).first()
            if variete and variete.culture:
                return get_cycle(variete.culture.nom, _depth=_depth + 1)
        except Exception:
            pass

    # 3. Correspondance partielle par clé la plus longue
    cles_triees = sorted(CYCLES_CULTURES.keys(), key=len, reverse=True)
    for cycle_cle in cles_triees:
        cle_nettoyee = _nettoyer_nom(cycle_cle)
        if cle_nettoyee in cle or cle in cle_nettoyee:
            return CYCLES_CULTURES[cycle_cle]

    # 4. Correspondance sur le premier mot
    premier_mot = cle.split()[0] if cle.split() else ''
    if premier_mot:
        for k, v in CYCLES_CULTURES.items():
            if _nettoyer_nom(k).split()[0] == premier_mot:
                return v

    return None

