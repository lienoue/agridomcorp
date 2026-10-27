"""
🌱 GÉNÉRATION MASSIVE DE CONSEILS PERSONNALISÉS POUR TOUTES LES VARIÉTÉS
Base de plus de 200 cultures avec conseils détaillés
"""

import os
import django
import random
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriculture.settings')
django.setup()

from vegetables_fruits.models import Variete, Culture, ConseilPersonnalise

print("=" * 70)
print("🌱 GÉNÉRATION MASSIVE DES CONSEILS PERSONNALISÉS")
print("=" * 70)

# ============================================================
# BASE DE CONSEILS EXHAUSTIVE - 200+ CULTURES
# ============================================================

CONSEILS_PAR_CULTURE = {

    # ==================== LÉGUMES-FRUITS (SOLANACÉES) ====================
    'tomate': {
        'famille': 'Solanacées',
        'arrosage': [
            "Arrosez régulièrement mais sans excès, surtout pendant la fructification.",
            "Privilégiez un arrosage au pied pour éviter le mildiou.",
            "En période de forte chaleur, arrosez tous les 2-3 jours."
        ],
        'plantation': [
            "Plantez en pleine terre après les dernières gelées.",
            "Tuteurez les plants pour éviter qu'ils ne cassent.",
            "Espacez les plants de 50 cm en tous sens."
        ],
        'fertilisation': [
            "Apportez du compost avant la plantation.",
            "Fertilisez avec un engrais riche en potassium pendant la fructification."
        ],
        'protection': [
            "Surveillez le mildiou et traitez à la bouillie bordelaise.",
            "Paillez pour garder l'humidité."
        ]
    },
    'tomate cerise': {
        'famille': 'Solanacées',
        'arrosage': [
            "Arrosez régulièrement mais sans excès.",
            "Arrosez au pied pour éviter les maladies."
        ],
        'plantation': [
            "Plantez en plein soleil après les gelées.",
            "Tuteurez les plants (ils peuvent atteindre 2m).",
            "Espacez de 40 cm."
        ],
        'fertilisation': [
            "Apportez du compost à la plantation.",
            "Engrais riche en potassium pendant la fructification."
        ],
        'protection': [
            "Surveillez le mildiou.",
            "Paillez pour garder l'humidité."
        ]
    },
    'tomate ancienne': {
        'famille': 'Solanacées',
        'arrosage': [
            "Arrosez régulièrement au pied.",
            "Évitez de mouiller les feuilles."
        ],
        'plantation': [
            "Plantez après les dernières gelées.",
            "Tuteurez les variétés hautes.",
            "Espacez de 50-60 cm."
        ],
        'fertilisation': [
            "Compost avant plantation.",
            "Engrais riche en potassium."
        ],
        'protection': [
            "Variétés souvent plus sensibles au mildiou.",
            "Paillez et traitez préventivement."
        ]
    },
    'aubergine': {
        'famille': 'Solanacées',
        'arrosage': [
            "Arrosez régulièrement sans excès.",
            "Arrosez au pied, matin ou soir."
        ],
        'plantation': [
            "Plantez en plein soleil.",
            "Sol chaud et bien drainé.",
            "Espacez de 50-60 cm."
        ],
        'fertilisation': [
            "Apportez du compost avant la plantation.",
            "Engrais riche en potassium."
        ],
        'protection': [
            "Protégez du vent.",
            "Paillez pour garder l'humidité."
        ]
    },
    'poivron': {
        'famille': 'Solanacées',
        'arrosage': [
            "Arrosez régulièrement sans excès.",
            "Arrosez au pied."
        ],
        'plantation': [
            "Plantez en plein soleil.",
            "Sol chaud.",
            "Espacez de 40-50 cm."
        ],
        'fertilisation': [
            "Compost avant plantation.",
            "Engrais riche en potassium."
        ],
        'protection': [
            "Protégez du vent.",
            "Paillez pour garder l'humidité."
        ]
    },
    'piment': {
        'famille': 'Solanacées',
        'arrosage': [
            "Arrosez régulièrement.",
            "Arrosez au pied."
        ],
        'plantation': [
            "Plantez en plein soleil.",
            "Sol chaud et bien drainé.",
            "Espacez de 40-50 cm."
        ],
        'fertilisation': [
            "Compost avant plantation.",
            "Engrais riche en potassium."
        ],
        'protection': [
            "Protégez du vent.",
            "Paillez pour garder l'humidité."
        ]
    },
    'pomme de terre': {
        'famille': 'Solanacées',
        'arrosage': [
            "Arrosez régulièrement en période de tuberisation.",
            "Évitez l'excès d'eau qui favorise le mildiou."
        ],
        'plantation': [
            "Plantez quand le sol est réchauffé (> 10°C).",
            "Buttez les plants.",
            "Espacez de 30-40 cm."
        ],
        'fertilisation': [
            "Compost avant plantation.",
            "Évitez les engrais trop riches en azote."
        ],
        'protection': [
            "Surveillez le mildiou et le doryphore.",
            "Traitez à la bouillie bordelaise si nécessaire."
        ]
    },

    # ==================== LÉGUMES-RACINES ====================
    'carotte': {
        'famille': 'Apiacées',
        'arrosage': [
            "Arrosez régulièrement pour éviter les carottes fibreuses.",
            "Arrosez en pluie fine."
        ],
        'plantation': [
            "Semez en place, ne repiquez pas.",
            "Éclaircissez à 3-5 cm.",
            "Sol léger et profond."
        ],
        'fertilisation': [
            "Évitez les engrais trop riches en azote.",
            "Compost bien décomposé avant semis."
        ],
        'protection': [
            "Protégez de la mouche de la carotte avec un voile."
        ]
    },
    'carotte violette': {
        'famille': 'Apiacées',
        'arrosage': ["Arrosez régulièrement en pluie fine."],
        'plantation': [
            "Semez en place.",
            "Éclaircissez à 5 cm."
        ],
        'fertilisation': ["Compost bien décomposé."],
        'protection': ["Protégez de la mouche de la carotte."]
    },
    'betterave': {
        'famille': 'Chénopodiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': [
            "Semez en place.",
            "Éclaircissez à 10 cm.",
            "Sol léger et bien drainé."
        ],
        'fertilisation': [
            "Compost avant semis.",
            "Évitez les engrais trop azotés."
        ],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'betterave rouge': {
        'famille': 'Chénopodiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place, éclaircissez à 10 cm."],
        'fertilisation': ["Compost avant semis."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'radis': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement pour éviter les radis piquants."],
        'plantation': [
            "Semez en place.",
            "Semez échelonné tous les 15 jours.",
            "Éclaircissez à 3 cm."
        ],
        'fertilisation': ["Sol frais et riche."],
        'protection': ["Protégez des altises."]
    },
    'radis noir': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en été pour récolte d'hiver."],
        'fertilisation': ["Sol profond et frais."],
        'protection': ["Protégez des altises."]
    },
    'navet': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': [
            "Semez en place.",
            "Éclaircissez à 10-15 cm."
        ],
        'fertilisation': ["Compost avant semis."],
        'protection': ["Protégez des altises."]
    },
    'panais': {
        'famille': 'Apiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': [
            "Semez en place.",
            "Éclaircissez à 10-15 cm.",
            "Sol profond."
        ],
        'fertilisation': ["Compost bien décomposé."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'salsifis': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': [
            "Semez en place.",
            "Éclaircissez à 10-15 cm."
        ],
        'fertilisation': ["Compost avant semis."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'scorsonère': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place, éclaircissez à 10 cm."],
        'fertilisation': ["Compost avant semis."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'céleri-rave': {
        'famille': 'Apiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': [
            "Plantez en pleine terre après les gelées.",
            "Espacez de 30 cm."
        ],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'topinambour': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez modérément."],
        'plantation': [
            "Plantez les tubercules au printemps.",
            "Attention : envahissant !"
        ],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Contenez la croissance."]
    },
    'patate douce': {
        'famille': 'Convolvulacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': [
            "Plantez après les gelées.",
            "Sol chaud et bien drainé."
        ],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'igname': {
        'famille': 'Dioscoréacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez au printemps."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Tuteurez les plants."]
    },
    'manioc': {
        'famille': 'Euphorbiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez les boutures au printemps."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Protégez du froid."]
    },

    # ==================== LÉGUMES-FEUILLES ====================
    'salade': {
        'famille': 'Astéracées',
        'arrosage': [
            "Arrosez régulièrement pour éviter qu'elle ne monte en graines.",
            "Arrosez le matin de préférence."
        ],
        'plantation': [
            "Plantez à mi-ombre en été.",
            "Semez échelonné tous les 15 jours."
        ],
        'fertilisation': ["Apportez un engrais riche en azote."],
        'protection': ["Protégez des limaces."]
    },
    'laitue': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez échelonné tous les 15 jours."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des limaces."]
    },
    'roquette': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place, éclaircissez à 10 cm."],
        'fertilisation': ["Sol riche."],
        'protection': ["Protégez des altises."]
    },
    'mâche': {
        'famille': 'Caprifoliacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en été/automne."],
        'fertilisation': ["Compost avant semis."],
        'protection': ["Protégez du froid."]
    },
    'épinard': {
        'famille': 'Chénopodiacées',
        'arrosage': [
            "Arrosez régulièrement.",
            "Arrosez au pied."
        ],
        'plantation': [
            "Plantez à mi-ombre en été.",
            "Sol frais et riche."
        ],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des limaces."]
    },
    'blette': {
        'famille': 'Chénopodiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place, éclaircissez à 30 cm."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des limaces."]
    },
    'chou': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': [
            "Plantez en plein soleil ou mi-ombre.",
            "Sol riche et frais."
        ],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des chenilles avec un voile."]
    },
    'chou vert': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des chenilles."]
    },
    'chou rouge': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des chenilles."]
    },
    'chou blanc': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des chenilles."]
    },
    'chou frisé': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des chenilles."]
    },
    'chou kale': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des chenilles."]
    },
    'chou de bruxelles': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil, espacez de 60 cm."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des chenilles."]
    },
    'chou-fleur': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des chenilles."]
    },
    'chou-rave': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des chenilles."]
    },
    'chou chinois': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des chenilles."]
    },
    'brocoli': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des chenilles."]
    },
    'endive': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Forçage en cave, arrosez régulièrement."],
        'fertilisation': ["Sol riche."],
        'protection': ["Protégez de la lumière."]
    },
    'cresson': {
        'famille': 'Brassicacées',
        'arrosage': ["Arrosez abondamment."],
        'plantation': ["Semez dans un sol humide."],
        'fertilisation': ["Sol riche."],
        'protection': ["Protégez des limaces."]
    },
    'pourpier': {
        'famille': 'Portulacacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Sol léger."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'oseille': {
        'famille': 'Polygonacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Sol riche."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'pissenlit': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Sol riche."],
        'protection': ["Couvrez pour blanchir les pousses."]
    },
    'rhubarbe': {
        'famille': 'Polygonacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez à mi-ombre."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Paillez pour garder l'humidité."]
    },

    # ==================== LÉGUMES-BULBES ====================
    'oignon': {
        'famille': 'Alliacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Surveillez le mildiou."]
    },
    'oignon rouge': {
        'famille': 'Alliacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Surveillez le mildiou."]
    },
    'oignon blanc': {
        'famille': 'Alliacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Surveillez le mildiou."]
    },
    'échalote': {
        'famille': 'Alliacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Surveillez le mildiou."]
    },
    'ail': {
        'famille': 'Alliacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en automne ou printemps."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Surveillez le mildiou."]
    },
    'ail rose': {
        'famille': 'Alliacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en automne."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Surveillez le mildiou."]
    },
    'poireau': {
        'famille': 'Alliacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'ciboulette': {
        'famille': 'Alliacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil ou mi-ombre."],
        'fertilisation': ["Compost au printemps."],
        'protection': ["Divisez les touffes tous les 3 ans."]
    },

    # ==================== LÉGUMES-FRUITS (CUCURBITACÉES) ====================
    'courgette': {
        'famille': 'Cucurbitacées',
        'arrosage': ["Arrosez abondamment mais espacé."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Surveillez l'oïdium."]
    },
    'concombre': {
        'famille': 'Cucurbitacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Protégez de l'oïdium."]
    },
    'cornichon': {
        'famille': 'Cucurbitacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Protégez de l'oïdium."]
    },
    'melon': {
        'famille': 'Cucurbitacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Protégez de l'oïdium."]
    },
    'pastèque': {
        'famille': 'Cucurbitacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Protégez de l'oïdium."]
    },
    'potiron': {
        'famille': 'Cucurbitacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Protégez de l'oïdium."]
    },
    'citrouille': {
        'famille': 'Cucurbitacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Protégez de l'oïdium."]
    },
    'courge': {
        'famille': 'Cucurbitacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Protégez de l'oïdium."]
    },
    'butternut': {
        'famille': 'Cucurbitacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Protégez de l'oïdium."]
    },
    'potimarron': {
        'famille': 'Cucurbitacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost avant plantation."],
        'protection': ["Protégez de l'oïdium."]
    },

    # ==================== LÉGUMINEUSES ====================
    'haricot': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez régulièrement en floraison."],
        'plantation': ["Semez quand le sol est chaud."],
        'fertilisation': ["Pas d'engrais azoté."],
        'protection': ["Surveillez les pucerons."]
    },
    'haricot vert': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en poquets de 3-4 graines."],
        'fertilisation': ["Pas d'engrais azoté."],
        'protection': ["Surveillez les pucerons."]
    },
    'haricot rouge': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en poquets."],
        'fertilisation': ["Pas d'engrais azoté."],
        'protection': ["Surveillez les pucerons."]
    },
    'haricot blanc': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en poquets."],
        'fertilisation': ["Pas d'engrais azoté."],
        'protection': ["Surveillez les pucerons."]
    },
    'petit pois': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en ligne, tuteurez."],
        'fertilisation': ["Pas d'engrais azoté."],
        'protection': ["Surveillez les pucerons."]
    },
    'pois': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en ligne."],
        'fertilisation': ["Pas d'engrais azoté."],
        'protection': ["Surveillez les pucerons."]
    },
    'pois chiche': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez au printemps."],
        'fertilisation': ["Pas d'engrais azoté."],
        'protection': ["Surveillez les pucerons."]
    },
    'fève': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en automne ou printemps."],
        'fertilisation': ["Pas d'engrais azoté."],
        'protection': ["Surveillez les pucerons noirs."]
    },
    'lentille': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez au printemps."],
        'fertilisation': ["Pas d'engrais azoté."],
        'protection': ["Surveillez les pucerons."]
    },
    'soja': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez quand le sol est chaud."],
        'fertilisation': ["Pas d'engrais azoté."],
        'protection': ["Surveillez les pucerons."]
    },
    'arachide': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez au printemps."],
        'fertilisation': ["Pas d'engrais azoté."],
        'protection': ["Paillez pour garder l'humidité."]
    },

    # ==================== AROMATIQUES ====================
    'basilic': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez régulièrement sans mouiller les feuilles."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez du froid."]
    },
    'persil': {
        'famille': 'Apiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Sol riche."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'coriandre': {
        'famille': 'Apiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Sol riche."],
        'protection': ["Protégez de la chaleur."]
    },
    'menthe': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez à mi-ombre."],
        'fertilisation': ["Compost."],
        'protection': ["Contenez la croissance."]
    },
    'thym': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Protégez du froid."]
    },
    'romarin': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Protégez du froid."]
    },
    'sauge': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Taillez après floraison."]
    },
    'origan': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Protégez du froid."]
    },
    'marjolaine': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Protégez du froid."]
    },
    'aneth': {
        'famille': 'Apiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Sol riche."],
        'protection': ["Protégez du vent."]
    },
    'estragon': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'mélisse': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez à mi-ombre."],
        'fertilisation': ["Compost."],
        'protection': ["Contenez la croissance."]
    },
    'verveine': {
        'famille': 'Verbenacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost."],
        'protection': ["Protégez du froid."]
    },
    'angélique': {
        'famille': 'Apiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez à mi-ombre."],
        'fertilisation': ["Sol riche."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'fenouil': {
        'famille': 'Apiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Sol riche."],
        'protection': ["Protégez du vent."]
    },
    'curcuma': {
        'famille': 'Zingibéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez les rhizomes au printemps."],
        'fertilisation': ["Compost riche."],
        'protection': ["Protégez du froid."]
    },
    'gingembre': {
        'famille': 'Zingibéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez les rhizomes au printemps."],
        'fertilisation': ["Compost riche."],
        'protection': ["Protégez du froid."]
    },
    'laurier': {
        'famille': 'Lauracées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Protégez du froid."]
    },
    'sarriette': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Protégez du froid."]
    },
    'cerfeuil': {
        'famille': 'Apiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Sol riche."],
        'protection': ["Protégez de la chaleur."]
    },
    'livèche': {
        'famille': 'Apiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez à mi-ombre."],
        'fertilisation': ["Sol riche."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'hysope': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Protégez du froid."]
    },
    'bourrache': {
        'famille': 'Boraginacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Sol riche."],
        'protection': ["Paillez pour garder l'humidité."]
    },
    'pimprenelle': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Paillez pour garder l'humidité."]
    },

    # ==================== FRUITS ====================
    'fraise': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez régulièrement sans excès."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Paillez pour protéger les fruits."]
    },
    'fraise des bois': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez à mi-ombre."],
        'fertilisation': ["Compost."],
        'protection': ["Paillez pour protéger les fruits."]
    },
    'framboise': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil ou mi-ombre."],
        'fertilisation': ["Compost."],
        'protection': ["Tuteurez les plants."]
    },
    'mûre': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost."],
        'protection': ["Tuteurez les plants."]
    },
    'myrtille': {
        'famille': 'Éricacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Sol acide."],
        'fertilisation': ["Engrais acide."],
        'protection': ["Protégez des oiseaux."]
    },
    'cassis': {
        'famille': 'Grossulariacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil ou mi-ombre."],
        'fertilisation': ["Compost."],
        'protection': ["Taillez en hiver."]
    },
    'groseille': {
        'famille': 'Grossulariacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil ou mi-ombre."],
        'fertilisation': ["Compost."],
        'protection': ["Taillez en hiver."]
    },
    'pomme': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez en période de sécheresse."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Traitez contre la tavelure."]
    },
    'poire': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez en période de sécheresse."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Traitez contre la tavelure."]
    },
    'pêche': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Traitez contre la cloque."]
    },
    'nectarine': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Traitez contre la cloque."]
    },
    'abricot': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Protégez des gelées."]
    },
    'cerise': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez en période de sécheresse."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Protégez des oiseaux."]
    },
    'prune': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez en période de sécheresse."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Taillez en hiver."]
    },
    'mirabelle': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez en période de sécheresse."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Taillez en hiver."]
    },
    'quetsche': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez en période de sécheresse."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Taillez en hiver."]
    },
    'raisin': {
        'famille': 'Vitacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Traitez contre le mildiou."]
    },
    'vigne': {
        'famille': 'Vitacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Traitez contre le mildiou."]
    },
    'kiwi': {
        'famille': 'Actinidiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost."],
        'protection': ["Plantez mâle et femelle."]
    },
    'figue': {
        'famille': 'Moracées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Protégez du froid."]
    },
    'olive': {
        'famille': 'Oléacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Protégez du froid."]
    },
    'grenade': {
        'famille': 'Lythracées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Protégez du froid."]
    },
    'kaki': {
        'famille': 'Ébenacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Protégez du froid."]
    },
    'coing': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Taillez en hiver."]
    },
    'noix': {
        'famille': 'Juglandacées',
        'arrosage': ["Arrosez en période de sécheresse."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Taillez en hiver."]
    },
    'noisette': {
        'famille': 'Bétulacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Taillez en hiver."]
    },
    'amande': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Protégez des gelées."]
    },
    'châtaigne': {
        'famille': 'Fagacées',
        'arrosage': ["Arrosez en période de sécheresse."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Taillez en hiver."]
    },
    'pistache': {
        'famille': 'Anacardiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Protégez du froid."]
    },
    'noix de coco': {
        'famille': 'Arécacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost riche."],
        'protection': ["Protégez du froid."]
    },
    'avocat': {
        'famille': 'Lauracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost riche."],
        'protection': ["Protégez du froid."]
    },
    'mangue': {
        'famille': 'Anacardiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost riche."],
        'protection': ["Protégez du froid."]
    },
    'papaye': {
        'famille': 'Caricacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost riche."],
        'protection': ["Protégez du vent."]
    },
    'banane': {
        'famille': 'Musacées',
        'arrosage': ["Arrosez abondamment."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost riche."],
        'protection': ["Protégez du vent."]
    },
    'ananas': {
        'famille': 'Broméliacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Protégez du froid."]
    },
    'litchi': {
        'famille': 'Sapindacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost riche."],
        'protection': ["Protégez du froid."]
    },
    'goyave': {
        'famille': 'Myrtacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost riche."],
        'protection': ["Protégez du froid."]
    },
    'fruit de la passion': {
        'famille': 'Passifloracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Tuteurez la plante."]
    },

    # ==================== CÉRÉALES ====================
    'blé': {
        'famille': 'Poacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez en automne ou printemps."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Surveillez les maladies fongiques."]
    },
    'maïs': {
        'famille': 'Poacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez quand le sol est chaud."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des oiseaux."]
    },
    'orge': {
        'famille': 'Poacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez en automne ou printemps."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Surveillez les maladies fongiques."]
    },
    'avoine': {
        'famille': 'Poacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez au printemps."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Surveillez les maladies fongiques."]
    },
    'seigle': {
        'famille': 'Poacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez en automne."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Surveillez les maladies fongiques."]
    },
    'riz': {
        'famille': 'Poacées',
        'arrosage': ["Maintenez une lame d'eau."],
        'plantation': ["Repiquez en rizière."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Surveillez les maladies fongiques."]
    },
    'millet': {
        'famille': 'Poacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez quand le sol est chaud."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des oiseaux."]
    },
    'sorgho': {
        'famille': 'Poacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez quand le sol est chaud."],
        'fertilisation': ["Engrais riche en azote."],
        'protection': ["Protégez des oiseaux."]
    },
    'quinoa': {
        'famille': 'Amaranthacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez au printemps."],
        'fertilisation': ["Compost."],
        'protection': ["Protégez des oiseaux."]
    },
    'sarrasin': {
        'famille': 'Polygonacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez en été."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Paillez pour garder l'humidité."]
    },

    # ==================== FLEURS ====================
    'lavande': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Taillez après floraison."]
    },
    'romarin': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Protégez du froid."]
    },
    'thym': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Taillez après floraison."]
    },
    'sauge': {
        'famille': 'Lamiacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Taillez après floraison."]
    },
    'tournesol': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Protégez des oiseaux."]
    },
    'rose': {
        'famille': 'Rosacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais spécial rosiers."],
        'protection': ["Taillez en hiver."]
    },
    'tulipe': {
        'famille': 'Liliacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en automne."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Protégez des rongeurs."]
    },
    'jonquille': {
        'famille': 'Amaryllidacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en automne."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Protégez des rongeurs."]
    },
    'iris': {
        'famille': 'Iridacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en automne."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Divisez les touffes."]
    },
    'pivoine': {
        'famille': 'Paeoniacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Protégez du froid."]
    },
    'hortensia': {
        'famille': 'Hydrangéacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez à mi-ombre."],
        'fertilisation': ["Engrais acide."],
        'protection': ["Protégez du gel."]
    },
    'jasmin': {
        'famille': 'Oléacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Taillez après floraison."]
    },
    'chèvrefeuille': {
        'famille': 'Caprifoliacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil ou mi-ombre."],
        'fertilisation': ["Compost."],
        'protection': ["Taillez après floraison."]
    },
    'buddleia': {
        'famille': 'Scrophulariacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost."],
        'protection': ["Taillez en hiver."]
    },
    'lilas': {
        'famille': 'Oléacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost en automne."],
        'protection': ["Taillez après floraison."]
    },
    'clématite': {
        'famille': 'Renonculacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez à mi-ombre."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Tuteurez la plante."]
    },
    'glycine': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Taillez en hiver."]
    },
    'hibiscus': {
        'famille': 'Malvacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Protégez du froid."]
    },
    'bougainvillier': {
        'famille': 'Nyctaginacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Protégez du froid."]
    },
    'plumeria': {
        'famille': 'Apocynacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Protégez du froid."]
    },
    'orchidée': {
        'famille': 'Orchidacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez à mi-ombre."],
        'fertilisation': ["Engrais spécial orchidées."],
        'protection': ["Protégez du froid."]
    },
    'œillet': {
        'famille': 'Caryophyllacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Taillez après floraison."]
    },
    'marguerite': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Compost."],
        'protection': ["Divisez les touffes."]
    },
    'coquelicot': {
        'famille': 'Papaveracées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Laissez se ressemer."]
    },
    'bleuet': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Laissez se ressemer."]
    },
    'capucine': {
        'famille': 'Tropaeolacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Surveillez les pucerons."]
    },
    'souci': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Laissez se ressemer."]
    },
    'œillet d\'inde': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Surveillez les limaces."]
    },
    'cosmos': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Laissez se ressemer."]
    },
    'zinnia': {
        'famille': 'Astéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Surveillez l'oïdium."]
    },
    'belle-de-jour': {
        'famille': 'Convolvulacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Contenez la croissance."]
    },
    'pois de senteur': {
        'famille': 'Fabacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Semez en automne ou printemps."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Tuteurez la plante."]
    },
    'nigelle': {
        'famille': 'Renonculacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Laissez se ressemer."]
    },
    'pavot': {
        'famille': 'Papaveracées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Semez en place."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Laissez se ressemer."]
    },

    # ==================== FLEURS TROPICALES ====================
    'canna': {
        'famille': 'Cannacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Protégez du froid."]
    },
    'gingembre ornemental': {
        'famille': 'Zingibéracées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez à mi-ombre."],
        'fertilisation': ["Compost riche."],
        'protection': ["Protégez du froid."]
    },
    'héliconia': {
        'famille': 'Heliconiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez à mi-ombre."],
        'fertilisation': ["Compost riche."],
        'protection': ["Protégez du vent."]
    },
    'strelitzia': {
        'famille': 'Strelitziacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Protégez du froid."]
    },
    'protea': {
        'famille': 'Protéacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Sol bien drainé."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Protégez du froid."]
    },
    'frangipanier': {
        'famille': 'Apocynacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Protégez du froid."]
    },
    'allamanda': {
        'famille': 'Apocynacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Engrais riche en potassium."],
        'protection': ["Protégez du froid."]
    },
    'ixora': {
        'famille': 'Rubiacées',
        'arrosage': ["Arrosez régulièrement."],
        'plantation': ["Plantez à mi-ombre."],
        'fertilisation': ["Engrais acide."],
        'protection': ["Protégez du froid."]
    },
    'lantana': {
        'famille': 'Verbénacées',
        'arrosage': ["Arrosez modérément."],
        'plantation': ["Plantez en plein soleil."],
        'fertilisation': ["Peu d'engrais."],
        'protection': ["Taillez après floraison."]
    },
}

