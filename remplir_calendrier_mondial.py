# Script : remplir_calendrier_mondial.py
# À exécuter dans : python manage.py shell
# Ce script remplit le calendrier des semis pour toutes les régions du monde

from vegetables_fruits.models import CalendrierSemis

# ==================== DONNÉES MONDIALES ====================

# Structure :
# {
# 'region': 'nom_de_la_region',
# 'cultures': [
# {'nom': 'culture', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 1, 'mois_recolte_fin': 12, 'type': 'pleine_terre'},
# ]
# }

DONNEES_MONDIALES = [

    # ============================================================
    # 🌍 AFRIQUE
    # ============================================================

    # Afrique du Nord (climat méditerranéen / désertique)
    {
        'region': 'afrique_nord',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 5, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 3, 'mois_recolte_fin': 5,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 5, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 6, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Aubergine', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 6, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Haricot', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Oignon', 'mois_debut': 1, 'mois_fin': 2, 'mois_recolte_debut': 6, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Ail', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 5, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 4, 'mois_recolte_fin': 5,
             'type': 'pleine_terre'},
            {'nom': 'Melon', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Pastèque', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Figue', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Grenade', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 8, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Abricot', 'mois_debut': 1, 'mois_fin': 2, 'mois_recolte_debut': 5, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Pêche', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Olive', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
        ]
    },

    # Afrique de l'Ouest (climat tropical)
    {
        'region': 'afrique_ouest',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 2, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Gombo (Okra)', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Manioc', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Igname', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 11,
             'type': 'pleine_terre'},
            {'nom': 'Cacao', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 4, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Café', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Ananas', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 12, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Banane', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Mangue', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 4, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Papaye', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
        ]
    },

    # Afrique de l'Est (climat tropical / montagnard)
    {
        'region': 'afrique_est',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 2, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 4, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 5, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Maïs', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Café', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Thé', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Avocat', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
        ]
    },

    # Afrique Australe (climat tempéré)
    {
        'region': 'afrique_australe',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 1, 'mois_recolte_fin': 3,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 8, 'mois_fin': 12, 'mois_recolte_debut': 12, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 8, 'mois_fin': 3, 'mois_recolte_debut': 10, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 12, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 1, 'mois_recolte_fin': 3,
             'type': 'sous_abri'},
            {'nom': 'Pomme de terre', 'mois_debut': 8, 'mois_fin': 9, 'mois_recolte_debut': 12, 'mois_recolte_fin': 1,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 8, 'mois_fin': 9, 'mois_recolte_debut': 11, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 6, 'mois_fin': 8, 'mois_recolte_debut': 2, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Vigne', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 2, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Olive', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 2, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Agrumes', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 5, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
        ]
    },

    # ============================================================
    # 🌍 AMÉRIQUE DU NORD
    # ============================================================

    # États-Unis (climat tempéré)
    {
        'region': 'usa_nord_est',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 4, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 4, 'mois_fin': 8, 'mois_recolte_debut': 5, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Aubergine', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Haricot', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Oignon', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 8, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 6, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Citrouille', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 10, 'mois_recolte_fin': 11,
             'type': 'pleine_terre'},
        ]
    },

    # Californie (climat méditerranéen)
    {
        'region': 'californie',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 2, 'mois_fin': 6, 'mois_recolte_debut': 5, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 1, 'mois_fin': 10, 'mois_recolte_debut': 3, 'mois_recolte_fin': 11,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 4, 'mois_fin': 6, 'mois_recolte_debut': 6, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Aubergine', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 4, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Avocat', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Agrumes', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 11, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Vigne', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 8, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Amande', 'mois_debut': 1, 'mois_fin': 2, 'mois_recolte_debut': 8, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Olive', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
        ]
    },

    # Canada (climat froid)
    {
        'region': 'canada',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 8, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Carotte', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 8, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 5, 'mois_fin': 8, 'mois_recolte_debut': 6, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 8, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Haricot', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 8, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Oignon', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 8, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Érable', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 3, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
        ]
    },

    # Mexique (climat tropical / désertique)
    {
        'region': 'mexique',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 2, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Maïs', 'mois_debut': 3, 'mois_fin': 6, 'mois_recolte_debut': 8, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Avocat', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Agrumes', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Mangue', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 4, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Papaye', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Pitaya (Fruit du dragon)', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6,
             'mois_recolte_fin': 12, 'type': 'pleine_terre'},
        ]
    },

    # ============================================================
    # 🌍 AMÉRIQUE CENTRALE & CARAÏBES
    # ============================================================

    {
        'region': 'amerique_centrale',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 2, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Banane', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Mangue', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 4, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Ananas', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 12, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Cacao', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 4, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Café', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
        ]
    },

    # ============================================================
    # 🌍 AMÉRIQUE DU SUD
    # ============================================================

    # Amazonie (climat équatorial)
    {
        'region': 'amazonie',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 2, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Manioc', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Cacao', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 4, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Café', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Banane', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Ananas', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 12, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Cupuaçu', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Açai', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
        ]
    },

    # Brésil (climat tropical / tempéré)
    {
        'region': 'bresil',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 11, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 8, 'mois_fin': 12, 'mois_recolte_debut': 12, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 8, 'mois_fin': 3, 'mois_recolte_debut': 10, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 11, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 11, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Maïs', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 12, 'mois_recolte_fin': 3,
             'type': 'pleine_terre'},
            {'nom': 'Café', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 5, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Orange', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 5, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
        ]
    },

    # Argentine (climat tempéré)
    {
        'region': 'argentine',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 1, 'mois_recolte_fin': 3,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 9, 'mois_fin': 12, 'mois_recolte_debut': 12, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 9, 'mois_fin': 3, 'mois_recolte_debut': 11, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 12, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 1, 'mois_recolte_fin': 3,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 9, 'mois_fin': 10, 'mois_recolte_debut': 1, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Vigne', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 3, 'mois_recolte_fin': 5,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 8, 'mois_fin': 9, 'mois_recolte_debut': 3, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
        ]
    },

    # Chili (climat méditerranéen / tempéré)
    {
        'region': 'chili',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 1, 'mois_recolte_fin': 3,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 9, 'mois_fin': 12, 'mois_recolte_debut': 12, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 9, 'mois_fin': 3, 'mois_recolte_debut': 11, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 1, 'mois_recolte_fin': 3,
             'type': 'pleine_terre'},
            {'nom': 'Avocat', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 3, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Vigne', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 3, 'mois_recolte_fin': 5,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 11, 'mois_recolte_fin': 1,
             'type': 'pleine_terre'},
        ]
    },

    # ============================================================
    # 🌍 ASIE
    # ============================================================

    # Chine (climat tempéré / continental)
    {
        'region': 'chine',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 3, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 3, 'mois_fin': 8, 'mois_recolte_debut': 5, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 4, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Aubergine', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Haricot', 'mois_debut': 4, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Oignon', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 7, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Ail', 'mois_debut': 10, 'mois_fin': 11, 'mois_recolte_debut': 6, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Riz', 'mois_debut': 4, 'mois_fin': 6, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Soja', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Poire', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Pêche', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 7, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
        ]
    },

    # Japon (climat tempéré)
    {
        'region': 'japon',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 4, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 4, 'mois_fin': 8, 'mois_recolte_debut': 5, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Aubergine', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Haricot', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Riz', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Soja', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 10, 'mois_recolte_fin': 11,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 5, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Poire', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Raisin', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 8, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Cerise', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 6, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Persimmon (Kaki)', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 10,
             'mois_recolte_fin': 11, 'type': 'pleine_terre'},
        ]
    },

    # Inde (climat tropical / subtropical)
    {
        'region': 'inde',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 2, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Riz', 'mois_debut': 6, 'mois_fin': 8, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Blé', 'mois_debut': 11, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Coton', 'mois_debut': 4, 'mois_fin': 6, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Café', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Thé', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Mangue', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 4, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Banane', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Papaye', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
        ]
    },

    # Asie du Sud-Est (climat tropical)
    {
        'region': 'asie_sud_est',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 2, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 3, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Riz', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Banane', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Mangue', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 4, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Ananas', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 12, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Papaye', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Durian', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Ramboutan', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Mangoustan', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Jacquier', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Longane', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Carambole', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Pitaya', 'mois_debut': 1, 'mois_fin': 12, 'mois_recolte_debut': 6, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
        ]
    },

    # Moyen-Orient (climat désertique / méditerranéen)
    {
        'region': 'moyen_orient',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 5, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 5, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 3, 'mois_recolte_fin': 5,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 5, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 5, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 5, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Oignon', 'mois_debut': 1, 'mois_fin': 2, 'mois_recolte_debut': 6, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Ail', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 5, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 4, 'mois_recolte_fin': 5,
             'type': 'pleine_terre'},
            {'nom': 'Agrumes', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 11, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Olive', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Dattier', 'mois_debut': 1, 'mois_fin': 3, 'mois_recolte_debut': 8, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
        ]
    },

    # ============================================================
    # 🌍 EUROPE
    # ============================================================

    # France (climat tempéré) – régions détaillées
    {
        'region': 'iledefrance',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 3, 'mois_fin': 7, 'mois_recolte_debut': 6, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 3, 'mois_fin': 9, 'mois_recolte_debut': 5, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Aubergine', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Haricot', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Oignon', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 8, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Ail', 'mois_debut': 10, 'mois_fin': 11, 'mois_recolte_debut': 6, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 5, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Framboise', 'mois_debut': 10, 'mois_fin': 11, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Poire', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Cerise', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 6, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Vigne', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
        ]
    },

    {
        'region': 'provence',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 6, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 2, 'mois_fin': 6, 'mois_recolte_debut': 5, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 2, 'mois_fin': 9, 'mois_recolte_debut': 4, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 6, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Aubergine', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 2, 'mois_fin': 3, 'mois_recolte_debut': 4, 'mois_recolte_fin': 5,
             'type': 'pleine_terre'},
            {'nom': 'Melon', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Pastèque', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Vigne', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 8, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Olive', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Amande', 'mois_debut': 2, 'mois_fin': 3, 'mois_recolte_debut': 8, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Figue', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Grenade', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 10, 'mois_recolte_fin': 11,
             'type': 'pleine_terre'},
            {'nom': 'Abricot', 'mois_debut': 2, 'mois_fin': 3, 'mois_recolte_debut': 6, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Pêche', 'mois_debut': 2, 'mois_fin': 3, 'mois_recolte_debut': 7, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
        ]
    },

    {
        'region': 'bretagne',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 4, 'mois_fin': 6, 'mois_recolte_debut': 8, 'mois_recolte_fin': 10,
             'type': 'sous_abri'},
            {'nom': 'Carotte', 'mois_debut': 3, 'mois_fin': 7, 'mois_recolte_debut': 6, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 3, 'mois_fin': 9, 'mois_recolte_debut': 5, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 4, 'mois_fin': 6, 'mois_recolte_debut': 8, 'mois_recolte_fin': 10,
             'type': 'sous_abri'},
            {'nom': 'Haricot', 'mois_debut': 5, 'mois_fin': 7, 'mois_recolte_debut': 8, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 6, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Poireau', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 8, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
        ]
    },

    {
        'region': 'alsace',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 3, 'mois_fin': 7, 'mois_recolte_debut': 6, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 3, 'mois_fin': 9, 'mois_recolte_debut': 5, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Vigne', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Framboise', 'mois_debut': 10, 'mois_fin': 11, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
        ]
    },

    {
        'region': 'normandie',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 4, 'mois_fin': 6, 'mois_recolte_debut': 8, 'mois_recolte_fin': 10,
             'type': 'sous_abri'},
            {'nom': 'Carotte', 'mois_debut': 3, 'mois_fin': 7, 'mois_recolte_debut': 6, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 3, 'mois_fin': 9, 'mois_recolte_debut': 5, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 5, 'mois_fin': 7, 'mois_recolte_debut': 8, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Poire', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Poireau', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 8, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
        ]
    },

    # Europe du Sud (Italie, Espagne, Grèce)
    {
        'region': 'europe_sud',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 6, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 2, 'mois_fin': 6, 'mois_recolte_debut': 5, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 2, 'mois_fin': 9, 'mois_recolte_debut': 4, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 6, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Aubergine', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 2, 'mois_fin': 3, 'mois_recolte_debut': 4, 'mois_recolte_fin': 5,
             'type': 'pleine_terre'},
            {'nom': 'Melon', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Vigne', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 8, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Olive', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Agrumes', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 11, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
        ]
    },

    # Europe du Nord (Royaume-Uni, Allemagne, Scandinavie)
    {
        'region': 'europe_nord',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 4, 'mois_fin': 6, 'mois_recolte_debut': 8, 'mois_recolte_fin': 10,
             'type': 'sous_abri'},
            {'nom': 'Carotte', 'mois_debut': 4, 'mois_fin': 7, 'mois_recolte_debut': 7, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 4, 'mois_fin': 8, 'mois_recolte_debut': 5, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 5, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 8, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 6, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Poire', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Framboise', 'mois_debut': 10, 'mois_fin': 11, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
            {'nom': 'Groseille', 'mois_debut': 10, 'mois_fin': 11, 'mois_recolte_debut': 6, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
        ]
    },

    # ============================================================
    # 🌍 OCÉANIE
    # ============================================================

    # Australie (climat tempéré / méditerranéen / tropical)
    {
        'region': 'australie_sud_est',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 1, 'mois_recolte_fin': 3,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 9, 'mois_fin': 12, 'mois_recolte_debut': 12, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 9, 'mois_fin': 3, 'mois_recolte_debut': 11, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 12, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 1, 'mois_recolte_fin': 3,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 12, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 8, 'mois_fin': 9, 'mois_recolte_debut': 12, 'mois_recolte_fin': 1,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 11, 'mois_recolte_fin': 1,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 6, 'mois_fin': 8, 'mois_recolte_debut': 2, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Poire', 'mois_debut': 6, 'mois_fin': 8, 'mois_recolte_debut': 2, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Vigne', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 2, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Agrumes', 'mois_debut': 6, 'mois_fin': 8, 'mois_recolte_debut': 5, 'mois_recolte_fin': 7,
             'type': 'pleine_terre'},
            {'nom': 'Avocat', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 6, 'mois_recolte_fin': 8,
             'type': 'pleine_terre'},
        ]
    },

    # Nouvelle-Zélande (climat tempéré)
    {
        'region': 'nouvelle_zelande',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 1, 'mois_recolte_fin': 3,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 9, 'mois_fin': 12, 'mois_recolte_debut': 12, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 9, 'mois_fin': 3, 'mois_recolte_debut': 11, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 12, 'mois_recolte_fin': 2,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 9, 'mois_fin': 11, 'mois_recolte_debut': 1, 'mois_recolte_fin': 3,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 8, 'mois_fin': 9, 'mois_recolte_debut': 12, 'mois_recolte_fin': 1,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 11, 'mois_recolte_fin': 1,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 6, 'mois_fin': 8, 'mois_recolte_debut': 2, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Poire', 'mois_debut': 6, 'mois_fin': 8, 'mois_recolte_debut': 2, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Kiwi', 'mois_debut': 6, 'mois_fin': 8, 'mois_recolte_debut': 2, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
            {'nom': 'Vigne', 'mois_debut': 8, 'mois_fin': 10, 'mois_recolte_debut': 2, 'mois_recolte_fin': 4,
             'type': 'pleine_terre'},
        ]
    },

    # ============================================================
    # 🌍 RÉGIONS POLAIRES
    # ============================================================

    {
        'region': 'arctique',
        'cultures': [
            {'nom': 'Salade', 'mois_debut': 6, 'mois_fin': 8, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
            {'nom': 'Radis', 'mois_debut': 6, 'mois_fin': 8, 'mois_recolte_debut': 7, 'mois_recolte_fin': 8,
             'type': 'sous_abri'},
            {'nom': 'Pomme de terre', 'mois_debut': 6, 'mois_fin': 7, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'sous_abri'},
            {'nom': 'Fraise', 'mois_debut': 6, 'mois_fin': 7, 'mois_recolte_debut': 8, 'mois_recolte_fin': 9,
             'type': 'sous_abri'},
        ]
    },

    # ============================================================
    # 🌍 RÉGION "TOUS" (fallback)
    # ============================================================

    {
        'region': 'tous',
        'cultures': [
            {'nom': 'Tomate', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Carotte', 'mois_debut': 3, 'mois_fin': 7, 'mois_recolte_debut': 6, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Salade', 'mois_debut': 2, 'mois_fin': 9, 'mois_recolte_debut': 4, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Courgette', 'mois_debut': 4, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Poivron', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Haricot', 'mois_debut': 4, 'mois_fin': 6, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Pomme de terre', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
            {'nom': 'Fraise', 'mois_debut': 3, 'mois_fin': 4, 'mois_recolte_debut': 5, 'mois_recolte_fin': 6,
             'type': 'pleine_terre'},
            {'nom': 'Pommier', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Vigne', 'mois_debut': 11, 'mois_fin': 3, 'mois_recolte_debut': 9, 'mois_recolte_fin': 10,
             'type': 'pleine_terre'},
            {'nom': 'Olive', 'mois_debut': 2, 'mois_fin': 4, 'mois_recolte_debut': 10, 'mois_recolte_fin': 12,
             'type': 'pleine_terre'},
            {'nom': 'Melon', 'mois_debut': 3, 'mois_fin': 5, 'mois_recolte_debut': 7, 'mois_recolte_fin': 9,
             'type': 'pleine_terre'},
        ]
    },
]

# ==================== EXÉCUTION ====================

print("\n" + "=" * 60)
print("🌍 REMPLISSAGE DU CALENDRIER MONDIAL DES SEMIS")
print("=" * 60)

crees = 0
ignores = 0

for region_data in DONNEES_MONDIALES:
    region = region_data['region']
    print(f"\n📌 Région : {region.upper()}")
    print("-" * 40)

    for culture in region_data['cultures']:
        existant = CalendrierSemis.objects.filter(
            culture=culture['nom'],
            region=region
        ).first()

        if existant:
            print(f" ℹ️ {culture['nom']} déjà existant")
            ignores += 1
        else:
            CalendrierSemis.objects.create(
                culture=culture['nom'],
                region=region,
                mois_debut_semis=culture['mois_debut'],
                mois_fin_semis=culture['mois_fin'],
                mois_debut_recolte=culture['mois_recolte_debut'],
                mois_fin_recolte=culture['mois_recolte_fin'],
                type_plantation=culture['type'],
                conseils=f"Culture adaptée à la région {region}."
            )
            print(f" ✅ {culture['nom']} ajouté")
            crees += 1

print("\n" + "=" * 60)
print("📊 RÉSUMÉ")
print("=" * 60)
print(f"✅ Entrées créées : {crees}")
print(f"ℹ️ Entrées existantes : {ignores}")
print(f"📊 Total calendrier : {CalendrierSemis.objects.count()}")
print("\n✅ Terminé !")