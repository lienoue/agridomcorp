# inserer_fruits_avec_prix_reels.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegetablesfruits.settings')
django.setup()

from vegetables_fruits.models import Fruit
import json

# ===== LISTE COMPLÈTE DES FRUITS =====
liste_fruits_complete = [
    'abricot', 'airelle', 'alkékenge', 'amande', 'amélanche', 'ananas',
    'arbouse', 'asimine', 'avocat', 'banane', 'bergamote', 'bigarade',
    'bleuet', 'canneberge', 'cantaloup', 'cassis', 'cerise', 'châtaigne',
    'citron', 'clémentine', 'coing', 'cornouiller du canada', 'cynorrhodon',
    'datte', 'épine-vinette', 'feijoa', 'figue', 'figue de barbarie',
    'fraise', 'framboise', 'grenade', 'griotte', 'groseille', 'jujube',
    'kaki', 'kiwaï', 'kiwi', 'lime', 'mandarine', 'marron', 'melon',
    'mûre', 'myrte', 'myrtille', 'nèfle', 'nèfle du japon', 'noisette',
    'noix', 'olive', 'orange', 'pamplemousse', 'pastèque', 'pêche',
    'physalis', 'pistache', 'plaquebière', 'poire', 'pomme', 'pomélos',
    'prunes', 'raisin', 'chicouté', 'pruneaux', 'mirabelle', 'quetsche',
    'reine-claude', 'prune citron', 'coqueret du pérou', 'brugnon',
    'nectarine', 'pavie', 'abricot des antilles', 'bigarade', 'citron vert',
    'combava', 'kumquat', 'orange amère', 'attier', 'cachiman', 'cherimole',
    'corossol', 'cerise des antilles', 'acérola', 'cacao', 'caïmite',
    'camu-camu', 'carambole', 'cerise de cayenne', 'durian', 'fe’i',
    'fruit-à-pain', 'fruit de la passion', 'girembelle', 'goyave', 'icaque',
    'jacque', 'jambose rouge', 'kiwano', 'litchi', 'longane', 'mangoustan',
    'mangue', 'mombin', 'myrobolan', 'noix de cajou', 'noix de coco',
    'noix de muscade', 'pain de singe', 'papaye', 'barbadine', 'grenadelle',
    'grenadille', 'pepino', 'pitaya', 'pomme de cajou', 'pomme de lait',
    'prune de cythère', 'quenette', 'ramboutan', 'salak', 'sapote',
    'sapotille', 'tamarillo', 'tamarin', 'tamarin des indes', 'taxo',
    'yuzu', 'jamalac', 'mamey', 'néflier des indes', 'maracudja',
    'pomme cannelle', 'açaï', 'aronia', 'bigaradier', 'cacahuète',
    'calamondin', 'cédrat', 'chérimole', 'cranberry', 'damassine',
    'fraise des bois', 'fruit du baobab', 'fruit du dragon',
    'groseille à maquereau', 'ichang papeda', 'jaboticaba', 'jamelon',
    'kabosu', 'limette', 'lucuma', 'merise', 'mineola', 'mûroise',
    'nashi', 'noix de macadamia', 'noix de pécan', 'orange sanguine',
    'pignon de pin', 'pomelo', 'pruneau', 'safou', 'salacca', 'sudachi',
    'sureau noir', 'surelle', 'tangelo', 'tangerine', 'tangor', 'tomate',
    'ugli', 'vanille', 'vavangue', 'ximenia', 'zatte'
]

