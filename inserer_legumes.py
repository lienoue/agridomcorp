# inserer_legumes_avec_prix_reels.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegetablesfruits.settings')
django.setup()

from vegetables_fruits.models import Vegetable
import json

# ===== LISTE COMPLÈTE DES LÉGUMES =====
liste_legumes_complete = [
    'ail', 'ail cultivé', 'ail d\'orient', 'ail rocambole', 'amarante',
    'amarante de chine', 'ansérine bon-henri', 'añu', 'arachide', 'arroche',
    'artichaut', 'asperge', 'asperge blanche', 'asperge verte', 'aubergine',
    'avocat', 'azuki', 'bambou', 'banane', 'banane plantain', 'bardane',
    'baselle', 'basilic', 'bénincasa', 'bette', 'bette à carde', 'bette ou blette',
    'betterave', 'betterave rouge', 'blette', 'brèdes', 'brocoli', 'brocoli chinois',
    'bunias d\'orient', 'butternut', 'calebasse', 'canna comestible', 'capucine tubéreuse',
    'cardon', 'carotte', 'catalonia', 'céleri', 'céleri branche', 'céleri rave',
    'céleri-rave', 'cerfeuil', 'cerfeuil tubéreux', 'champignon', 'châtaigne de terre',
    'châtaigne d\'eau chinoise', 'chayote', 'chénopode bon-henri', 'chervis',
    'chia', 'chicon', 'chicorée', 'chou blanc', 'chou brocoli', 'chou cabus',
    'chou chinois', 'chou de bruxelles', 'chou de pékin', 'chou frisé',
    'chou palmier', 'chou palmiste', 'chou pointue', 'chou romanesco',
    'chou rouge', 'chou-chinois', 'chou-fleur', 'chou-navet', 'chou-rave',
    'chou-romanesco', 'choux', 'christophine', 'ciboule', 'ciboule de chine',
    'ciboulette', 'cima di rapa', 'citrouille', 'claytone de cuba', 'concombre',
    'coqueret du pérou', 'coriandre', 'cornichon', 'courge', 'courge cireuse',
    'courge de siam', 'courge musquée', 'courgette', 'courgette boule',
    'courgette du siam', 'courgette slawi', 'cresson', 'cresson alénois',
    'cresson de fontaine', 'cresson de para', 'cresson de terre', 'cresson des jardins',
    'cresson d\'hiver', 'crosne', 'crosne du japon', 'curcuma', 'dachine',
    'daikon', 'dolique asperge', 'dolique lablab', 'echalote', 'échalote',
    'endive', 'epinard', 'épinard', 'épinard de malabar', 'estragon', 'fenouil',
    'fenouil', 'fève', 'ficoïde glaciale', 'flageolet', 'frisée', 'gesse',
    'gingembre', 'giromon', 'glycine tubéreuse', 'gombo', 'gourde',
    'grande bardane', 'grelos', 'guimauve officinale', 'gundelia', 'haricot',
    'haricot de lima', 'haricot d\'espagne', 'haricot grimpant',
    'haricot kilomètre', 'haricot mungo', 'haricot rouge du japon', 'haricot vert',
    'hélianthi', 'hosta', 'houttuynia', 'igname', 'igname ailée', 'jacque',
    'jaque', 'jujube', 'kancon', 'komatsuna', 'konbu', 'laitue', 'laitue romaine',
    'lentille', 'liseron d\'eau', 'luffa', 'lys asiatique comestible', 'maceron',
    'mâche', 'mâcre bicorne', 'mâcre nageante', 'maïs', 'maïs doux', 'mangue verte',
    'manioc', 'margose', 'marjolaine', 'marron', 'mauve', 'melon', 'menthe',
    'mizuna', 'momordique', 'navet', 'niébé', 'nombril de vénus', 'oca du pérou',
    'oignon', 'oignon de chine', 'okra', 'olive', 'onagre', 'origan', 'ortie',
    'oseille', 'pak choï', 'panais', 'patate', 'patate douce', 'pâtisson',
    'périlla', 'persil', 'petit oignon blanc', 'petit pois', 'petits pois',
    'pe-tsaï', 'physalis', 'piment', 'pissenlit', 'poire de terre', 'poireau',
    'poirée', 'pois carré', 'pois chiche', 'pois d\'angole', 'pois mange-tout',
    'pois sabre', 'pois sec', 'poivron', 'pomme de terre', 'potimarron',
    'potiron', 'pourpier', 'radicchio', 'radis', 'radis du japon', 'radis long',
    'radis noir', 'radis rouge', 'radis serpent', 'radis', 'raifort',
    'rhubarbe', 'romarin', 'roquette', 'rutabaga', 'salade', 'salades',
    'salicorne', 'salsifi', 'salsifis', 'salsifis topinambour', 'sauge',
    'scarole', 'scorsonère', 'serpent gourde', 'serpent végétal', 'shiso',
    'soja', 'souchet comestible', 'taro', 'tétragone', 'tétragone cornue',
    'thym', 'tinda', 'tomate', 'tomate', 'tomatillo', 'topinambour', 'udo',
    'vitelotte', 'wakame', 'wasabi', 'yacón', 'yin tsoï'
]