# ============================================================
# CONSEILS GÉNÉRAUX
# ============================================================

CONSEILS_GENERAUX = [
    "🌱 La rotation des cultures évite l'épuisement du sol.",
    "🐞 Les coccinelles sont vos alliées contre les pucerons.",
    "🌿 Le paillage conserve l'humidité et limite les mauvaises herbes.",
    "🍅 Retirez les gourmands des tomates pour favoriser la fructification.",
    "🌼 Les fleurs attirent les pollinisateurs, augmentez vos récoltes.",
    "💧 Arrosez le matin pour limiter l'évaporation.",
    "🌱 Le purin d'ortie est un excellent engrais naturel.",
    "🍂 Le compost maison enrichit le sol gratuitement.",
    "🌿 Associez les cultures pour repousser les nuisibles.",
    "💚 Plantez des engrais verts entre deux cultures.",
    "🌻 Le tournesol attire les pollinisateurs et les oiseaux.",
    "🐛 Inspectez régulièrement le dessous des feuilles.",
    "🍃 Taillez les plantes pour stimuler la croissance.",
    "🌙 Arrosez le soir en période de canicule.",
    "🪱 Les vers de terre indiquent un sol en bonne santé.",
]

CONSEILS_SAISON = {
    'printemps': [
        "🌱 C'est la saison des semis ! Plantez vos légumes d'été.",
        "💧 Arrosez modérément, la terre est encore humide.",
        "🌿 Apportez un engrais riche en azote pour le démarrage.",
        "⚠️ Surveillez les gelées tardives.",
        "🌻 Semez les fleurs pour attirer les pollinisateurs.",
    ],
    'ete': [
        "☀️ Arrosez tôt le matin ou tard le soir.",
        "💧 Évitez d'arroser les feuilles pour prévenir les maladies.",
        "🌿 Apportez un engrais riche en potassium pour la floraison.",
        "☂️ Installez un ombrage pour les cultures sensibles.",
        "🍅 Récoltez régulièrement pour stimuler la production.",
    ],
    'automne': [
        "🍂 Plantez les bulbes de printemps (ail, oignon).",
        "🌿 Apportez du compost pour préparer le sol.",
        "🧤 Paillez pour protéger du froid hivernal.",
        "💧 Arrosez moins fréquemment.",
        "🥬 Plantez les légumes d'hiver.",
    ],
    'hiver': [
        "❄️ Protégez les plantes sensibles au gel.",
        "🧤 Paillez les pieds des plantes.",
        "🌿 Apportez du compost en surface.",
        "💧 Arrosez très modérément.",
        "📚 Profitez-en pour planifier le printemps.",
    ]
}