# ===== DONNÉES COMPLÈTES PAR FRUIT =====
FRUITS_COMPLETE_DATA = {
    # === AGRUMES (prix INSEE - indice 2026) [citation:5]===
    'orange': {
        'couleur': 'Orange', 'saison': 'Hiver', 'provenance': 'Espagne/Maroc',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier (agrume)', 'recolte': 'Décembre-mai',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Avril-Mai',
        'jours_levée': 25, 'jours_recolte': 240, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '500x500 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 20, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'citron': {
        'couleur': 'Jaune', 'saison': 'Toute année', 'provenance': 'Espagne/Italie',
        'prix': 2.80, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier (agrume)', 'recolte': 'Toute année',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Avril-Mai',
        'jours_levée': 25, 'jours_recolte': 365, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 20, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'mandarine': {
        'couleur': 'Orange', 'saison': 'Hiver', 'provenance': 'Espagne/Maroc',
        'prix': 2.80, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier (agrume)', 'recolte': 'Novembre-janvier',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Avril-Mai',
        'jours_levée': 25, 'jours_recolte': 240, 'temperature_min': 12,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 15, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'clémentine': {
        'couleur': 'Orange', 'saison': 'Hiver', 'provenance': 'Espagne/Maroc',
        'prix': 2.90, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier (agrume)', 'recolte': 'Novembre-janvier',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Avril-Mai',
        'jours_levée': 25, 'jours_recolte': 240, 'temperature_min': 12,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 15, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile, sans pépins'
    },
    'pamplemousse': {
        'couleur': 'Jaune/Rose', 'saison': 'Hiver', 'provenance': 'USA/Israël',
        'prix': 3.20, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier (agrume)', 'recolte': 'Novembre-mai',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Avril-Mai',
        'jours_levée': 25, 'jours_recolte': 365, 'temperature_min': 10,
        'profondeur_semis': '2 cm', 'espacement': '500x500 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 20, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'kumquat': {
        'couleur': 'Orange', 'saison': 'Hiver', 'provenance': 'Chine/Espagne',
        'prix': 6.00, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier (agrume)', 'recolte': 'Novembre-mars',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Avril-Mai',
        'jours_levée': 30, 'jours_recolte': 180, 'temperature_min': 10,
        'profondeur_semis': '1.5 cm', 'espacement': '300x300 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile, se mange avec la peau'
    },
    'yuzu': {
        'couleur': 'Jaune', 'saison': 'Hiver', 'provenance': 'Japon',
        'prix': 8.00, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier (agrume)', 'recolte': 'Novembre-janvier',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Avril-Mai',
        'jours_levée': 30, 'jours_recolte': 240, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 15, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },

    # === BANANES (prix conjoncture février 2026) [citation:4]===
    'banane': {
        'couleur': 'Jaune', 'saison': 'Toute année', 'provenance': 'Équateur/Costa Rica/Colombie',
        'prix': 1.80, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée géante', 'recolte': '9-12 mois après plantation',
        'semis_interieur': 'Janvier', 'semis_exterieur': 'Mars',
        'jours_levée': 20, 'jours_recolte': 365, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '300x300 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 30, 'periode_floraison': 'Toute année',
        'conseils_pollinisation': 'Pollinisation naturelle par les oiseaux'
    },
    'banane basrai': {
        'couleur': 'Jaune', 'saison': 'Toute année', 'provenance': 'Inde',
        'prix': 1.80, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '9-12 mois',
        'semis_interieur': 'Janvier', 'semis_exterieur': 'Mars',
        'jours_levée': 20, 'jours_recolte': 365, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '300x300 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 30, 'periode_floraison': 'Toute année',
        'conseils_pollinisation': 'Pollinisation naturelle'
    },
    'banane dwarf cavendish': {
        'couleur': 'Jaune', 'saison': 'Toute année', 'provenance': 'Équateur',
        'prix': 1.80, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée naine', 'recolte': '9-12 mois',
        'semis_interieur': 'Janvier', 'semis_exterieur': 'Mars',
        'jours_levée': 20, 'jours_recolte': 365, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '250x250 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 30, 'periode_floraison': 'Toute année',
        'conseils_pollinisation': 'Pollinisation naturelle'
    },
    'banane petite naine': {
        'couleur': 'Jaune', 'saison': 'Toute année', 'provenance': 'Antilles',
        'prix': 2.00, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée naine', 'recolte': '9-12 mois',
        'semis_interieur': 'Janvier', 'semis_exterieur': 'Mars',
        'jours_levée': 20, 'jours_recolte': 365, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '250x250 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 30, 'periode_floraison': 'Toute année',
        'conseils_pollinisation': 'Pollinisation naturelle'
    },

    # === PATATES DOUCES (prix FranceAgriMer 2026) [citation:2]===
    'patate douce': {
        'couleur': 'Orange/Violet', 'saison': 'Toute année', 'provenance': 'France/Espagne/Égypte',
        'prix': 1.95, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Septembre-novembre',
        'semis_interieur': 'Mars-Avril', 'semis_exterieur': 'Mai-Juin',
        'jours_levée': 14, 'jours_recolte': 120, 'temperature_min': 15,
        'profondeur_semis': '2-3 cm', 'espacement': '80x30 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile'
    },

    # === GINGEMBRE (prix FranceAgriMer 2026) [citation:2]===
    'gingembre': {
        'couleur': 'Brun', 'saison': 'Toute année', 'provenance': 'Chine/Brésil',
        'prix': 4.10, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '8-10 mois après plantation',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 21, 'jours_recolte': 240, 'temperature_min': 22,
        'profondeur_semis': '5 cm', 'espacement': '30x30 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Variable',
        'conseils_pollinisation': 'Autofertile'
    },

    # === ANANAS ===
    'ananas': {
        'couleur': 'Jaune', 'saison': 'Toute année', 'provenance': 'Costa Rica/Brésil',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '12-24 mois',
        'semis_interieur': 'Janvier', 'semis_exterieur': 'Mars',
        'jours_levée': 30, 'jours_recolte': 365, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '100x100 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 20, 'periode_floraison': 'Toute année',
        'conseils_pollinisation': 'Pollinisation par les colibris'
    },

    # === AVOCAT ===
    'avocat': {
        'couleur': 'Vert', 'saison': 'Toute année', 'provenance': 'Mexique/Chili',
        'prix': 2.20, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': '6-12 mois après floraison',
        'semis_interieur': 'Janvier', 'semis_exterieur': 'Mars',
        'jours_levée': 30, 'jours_recolte': 365, 'temperature_min': 15,
        'profondeur_semis': '3 cm', 'espacement': '800x800 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 50, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Planter types A et B pour pollinisation'
    },

    # === FRUITS ROUGES ===
    'fraise': {
        'couleur': 'Rouge', 'saison': 'Printemps-Été', 'provenance': 'France/Espagne',
        'prix': 4.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Mai-octobre',
        'semis_interieur': 'Janvier-Février', 'semis_exterieur': 'Mars-Avril',
        'jours_levée': 15, 'jours_recolte': 60, 'temperature_min': 8,
        'profondeur_semis': '0.5 cm', 'espacement': '30x30 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Avril-septembre',
        'conseils_pollinisation': 'Favoriser les abeilles'
    },
    'framboise': {
        'couleur': 'Rouge', 'saison': 'Été', 'provenance': 'France',
        'prix': 5.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbuste', 'recolte': 'Juin-août',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 20, 'jours_recolte': 60, 'temperature_min': 8,
        'profondeur_semis': '0.5 cm', 'espacement': '50x50 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Mai-août',
        'conseils_pollinisation': 'Autofertile'
    },
    'myrtille': {
        'couleur': 'Bleu', 'saison': 'Été', 'provenance': 'France/Amérique du Nord',
        'prix': 6.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbuste', 'recolte': 'Juillet-août',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Mars-Avril',
        'jours_levée': 20, 'jours_recolte': 80, 'temperature_min': 8,
        'profondeur_semis': '0.5 cm', 'espacement': '150x150 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 15, 'periode_floraison': 'Avril-mai',
        'conseils_pollinisation': 'Planter plusieurs variétés'
    },
    'cassis': {
        'couleur': 'Noir', 'saison': 'Été', 'provenance': 'France',
        'prix': 5.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Arbuste', 'recolte': 'Juillet-août',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 20, 'jours_recolte': 70, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '150x150 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Avril-mai',
        'conseils_pollinisation': 'Autofertile'
    },
    'groseille': {
        'couleur': 'Rouge/Blanc', 'saison': 'Été', 'provenance': 'France',
        'prix': 4.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbuste', 'recolte': 'Juillet-août',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 15, 'jours_recolte': 70, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '40x40 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Avril-mai',
        'conseils_pollinisation': 'Autofertile'
    },
    'mûre': {
        'couleur': 'Noire', 'saison': 'Été', 'provenance': 'France',
        'prix': 5.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbuste', 'recolte': 'Août-septembre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril-mai',
        'jours_levée': 20, 'jours_recolte': 60, 'temperature_min': 10,
        'profondeur_semis': '1 cm', 'espacement': '100x50 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 15, 'periode_floraison': 'Mai-août',
        'conseils_pollinisation': 'Autofertile'
    },

    # === FRUITS À NOYAU ===
    'abricot': {
        'couleur': 'Orange', 'saison': 'Été', 'provenance': 'France/Espagne',
        'prix': 3.50, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Juillet-août',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Mars-Avril',
        'jours_levée': 25, 'jours_recolte': 120, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 30, 'periode_floraison': 'Mars',
        'conseils_pollinisation': 'Autofertile'
    },
    'pêche': {
        'couleur': 'Orange/Rose', 'saison': 'Été', 'provenance': 'France/Espagne',
        'prix': 3.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Juillet-août',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Mars-Avril',
        'jours_levée': 20, 'jours_recolte': 120, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 20, 'periode_floraison': 'Mars-Avril',
        'conseils_pollinisation': 'Autofertile'
    },
    'nectarine': {
        'couleur': 'Orange/Rouge', 'saison': 'Été', 'provenance': 'France/Espagne',
        'prix': 3.20, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Juillet-août',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Mars-Avril',
        'jours_levée': 20, 'jours_recolte': 120, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 20, 'periode_floraison': 'Mars-Avril',
        'conseils_pollinisation': 'Autofertile'
    },
    'cerise': {
        'couleur': 'Rouge', 'saison': 'Printemps', 'provenance': 'France',
        'prix': 5.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Mai-juillet',
        'semis_interieur': 'Automne', 'semis_exterieur': 'Novembre',
        'jours_levée': 120, 'jours_recolte': 60, 'temperature_min': 5,
        'profondeur_semis': '3 cm', 'espacement': '500x500 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 30, 'periode_floraison': 'Avril',
        'conseils_pollinisation': 'Nécessite un pollinisateur'
    },
    'prune': {
        'couleur': 'Violet/Rouge/Jaune', 'saison': 'Été', 'provenance': 'France',
        'prix': 3.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Juillet-septembre',
        'semis_interieur': 'Automne', 'semis_exterieur': 'Novembre',
        'jours_levée': 60, 'jours_recolte': 120, 'temperature_min': 5,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'mixte', 'besoin_pollinisateur': True,
        'distance_pollinisation': 40, 'periode_floraison': 'Avril',
        'conseils_pollinisation': 'Certaines variétés autofertiles'
    },
    'mirabelle': {
        'couleur': 'Jaune', 'saison': 'Été', 'provenance': 'France (Lorraine)',
        'prix': 4.50, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Juillet-août',
        'semis_interieur': 'Automne', 'semis_exterieur': 'Novembre',
        'jours_levée': 60, 'jours_recolte': 120, 'temperature_min': 5,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 30, 'periode_floraison': 'Avril',
        'conseils_pollinisation': 'Autofertile'
    },
    'quetsche': {
        'couleur': 'Violet', 'saison': 'Été', 'provenance': 'France',
        'prix': 3.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Août-septembre',
        'semis_interieur': 'Automne', 'semis_exterieur': 'Novembre',
        'jours_levée': 60, 'jours_recolte': 120, 'temperature_min': 5,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 30, 'periode_floraison': 'Avril',
        'conseils_pollinisation': 'Autofertile'
    },
    'reine-claude': {
        'couleur': 'Vert', 'saison': 'Été', 'provenance': 'France',
        'prix': 4.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Août-septembre',
        'semis_interieur': 'Automne', 'semis_exterieur': 'Novembre',
        'jours_levée': 60, 'jours_recolte': 120, 'temperature_min': 5,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 30, 'periode_floraison': 'Avril',
        'conseils_pollinisation': 'Autofertile'
    },
    'brugnon': {
        'couleur': 'Rouge/Violet', 'saison': 'Été', 'provenance': 'France',
        'prix': 3.50, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Juillet-août',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Mars-Avril',
        'jours_levée': 20, 'jours_recolte': 120, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 20, 'periode_floraison': 'Mars-Avril',
        'conseils_pollinisation': 'Autofertile'
    },

    # === FRUITS À PÉPINS ===
    'pomme': {
        'couleur': 'Rouge/Vert/Jaune', 'saison': 'Automne', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Août-octobre',
        'semis_interieur': 'Automne', 'semis_exterieur': 'Novembre',
        'jours_levée': 60, 'jours_recolte': 180, 'temperature_min': 5,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 50, 'periode_floraison': 'Avril-mai',
        'conseils_pollinisation': 'Planter deux variétés différentes'
    },
    'poire': {
        'couleur': 'Jaune/Vert', 'saison': 'Automne', 'provenance': 'France',
        'prix': 3.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Août-septembre',
        'semis_interieur': 'Automne', 'semis_exterieur': 'Novembre',
        'jours_levée': 90, 'jours_recolte': 150, 'temperature_min': 5,
        'profondeur_semis': '2 cm', 'espacement': '500x500 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 40, 'periode_floraison': 'Avril',
        'conseils_pollinisation': 'Nécessite un pollinisateur'
    },
    'coing': {
        'couleur': 'Jaune', 'saison': 'Automne', 'provenance': 'France',
        'prix': 3.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Octobre-novembre',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Mars-Avril',
        'jours_levée': 30, 'jours_recolte': 180, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 20, 'periode_floraison': 'Mai',
        'conseils_pollinisation': 'Autofertile'
    },
    'nashi': {
        'couleur': 'Jaune/Brun', 'saison': 'Automne', 'provenance': 'Japon/France',
        'prix': 5.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Août-octobre',
        'semis_interieur': 'Février-Mars', 'semis_exterieur': 'Mars-Avril',
        'jours_levée': 25, 'jours_recolte': 150, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 30, 'periode_floraison': 'Avril',
        'conseils_pollinisation': 'Nécessite un pollinisateur'
    },

    # === FRUITS EXOTIQUES ===
    'mangue': {
        'couleur': 'Jaune/Orange', 'saison': 'Été', 'provenance': 'Brésil/Pérou',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Mai-septembre',
        'semis_interieur': 'Janvier', 'semis_exterieur': 'Mars',
        'jours_levée': 20, 'jours_recolte': 180, 'temperature_min': 15,
        'profondeur_semis': '3 cm', 'espacement': '800x800 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 30, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Pollinisation par les mouches'
    },
    'papaye': {
        'couleur': 'Orange', 'saison': 'Toute année', 'provenance': 'Brésil',
        'prix': 3.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier tropical', 'recolte': '6-12 mois',
        'semis_interieur': 'Janvier-février', 'semis_exterieur': 'Mars-avril',
        'jours_levée': 15, 'jours_recolte': 180, 'temperature_min': 18,
        'profondeur_semis': '1 cm', 'espacement': '200x200 cm',
        'pollinisation_type': 'mixte', 'besoin_pollinisateur': True,
        'distance_pollinisation': 50, 'periode_floraison': 'Toute année',
        'conseils_pollinisation': 'Nécessite pied mâle et femelle'
    },
    'litchi': {
        'couleur': 'Rose/Blanc', 'saison': 'Été', 'provenance': 'Chine/Madagascar',
        'prix': 8.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Décembre-janvier',
        'semis_interieur': 'Janvier-février', 'semis_exterieur': 'Mars-avril',
        'jours_levée': 30, 'jours_recolte': 120, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '800x800 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 20, 'periode_floraison': 'Février-avril',
        'conseils_pollinisation': 'Nécessite pollinisation croisée'
    },
    'fruit de la passion': {
        'couleur': 'Violet/Jaune', 'saison': 'Toute année', 'provenance': 'Colombie/Équateur',
        'prix': 6.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Liane', 'recolte': '70-80 jours',
        'semis_interieur': 'Février-mars', 'semis_exterieur': 'Avril-mai',
        'jours_levée': 20, 'jours_recolte': 70, 'temperature_min': 15,
        'profondeur_semis': '1 cm', 'espacement': '300x300 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 30, 'periode_floraison': 'Printemps-été',
        'conseils_pollinisation': 'Pollinisation manuelle possible'
    },
    'goyave': {
        'couleur': 'Vert/Jaune', 'saison': 'Été', 'provenance': 'Brésil',
        'prix': 4.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Été-automne',
        'semis_interieur': 'Février-mars', 'semis_exterieur': 'Avril-mai',
        'jours_levée': 20, 'jours_recolte': 150, 'temperature_min': 15,
        'profondeur_semis': '1 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 15, 'periode_floraison': 'Printemps-été',
        'conseils_pollinisation': 'Autofertile'
    },
    'carambole': {
        'couleur': 'Jaune', 'saison': 'Été', 'provenance': 'Asie du Sud-Est',
        'prix': 5.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Été-automne',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars',
        'jours_levée': 20, 'jours_recolte': 120, 'temperature_min': 15,
        'profondeur_semis': '1.5 cm', 'espacement': '600x600 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Plusieurs fois par an',
        'conseils_pollinisation': 'Autofertile'
    },
    'pitaya': {
        'couleur': 'Rose/Blanc', 'saison': 'Été', 'provenance': 'Vietnam/Colombie',
        'prix': 7.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Cactus', 'recolte': 'Été',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars',
        'jours_levée': 15, 'jours_recolte': 180, 'temperature_min': 15,
        'profondeur_semis': '1 cm', 'espacement': '300x300 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 30, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Pollinisation nocturne'
    },
    'kiwi': {
        'couleur': 'Vert', 'saison': 'Automne', 'provenance': 'France/Nouvelle-Zélande',
        'prix': 3.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Liane', 'recolte': 'Octobre-novembre',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars',
        'jours_levée': 25, 'jours_recolte': 180, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 20, 'periode_floraison': 'Mai-juin',
        'conseils_pollinisation': 'Nécessite pied mâle et femelle'
    },

    # === FRUITS SECS ===
    'noix': {
        'couleur': 'Beige', 'saison': 'Automne', 'provenance': 'France',
        'prix': 8.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Automne', 'semis_exterieur': 'Novembre',
        'jours_levée': 150, 'jours_recolte': 150, 'temperature_min': 5,
        'profondeur_semis': '5 cm', 'espacement': '1000x1000 cm',
        'pollinisation_type': 'vent', 'besoin_pollinisateur': True,
        'distance_pollinisation': 100, 'periode_floraison': 'Avril-mai',
        'conseils_pollinisation': 'Pollinisation par le vent'
    },
    'noisette': {
        'couleur': 'Beige', 'saison': 'Automne', 'provenance': 'France',
        'prix': 7.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Arbuste', 'recolte': 'Août-septembre',
        'semis_interieur': 'Novembre', 'semis_exterieur': 'Novembre-décembre',
        'jours_levée': 180, 'jours_recolte': 365, 'temperature_min': 5,
        'profondeur_semis': '5 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'vent', 'besoin_pollinisateur': True,
        'distance_pollinisation': 100, 'periode_floraison': 'Février-mars',
        'conseils_pollinisation': 'Planter plusieurs variétés'
    },
    'amande': {
        'couleur': 'Beige', 'saison': 'Été', 'provenance': 'Espagne/Californie',
        'prix': 12.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Août-septembre',
        'semis_interieur': 'Automne', 'semis_exterieur': 'Novembre',
        'jours_levée': 120, 'jours_recolte': 210, 'temperature_min': 8,
        'profondeur_semis': '4 cm', 'espacement': '600x600 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 50, 'periode_floraison': 'Février-mars',
        'conseils_pollinisation': 'Nécessite pollinisation croisée'
    },
    'châtaigne': {
        'couleur': 'Marron', 'saison': 'Automne', 'provenance': 'France',
        'prix': 6.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Octobre-novembre',
        'semis_interieur': 'Automne', 'semis_exterieur': 'Novembre',
        'jours_levée': 180, 'jours_recolte': 150, 'temperature_min': 5,
        'profondeur_semis': '4 cm', 'espacement': '1000x1000 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 100, 'periode_floraison': 'Juin-juillet',
        'conseils_pollinisation': 'Planter plusieurs arbres'
    },
    'pistache': {
        'couleur': 'Vert/Rouge', 'saison': 'Automne', 'provenance': 'Iran/USA',
        'prix': 15.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Janvier', 'semis_exterieur': 'Mars',
        'jours_levée': 30, 'jours_recolte': 210, 'temperature_min': 10,
        'profondeur_semis': '3 cm', 'espacement': '600x600 cm',
        'pollinisation_type': 'vent', 'besoin_pollinisateur': True,
        'distance_pollinisation': 50, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Arbre dioïque'
    },

    # === MÉLONS ===
    'melon': {
        'couleur': 'Vert/Jaune', 'saison': 'Été', 'provenance': 'France/Espagne',
        'prix': 2.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Plante rampante', 'recolte': 'Juillet-septembre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 8, 'jours_recolte': 85, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '100x100 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 50, 'periode_floraison': 'Juin-juillet',
        'conseils_pollinisation': 'Fleurs mâles et femelles'
    },
    'pastèque': {
        'couleur': 'Vert/Rouge', 'saison': 'Été', 'provenance': 'France/Espagne',
        'prix': 1.80, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante rampante', 'recolte': 'Juillet-septembre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 10, 'jours_recolte': 85, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '150x150 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 50, 'periode_floraison': 'Juin-juillet',
        'conseils_pollinisation': 'Nécessite des abeilles'
    },
    'cantaloup': {
        'couleur': 'Orange', 'saison': 'Été', 'provenance': 'France',
        'prix': 2.20, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Plante rampante', 'recolte': 'Août-septembre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 8, 'jours_recolte': 80, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '100x100 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 50, 'periode_floraison': 'Juin-juillet',
        'conseils_pollinisation': 'Fleurs mâles et femelles'
    },

    # === FRUITS MÉDITERRANÉENS ===
    'figue': {
        'couleur': 'Violet/Vert', 'saison': 'Été', 'provenance': 'France',
        'prix': 4.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Août-septembre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 15, 'jours_recolte': 120, 'temperature_min': 10,
        'profondeur_semis': '1 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 20, 'periode_floraison': 'Printemps-été',
        'conseils_pollinisation': 'Variétés communes sans pollinisation'
    },
    'grenade': {
        'couleur': 'Rouge', 'saison': 'Automne', 'provenance': 'Espagne',
        'prix': 4.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbuste', 'recolte': 'Septembre-novembre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 20, 'jours_recolte': 180, 'temperature_min': 10,
        'profondeur_semis': '1.5 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 15, 'periode_floraison': 'Mai-juin',
        'conseils_pollinisation': 'Autofertile'
    },
    'datte': {
        'couleur': 'Marron', 'saison': 'Automne', 'provenance': 'Tunisie/Algérie',
        'prix': 6.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Palmier', 'recolte': 'Septembre-décembre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 30, 'jours_recolte': 240, 'temperature_min': 15,
        'profondeur_semis': '3 cm', 'espacement': '800x800 cm',
        'pollinisation_type': 'vent', 'besoin_pollinisateur': True,
        'distance_pollinisation': 100, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Pollinisation manuelle souvent pratiquée'
    },
    'olive': {
        'couleur': 'Vert/Noir', 'saison': 'Automne', 'provenance': 'France/Espagne',
        'prix': 4.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Septembre-novembre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 30, 'jours_recolte': 210, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '800x800 cm',
        'pollinisation_type': 'vent', 'besoin_pollinisateur': True,
        'distance_pollinisation': 100, 'periode_floraison': 'Mai-juin',
        'conseils_pollinisation': 'Planter plusieurs variétés'
    },
    'kaki': {
        'couleur': 'Orange', 'saison': 'Automne', 'provenance': 'Espagne',
        'prix': 4.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbre fruitier', 'recolte': 'Octobre-novembre',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars-avril',
        'jours_levée': 30, 'jours_recolte': 210, 'temperature_min': 10,
        'profondeur_semis': '2 cm', 'espacement': '500x500 cm',
        'pollinisation_type': 'mixte', 'besoin_pollinisateur': False,
        'distance_pollinisation': 30, 'periode_floraison': 'Mai-juin',
        'conseils_pollinisation': 'Parthénocarpique possible'
    },
    'jujube': {
        'couleur': 'Rouge-brun', 'saison': 'Automne', 'provenance': 'Chine',
        'prix': 6.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Arbuste', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 20, 'jours_recolte': 150, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '400x400 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 15, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile'
    },
    'figue de barbarie': {
        'couleur': 'Orange/Rouge', 'saison': 'Été', 'provenance': 'Mexique/Italie',
        'prix': 5.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Cactus', 'recolte': 'Août-octobre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 20, 'jours_recolte': 150, 'temperature_min': 10,
        'profondeur_semis': '1 cm', 'espacement': '300x300 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 20, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
}

# Valeurs par défaut pour les fruits non répertoriés
DEFAULT_VALUES = {
    'couleur': 'Variable',
    'provenance': 'Variable',
    'saison': 'Variable',
    'prix': 0,
    'bourse': False,
    'AOP': False,
    'IGP': False,
    'url': '',
    'plantation': 'Variable',
    'recolte': 'Variable',
    'semis_interieur': 'Février-Mars',
    'semis_exterieur': 'Avril-Mai',
    'jours_levée': 20,
    'jours_recolte': 120,
    'temperature_min': 15,
    'profondeur_semis': '1-2 cm',
    'espacement': 'Variable',
    'pollinisation_type': 'auto',
    'besoin_pollinisateur': False,
    'pollinisateurs_conseilles': '',
    'distance_pollinisation': 10,
    'periode_floraison': 'Printemps-Été',
    'conseils_pollinisation': 'Information à compléter'
}


def get_fruit_data(nom):
    """Retourne les données du fruit si disponible, sinon les valeurs par défaut"""
    nom_clean = nom.lower().strip()

    # Correspondance exacte
    if nom_clean in FRUITS_COMPLETE_DATA:
        return FRUITS_COMPLETE_DATA[nom_clean]

    # Correspondance partielle
    for key in FRUITS_COMPLETE_DATA:
        if key in nom_clean or nom_clean in key:
            print(f" → Correspondance trouvée: {key} pour {nom}")
            return FRUITS_COMPLETE_DATA[key]

    return DEFAULT_VALUES.copy()


def inserer_tous_les_fruits():
    """Insère tous les fruits avec leurs données réelles"""

    print("=== INSERTION DES FRUITS AVEC PRIX RÉELS ===\n")
    print(f"Nombre total de fruits à traiter : {len(liste_fruits_complete)}")

    compteur_nouveaux = 0
    compteur_existants = 0
    compteur_erreurs = 0

    for nom in liste_fruits_complete:
        nom_clean = nom.strip()

        # Vérifier si le fruit existe déjà
        if Fruit.objects.filter(nom__iexact=nom_clean).exists():
            print(f"⏭️ Déjà présent: {nom_clean}")
            compteur_existants += 1
            continue

        # Récupérer les données
        data = get_fruit_data(nom_clean)

        try:
            nouveau_fruit = Fruit(
                nom=nom_clean,
                couleur=data.get('couleur', 'Variable'),
                provenance=data.get('provenance', 'Variable'),
                saison=data.get('saison', 'Variable'),
                prix=data.get('prix', 0),
                bourse=data.get('bourse', False),
                AOP=data.get('AOP', False),
                IGP=data.get('IGP', False),
                url=data.get('url', ''),
                plantation=data.get('plantation', 'Variable'),
                recolte=data.get('recolte', 'Variable'),
                semis_interieur=data.get('semis_interieur', 'Février-Mars'),
                semis_exterieur=data.get('semis_exterieur', 'Avril-Mai'),
                jours_levée=data.get('jours_levée', 20),
                jours_recolte=data.get('jours_recolte', 120),
                temperature_min=data.get('temperature_min', 15),
                profondeur_semis=data.get('profondeur_semis', '1-2 cm'),
                espacement=data.get('espacement', 'Variable'),
                pollinisation_type=data.get('pollinisation_type', 'auto'),
                besoin_pollinisateur=data.get('besoin_pollinisateur', False),
                pollinisateurs_conseilles=data.get('pollinisateurs_conseilles', ''),
                distance_pollinisation=data.get('distance_pollinisation', 10),
                periode_floraison=data.get('periode_floraison', 'Printemps-Été'),
                conseils_pollinisation=data.get('conseils_pollinisation', 'Information à compléter')
            )
            nouveau_fruit.save()
            print(f"✅ Ajouté: {nom_clean} - {data.get('prix', 0)}€ - {data.get('plantation', 'Type inconnu')}")
            compteur_nouveaux += 1


        except Exception as e:
            print(f"❌ Erreur pour {nom_clean}: {e}")
            compteur_erreurs += 1

    print(f"\n=== RÉSUMÉ FINAL ===")
    print(f"📊 Statistiques:")
    print(f" - Nouveaux fruits ajoutés : {compteur_nouveaux}")
    print(f" - Fruits déjà existants : {compteur_existants}")
    print(f" - Erreurs : {compteur_erreurs}")
    print(f" - Total traité : {len(liste_fruits_complete)}")

    # Vérification finale
    total_apres = Fruit.objects.count()
    print(f"\n📦 Base de données après insertion : {total_apres} fruits")


if __name__ == '__main__':
    inserer_tous_les_fruits()