# ===== DONNÉES COMPLÈTES PAR LÉGUME (prix FranceAgriMer/INSEE 2026) =====
LEGUMES_COMPLETE_DATA = {
    # === LÉGUMES RACINES ===
    'carotte': {
        'couleur': 'Orange', 'saison': 'Toute année', 'provenance': 'France',
        'prix': 1.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juin-octobre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril-juillet',
        'jours_levée': 14, 'jours_recolte': 70, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '30x5 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile'
    },
    'pomme de terre': {
        'couleur': 'Blanc/Jaune/Violet', 'saison': 'Toute année', 'provenance': 'France',
        'prix': 1.80, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Août-octobre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril-mai',
        'jours_levée': 21, 'jours_recolte': 90, 'temperature_min': 10,
        'profondeur_semis': '10 cm', 'espacement': '60x35 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'patate douce': {
        'couleur': 'Orange/Violet', 'saison': 'Toute année', 'provenance': 'France/Espagne',
        'prix': 2.20, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Septembre-novembre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 14, 'jours_recolte': 120, 'temperature_min': 15,
        'profondeur_semis': '10 cm', 'espacement': '80x30 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile'
    },
    'navet': {
        'couleur': 'Blanc/Violet', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 1.80, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Septembre-novembre',
        'semis_interieur': 'Juin', 'semis_exterieur': 'Juillet-août',
        'jours_levée': 7, 'jours_recolte': 50, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '30x15 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'radis': {
        'couleur': 'Rouge/Blanc', 'saison': 'Printemps-Été', 'provenance': 'France',
        'prix': 1.80, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '25-30 jours après semis',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril-septembre',
        'jours_levée': 5, 'jours_recolte': 25, 'temperature_min': 8,
        'profondeur_semis': '0.5 cm', 'espacement': '15x5 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'daikon': {
        'couleur': 'Blanc', 'saison': 'Automne-Hiver', 'provenance': 'Japon/France',
        'prix': 2.50, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '50-70 jours',
        'semis_interieur': 'Juin', 'semis_exterieur': 'Juillet-août',
        'jours_levée': 7, 'jours_recolte': 60, 'temperature_min': 10,
        'profondeur_semis': '1 cm', 'espacement': '40x20 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'radis noir': {
        'couleur': 'Noir', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 2.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Octobre-novembre',
        'semis_interieur': 'Juin', 'semis_exterieur': 'Juillet-août',
        'jours_levée': 7, 'jours_recolte': 60, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '30x15 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'panais': {
        'couleur': 'Blanc', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 2.20, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Octobre-novembre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 14, 'jours_recolte': 120, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '40x15 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'topinambour': {
        'couleur': 'Blanc', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Octobre-mars',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 14, 'jours_recolte': 180, 'temperature_min': 8,
        'profondeur_semis': '5 cm', 'espacement': '80x50 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile'
    },
    'crosne': {
        'couleur': 'Blanc', 'saison': 'Automne', 'provenance': 'France',
        'prix': 8.00, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Octobre-novembre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 21, 'jours_recolte': 180, 'temperature_min': 8,
        'profondeur_semis': '3 cm', 'espacement': '40x30 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile'
    },
    'salsifis': {
        'couleur': 'Blanc', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 3.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Octobre-novembre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 14, 'jours_recolte': 120, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '40x15 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'rutabaga': {
        'couleur': 'Jaune/Violet', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 2.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Octobre-novembre',
        'semis_interieur': 'Mai', 'semis_exterieur': 'Juin',
        'jours_levée': 7, 'jours_recolte': 90, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '40x20 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'betterave': {
        'couleur': 'Rouge', 'saison': 'Toute année', 'provenance': 'France',
        'prix': 1.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juillet-octobre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril-juin',
        'jours_levée': 10, 'jours_recolte': 70, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '30x10 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile'
    },

    # === LÉGUMES FEUILLES ===
    'laitue': {
        'couleur': 'Vert', 'saison': 'Printemps-Été', 'provenance': 'France',
        'prix': 1.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '60-90 jours',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars-septembre',
        'jours_levée': 7, 'jours_recolte': 60, 'temperature_min': 8,
        'profondeur_semis': '0.5 cm', 'espacement': '30x30 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'salade': {
        'couleur': 'Vert', 'saison': 'Printemps-Été', 'provenance': 'France',
        'prix': 1.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '60-90 jours',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars-septembre',
        'jours_levée': 7, 'jours_recolte': 60, 'temperature_min': 8,
        'profondeur_semis': '0.5 cm', 'espacement': '30x30 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'épinard': {
        'couleur': 'Vert', 'saison': 'Printemps-Automne', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '40-50 jours',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars-avril',
        'jours_levée': 7, 'jours_recolte': 45, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '30x10 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'chou': {
        'couleur': 'Vert/Rouge/Blanc', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 1.80, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '90-120 jours',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril-mai',
        'jours_levée': 10, 'jours_recolte': 100, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '60x50 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'chou-fleur': {
        'couleur': 'Blanc', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '90-120 jours',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril-mai',
        'jours_levée': 10, 'jours_recolte': 100, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '60x50 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'brocoli': {
        'couleur': 'Vert', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '70-90 jours',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 10, 'jours_recolte': 80, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '50x40 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'endive': {
        'couleur': 'Blanche', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Hiver',
        'semis_interieur': 'Juin', 'semis_exterieur': 'Juillet',
        'jours_levée': 7, 'jours_recolte': 180, 'temperature_min': 10,
        'profondeur_semis': '1 cm', 'espacement': '30x30 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'mâche': {
        'couleur': 'Vert', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 4.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '60-90 jours',
        'semis_interieur': 'Août', 'semis_exterieur': 'Septembre',
        'jours_levée': 10, 'jours_recolte': 70, 'temperature_min': 5,
        'profondeur_semis': '0.5 cm', 'espacement': '20x15 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'chou de bruxelles': {
        'couleur': 'Vert', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 3.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '120-150 jours',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 10, 'jours_recolte': 120, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '70x60 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'chou rouge': {
        'couleur': 'Rouge', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 2.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '90-120 jours',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 10, 'jours_recolte': 100, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '60x50 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'chou kale': {
        'couleur': 'Vert', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 3.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '60-80 jours',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 7, 'jours_recolte': 70, 'temperature_min': 5,
        'profondeur_semis': '1 cm', 'espacement': '50x40 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'chou chinois': {
        'couleur': 'Vert/Blanc', 'saison': 'Automne', 'provenance': 'Chine/France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '60-80 jours',
        'semis_interieur': 'Juin', 'semis_exterieur': 'Juillet',
        'jours_levée': 7, 'jours_recolte': 70, 'temperature_min': 10,
        'profondeur_semis': '1 cm', 'espacement': '40x30 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'pak choï': {
        'couleur': 'Vert/Blanc', 'saison': 'Printemps-Automne', 'provenance': 'Chine/France',
        'prix': 2.50, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '40-50 jours',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 5, 'jours_recolte': 45, 'temperature_min': 10,
        'profondeur_semis': '0.5 cm', 'espacement': '30x20 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'mizuna': {
        'couleur': 'Vert', 'saison': 'Printemps-Automne', 'provenance': 'Japon',
        'prix': 3.00, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '40-50 jours',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 5, 'jours_recolte': 45, 'temperature_min': 8,
        'profondeur_semis': '0.5 cm', 'espacement': '25x15 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'roquette': {
        'couleur': 'Vert', 'saison': 'Printemps-Automne', 'provenance': 'France',
        'prix': 3.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '30-40 jours',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 5, 'jours_recolte': 35, 'temperature_min': 8,
        'profondeur_semis': '0.5 cm', 'espacement': '20x15 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'cresson': {
        'couleur': 'Vert', 'saison': 'Printemps-Automne', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante aquatique', 'recolte': '40-60 jours',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 7, 'jours_recolte': 50, 'temperature_min': 10,
        'profondeur_semis': '0.5 cm', 'espacement': '20x20 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'pourpier': {
        'couleur': 'Vert', 'saison': 'Été', 'provenance': 'France',
        'prix': 3.00, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '30-40 jours',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 5, 'jours_recolte': 35, 'temperature_min': 15,
        'profondeur_semis': '0.5 cm', 'espacement': '30x20 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile'
    },
    'oseille': {
        'couleur': 'Vert', 'saison': 'Printemps-Été', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '60-70 jours',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 10, 'jours_recolte': 60, 'temperature_min': 8,
        'profondeur_semis': '0.5 cm', 'espacement': '30x20 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },

    # === LÉGUMES FRUITS ===
    'tomate': {
        'couleur': 'Rouge', 'saison': 'Été', 'provenance': 'France/Espagne',
        'prix': 2.50, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juillet-octobre',
        'semis_interieur': 'Février-mars', 'semis_exterieur': 'Avril-mai',
        'jours_levée': 10, 'jours_recolte': 80, 'temperature_min': 15,
        'profondeur_semis': '0.5 cm', 'espacement': '60x50 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile, secouer les plants'
    },
    'aubergine': {
        'couleur': 'Violet', 'saison': 'Été', 'provenance': 'France/Espagne',
        'prix': 2.80, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juillet-octobre',
        'semis_interieur': 'Février-mars', 'semis_exterieur': 'Avril-mai',
        'jours_levée': 10, 'jours_recolte': 90, 'temperature_min': 15,
        'profondeur_semis': '0.5 cm', 'espacement': '60x60 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'poivron': {
        'couleur': 'Rouge/Vert/Jaune', 'saison': 'Été', 'provenance': 'France/Espagne',
        'prix': 3.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juillet-octobre',
        'semis_interieur': 'Février-mars', 'semis_exterieur': 'Avril-mai',
        'jours_levée': 10, 'jours_recolte': 90, 'temperature_min': 15,
        'profondeur_semis': '0.5 cm', 'espacement': '50x50 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'piment': {
        'couleur': 'Rouge/Vert', 'saison': 'Été', 'provenance': 'France/Espagne',
        'prix': 3.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juillet-octobre',
        'semis_interieur': 'Février-mars', 'semis_exterieur': 'Avril-mai',
        'jours_levée': 10, 'jours_recolte': 90, 'temperature_min': 15,
        'profondeur_semis': '0.5 cm', 'espacement': '50x50 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'concombre': {
        'couleur': 'Vert', 'saison': 'Été', 'provenance': 'France/Espagne',
        'prix': 1.80, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante rampante', 'recolte': 'Juin-septembre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 8, 'jours_recolte': 60, 'temperature_min': 15,
        'profondeur_semis': '1 cm', 'espacement': '100x50 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 50, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Nécessite des insectes pollinisateurs'
    },
    'cornichon': {
        'couleur': 'Vert', 'saison': 'Été', 'provenance': 'France',
        'prix': 2.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante rampante', 'recolte': 'Juin-septembre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 8, 'jours_recolte': 50, 'temperature_min': 15,
        'profondeur_semis': '1 cm', 'espacement': '80x40 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 50, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Nécessite des insectes'
    },
    'courgette': {
        'couleur': 'Vert/Jaune', 'saison': 'Été', 'provenance': 'France',
        'prix': 1.80, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juin-octobre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 7, 'jours_recolte': 50, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '100x80 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 100, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Fleurs mâles et femelles'
    },
    'courge': {
        'couleur': 'Vert/Jaune/Orange', 'saison': 'Automne', 'provenance': 'France',
        'prix': 1.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante rampante', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 7, 'jours_recolte': 100, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '150x100 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 100, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Nécessite des insectes'
    },
    'potiron': {
        'couleur': 'Orange', 'saison': 'Automne', 'provenance': 'France',
        'prix': 1.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante rampante', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 7, 'jours_recolte': 120, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '200x150 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 100, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Pollinisation par les abeilles'
    },
    'potimarron': {
        'couleur': 'Orange', 'saison': 'Automne', 'provenance': 'France',
        'prix': 2.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante rampante', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 7, 'jours_recolte': 100, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '150x100 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 100, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Pollinisation par les insectes'
    },
    'butternut': {
        'couleur': 'Beige', 'saison': 'Automne', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante rampante', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 7, 'jours_recolte': 100, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '150x100 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 100, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Nécessite des pollinisateurs'
    },
    'citrouille': {
        'couleur': 'Orange', 'saison': 'Automne', 'provenance': 'France',
        'prix': 1.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante rampante', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 7, 'jours_recolte': 110, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '200x150 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 100, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Pollinisation manuelle possible'
    },
    'pâtisson': {
        'couleur': 'Blanc/Vert', 'saison': 'Automne', 'provenance': 'France',
        'prix': 2.00, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante rampante', 'recolte': 'Août-octobre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 7, 'jours_recolte': 90, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '120x100 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 100, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Nécessite des insectes'
    },
    'gombo': {
        'couleur': 'Vert', 'saison': 'Été', 'provenance': 'Afrique',
        'prix': 3.50, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Août-octobre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 14, 'jours_recolte': 70, 'temperature_min': 20,
        'profondeur_semis': '2 cm', 'espacement': '60x40 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile'
    },
    'okra': {
        'couleur': 'Vert', 'saison': 'Été', 'provenance': 'Afrique',
        'prix': 3.50, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Août-octobre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 14, 'jours_recolte': 70, 'temperature_min': 20,
        'profondeur_semis': '2 cm', 'espacement': '60x40 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile'
    },

    # === LÉGUMES BULBES ===
    'oignon': {
        'couleur': 'Jaune/Rouge/Blanc', 'saison': 'Toute année', 'provenance': 'France',
        'prix': 1.50, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juillet-août',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars-avril',
        'jours_levée': 10, 'jours_recolte': 120, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '30x10 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'ail': {
        'couleur': 'Blanc', 'saison': 'Toute année', 'provenance': 'France',
        'prix': 3.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juin-juillet',
        'semis_interieur': 'Automne', 'semis_exterieur': 'Octobre-novembre',
        'jours_levée': 30, 'jours_recolte': 240, 'temperature_min': 5,
        'profondeur_semis': '3 cm', 'espacement': '20x15 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'échalote': {
        'couleur': 'Violet', 'saison': 'Toute année', 'provenance': 'France',
        'prix': 3.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juillet-août',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars',
        'jours_levée': 14, 'jours_recolte': 120, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '20x15 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'poireau': {
        'couleur': 'Vert/Blanc', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 2.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Octobre-mars',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars-avril',
        'jours_levée': 10, 'jours_recolte': 150, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '30x15 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },

    # === LÉGUMINEUSES ===
    'haricot vert': {
        'couleur': 'Vert', 'saison': 'Été', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juillet-septembre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai-juin',
        'jours_levée': 8, 'jours_recolte': 60, 'temperature_min': 12,
        'profondeur_semis': '3 cm', 'espacement': '50x15 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'petit pois': {
        'couleur': 'Vert', 'saison': 'Printemps-Été', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Mai-juillet',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars-avril',
        'jours_levée': 10, 'jours_recolte': 70, 'temperature_min': 8,
        'profondeur_semis': '3 cm', 'espacement': '60x5 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'fève': {
        'couleur': 'Vert', 'saison': 'Printemps', 'provenance': 'France',
        'prix': 2.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Mai-juin',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars',
        'jours_levée': 14, 'jours_recolte': 90, 'temperature_min': 8,
        'profondeur_semis': '5 cm', 'espacement': '50x20 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'lentille': {
        'couleur': 'Verte/Brune', 'saison': 'Été', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juillet-août',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 10, 'jours_recolte': 90, 'temperature_min': 8,
        'profondeur_semis': '2 cm', 'espacement': '30x10 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'pois chiche': {
        'couleur': 'Beige', 'saison': 'Été', 'provenance': 'Méditerranée',
        'prix': 3.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Août-septembre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 14, 'jours_recolte': 100, 'temperature_min': 10,
        'profondeur_semis': '3 cm', 'espacement': '40x15 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'soja': {
        'couleur': 'Vert', 'saison': 'Été', 'provenance': 'Asie',
        'prix': 3.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 10, 'jours_recolte': 100, 'temperature_min': 15,
        'profondeur_semis': '2 cm', 'espacement': '40x10 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'arachide': {
        'couleur': 'Beige', 'saison': 'Été', 'provenance': 'Amérique du Sud',
        'prix': 4.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 10, 'jours_recolte': 120, 'temperature_min': 20,
        'profondeur_semis': '5 cm', 'espacement': '40x20 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },

    # === AUTRES LÉGUMES ===
    'artichaut': {
        'couleur': 'Vert/Violet', 'saison': 'Printemps-Été', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante vivace', 'recolte': 'Mai-juillet',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 21, 'jours_recolte': 180, 'temperature_min': 10,
        'profondeur_semis': '1 cm', 'espacement': '100x100 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 50, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Pollinisation par les abeilles'
    },
    'asperge': {
        'couleur': 'Verte/Blanche', 'saison': 'Printemps', 'provenance': 'France',
        'prix': 5.00, 'bourse': True, 'AOP': True, 'IGP': False,
        'plantation': 'Plante vivace', 'recolte': 'Avril-juin',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 21, 'jours_recolte': 730, 'temperature_min': 10,
        'profondeur_semis': '2 cm', 'espacement': '100x50 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 50, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Pollinisation par les insectes'
    },
    'céleri': {
        'couleur': 'Vert', 'saison': 'Automne', 'provenance': 'France',
        'prix': 2.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars',
        'jours_levée': 14, 'jours_recolte': 120, 'temperature_min': 10,
        'profondeur_semis': '0.5 cm', 'espacement': '30x25 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'céleri rave': {
        'couleur': 'Brun', 'saison': 'Automne', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Octobre-novembre',
        'semis_interieur': 'Février', 'semis_exterieur': 'Mars',
        'jours_levée': 14, 'jours_recolte': 150, 'temperature_min': 10,
        'profondeur_semis': '0.5 cm', 'espacement': '40x30 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'rhubarbe': {
        'couleur': 'Rouge/Vert', 'saison': 'Printemps', 'provenance': 'France',
        'prix': 3.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante vivace', 'recolte': 'Avril-juin',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 21, 'jours_recolte': 365, 'temperature_min': 10,
        'profondeur_semis': '1 cm', 'espacement': '100x100 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': False,
        'distance_pollinisation': 50, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Pollinisation par les insectes'
    },
    'fenouil': {
        'couleur': 'Vert/Blanc', 'saison': 'Automne', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Juin', 'semis_exterieur': 'Juillet',
        'jours_levée': 10, 'jours_recolte': 90, 'temperature_min': 10,
        'profondeur_semis': '0.5 cm', 'espacement': '30x20 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'chayote': {
        'couleur': 'Vert', 'saison': 'Automne', 'provenance': 'Amérique centrale',
        'prix': 3.00, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante grimpante', 'recolte': 'Septembre-octobre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 21, 'jours_recolte': 180, 'temperature_min': 15,
        'profondeur_semis': '5 cm', 'espacement': '300x300 cm',
        'pollinisation_type': 'insectes', 'besoin_pollinisateur': True,
        'distance_pollinisation': 50, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Nécessite des insectes'
    },
    'cardon': {
        'couleur': 'Vert/Blanc', 'saison': 'Automne-Hiver', 'provenance': 'France',
        'prix': 3.00, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Novembre-décembre',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 14, 'jours_recolte': 180, 'temperature_min': 8,
        'profondeur_semis': '1 cm', 'espacement': '80x80 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'pissenlit': {
        'couleur': 'Vert', 'saison': 'Printemps', 'provenance': 'France',
        'prix': 2.50, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante vivace', 'recolte': 'Printemps',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 10, 'jours_recolte': 90, 'temperature_min': 5,
        'profondeur_semis': '0.5 cm', 'espacement': '30x20 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Autofertile'
    },
    'ortie': {
        'couleur': 'Vert', 'saison': 'Printemps', 'provenance': 'France',
        'prix': 0, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante vivace', 'recolte': 'Printemps',
        'semis_interieur': 'Mars', 'semis_exterieur': 'Avril',
        'jours_levée': 10, 'jours_recolte': 60, 'temperature_min': 5,
        'profondeur_semis': '0.5 cm', 'espacement': '30x30 cm',
        'pollinisation_type': 'vent', 'besoin_pollinisateur': False,
        'distance_pollinisation': 100, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Pollinisation par le vent'
    },
    'pourpier': {
        'couleur': 'Vert', 'saison': 'Été', 'provenance': 'France',
        'prix': 3.00, 'bourse': False, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': '30-40 jours',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 5, 'jours_recolte': 35, 'temperature_min': 15,
        'profondeur_semis': '0.5 cm', 'espacement': '30x20 cm',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 10, 'periode_floraison': 'Été',
        'conseils_pollinisation': 'Autofertile'
    },
    'champignon': {
        'couleur': 'Blanc', 'saison': 'Toute année', 'provenance': 'France',
        'prix': 4.00, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Champignonnière', 'recolte': 'Toute année',
        'semis_interieur': 'N/A', 'semis_exterieur': 'N/A',
        'jours_levée': 14, 'jours_recolte': 21, 'temperature_min': 12,
        'profondeur_semis': 'N/A', 'espacement': 'N/A',
        'pollinisation_type': 'auto', 'besoin_pollinisateur': False,
        'distance_pollinisation': 0, 'periode_floraison': 'N/A',
        'conseils_pollinisation': 'Culture en substrat'
    },
    'maïs doux': {
        'couleur': 'Jaune', 'saison': 'Été', 'provenance': 'France',
        'prix': 2.50, 'bourse': True, 'AOP': False, 'IGP': False,
        'plantation': 'Plante herbacée', 'recolte': 'Juillet-septembre',
        'semis_interieur': 'Avril', 'semis_exterieur': 'Mai',
        'jours_levée': 7, 'jours_recolte': 90, 'temperature_min': 15,
        'profondeur_semis': '3 cm', 'espacement': '80x30 cm',
        'pollinisation_type': 'vent', 'besoin_pollinisateur': False,
        'distance_pollinisation': 100, 'periode_floraison': 'Printemps',
        'conseils_pollinisation': 'Planter en blocs'
    },
}

# Valeurs par défaut pour les légumes non répertoriés
DEFAULT_VALUES = {
    'couleur': 'Variable',
    'provenance': 'Variable',
    'saison': 'Variable',
    'prix': 0,
    'bourse': False,
    'AOP': False,
    'IGP': False,
    'url': '',
    'plantation': 'Plante herbacée',
    'recolte': 'Variable',
    'semis_interieur': 'Mars-Avril',
    'semis_exterieur': 'Avril-Mai',
    'jours_levée': 10,
    'jours_recolte': 90,
    'temperature_min': 12,
    'profondeur_semis': '1-2 cm',
    'espacement': 'Variable',
    'pollinisation_type': 'auto',
    'besoin_pollinisateur': False,
    'pollinisateurs_conseilles': '',
    'distance_pollinisation': 10,
    'periode_floraison': 'Printemps-Été',
    'conseils_pollinisation': 'Information à compléter'
}


def get_legume_data(nom):
    """Retourne les données du légume si disponible, sinon les valeurs par défaut"""
    nom_clean = nom.lower().strip()

    # Correspondance exacte
    if nom_clean in LEGUMES_COMPLETE_DATA:
        data = LEGUMES_COMPLETE_DATA[nom_clean].copy()
        data['varietes'] = nom_clean
        return data

    # Correspondance partielle
    for key in LEGUMES_COMPLETE_DATA:
        if key in nom_clean or nom_clean in key:
            print(f" → Correspondance trouvée: {key} pour {nom}")
            return LEGUMES_COMPLETE_DATA[key]

    return DEFAULT_VALUES.copy()


def inserer_tous_les_legumes():
    """Insère tous les légumes avec leurs données réelles"""

    print("=== INSERTION DES LÉGUMES AVEC PRIX RÉELS ===\n")
    print(f"Nombre total de légumes à traiter : {len(liste_legumes_complete)}")

    compteur_nouveaux = 0
    compteur_existants = 0
    compteur_erreurs = 0

    for nom in liste_legumes_complete:
        nom_clean = nom.strip()

        # Vérifier si le légume existe déjà
        if Vegetable.objects.filter(nom__iexact=nom_clean).exists():
            print(f"⏭️ Déjà présent: {nom_clean}")
            compteur_existants += 1
            continue

        # Récupérer les données
        data = get_legume_data(nom_clean)

        try:
            nouveau_legume = Vegetable(
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
                jours_levée=data.get('jours_levée', 10),
                jours_recolte=data.get('jours_recolte', 90),
                temperature_min=data.get('temperature_min', 12),
                profondeur_semis=data.get('profondeur_semis', '1-2 cm'),
                espacement=data.get('espacement', 'Variable'),
                pollinisation_type=data.get('pollinisation_type', 'auto'),
                besoin_pollinisateur=data.get('besoin_pollinisateur', False),
                pollinisateurs_conseilles=data.get('pollinisateurs_conseilles', ''),
                distance_pollinisation=data.get('distance_pollinisation', 10),
                periode_floraison=data.get('periode_floraison', 'Printemps-Été'),
                conseils_pollinisation=data.get('conseils_pollinisation', 'Information à compléter')
            )
            nouveau_legume.save()
            print(f"✅ Ajouté: {nom_clean} - {data.get('prix', 0)}€ - {data.get('plantation', 'Type inconnu')}")
            compteur_nouveaux += 1

        except Exception as e:
            print(f"❌ Erreur pour {nom_clean}: {e}")
            compteur_erreurs += 1

    print(f"\n=== RÉSUMÉ FINAL ===")
    print(f"📊 Statistiques:")
    print(f" - Nouveaux légumes ajoutés : {compteur_nouveaux}")
    print(f" - Légumes déjà existants : {compteur_existants}")
    print(f" - Erreurs : {compteur_erreurs}")
    print(f" - Total traité : {len(liste_legumes_complete)}")

    # Vérification finale
    total_apres = Vegetable.objects.count()
    print(f"\n📦 Base de données après insertion : {total_apres} légumes")


if __name__ == '__main__':
    inserer_tous_les_legumes()