# ============================================================
# FONCTION DE GÉNÉRATION
# ============================================================

def generer_conseils_pour_variete(variete):
    """Génère des conseils personnalisés pour une variété"""

    conseils = {
        'conseils_arrosage': [],
        'conseils_plantation': [],
        'conseils_fertilisation': [],
        'conseils_protection': [],
        'conseils_generaux': [],
        'conseils_saison': [],
        'saison': '',
        'climat': variete.climat if variete.climat else 'tempere',
    }

    # Récupérer les conseils de base par culture
    nom_culture = variete.culture.nom.lower() if variete.culture else ''

    # Chercher les conseils par culture parente
    for cle, valeur in CONSEILS_PAR_CULTURE.items():
        if cle in nom_culture or nom_culture in cle:
            conseils['conseils_arrosage'] = valeur.get('arrosage', [])
            conseils['conseils_plantation'] = valeur.get('plantation', [])
            conseils['conseils_fertilisation'] = valeur.get('fertilisation', [])
            conseils['conseils_protection'] = valeur.get('protection', [])
            break

    # Si pas de conseils trouvés, utiliser des génériques
    if not conseils['conseils_arrosage']:
        conseils['conseils_arrosage'] = [
            "Arrosez régulièrement selon les besoins de la plante.",
            "Privilégiez un arrosage au pied pour éviter les maladies."
        ]
        conseils['conseils_plantation'] = [
            "Plantez en pleine terre après les dernières gelées.",
            "Espacez les plants selon les recommandations de la variété."
        ]
        conseils['conseils_fertilisation'] = [
            "Apportez du compost avant la plantation.",
            "Fertilisez selon les besoins de la culture."
        ]
        conseils['conseils_protection'] = [
            "Surveillez les maladies et les ravageurs.",
            "Paillez pour protéger le sol."
        ]

    # Conseils généraux
    conseils['conseils_generaux'] = random.sample(CONSEILS_GENERAUX, 3)

    # Déterminer la saison actuelle
    mois = datetime.now().month
    if 3 <= mois <= 5:
        saison = 'printemps'
    elif 6 <= mois <= 8:
        saison = 'ete'
    elif 9 <= mois <= 11:
        saison = 'automne'
    else:
        saison = 'hiver'

    conseils['saison'] = saison
    conseils['conseils_saison'] = random.sample(CONSEILS_SAISON.get(saison, []), 3)

    return conseils


# ============================================================
# SAUVEGARDE EN BASE
# ============================================================

def sauvegarder_conseils():
    varietes = Variete.objects.all().select_related('culture')
    total = varietes.count()
    cree = 0
    mis_a_jour = 0
    erreurs = 0

    print(f"\n📊 {total} variété(s) à traiter")
    print("-" * 70)

    for i, variete in enumerate(varietes, 1):
        try:
            print(f"[{i}/{total}] 🌱 {variete.nom}", end=" ... ")

            conseils_data = generer_conseils_pour_variete(variete)

            conseil, created = ConseilPersonnalise.objects.update_or_create(
                variete=variete,
                defaults={
                    'conseils_arrosage': conseils_data['conseils_arrosage'],
                    'conseils_plantation': conseils_data['conseils_plantation'],
                    'conseils_fertilisation': conseils_data['conseils_fertilisation'],
                    'conseils_protection': conseils_data['conseils_protection'],
                    'conseils_generaux': conseils_data['conseils_generaux'],
                    'conseils_saison': conseils_data['conseils_saison'],
                    'saison': conseils_data['saison'],
                    'climat': conseils_data['climat'],
                }
            )

            if created:
                cree += 1
                print("✅")
            else:
                mis_a_jour += 1
                print("🔄")

        except Exception as e:
            erreurs += 1
            print(f"❌ Erreur: {e}")

    print("\n" + "=" * 70)
    print("📋 RÉCAPITULATIF")
    print("=" * 70)
    print(f" ✅ Créés : {cree}")
    print(f" 🔄 Mis à jour : {mis_a_jour}")
    print(f" ❌ Erreurs : {erreurs}")
    print(f" 📊 Total : {cree + mis_a_jour}/{total}")
    print("=" * 70)


# Exécution directe
sauvegarder_conseils()