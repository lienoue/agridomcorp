import csv
import time
from django.db.models.functions import Lower
import requests
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q
from django.core.mail import send_mail
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, FigureForm, InscriptionEleveForm
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Vegetable, GeometricFigure, Fruit, AlerteSemis, ProgressionJunior, Classe, Eleve, NotificationEnseignant, ChronologieCulture, QuestionQuiz, QuizUtilisateur, Badge, AlerteMeteo, SignalementForum, MessageForum, SujetForum, CategorieForum, MissionHebdomadaire
import logging
import json
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordResetForm
from django.core.paginator import Paginator
import stripe
from django.views.decorators.http import require_POST
from datetime import datetime, date
from .models import (
    CustomUser, PlanTarification, Abonnement,
    Facture, ConsentementRGPD, JournalBord, ProgressionMissionHebdo, StreakConnexion, CalendrierSemis, Autosuffisance, RappelUtilisateur, RotationCulture, AssociationCulture, BilanCarbone, SujetLu
)
from django.core.mail import send_mail
from .subscription_utils import has_quiz_access
from django.core.cache import cache
from PIL import Image as PilImage
from .models import (
    # Forum Adulte
    ForumAdulteCategorie,
    ForumAdulteSujet,
    MessageForumAdulte,
    ForumAdulteVote,
    ForumAdulteSignalement,
    ForumAdulteNotification,
    ForumBadge,
    ForumBadgeUtilisateur,
    ModerateurForum,
    SanctionUtilisateur,
)

# ✅ Mapping des départements/régions Mapbox vers les régions de la base
REGION_MAPPING = {
    # ==================== FRANCE ====================
    # Île-de-France
    'seine-et-marne': 'iledefrance',
    'yvelines': 'iledefrance',
    'essonne': 'iledefrance',
    'hauts-de-seine': 'iledefrance',
    'seine-saint-denis': 'iledefrance',
    'val-de-marne': 'iledefrance',
    'val-d-90ise': 'iledefrance',
    'paris': 'iledefrance',
    'ile-de-france': 'iledefrance',
    'iledefrance': 'iledefrance',

    # Provence
    'bouches-du-rhone': 'provence',
    'var': 'provence',
    'vaucluse': 'provence',
    'alpes-de-haute-provence': 'provence',
    'alpes-maritimes': 'provence',
    'hautes-alpes': 'provence',
    'provence-alpes-cote-d-azur': 'provence',
    'provence': 'provence',

    # Bretagne
    'finistere': 'bretagne',
    'cotes-d-armor': 'bretagne',
    'morbihan': 'bretagne',
    'ille-et-vilaine': 'bretagne',
    'bretagne': 'bretagne',

    # Normandie
    'seine-maritime': 'normandie',
    'eure': 'normandie',
    'calvados': 'normandie',
    'manche': 'normandie',
    'orne': 'normandie',
    'normandie': 'normandie',

    # Alsace
    'bas-rhin': 'alsace',
    'haut-rhin': 'alsace',
    'alsace': 'alsace',

    # ==================== JAPON ====================
    'japan': 'japon',
    'japon': 'japon',
    'tokyo': 'japon',
    'osaka': 'japon',
    'kyoto': 'japon',
    'hokkaido': 'japon',

    # ==================== EUROPE ====================
    'germany': 'europe_nord',
    'deutschland': 'europe_nord',
    'berlin': 'europe_nord',
    'italy': 'europe_sud',
    'italia': 'europe_sud',
    'spain': 'europe_sud',
    'espana': 'europe_sud',
    'portugal': 'europe_sud',
    'greece': 'europe_sud',
    'netherlands': 'europe_nord',
    'belgium': 'europe_nord',
    'switzerland': 'europe_sud',
    'austria': 'europe_sud',
    'sweden': 'europe_nord',
    'norway': 'europe_nord',
    'finland': 'europe_nord',
    'denmark': 'europe_nord',
    'poland': 'europe_nord',

    # ==================== AMÉRIQUE DU NORD ====================
    'california': 'californie',
    'californie': 'californie',
    'los angeles': 'californie',
    'san francisco': 'californie',
    'new york': 'usa_nord_est',
    'boston': 'usa_nord_est',
    'chicago': 'usa_nord_est',
    'canada': 'canada',
    'quebec': 'canada',
    'ontario': 'canada',
    'mexico': 'mexique',
    'mexique': 'mexique',

    # ==================== AMÉRIQUE DU SUD ====================
    'brazil': 'bresil',
    'bresil': 'bresil',
    'sao paulo': 'bresil',
    'argentina': 'argentine',
    'argentine': 'argentine',
    'buenos aires': 'argentine',
    'chile': 'chili',
    'chili': 'chili',
    'santiago': 'chili',

    # ==================== ASIE ====================
    'china': 'chine',
    'chine': 'chine',
    'beijing': 'chine',
    'shanghai': 'chine',
    'india': 'inde',
    'inde': 'inde',
    'delhi': 'inde',
    'mumbai': 'inde',

    # ==================== OCÉANIE ====================
    'australia': 'australie_sud_est',
    'australie': 'australie_sud_est',
    'sydney': 'australie_sud_est',
    'melbourne': 'australie_sud_est',
    'new zealand': 'nouvelle_zelande',
    'nouvelle-zelande': 'nouvelle_zelande',
    'auckland': 'nouvelle_zelande',

    # ==================== AFRIQUE ====================
    'morocco': 'afrique_nord',
    'maroc': 'afrique_nord',
    'algeria': 'afrique_nord',
    'algerie': 'afrique_nord',
    'tunisia': 'afrique_nord',
    'tunisie': 'afrique_nord',
    'egypt': 'afrique_nord',
    'egypte': 'afrique_nord',
    'senegal': 'afrique_ouest',
    'ivory coast': 'afrique_ouest',
    'cote d ivoire': 'afrique_ouest',
    'nigeria': 'afrique_ouest',
    'kenya': 'afrique_est',
    'tanzania': 'afrique_est',
    'ethiopia': 'afrique_est',
    'south africa': 'afrique_australe',
    'afrique du sud': 'afrique_australe',

    # ==================== MOYEN-ORIENT ====================
    'israel': 'moyen_orient',
    'turkey': 'moyen_orient',
    'turquie': 'moyen_orient',
    'iran': 'moyen_orient',
    'iraq': 'moyen_orient',
    'saudi arabia': 'moyen_orient',
    'arabie saoudite': 'moyen_orient',
    'uae': 'moyen_orient',
    'emirats arabes unis': 'moyen_orient',
}


# Configuration du logger
logger = logging.getLogger(__name__)

# ==================== DICTIONNAIRE DES TYPES DE SOL PAR RÉGION ====================
SOL_PAR_REGION = {
    # ==================== FRANCE ====================
    'provence': 'calcaire',
    'provence-alpes-côte-dazur': 'calcaire',
    'paca': 'calcaire',
    'iledefrance': 'limoneux',
    'île-de-france': 'limoneux',
    'paris': 'limoneux',
    'seine-et-marne': 'limoneux',
    'yvelines': 'limoneux',
    'essonne': 'limoneux',
    'hauts-de-seine': 'limoneux',
    'seine-saint-denis': 'limoneux',
    'val-de-marne': 'limoneux',
    'val-doisie': 'limoneux',
    'nord': 'argileux',
    'nord-pas-de-calais': 'argileux',
    'alsace': 'limoneux',
    'bretagne': 'argileux',
    'aquitaine': 'sableux',
    'nouvelle-aquitaine': 'sableux',
    'gironde': 'sableux',
    'landes': 'sableux',
    'occitanie': 'calcaire',
    'languedoc': 'calcaire',
    'auvergne': 'volcanique',
    'auvergne-rhône-alpes': 'volcanique',
    'rhone-alpes': 'volcanique',
    'ardeche': 'volcanique',
    'puy-de-dome': 'volcanique',
    'centre': 'limoneux',
    'centre-val-de-loire': 'limoneux',
    'normandie': 'limoneux',
    'haute-normandie': 'limoneux',
    'basse-normandie': 'argileux',
    'pays-de-la-loire': 'argileux',
    'bourgogne': 'calcaire',
    'bourgogne-franche-comte': 'calcaire',
    'franche-comte': 'calcaire',
    'grand-est': 'limoneux',
    'lorraine': 'argileux',
    'champagne': 'calcaire',
    'corse': 'calcaire',
    'corsica': 'calcaire',

    # ==================== EUROPE ====================
    'england': 'limoneux',
    'scotland': 'tourbeux',
    'wales': 'limoneux',
    'northern ireland': 'tourbeux',
    'london': 'limoneux',
    'manchester': 'argileux',
    'germany': 'limoneux',
    'deutschland': 'limoneux',
    'berlin': 'sableux',
    'bayern': 'calcaire',
    'bavaria': 'calcaire',
    'baden': 'limoneux',
    'rhineland': 'limoneux',
    'saxony': 'argileux',
    'italy': 'calcaire',
    'italia': 'calcaire',
    'toscana': 'calcaire',
    'tuscany': 'calcaire',
    'lazio': 'volcanique',
    'sicilia': 'calcaire',
    'sicily': 'calcaire',
    'campania': 'volcanique',
    'puglia': 'calcaire',
    'spain': 'calcaire',
    'españa': 'calcaire',
    'andalusia': 'calcaire',
    'andalucia': 'calcaire',
    'catalonia': 'calcaire',
    'cataluña': 'calcaire',
    'madrid': 'argileux',
    'valencia': 'sableux',
    'galicia': 'limoneux',
    'portugal': 'calcaire',
    'lisboa': 'calcaire',
    'algarve': 'sableux',
    'netherlands': 'argileux',
    'nederland': 'argileux',
    'amsterdam': 'argileux',
    'belgium': 'limoneux',
    'belgique': 'limoneux',
    'bruxelles': 'limoneux',
    'wallonie': 'argileux',
    'vlaanderen': 'sableux',
    'switzerland': 'calcaire',
    'schweiz': 'calcaire',
    'suisse': 'calcaire',
    'zurich': 'limoneux',
    'geneva': 'calcaire',
    'austria': 'calcaire',
    'österreich': 'calcaire',
    'vienna': 'limoneux',
    'tirol': 'calcaire',
    'sweden': 'tourbeux',
    'sverige': 'tourbeux',
    'norway': 'tourbeux',
    'norge': 'tourbeux',
    'finland': 'tourbeux',
    'suomi': 'tourbeux',
    'denmark': 'sableux',
    'danmark': 'sableux',
    'poland': 'limoneux',
    'polska': 'limoneux',
    'czechia': 'limoneux',
    'slovakia': 'limoneux',
    'hungary': 'limoneux',
    'romania': 'limoneux',
    'bulgaria': 'calcaire',
    'greece': 'calcaire',
    'ελλάδα': 'calcaire',
    'croatia': 'calcaire',
    'serbia': 'limoneux',

    # ==================== ASIE ====================
    'china': 'loess',
    'chine': 'loess',
    'république populaire de chine': 'loess',
    'mongolie-intérieure': 'steppique',
    'pekin': 'loess',
    'beijing': 'loess',
    'shanghai': 'alluvial',
    'guangzhou': 'latéritique',
    'shenzhen': 'latéritique',
    'hong kong': 'latéritique',
    'tibet': 'steppique',
    'xinjiang': 'désertique',
    'japan': 'volcanique',
    'japon': 'volcanique',
    'tokyo': 'volcanique',
    'hokkaido': 'volcanique',
    'osaka': 'alluvial',
    'kyoto': 'volcanique',
    'nagoya': 'alluvial',
    'fukuoka': 'volcanique',
    'okinawa': 'latéritique',
    'korea': 'limoneux',
    'south korea': 'limoneux',
    'north korea': 'limoneux',
    'seoul': 'limoneux',
    'india': 'latéritique',
    'inde': 'latéritique',
    'mumbai': 'latéritique',
    'delhi': 'alluvial',
    'kolkata': 'alluvial',
    'chennai': 'latéritique',
    'punjab': 'alluvial',
    'vietnam': 'latéritique',
    'thailand': 'latéritique',
    'indonesia': 'volcanique',
    'philippines': 'volcanique',
    'malaysia': 'latéritique',
    'singapore': 'latéritique',
    'myanmar': 'latéritique',
    'cambodia': 'latéritique',
    'laos': 'latéritique',
    'israel': 'désertique',
    'jordan': 'désertique',
    'lebanon': 'calcaire',
    'turkey': 'calcaire',
    'türkiye': 'calcaire',
    'istanbul': 'limoneux',
    'ankara': 'calcaire',
    'iran': 'désertique',
    'iraq': 'alluvial',
    'saudi arabia': 'désertique',
    'yemen': 'désertique',
    'oman': 'désertique',
    'uae': 'désertique',
    'dubai': 'sableux',
    'kazakhstan': 'steppique',
    'uzbekistan': 'désertique',
    'turkmenistan': 'désertique',
    'kyrgyzstan': 'calcaire',
    'tajikistan': 'calcaire',

    # ==================== AMÉRIQUE DU NORD ====================
    'usa': 'limoneux',
    'united states': 'limoneux',
    'california': 'méditerranéen',
    'californie': 'méditerranéen',
    'los angeles': 'méditerranéen',
    'san francisco': 'limoneux',
    'new york': 'limoneux',
    'texas': 'argileux',
    'florida': 'sableux',
    'floride': 'sableux',
    'chicago': 'limoneux',
    'seattle': 'limoneux',
    'denver': 'calcaire',
    'arizona': 'désertique',
    'nevada': 'désertique',
    'colorado': 'calcaire',
    'oregon': 'limoneux',
    'washington': 'limoneux',
    'canada': 'tourbeux',
    'quebec': 'tourbeux',
    'québec': 'tourbeux',
    'ontario': 'limoneux',
    'british columbia': 'limoneux',
    'alberta': 'limoneux',
    'manitoba': 'limoneux',
    'saskatchewan': 'limoneux',
    'montreal': 'limoneux',
    'toronto': 'limoneux',
    'vancouver': 'limoneux',
    'mexico': 'volcanique',
    'méxique': 'volcanique',
    'mexico city': 'volcanique',
    'guadalajara': 'volcanique',
    'monterrey': 'calcaire',
    'cancun': 'calcaire',
    'yucatan': 'calcaire',

    # ==================== AMÉRIQUE CENTRALE ====================
    'costa rica': 'volcanique',
    'puntarenas': 'volcanique',
    'san josé': 'volcanique',
    'panama': 'latéritique',
    'guatemala': 'volcanique',
    'honduras': 'latéritique',
    'nicaragua': 'volcanique',
    'el salvador': 'volcanique',
    'belize': 'calcaire',
    'cuba': 'calcaire',
    'jamaica': 'calcaire',
    'dominican republic': 'calcaire',
    'puerto rico': 'latéritique',
    'haiti': 'latéritique',
    'barbados': 'calcaire',

    # ==================== AMÉRIQUE DU SUD ====================
    'brazil': 'latéritique',
    'brésil': 'latéritique',
    'são paulo': 'latéritique',
    'rio de janeiro': 'latéritique',
    'amazonas': 'latéritique',
    'amazonie': 'latéritique',
    'argentina': 'limoneux',
    'argentine': 'limoneux',
    'buenos aires': 'limoneux',
    'chile': 'volcanique',
    'chili': 'volcanique',
    'santiago': 'calcaire',
    'peru': 'calcaire',
    'pérou': 'calcaire',
    'lima': 'désertique',
    'colombia': 'latéritique',
    'colombie': 'latéritique',
    'bogota': 'volcanique',
    'venezuela': 'latéritique',
    'ecuador': 'volcanique',
    'bolivia': 'calcaire',
    'paraguay': 'latéritique',
    'uruguay': 'limoneux',
    'guyana': 'latéritique',
    'suriname': 'latéritique',
    'french guiana': 'latéritique',

    # ==================== AFRIQUE ====================
    'morocco': 'calcaire',
    'maroc': 'calcaire',
    'casablanca': 'calcaire',
    'algeria': 'désertique',
    'algérie': 'désertique',
    'tunisia': 'calcaire',
    'tunisie': 'calcaire',
    'libya': 'désertique',
    'egypt': 'alluvial',
    'egypte': 'alluvial',
    'cairo': 'alluvial',
    'senegal': 'latéritique',
    'mali': 'désertique',
    'nigeria': 'latéritique',
    'ghana': 'latéritique',
    'ivory coast': 'latéritique',
    "côte d'ivoire": 'latéritique',
    'benin': 'latéritique',
    'togo': 'latéritique',
    'guinea': 'latéritique',
    'kenya': 'volcanique',
    'tanzania': 'latéritique',
    'ethiopia': 'volcanique',
    'éthiopie': 'volcanique',
    'uganda': 'volcanique',
    'rwanda': 'volcanique',
    'somalia': 'désertique',
    'congo': 'latéritique',
    'dr congo': 'latéritique',
    'cameroon': 'latéritique',
    'gabon': 'latéritique',
    'angola': 'latéritique',
    'south africa': 'calcaire',
    'afrique du sud': 'calcaire',
    'cape town': 'sableux',
    'johannesburg': 'limoneux',
    'zimbabwe': 'latéritique',
    'mozambique': 'latéritique',
    'namibia': 'désertique',
    'botswana': 'désertique',
    'zambia': 'latéritique',
    'madagascar': 'latéritique',

    # ==================== OCÉANIE ====================
    'australia': 'lateritique',
    'australie': 'lateritique',
    'sydney': 'sableux',
    'melbourne': 'limoneux',
    'brisbane': 'sableux',
    'perth': 'sableux',
    'adelaide': 'calcaire',
    'canberra': 'limoneux',
    'darwin': 'latéritique',
    'outback': 'désertique',
    'new zealand': 'volcanique',
    'nouvelle-zélande': 'volcanique',
    'auckland': 'volcanique',
    'wellington': 'limoneux',
    'christchurch': 'alluvial',
    'papua new guinea': 'latéritique',
    'fiji': 'volcanique',
    'tahiti': 'volcanique',
    'samoa': 'volcanique',
    'hawaii': 'volcanique',
    'guam': 'calcaire',

    # ==================== RÉGIONS POLAIRES ====================
    'greenland': 'tourbeux',
    'groenland': 'tourbeux',
    'iceland': 'volcanique',
    'islande': 'volcanique',
    'antarctica': 'glaciaire',
    'antarctique': 'glaciaire',
}

AGE_MAJORITE_PAR_LOCATION = {
    # Europe
    'france': 18,
    'allemagne': 18,
    'espagne': 18,
    'italie': 18,
    'royaume-uni': 18,
    'angleterre': 18,
    'ecosse': 16,
    'pays-bas': 18,
    'belgique': 18,
    'suisse': 18,
    'portugal': 18,
    'grece': 18,
    'suede': 18,
    'norvege': 18,
    'danemark': 18,
    'finlande': 18,
    'irlande': 18,
    'autriche': 18,
    'pologne': 18,
    'hongrie': 18,
    'republique tcheque': 18,
    'roumanie': 18,
    'bulgarie': 18,

    # Amérique du Nord
    'etats-unis': 21,
    'usa': 21,
    'canada': 18,
    'mexique': 18,

    # Amérique du Sud
    'bresil': 18,
    'argentine': 18,
    'chili': 18,
    'colombie': 18,
    'perou': 18,
    'venezuela': 18,
    'uruguay': 18,

    # Afrique
    'afrique du sud': 18,
    'senegal': 18,
    "côte d'ivoire": 18,
    'maroc': 18,
    'tunisie': 18,
    'algerie': 18,
    'egypte': 18,
    'kenya': 18,
    'nigeria': 18,
    'ghana': 18,
    'cameroun': 18,

    # Asie
    'japon': 18,
    'chine': 18,
    'inde': 18,
    'coree du sud': 19,
    'coree': 19,
    'singapour': 21,
    'malaisie': 18,
    'indonesie': 18,
    'thailande': 20,
    'vietnam': 18,
    'philippines': 18,
    'israel': 18,
    'turquie': 18,
    'iran': 18,
    'arabie saoudite': 18,

    # Océanie
    'australie': 18,
    'nouvelle-zelande': 18,
    'fidji': 18,

    # Par défaut
    'default': 18,
}

# ==================== CONSEILS PAR TYPE DE TERRAIN ====================
CONSEILS_PAR_TYPE_TERRAIN = {
    'appartement': {
        'emoji': '🏢',
        'titre': 'Culture en appartement',
        'conseils': [
            "🪴 Utilisez des pots de 20-30 cm de profondeur minimum.",
            "☀️ Placez vos plantes près d'une fenêtre lumineuse (6h de soleil).",
            "💧 Arrosez plus fréquemment qu'en pleine terre (le substrat sèche vite).",
            "🌱 Utilisez un terreau de qualité adapté aux cultures en pot.",
            "💨 Aérez régulièrement pour éviter les maladies fongiques.",
            "🔄 Rempotez tous les 1-2 ans pour renouveler le substrat.",
        ]
    },
    'maison': {
        'emoji': '🏡',
        'titre': 'Jardin de maison',
        'conseils': [
            "🌳 Plantez vos arbres fruitiers à 3-5 m des murs.",
            "🌱 Préparez le sol avec du compost avant plantation.",
            "💧 Installez un système d'arrosage automatique.",
            "🍂 Paillez pour protéger du froid en hiver.",
            "🌿 Alternez les cultures pour éviter l'épuisement du sol.",
        ]
    },
    'verger': {
        'emoji': '🍎',
        'titre': 'Verger',
        'conseils': [
            "🌳 Plantez 2 variétés différentes pour la pollinisation croisée.",
            "✂️ Taillez chaque hiver pour favoriser la fructification.",
            "🍎 Éclaircissez les fruits pour de plus belles pommes.",
            "🐛 Surveillez le carpocapse et la tavelure.",
            "📏 Espacez les arbres de 5-8 m selon la variété.",
        ]
    },
    'vigne': {
        'emoji': '🍇',
        'titre': 'Vigne',
        'conseils': [
            "🍇 Plantez en plein soleil avec un bon drainage.",
            "✂️ Taille d'hiver : gardez 1-2 yeux par sarment.",
            "🌿 Palissez les sarments pour une meilleure exposition.",
            "🍇 Récoltez quand les grappes sont sucrées (août-septembre).",
            "🦠 Surveillez le mildiou et l'oïdium.",
        ]
    },
    'serre': {
        'emoji': '♻️',
        'titre': 'Serre',
        'conseils': [
            "🌡️ Ventilez tous les jours pour éviter la surchauffe.",
            "💧 Arrosez moins souvent mais abondamment.",
            "🐝 Pollinisez manuellement (pas d'insectes en serre).",
            "🌿 Attention aux maladies fongiques (humidité élevée).",
            "📅 Semez plus tôt qu'en pleine terre (protection du gel).",
        ]
    },
    'batiment': {
        'emoji': '🏠',
        'titre': 'Bâtiment / Hangar',
        'conseils': [
            "🪴 Utilisez des jardinières ou des bacs surélevés.",
            "💧 Prévoyez un système d'arrosage régulier.",
            "☀️ Vérifiez l'ensoleillement de la zone.",
            "🌱 Adaptez les cultures à l'espace disponible.",
        ]
    },
    'maison': {
        'emoji': '🏡',
        'titre': 'Maison d\'habitation',
        'conseils': [
            "🌳 Plantez vos arbres fruitiers à 3-5 m des murs.",
            "🌱 Préparez le sol avec du compost avant plantation.",
            "💧 Installez un système d'arrosage automatique.",
            "🍂 Paillez pour protéger du froid en hiver.",
        ]
    },
    'friche': {
        'emoji': '🌿',
        'titre': 'Friche / Jachère',
        'conseils': [
            "🌱 Commencez par désherber et ameublir le sol.",
            "🌿 Plantez des engrais verts pour régénérer le sol.",
            "🐛 Attention aux ravageurs déjà présents.",
            "📅 Attendez 1 saison avant de planter des cultures exigeantes.",
        ]
    },
    'point_eau': {
        'emoji': '💧',
        'titre': 'Point d\'eau / Bassin',
        'conseils': [
            "💧 Utilisez cette réserve pour l'irrigation.",
            "🐟 Évitez les traitements chimiques à proximité.",
            "🌿 Plantez des plantes filtrantes autour (roseaux, iris).",
        ]
    },
    'zone_irrigation': {
        'emoji': '💦',
        'titre': 'Zone d\'irrigation',
        'conseils': [
            "💦 Installez un goutte-à-goutte pour économiser l'eau.",
            "📅 Arrosez tôt le matin ou tard le soir.",
            "🌱 Paillez pour limiter l'évaporation.",
        ]
    },
    'zone_paturage': {
        'emoji': '🐄',
        'titre': 'Zone de pâturage',
        'conseils': [
            "🐄 Rotation des pâturages pour éviter la surcharge.",
            "🌱 Semez des graminées adaptées au climat.",
            "💧 Prévoyez un abreuvoir pour les animaux.",
        ]
    },
    'foret': {
        'emoji': '🌲',
        'titre': 'Forêt / Bois',
        'conseils': [
            "🌲 Préservez la biodiversité existante.",
            "🍄 La forêt peut accueillir des champignons.",
            "🌿 Évitez de planter des cultures qui ont besoin de plein soleil.",
        ]
    },
    'autre': {
        'emoji': '📌',
        'titre': 'Autre',
        'conseils': [
            "🌱 Adaptez vos cultures à l'espace disponible.",
            "☀️ Vérifiez l'ensoleillement de la zone.",
            "💧 Prévoyez un arrosage adapté.",
        ]
    },
}
# ==================== FIN CONSEILS TYPE TERRAIN ====================

# ✅ DICTIONNAIRE EXHAUSTIF DES TAILLES (70+ cultures)
TAILLES_CULTURES = {
    # ===== FRUITS TROPICAUX & EXOTIQUES =====
    'abrico': {'hauteur': '200-400 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
               'espacement_rangs': '400-600 cm'},
    'açaï': {'hauteur': '1500-2000 cm', 'largeur': '100-200 cm', 'espacement': '200-300 cm',
             'espacement_rangs': '300-400 cm'},
    'acérola': {'hauteur': '200-300 cm', 'largeur': '200-300 cm', 'espacement': '200-300 cm',
                'espacement_rangs': '300-400 cm'},
    'achacha': {'hauteur': '300-600 cm', 'largeur': '200-400 cm', 'espacement': '400-600 cm',
                'espacement_rangs': '500-700 cm'},
    'aguaje': {'hauteur': '1500-2500 cm', 'largeur': '100-200 cm', 'espacement': '200-300 cm',
               'espacement_rangs': '300-400 cm'},
    'ananas': {'hauteur': '60-100 cm', 'largeur': '60-100 cm', 'espacement': '50-70 cm',
               'espacement_rangs': '80-100 cm'},
    'avocat': {'hauteur': '400-1000 cm', 'largeur': '300-600 cm', 'espacement': '500-800 cm',
               'espacement_rangs': '600-900 cm'},
    'banane': {'hauteur': '200-800 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
               'espacement_rangs': '400-600 cm'},
    'bergamote': {'hauteur': '200-400 cm', 'largeur': '200-300 cm', 'espacement': '300-400 cm',
                  'espacement_rangs': '400-500 cm'},
    'bilimbi': {'hauteur': '300-500 cm', 'largeur': '200-400 cm', 'espacement': '300-400 cm',
                'espacement_rangs': '400-500 cm'},
    'cacao': {'hauteur': '400-800 cm', 'largeur': '300-500 cm', 'espacement': '300-400 cm',
              'espacement_rangs': '400-500 cm'},
    'calamondin': {'hauteur': '200-300 cm', 'largeur': '200-300 cm', 'espacement': '200-300 cm',
                   'espacement_rangs': '300-400 cm'},
    'canistel': {'hauteur': '400-800 cm', 'largeur': '300-500 cm', 'espacement': '500-700 cm',
                 'espacement_rangs': '600-800 cm'},
    'carambole': {'hauteur': '300-500 cm', 'largeur': '200-400 cm', 'espacement': '300-400 cm',
                  'espacement_rangs': '400-500 cm'},
    'cassis': {'hauteur': '100-150 cm', 'largeur': '100-150 cm', 'espacement': '100-150 cm',
               'espacement_rangs': '150-200 cm'},
    'cerise': {'hauteur': '400-800 cm', 'largeur': '300-600 cm', 'espacement': '500-800 cm',
               'espacement_rangs': '600-900 cm'},
    'chérinole': {'hauteur': '300-600 cm', 'largeur': '200-400 cm', 'espacement': '300-400 cm',
                  'espacement_rangs': '400-500 cm'},
    'citron': {'hauteur': '200-400 cm', 'largeur': '200-300 cm', 'espacement': '300-400 cm',
               'espacement_rangs': '400-500 cm'},
    'coing': {'hauteur': '200-400 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
              'espacement_rangs': '400-600 cm'},
    'corossol': {'hauteur': '300-600 cm', 'largeur': '200-400 cm', 'espacement': '300-400 cm',
                 'espacement_rangs': '400-500 cm'},
    'datte': {'hauteur': '1000-1500 cm', 'largeur': '300-500 cm', 'espacement': '500-800 cm',
              'espacement_rangs': '600-900 cm'},
    'durian': {'hauteur': '1500-3000 cm', 'largeur': '300-600 cm', 'espacement': '500-800 cm',
               'espacement_rangs': '600-900 cm'},
    'feijoa': {'hauteur': '200-400 cm', 'largeur': '200-300 cm', 'espacement': '200-300 cm',
               'espacement_rangs': '300-400 cm'},
    'figue': {'hauteur': '200-400 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
              'espacement_rangs': '400-600 cm'},
    'fraise': {'hauteur': '15-30 cm', 'largeur': '30-50 cm', 'espacement': '30-40 cm',
               'espacement_rangs': '40-60 cm'},
    'framboise': {'hauteur': '150-200 cm', 'largeur': '50-100 cm', 'espacement': '50-70 cm',
                  'espacement_rangs': '150-200 cm'},
    'fruit de la passion': {'hauteur': '300-600 cm', 'largeur': '200-300 cm', 'espacement': '200-300 cm',
                            'espacement_rangs': '300-400 cm'},
    'fruit du dragon': {'hauteur': '200-400 cm', 'largeur': '200-300 cm', 'espacement': '200-300 cm',
                        'espacement_rangs': '300-400 cm'},
    'goyave': {'hauteur': '200-400 cm', 'largeur': '200-300 cm', 'espacement': '200-300 cm',
               'espacement_rangs': '300-400 cm'},
    'grenade': {'hauteur': '200-400 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
                'espacement_rangs': '400-600 cm'},
    'groseille': {'hauteur': '100-150 cm', 'largeur': '100-150 cm', 'espacement': '100-150 cm',
                  'espacement_rangs': '150-200 cm'},
    'jaboticaba': {'hauteur': '300-600 cm', 'largeur': '200-400 cm', 'espacement': '300-400 cm',
                   'espacement_rangs': '400-500 cm'},
    'kaki': {'hauteur': '300-600 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
             'espacement_rangs': '400-600 cm'},
    'kiwi': {'hauteur': '300-600 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
             'espacement_rangs': '400-600 cm'},
    'kumquat': {'hauteur': '150-300 cm', 'largeur': '150-250 cm', 'espacement': '150-200 cm',
                'espacement_rangs': '200-300 cm'},
    'litchi': {'hauteur': '400-800 cm', 'largeur': '300-500 cm', 'espacement': '500-700 cm',
               'espacement_rangs': '600-800 cm'},
    'longane': {'hauteur': '400-800 cm', 'largeur': '300-500 cm', 'espacement': '500-700 cm',
                'espacement_rangs': '600-800 cm'},
    'mangoustan': {'hauteur': '400-800 cm', 'largeur': '300-500 cm', 'espacement': '500-700 cm',
                   'espacement_rangs': '600-800 cm'},
    'mangue': {'hauteur': '400-1000 cm', 'largeur': '300-600 cm', 'espacement': '500-800 cm',
               'espacement_rangs': '600-900 cm'},
    'melon': {'hauteur': '40-60 cm', 'largeur': '100-200 cm', 'espacement': '80-100 cm',
              'espacement_rangs': '150-200 cm'},
    'mirabelle': {'hauteur': '200-400 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
                  'espacement_rangs': '400-600 cm'},
    'myrtille': {'hauteur': '100-200 cm', 'largeur': '100-150 cm', 'espacement': '100-150 cm',
                 'espacement_rangs': '150-200 cm'},
    'nèfle': {'hauteur': '200-400 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
              'espacement_rangs': '400-600 cm'},
    'noix de coco': {'hauteur': '1500-3000 cm', 'largeur': '300-600 cm', 'espacement': '500-800 cm',
                     'espacement_rangs': '600-900 cm'},
    'orange': {'hauteur': '300-600 cm', 'largeur': '300-500 cm', 'espacement': '400-600 cm',
               'espacement_rangs': '500-700 cm'},
    'pamplemousse': {'hauteur': '300-600 cm', 'largeur': '300-500 cm', 'espacement': '400-600 cm',
                     'espacement_rangs': '500-700 cm'},
    'papaye': {'hauteur': '300-600 cm', 'largeur': '200-300 cm', 'espacement': '300-400 cm',
               'espacement_rangs': '400-500 cm'},
    'pastèque': {'hauteur': '40-60 cm', 'largeur': '200-400 cm', 'espacement': '100-150 cm',
                 'espacement_rangs': '200-300 cm'},
    'pêche': {'hauteur': '200-400 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
              'espacement_rangs': '400-600 cm'},
    'physalis': {'hauteur': '60-100 cm', 'largeur': '40-60 cm', 'espacement': '40-50 cm',
                 'espacement_rangs': '60-80 cm'},
    'poire': {'hauteur': '200-400 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
              'espacement_rangs': '400-600 cm'},
    'pomme': {'hauteur': '200-400 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
              'espacement_rangs': '400-600 cm'},
    'prune': {'hauteur': '200-400 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
              'espacement_rangs': '400-600 cm'},
    'raisin': {'hauteur': '150-300 cm', 'largeur': '100-200 cm', 'espacement': '100-150 cm',
               'espacement_rangs': '150-250 cm'},
    'ramboutan': {'hauteur': '400-800 cm', 'largeur': '300-500 cm', 'espacement': '500-700 cm',
                  'espacement_rangs': '600-800 cm'},
    'sapote': {'hauteur': '400-800 cm', 'largeur': '300-500 cm', 'espacement': '500-700 cm',
               'espacement_rangs': '600-800 cm'},
    'tamarin': {'hauteur': '1000-2000 cm', 'largeur': '300-600 cm', 'espacement': '500-800 cm',
                'espacement_rangs': '600-900 cm'},
    'vanille': {'hauteur': '300-600 cm', 'largeur': '100-200 cm', 'espacement': '100-150 cm',
                'espacement_rangs': '200-300 cm'},
    'yuzu': {'hauteur': '200-400 cm', 'largeur': '200-300 cm', 'espacement': '300-400 cm',
             'espacement_rangs': '400-500 cm'},
    'pomelo': {'hauteur': '300-600 cm', 'largeur': '300-500 cm', 'espacement': '400-600 cm',
               'espacement_rangs': '500-700 cm'},
    'tangelo': {'hauteur': '300-600 cm', 'largeur': '300-500 cm', 'espacement': '400-600 cm',
                'espacement_rangs': '500-700 cm'},
    'tangerine': {'hauteur': '300-500 cm', 'largeur': '300-400 cm', 'espacement': '300-400 cm',
                  'espacement_rangs': '400-500 cm'},
    'ugli': {'hauteur': '300-500 cm', 'largeur': '300-400 cm', 'espacement': '300-400 cm',
             'espacement_rangs': '400-500 cm'},
    'pitaya': {'hauteur': '200-400 cm', 'largeur': '200-300 cm', 'espacement': '200-300 cm',
               'espacement_rangs': '300-400 cm'},
    'cherimoya': {'hauteur': '300-600 cm', 'largeur': '200-400 cm', 'espacement': '300-400 cm',
                  'espacement_rangs': '400-500 cm'},
    'lulo': {'hauteur': '200-300 cm', 'largeur': '150-200 cm', 'espacement': '150-200 cm',
             'espacement_rangs': '200-300 cm'},
    'cupuaçu': {'hauteur': '400-800 cm', 'largeur': '300-500 cm', 'espacement': '300-400 cm',
                'espacement_rangs': '400-500 cm'},
    'kiwano': {'hauteur': '30-50 cm', 'largeur': '100-200 cm', 'espacement': '80-100 cm',
               'espacement_rangs': '150-200 cm'},
    'pepino': {'hauteur': '60-100 cm', 'largeur': '40-60 cm', 'espacement': '40-50 cm',
               'espacement_rangs': '60-80 cm'},
    'maracudja': {'hauteur': '300-600 cm', 'largeur': '200-300 cm', 'espacement': '200-300 cm',
                  'espacement_rangs': '300-400 cm'},
    'nashi': {'hauteur': '200-400 cm', 'largeur': '200-400 cm', 'espacement': '300-500 cm',
              'espacement_rangs': '400-600 cm'},
    'lime': {'hauteur': '200-400 cm', 'largeur': '200-300 cm', 'espacement': '300-400 cm',
             'espacement_rangs': '400-500 cm'},
    'mandarine': {'hauteur': '300-500 cm', 'largeur': '300-400 cm', 'espacement': '300-400 cm',
                  'espacement_rangs': '400-500 cm'},
    'mûre': {'hauteur': '150-250 cm', 'largeur': '100-200 cm', 'espacement': '50-70 cm',
             'espacement_rangs': '150-200 cm'},
    'olive': {'hauteur': '300-800 cm', 'largeur': '300-600 cm', 'espacement': '500-800 cm',
              'espacement_rangs': '600-900 cm'},
    'noix': {'hauteur': '1000-2000 cm', 'largeur': '300-600 cm', 'espacement': '500-800 cm',
             'espacement_rangs': '600-900 cm'},
    'noisette': {'hauteur': '200-400 cm', 'largeur': '200-300 cm', 'espacement': '200-300 cm',
                 'espacement_rangs': '300-400 cm'},
    'amande': {'hauteur': '300-600 cm', 'largeur': '300-500 cm', 'espacement': '400-600 cm',
               'espacement_rangs': '500-700 cm'},
    'pistache': {'hauteur': '300-600 cm', 'largeur': '300-500 cm', 'espacement': '400-600 cm',
                 'espacement_rangs': '500-700 cm'},
    'châtaigne': {'hauteur': '1000-2000 cm', 'largeur': '300-600 cm', 'espacement': '500-800 cm',
                  'espacement_rangs': '600-900 cm'},
    'noix de cajou': {'hauteur': '400-800 cm', 'largeur': '300-600 cm', 'espacement': '500-800 cm',
                      'espacement_rangs': '600-900 cm'},
    'noix de macadamia': {'hauteur': '400-800 cm', 'largeur': '300-600 cm', 'espacement': '500-800 cm',
                          'espacement_rangs': '600-900 cm'},
    'noix de pécan': {'hauteur': '1000-2000 cm', 'largeur': '300-600 cm', 'espacement': '500-800 cm',
                      'espacement_rangs': '600-900 cm'},

    # ===== LÉGUMES =====
    'ail': {'hauteur': '30-60 cm', 'largeur': '10-15 cm', 'espacement': '10-15 cm', 'espacement_rangs': '20-30 cm'},
    'amarante': {'hauteur': '100-200 cm', 'largeur': '30-50 cm', 'espacement': '20-30 cm',
                 'espacement_rangs': '30-40 cm'},
    'arachide': {'hauteur': '30-50 cm', 'largeur': '30-40 cm', 'espacement': '20-30 cm',
                 'espacement_rangs': '40-50 cm'},
    'artichaut': {'hauteur': '100-150 cm', 'largeur': '80-120 cm', 'espacement': '80-100 cm',
                  'espacement_rangs': '100-120 cm'},
    'asperge': {'hauteur': '100-150 cm', 'largeur': '40-60 cm', 'espacement': '40-50 cm',
                'espacement_rangs': '100-120 cm'},
    'aubergine': {'hauteur': '60-100 cm', 'largeur': '50-70 cm', 'espacement': '50-60 cm',
                  'espacement_rangs': '80-100 cm'},
    'basilic': {'hauteur': '20-40 cm', 'largeur': '20-30 cm', 'espacement': '20-30 cm',
                'espacement_rangs': '30-40 cm'},
    'betterave': {'hauteur': '30-40 cm', 'largeur': '10-15 cm', 'espacement': '10-15 cm',
                  'espacement_rangs': '20-30 cm'},
    'blette': {'hauteur': '40-60 cm', 'largeur': '30-40 cm', 'espacement': '30-40 cm',
               'espacement_rangs': '40-50 cm'},
    'brocoli': {'hauteur': '40-70 cm', 'largeur': '40-60 cm', 'espacement': '50-60 cm',
                'espacement_rangs': '60-80 cm'},
    'cardon': {'hauteur': '100-150 cm', 'largeur': '60-100 cm', 'espacement': '60-80 cm',
               'espacement_rangs': '80-100 cm'},
    'carotte': {'hauteur': '30-40 cm', 'largeur': '10-15 cm', 'espacement': '3-5 cm',
                'espacement_rangs': '15-20 cm'},
    'céleri': {'hauteur': '40-60 cm', 'largeur': '30-40 cm', 'espacement': '30-40 cm',
               'espacement_rangs': '40-50 cm'},
    'chou': {'hauteur': '30-50 cm', 'largeur': '40-60 cm', 'espacement': '50-60 cm',
             'espacement_rangs': '60-80 cm'},
    'chou chinois': {'hauteur': '20-40 cm', 'largeur': '30-40 cm', 'espacement': '30-40 cm',
                     'espacement_rangs': '40-50 cm'},
    'chou de bruxelles': {'hauteur': '60-90 cm', 'largeur': '40-60 cm', 'espacement': '50-60 cm',
                          'espacement_rangs': '60-80 cm'},
    'chou-fleur': {'hauteur': '40-60 cm', 'largeur': '40-60 cm', 'espacement': '50-60 cm',
                   'espacement_rangs': '60-80 cm'},
    'chou-rave': {'hauteur': '30-40 cm', 'largeur': '20-30 cm', 'espacement': '30-40 cm',
                  'espacement_rangs': '40-50 cm'},
    'ciboulette': {'hauteur': '20-30 cm', 'largeur': '15-20 cm', 'espacement': '10-15 cm',
                   'espacement_rangs': '20-30 cm'},
    'citrouille': {'hauteur': '40-60 cm', 'largeur': '200-500 cm', 'espacement': '100-150 cm',
                   'espacement_rangs': '200-300 cm'},
    'concombre': {'hauteur': '30-40 cm', 'largeur': '100-150 cm', 'espacement': '30-40 cm',
                  'espacement_rangs': '80-100 cm'},
    'coriandre': {'hauteur': '30-50 cm', 'largeur': '20-30 cm', 'espacement': '15-20 cm',
                  'espacement_rangs': '20-30 cm'},
    'cornichon': {'hauteur': '30-40 cm', 'largeur': '80-120 cm', 'espacement': '30-40 cm',
                  'espacement_rangs': '80-100 cm'},
    'courge': {'hauteur': '40-60 cm', 'largeur': '200-500 cm', 'espacement': '100-150 cm',
               'espacement_rangs': '200-300 cm'},
    'courgette': {'hauteur': '40-60 cm', 'largeur': '80-120 cm', 'espacement': '80-100 cm',
                  'espacement_rangs': '100-120 cm'},
    'cresson': {'hauteur': '10-20 cm', 'largeur': '10-20 cm', 'espacement': '5-10 cm',
                'espacement_rangs': '10-15 cm'},
    'crosne': {'hauteur': '30-50 cm', 'largeur': '20-30 cm', 'espacement': '20-30 cm',
               'espacement_rangs': '30-40 cm'},
    'curcuma': {'hauteur': '60-100 cm', 'largeur': '40-60 cm', 'espacement': '30-40 cm',
                'espacement_rangs': '50-60 cm'},
    'échalote': {'hauteur': '20-30 cm', 'largeur': '10-15 cm', 'espacement': '10-15 cm',
                 'espacement_rangs': '20-30 cm'},
    'endive': {'hauteur': '15-25 cm', 'largeur': '10-15 cm', 'espacement': '10-15 cm',
               'espacement_rangs': '20-25 cm'},
    'épinard': {'hauteur': '15-30 cm', 'largeur': '15-20 cm', 'espacement': '5-10 cm',
                'espacement_rangs': '20-30 cm'},
    'estragon': {'hauteur': '30-60 cm', 'largeur': '20-30 cm', 'espacement': '20-30 cm',
                 'espacement_rangs': '30-40 cm'},
    'fenouil': {'hauteur': '60-120 cm', 'largeur': '30-40 cm', 'espacement': '30-40 cm',
                'espacement_rangs': '40-50 cm'},
    'fève': {'hauteur': '30-60 cm', 'largeur': '30-40 cm', 'espacement': '20-30 cm',
             'espacement_rangs': '40-50 cm'},
    'gingembre': {'hauteur': '60-100 cm', 'largeur': '40-60 cm', 'espacement': '30-40 cm',
                  'espacement_rangs': '50-60 cm'},
    'gombo': {'hauteur': '100-200 cm', 'largeur': '50-80 cm', 'espacement': '40-60 cm',
              'espacement_rangs': '80-100 cm'},
    'haricot': {'hauteur': '40-60 cm', 'largeur': '30-40 cm', 'espacement': '5-10 cm',
                'espacement_rangs': '40-50 cm'},
    'haricot vert': {'hauteur': '40-60 cm', 'largeur': '30-40 cm', 'espacement': '5-10 cm',
                     'espacement_rangs': '40-50 cm'},
    'laitue': {'hauteur': '20-30 cm', 'largeur': '20-30 cm', 'espacement': '25-30 cm',
               'espacement_rangs': '30-40 cm'},
    'lentille': {'hauteur': '20-40 cm', 'largeur': '20-30 cm', 'espacement': '5-10 cm',
                 'espacement_rangs': '20-30 cm'},
    'mâche': {'hauteur': '10-15 cm', 'largeur': '10-15 cm', 'espacement': '5-10 cm',
              'espacement_rangs': '10-15 cm'},
    'maïs': {'hauteur': '150-300 cm', 'largeur': '50-80 cm', 'espacement': '30-40 cm',
             'espacement_rangs': '70-80 cm'},
    'manioc': {'hauteur': '200-400 cm', 'largeur': '100-200 cm', 'espacement': '80-100 cm',
               'espacement_rangs': '100-120 cm'},
    'menthe': {'hauteur': '30-60 cm', 'largeur': '30-50 cm', 'espacement': '20-30 cm',
               'espacement_rangs': '30-40 cm'},
    'navet': {'hauteur': '20-30 cm', 'largeur': '5-10 cm', 'espacement': '10-15 cm',
              'espacement_rangs': '20-30 cm'},
    'oca du pérou': {'hauteur': '20-30 cm', 'largeur': '30-50 cm', 'espacement': '30-40 cm',
                     'espacement_rangs': '40-50 cm'},
    'oignon': {'hauteur': '30-50 cm', 'largeur': '10-15 cm', 'espacement': '10-15 cm',
               'espacement_rangs': '20-30 cm'},
    'oseille': {'hauteur': '20-40 cm', 'largeur': '20-30 cm', 'espacement': '20-25 cm',
                'espacement_rangs': '30-40 cm'},
    'panais': {'hauteur': '30-40 cm', 'largeur': '10-15 cm', 'espacement': '10-15 cm',
               'espacement_rangs': '20-30 cm'},
    'patate douce': {'hauteur': '20-30 cm', 'largeur': '100-200 cm', 'espacement': '30-40 cm',
                     'espacement_rangs': '80-100 cm'},
    'persil': {'hauteur': '20-30 cm', 'largeur': '15-20 cm', 'espacement': '10-15 cm',
               'espacement_rangs': '20-30 cm'},
    'petit pois': {'hauteur': '30-60 cm', 'largeur': '20-30 cm', 'espacement': '5-10 cm',
                   'espacement_rangs': '30-40 cm'},
    'piment': {'hauteur': '40-80 cm', 'largeur': '30-50 cm', 'espacement': '40-50 cm',
               'espacement_rangs': '60-80 cm'},
    'pissenlit': {'hauteur': '10-20 cm', 'largeur': '15-20 cm', 'espacement': '10-15 cm',
                  'espacement_rangs': '20-25 cm'},
    'poireau': {'hauteur': '40-60 cm', 'largeur': '3-5 cm', 'espacement': '15-20 cm',
                'espacement_rangs': '30-40 cm'},
    'pois chiche': {'hauteur': '30-60 cm', 'largeur': '30-40 cm', 'espacement': '20-30 cm',
                    'espacement_rangs': '40-50 cm'},
    'poivron': {'hauteur': '50-80 cm', 'largeur': '40-60 cm', 'espacement': '40-50 cm',
                'espacement_rangs': '60-80 cm'},
    'pomme de terre': {'hauteur': '40-60 cm', 'largeur': '30-50 cm', 'espacement': '30-40 cm',
                       'espacement_rangs': '60-80 cm'},
    'potiron': {'hauteur': '40-60 cm', 'largeur': '200-500 cm', 'espacement': '100-150 cm',
                'espacement_rangs': '200-300 cm'},
    'pourpier': {'hauteur': '10-20 cm', 'largeur': '20-30 cm', 'espacement': '10-15 cm',
                 'espacement_rangs': '20-25 cm'},
    'radis': {'hauteur': '15-20 cm', 'largeur': '3-5 cm', 'espacement': '2-3 cm', 'espacement_rangs': '10-15 cm'},
    'raifort': {'hauteur': '40-60 cm', 'largeur': '20-30 cm', 'espacement': '20-30 cm',
                'espacement_rangs': '30-40 cm'},
    'rhubarbe': {'hauteur': '40-60 cm', 'largeur': '60-100 cm', 'espacement': '60-80 cm',
                 'espacement_rangs': '80-100 cm'},
    'romarin': {'hauteur': '50-150 cm', 'largeur': '50-150 cm', 'espacement': '50-80 cm',
                'espacement_rangs': '80-100 cm'},
    'roquette': {'hauteur': '15-20 cm', 'largeur': '10-15 cm', 'espacement': '10-15 cm',
                 'espacement_rangs': '20-25 cm'},
    'rutabaga': {'hauteur': '30-40 cm', 'largeur': '10-15 cm', 'espacement': '15-20 cm',
                 'espacement_rangs': '30-40 cm'},
    'salade': {'hauteur': '20-30 cm', 'largeur': '20-30 cm', 'espacement': '25-30 cm',
               'espacement_rangs': '30-40 cm'},
    'salsifis': {'hauteur': '30-40 cm', 'largeur': '5-8 cm', 'espacement': '10-15 cm',
                 'espacement_rangs': '20-30 cm'},
    'sauge': {'hauteur': '30-60 cm', 'largeur': '30-50 cm', 'espacement': '30-40 cm',
              'espacement_rangs': '40-50 cm'},
    'soja': {'hauteur': '30-60 cm', 'largeur': '30-40 cm', 'espacement': '20-30 cm',
             'espacement_rangs': '40-50 cm'},
    'thym': {'hauteur': '15-30 cm', 'largeur': '20-40 cm', 'espacement': '20-30 cm',
             'espacement_rangs': '30-40 cm'},
    'tomate': {'hauteur': '50-150 cm', 'largeur': '40-80 cm', 'espacement': '50-60 cm',
               'espacement_rangs': '80-100 cm'},
    'topinambour': {'hauteur': '150-250 cm', 'largeur': '50-80 cm', 'espacement': '40-50 cm',
                    'espacement_rangs': '80-100 cm'},
    'wasabi': {'hauteur': '20-40 cm', 'largeur': '20-30 cm', 'espacement': '15-20 cm',
               'espacement_rangs': '20-30 cm'},
    'yacón': {'hauteur': '100-200 cm', 'largeur': '80-120 cm', 'espacement': '60-80 cm',
              'espacement_rangs': '80-100 cm'},

    # ===== AROMATIQUES & HERBES =====
    'aneth': {'hauteur': '30-60 cm', 'largeur': '20-30 cm', 'espacement': '15-20 cm',
              'espacement_rangs': '20-30 cm'},
    'marjolaine': {'hauteur': '20-40 cm', 'largeur': '20-30 cm', 'espacement': '20-30 cm',
                   'espacement_rangs': '30-40 cm'},
    'origan': {'hauteur': '20-40 cm', 'largeur': '20-30 cm', 'espacement': '20-30 cm',
               'espacement_rangs': '30-40 cm'},
    'périlla': {'hauteur': '30-60 cm', 'largeur': '20-30 cm', 'espacement': '20-30 cm',
                'espacement_rangs': '30-40 cm'},
    'shiso': {'hauteur': '30-60 cm', 'largeur': '20-30 cm', 'espacement': '20-30 cm',
              'espacement_rangs': '30-40 cm'},
    'laurier': {'hauteur': '200-400 cm', 'largeur': '200-300 cm', 'espacement': '200-300 cm',
                'espacement_rangs': '300-400 cm'},

    # ===== FLEURS POLLINISATRICES =====
    'lavande': {'hauteur': '30-60 cm', 'largeur': '30-50 cm', 'espacement': '30-40 cm',
                'espacement_rangs': '40-50 cm'},
    'tournesol': {'hauteur': '100-300 cm', 'largeur': '50-80 cm', 'espacement': '30-40 cm',
                  'espacement_rangs': '50-60 cm'},
    'rose': {'hauteur': '50-200 cm', 'largeur': '50-150 cm', 'espacement': '50-80 cm',
             'espacement_rangs': '80-100 cm'},
    'tulipe': {'hauteur': '20-60 cm', 'largeur': '10-20 cm', 'espacement': '10-15 cm',
               'espacement_rangs': '15-20 cm'},
    'orchidée': {'hauteur': '20-100 cm', 'largeur': '20-40 cm', 'espacement': '20-30 cm',
                 'espacement_rangs': '30-40 cm'},
    'jasmin': {'hauteur': '200-400 cm', 'largeur': '100-200 cm', 'espacement': '100-150 cm',
               'espacement_rangs': '150-200 cm'},
    'hortensia': {'hauteur': '100-200 cm', 'largeur': '100-200 cm', 'espacement': '100-150 cm',
                  'espacement_rangs': '150-200 cm'},
    'pivoine': {'hauteur': '60-100 cm', 'largeur': '60-100 cm', 'espacement': '60-80 cm',
                'espacement_rangs': '80-100 cm'},
    'iris': {'hauteur': '30-90 cm', 'largeur': '20-40 cm', 'espacement': '20-30 cm',
             'espacement_rangs': '30-40 cm'},
    'marguerite': {'hauteur': '20-40 cm', 'largeur': '20-30 cm', 'espacement': '20-25 cm',
                   'espacement_rangs': '30-40 cm'},
    'coquelicot': {'hauteur': '30-60 cm', 'largeur': '20-30 cm', 'espacement': '15-20 cm',
                   'espacement_rangs': '25-30 cm'},

    # ===== CÉRÉALES =====
    'riz': {'hauteur': '80-150 cm', 'largeur': '30-50 cm', 'espacement': '15-20 cm',
            'espacement_rangs': '20-30 cm'},
    'blé': {'hauteur': '60-120 cm', 'largeur': '20-30 cm', 'espacement': '5-10 cm', 'espacement_rangs': '15-20 cm'},
    'orge': {'hauteur': '60-100 cm', 'largeur': '20-30 cm', 'espacement': '5-10 cm',
             'espacement_rangs': '15-20 cm'},
    'avoine': {'hauteur': '80-120 cm', 'largeur': '20-30 cm', 'espacement': '5-10 cm',
               'espacement_rangs': '15-20 cm'},
    'seigle': {'hauteur': '80-150 cm', 'largeur': '20-30 cm', 'espacement': '5-10 cm',
               'espacement_rangs': '15-20 cm'},
    'millet': {'hauteur': '100-200 cm', 'largeur': '30-50 cm', 'espacement': '15-20 cm',
               'espacement_rangs': '30-40 cm'},
    'sorgho': {'hauteur': '100-300 cm', 'largeur': '30-50 cm', 'espacement': '15-20 cm',
               'espacement_rangs': '30-40 cm'},
}


def verifier_acces_abonnement(user, plan_requis=None):
    """
    Vérifie si l'utilisateur a accès à une fonctionnalité
    plan_requis: 'PREMIUM', 'ENSEIGNANT', 'BASIQUE', None (tous)
    Retourne: (acces: bool, message: str|None)
    """
    # Si aucun plan requis, tout le monde a accès
    if plan_requis is None:
        return True, None

    try:
        abonnement = user.abonnement
        if abonnement.est_actif and abonnement.plan.nom in ['PREMIUM', 'ENSEIGNANT']:
            return True, None
        if abonnement.est_actif and abonnement.plan.nom == plan_requis:
            return True, None
        return False, f"Cette fonctionnalité est disponible avec l'abonnement {plan_requis}."
    except Abonnement.DoesNotExist:
        if plan_requis == 'GRATUIT':
            return True, None
        return False, f"Cette fonctionnalité est disponible avec l'abonnement {plan_requis}."


def render_restriction_html(plan_requis, tab_name):
    """Retourne le HTML de restriction d'accès"""
    return f'''
        <div class="alert alert-warning" style="padding:30px; text-align:center; border-radius:15px; margin:20px 0;">
            <span style="font-size:3rem;">🔒</span>
            <h4 style="margin:15px 0 10px; color:#856404;">Fonctionnalité réservée</h4>
            <p style="color:#856404;">L'onglet "{tab_name}" est disponible avec l'abonnement <strong>{plan_requis}</strong>.</p>
            <p style="color:#856404; font-size:0.9rem;">Passez à l'offre supérieure pour y accéder.</p>
            <a href="/tarification/" class="btn btn-success" style="margin-top:15px; padding:10px 30px; border-radius:50px;">
                💰 Découvrir les offres
            </a>
        </div>
    '''


def get_age_majorite(location):
    """
    Retourne l'âge de majorité légal pour une localisation donnée
    """
    if not location:
        return AGE_MAJORITE_PAR_LOCATION.get('default', 18)

    location_lower = location.lower().strip()

    # Vérifier les correspondances exactes
    if location_lower in AGE_MAJORITE_PAR_LOCATION:
        return AGE_MAJORITE_PAR_LOCATION[location_lower]

    # Vérifier les correspondances partielles
    for key, age in AGE_MAJORITE_PAR_LOCATION.items():
        if key in location_lower or location_lower in key:
            return age

    return AGE_MAJORITE_PAR_LOCATION.get('default', 18)


def get_user_location(user):
    """
    Récupère la localisation (pays/région) de l'utilisateur
    """
    # 1. Si la location est déjà stockée en base
    if user.location:
        return user.location

    # 2. Essayer de récupérer depuis la première figure avec coordonnées
    from .models import GeometricFigure
    figure = GeometricFigure.objects.filter(
        user=user,
        adresse_lat__isnull=False,
        adresse_lng__isnull=False
    ).first()

    if figure:
        # Si l'adresse formatée est disponible
        if figure.adresse_formatted:
            parts = figure.adresse_formatted.split(',')
            if len(parts) >= 2:
                location = parts[-1].strip()
                if len(location) > 3 and not location[0].isdigit():
                    # Stocker pour la prochaine fois
                    user.location = location
                    user.save()
                    return location

        # Si on a des coordonnées, utiliser Mapbox
        try:
            import requests
            from django.conf import settings
            url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{figure.adresse_lng},{figure.adresse_lat}.json?access_token={settings.MAPBOX_TOKEN}&language=fr"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                for feature in data.get('features', []):
                    if 'country' in feature.get('place_type', []):
                        location = feature.get('text', '')
                        if location:
                            user.location = location
                            user.save()
                            return location
        except:
            pass

    # 3. Fallback : utiliser la région depuis get_region_utilisateur
    from .views import get_region_utilisateur
    region_info = get_region_utilisateur(user)
    return region_info.get('pays', 'france')


def est_mineur(user):
    """
    Détermine si un utilisateur est mineur selon la législation de sa localisation
    """
    if not user.birth_date:
        return False

    location = get_user_location(user)
    age_majorite = get_age_majorite(location)

    from datetime import date
    today = date.today()
    age = today.year - user.birth_date.year - (
            (today.month, today.day) < (user.birth_date.month, user.birth_date.day)
    )

    return age < age_majorite

def get_type_sol_auto(region, pays, continent):
    """
    Retourne le type de sol avec une approche hiérarchique :
    1. D'abord par région (le plus précis)
    2. Puis par pays
    3. Puis par continent
    4. Enfin par défaut
    """
    # Niveau 1 : Région
    if region in SOL_PAR_REGION:
        logger.debug(f"🔍 Type de sol trouvé par région: {region} → {SOL_PAR_REGION[region]}")

        return SOL_PAR_REGION[region]

    # Niveau 2 : Pays
    pays_sols = {
        'france': 'limoneux',
        'italy': 'calcaire',
        'italia': 'calcaire',
        'spain': 'calcaire',
        'españa': 'calcaire',
        'germany': 'limoneux',
        'deutschland': 'limoneux',
        'china': 'loess',
        'chine': 'loess',
        'république populaire de chine': 'loess',
        'japan': 'volcanique',
        'japon': 'volcanique',
        'india': 'latéritique',
        'inde': 'latéritique',
        'usa': 'limoneux',
        'united states': 'limoneux',
        'canada': 'tourbeux',
        'brazil': 'latéritique',
        'brésil': 'latéritique',
        'australia': 'lateritique',
        'australie': 'lateritique',
        'egypt': 'alluvial',
        'egypte': 'alluvial',
        'south africa': 'calcaire',
        'afrique du sud': 'calcaire',
        'morocco': 'calcaire',
        'maroc': 'calcaire',
        'tunisia': 'calcaire',
        'tunisie': 'calcaire',
        'greece': 'calcaire',
        'turkey': 'calcaire',
        'türkiye': 'calcaire',
        'mexico': 'volcanique',
        'méxique': 'volcanique',
    }

    if pays and pays.lower() in pays_sols:
        logger.debug(f"🔍 Type de sol trouvé par pays: {pays} → {pays_sols[pays.lower()]}")

        return pays_sols[pays.lower()]

    # Niveau 3 : Continent
    continent_sols = {
        'europe': 'limoneux',
        'asie': 'limoneux',
        'amerique': 'limoneux',
        'afrique': 'latéritique',
        'oceanie': 'lateritique',
        'arctique': 'tourbeux',
        'antarctique': 'glaciaire',
    }

    if continent and continent.lower() in continent_sols:
        logger.debug(f"🔍 Type de sol trouvé par continent: {continent} → {continent_sols[continent.lower()]}")

        return continent_sols[continent.lower()]

    # Niveau 4 : Par défaut
    logger.warning(f"⚠️ Aucun type de sol trouvé pour région={region}, pays={pays}, continent={continent} → 'autre'")

    return 'autre'


def verifier_email_academique(email):
    """
    Vérifie si l'email est académique (international)
    Retourne True si académique, False sinon
    """
    # Domaines académiques internationaux
    domaines_academiques = [
        # France
        '.edu.fr', '.ac-', '.academy',
        '.universite', '.univ-', '.university',
        '.ens-', '.ecole', '.lycee', '.college',
        '.sup', '.sup.fr', '.gouv', '.ministere',
        '.rectorat', '.academie',
        # UK
        '.ac.uk', '.sch.uk', '.school.uk',
        # USA / Canada
        '.edu', '.k12', '.school', '.k12.ca.us',
        # International
        '.ac.', '.sch.', '.school.',
        '.education', '.campus', '.institution',
        '.learning', '.academy',
        # Belgique
        '.be', '.ac.be',
        # Suisse
        '.ch', '.ac.ch',
        # Luxembourg
        '.lu',
        # Québec
        '.qc.ca', '.csmb.qc.ca',
    ]

    email_lower = email.lower()

    for domaine in domaines_academiques:
        if domaine in email_lower:
            return True

    return False


from difflib import get_close_matches
import requests
from django.core.cache import cache
from django.conf import settings


# ============================================================
# NIVEAU 1 : CACHE DE LA RÉGION (durée : 24h)
# ============================================================
def get_region_utilisateur(user, figure=None):
    """
    Retourne le continent, pays et région de l'utilisateur
    Version avec cache 24h pour éviter les appels API Mapbox répétés
    """
    # 🔥 CACHE CLÉ
    if figure:
        cache_key = f"region_user_{user.id}_figure_{figure.id}"
    else:
        cache_key = f"region_user_{user.id}"

    # Vérifier le cache
    cached_result = cache.get(cache_key)
    if cached_result:
        logger.debug(f"📦 Cache région HIT pour {user.username}")

        return cached_result

    logger.debug(f"🔄 Cache région MISS pour {user.username} - Appel API...")


    from django.conf import settings
    import requests

    # Valeurs par défaut
    continent = 'europe'
    pays = 'France'
    region = 'iledefrance'
    saison = get_saison_actuelle()

    # Récupérer la figure
    if figure is None:
        figure = user.geometricfigure_set.filter(adresse_lat__isnull=False).first()

    if figure and figure.adresse_lat and figure.adresse_lng:
        try:
            url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{figure.adresse_lng},{figure.adresse_lat}.json?access_token={settings.MAPBOX_TOKEN}&language=fr"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                features = data.get('features', [])

                for feature in features:
                    place_type = feature.get('place_type', [])
                    text = feature.get('text', '')

                    if 'country' in place_type:
                        pays = text
                    if 'region' in place_type:
                        # ✅ Normaliser la région
                        region_brute = text.lower().replace(' ', '-').replace("'", '-')
                        region = region_brute

                        # ✅ Mapper vers les régions de la base
                        if region_brute in REGION_MAPPING:
                            region = REGION_MAPPING[region_brute]
                        else:
                            # Essayer une correspondance partielle
                            for key, value in REGION_MAPPING.items():
                                if key in region_brute or region_brute in key:
                                    region = value
                                    logger.debug(f"🔍 Mapping partiel : '{region_brute}' → '{region}'")

                                    break

                # Déterminer le continent
                lat = figure.adresse_lat
                lng = figure.adresse_lng

                if lat > 66.5:
                    continent = 'arctique'
                elif lat < -66.5:
                    continent = 'antarctique'
                elif lat > 35:
                    if lng > -10 and lng < 40:
                        continent = 'europe'
                    elif lng > 40 and lng < 150:
                        continent = 'asie'
                    elif lng > -130 and lng < -60:
                        continent = 'amerique'
                    else:
                        continent = 'europe'
                elif lat > 23.5:
                    if lng > -120 and lng < -60:
                        continent = 'amerique'
                    elif lng > 0 and lng < 50:
                        continent = 'afrique'
                    elif lng > 50 and lng < 150:
                        continent = 'asie'
                    else:
                        continent = 'europe'
                elif lat > -23.5:
                    if lng > -130 and lng < -30:
                        continent = 'amerique'
                    elif lng > -30 and lng < 50:
                        continent = 'afrique'
                    elif lng > 50 and lng < 150:
                        continent = 'asie'
                    elif lng > 150 and lng < 180:
                        continent = 'oceanie'
                    else:
                        continent = 'europe'
                elif lat > -35:
                    if lng > -80 and lng < -30:
                        continent = 'amerique'
                    elif lng > 150 and lng < 180:
                        continent = 'oceanie'
                    else:
                        continent = 'oceanie'
                else:
                    if lng > 150 and lng < 180:
                        continent = 'oceanie'
                    elif lng > -80 and lng < -30:
                        continent = 'amerique'
                    else:
                        continent = 'oceanie'

        except Exception as e:
            logger.error(f"❌ ERREUR géocodage: {type(e).__name__}: {e}")


    resultat = {
        'continent': continent,
        'pays': pays,
        'region': region,
        'saison': saison,
    }

    # 🔥 ENREGISTRER DANS LE CACHE (24 heures)
    cache.set(cache_key, resultat, 60 * 60 * 24)
    logger.info(f"✅ Cache région enregistré pour {user.username}")


    return resultat


# ============================================================
# NIVEAU 2 : CACHE DE LA MÉTÉO (durée : 10 min)
# ============================================================
def get_meteo_cached(lat, lng, figure_id=None):
    """
    Récupère la météo avec cache 10 minutes
    """
    cache_key = f"meteo_{lat}_{lng}_{figure_id}" if figure_id else f"meteo_{lat}_{lng}"

    # Vérifier le cache
    meteo = cache.get(cache_key)
    if meteo:
        logger.debug(f"📦 Cache météo HIT pour lat={lat}, lng={lng}")

        return meteo

    logger.debug(f"🔄 Cache météo MISS - Appel API OpenWeatherMap...")


    try:
        api_key = settings.OPENWEATHER_API_KEY
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&units=metric&lang=fr&appid={api_key}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            meteo = {
                'temperature': round(data['main']['temp'], 1),
                'conditions': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'rain': data.get('rain', {}).get('1h', 0),
                'feels_like': round(data['main']['feels_like'], 1),
            }
            # 🔥 ENREGISTRER DANS LE CACHE (10 minutes)
            cache.set(cache_key, meteo, 600)
            logger.info(f"✅ Cache météo enregistré: {meteo['temperature']}°C")

            return meteo
        else:
            logger.error(f"❌ Erreur météo: {response.status_code}")

            return None
    except Exception as e:
        logger.error(f"❌ Erreur météo: {e}")

        return None


def get_saison_actuelle():
    """Retourne la saison actuelle basée sur la date et l'hémisphère"""
    from datetime import date
    mois = date.today().month

    # Hémisphère nord par défaut (ajuster selon coordonnées)
    if 3 <= mois <= 5:
        return 'printemps'
    elif 6 <= mois <= 8:
        return 'ete'
    elif 9 <= mois <= 11:
        return 'automne'
    else:
        return 'hiver'

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('vegetables_fruits:profile')
    template_name = 'vegetables_fruits/creation_compte.html'

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)

        if not user.tutoriel_termine:
            return redirect('vegetables_fruit:tutoriel')

        from datetime import date

        # Activer mode junior si mineur
        if user.birth_date:
            age = (date.today() - user.birth_date).days // 365
            if age < 18:
                user.mode_junior = True
                user.save()
                Eleve.objects.get_or_create(user=user)

        # Redirection selon profil
        if user.is_enseignant:
            return redirect('vegetables_fruits:dashboard_enseignant')

        return redirect('vegetables_fruits:profile')


def index(request):
    legumes = Vegetable.objects.all()
    fruits = Fruit.objects.all()
    return render(request, 'vegetables_fruits/index.html', {'legumes': legumes, 'fruits': fruits})


def connexion(request):

    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Vous avez été déconnecté.")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'vegetables_fruits/connexion.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie !")

            # ✅ VÉRIFIER LE CONSENTEMENT PARENTAL
            from .models import ConsentementRGPD
            try:
                consentement = user.consentements.filter(est_mineur=True).first()
                if consentement and consentement.est_bloquant():
                    messages.warning(
                        request,
                        "🔒 Votre compte est en attente de validation parentale. "
                        "Vos parents doivent valider votre inscription."
                    )
                    logout(request)
                    return redirect('vegetables_fruits:consentement_parental_attente')
            except ConsentementRGPD.DoesNotExist:
                pass
            except Exception as e:
                logger.error(f"Erreur vérification consentement : {e}")


            # ✅ Vérification Tutoriel
            if not user.tutoriel_termine:
                return redirect('vegetables_fruits:tutoriel')

            # ✅ Vérification Enseignant
            if user.is_enseignant:
                return redirect('vegetables_fruits:dashboard_enseignant')

            # ✅ Vérification : mineur ou majeur
            if est_mineur(user):
                # Mineur en classe → dashboard élève
                if hasattr(user, 'profil_eleve') and user.profil_eleve and user.profil_eleve.classe:
                    return redirect('vegetables_fruits:dashboard_eleve')
                # Mineur particulier → dashboard junior
                else:
                    return redirect('vegetables_fruits:dashboard_junior')
            else:
                return redirect('vegetables_fruits:dashboard_particulier')
        else:
            messages.error(request, "Identifiants incorrects. Veuillez réessayer.")
            return render(request, 'vegetables_fruits/connexion.html')

    return render(request, 'vegetables_fruits/connexion.html')


def deconnexion(request):
    logout(request)
    return redirect('vegetables_fruits:index')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'vegetables_fruits/password_reset.html'
    email_template_name = 'vegetables_fruits/password_reset_email.html'
    subject_template_name = 'vegetables_fruits/password_reset_subject.txt'
    success_url = reverse_lazy('vegetables_fruits:password_reset_done')
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'vegetables_fruits/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'vegetables_fruits/password_reset_confirm.html'
    success_url = reverse_lazy('vegetables_fruits:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'vegetables_fruits/password_reset_complete.html'


@login_required(login_url='vegetables_fruits:login')
def profile(request):
    user = request.user
    context = {
        'user': user,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    }

    from datetime import date
    if user.birth_date:
        age = (date.today() - user.birth_date).days // 365
        context['mineur'] = age < 18
    else:
        context['mineur'] = False

    if hasattr(user, 'drawings'):
        drawings = user.drawings.all().order_by('-created_at')
        context.update({
            'drawings': drawings[:5],
            'drawings_count': drawings.count(),
            'has_drawings': drawings.exists(),
        })
    messages.info(request, f"Bienvenue sur votre profil, {user.username} !")
    return render(request, 'vegetables_fruits/profile.html', context)


def creation_compte(request):
    try:
        if request.user.is_authenticated:
            messages.info(request, "Vous êtes déjà connecté!")
            return redirect('vegetables_fruits:index')

        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            logger.debug("Formulaire reçu: %s", request.POST)

            if form.is_valid():
                try:
                    from datetime import date
                    from .models import Eleve

                    user = form.save(commit=False)
                    is_enseignant = form.cleaned_data.get('is_enseignant', False)

                    # ✅ VÉRIFICATION ENSEIGNANT (avec domaines internationaux)
                    if is_enseignant:
                        email = form.cleaned_data.get('email')

                        # Domaines académiques internationaux
                        domaines_academiques = [
                            # France
                            '.edu', '.edu.fr', '.ac-', '.academy',
                            '.universite', '.univ-', '.university',
                            '.ens-', '.ecole', '.lycee', '.college',
                            '.sup', '.sup.fr', '.gouv', '.ministere',
                            '.rectorat', '.academie',
                            # UK
                            '.ac.uk', '.sch.uk', '.school.uk',
                            # USA / Canada
                            '.edu', '.k12', '.school', '.k12.ca.us',
                            # International
                            '.edu', '.ac.', '.sch.', '.school.',
                            '.education', '.campus', '.institution',
                            # Belgique / Suisse
                            '.be', '.ch', '.lu',
                        ]

                        # Extraire le domaine
                        email_lower = email.lower()
                        domaine_trouve = False

                        for domaine in domaines_academiques:
                            if domaine in email_lower:
                                domaine_trouve = True
                                break

                        if not domaine_trouve:
                            messages.error(request,
                                           "❌ Pour vous inscrire en tant qu'enseignant, veuillez utiliser une adresse email académique "
                                           "(ex: nom@universite.fr, nom@ac-ville.fr, nom@ac.uk, nom@edu, nom@school.be)"
                                           )
                            return render(request, 'vegetables_fruits/creation_compte.html', {'form': form})

                        user.is_enseignant = True
                        messages.success(request,
                                         "✅ Bienvenue enseignant ! Vous pouvez maintenant créer des classes et gérer vos élèves.")

                    user.save()

                    # ✅ GESTION DU CONSENTEMENT PARENTAL
                    from datetime import date
                    from .models import ConsentementRGPD
                    import secrets

                    if user.birth_date:
                        age = (date.today() - user.birth_date).days // 365

                        if age < 15:
                            # 🔒 CONSENTEMENT OBLIGATOIRE (-15 ans)
                            consentement = ConsentementRGPD.objects.create(
                                utilisateur=user,
                                est_mineur=True,
                                type_consentement='obligatoire',
                                statut='en_attente',
                                ip_address=get_client_ip(request),
                                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                            )

                            # ✅ STOCKER L'ID DANS LA SESSION
                            request.session['consentement_id'] = consentement.id

                            logger.debug(f"🔒 Consentement parental obligatoire pour {user.username} ({age} ans)")


                            messages.warning(
                                request,
                                "🔒 Pour les mineurs de moins de 15 ans, un consentement parental est obligatoire. "
                                "Demandez à vos parents de valider votre inscription via le lien envoyé par email."
                            )

                            # ✅ Rediriger vers la page d'attente (sans connecter l'utilisateur)
                            return redirect('vegetables_fruits:consentement_parental_attente')

                        elif age < 18:
                            # ⚠️ CONSENTEMENT RECOMMANDÉ (15-17 ans)
                            consentement = ConsentementRGPD.objects.create(
                                utilisateur=user,
                                est_mineur=True,
                                type_consentement='recommande',
                                statut='en_attente',
                                ip_address=get_client_ip(request),
                                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                            )

                            logger.warning(f"⚠️ Consentement parental recommandé pour {user.username} ({age} ans)")


                            messages.info(
                                request,
                                "ℹ️ Un email a été envoyé à vos parents pour information. "
                                "Vous pouvez utiliser l'application normalement."
                            )

                        else:
                            # ✅ MAJEUR (18+)
                            consentement = ConsentementRGPD.objects.create(
                                utilisateur=user,
                                est_mineur=False,
                                type_consentement='personnel',
                                statut='valide',
                                ip_address=get_client_ip(request),
                                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                            )

                    # ✅ Gestion du mode Junior + classe
                    if user.birth_date:
                        age = (date.today() - user.birth_date).days // 365

                        if age < 18:
                            user.mode_junior = True
                            user.save()

                            # ✅ Si le mineur a renseigné un code de classe → créer Eleve avec la classe
                            est_dans_classe = form.cleaned_data.get('est_dans_classe', False)
                            classe_obj = form.cleaned_data.get('classe_obj', None)

                            if est_dans_classe and classe_obj:
                                # ✅ Créer le profil Eleve AVEC la classe
                                eleve, created = Eleve.objects.get_or_create(user=user)
                                eleve.classe = classe_obj
                                eleve.save()
                                logger.info(
                                    "Profil élève créé pour le mineur %s dans la classe %s",
                                    user.username, classe_obj.nom
                                )
                            # ⚠️ Sinon : NE PAS créer de profil Eleve (mineur particulier)

                    logger.info("Nouvel utilisateur créé: %s (enseignant=%s)", user.username, user.is_enseignant)

                    user = authenticate(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1']
                    )

                    if user is not None:
                        login(request, user)
                        messages.success(request, f'Bienvenue {user.username}! Votre compte a été créé avec succès.')

                        if user.is_enseignant:
                            return redirect('vegetables_fruits:dashboard_enseignant')
                        return redirect('vegetables_fruits:profile')
                    else:
                        messages.error(request, "Échec de l'authentification automatique.")
                        return redirect('login')

                except Exception as e:
                    logger.error("Erreur lors de la création du compte: %s", str(e))
                    messages.error(request, "Une erreur technique est survenue.")
                    return render(request, 'vegetables_fruits/creation_compte.html', {'form': form})
            else:
                logger.warning("Erreurs de formulaire: %s", form.errors)
                messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
        else:
            form = CustomUserCreationForm()

        return render(request, 'vegetables_fruits/creation_compte.html', {'form': form})

    except Exception as e:
        logger.critical("Erreur critique: %s", str(e))
        messages.error(request, "Une erreur inattendue est survenue.")
        return redirect('vegetables_fruits:index')

@login_required
def draw_figure(request):
    # ⭐ VÉRIFICATION SI LE QUOTAS DE FIGURE N'EST PAS ATTEINT
    peut_creer, message = verifier_quota_parcelles(request.user)
    if not peut_creer:
        if message == 'limite':
            return redirect('vegetables_fruits:limite_parcelles')
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    if request.method == 'POST':
        form = FigureForm(request.POST)
        if form.is_valid():
            return redirect('vegetables_fruits:view_figure')
    else:
        form = FigureForm()
    return render(request, 'vegetables_fruits/draw/draw_interactive.html', {'form': form})


@csrf_exempt
@login_required
def save_figure(request):
    # VÉRIFICATION DU QUOTA
    peut_creer, message = verifier_quota_parcelles(request.user)
    if not peut_creer:
        if message == 'limite':
            return JsonResponse({'success': False, 'message': 'limite', 'redirect': True})
        return JsonResponse({'success': False, 'message': message, 'redirect': True})

    if request.method == 'POST':
        try:
            geojson_str = request.POST.get('geojson_data')
            type_terrain = request.POST.get('type_terrain_draw')
            nom = request.POST.get('nom')
            description = request.POST.get('description_draw')
            adresse = request.POST.get('adresse')
            adresse_lat_input = request.POST.get('address_lat')
            adresse_lng_input = request.POST.get('address_lng')
            adresse_formatted = request.POST.get('adresse_formatted')
            sol_mode = request.POST.get('sol_mode', 'manuel')
            logger.debug(f"sol_mode reçu : {sol_mode}")
            type_sol = request.POST.get('type_sol', '')
            logger.debug(f"{type_sol}")

            if sol_mode == 'auto':
                # Récupérer la région via la fonction existante
                region_info = get_region_utilisateur(request.user)
                region = region_info['region']
                logger.debug(f" Région detectée : {region}")

                # Assigner un type de sol par défaut selon la région
                sol_par_region = {
                    'provence': 'calcaire',
                    'iledefrance': 'limoneux',
                    'nord': 'argileux',
                    'alsace': 'limoneux',
                    'bretagne': 'argileux',
                    'aquitaine': 'sableux',
                }
                type_sol = sol_par_region.get(region, 'autre')
            else:
                type_sol = request.POST.get('type_sol', '')

            if not type_sol and sol_mode == 'auto':
                type_sol = 'limoneux'

            geojson_data = json.loads(geojson_str)

            # ⭐ CALCUL DES COORDONNÉES POUR LA MÉTÉO À PARTIR DU GEOJSON ⭐
            center_lat = None
            center_lng = None

            if geojson_data.get('features') and len(geojson_data['features']) > 0:
                geometry = geojson_data['features'][0].get('geometry', {})
                geom_type = geometry.get('type')
                coords = geometry.get('coordinates', [])

                if geom_type == 'Point':
                    if coords and len(coords) >= 2:
                        center_lng = coords[0]
                        center_lat = coords[1]
                        logger.debug(f"📍 Point - lat={center_lat}, lng={center_lng}")

                elif geom_type == 'Polygon':
                    if coords and coords[0] and len(coords[0]) > 0:
                        lats = [c[1] for c in coords[0]]
                        lngs = [c[0] for c in coords[0]]
                        center_lat = sum(lats) / len(lats)
                        center_lng = sum(lngs) / len(lngs)
                        logger.debug(f"🔷 Polygone - centre calculé: lat={center_lat}, lng={center_lng}")

                elif geom_type == 'LineString':
                    if coords and len(coords) > 0:
                        lats = [c[1] for c in coords]
                        lngs = [c[0] for c in coords]
                        center_lat = sum(lats) / len(lats)
                        center_lng = sum(lngs) / len(lngs)
                        logger.debug(f"📏 Ligne - centre calculé: lat={center_lat}, lng={center_lng}")

            # Utiliser les coordonnées calculées ou celles du formulaire
            final_lat = center_lat if center_lat is not None else (adresse_lat_input if adresse_lat_input else None)
            final_lng = center_lng if center_lng is not None else (adresse_lng_input if adresse_lng_input else None)

            logger.debug(f"🎯 Coordonnées finales: lat={final_lat}, lng={final_lng}")

            # Détection du type de géométrie pour le comptage de points
            geometry_type = None
            if geojson_data.get('features') and len(geojson_data['features']) > 0:
                geometry = geojson_data['features'][0].get('geometry', {})
                geometry_type = geometry.get('type')
                logger.debug(f"🎯 Type détecté: {geometry_type}")

            # Calcul du nombre de points selon le type
            nb_points = 0
            if geometry_type == 'Point':
                nb_points = 1
            elif geometry_type == 'Polygon':
                coords = geometry.get('coordinates', [[]])
                nb_points = len(coords[0]) if coords else 0
            elif geometry_type == 'LineString':
                coords = geometry.get('coordinates', [])
                nb_points = len(coords)

            figure = GeometricFigure(
                user=request.user,
                name=nom,
                figure_type=type_terrain,
                geojson_data=geojson_data,  # GeoJSON original NON modifié
                nb_points=nb_points,
                description=description,
                adresse=adresse,
                adresse_lat=final_lat,
                adresse_lng=final_lng,
                adresse_formatted=adresse_formatted
            )
            figure.save()

            # ✅ CRÉATION AUTOMATIQUE DE LA PARCELLE (SANS DOUBLON)
            parcelle = Parcelle.objects.filter(figure=figure, utilisateur=request.user).first()

            if parcelle:
                # ✅ Mettre à jour l'existante
                parcelle.nom = figure.name
                parcelle.surface_m2 = figure.surface_hectares * 10000 if figure.surface_hectares else 10
                parcelle.type_sol = type_sol
                parcelle.save()
                logger.debug(f"ℹ️ Parcelle mise à jour : {parcelle.nom} (figure {figure.id})")
            else:
                # ✅ Créer une nouvelle
                parcelle = Parcelle.objects.create(
                    figure=figure,
                    utilisateur=request.user,
                    nom=figure.name,
                    surface_m2=figure.surface_hectares * 10000 if figure.surface_hectares else 10,
                    type_sol=type_sol,
                )
                logger.info(f"✅ Parcelle créée : {parcelle.nom} (liée à figure {figure.id})")


            if hasattr(request.user, 'profil_eleve'):
                eleve = request.user.profil_eleve
                mettre_a_jour_progres_defi(request.user.profil_eleve, 'planter')
                verifier_competences(eleve)

            # Attribution des points pour mode junior
            if request.user.mode_junior and hasattr(request.user, 'profil_eleve'):
                request.user.profil_eleve.ajouter_points(10, action_type='creer_parcelle')

            if request.user.is_authenticated and hasattr(request.user, 'profil_eleve'):
                eleve = request.user.profil_eleve
                eleve.ajouter_points(10)
                messages.success(request, f"🎉 +10 points ! Tu as maintenant {eleve.points} points.")

            if hasattr(request.user, 'mode_junior') and request.user.mode_junior:
                from .models import ProgressionJunior
                progression, _ = ProgressionJunior.objects.get_or_create(user=request.user)
                progression.points += 10
                ancien_niveau = progression.niveau
                nouveau_niveau = progression.points // 100 + 1
                if nouveau_niveau > ancien_niveau:
                    messages.success(request, f"🎉 Félicitations ! Tu es passé au niveau {nouveau_niveau} ! 🎉")
                progression.niveau = nouveau_niveau
                progression.save()
                logger.debug(f"🏆 {request.user.username} - {progression.points} points (niveau {progression.niveau})")

            messages.success(request, f"Figure '{nom}' sauvegardée!")
            return redirect('vegetables_fruits:view_figure')

        except Exception as e:
            logger.error(f"❌ Erreur save_figure: {e}")
            messages.error(request, f"Erreur: {str(e)}")
            return redirect('vegetables_fruits:draw_figure')


@login_required
def save_terrain_figure(request):
    if request.method == 'POST':
        try:
            # Vérifier si c'est une requête JSON (AJAX) ou formulaire classique
            is_ajax = request.headers.get('Content-Type') == 'application/json'

            if is_ajax:
                # Traitement pour les requêtes JSON
                data = json.loads(request.body)
                type_terrain = data.get('type')
                nom = data.get('nom', "Figure terrain")
                culture = data.get('culture')
                description = data.get('description', '')
                points = data.get('points', [])
                figure_shape = data.get('figure_shape', 'polygon')
                rayon = data.get('circle_radius', 100)
                adresse = data.get('adresse', '')
                adresse_lat = data.get('adresse_lat')
                adresse_lng = data.get('adresse_lng')
                adresse_formatted = data.get('adresse_formatted', '')
            else:
                # Traitement pour les formulaires classiques
                type_terrain = request.POST.get('type_terrain')
                nom = request.POST.get('nom_terrain') or "Figure terrain"
                culture = request.POST.get('culture')
                description = request.POST.get('description_terrain')
                points_json = request.POST.get('terrain_coords')
                points = json.loads(points_json) if points_json else []
                figure_shape = request.POST.get('figure_shape', 'polygon')
                rayon = request.POST.get('circle_radius', 100)
                adresse = request.POST.get('adresse')
                adresse_lat = request.POST.get('adresse_lat')
                adresse_lng = request.POST.get('adresse_lng')
                adresse_formatted = request.POST.get('adresse_formatted')

            logger.debug(f"=== MODE TERRAIN ===")

            logger.debug(f"Type: {type_terrain}")

            logger.debug(f"Forme: {figure_shape}")

            logger.debug(f"Points reçus: {len(points)}")


            # Construction du GeoJSON
            if figure_shape == 'circle' and len(points) == 1:
                geojson_data = {
                    "type": "FeatureCollection",
                    "features": [{
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [points[0]['lng'], points[0]['lat']]
                        },
                        "properties": {
                            "radius": float(rayon),
                            "shape": "circle"
                        }
                    }]
                }
                nb_points = 1
            elif figure_shape == 'point' and len(points) == 1:
                geojson_data = {
                    "type": "FeatureCollection",
                    "features": [{
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [points[0]['lng'], points[0]['lat']]
                        },
                        "properties": {
                            "shape": "point"
                        }
                    }]
                }
                nb_points = 1
            else:
                # Polygone ou ligne
                if len(points) < 3:
                    if is_ajax:
                        return JsonResponse({'success': False, 'error': 'Au moins 3 points requis pour un polygone'})
                    else:
                        messages.error(request, "Au moins 3 points requis pour un polygone")
                        return redirect('vegetables_fruits:draw_figure')

                geojson_data = {
                    "type": "FeatureCollection",
                    "features": [{
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [[[p['lng'], p['lat']] for p in points]]
                        },
                        "properties": {
                            "shape": "polygon"
                        }
                    }]
                }
                nb_points = len(points)

            figure = GeometricFigure(
                user=request.user,
                name=nom,
                figure_type=type_terrain,
                geojson_data=geojson_data,
                nb_points=nb_points,
                description=description,
                adresse=adresse,
                adresse_lat=adresse_lat,
                adresse_lng=adresse_lng,
                adresse_formatted=adresse_formatted
            )
            figure.save()

            # ✅ CRÉATION AUTOMATIQUE DE LA PARCELLE (SANS DOUBLON)
            parcelle = Parcelle.objects.filter(figure=figure, utilisateur=request.user).first()

            if parcelle:
                # ✅ Mettre à jour l'existante
                parcelle.nom = figure.name
                parcelle.surface_m2 = figure.surface_hectares * 10000 if figure.surface_hectares else 10
                parcelle.save()
                logger.debug(f"ℹ️ Parcelle mise à jour : {parcelle.nom} (figure {figure.id})")

            else:
                # ✅ Créer une nouvelle
                parcelle = Parcelle.objects.create(
                    figure=figure,
                    utilisateur=request.user,
                    nom=figure.name,
                    surface_m2=figure.surface_hectares * 10000 if figure.surface_hectares else 10,
                )
                logger.info(f"✅ Parcelle créée : {parcelle.nom} (liée à figure {figure.id})")



            if culture:
                figure.crops = [{'culture': culture}]
                figure.save()

            # Réponse selon le type de requête
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': f"Figure terrain '{nom}' sauvegardée!",
                    'figure_id': figure.id
                })
            else:
                messages.success(request, f"Figure terrain '{nom}' sauvegardée!")
                from django.urls import reverse
                return redirect(reverse('view_figure'))

        except Exception as e:
            logger.error(f"❌ Erreur: {str(e)}")

            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)})
            else:
                messages.error(request, f"Erreur: {str(e)}")
                return redirect('vegetables_fruits:draw_figure')

    return redirect('vegetables_fruits:draw_figure')


@login_required
def view_figure(request):
    figures_list = GeometricFigure.objects.filter(user=request.user).select_related('user').order_by('-created_at')
    paginator = Paginator(figures_list, 12)
    page_number = request.GET.get('page')
    figures = paginator.get_page(page_number)

    # 🌤️ Récupérer la météo pour chaque parcelle
    for figure in figures:
        figure.meteo = get_meteo_for_figure(figure)

    return render(request, 'vegetables_fruits/draw/view.html', {
        'figures': figures,
        'total_count': figures_list.count()
    })


@login_required
def ajouter_chronologie(request):
    """Ajoute une chronologie pour une culture"""
    if request.method == 'POST':
        figure_id = request.POST.get('figure_id')
        culture_nom = request.POST.get('culture_nom')
        culture_emoji = request.POST.get('culture_emoji', '🌱')
        date_semis = request.POST.get('date_semis')
        jours_recolte = int(request.POST.get('jours_recolte', 0))

        # ✅ Si pas fourni par le formulaire, chercher la vraie durée
        if jours_recolte <= 0:
            from .models import Fruit, Vegetable, Culture as CultureModel
            fruit = Fruit.objects.filter(nom__iexact=culture_nom).first()
            if fruit and fruit.jours_recolte:
                jours_recolte = fruit.jours_recolte
            else:
                veg = Vegetable.objects.filter(nom__iexact=culture_nom).first()
                if veg and veg.jours_recolte:
                    jours_recolte = veg.jours_recolte
                else:
                    cult = CultureModel.objects.filter(nom__iexact=culture_nom).first()
                    if cult:
                        if cult.jours_pousse:
                            jours_recolte = cult.jours_pousse
                        elif cult.duree_culture_max_jours:
                            jours_recolte = cult.duree_culture_max_jours
                    if jours_recolte <= 0:
                        jours_recolte = 90

        from datetime import date, timedelta

        figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)
        date_semis_date = date.fromisoformat(date_semis)
        date_recolte = date_semis_date + timedelta(days=jours_recolte)


        chrono = ChronologieCulture.objects.create(
            figure=figure,
            culture_nom=culture_nom,
            culture_emoji=culture_emoji,
            date_semis=date_semis_date,
            date_recolte_prevue=date_recolte,
        )
        chrono.calculer_progression()

        messages.success(request, f"Chronologie créée pour {culture_emoji} {culture_nom} !")
        return redirect('vegetables_fruits:figure_detail', figure_id=figure.id)

    return redirect('vegetables_fruits:view_figure')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import BesoinsEau, Parcelle, Culture, DigestMeteo


@login_required
def ajuster_besoins_annuels(request):
    from .models import Parcelle, BesoinsEau, GeometricFigure
    from django.contrib import messages
    from django.urls import reverse

    user = request.user
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    # ✅ Récupérer figure_id ou parcelle_id
    figure_id = request.GET.get('figure_id')
    parcelle_id = request.GET.get('parcelle_id')
    selected_parcelle = None

    if figure_id:
        try:
            figure = GeometricFigure.objects.get(id=figure_id, user=user)
            selected_parcelle = Parcelle.objects.get(figure=figure, utilisateur=user)
        except (GeometricFigure.DoesNotExist, Parcelle.DoesNotExist):
            selected_parcelle = None
    elif parcelle_id:
        try:
            selected_parcelle = parcelles.get(id=parcelle_id)
        except Parcelle.DoesNotExist:
            selected_parcelle = None

    if not selected_parcelle:
        messages.warning(request, "Veuillez sélectionner une parcelle d'abord.")
        return redirect('vegetables_fruits:besoins_eau')

    # Récupérer les besoins de cette parcelle uniquement
    besoins = BesoinsEau.objects.filter(parcelle=selected_parcelle)

    total_besoins = sum([
        besoin.besoin_litres_par_m2 * besoin.parcelle.surface_m2 * 52
        for besoin in besoins
    ])

    # Traitement POST
    if request.method == 'POST':
        action = request.POST.get('action')
        ajustement = request.POST.get('ajustement', '1.0')

        try:
            ajustement = float(ajustement)
            if action == 'parcelle':
                # Appliquer à cette parcelle
                for besoin in besoins:
                    besoin.besoin_litres_par_m2 = besoin.besoin_litres_par_m2 * ajustement
                    besoin.save()
                messages.success(request, f"✅ Ajustement appliqué à la parcelle {selected_parcelle.nom}.")
                return redirect(f"{reverse('vegetables_fruits:autosuffisance')}?parcelle_id={selected_parcelle.id}")
            elif action == 'toutes':
                # Appliquer à toutes les parcelles
                for besoin in BesoinsEau.objects.filter(parcelle__in=parcelles):
                    besoin.besoin_litres_par_m2 = besoin.besoin_litres_par_m2 * ajustement
                    besoin.save()
                messages.success(request, "✅ Ajustement appliqué à toutes les parcelles.")
                return redirect(f"{reverse('vegetables_fruits:autosuffisance')}?parcelle_id={selected_parcelle.id}")
        except ValueError:
            messages.error(request, "Veuillez entrer un nombre valide.")

    return render(request, 'vegetables_fruits/ajuster_besoins.html', {
        'selected_parcelle': selected_parcelle,
        'besoins': besoins,
        'total_besoins': total_besoins,
    })



# ===== FONCTION D'ENRICHISSEMENT RÉUTILISABLE =====
# ⚠️ PLACÉE ICI pour être accessible par toutes les vues
def enrichir_culture(crop):
    """Enrichit une culture avec tous les détails disponibles"""
    crop_copy = crop.copy()


    if 'fruit_id' in crop:
        try:
            fruit = Fruit.objects.get(id=crop['fruit_id'])

            # ✅ Récupérer les données de taille
            nom_lower = fruit.nom.lower()
            taille = {}

            # Recherche flexible
            for cle, valeurs in TAILLES_CULTURES.items():
                if cle in nom_lower or nom_lower in cle:
                    taille = valeurs
                    logger.info(f" ✅ Taille trouvée pour {fruit.nom} via '{cle}'")

                    break

            crop_copy['details'] = {
                'id': fruit.id,
                'nom': fruit.nom,
                'couleur': fruit.couleur,
                'prix': fruit.prix,
                'saison': fruit.saison,
                'provenance': fruit.provenance,
                'type': 'fruit',
                'semis_interieur': fruit.semis_interieur or '',
                'semis_exterieur': fruit.semis_exterieur or '',
                'jours_levée': fruit.jours_levée or 0,
                'jours_recolte': fruit.jours_recolte or 0,
                'temperature_min': fruit.temperature_min or 0,
                'profondeur_semis': str(fruit.profondeur_semis) if fruit.profondeur_semis else '',
                'espacement': fruit.espacement or '',
                'pollinisation_type': fruit.pollinisation_type or '',
                'besoin_pollinisateur': fruit.besoin_pollinisateur,
                'pollinisateurs_conseilles': fruit.pollinisateurs_conseilles or '',
                'distance_pollinisation': fruit.distance_pollinisation or 0,
                'periode_floraison': fruit.periode_floraison or '',
                'conseils_pollinisation': fruit.conseils_pollinisation or '',
                'conseils_preparation_sol': fruit.conseils_preparation_sol or '',
                'conseils_apres_recolte': fruit.conseils_apres_recolte or '',
                'rotation_conseillee': fruit.rotation_conseillee or '',
                'rotation_deconseillee': fruit.rotation_deconseillee or '',
                'plantation': fruit.plantation or '',
                'recolte': fruit.recolte or '',
                # ✅ TAILLES
                'hauteur': taille.get('hauteur', ''),
                'largeur': taille.get('largeur', ''),
                'espacement': taille.get('espacement', ''),
                'espacement_rangs': taille.get('espacement_rangs', ''),
            }
        except Fruit.DoesNotExist:
            crop_copy['details'] = None

    elif 'vegetable_id' in crop:
        try:
            vegetable = Vegetable.objects.get(id=crop['vegetable_id'])

            # ✅ Récupérer les données de taille
            nom_lower = vegetable.nom.lower()
            taille = {}

            # Recherche flexible
            for cle, valeurs in TAILLES_CULTURES.items():
                if cle in nom_lower or nom_lower in cle:
                    taille = valeurs
                    logger.info(f" ✅ Taille trouvée pour {vegetable.nom} via '{cle}'")

                    break

            crop_copy['details'] = {
                'id': vegetable.id,
                'nom': vegetable.nom,
                'couleur': vegetable.couleur,
                'prix': vegetable.prix,
                'saison': vegetable.saison,
                'provenance': vegetable.provenance,
                'type': 'vegetable',
                'semis_interieur': vegetable.semis_interieur or '',
                'semis_exterieur': vegetable.semis_exterieur or '',
                'jours_levée': vegetable.jours_levée or 0,
                'jours_recolte': vegetable.jours_recolte or 0,
                'temperature_min': vegetable.temperature_min or 0,
                'profondeur_semis': str(vegetable.profondeur_semis) if vegetable.profondeur_semis else '',
                'espacement': vegetable.espacement or '',
                'pollinisation_type': vegetable.pollinisation_type or '',
                'besoin_pollinisateur': vegetable.besoin_pollinisateur,
                'pollinisateurs_conseilles': vegetable.pollinisateurs_conseilles or '',
                'distance_pollinisation': vegetable.distance_pollinisation or 0,
                'periode_floraison': vegetable.periode_floraison or '',
                'conseils_pollinisation': vegetable.conseils_pollinisation or '',
                'conseils_preparation_sol': vegetable.conseils_preparation_sol or '',
                'conseils_apres_recolte': vegetable.conseils_apres_recolte or '',
                'rotation_conseillee': vegetable.rotation_conseillee or '',
                'rotation_deconseillee': vegetable.rotation_deconseillee or '',
                'plantation': vegetable.plantation or '',
                'recolte': vegetable.recolte or '',
                # ✅ TAILLES
                'hauteur': taille.get('hauteur', ''),
                'largeur': taille.get('largeur', ''),
                'espacement': taille.get('espacement', ''),
                'espacement_rangs': taille.get('espacement_rangs', ''),
            }
        except Vegetable.DoesNotExist:
            crop_copy['details'] = None
    else:
        crop_copy['details'] = None

    return crop_copy

def enrichir_culture_depuis_obj(crop, obj, type_obj):
    """
    Version rapide d'enrichir_culture : reçoit l'objet Fruit/Vegetable
    déjà chargé au lieu de faire une requête DB.

    type_obj : 'fruit' ou 'vegetable'
    """
    crop_copy = crop.copy()


    if obj is None:
        crop_copy['details'] = None
        return crop_copy

    nom_lower = obj.nom.lower()
    taille = {}
    for cle, valeurs in TAILLES_CULTURES.items():
        if cle in nom_lower or nom_lower in cle:
            taille = valeurs
            break

    crop_copy['details'] = {
        'id': obj.id,
        'nom': obj.nom,
        'couleur': obj.couleur,
        'prix': obj.prix,
        'saison': obj.saison,
        'provenance': obj.provenance,
        'type': type_obj,
        'semis_interieur': obj.semis_interieur or '',
        'semis_exterieur': obj.semis_exterieur or '',
        'jours_levée': obj.jours_levée or 0,
        'jours_recolte': obj.jours_recolte or 0,
        'temperature_min': obj.temperature_min or 0,
        'profondeur_semis': str(obj.profondeur_semis) if obj.profondeur_semis else '',
        'espacement': obj.espacement or '',
        'pollinisation_type': obj.pollinisation_type or '',
        'besoin_pollinisateur': obj.besoin_pollinisateur,
        'pollinisateurs_conseilles': obj.pollinisateurs_conseilles or '',
        'distance_pollinisation': obj.distance_pollinisation or 0,
        'periode_floraison': obj.periode_floraison or '',
        'conseils_pollinisation': obj.conseils_pollinisation or '',
        'conseils_preparation_sol': obj.conseils_preparation_sol or '',
        'conseils_apres_recolte': obj.conseils_apres_recolte or '',
        'rotation_conseillee': obj.rotation_conseillee or '',
        'rotation_deconseillee': obj.rotation_deconseillee or '',
        'plantation': obj.plantation or '',
        'recolte': obj.recolte or '',
        'hauteur': taille.get('hauteur', ''),
        'largeur': taille.get('largeur', ''),
        'espacement': taille.get('espacement', ''),
        'espacement_rangs': taille.get('espacement_rangs', ''),
    }
    return crop_copy


def get_conseils_culture(culture_nom):
    from .models import Culture, Vegetable, Fruit, Variete, ConseilsTypeCulture
    from difflib import get_close_matches

    if not culture_nom:
        return None

    nom_propre = culture_nom.strip()


    if not nom_propre:
        return None

    culture_obj = None

    # 1. Chercher la variété pour remonter à la culture
    variete = Variete.objects.filter(nom__iexact=nom_propre).select_related('culture').first()
    if variete and variete.culture:
        nom_propre = variete.culture.nom

    # 2. Recherche exacte
    for model in [Culture, Vegetable, Fruit]:
        culture_obj = model.objects.filter(
            nom__iexact=nom_propre
        ).select_related('famille').first()
        if culture_obj:
            break

    # 3. Recherche floue
    if not culture_obj:
        noms_dispo = get_tous_les_noms_cultures()
        matches = get_close_matches(nom_propre, noms_dispo, n=1, cutoff=0.85)
        if matches:
            for model in [Culture, Vegetable, Fruit]:
                culture_obj = model.objects.filter(
                    nom__iexact=matches[0]
                ).select_related('famille').first()
                if culture_obj:
                    break

    # 4. Fallback générique (si la culture n'est pas du tout en base)
    if not culture_obj:
        return {
            'nom': nom_propre,
            'famille': None,
            'famille_emoji': '🌱',
            'est_generique': True,
            'conseils_generaux': f"🌱 **{nom_propre}** n'a pas encore de fiche détaillée. Renseigne-toi sur ses besoins spécifiques.",
            'temperature_min': None, 'temperature_optimale_min': None, 'temperature_optimale_max': None,
            'temperature_max': None,
            'duree_culture_min_jours': None, 'duree_culture_max_jours': None, 'methode_plantation': None,
            'hivernage': None,
            'conseils_climat': None, 'conseils_plantation': None, 'conseils_arrosage': None,
            'conseils_fertilisation': None,
            'conseils_protection': None, 'conseils_recolte': None, 'conseils_conservation': None,
        }

    # ✅ NOUVEAU : On détermine le type agronomique
    type_agro = None

    # On utilise le type_culture du modèle Culture s'il existe
    if hasattr(culture_obj, 'type_culture') and culture_obj.type_culture:
        t = culture_obj.type_culture.lower()
        if 'fruit' in t:
            type_agro = 'arbre_fruitier'  # Par défaut, on suppose que c'est un arbre
        elif 'legume' in t:
            type_agro = 'legume_fruit'  # Par défaut
        elif 'aromatique' in t:
            type_agro = 'aromatique'
        elif 'fleur' in t:
            type_agro = 'fleur'
    else:
        # Si c'est un Fruit (modèle Fruit) -> Arbre
        if isinstance(culture_obj, Fruit):
            type_agro = 'arbre_fruitier'
        # Si c'est un Vegetable -> Légume
        elif isinstance(culture_obj, Vegetable):
            type_agro = 'legume_feuille'

    # ✅ On va chercher les conseils dans la nouvelle table !
    conseils_type = ConseilsTypeCulture.objects.filter(type_culture=type_agro).first()

    # Fallback si le type n'est pas trouvé dans la table
    if not conseils_type:
        conseils_type = ConseilsTypeCulture.objects.filter(type_culture='arbre_fruitier').first()

    CHAMPS_A_FUSIONNER = [
        'temperature_min', 'temperature_optimale_min', 'temperature_optimale_max', 'temperature_max',
        'duree_culture_min_jours', 'duree_culture_max_jours', 'methode_plantation', 'hivernage',
        'conseils_climat', 'conseils_plantation', 'conseils_arrosage', 'conseils_fertilisation',
        'conseils_protection', 'conseils_recolte', 'conseils_conservation',
    ]

    conseils = {
        'nom': culture_obj.nom,
        'famille': culture_obj.famille.nom if culture_obj.famille else None,
        'famille_emoji': culture_obj.famille.emoji if culture_obj.famille else '🌱',
        'est_generique': False,
    }
    for champ in CHAMPS_A_FUSIONNER:
        conseils[champ] = None

    # Étape A : hériter du TYPE de culture (Arbre, Baie, Légume...)
    if conseils_type:
        for champ in CHAMPS_A_FUSIONNER:
            valeur = getattr(conseils_type, champ, None)
            if valeur not in (None, ''):
                conseils[champ] = valeur

    # Étape B : surcharger avec les valeurs spécifiques de la culture (ex: Pêche)
    for champ in CHAMPS_A_FUSIONNER:
        valeur = getattr(culture_obj, champ, None)
        if valeur not in (None, ''):
            conseils[champ] = valeur

    return conseils



# ============================================================
# ✅ NOUVELLE FONCTION : Cache des noms de cultures
# ============================================================
def get_tous_les_noms_cultures():
    """
    Retourne la liste complète des noms de cultures
    (Culture + Vegetable + Fruit), avec cache de 1 heure.

    Utile pour la recherche floue (get_close_matches) : évite
    3 requêtes SQL à chaque appel.
    """
    from .models import Culture, Vegetable, Fruit
    from django.core.cache import cache

    cache_key = 'tous_noms_cultures_v1'
    noms = cache.get(cache_key)

    if noms is None:
        noms = (
            list(Culture.objects.values_list('nom', flat=True)) +
            list(Vegetable.objects.values_list('nom', flat=True)) +
            list(Fruit.objects.values_list('nom', flat=True))
        )
        cache.set(cache_key, noms, 3600) # 1 heure
        logger.debug(f"🔄 Cache noms cultures rechargé ({len(noms)} noms)")


    return noms


def get_conseils_contextuels(climat, saison):
    """
    Retourne des conseils supplémentaires selon le climat de la parcelle.
    """
    conseils = []

    if climat == 'tropical':
        if saison in ['hiver', 'automne']:
            conseils.append("🌧️ Saison des pluies : surveillez le drainage de votre sol pour éviter le pourrissement des racines.")
        else:
            conseils.append("☀️ Saison sèche : installez un système de goutte-à-goutte pour économiser l'eau.")
    elif climat == 'desertique':
        conseils.append("💧 Arrosage crucial : arrosez le soir ou tôt le matin pour limiter l'évaporation. Paillez épais.")
    elif climat == 'continental':
        if saison == 'hiver':
            conseils.append("❄️ Hiver rigoureux : protégez les pieds avec un épais paillage (feuilles mortes) et badigeonnez les troncs à la chaux.")
    elif climat == 'tempere':
        if saison == 'printemps':
            conseils.append("🌱 Printemps : attention aux dernières gelées ! Gardez un voile d'hivernage à portée de main.")

    return conseils



# ===== VUE POUR LE DÉTAIL D'UNE FIGURE =====
@login_required
def figure_detail(request, figure_id):
    figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)

    logger.debug(f"\n=== FIGURE DETAIL ===")
    logger.debug(f"Figure: {figure.name}")
    logger.debug(f"ID: {figure.id}")
    logger.debug(f"Crops bruts: {figure.crops}")

    # ✅ Récupérer les cultures déjà planifiées et plantées (AVANT la boucle)
    cultures_planifiees = CalendrierUser.objects.filter(
        utilisateur=request.user,
        figure=figure
    ).values_list('culture', flat=True)

    cultures_plantees = ChronologieCulture.objects.filter(
        figure=figure
    ).values_list('culture_nom', flat=True)

    logger.debug(f"📅 Cultures planifiées : {list(cultures_planifiees)}")
    logger.debug(f"🌿 Cultures plantées : {list(cultures_plantees)}")

    # Enrichir les crops
    enriched_crops = []

    # ✅ Optimisation : pré-charger tous les Fruits et Vegetables en 2 requêtes
    fruit_ids = [c['fruit_id'] for c in figure.crops if 'fruit_id' in c]
    vegetable_ids = [c['vegetable_id'] for c in figure.crops if 'vegetable_id' in c]

    fruits_dict = {
        f.id: f for f in Fruit.objects.filter(id__in=fruit_ids)
    }
    vegetables_dict = {
        v.id: v for v in Vegetable.objects.filter(id__in=vegetable_ids)
    }

    # Enrichir les crops
    enriched_crops = []

    for crop in figure.crops:
        # ✅ Version rapide : utilise les objets déjà chargés
        if 'fruit_id' in crop:
            obj = fruits_dict.get(crop['fruit_id'])
            enriched = enrichir_culture_depuis_obj(crop, obj, 'fruit')
        elif 'vegetable_id' in crop:
            obj = vegetables_dict.get(crop['vegetable_id'])
            enriched = enrichir_culture_depuis_obj(crop, obj, 'vegetable')
        else:
            enriched = enrichir_culture_depuis_obj(crop, None, None)

        # ✅ Gère les détails
        if enriched.get('details'):
            enriched['details_json'] = json.dumps(enriched['details'], ensure_ascii=False)
        else:
            enriched['details_json'] = '{}'

        # ✅ Vérifier si la culture est déjà planifiée ou plantée
        nom = enriched.get('name', '')
        if nom in cultures_planifiees or nom in cultures_plantees:
            enriched['planification_disponible'] = False
        else:
            enriched['planification_disponible'] = True

        # ✅ Conseils enrichis
        enriched['conseils'] = get_conseils_culture(enriched.get('name'))

        # ✅ NOUVEAU : Ajout des conseils géographiques
        if enriched['conseils']:
            # On récupère le climat et la saison de la parcelle
            climat = get_climat_mondial(figure.adresse_lat, figure.adresse_lng) if figure.adresse_lat else 'tempere'
            saison = get_saison_actuelle()  # Ta fonction existante

            # On ajoute la liste des conseils contextuels
            enriched['conseils']['conseils_contextuels'] = get_conseils_contextuels(climat, saison)

        enriched_crops.append(enriched)

    # ✅ Filtrer les cultures disponibles pour la planification
    cultures_disponibles = []
    for crop in figure.crops:
        nom = crop.get('name', '')
        est_planifiee = nom in cultures_planifiees
        est_plante = nom in cultures_plantees

        logger.debug(f"🔍 Culture: '{nom}' - Planifiée: {est_planifiee} - Plantée: {est_plante}")

        if nom and not est_planifiee and not est_plante:
            cultures_disponibles.append(crop)
            logger.debug(f" ✅ AJOUTÉE à disponibles")
        else:
            logger.debug(f" ❌ IGNORÉE")

    logger.debug(f"📊 cultures_disponibles: {len(cultures_disponibles)}")
    for c in cultures_disponibles:
        logger.debug(f" - {c.get('name')}")

    # ✅ Récupérer les chronologies pour cette figure (EXCLURE LES RÉCOLTÉES)
    chronologie_cultures = ChronologieCulture.objects.filter(
        figure=figure
    ).exclude(
        statut='recolte' # ✅ EXCLURE LES RÉCOLTÉES
    ).select_related('figure__user').order_by('-date_semis')

    for chrono in chronologie_cultures:
        chrono.calculer_progression()

    # Debug
    logger.debug(f"\n=== CULTURES ENRICHIES ===")
    logger.debug(f"Nombre de cultures: {len(enriched_crops)}")

    logger.debug(f"\n=== VÉRIFICATION DES JSONS ===")
    for i, crop in enumerate(enriched_crops):
        logger.debug(f"Culture {i + 1}: {crop.get('name')}")
        logger.debug(f" details_json: {crop.get('details_json')}")
        logger.debug(f" details_json type: {type(crop.get('details_json'))}")
        logger.debug(f" longueur: {len(crop.get('details_json')) if crop.get('details_json') else 0}")

    geojson_string = json.dumps(figure.geojson_data, separators=(',', ':')) if figure.geojson_data else '{}'

    logger.debug(f"🔍 geojson_string pour figure {figure.id}: {geojson_string[:200]}")

    # Si les champs adresse_lat/adresse_lng sont vides, on les extrait du GeoJSON
    if not figure.adresse_lat and figure.geojson_data:
        try:
            coords = figure.geojson_data['features'][0]['geometry']['coordinates'][0][0]
            figure_lat = coords[1]
            figure_lng = coords[0]
        except:
            figure_lat = None
            figure_lng = None
    else:
        figure_lat = figure.adresse_lat
        figure_lng = figure.adresse_lng

    fruits = Fruit.objects.all().order_by('nom')
    vegetables = Vegetable.objects.all().order_by('nom')

    # ✅ CONSEILS PERSONNALISÉS
    conseils = {}
    conseils_par_culture = []
    if figure:
        conseils = get_conseils_personnalises(request.user, figure)
        conseils_par_culture = conseils.get('conseils_par_culture', [])

    logger.debug(f" Conseils par culture: {conseils_par_culture}")


    return render(request, 'vegetables_fruits/draw/figure_detail.html', {
        'figure': figure,
        'geojson_string': geojson_string,
        'enriched_crops': enriched_crops,
        'mapbox_token': settings.MAPBOX_TOKEN,
        'chronologie_cultures': chronologie_cultures,
        'figure_lat': figure_lat,
        'figure_lng': figure_lng,
        'fruits': fruits,
        'vegetables': vegetables,
        'conseils': conseils,
        'conseils_par_culture': conseils.get('conseils_par_culture', []),
        'cultures_disponibles': cultures_disponibles,
    })


# ===== VUE POUR ÉDITER LES CULTURES =====
@login_required
def edit_figure(request, figure_id):
    """
    Modifier les cultures placées sur une figure
    """


    from .models import Variete
    figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)
    culture_preselect = request.GET.get('culture')
    parcelle = Parcelle.objects.filter(figure=figure).first()

    logger.debug("\n=== DEBUG EDIT FIGURE ===")
    logger.debug(f"Figure ID: {figure.id}")
    logger.debug(f"Figure name: {figure.name}")

    fruits = Fruit.objects.all().order_by(Lower('nom')).prefetch_related(
        models.Prefetch('varietes_m2m', queryset=Variete.objects.order_by(Lower('nom')))
    )

    vegetables = Vegetable.objects.all().order_by(Lower('nom')).prefetch_related(
        models.Prefetch('varietes_m2m', queryset=Variete.objects.order_by(Lower('nom')))
    )

    if request.method == 'POST':
        # ⭐⭐ GESTION DU TYPE DE SOL ⭐⭐
        sol_mode = request.POST.get('sol_mode', 'manuel')
        type_sol = request.POST.get('type_sol', '')

        logger.debug(f"🔍 edit_figure - sol_mode reçu : {sol_mode}")
        logger.debug(f"🔍 edit_figure - type_sol reçu : {type_sol}")

        if sol_mode == 'auto':
            # Récupérer les coordonnées du formulaire
            adresse_lat = request.POST.get('adresse_lat')
            adresse_lng = request.POST.get('adresse_lng')
            adresse = request.POST.get('adresse', '')

            logger.debug(f"🔍 edit_figure - adresse_lat reçu : {adresse_lat}")
            logger.debug(f"🔍 edit_figure - adresse_lng reçu : {adresse_lng}")
            logger.debug(f"🔍 edit_figure - adresse reçue : {adresse}")

            # Mettre à jour les coordonnées de la figure
            if adresse_lat and adresse_lng:
                figure.adresse_lat = float(adresse_lat)
                figure.adresse_lng = float(adresse_lng)
                figure.adresse = adresse
                figure.save()
                logger.info(f"✅ Coordonnées de la figure mises à jour : {figure.adresse_lat}, {figure.adresse_lng}")

            exposition = request.POST.get('exposition')
            if exposition:
                parcelle.exposition = exposition
                parcelle.save()

            # Récupérer la région via Mapbox
            region_info = get_region_utilisateur(request.user, figure)
            region = region_info['region']
            pays = region_info['pays']
            continent = region_info['continent']

            logger.debug(f"🔍 Région détectée : {figure.name}: {region}")
            logger.debug(f"🔍 Pays détecté : {pays}")
            logger.debug(f"🔍 Continent détecté : {continent}")

            # 🔥 LOGIQUE HIÉRARCHIQUE : Région → Pays → Continent
            type_sol = SOL_PAR_REGION.get(region)  # D'abord par région

            if not type_sol:
                # Si région non trouvée, essayer par pays
                pays_sols = {
                    'france': 'limoneux',
                    'italie': 'calcaire',
                    'italy': 'calcaire',
                    'espagne': 'calcaire',
                    'spain': 'calcaire',
                    'allemagne': 'limoneux',
                    'germany': 'limoneux',
                    'chine': 'loess',
                    'china': 'loess',
                    'république populaire de chine': 'loess',
                    'japon': 'volcanique',
                    'japan': 'volcanique',
                    'inde': 'latéritique',
                    'india': 'latéritique',
                    'etats-unis': 'limoneux',
                    'usa': 'limoneux',
                    'united states': 'limoneux',
                    'canada': 'tourbeux',
                    'bresil': 'latéritique',
                    'brazil': 'latéritique',
                    'australie': 'lateritique',
                    'australia': 'lateritique',
                    'egypte': 'alluvial',
                    'egypt': 'alluvial',
                    'afrique du sud': 'calcaire',
                    'south africa': 'calcaire',
                    'maroc': 'calcaire',
                    'morocco': 'calcaire',
                    'tunisie': 'calcaire',
                    'tunisia': 'calcaire',
                    'grece': 'calcaire',
                    'greece': 'calcaire',
                    'turquie': 'calcaire',
                    'turkey': 'calcaire',
                    'türkiye': 'calcaire',
                    'mexique': 'volcanique',
                    'mexico': 'volcanique',
                    'portugal': 'calcaire',
                    'pays-bas': 'argileux',
                    'netherlands': 'argileux',
                    'belgique': 'limoneux',
                    'belgium': 'limoneux',
                    'suisse': 'calcaire',
                    'switzerland': 'calcaire',
                    'autriche': 'calcaire',
                    'austria': 'calcaire',
                    'suede': 'tourbeux',
                    'sweden': 'tourbeux',
                    'norvege': 'tourbeux',
                    'norway': 'tourbeux',
                    'finlande': 'tourbeux',
                    'finland': 'tourbeux',
                    'danemark': 'sableux',
                    'denmark': 'sableux',
                    'pologne': 'limoneux',
                    'poland': 'limoneux',
                    'republique tcheque': 'limoneux',
                    'czechia': 'limoneux',
                    'slovaquie': 'limoneux',
                    'slovakia': 'limoneux',
                    'hongrie': 'limoneux',
                    'hungary': 'limoneux',
                    'roumanie': 'limoneux',
                    'romania': 'limoneux',
                    'bulgarie': 'calcaire',
                    'bulgaria': 'calcaire',
                    'croatie': 'calcaire',
                    'croatia': 'calcaire',
                    'serbie': 'limoneux',
                    'serbia': 'limoneux',
                    'israel': 'désertique',
                    'jordanie': 'désertique',
                    'jordan': 'désertique',
                    'liban': 'calcaire',
                    'lebanon': 'calcaire',
                    'iran': 'désertique',
                    'irak': 'alluvial',
                    'iraq': 'alluvial',
                    'arabie saoudite': 'désertique',
                    'saudi arabia': 'désertique',
                    'emirats arabes unis': 'désertique',
                    'uae': 'désertique',
                    'kazakhstan': 'steppique',
                    'coree': 'limoneux',
                    'korea': 'limoneux',
                    'vietnam': 'latéritique',
                    'thailande': 'latéritique',
                    'thailand': 'latéritique',
                    'indonesie': 'volcanique',
                    'indonesia': 'volcanique',
                    'philippines': 'volcanique',
                    'malaisie': 'latéritique',
                    'malaysia': 'latéritique',
                    'singapour': 'latéritique',
                    'singapore': 'latéritique',
                    'costa rica': 'volcanique',
                    'panama': 'latéritique',
                    'guatemala': 'volcanique',
                    'cuba': 'calcaire',
                    'jamaique': 'calcaire',
                    'jamaica': 'calcaire',
                    'argentine': 'limoneux',
                    'argentina': 'limoneux',
                    'chili': 'volcanique',
                    'chile': 'volcanique',
                    'perou': 'calcaire',
                    'peru': 'calcaire',
                    'colombie': 'latéritique',
                    'colombia': 'latéritique',
                    'venezuela': 'latéritique',
                    'equateur': 'volcanique',
                    'ecuador': 'volcanique',
                    'bolivie': 'calcaire',
                    'bolivia': 'calcaire',
                    'paraguay': 'latéritique',
                    'uruguay': 'limoneux',
                    'senegal': 'latéritique',
                    'nigeria': 'latéritique',
                    'ghana': 'latéritique',
                    'kenya': 'volcanique',
                    'tanzanie': 'latéritique',
                    'tanzania': 'latéritique',
                    'ethiopie': 'volcanique',
                    'ethiopia': 'volcanique',
                    'ouganda': 'volcanique',
                    'uganda': 'volcanique',
                    'rwanda': 'volcanique',
                    'congo': 'latéritique',
                    'cameroon': 'latéritique',
                    'angola': 'latéritique',
                    'mozambique': 'latéritique',
                    'zimbabwe': 'latéritique',
                    'zambie': 'latéritique',
                    'zambia': 'latéritique',
                    'madagascar': 'latéritique',
                    'nouvelle-zelande': 'volcanique',
                    'new zealand': 'volcanique',
                    'papouasie-nouvelle-guinee': 'latéritique',
                    'papua new guinea': 'latéritique',
                    'fidji': 'volcanique',
                    'fiji': 'volcanique',
                    'hawaii': 'volcanique',
                    'groenland': 'tourbeux',
                    'greenland': 'tourbeux',
                    'islande': 'volcanique',
                    'iceland': 'volcanique',
                }
                type_sol = pays_sols.get(pays.lower())
                if type_sol:
                    logger.debug(f"🔍 Type de sol trouvé par pays: {pays} → {type_sol}")

            if not type_sol:
                # Si pays non trouvé, essayer par continent
                continent_sols = {
                    'europe': 'limoneux',
                    'asie': 'limoneux',
                    'amerique': 'limoneux',
                    'afrique': 'latéritique',
                    'oceanie': 'lateritique',
                    'arctique': 'tourbeux',
                    'antarctique': 'glaciaire',
                }
                type_sol = continent_sols.get(continent)
                if type_sol:
                    logger.debug(f"🔍 Type de sol trouvé par continent: {continent} → {type_sol}")

            if not type_sol:
                type_sol = 'autre'
                logger.warning(f"⚠️ Aucun type de sol trouvé pour région={region}, pays={pays}, continent={continent} → 'autre'")

            logger.debug(f"🔍 Type de sol final assigné : {type_sol}")

        # Mettre à jour le type de sol dans la parcelle
        if type_sol:
            parcelle = Parcelle.objects.filter(figure=figure).first()
            if parcelle:
                parcelle.type_sol = type_sol
                parcelle.save()
                logger.info(f"✅ Type de sol mis à jour pour {parcelle.nom}: {type_sol}")
            else:
                logger.warning("⚠️ Aucune parcelle trouvée pour mettre à jour le type de sol")

        # Mise à jour du nom et de la description
        figure.name = request.POST.get('name', figure.name)
        figure.description = request.POST.get('description', figure.description)
        figure.save()

        crops_data = request.POST.get('crops_data')
        if crops_data:
            try:
                crops_list = json.loads(crops_data)
                figure.crops = crops_list
                figure.save()

                # ✅ AUTOMATISATION BESOINS EAU
                parcelle = Parcelle.objects.filter(figure=figure).first()

                if parcelle:
                    logger.info(f"✅ Parcelle trouvée : {parcelle.nom}")
                    for crop in crops_list:
                        culture_nom = crop.get('name', '')
                        if culture_nom:
                            besoin_existant = BesoinsEau.objects.filter(
                                parcelle=parcelle,
                                culture__icontains=culture_nom
                            ).exists()

                            if not besoin_existant:
                                nouveau_besoin = BesoinsEau.objects.create(
                                    parcelle=parcelle,
                                    culture=culture_nom,
                                    besoin_litres_par_m2=10.0,
                                    frequence_arrosage_jours=3,
                                    periode_sensible=""
                                )
                                logger.info(f"✅ Besoin en eau créé pour {culture_nom} (ID: {nouveau_besoin.id})")
                            else:
                                logger.debug(f"ℹ️ Besoin en eau déjà existant pour {culture_nom}")
                else:
                    logger.warning("⚠️ Aucune parcelle associée à cette figure")

                # Points pour l'élève
                if request.user.is_authenticated and hasattr(request.user, 'profil_eleve'):
                    eleve = request.user.profil_eleve
                    eleve.ajouter_points(5)

                    if request.user.mode_junior:
                        for crop in crops_list:
                            if 'fleur' in crop.get('name', '').lower():
                                eleve.ajouter_points(8, action_type='planter_fleur')
                                messages.success(request, "🌼 +8 points pour avoir planté une fleur pollinisatrice !")
                                break

                messages.success(request, f"{len(crops_list)} culture(s) enregistrée(s) avec succès!")
                return redirect('vegetables_fruits:figure_detail', figure_id=figure.id)

            except json.JSONDecodeError:
                messages.error(request, "Erreur de format des données")


        return redirect('vegetables_fruits:figure_detail', figure_id=figure.id)

    # GET : afficher le formulaire
    enriched_crops = [enrichir_culture(crop) for crop in figure.crops]
    valid_crops = [c for c in enriched_crops if c['details'] is not None]
    failed_crops = len(enriched_crops) - len(valid_crops)

    if failed_crops > 0:
        logger.warning(f"⚠️ {failed_crops} culture(s) n'ont pas pu être enrichies")
        messages.warning(request, f"{failed_crops} culture(s) n'ont pas pu être chargées complètement")

    # ✅ Récupérer les variétés
    from .models import Variete
    varietes = Variete.objects.select_related('culture').order_by('culture__nom', 'nom')

    return render(request, 'vegetables_fruits/draw/edit_figure.html', {
        'figure': figure,
        'fruits': fruits,
        'vegetables': vegetables,
        'enriched_crops': json.dumps(valid_crops),
        'varietes': varietes,
        'mapbox_token': settings.MAPBOX_TOKEN,
        'culture_preselect': culture_preselect,
    })
@login_required
def delete_figure(request, figure_id):
    """Supprime une figure"""
    figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)

    if request.method == 'POST':
        figure.delete()
        messages.success(request, "Figure supprimée avec succès!")
        return redirect('vegetables_fruits:view_figure')

    return render(request, 'vegetables_fruits/draw/confirm_delete.html', {'figure': figure})


# ===== API POUR RÉCUPÉRER LES DÉTAILS D'UN FRUIT/LÉGUME =====
@login_required
def get_crop_details(request):
    """Endpoint API pour récupérer les détails d'un fruit ou légume"""
    crop_type = request.GET.get('type')
    crop_id = request.GET.get('id')

    if crop_type == 'fruit':
        try:
            fruit = Fruit.objects.get(id=crop_id)
            return JsonResponse({
                'success': True,
                'data': {
                    'id': fruit.id,
                    'nom': fruit.nom,
                    'couleur': fruit.couleur,
                    'prix': fruit.prix,
                    'saison': fruit.saison,
                    'emoji': '🍎'
                }
            })
        except Fruit.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Fruit non trouvé'})

    elif crop_type == 'vegetable':
        try:
            vegetable = Vegetable.objects.get(id=crop_id)
            return JsonResponse({
                'success': True,
                'data': {
                    'id': vegetable.id,
                    'nom': vegetable.nom,
                    'couleur': vegetable.couleur,
                    'prix': vegetable.prix,
                    'saison': vegetable.saison,
                    'emoji': '🥕'
                }
            })
        except Vegetable.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Légume non trouvé'})

    return JsonResponse({'success': False, 'error': 'Type invalide'})


@login_required
def planifier_alertes(request):
    """Planifie les alertes pour les semis et récoltes"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

    try:
        data = json.loads(request.body)
        figure_id = data.get('figure_id')
        crop_data = data.get('crop')
        dates = data.get('dates', {})
        canal = data.get('canal', 'email')
        alertes = data.get('alertes', [])

        figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)

        alertes_crees = 0

        for alerte in alertes:
            # Créer l'alerte en base
            nouvelle_alerte = AlerteSemis.objects.create(
                figure=figure,
                crop_data=crop_data,
                type_alerte=alerte['type'],
                canal=canal,
                titre=alerte['titre'],
                message=alerte['message'],
                date_declenchement=alerte['date'],
                email_destinataire=request.user.email if canal in ['email', 'les_deux'] else None,
                telephone_destinataire=request.user.telephone if hasattr(request.user, 'telephone') and canal in ['sms',
                                                                                                                  'les_deux'] else None,
                statut='en_attente'
            )
            alertes_crees += 1

        return JsonResponse({
            'success': True,
            'alertes_crees': alertes_crees,
            'message': f'{alertes_crees} alerte(s) planifiée(s)'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def planifier_rappel_semis(user, culture, date_semis):
    """Planifie un rappel de semis"""
    AlerteSemis.objects.create(
        utilisateur=user,
        type_alerte='semis',
        titre=f"📅 Semis des {culture}",
        message=f"Pensez à semer vos {culture} aujourd'hui !",
        date_declenchement=date_semis,
        canal='email',
    )

@login_required
def mes_alertes(request):
    """Affiche les alertes de l'utilisateur"""
    from django.utils import timezone

    figures = GeometricFigure.objects.filter(user=request.user)

    alertes_en_attente = AlerteSemis.objects.filter(
         figure__in=figures,
        statut='en_attente'
    ).order_by('date_declenchement')

    # Ajouter des propriétés pour l'urgence
    aujourdhui = timezone.now()
    for alerte in alertes_en_attente:
        jours_restants = (alerte.date_declenchement - aujourdhui).days
        alerte.est_urgente = jours_restants <= 1
        alerte.est_proche = 1 < jours_restants <= 3

    alertes_envoyees = AlerteSemis.objects.filter(
        figure__in=figures,
        statut='envoyee'
    ).order_by('-date_envoi')

    alertes_ignorees = AlerteSemis.objects.filter(
        figure__in=figures,
        statut='ignoree'
    ).order_by('-date_declenchement')

    # Alertes dans les 7 prochains jours
    date_limite = aujourdhui + timedelta(days=7)
    alertes_prochaines = alertes_en_attente.filter(
        date_declenchement__lte=date_limite
    ).count()

    stats = {
        'en_attente': alertes_en_attente.count(),
        'envoyees': alertes_envoyees.count(),
        'ignorees': alertes_ignorees.count(),
        'prochaines': alertes_prochaines,
    }

    return render(request, 'vegetables_fruits/alertes.html', {
        'alertes_en_attente': alertes_en_attente,
        'alertes_envoyees': alertes_envoyees,
        'alertes_ignorees': alertes_ignorees,
        'stats': stats
    })


@login_required
def ignorer_alerte_semis(request, alerte_id):
    """Marque une alerte comme ignorée"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

    try:
        alerte = get_object_or_404(AlerteSemis, id=alerte_id, figure__user=request.user)
        alerte.statut = 'ignoree'
        alerte.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def restaurer_alerte_semis(request, alerte_id):
    """Restaure une alerte ignorée"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

    try:
        alerte = get_object_or_404(AlerteSemis, id=alerte_id, figure__user=request.user)
        alerte.statut = 'en_attente'
        alerte.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



@login_required
def basculer_mode_junior(request):
    if request.method == 'POST':
        activer = request.POST.get('actif') == 'true'
        if activer and request.user.birth_date:
            from datetime import date
            age = (date.today() - request.user.birth_date).days // 365
            if age >= 18:
                return JsonResponse({'success': False, 'error': 'Le mode Junior est réservé au moins de 18 ans.'})
        request.user.mode_junior = activer
        request.user.save()
        return JsonResponse({'success': True})

@login_required
def mettre_a_jour_coordonnees(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')

        if email:
            request.user.email = email
        if telephone:
            request.user.telephone = telephone

        request.user.save()
        messages.success(request, "Vos coordonnées ont été mises à jour")
        return redirect('profile')

    return redirect('vegetables_fruits:profile')


@login_required
def progression_junior(request):
    progression, created = ProgressionJunior.objects.get_or_create(user=request.user)

    # Calculer le niveau (100 points par niveau)
    niveau = progression.points // 100 + 1
    progression.niveau = niveau
    progression.pourcentage = (progression.points % 100)
    progression.save()

    return JsonResponse({
        'niveau': progression.niveau,
        'points': progression.points,
        'badges': [{'nom': b.nom, 'emoji': b.emoji} for b in progression.badges.all()]
    })


# ==================== VUES ENSEIGNANT / ÉLÈVES ====================

@login_required
def creer_classe(request):
    """Créer une nouvelle classe (réservé aux enseignants)"""
    if not request.user.is_enseignant:
        messages.error(request, "Vous n'avez pas les droits pour créer une classe")
        return redirect('index')

    if request.method == 'POST':
        nom = request.POST.get('nom')
        if nom:
            classe = Classe.objects.create(
                nom=nom,
                enseignant=request.user
            )
            # Le code est généré automatiquement par la méthode save()
            messages.success(request, f"✅ Classe '{nom}' créée ! Code d'invitation : {classe.code}")
            return redirect('vegetables_fruits:dashboard_enseignant')
        else:
            messages.error(request, "Veuillez entrer un nom de classe")

    return render(request, 'vegetables_fruits/enseignant/creer_classe.html')


@login_required
def dashboard_enseignant(request):
    """Tableau de bord de l'enseignant"""
    if not request.user.is_enseignant:
        messages.error(request, "Accès non autorisé")
        return redirect('vegetables_fruits:index')

    classes = Classe.objects.filter(enseignant=request.user)
    eleves = Eleve.objects.filter(classe__enseignant=request.user)

    # Calculer les stats
    total_eleves = eleves.count()
    total_points = sum(eleve.points for eleve in eleves)

    signalements_en_attente = SignalementForum.objects.filter(statut='en_attente').count()
    logger.debug(f" Signalements en attente : {signalements_en_attente}")


    context = {
        'classes': classes,
        'eleves': eleves,
        'total_eleves': total_eleves,
        'total_points': total_points,
        'signalements_en_attente': signalements_en_attente,
    }

    return render(request, 'vegetables_fruits/enseignant/dashboard.html', context)


@login_required
def marquer_signalements_lus(request):
    """Marque tous les signalements en attente comme lus pour l'enseignant"""
    if not request.user.is_enseignant:
        return JsonResponse({'error': 'Non autorisé'}, status=403)

    SignalementForum.objects.filter(statut='en_attente').update(est_lu_par_enseignant=True)

    return redirect('vegetables_fruits:dashboard_enseignant')



@login_required
def rejoindre_classe(request):
    if request.method == 'POST':
        code = request.POST.get('code_classe', '').strip().upper()

        if not code:
            messages.error(request, "Veuillez entrer un code de classe.")
            return redirect('vegetables_fruits:profile')

        try:
            classe = Classe.objects.get(code=code)
        except Classe.DoesNotExist:
            messages.error(request, "Code invalide. Vérifie auprès de ton professeur.")
            return redirect('vegetables_fruits:profile')

        # ✅ Créer OU récupérer le profil Eleve
        # (au cas où l'utilisateur était un mineur particulier avant)
        eleve, eleve_created = Eleve.objects.get_or_create(user=request.user)
        eleve.classe = classe
        eleve.save()

        if eleve_created:
            messages.success(request, f"🎉 Ton profil élève a été créé et tu as rejoint la classe « {classe.nom} » !")
        else:
            messages.success(request, f"🎉 Tu as rejoint la classe « {classe.nom} » !")

        return redirect('vegetables_fruits:profile')

    return redirect('vegetables_fruits:profile')

@login_required
def toggle_mode_junior_eleve(request, eleve_id):
    """Activer/désactiver le mode junior pour un élève"""
    if not request.user.is_enseignant:
        return JsonResponse({'error': 'Non autorisé'}, status=403)

    try:
        eleve = get_object_or_404(Eleve, id=eleve_id, classe__enseignant=request.user)
        eleve.user.mode_junior = not eleve.user.mode_junior
        eleve.user.save()

        status = "activé" if eleve.user.mode_junior else "désactivé"
        return JsonResponse(
            {'success': True, 'mode_junior': eleve.user.mode_junior, 'message': f"Mode junior {status}"})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def supprimer_eleve(request, eleve_id):
    """Supprimer un élève de la classe"""
    if not request.user.is_enseignant:
        return JsonResponse({'error': 'Non autorisé'}, status=403)

    try:
        eleve = get_object_or_404(Eleve, id=eleve_id, classe__enseignant=request.user)
        nom_eleve = eleve.user.username
        eleve.user.delete()
        eleve.delete()
        return JsonResponse({'success': True, 'message': f"Élève {nom_eleve} supprimé"})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def classement_eleve(request):
    # Récupérer l'utilisateur connecté
    user = request.user
    classe = None
    eleves = None

    # Cas 1 : L'utilisateur est un ÉLÈVE
    if hasattr(user, 'profil_eleve') and user.profil_eleve.classe:
        classe = user.profil_eleve.classe
        eleves = classe.eleves.all().order_by('-points')

    # Cas 2 : L'utilisateur est un ENSEIGNANT
    elif user.is_enseignant:
        # Récupérer la première classe de l'enseignant (ou classe sélectionnée)
        classe_id = request.GET.get('classe_id')
        if classe_id:
            classe = Classe.objects.filter(id=classe_id, enseignant=user).first()
        else:
            classe = Classe.objects.filter(enseignant=user).first()

        if classe:
            eleves = classe.eleves.all().order_by('-points')

    # Cas 3 : Aucune classe associée
    if not classe or not eleves:
        if user.is_enseignant:
            messages.warning(request, "Vous n'avez pas encore de classe. Créez-en une !")
            return redirect('vegetables_fruits:dashboard_enseignant')
        else:
            messages.warning(request, "Vous n'êtes pas encore dans une classe. Rejoignez-en une !")
            return redirect('vegetables_fruits:profile')

    # Construction du classement
    classement = []
    for i, eleve in enumerate(eleves, 1):
        classement.append({
            'rang': i,
            'eleve': eleve,
            'points': eleve.points,
            'niveau': eleve.niveau,
            'badge_count': eleve.badges.count()
        })

    # Position de l'utilisateur connecté (s'il est élève)
    position_user = None
    if hasattr(user, 'profil_eleve'):
        position_user = next((c for c in classement if c['eleve'].user == user), None)

    if position_user:
        points_dans_niveau = position_user['points'] % 100
        points_prochain_niveau = 100 - points_dans_niveau

        niveaux = [
            {'numero': 1, 'emoji': '🌱'},
            {'numero': 2, 'emoji': '🌿'},
            {'numero': 3, 'emoji': '🌳'},
            {'numero': 4, 'emoji': '🌸'},
            {'numero': 5, 'emoji': '🍎'},
            {'numero': 6, 'emoji': '👑'},
        ]

        position_user['points_dans_niveau'] = points_dans_niveau
        position_user['points_prochain_niveau'] = points_prochain_niveau

    # Pour l'enseignant : liste des classes pour le sélecteur
    classes_list = []
    if user.is_enseignant:
        classes_list = Classe.objects.filter(enseignant=user)

    return render(request, 'vegetables_fruits/classement.html', {
        'classement': classement,
        'position_user': position_user,
        'classe': classe,
        'classes_list': classes_list,
        'is_enseignant': user.is_enseignant,
    })

# ===== EXPORT CSV =====
@login_required
def export_eleves_csv(request, classe_id):
    """Exporte la liste des élèves d'une classe au format CSV"""
    if not request.user.is_enseignant:
        messages.error(request, "Accès non autorisé")
        return redirect('vegetables_fruits:index')

    classe = get_object_or_404(Classe, id=classe_id, enseignant=request.user)

    # Créer la réponse HTTP avec l'en-tête CSV
    response = HttpResponse(content_type='text/csv')
    response[
        'Content-Disposition'] = f'attachment; filename="classe_{classe.nom}_{datetime.now().strftime("%Y%m%d")}.csv"'

    writer = csv.writer(response)

    # En-têtes
    writer.writerow(['Nom', 'Email', 'Date inscription', 'Points', 'Niveau', 'Badges', 'Mode Junior'])

    # Données
    for eleve in classe.eleves.all():
        writer.writerow([
            eleve.user.username,
            eleve.user.email,
            eleve.date_inscription.strftime('%d/%m/%Y'),
            eleve.points,
            eleve.niveau,
            eleve.badges.count(),
            'Oui' if eleve.user.mode_junior else 'Non'
        ])

    return response


# ===== EXPORT PDF =====
@login_required
def export_eleves_pdf(request, classe_id):
    """Exporte la liste des élèves d'une classe au format PDF"""
    if not request.user.is_enseignant:
        messages.error(request, "Accès non autorisé")
        return redirect('vegetables_fruits:index')

    classe = get_object_or_404(Classe, id=classe_id, enseignant=request.user)

    # Créer la réponse HTTP avec l'en-tête PDF
    response = HttpResponse(content_type='application/pdf')
    response[
        'Content-Disposition'] = f'attachment; filename="classe_{classe.nom}_{datetime.now().strftime("%Y%m%d")}.pdf"'

    # Créer le document PDF
    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#28a745'),
        alignment=1  # Centre
    )

    # Titre
    elements.append(Paragraph(f"📊 Rapport de la classe : {classe.nom}", title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Date d'export : {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Statistiques
    total_eleves = classe.eleves.count()
    total_points = sum(eleve.points for eleve in classe.eleves.all())
    moyenne_points = total_points / total_eleves if total_eleves > 0 else 0

    stats_data = [
        ['📊 Statistiques', ''],
        ['Nombre d\'élèves', str(total_eleves)],
        ['Points totaux', str(total_points)],
        ['Moyenne des points', f"{moyenne_points:.1f}"],
        ['Niveau moyen',
         f"{sum(eleve.niveau for eleve in classe.eleves.all()) / total_eleves:.1f}" if total_eleves > 0 else '0']
    ]

    stats_table = Table(stats_data, colWidths=[150, 100])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 20))

    # Tableau des élèves
    data = [['#', 'Élève', 'Points', 'Niveau', 'Badges', 'Inscription']]

    for i, eleve in enumerate(classe.eleves.all().order_by('-points'), 1):
        data.append([
            str(i),
            eleve.user.username,
            str(eleve.points),
            str(eleve.niveau),
            str(eleve.badges.count()),
            eleve.date_inscription.strftime('%d/%m/%Y')
        ])

    # Créer le tableau
    table = Table(data, colWidths=[40, 100, 60, 60, 60, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(table)

    # Construire le PDF
    doc.build(elements)
    return response


# ===== EXPORT INDIVIDUEL D'UN ÉLÈVE =====
@login_required
def export_eleve_pdf(request, eleve_id):
    """Exporte le rapport individuel d'un élève au format PDF"""
    if not request.user.is_enseignant:
        messages.error(request, "Accès non autorisé")
        return redirect('vegetables_fruits:index')

    eleve = get_object_or_404(Eleve, id=eleve_id, classe__enseignant=request.user)

    response = HttpResponse(content_type='application/pdf')
    response[
        'Content-Disposition'] = f'attachment; filename="eleve_{eleve.user.username}_{datetime.now().strftime("%Y%m%d")}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#28a745'),
        alignment=1
    )

    # Titre
    elements.append(Paragraph(f"📊 Rapport individuel : {eleve.user.username}", title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Classe : {eleve.classe.nom}", styles['Normal']))
    elements.append(Paragraph(f"Date d'export : {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Informations générales
    info_data = [
        ['📋 Informations', ''],
        ['Nom d\'utilisateur', eleve.user.username],
        ['Email', eleve.user.email or 'Non renseigné'],
        ['Date d\'inscription', eleve.date_inscription.strftime('%d/%m/%Y')],
        ['Points', str(eleve.points)],
        ['Niveau', str(eleve.niveau)],
        ['Mode Junior', 'Activé' if eleve.user.mode_junior else 'Désactivé']
    ]

    info_table = Table(info_data, colWidths=[120, 200])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # Badges
    if eleve.badges.all():
        badges_text = ", ".join([f"{b.emoji} {b.nom}" for b in eleve.badges.all()])
        elements.append(Paragraph(f"🏅 Badges débloqués : {badges_text}", styles['Normal']))
    else:
        elements.append(Paragraph("🏅 Badges débloqués : Aucun badge pour le moment", styles['Normal']))

    doc.build(elements)
    return response


# ==================== NOTIFICATIONS ENSEIGNANT ====================

def creer_notification(enseignant, type_notif, titre, message, lien=None):
    """Crée une notification pour un enseignant"""
    NotificationEnseignant.objects.create(
        enseignant=enseignant,
        type_notification=type_notif,
        titre=titre,
        message=message,
        lien=lien
    )


@login_required
def get_notifications(request):
    """API pour récupérer les notifications (AJAX)"""
    if not request.user.is_enseignant:
        return JsonResponse({'error': 'Non autorisé'}, status=403)

    notifications = NotificationEnseignant.objects.filter(
        enseignant=request.user,
        est_lu=False
    ).order_by('-date_creation')[:10]

    data = {
        'non_lues': NotificationEnseignant.objects.filter(enseignant=request.user, est_lu=False).count(),
        'notifications': [
            {
                'id': n.id,
                'type': n.type_notification,
                'titre': n.titre,
                'message': n.message,
                'lien': n.lien,
                'date': n.date_creation.strftime('%d/%m/%Y %H:%M'),
            }
            for n in notifications
        ]
    }
    return JsonResponse(data)


@login_required
def marquer_notification_lue(request, notif_id):
    """Marque une notification comme lue"""
    if request.method == 'POST':
        try:
            notif = NotificationEnseignant.objects.get(id=notif_id, enseignant=request.user)
            notif.est_lu = True
            notif.save()
            return JsonResponse({'success': True})
        except NotificationEnseignant.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification non trouvée'})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


@login_required
def marquer_toutes_notifications_lues(request):
    """Marque toutes les notifications comme lues"""
    if request.method == 'POST':
        NotificationEnseignant.objects.filter(enseignant=request.user, est_lu=False).update(est_lu=True)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})


# ==================== DÉCLENCHEURS DE NOTIFICATIONS ====================

def check_and_send_notifications():
    """Fonction à appeler périodiquement (cron ou celery)"""
    from .models import Classe, Eleve

    # Vérifier les classes qui ont des nouveaux élèves depuis 7 jours
    date_limite = timezone.now() - timedelta(days=7)

    for classe in Classe.objects.filter(enseignant__is_enseignant=True):
        # Nouveaux élèves cette semaine
        nouveaux = classe.eleves.filter(date_inscription__gte=date_limite).count()
        if nouveaux > 0:
            creer_notification(
                classe.enseignant,
                'nouvel_eleve',
                f"🎉 {nouveaux} nouvel(s) élève(s) !",
                f"{nouveaux} élève(s) ont rejoint votre classe '{classe.nom}' cette semaine.",
                f"/dashboard-enseignant/"
            )

        # Vérifier les points totaux de la classe
        total_points = classe.eleves.aggregate(Sum('points'))['points__sum'] or 0
        if total_points >= 500 and total_points < 600:
            creer_notification(
                classe.enseignant,
                'succes',
                f"🏆 500 points pour la classe {classe.nom} !",
                f"Félicitations ! Votre classe a atteint 500 points cumulés.",
                f"/dashboard-enseignant/"
            )


# Modifier la vue inscription_eleve pour ajouter une notification

def inscription_eleve(request):
    """Inscription d'un élève avec code de classe"""
    if request.method == 'POST':
        form = InscriptionEleveForm(request.POST)
        if form.is_valid():
            user = form.save()
            code_classe = form.cleaned_data.get('code_classe')

            try:
                classe = Classe.objects.get(code=code_classe)
                eleve = Eleve.objects.create(
                    user=user,
                    classe=classe
                )

                # ✅ NOTIFICATION POUR L'ENSEIGNANT
                creer_notification(
                    classe.enseignant,
                    'nouvel_eleve',
                    f"🎉 Nouvel élève : {user.username}",
                    f"{user.username} a rejoint votre classe '{classe.nom}'.",
                    f"/dashboard-enseignant/"
                )

                # Optionnel : envoyer un email à l'enseignant
                if classe.enseignant.email:
                    send_mail(
                        f'Nouvel élève dans la classe {classe.nom}',
                        f"Bonjour,\n\n{user.username} vient de rejoindre votre classe {classe.nom}.\n\nCordialement,\nAgriculture 2.0",
                        settings.DEFAULT_FROM_EMAIL,
                        [classe.enseignant.email],
                        fail_silently=True,
                    )

                messages.success(request, f"🎉 Inscription réussie ! Bienvenue {user.username} !")
                return redirect('vegetables_fruits:login')
            except Classe.DoesNotExist:
                messages.error(request, "❌ Code de classe invalide. Vérifie auprès de ton professeur.")
        else:
            messages.error(request, "Erreur dans le formulaire. Vérifie les champs.")
    else:
        form = InscriptionEleveForm()

    return render(request, 'vegetables_fruits/inscription_eleve.html', {'form': form})


# Ajouter une notification quand un élève débloque un badge
def ajouter_points_eleve(eleve, points):
    """Ajoute des points à un élève et vérifie les badges"""
    eleve.points += points
    mettre_a_jour_progres_defi(eleve, 'points', points)
    nouveau_niveau = eleve.points // 100 + 1

    if nouveau_niveau > eleve.niveau:
        eleve.niveau = nouveau_niveau

        # ✅ NOTIFICATION POUR L'ENSEIGNANT
        creer_notification(
            eleve.classe.enseignant,
            'point_fort',
            f"⭐ {eleve.user.username} passe niveau {nouveau_niveau} !",
            f"{eleve.user.username} a atteint le niveau {nouveau_niveau} avec {eleve.points} points !",
            f"/dashboard-enseignant/"
        )

    eleve.save()


@login_required
def notifications_page(request):
    """Page affichant toutes les notifications"""
    if not request.user.is_enseignant:
        messages.error(request, "Accès non autorisé")
        return redirect('vegetables_fruits:index')

    notifications = NotificationEnseignant.objects.filter(enseignant=request.user)

    return render(request, 'vegetables_fruits/notifications.html', {
        'notifications': notifications
    })




# Configuration Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# --- PAGE TARIFICATION ---

def tarification(request):
    """Affiche la page des offres"""

    from datetime import date
    # Vérifier si l'utilisateur est mineur
    mineur = False
    if request.user.is_authenticated and request.user.birth_date:
        age = (date.today() - request.user.birth_date).days // 365
        mineur = age < 18

    plans = PlanTarification.objects.filter(actif=True).order_by('prix_mensuel')

    # Vérifier si l'utilisateur a déjà un abonnement
    abonnement_actif = None
    if request.user.is_authenticated:
        try:
            abonnement_actif = request.user.abonnement
        except Abonnement.DoesNotExist:
            pass

    context = {
        'plans': plans,
        'abonnement_actif': abonnement_actif,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'mineur': mineur,
    }
    return render(request, 'vegetables_fruits/tarification.html', context)


# --- CRÉATION SESSION STRIPE ---

@login_required
def create_checkout_session(request):
    """Crée une session de paiement Stripe Checkout"""

    # ✅ Récupérer le plan (GET ou POST)
    if request.method == 'POST':
        plan_identifier = request.POST.get('plan')
        frequence = request.POST.get('frequence', 'MENSUEL')
    else:
        plan_identifier = request.GET.get('plan')
        frequence = request.GET.get('frequence', 'MENSUEL')

    # ✅ Chercher le plan par nom
    plan = get_object_or_404(PlanTarification, nom__iexact=plan_identifier, actif=True)

    # Récupérer le price_id selon la fréquence
    if frequence == 'ANNUEL':
        price_id = plan.stripe_price_id_annuel
        mode = 'payment'
    else:
        price_id = plan.stripe_price_id_mensuel
        mode = 'subscription'

    if not price_id:
        messages.error(request, f"Le prix pour le plan {plan.get_nom_display()} n'est pas configuré.")
        return redirect('vegetables_fruits:tarification')

    # ✅ Vérification accès mineurs (autorisation parentale)
    if est_mineur(request.user):
        autorisation_valide = request.user.autorisations_achat.filter(
            statut='validee',
            date_expiration__gt=timezone.now()
        ).first()

        if not autorisation_valide:
            messages.warning(
                request,
                "🔒 Tu dois d'abord obtenir l'autorisation d'un parent "
                "avant de pouvoir souscrire à un abonnement."
            )
            url_demande = reverse('vegetables_fruits:demander_autorisation_achat')
            return redirect(f"{url_demande}?plan={plan_identifier}&frequence={frequence}")

    try:
        # ✅ ÉTAPE 1 : Récupérer ou créer le customer Stripe
        customer_id = None
        try:
            abonnement = request.user.abonnement
            customer_id = abonnement.stripe_customer_id
        except Abonnement.DoesNotExist:
            pass

        if not customer_id:
            # Créer un nouveau customer Stripe
            customer = stripe.Customer.create(
                email=request.user.email,
                name=request.user.username,
                metadata={'user_id': request.user.id},
            )
            customer_id = customer.id

        # ✅ ÉTAPE 2 : Construire les métadonnées
        metadata = {
            'user_id': request.user.id,
            'plan_id': plan.id,
            'frequence': frequence,
            'customer_id': customer_id,
        }

        # ✅ ÉTAPE 3 : Ajouter les métadonnées d'autorisation parentale si applicable
        if est_mineur(request.user):
            autorisation = request.user.autorisations_achat.filter(
                statut='validee',
                date_expiration__gt=timezone.now()
            ).first()
            if autorisation:
                metadata['autorisation_id'] = autorisation.id
                metadata['parent_email'] = autorisation.parent_email
                metadata['mineur'] = 'True'

        # ✅ ÉTAPE 4 : Créer la session Stripe Checkout
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode=mode,
            success_url=request.build_absolute_uri('/abonnement/succes/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/tarification/'),
            customer=customer_id,
            metadata=metadata,
        )
        return redirect(checkout_session.url)

    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return redirect('vegetables_fruits:tarification')


def _souscrire_gratuit(request, plan):
    """Active un abonnement gratuit sans paiement"""
    user = request.user
    from datetime import date

    # Vérifier si a déjà utilisé l'essai gratuit
    if user.essai_gratuit_utilise:
        messages.warning(request, "Vous avez déjà utilisé votre offre gratuite.")
        return redirect('vegetables_fruits:tarification')

    # Désactiver l'ancien abonnement si existant
    try:
        ancien_abo = user.abonnement
        ancien_abo.statut = 'ANNULE'
        ancien_abo.date_fin = timezone.now()
        ancien_abo.save()
    except Abonnement.DoesNotExist:
        pass

    # Créer le nouvel abonnement gratuit
    abonnement = Abonnement.objects.create(
        utilisateur=user,
        plan=plan,
        statut='ACTIF' if plan.nom == 'GRATUIT' else 'ESSAI',
        frequence='MENSUEL',
        date_fin=timezone.now() + timedelta(days=30) if plan.nom != 'GRATUIT' else None,
    )

    user.essai_gratuit_utilise = True
    user.save()

    messages.success(request, f"Vous êtes maintenant sur le plan {plan.get_nom_display()} !")

    # === REDIRECTION INTELLIGENTE ===
    # Enseignant
    if user.is_enseignant:
        return redirect('vegetables_fruits:dashboard_enseignant')

    # Élève (mineur avec classe)
    if hasattr(user, 'profil_eleve') and user.profil_eleve and user.profil_eleve.classe:
        return redirect('vegetables_fruits:profile')

    # Mineur sans classe ou majeur
    return redirect('vegetables_fruits:profile')


# --- SUCCÈS PAIEMENT ---

from django.db import transaction

@login_required
def abonnement_succes(request):
    import stripe
    from django.conf import settings
    from .models import Abonnement, PlanTarification, CustomUser
    from django.utils import timezone

    stripe.api_key = settings.STRIPE_SECRET_KEY

    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "Session de paiement invalide.")
        return redirect('vegetables_fruits:profile')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == 'paid':
            user_id = int(session.metadata.get('user_id'))
            plan_id = int(session.metadata.get('plan_id'))
            frequence = session.metadata.get('frequence', 'MENSUEL')

            with transaction.atomic():
                user = CustomUser.objects.select_for_update().get(id=user_id)
                plan = PlanTarification.objects.select_for_update().get(id=plan_id)
                user.refresh_from_db()
                plan.refresh_from_db()

                Abonnement.objects.filter(utilisateur=user).delete()
                abonnement = Abonnement.objects.create(
                    utilisateur=user,
                    plan=plan,
                    statut='ACTIF',
                    frequence=frequence,
                    stripe_customer_id=session.customer,
                    stripe_subscription_id=session.subscription,
                    date_debut=timezone.now(),
                )
            messages.success(request, f"Abonnement {plan.get_nom_display()} activé !")
        else:
            messages.error(request, "Le paiement n'a pas été confirmé.")
    except Exception as e:
        messages.error(request, f"Erreur lors de l'activation : {str(e)}")

    return redirect('vegetables_fruits:profile')


# --- PORTAIL CLIENT STRIPE (gérer son abonnement) ---

@login_required
def stripe_portal(request):
    """Redirige vers le portail client Stripe"""
    try:
        abonnement = request.user.abonnement
        customer_id = abonnement.stripe_customer_id or request.user.stripe_customer_id
    except Abonnement.DoesNotExist:
        messages.error(request, "Vous n'avez pas d'abonnement actif.")
        return redirect('vegetables_fruits:tarification')

    if not customer_id:
        messages.error(request, "Aucun compte de paiement trouvé.")
        return redirect('vegetables_fruits:tarification')

    try:
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=request.build_absolute_uri('/profile/'),
        )
        return redirect(session.url)
    except Exception as e:
        messages.error(request, f"Erreur d'accès au portail : {str(e)}")
        return redirect('vegetables_fruits:profile')


# --- WEBHOOK STRIPE ---

@csrf_exempt
def stripe_webhook(request):
    """
    Webhook Stripe : reçoit les événements de paiement.

    ⚠️ IMPORTANT : les objets Stripe (metadata, invoice, etc.) ne supportent PAS
    la méthode .get() comme les dictionnaires Python. Il faut convertir en dict()
    ou utiliser la syntaxe obj['key'] avec vérification 'in'.
    """
    import stripe
    from django.conf import settings
    from .models import Abonnement, PlanTarification, CustomUser
    from django.utils import timezone

    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    # ✅ Vérification de la signature Stripe
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        logger.error("❌ Webhook : payload invalide")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("❌ Webhook : signature invalide")
        return HttpResponse(status=400)

    logger.info(f"🔔 Webhook reçu : {event['type']}")

    # ============================================================
    # ✅ ÉVÉNEMENT : Paiement Checkout complété
    # ============================================================
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # ✅ Convertir les metadata Stripe en dict Python
        if session.metadata:
            try:
                metadata = session.metadata.to_dict()
            except Exception:
                metadata = dict(session.metadata._data) if hasattr(session.metadata, '_data') else {}
        else:
            metadata = {}

        if 'user_id' not in metadata or 'plan_id' not in metadata:
            logger.error(f"❌ Webhook : métadonnées manquantes (metadata={metadata})")
            return HttpResponse(status=400)

        try:
            user_id = int(metadata['user_id'])
            plan_id = int(metadata['plan_id'])
            frequence = metadata.get('frequence', 'MENSUEL')

            user = CustomUser.objects.get(id=user_id)
            plan = PlanTarification.objects.get(id=plan_id)

            # ✅ ÉTAPE 1 : Récupérer ou créer l'abonnement (OneToOneField)
            abonnement, created = Abonnement.objects.get_or_create(
                utilisateur=user,
                defaults={
                    'plan': plan,
                    'statut': 'ACTIF',
                    'frequence': frequence,
                    'stripe_customer_id': session.customer,
                    'stripe_subscription_id': session.subscription,
                    'date_debut': timezone.now(),
                }
            )

            if not created:
                # ✅ Mise à jour de l'abonnement existant
                abonnement.plan = plan
                abonnement.statut = 'ACTIF'
                abonnement.frequence = frequence
                abonnement.stripe_customer_id = session.customer
                abonnement.stripe_subscription_id = session.subscription
                abonnement.date_debut = timezone.now()
                abonnement.date_fin = None
                abonnement.save()
                logger.info(f" 🔄 Abo {plan.nom} mis à jour pour {user.username}")
            else:
                logger.info(f" ✅ Abo {plan.nom} créé pour {user.username}")

            # ✅ ÉTAPE 2 : Log si autorisation parentale utilisée
            if 'autorisation_id' in metadata:
                logger.debug(f" 🔒 Autorisation parentale utilisée (id={metadata['autorisation_id']})")

        except (CustomUser.DoesNotExist, PlanTarification.DoesNotExist) as e:
            logger.error(f"❌ Webhook : utilisateur ou plan introuvable : {e}")
            return HttpResponse(status=400)
        except Exception as e:
            logger.error(f"❌ Webhook : erreur inattendue : {e}")
            return HttpResponse(status=500)

    # ============================================================
    # ✅ ÉVÉNEMENT : Facture payée
    # ============================================================
    elif event['type'] == 'invoice.paid':
        invoice = event['data']['object']

        # ✅ Récupérer le subscription_id en toute sécurité
        subscription_id = invoice['subscription'] if 'subscription' in invoice else None

        if subscription_id:
            try:
                abonnement = Abonnement.objects.get(stripe_subscription_id=subscription_id)
                abonnement.date_prochain_paiement = timezone.now() + timezone.timedelta(days=30)
                abonnement.statut = 'ACTIF'
                abonnement.save()
                logger.info(f" 💰 Facture payée pour {abonnement.utilisateur.username}")
            except Abonnement.DoesNotExist:
                logger.warning(f" ⚠️ Abonnement {subscription_id} introuvable")
        else:
            logger.warning(f" ⚠️ Pas de subscription_id dans la facture")

    # ============================================================
    # ✅ ÉVÉNEMENT : Facture payée (alternative récente)
    # ============================================================
    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        subscription_id = invoice['subscription'] if 'subscription' in invoice else None

        if subscription_id:
            try:
                abonnement = Abonnement.objects.get(stripe_subscription_id=subscription_id)
                abonnement.date_prochain_paiement = timezone.now() + timezone.timedelta(days=30)
                abonnement.statut = 'ACTIF'
                abonnement.save()
                logger.info(f" 💰 Paiement réussi pour {abonnement.utilisateur.username}")
            except Abonnement.DoesNotExist:
                logger.warning(f" ⚠️ Abonnement {subscription_id} introuvable")

    # ============================================================
    # ✅ ÉVÉNEMENT : Facture échouée
    # ============================================================
    elif event['type'] == 'invoice.payment_failed':
        invoice = event['data']['object']
        subscription_id = invoice['subscription'] if 'subscription' in invoice else None

        if subscription_id:
            try:
                abonnement = Abonnement.objects.get(stripe_subscription_id=subscription_id)
                abonnement.statut = 'EXPIRE'
                abonnement.save()
                logger.warning(f" ❌ Paiement échoué pour {abonnement.utilisateur.username}")
            except Abonnement.DoesNotExist:
                logger.warning(f" ⚠️ Abonnement {subscription_id} introuvable")

    # ============================================================
    # ✅ ÉVÉNEMENT : Abonnement supprimé (résiliation)
    # ============================================================
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        subscription_id = subscription['id'] if 'id' in subscription else None

        if subscription_id:
            try:
                abonnement = Abonnement.objects.get(stripe_subscription_id=subscription_id)
                abonnement.statut = 'ANNULE'
                abonnement.date_fin = timezone.now()
                abonnement.save()
                logger.info(f" 🔓 Abonnement annulé pour {abonnement.utilisateur.username}")
            except Abonnement.DoesNotExist:
                logger.warning(f" ⚠️ Abonnement {subscription_id} introuvable")

    # ============================================================
    # ✅ ÉVÉNEMENT : Abonnement mis à jour
    # ============================================================
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        subscription_id = subscription['id'] if 'id' in subscription else None
        statut_stripe = subscription['status'] if 'status' in subscription else None
        # ✅ Nouvelle API Stripe : cancel_at + canceled_at
        cancel_at = subscription['cancel_at'] if 'cancel_at' in subscription else None
        canceled_at = subscription['canceled_at'] if 'canceled_at' in subscription else None

        # ✅ Récupérer current_period_end depuis items (nouvelle API)
        current_period_end = None
        if 'items' in subscription and 'data' in subscription['items']:
            items_data = subscription['items']['data']
            if items_data and len(items_data) > 0:
                first_item = items_data[0]
                if 'current_period_end' in first_item:
                    current_period_end = first_item['current_period_end']

        # ✅ Détecter la résiliation programmée
        # Elle est active si cancel_at est défini ET canceled_at est défini
        if cancel_at and canceled_at:
            resiliation_programmee = True
            date_fin_prevue_ts = cancel_at
        elif cancel_at and not canceled_at:
            # cancel_at seul = programmée plus tard
            resiliation_programmee = True
            date_fin_prevue_ts = cancel_at
        else:
            resiliation_programmee = False
            date_fin_prevue_ts = None

        if subscription_id:
            try:
                abonnement = Abonnement.objects.get(stripe_subscription_id=subscription_id)

                # ✅ Statut
                if statut_stripe == 'active':
                    abonnement.statut = 'ACTIF'
                elif statut_stripe == 'past_due':
                    abonnement.statut = 'EXPIRE'
                elif statut_stripe == 'unpaid':
                    abonnement.statut = 'EXPIRE'
                elif statut_stripe == 'canceled':
                    abonnement.statut = 'ANNULE'
                    abonnement.date_fin = timezone.now()
                elif statut_stripe == 'incomplete':
                    abonnement.statut = 'EN_ATTENTE'
                elif statut_stripe == 'incomplete_expired':
                    abonnement.statut = 'ANNULE'
                    abonnement.date_fin = timezone.now()

                # ✅ Résiliation programmée
                abonnement.resiliation_programmee = resiliation_programmee

                if resiliation_programmee and date_fin_prevue_ts:
                    from datetime import timezone as dt_timezone
                    abonnement.date_fin_prevue = datetime.fromtimestamp(date_fin_prevue_ts, tz=dt_timezone.utc)
                    logger.info(f" ⏸️ Résiliation programmée pour le {abonnement.date_fin_prevue.strftime('%d/%m/%Y')}")
                else:
                    abonnement.date_fin_prevue = None

                abonnement.save()
                logger.info(f" 🔄 Abonnement {subscription_id} → {abonnement.statut}")

            except Abonnement.DoesNotExist:
                logger.warning(f" ⚠️ Abonnement {subscription_id} introuvable")

    # ============================================================
    # Toujours retourner 200 pour éviter les retry infinis de Stripe
    # ============================================================
    return HttpResponse(status=200)


def _handle_checkout_completed(session):
    """Traite une session de paiement complétée"""
    user_id = session.get('metadata', {}).get('user_id')
    if user_id:
        try:
            user = CustomUser.objects.get(id=user_id)
            _activer_abonnement_depuis_session(user, session)
        except CustomUser.DoesNotExist:
            pass


def _handle_invoice_paid(invoice):
    """Enregistre une facture payée"""
    customer_id = invoice.get('customer')
    subscription_id = invoice.get('subscription')

    try:
        abonnement = Abonnement.objects.filter(stripe_subscription_id=subscription_id).first()
        if abonnement:
            Facture.objects.update_or_create(
                stripe_invoice_id=invoice['id'],
                defaults={
                    'utilisateur': abonnement.utilisateur,
                    'abonnement': abonnement,
                    'montant_ht': invoice['subtotal'] / 100,
                    'montant_ttc': invoice['total'] / 100,
                    'statut': 'PAYEE',
                    'date_paiement': datetime.fromtimestamp(invoice['status_transitions']['paid_at']),
                }
            )
    except Abonnement.DoesNotExist:
        pass


def _handle_invoice_failed(invoice):
    """Gère un échec de paiement"""
    subscription_id = invoice.get('subscription')
    try:
        abonnement = Abonnement.objects.get(stripe_subscription_id=subscription_id)
        abonnement.statut = 'EXPIRE'
        abonnement.save()
    except Abonnement.DoesNotExist:
        pass


def _handle_subscription_deleted(subscription):
    """Gère l'annulation d'un abonnement"""
    try:
        abonnement = Abonnement.objects.get(stripe_subscription_id=subscription['id'])
        abonnement.statut = 'ANNULE'
        abonnement.date_fin = timezone.now()
        abonnement.save()
    except Abonnement.DoesNotExist:
        pass


def _handle_subscription_updated(subscription):
    """Gère la mise à jour d'un abonnement"""
    try:
        abonnement = Abonnement.objects.get(stripe_subscription_id=subscription['id'])
        statut_stripe = subscription.get('status')
        if statut_stripe == 'active':
            abonnement.statut = 'ACTIF'
        elif statut_stripe == 'past_due':
            abonnement.statut = 'EXPIRE'
        abonnement.save()
    except Abonnement.DoesNotExist:
        pass


@login_required
def reactiver_abonnement(request):
    """
    Réactive un abonnement programmé pour annulation.
    Appelle l'API Stripe pour annuler la résiliation programmée.
    """
    import stripe
    from django.conf import settings

    try:
        abonnement = request.user.abonnement
    except Abonnement.DoesNotExist:
        messages.error(request, "Vous n'avez pas d'abonnement à réactiver.")
        return redirect('vegetables_fruits:profile')

    if not abonnement.stripe_subscription_id:
        messages.error(request, "Aucun abonnement Stripe associé à votre compte.")
        return redirect('vegetables_fruits:profile')

    if not abonnement.resiliation_programmee:
        messages.info(request, "Votre abonnement est déjà actif.")
        return redirect('vegetables_fruits:profile')

    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # ✅ Réactiver l'abonnement côté Stripe
        stripe.Subscription.modify(
            abonnement.stripe_subscription_id,
            cancel_at_period_end=False
        )

        # ✅ Mettre à jour en base immédiatement
        # (le webhook le fera aussi, mais autant être réactif)
        abonnement.resiliation_programmee = False
        abonnement.date_fin_prevue = None
        abonnement.save()

        messages.success(
            request,
            "✅ Votre abonnement a été réactivé avec succès. Il continuera automatiquement."
        )
        logger.info(f"✅ Abonnement {abonnement.stripe_subscription_id} réactivé pour {request.user.username}")


    except stripe.error.StripeError as e:
        messages.error(request, f"Erreur Stripe : {str(e)}")
        logger.error(f"❌ Erreur Stripe réactivation : {e}")

    except Exception as e:
        messages.error(request, f"Erreur : {str(e)}")
        logger.error(f"❌ Erreur réactivation : {e}")


    return redirect('vegetables_fruits:profile')


# --- FONCTIONS UTILITAIRES ---

def _get_or_create_stripe_customer(user):
    """Récupère ou crée le customer Stripe"""
    if user.stripe_customer_id:
        return user.stripe_customer_id

    customer = stripe.Customer.create(
        email=user.email,
        name=user.get_full_name() or user.username,
        metadata={'user_id': user.id},
    )

    user.stripe_customer_id = customer.id
    user.save()

    return customer.id


def _activer_abonnement_depuis_session(user, session):
    """Active un abonnement après un paiement réussi"""
    logger.debug("USER:", user)

    logger.debug("SESSION", session)

    metadata = dict(session.metadata)
    logger.debug("METADATA", metadata)

    plan_id = metadata.get('plan_id')
    logger.debug("PLAN ID", plan_id)


    if not plan_id:
        logger.debug("PAS DE PLAN ID DNAS LES METADATA")

        return None
    frequence = metadata.get('frequence', 'MENSUEL')
    est_groupe_scolaire = metadata.get('est_groupe_scolaire') == 'True'
    reduction = int(metadata.get('reduction', 0))

    plan = PlanTarification.objects.get(id=plan_id)

    # Désactiver l'ancien abonnement
    try:
        ancien_abo = user.abonnement
        ancien_abo.statut = 'ANNULE'
        ancien_abo.date_fin = timezone.now()
        ancien_abo.save()
    except Abonnement.DoesNotExist:
        pass

    # Créer le nouvel abonnement
    abonnement = Abonnement.objects.create(
        utilisateur=user,
        plan=plan,
        statut='ACTIF',
        frequence=frequence,
        stripe_customer_id=session.customer,
        stripe_subscription_id=session.subscription,
        est_groupe_scolaire=est_groupe_scolaire,
        reduction_appliquee=reduction,
    )

    logger.debug("ABONNEMENT CREE:", abonnement)


    return abonnement


# --- VÉRIFICATEUR DE QUOTA (à utiliser dans les vues existantes) ---

def verifier_quota_parcelles(user):
    """
    Vérifie si l'utilisateur peut encore créer des parcelles.
    Retourne (peut_creer, message)
    """
    try:
        abonnement = user.abonnement
        if not abonnement.est_actif:
            return False, "Votre abonnement n'est plus actif."

        compte = GeometricFigure.objects.filter(user=user).count()
        max_parcelles = abonnement.plan.max_parcelles

        # ✅ LOGS POUR DÉBOGUER
        logger.debug(f"🔍 Quota - User: {user.username}")

        logger.debug(f" Plan: {abonnement.plan.nom}")

        logger.debug(f" Max parcelles: {max_parcelles}")

        logger.debug(f" Parcelles actuelles: {compte}")


        if compte >= max_parcelles:
            return False, 'limite'

        return True, ""

    except Abonnement.DoesNotExist:
        # Pas d'abonnement = plan gratuit par défaut
        plan_gratuit = PlanTarification.objects.filter(nom='GRATUIT').first()
        if plan_gratuit:
            compte = GeometricFigure.objects.filter(user=user).count()
            if compte >= plan_gratuit.max_parcelles:
                return False, 'limite'
        return True, ""


# --- DOCUMENTS JURIDIQUES ---

def cgu(request):
    """Page des Conditions Générales d'Utilisation"""
    return render(request, 'vegetables_fruits/cgu.html')


def confidentialite(request):
    """Page de la Politique de Confidentialité"""
    return render(request, 'vegetables_fruits/confidentialite.html')


@login_required
def consentement_rgpd(request):
    """Enregistrement du consentement RGPD"""
    if request.method == 'POST':
        est_mineur = request.POST.get('est_mineur') == 'on'

        consentement = ConsentementRGPD.objects.create(
            utilisateur=request.user,
            cgu_acceptees=request.POST.get('cgu') == 'on',
            politique_confidentialite_acceptee=request.POST.get('confidentialite') == 'on',
            consentement_donnees=request.POST.get('donnees') == 'on',
            consentement_marketing=request.POST.get('marketing') == 'on',
            est_mineur=est_mineur,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
        )

        # Si mineur, ajouter les infos parentales
        if est_mineur and request.POST.get('parent_consent') == 'on':
            consentement.representant_legal_nom = request.POST.get('parent_nom', '')
            consentement.representant_legal_prenom = request.POST.get('parent_prenom', '')
            consentement.representant_legal_email = request.POST.get('parent_email', '')
            consentement.representant_legal_telephone = request.POST.get('parent_tel', '')
            consentement.date_consentement_parental = timezone.now()
            consentement.save()

        messages.success(request, "Vos consentements ont bien été enregistrés. Merci !")
        return redirect('vegetables_fruits:dashboard')

    # Vérifier si déjà consenti
    consentement_existant = ConsentementRGPD.objects.filter(
        utilisateur=request.user
    ).order_by('-date_consentement').first()

    if consentement_existant:
        messages.info(request, "Vous avez déjà donné vos consentements.")

    return render(request, 'vegetables_fruits/consentement.html', {
        'consentement_existant': consentement_existant,
    })

# POUR MIGRATION MAPBOX

def geocode_mapbox(request):
    """Proxy pour géocodage Mapbox"""
    query = request.GET.get('q', '')
    mode = request.GET.get('mode', 'search')
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    token = settings.MAPBOX_TOKEN

    if mode == 'reverse' and lat and lng:
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{lng},{lat}.json?access_token={token}&limit=1&language=fr"
    elif query:
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{query}.json?access_token={token}&limit=5&language=fr"
    else:
        return JsonResponse({'error': 'Paramètres invalides'}, status=400)

    response = requests.get(url)
    return JsonResponse(response.json())

@login_required
def limite_parcelles(request):
    """Page affichée quand l'utilisateur a atteint sa limite de parcelles"""
    from .models import GeometricFigure

    abonnement = None
    nb_parcelles = GeometricFigure.objects.filter(user=request.user).count()
    max_parcelles = 3  # Valeur par défaut (Gratuit)

    try:
        abonnement = request.user.abonnement
        if abonnement and abonnement.est_actif:
            max_parcelles = abonnement.plan.max_parcelles
    except:
        pass

    return render(request, 'vegetables_fruits/limite_parcelles.html', {
        'abonnement': abonnement,
        'nb_parcelles': nb_parcelles,
        'max_parcelles': max_parcelles,
    })


@login_required
def recolter_culture(request):
    """Marque une culture comme récoltée et donne des points"""
    if request.method == 'POST':
        chrono_id = request.POST.get('chrono_id')
        from datetime import date

        chrono = get_object_or_404(ChronologieCulture, id=chrono_id, figure__user=request.user)
        chrono.date_recolte_effective = date.today()
        chrono.statut = 'recolte'
        chrono.progression = 100
        chrono.points_gagnes = 10
        chrono.save()

        if request.user.mode_junior and hasattr(request.user, 'profil_eleve'):
            eleve = request.user.profil_eleve
            eleve.ajouter_points(10, action_type='recolter')
            mettre_a_jour_progres_defi(eleve, 'recolter')
            verifier_competences(eleve) # ← AJOUT

            if chrono.culture_nom and 'fleur' in chrono.culture_nom.lower():
                eleve.ajouter_points(5, action_type='recolter_fleur')
                messages.success(request, f"🌸 +5 points bonus pour récolte de fleur !")

        messages.success(request, f"🧺 {chrono.culture_nom} récolté ! +10 points !")
        return redirect('vegetables_fruits:figure_detail', figure_id=chrono.figure.id)

    return redirect('vegetables_fruits:view_figure')

from django.core.cache import cache
def meteo_mapbox(request):
    try:
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        cache_key = f"meteo_{lat}_{lon}"

        # Verifier le cahce
        cached_data = cache.get(cache_key)
        if cached_data:
            return JsonResponse(cached_data)


        if not lat or not lon:
            return JsonResponse({'error': 'Latitude et longitude requises'}, status=400)

        api_key = settings.OPENWEATHER_API_KEY
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=fr&appid={api_key}"

        response = requests.get(url)
        data = response.json()

        result = {
            'properties': {
                'temp': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'conditions': data['weather'][0]['description'],
                'icon': data['weather'][0]['main']
            }
        }
        # Mettre en cache pendant 10min
        cache.set(cache_key, result, 60 * 10)
        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@login_required
def ajouter_fleur(request, figure_id):
    """Ajoute une fleur pollinisatrice sur une parcelle"""
    figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)

    # ✅ Récupérer les cultures existantes
    cultures_existantes = []
    if figure.crops:
        for crop in figure.crops:
            if 'name' in crop:
                cultures_existantes.append(crop['name'].lower())

    # ✅ Récupérer la région et le climat
    region_info = get_region_utilisateur(request.user, figure)
    region = region_info.get('region', 'iledefrance')
    climat = 'tempere'
    if figure.adresse_lat and figure.adresse_lng:
        climat = get_climat_mondial(figure.adresse_lat, figure.adresse_lng)

    # ✅ Suggérer des fleurs en fonction des cultures et du climat
    fleurs_suggerees = get_fleurs_suggerées(cultures_existantes, climat)

    # ✅ Liste des 35 fleurs pollinisatrices essentielles
    FLEURS_DISPONIBLES = [
        # ==================== FLEURS SAUVAGES & INDIGÈNES (20) ====================
        {'nom': 'Achillée millefeuille', 'emoji': '🌼'},
        {'nom': 'Centaurée bleuet', 'emoji': '🌸'},
        {'nom': 'Coquelicot', 'emoji': '🌺'},
        {'nom': 'Marguerite', 'emoji': '🌼'},
        {'nom': 'Pissenlit', 'emoji': '🌼'},
        {'nom': 'Trèfle blanc', 'emoji': '🍀'},
        {'nom': 'Trèfle rouge', 'emoji': '🍀'},
        {'nom': 'Luzerne', 'emoji': '🌿'},
        {'nom': 'Sainfoin', 'emoji': '🌸'},
        {'nom': 'Vesce', 'emoji': '🌿'},
        {'nom': 'Mélilot', 'emoji': '🌼'},
        {'nom': 'Bourrache', 'emoji': '💙'},
        {'nom': 'Consoude', 'emoji': '💜'},
        {'nom': 'Échinacée', 'emoji': '🌸'},
        {'nom': 'Rudbeckie', 'emoji': '🌼'},
        {'nom': 'Zinnia', 'emoji': '🌸'},
        {'nom': 'Cosmos', 'emoji': '🌸'},
        {'nom': 'Gaillarde', 'emoji': '🌼'},
        {'nom': 'Verveine', 'emoji': '💜'},
        {'nom': 'Phacélie', 'emoji': '💜'},

        # ==================== AROMATIQUES & MÉDICINALES (12) ====================
        {'nom': 'Lavande', 'emoji': '💜'},
        {'nom': 'Romarin', 'emoji': '🌿'},
        {'nom': 'Thym', 'emoji': '🌿'},
        {'nom': 'Sauge', 'emoji': '🌿'},
        {'nom': 'Origan', 'emoji': '🌿'},
        {'nom': 'Marjolaine', 'emoji': '🌿'},
        {'nom': 'Menthe', 'emoji': '🌿'},
        {'nom': 'Mélisse', 'emoji': '🌿'},
        {'nom': 'Angélique', 'emoji': '🌿'},
        {'nom': 'Fenouil', 'emoji': '🌿'},
        {'nom': 'Aneth', 'emoji': '🌿'},
        {'nom': 'Coriandre', 'emoji': '🌿'},

        # ==================== FLEURS ORNEMENTALES & VIVACES (13) ====================
        {'nom': 'Rose', 'emoji': '🌹'},
        {'nom': 'Tulipe', 'emoji': '🌷'},
        {'nom': 'Jonquille', 'emoji': '💛'},
        {'nom': 'Iris', 'emoji': '🌸'},
        {'nom': 'Pivoine', 'emoji': '🌺'},
        {'nom': 'Hortensia', 'emoji': '💐'},
        {'nom': 'Jasmin', 'emoji': '🌸'},
        {'nom': 'Chèvrefeuille', 'emoji': '🌸'},
        {'nom': 'Buddleia', 'emoji': '💜'},
        {'nom': 'Lilas', 'emoji': '💜'},
        {'nom': 'Clématite', 'emoji': '💜'},
        {'nom': 'Glycine', 'emoji': '💜'},
        {'nom': 'Chardon', 'emoji': '🌼'},

        # ==================== FLEURS MÉDITERRANÉENNES (3) ====================
        {'nom': 'Ciste', 'emoji': '🌸'},
        {'nom': 'Lavande papillon', 'emoji': '💜'},
        {'nom': 'Romarin', 'emoji': '🌿'},  # Déjà dans aromatiques

        # ==================== FLEURS TROPICALES & EXOTIQUES (12) ====================
        {'nom': 'Hibiscus', 'emoji': '🌺'},
        {'nom': 'Bougainvillier', 'emoji': '🌸'},
        {'nom': 'Plumeria', 'emoji': '🌸'},
        {'nom': 'Lantana', 'emoji': '🌸'},
        {'nom': 'Passiflore', 'emoji': '🌸'},
        {'nom': 'Frangipanier', 'emoji': '🌸'},
        {'nom': 'Allamanda', 'emoji': '🌸'},
        {'nom': 'Ixora', 'emoji': '🌸'},
        {'nom': 'Heliconia', 'emoji': '🌺'},
        {'nom': 'Gingembre ornemental', 'emoji': '🌸'},
        {'nom': 'Strelitzia', 'emoji': '🌺'},
        {'nom': 'Protea', 'emoji': '🌺'},

        # ==================== FLEURS À SEMIS FACILE (7) ====================
        {'nom': 'Œillet d\'Inde', 'emoji': '🌸'},
        {'nom': 'Capucine', 'emoji': '🌸'},
        {'nom': 'Souci', 'emoji': '🌼'},
        {'nom': 'Nigelle de Damas', 'emoji': '💙'},
        {'nom': 'Pois de senteur', 'emoji': '🌸'},
        {'nom': 'Belle-de-jour', 'emoji': '🌸'},
        {'nom': 'Pavot de Californie', 'emoji': '🌼'},

        # ==================== FLEURS DE JARDIN POTAGER (8) ====================
        {'nom': 'Tournesol', 'emoji': '🌻'},
        {'nom': 'Courge', 'emoji': '🌼'},
        {'nom': 'Cucurbitacées', 'emoji': '🌼'},
        {'nom': 'Haricot', 'emoji': '🌸'},
        {'nom': 'Pois', 'emoji': '🌸'},
        {'nom': 'Fève', 'emoji': '🌸'},
        {'nom': 'Aubergine', 'emoji': '🌸'},
        {'nom': 'Tomate', 'emoji': '🌸'},
    ]

    if request.method == 'POST':
        fleur_nom = request.POST.get('fleur_nom')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')

        if not fleur_nom or not lat or not lng:
            messages.error(request, "Veuillez sélectionner une fleur et cliquer sur la carte.")
            return redirect('vegetables_fruits:ajouter_fleur', figure_id=figure.id)

        # ✅ Récupérer l'emoji depuis la liste
        fleur_trouvee = next((f for f in FLEURS_DISPONIBLES if f['nom'] == fleur_nom), None)
        fleur_emoji = fleur_trouvee['emoji'] if fleur_trouvee else '🌻'

        nouvelles_cultures = figure.crops or []
        nouvelles_cultures.append({
            'name': fleur_nom,
            'type': 'fleur',
            'est_pollinisatrice': True,
            'emoji': fleur_emoji,
            'lat': float(lat),
            'lng': float(lng),
            'date_plantation': date.today().isoformat()
        })
        figure.crops = nouvelles_cultures
        figure.save()

        if request.user.mode_junior and hasattr(request.user, 'profil_eleve'):
            eleve = request.user.profil_eleve
            eleve.ajouter_points(8, action_type='planter_fleur')
            mettre_a_jour_progres_defi(eleve, 'fleur')
            verifier_competences(eleve)
            messages.success(request, f"🌼 +8 points ! {fleur_emoji} {fleur_nom} plantée !")
        else:
            messages.success(request, f"🌼 {fleur_emoji} {fleur_nom} plantée avec succès !")

        return redirect('vegetables_fruits:figure_detail', figure_id=figure.id)

    return render(request, 'vegetables_fruits/ajouter_fleur.html', {
        'figure': figure,
        'mapbox_token': settings.MAPBOX_TOKEN,
        'fleurs': FLEURS_DISPONIBLES,
        'fleurs_suggerees': fleurs_suggerees,
        'cultures_existantes': cultures_existantes,
        'climat': climat,
        'region': region,
    })


def get_fleurs_suggerées(cultures, climat):
    """
    Suggère des fleurs pollinisatrices adaptées aux cultures et au climat
    Version mondiale avec mapping exhaustif
    """
    suggestions = []

    # ============================================================ #
    # MAPPING CULTURES → FLEURS COMPATIBLES (MONDIAL) #
    # ============================================================ #
    compatibilites = {
        # ==================== LÉGUMES ====================
        'tomate': ['Bourrache', 'Souci', 'Œillet d\'Inde', 'Basilic', 'Capucine'],
        'tomate cerise': ['Bourrache', 'Souci', 'Œillet d\'Inde', 'Basilic'],
        'tomate ancienne': ['Bourrache', 'Souci', 'Œillet d\'Inde', 'Basilic'],

        'carotte': ['Romarin', 'Thym', 'Sauge', 'Œillet d\'Inde', 'Souci'],
        'carotte violette': ['Romarin', 'Thym', 'Sauge', 'Œillet d\'Inde'],
        'carotte jaune': ['Romarin', 'Thym', 'Sauge', 'Souci'],

        'salade': ['Œillet d\'Inde', 'Capucine', 'Souci', 'Lavande'],
        'laitue': ['Œillet d\'Inde', 'Capucine', 'Souci'],
        'roquette': ['Œillet d\'Inde', 'Capucine', 'Souci'],
        'mâche': ['Œillet d\'Inde', 'Capucine'],

        'courgette': ['Bourrache', 'Tournesol', 'Souci', 'Œillet d\'Inde', 'Capucine'],
        'courge': ['Bourrache', 'Tournesol', 'Souci', 'Œillet d\'Inde'],
        'potiron': ['Bourrache', 'Tournesol', 'Souci', 'Œillet d\'Inde'],
        'citrouille': ['Bourrache', 'Tournesol', 'Souci', 'Œillet d\'Inde'],

        'concombre': ['Bourrache', 'Tournesol', 'Souci', 'Œillet d\'Inde'],
        'cornichon': ['Bourrache', 'Tournesol', 'Souci', 'Œillet d\'Inde'],

        'aubergine': ['Bourrache', 'Souci', 'Lavande', 'Œillet d\'Inde'],
        'aubergine blanche': ['Bourrache', 'Souci', 'Lavande'],

        'poivron': ['Bourrache', 'Souci', 'Lavande', 'Œillet d\'Inde'],
        'piment': ['Bourrache', 'Souci', 'Lavande', 'Œillet d\'Inde'],
        'piment fort': ['Bourrache', 'Souci', 'Lavande'],

        'pomme de terre': ['Œillet d\'Inde', 'Capucine', 'Souci', 'Lavande'],
        'patate douce': ['Œillet d\'Inde', 'Capucine', 'Souci'],

        'chou': ['Œillet d\'Inde', 'Capucine', 'Souci', 'Lavande'],
        'chou rouge': ['Œillet d\'Inde', 'Capucine', 'Souci'],
        'chou chinois': ['Œillet d\'Inde', 'Capucine', 'Souci'],
        'chou de bruxelles': ['Œillet d\'Inde', 'Capucine', 'Souci'],

        'brocoli': ['Œillet d\'Inde', 'Capucine', 'Souci'],
        'chou-fleur': ['Œillet d\'Inde', 'Capucine', 'Souci'],
        'chou-rave': ['Œillet d\'Inde', 'Capucine', 'Souci'],

        'oignon': ['Romarin', 'Thym', 'Sauge', 'Œillet d\'Inde'],
        'oignon rouge': ['Romarin', 'Thym', 'Sauge'],
        'oignon blanc': ['Romarin', 'Thym', 'Sauge'],
        'échalote': ['Romarin', 'Thym', 'Sauge'],

        'ail': ['Romarin', 'Thym', 'Sauge', 'Œillet d\'Inde'],
        'ail rose': ['Romarin', 'Thym', 'Sauge'],
        'ail noir': ['Romarin', 'Thym', 'Sauge'],

        'haricot': ['Bourrache', 'Souci', 'Œillet d\'Inde'],
        'haricot vert': ['Bourrache', 'Souci', 'Œillet d\'Inde'],
        'haricot rouge': ['Bourrache', 'Souci'],
        'haricot blanc': ['Bourrache', 'Souci'],
        'haricot mungo': ['Bourrache', 'Souci'],

        'pois': ['Bourrache', 'Souci', 'Œillet d\'Inde'],
        'petit pois': ['Bourrache', 'Souci'],
        'pois chiche': ['Bourrache', 'Souci', 'Œillet d\'Inde'],

        'fève': ['Bourrache', 'Souci', 'Œillet d\'Inde'],
        'lentille': ['Bourrache', 'Souci'],
        'soja': ['Bourrache', 'Souci'],

        'épinard': ['Œillet d\'Inde', 'Capucine', 'Souci'],
        'betterave': ['Œillet d\'Inde', 'Capucine', 'Souci'],
        'blette': ['Œillet d\'Inde', 'Capucine', 'Souci'],

        'radis': ['Romarin', 'Thym', 'Sauge'],
        'radis noir': ['Romarin', 'Thym', 'Sauge'],
        'radis rose': ['Romarin', 'Thym', 'Sauge'],

        'poireau': ['Romarin', 'Thym', 'Sauge'],
        'céleri': ['Œillet d\'Inde', 'Capucine', 'Souci'],
        'céleri-rave': ['Œillet d\'Inde', 'Capucine'],

        'fenouil': ['Bourrache', 'Souci', 'Lavande'],
        'asparagus': ['Lavande', 'Romarin', 'Sauge'],
        'asperge': ['Lavande', 'Romarin', 'Sauge'],

        'artichaut': ['Lavande', 'Romarin', 'Sauge'],
        'artichaut violet': ['Lavande', 'Romarin', 'Sauge'],

        'topinambour': ['Tournesol', 'Bourrache', 'Souci'],

        'panais': ['Romarin', 'Thym', 'Sauge'],
        'navet': ['Œillet d\'Inde', 'Capucine', 'Souci'],
        'rutabaga': ['Œillet d\'Inde', 'Capucine', 'Souci'],
        'salsifis': ['Romarin', 'Thym', 'Sauge'],
        'scorsonère': ['Romarin', 'Thym', 'Sauge'],

        'rhubarbe': ['Lavande', 'Romarin', 'Sauge'],
        'cresson': ['Œillet d\'Inde', 'Capucine'],

        'maïs': ['Tournesol', 'Bourrache', 'Souci', 'Œillet d\'Inde'],
        'blé': ['Coquelicot', 'Bourrache', 'Souci'],
        'riz': ['Lavande', 'Sauge', 'Romarin'],
        'orge': ['Coquelicot', 'Bourrache'],
        'avoine': ['Coquelicot', 'Bourrache'],
        'seigle': ['Coquelicot', 'Bourrache'],
        'millet': ['Bourrache', 'Tournesol'],
        'sorgho': ['Bourrache', 'Tournesol'],

        # ==================== FRUITS ====================
        'pomme': ['Lavande', 'Romarin', 'Sauge', 'Thym', 'Bourrache'],
        'poire': ['Lavande', 'Romarin', 'Sauge', 'Thym'],
        'pêche': ['Lavande', 'Romarin', 'Sauge', 'Thym'],
        'abricot': ['Lavande', 'Romarin', 'Sauge', 'Thym'],
        'cerise': ['Lavande', 'Romarin', 'Sauge', 'Thym', 'Bourrache'],
        'prune': ['Lavande', 'Romarin', 'Sauge', 'Thym'],
        'mirabelle': ['Lavande', 'Romarin', 'Sauge', 'Thym'],
        'nectarine': ['Lavande', 'Romarin', 'Sauge', 'Thym'],

        'fraise': ['Souci', 'Bourrache', 'Lavande', 'Œillet d\'Inde'],
        'framboise': ['Lavande', 'Romarin', 'Sauge', 'Bourrache'],
        'myrtille': ['Lavande', 'Romarin', 'Sauge', 'Bourrache'],
        'airelle': ['Lavande', 'Romarin', 'Sauge'],
        'groseille': ['Lavande', 'Romarin', 'Sauge'],
        'cassis': ['Lavande', 'Romarin', 'Sauge'],
        'mûre': ['Lavande', 'Romarin', 'Sauge', 'Bourrache'],

        'vigne': ['Lavande', 'Romarin', 'Sauge', 'Thym'],
        'raisin': ['Lavande', 'Romarin', 'Sauge', 'Thym'],

        'olivier': ['Lavande', 'Romarin', 'Thym', 'Sauge', 'Ciste'],
        'amandier': ['Lavande', 'Romarin', 'Thym', 'Sauge'],
        'noyer': ['Lavande', 'Romarin', 'Sauge'],
        'noisetier': ['Lavande', 'Romarin', 'Sauge'],
        'châtaignier': ['Lavande', 'Romarin', 'Sauge'],

        'citronnier': ['Lavande', 'Romarin', 'Thym', 'Sauge'],
        'oranger': ['Lavande', 'Romarin', 'Thym', 'Sauge'],
        'pamplemousse': ['Lavande', 'Romarin', 'Thym', 'Sauge'],
        'mandarine': ['Lavande', 'Romarin', 'Thym', 'Sauge'],
        'kumquat': ['Lavande', 'Romarin', 'Thym', 'Sauge'],
        'lime': ['Lavande', 'Romarin', 'Thym', 'Sauge'],

        'avocat': ['Lavande', 'Romarin', 'Sauge', 'Bourrache'],
        'kiwi': ['Lavande', 'Romarin', 'Sauge', 'Bourrache'],
        'bananier': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'ananas': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'manguier': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'papaye': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'goyave': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'litchi': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'longane': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'ramboutan': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'durian': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'jaboticaba': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'carambole': ['Hibiscus', 'Bougainvillier', 'Passiflore'],

        'melon': ['Bourrache', 'Tournesol', 'Souci'],
        'pastèque': ['Bourrache', 'Tournesol', 'Souci'],
        'kiwano': ['Bourrache', 'Tournesol', 'Souci'],

        # ==================== AROMATIQUES ====================
        'basilic': ['Bourrache', 'Souci', 'Lavande'],
        'menthe': ['Lavande', 'Romarin', 'Sauge'],
        'coriandre': ['Bourrache', 'Souci', 'Lavande'],
        'persil': ['Lavande', 'Romarin', 'Sauge'],
        'ciboulette': ['Lavande', 'Romarin', 'Sauge'],
        'aneth': ['Bourrache', 'Souci', 'Lavande'],
        'estragon': ['Lavande', 'Romarin', 'Sauge'],
        'origan': ['Lavande', 'Romarin', 'Sauge', 'Thym'],
        'marjolaine': ['Lavande', 'Romarin', 'Sauge', 'Thym'],
        'sauge': ['Lavande', 'Romarin', 'Thym'],
        'romarin': ['Lavande', 'Thym', 'Sauge'],
        'thym': ['Lavande', 'Romarin', 'Sauge'],
        'lavande': ['Romarin', 'Thym', 'Sauge'],
        'verveine': ['Lavande', 'Romarin', 'Sauge'],
        'mélisse': ['Lavande', 'Romarin', 'Sauge'],

        # ==================== FLEURS & ORNEMENTALES ====================
        'rose': ['Lavande', 'Romarin', 'Thym', 'Sauge'],
        'tulipe': ['Lavande', 'Romarin', 'Sauge'],
        'hortensia': ['Lavande', 'Romarin', 'Sauge'],
        'pivoine': ['Lavande', 'Romarin', 'Sauge'],
        'iris': ['Lavande', 'Romarin', 'Sauge'],
        'orchidée': ['Lavande', 'Romarin', 'Sauge'],
        'jasmin': ['Lavande', 'Romarin', 'Sauge'],
        'tournesol': ['Bourrache', 'Souci', 'Œillet d\'Inde'],

        # ==================== CULTURES TROPICALES ====================
        'cacao': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'café': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'vanille': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'gingembre': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'curcuma': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'cannelle': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'poivre': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'manioc': ['Hibiscus', 'Bougainvillier', 'Passiflore'],
        'igname': ['Hibiscus', 'Bougainvillier', 'Passiflore'],

        # ==================== CULTURES DÉSERTIQUES ====================
        'dattier': ['Lavande', 'Romarin', 'Thym', 'Sauge'],
        'figue': ['Lavande', 'Romarin', 'Thym', 'Sauge'],
        'grenade': ['Lavande', 'Romarin', 'Thym', 'Sauge'],
        'caroubier': ['Lavande', 'Romarin', 'Thym', 'Sauge'],
        'pistache': ['Lavande', 'Romarin', 'Thym', 'Sauge'],

        # ==================== CULTURES MÉDITERRANÉENNES ====================
        'lavande': ['Romarin', 'Thym', 'Sauge', 'Ciste'],
        'romarin': ['Lavande', 'Thym', 'Sauge', 'Ciste'],
        'thym': ['Lavande', 'Romarin', 'Sauge', 'Ciste'],
        'sauge': ['Lavande', 'Romarin', 'Thym', 'Ciste'],
        'ciste': ['Lavande', 'Romarin', 'Thym', 'Sauge'],

        # ==================== CULTURES MONTAGNARDES ====================
        'gentiane': ['Souci', 'Œillet d\'Inde'],
        'rhubarbe': ['Lavande', 'Romarin', 'Sauge'],
    }

    # ============================================================ #
    # FLEURS ADAPTÉES AU CLIMAT (MONDIAL) #
    # ============================================================ #
    climat_fleurs = {
        'mediterraneen': ['Lavande', 'Romarin', 'Thym', 'Sauge', 'Ciste', 'Bourrache', 'Souci'],
        'tempere': ['Souci', 'Œillet d\'Inde', 'Tournesol', 'Bourrache', 'Cosmos', 'Lavande'],
        'continental': ['Souci', 'Œillet d\'Inde', 'Tournesol', 'Cosmos', 'Lavande'],
        'oceanique': ['Souci', 'Œillet d\'Inde', 'Bourrache', 'Hortensia', 'Lavande'],
        'tropical': ['Hibiscus', 'Bougainvillier', 'Passiflore', 'Lantana', 'Plumeria', 'Frangipanier'],
        'desertique': ['Lavande', 'Romarin', 'Thym', 'Sauge', 'Ciste'],
        'montagnard': ['Pivoine', 'Tournesol', 'Souci', 'Lavande'],
        'subtropical': ['Hibiscus', 'Bougainvillier', 'Passiflore', 'Lantana', 'Plumeria'],
        'arctique': ['Pivoine', 'Tournesol', 'Souci'],
        'subpolaire': ['Pivoine', 'Tournesol', 'Souci'],
    }

    # ============================================================ #
    # 1. SUGGESTIONS BASÉES SUR LES CULTURES #
    # ============================================================ #
    for culture in cultures:
        culture_lower = culture.lower()
        for cle, fleurs in compatibilites.items():
            if cle in culture_lower or culture_lower in cle:
                suggestions.extend(fleurs)

    # ============================================================ #
    # 2. SUGGESTIONS BASÉES SUR LE CLIMAT #
    # ============================================================ #
    fleurs_climat = climat_fleurs.get(climat, [])
    for fleur in fleurs_climat:
        if fleur not in suggestions:
            suggestions.append(fleur)

    # ============================================================ #
    # 3. AJOUTER DES FLEURS DE BASE SI AUCUNE SUGGESTION #
    # ============================================================ #
    if not suggestions:
        suggestions = ['Souci', 'Œillet d\'Inde', 'Bourrache', 'Lavande', 'Tournesol']

    # ============================================================ #
    # 4. ÉVITER LES DOUBLONS #
    # ============================================================ #
    suggestions = list(dict.fromkeys(suggestions))

    # ============================================================ #
    # 5. LIMITER À 8 SUGGESTIONS #
    # ============================================================ #
    return suggestions[:8]

@login_required
def quiz_resultat(request, quiz_id):
    quiz = get_object_or_404(QuizUtilisateur, id=quiz_id, user=request.user)
    questions = []
    for q_id, reponse in quiz.reponses.items():
        question = QuestionQuiz.objects.get(id=int(q_id))
        questions.append({
            'question': question,
            'reponse_user': reponse,
            'bonne_reponse': question.bonne_reponse,
            'est_juste': reponse == question.bonne_reponse,
        })

    return render(request, 'vegetables_fruits/quiz_resultat.html', {
        'quiz': quiz,
        'questions': questions,
    })


@login_required
def quiz(request):
    """Page du quiz jardinage"""

    from datetime import date
    from django.utils import timezone

    # ✅ COMPTER LES QUIZ DU JOUR
    today = date.today()
    quiz_du_jour = QuizUtilisateur.objects.filter(
        user=request.user,
        date=today
    ).first()

    if quiz_du_jour:
        nb_quiz_aujourdhui = quiz_du_jour.nb_quiz
    else:
        nb_quiz_aujourdhui = 0

    logger.debug(f"🔍 Quiz aujourd'hui pour {request.user.username}: {nb_quiz_aujourdhui}")

    # ✅ VÉRIFIER LE QUOTA POUR BASIQUE (3 quiz/jour)
    try:
        abonnement = request.user.abonnement
        if abonnement and abonnement.plan.nom == 'BASIQUE':
            if nb_quiz_aujourdhui >= 3:
                messages.warning(
                    request,
                    "📝 Vous avez atteint votre limite de 3 quiz par jour pour le plan Basique. "
                    "Revenez demain ou passez à Premium pour des quiz illimités !"
                )
                return redirect('vegetables_fruits:dashboard_particulier')
    except:
        pass

    # Vérifier si l'utilisateur a droit à un quiz aujourd'hui
    peut_jouer, raison = has_quiz_access(request.user)

    # Vérifier si l'utilisateur a droit à un quiz aujourd'hui
    peut_jouer, raison = has_quiz_access(request.user)

    if not peut_jouer:
        # ✅ Message clair selon la raison
        messages.warning(
            request,
            f"⏳ {raison} Reviens demain pour de nouveaux quiz ! 🌱"
        )

        # ✅ Redirection selon le profil
        if est_mineur(request.user):
            # Mineur en classe → dashboard élève
            if hasattr(request.user, 'profil_eleve') and request.user.profil_eleve and request.user.profil_eleve.classe:
                return redirect('vegetables_fruits:dashboard_eleve')
            # Mineur particulier → dashboard junior
            else:
                return redirect('vegetables_fruits:dashboard_junior')
        # Majeur → dashboard particulier
        else:
            return redirect('vegetables_fruits:dashboard_particulier')

    if request.method == 'POST':
        # ✅ Récupérer les IDs des questions depuis les champs cachés
        question_ids_str = request.POST.get('question_ids', '')
        # Filtrer les valeurs vides et convertir en entiers
        question_ids = [int(id) for id in question_ids_str.split(',') if id]

        if question_ids:
            questions = QuestionQuiz.objects.filter(id__in=question_ids)
        else:
            questions = QuestionQuiz.objects.all()

        total = questions.count()
        score = 0
        reponses_utilisateur = {}

        # Dictionnaire pour mapper les valeurs aux textes des choix
        choix_map = {}

        # Parcourir chaque question pour traiter la réponse
        for question in questions:
            # Stocker les choix pour cette question
            choix_map[question.id] = {
                '1': question.choix_1,
                '2': question.choix_2,
                '3': question.choix_3,
                '4': question.choix_4,
            }

            # Récupérer la réponse de l'utilisateur
            reponse = request.POST.get(f'q{question.id}')
            reponses_utilisateur[question.id] = reponse

            # Vérifier si la réponse est correcte
            if reponse and int(reponse) == question.bonne_reponse:
                score += 1

        # Calcul des points
        points_gagnes = score * 2
        bonus_tout_juste = False

        if score == total and total > 0:
            points_gagnes += 5
            bonus_tout_juste = True

        # ✅ Créer ou mettre à jour le quiz
        quiz_resultat, created = QuizUtilisateur.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={
                'score': score,
                'reponses': reponses_utilisateur,
                'nb_quiz': 1,
            }
        )

        if not created:
            quiz_resultat.score = score
            quiz_resultat.reponses = reponses_utilisateur
            quiz_resultat.nb_quiz += 1
            quiz_resultat.save()

        logger.info(f"✅ Quiz {'créé' if created else 'mis à jour'} pour {request.user.username} - nb_quiz: {quiz_resultat.nb_quiz}")


        # Ajouter les points à l'élève (si mode junior)
        nouveaux_badges = []
        if hasattr(request.user, 'profil_eleve') and request.user.mode_junior:
            eleve = request.user.profil_eleve
            eleve.ajouter_points(points_gagnes)
            nouveaux_badges = check_and_award_badges(eleve)
            mettre_a_jour_progres_defi(request.user.profil_eleve, 'quiz', score)
            verifier_competences(eleve)

        # Préparer les détails des réponses
        reponses_details = []
        for question in questions:
            reponse_utilisateur = reponses_utilisateur.get(question.id)
            est_correcte = (reponse_utilisateur and int(reponse_utilisateur) == question.bonne_reponse)

            texte_reponse = choix_map[question.id].get(reponse_utilisateur, '')
            texte_correcte = choix_map[question.id].get(str(question.bonne_reponse), '')

            reponses_details.append({
                'texte': question.question,
                'reponse_utilisateur': texte_reponse,
                'correct': est_correcte,
                'reponse_correcte': texte_correcte,
            })

        context = {
            'score': score,
            'total': total,
            'points_gagnes': points_gagnes,
            'bonus_tout_juste': bonus_tout_juste,
            'pourcentage': int((score / total) * 100) if total > 0 else 0,
            'reponses_details': reponses_details,
            'nouveaux_badges': nouveaux_badges,
        }

        return render(request, 'vegetables_fruits/quiz_resultat.html', context)

    else:

        # ✅ GET : Sélectionner 5 questions aléatoires
        toutes_questions = QuestionQuiz.objects.all()

        # ✅ NOUVEAU : Filtrage par âge / mode junior
        est_mineur = request.user.mode_junior or (
                request.user.birth_date and (date.today() - request.user.birth_date).days // 365 < 18
        )

        if est_mineur:
            toutes_questions = toutes_questions.filter(difficulte=1)  # Uniquement facile

        questions = toutes_questions.order_by('?')[:5]

        # Transformer chaque question en format avec options
        for question in questions:
            options = []
            if question.choix_1:
                options.append({'value': '1', 'text': question.choix_1})
            if question.choix_2:
                options.append({'value': '2', 'text': question.choix_2})
            if question.choix_3:
                options.append({'value': '3', 'text': question.choix_3})
            if question.choix_4:
                options.append({'value': '4', 'text': question.choix_4})
            question.options_list = options

        # ✅ Passer les IDs des questions au template
        question_ids = [str(q.id) for q in questions]

        context = {
            'questions': questions,
            'question_ids': question_ids,
            'nb_quiz_aujourdhui': nb_quiz_aujourdhui,
        }
        return render(request, 'vegetables_fruits/quiz.html', context)


def check_and_award_badges(eleve):
    """Vérifier et attribuer les badges"""
    nouveaux_badges = []

    # Badge "Premier pas" (100 points)
    if eleve.points >= 100 and not eleve.badges.filter(nom="Premier pas").exists():
        try:
            badge = Badge.objects.get(nom="Premier pas")
            eleve.badges.add(badge)
            nouveaux_badges.append(badge)
        except Badge.DoesNotExist:
            pass

    # Badge "Apprenti jardinier" (500 points)
    if eleve.points >= 500 and not eleve.badges.filter(nom="Apprenti jardinier").exists():
        try:
            badge = Badge.objects.get(nom="Apprenti jardinier")
            eleve.badges.add(badge)
            nouveaux_badges.append(badge)
        except Badge.DoesNotExist:
            pass

    # Badge "Quiz master" (3 quiz parfaits)
    total_questions = QuestionQuiz.objects.count()

    if total_questions > 0:
        quiz_parfaits = QuizUtilisateur.objects.filter(
            user=eleve.user,
            score=total_questions
        ).count()

        if quiz_parfaits >= 3 and not eleve.badges.filter(nom="Quiz master").exists():
            try:
                badge = Badge.objects.get(nom="Quiz master")
                eleve.badges.add(badge)
                nouveaux_badges.append(badge)
            except Badge.DoesNotExist:
                pass

    return nouveaux_badges

# VUE POUR LA VERIFICATION ACCES JOURNAL DE BORD


def verifier_acces_journal(user):
    """Retourne (acces: bool, message: str|None)"""
    if user.is_enseignant:
        return True, None
    try:
        abonnement = user.abonnement
        if abonnement.est_actif and abonnement.plan.nom in ['BASIQUE', 'PREMIUM']:
            return True, None
    except Abonnement.DoesNotExist:
        pass
    return False, "Le journal de bord est disponible avec les abonnements Basique et Premium. ✨"


@login_required
def journal_liste(request):
    """Liste des notes du journal"""
    acces, message = verifier_acces_journal(request.user)
    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    notes = JournalBord.objects.filter(utilisateur=request.user).select_related('figure')

    # ✅ COMPTER LES NOTES
    nb_notes = notes.count()

    # ✅ Filtre par culture (en Python car SQLite ne supporte pas contains)
    culture_id = request.GET.get('culture')
    if culture_id:
        # ✅ L'ID peut être un nombre ou une chaîne (ex: 'crop_3')
        notes = list(notes)
        notes = [note for note in notes if note.culture and str(note.culture.get('id')) == culture_id]
    else:
        notes = list(notes)

    paginator = Paginator(notes, 10)
    page = request.GET.get('page')
    notes_page = paginator.get_page(page)

    # ✅ Récupérer toutes les cultures depuis les parcelles
    cultures_utilisees = set()
    figures = GeometricFigure.objects.filter(user=request.user)

    for figure in figures:
        if figure.crops:
            for crop in figure.crops:
                if 'name' in crop:
                    # ✅ Récupérer l'ID depuis fruit_id ou vegetable_id
                    crop_id = crop.get('fruit_id') or crop.get('vegetable_id')
                    if not crop_id:
                        # Si pas d'ID, utiliser un ID fictif
                        crop_id = f"crop_{len(cultures_utilisees)}"
                    cultures_utilisees.add((crop_id, crop.get('name'), crop.get('emoji', '🌱')))

    return render(request, 'vegetables_fruits/journal/liste.html', {
        'notes': notes_page,
        'nb_notes': nb_notes,  # ✅ AJOUTÉ
        'cultures_filtre': sorted(cultures_utilisees, key=lambda x: x[1]),
        'culture_selectionnee': culture_id,
    })


@login_required
def journal_ajouter(request, figure_id=None):
    """Ajouter une note (optionnellement liée à une parcelle)"""
    import requests
    from django.conf import settings
    logger.debug("🔑 OPENWEATHER_API_KEY dans settings:", getattr(settings, 'OPENWEATHER_API_KEY', 'NON TROUVEE'))


    acces, message = verifier_acces_journal(request.user)
    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    # ✅ VÉRIFIER LE QUOTA POUR BASIQUE
    try:
        abonnement = request.user.abonnement
        if abonnement and abonnement.plan.nom == 'BASIQUE':
            nb_notes = JournalBord.objects.filter(utilisateur=request.user).count()
            if nb_notes >= 10:
                messages.warning(
                    request,
                    "📓 Vous avez atteint la limite de 10 notes pour le plan Basique. "
                    "Passez à Premium pour des notes illimitées !"
                )
                return redirect('vegetables_fruits:journal_liste')
    except:
        pass

    figure = None
    if figure_id:
        figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)

    if request.method == 'POST':
        titre = request.POST.get('titre')
        note = request.POST.get('note')
        date_note = request.POST.get('date_note')
        culture_json = request.POST.get('culture_json', '{}')
        tags = request.POST.get('tags', '')

        # Météo automatique (optionnelle)
        meteo = request.POST.get('meteo')
        if meteo == '':
            meteo = None

        temperature = request.POST.get('temperature')
        if temperature =='':
            temperature = None
        else:
            temperature = temperature.replace(',', '.')
            try:
                temperature = float(temperature)
            except ValueError:
                temperature = None

        image = request.FILES.get('image')

        # ✅ Validation MIME réelle si une image est fournie
        if image:
            valide, message_erreur = valider_image_upload(image, taille_max_mo=5)
            if not valide:
                logger.warning(f"Upload journal refusé ({image.name}) : {message_erreur}")
                messages.error(request, message_erreur)
                return redirect('vegetables_fruits:journal_liste')

        try:
            culture_data = json.loads(culture_json)
        except:
            culture_data = {}

        nouvelle_note = JournalBord.objects.create(
            utilisateur=request.user,
            figure=figure,
            culture=culture_data,
            titre=titre,
            note=note,
            date_note=date_note or timezone.now().date(),
            tags=tags,
            meteo=meteo,
            temperature=temperature,
            image=image
        )

        if hasattr(request.user, 'profil_eleve'):
            eleve = request.user.profil_eleve
            mettre_a_jour_progres_defi(eleve, 'journal')
            verifier_competences(eleve)

        # Redimensionnement basique de l'image
        if image:
            try:
                img = PilImage.open(image)
                img.thumbnail((800, 800))
                img.save(image.path)
            except:
                pass

        messages.success(request, "Note ajoutée avec succès !")
        return redirect('vegetables_fruits:journal_detail', note_id=nouvelle_note.id)

    # Récupérer les cultures de l'utilisateur pour le sélecteur
    cultures_user = []
    if figure:
        for crop in figure.crops:
            if 'name' in crop:
                cultures_user.append({
                    'id': crop.get('fruit_id') or crop.get('vegetable_id'),
                    'nom': crop.get('name'),
                    'emoji': crop.get('emoji', '🌱'),
                    'type': 'fruit' if 'fruit_id' in crop else 'vegetable'
                })

    # Météo actuelle via OpenWeatherMap direct
    meteo_actuelle = None
    temperature_actuelle = None
    logger.debug(f"figure = {figure}")

    if figure:
        logger.debug(f" figure.adresse_lat = {figure.adresse_lat}")

        logger.debug(f" figure.adresse_lng = {figure.adresse_lng}")

    else:
        logger.debug(" figure est None")


    if figure:
        meteo_data = get_meteo_for_figure(figure)
        if meteo_data:
            meteo_actuelle = meteo_data['conditions']
            temperature_actuelle = meteo_data['temperature']

    return render(request, 'vegetables_fruits/journal/editer.html', {
        'figure': figure,
        'cultures_user': cultures_user,
        'meteo_actuelle': meteo_actuelle,
        'temperature_actuelle': temperature_actuelle,
    })

@login_required
def journal_modifier(request, note_id):
    """Modifier une note existante"""
    acces, message = verifier_acces_journal(request.user)
    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    note = get_object_or_404(JournalBord, id=note_id, utilisateur=request.user)

    if request.method == 'POST':
        # ✅ VÉRIFIER LE QUOTA POUR BASIQUE (pour la création de nouvelles notes uniquement)
        try:
            abonnement = request.user.abonnement
            if abonnement and abonnement.plan.nom == 'BASIQUE':
                nb_notes = JournalBord.objects.filter(utilisateur=request.user).count()
                if nb_notes >= 10 and note_id not in [n.id for n in JournalBord.objects.filter(utilisateur=request.user)]:
                    messages.warning(
                        request,
                        "📓 Vous avez atteint la limite de 10 notes pour le plan Basique. "
                        "Passez à Premium pour des notes illimitées !"
                    )
                    return redirect('vegetables_fruits:journal_liste')
        except:
            pass

        note.titre = request.POST.get('titre')
        note.note = request.POST.get('note')
        note.date_note = request.POST.get('date_note') or note.date_note
        note.tags = request.POST.get('tags', '')
        note.meteo = request.POST.get('meteo')
        if note.meteo == '':
            note.meteo = None

        note.temperature = request.POST.get('temperature')
        if note.temperature == '':
            note.temperature = None

        culture_json = request.POST.get('culture_json', '{}')
        try:
            note.culture = json.loads(culture_json)
        except:
            pass

        nouvelle_image = request.FILES.get('image')
        if nouvelle_image:
            # ✅ Validation MIME réelle
            valide, message_erreur = valider_image_upload(nouvelle_image, taille_max_mo=5)
            if not valide:
                logger.warning(f"Upload journal refusé ({nouvelle_image.name}) : {message_erreur}")
                messages.error(request, message_erreur)
                return redirect('vegetables_fruits:journal_modifier', note_id=note.id)

            # Supprimer l'ancienne image
            if note.image:
                note.image.delete()

            # Assigner la nouvelle
            note.image = nouvelle_image

            # Redimensionnement
            try:
                img = PilImage.open(note.image)
                img.thumbnail((800, 800))
                img.save(note.image.path)
            except Exception as e:
                logger.warning(f"Redimensionnement échoué : {e}")

        note.save()
        messages.success(request, "Note modifiée avec succès !")
        return redirect('vegetables_fruits:journal_detail', note_id=note.id)

    # Préparer les cultures disponibles (même logique)
    cultures_user = []
    if note.figure:
        for crop in note.figure.crops:
            if 'name' in crop:
                cultures_user.append({
                    'id': crop.get('fruit_id') or crop.get('vegetable_id'),
                    'nom': crop.get('name'),
                    'emoji': crop.get('emoji', '🌱'),
                    'type': 'fruit' if 'fruit_id' in crop else 'vegetable'
                })

    return render(request, 'vegetables_fruits/journal/editer.html', {
        'note': note,
        'figure': note.figure,
        'cultures_user': cultures_user,
    })



@login_required
def journal_detail(request, note_id):
    """Afficher une note en détail"""
    acces, message = verifier_acces_journal(request.user)
    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    note = get_object_or_404(JournalBord, id=note_id, utilisateur=request.user)
    return render(request, 'vegetables_fruits/journal/detail.html', {'note': note})


@login_required
def journal_supprimer(request, note_id):
    """Supprimer une note (POST only)"""
    acces, message = verifier_acces_journal(request.user)
    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    note = get_object_or_404(JournalBord, id=note_id, utilisateur=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, "Note supprimée.")
        return redirect('vegetables_fruits:journal_liste')

    return redirect('vegetables_fruits:journal_detail', note_id=note.id)

# ============================================================
# DÉTECTION DES ALERTES MÉTÉO CRITIQUES
# ============================================================

# Seuils au-delà desquels une alerte est "critique" (envoi immédiat)
SEUILS_CRITIQUES = {
    'gel': -2, # Gel sévère
    'canicule': 38, # Canicule extrême
    'vent': 60, # Vent violent
}


def est_alerte_meteo_critique(type_alerte, valeur):
    """
    Détermine si une alerte météo est critique (envoi immédiat).

    - gel : température <= -2°C
    - canicule : température >= 38°C
    - vent : vitesse >= 60 km/h
    - pluie / humidité : jamais critique (toujours en digest)
    """
    if type_alerte == 'gel' and valeur <= SEUILS_CRITIQUES['gel']:
        return True
    if type_alerte == 'canicule' and valeur >= SEUILS_CRITIQUES['canicule']:
        return True
    if type_alerte == 'vent' and valeur >= SEUILS_CRITIQUES['vent']:
        return True
    return False


def envoyer_email_alerte_critique(user, alerte):
    """
    Envoie un email IMMÉDIAT pour une alerte météo critique.
    Retourne True si envoyé, False sinon.
    """
    if not user.email:
        logger.warning(f"Pas d'email pour {user.username} → alerte critique non envoyée")
        return False

    try:
        send_mail(
            subject=f"🚨 ALERTE CRITIQUE - {alerte['type'].upper()}",
            message=(
                f"Bonjour {user.username},\n\n"
                f"🚨 Alerte météo CRITIQUE détectée :\n\n"
                f"{alerte['message']}\n\n"
                f"Parcelle : {alerte.get('figure', 'N/A')}\n"
                f"Culture : {alerte.get('culture', 'N/A')}\n\n"
                f"👉 Agissez rapidement pour protéger vos cultures !\n\n"
                f"L'équipe Agriculture 2.0"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info(f"🚨 Email critique envoyé à {user.email} ({alerte['type']})")
        return True
    except Exception as e:
        logger.error(f"Erreur envoi email critique à {user.email} : {e}")
        return False

def verifier_alertes_meteo():
    """
    Fonction à appeler périodiquement (cron ou celery)
    Vérifie les alertes météo pour TOUS les utilisateurs
    """
    from .models import GeometricFigure, AlerteMeteo, Abonnement
    from django.conf import settings
    from django.contrib.auth import get_user_model
    import requests
    from datetime import datetime

    User = get_user_model()

    logger.debug(f"🔍 Début vérification alertes météo - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")


    # Seuils d'alerte par défaut
    SEUILS_DEFAUT = {
        'gel': 0,
        'canicule': 35,
        'pluie': 20,
        'vent': 50,
    }

    # Récupérer TOUS les utilisateurs
    users = User.objects.all()
    logger.debug(f"👤 {users.count()} utilisateur(s)")


    alertes_crees = 0

    for user in users:
        # Vérifier si l'utilisateur a un abonnement actif
        try:
            abonnement = user.abonnement
            if not abonnement.est_actif:
                continue
        except Abonnement.DoesNotExist:
            # Pas d'abonnement = plan gratuit
            pass

        logger.debug(f"\n👤 Utilisateur: {user.username} (ID: {user.id})")


        # Récupérer les parcelles de CET utilisateur
        figures = GeometricFigure.objects.filter(
            user=user,
            adresse_lat__isnull=False,
            adresse_lng__isnull=False
        )

        if not figures.exists():
            logger.warning(f"  ⚠️ Aucune parcelle avec coordonnées pour {user.username}")

            continue

        logger.debug(f"  📍 {figures.count()} parcelle(s)")


        for figure in figures:
            try:
                logger.debug(f"    🌾 {figure.name}...", end='')


                # Appel API météo
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={figure.adresse_lat}&lon={figure.adresse_lng}&units=metric&lang=fr&appid={settings.OPENWEATHER_API_KEY}"
                response = requests.get(url, timeout=10)

                if response.status_code != 200:
                    logger.error(f" ⚠️ API error {response.status_code}")

                    continue

                data = response.json()
                temp = round(data['main']['temp'], 1)
                humidite = data['main']['humidity']
                precipitation = data.get('rain', {}).get('1h', 0)
                wind_speed = data['wind']['speed']
                description = data['weather'][0]['description']

                logger.debug(f" 🌡️ {temp}°C, 💧 {humidite}%")


                # Récupérer les cultures de la parcelle
                cultures = []
                if figure.crops:
                    for crop in figure.crops:
                        if 'name' in crop:
                            cultures.append(crop['name'])

                # Si pas de cultures, utiliser des valeurs par défaut
                if not cultures:
                    cultures = ['Culture générique']

                # Vérifier les alertes pour chaque culture
                for culture_nom in cultures:
                    # Récupérer la culture en base pour les seuils
                    culture_obj = Culture.objects.filter(nom__icontains=culture_nom).first()

                    # Seuils personnalisés ou défauts
                    gel_seuil = culture_obj.temperature_mingel if culture_obj and culture_obj.temperature_mingel is not None else \
                    SEUILS_DEFAUT['gel']
                    canicule_seuil = culture_obj.temperature_max_canicule if culture_obj and culture_obj.temperature_max_canicule is not None else \
                    SEUILS_DEFAUT['canicule']
                    pluie_seuil = culture_obj.precipitation_max if culture_obj and culture_obj.precipitation_max is not None else \
                    SEUILS_DEFAUT['pluie']
                    vent_seuil = culture_obj.vent_max if culture_obj and culture_obj.vent_max is not None else \
                    SEUILS_DEFAUT['vent']

                    alertes_parcelle = []

                    # Alerte gel
                    if temp <= gel_seuil:
                        alertes_parcelle.append({
                            'type': 'gel',
                            'culture': culture_nom,
                            'message': f"❄️ Alerte gel ! {culture_nom} ({temp}°C, seuil: {gel_seuil}°C)"
                        })

                    # Alerte canicule
                    if temp >= canicule_seuil:
                        alertes_parcelle.append({
                            'type': 'canicule',
                            'culture': culture_nom,
                            'message': f"🌡️ Alerte canicule ! {culture_nom} ({temp}°C, seuil: {canicule_seuil}°C)"
                        })

                    # Alerte pluie
                    if precipitation >= pluie_seuil:
                        alertes_parcelle.append({
                            'type': 'pluie',
                            'culture': culture_nom,
                            'message': f"🌧️ Alerte forte pluie ! {culture_nom} ({precipitation}mm, seuil: {pluie_seuil}mm)"
                        })

                    # Alerte vent
                    if wind_speed >= vent_seuil:
                        alertes_parcelle.append({
                            'type': 'vent',
                            'culture': culture_nom,
                            'message': f"💨 Alerte vent fort ! {culture_nom} ({wind_speed}km/h, seuil: {vent_seuil}km/h)"
                        })

                    # Sauvegarder les alertes en base
                    # Sauvegarder les alertes en base
                    from datetime import date
                    aujourdhui = date.today()

                    for alerte in alertes_parcelle:
                        alerte_existante = AlerteMeteo.objects.filter(
                            utilisateur=user,
                            figure=figure,
                            type_alerte=alerte['type'],
                            date_declenchement__date=aujourdhui
                        ).exists()

                        if not alerte_existante:
                            # 1. Toujours créer en base (pour l'historique in-app)
                            AlerteMeteo.objects.create(
                                utilisateur=user,
                                figure=figure,
                                type_alerte=alerte['type'],
                                message=alerte['message'],
                                temperature=temp,
                                date_declenchement=timezone.now(),
                                statut='en_attente'
                            )
                            alertes_crees += 1

                            # 2. Déterminer la valeur pour le test critique
                            if alerte['type'] == 'gel':
                                valeur = temp
                            elif alerte['type'] == 'canicule':
                                valeur = temp
                            elif alerte['type'] == 'vent':
                                valeur = wind_speed
                            else:
                                valeur = None

                            # 3. Créer/récupérer le digest du jour
                            digest, _ = DigestMeteo.objects.get_or_create(
                                utilisateur=user,
                                date=aujourdhui,
                            )

                            # 4. Construire l'alerte pour le digest
                            alerte_data = {
                                'type': alerte['type'],
                                'culture': culture_nom,
                                'figure': figure.name,
                                'message': alerte['message'],
                                'temperature': temp,
                                'est_critique': False,
                            }

                            # 5. Critique → envoi immédiat + ajout au digest (traçabilité)
                            if valeur is not None and est_alerte_meteo_critique(alerte['type'], valeur):
                                alerte_data['est_critique'] = True
                                if envoyer_email_alerte_critique(user, alerte_data):
                                    digest.nb_critiques_envoyees += 1

                            # 6. Ajouter au digest (critiques + normales)
                            digest.alertes.append(alerte_data)
                            digest.save()

                            logger.info(f"✅ Alerte {alerte['type']} ajoutée au digest de {user.username}")


            except Exception as e:
                logger.error(f" ❌ Erreur: {str(e)}")

                continue

    logger.info(f"\n✅ Fin vérification alertes météo - {alertes_crees} alerte(s) créée(s)")

    return alertes_crees


def envoyer_alerte_meteo(user, type_alerte, message):
    """Envoie une notification par email"""
    from django.core.mail import send_mail

    if user.email:
        try:
            send_mail(
                subject=f"🌤️ Alerte météo - {type_alerte.upper()}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"✅ Email envoyé à {user.email} pour alerte {type_alerte}")

        except Exception as e:
            logger.error(f"❌ Erreur envoi email: {e}")



@login_required
def mes_alertes_meteo(request):
    """Affiche les alertes météo de l'utilisateur"""
    alertes = AlerteMeteo.objects.filter(utilisateur=request.user).order_by('-date_declenchement')

    # Statistiques
    stats = {
        'total': alertes.count(),
        'gel': alertes.filter(type_alerte='gel').count(),
        'canicule': alertes.filter(type_alerte='canicule').count(),
        'non_lues': alertes.filter(statut='en_attente').count(),
    }

    return render(request, 'vegetables_fruits/alertes_meteo.html', {
        'alertes': alertes,
        'stats': stats,
    })


from django.utils import timezone
from .models import Defi, ProgresDefi, Badge


def mettre_a_jour_progres_defi(eleve, type_action, valeur=1):
    """
    Met à jour la progression des défis d'un élève
    type_action: 'planter', 'recolter', 'quiz', 'journal', 'points', 'fleur'
    valeur: nombre de points/actions à ajouter
    """
    if not eleve or not eleve.classe:
        return

    # Récupérer les défis actifs de la classe
    defis_actifs = Defi.objects.filter(
        classe=eleve.classe,
        statut='actif',
        type_action=type_action,
        date_debut__lte=timezone.now(),
        date_fin__gte=timezone.now()
    )

    for defi in defis_actifs:
        # Récupérer ou créer la progression de l'élève
        progres, created = ProgresDefi.objects.get_or_create(
            eleve=eleve,
            defi=defi,
            defaults={'valeur_objectif': defi.objectif}
        )

        # Ajouter la progression
        progres.ajouter_progression(valeur)

        # Vérifier si le défi est terminé par la classe
        progression_totale = sum(
            p.valeur_actuelle for p in ProgresDefi.objects.filter(defi=defi)
        )

        if progression_totale >= defi.objectif and defi.statut == 'actif':
            # Marquer le défi comme terminé
            defi.statut = 'termine'
            defi.save()

            # Ajouter les points à la classe (pour le classement)
            for eleve_classe in defi.classe.eleves.all():
                eleve_classe.points += defi.points_recompense
                eleve_classe.save()

            # Attribuer le badge à tous les élèves de la classe
            if defi.badge_nom:
                badge, _ = Badge.objects.get_or_create(
                    nom=defi.badge_nom,
                    defaults={
                        'emoji': defi.badge_emoji or '🏆',
                        'description': f"Récompense du défi '{defi.titre}'",
                        'points': defi.points_recompense
                    }
                )
                for eleve_classe in defi.classe.eleves.all():
                    if not eleve_classe.badges.filter(id=badge.id).exists():
                        eleve_classe.badges.add(badge)

            # Notification aux élèves (optionnel)
            from django.core.mail import send_mail
            for eleve_classe in defi.classe.eleves.all():
                if eleve_classe.user.email:
                    send_mail(
                        subject=f"🏆 Défi terminé : {defi.titre}",
                        message=f"Félicitations ! Votre classe a relevé le défi '{defi.titre}' ! Vous avez gagné {defi.points_recompense} points et {defi.badge_emoji} {defi.badge_nom} !",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[eleve_classe.user.email],
                        fail_silently=True,
                    )
@login_required
def defis_liste(request):
    """Liste des défis de la classe de l'élève"""
    if not hasattr(request.user, 'profil_eleve') or not request.user.profil_eleve.classe:
        messages.warning(request, "Vous devez être dans une classe pour participer aux défis.")
        return redirect('vegetables_fruits:profile')

    classe = request.user.profil_eleve.classe
    defis = Defi.objects.filter(classe=classe).order_by('-date_creation')

    # Calculer la progression pour chaque défi
    for defi in defis:
        defi.progression_actuelle = defi.progression_classe()
        defi.pourcentage = int((defi.progression_actuelle / defi.objectif) * 100) if defi.objectif > 0 else 0

    return render(request, 'vegetables_fruits/defis/liste.html', {
        'defis': defis,
        'classe': classe,
    })


@login_required
def defi_detail(request, defi_id):
    """Détail d'un défi avec progression des élèves"""
    defi = get_object_or_404(Defi, id=defi_id)

    # Vérifier l'accès
    if not request.user.is_enseignant and request.user.profil_eleve.classe != defi.classe:
        messages.error(request, "Accès non autorisé")
        return redirect('vegetables_fruits:defis_liste')

    progres = ProgresDefi.objects.filter(defi=defi).select_related('eleve')

    # Progression par élève
    progres_eleves = []
    for prog in progres:
        progres_eleves.append({
            'eleve': prog.eleve,
            'progression': prog.valeur_actuelle,
            'objectif': prog.valeur_objectif,
            'pourcentage': int((prog.valeur_actuelle / prog.valeur_objectif) * 100) if prog.valeur_objectif > 0 else 0,
            'complete': prog.est_complete,
        })

    return render(request, 'vegetables_fruits/defis/detail.html', {
        'defi': defi,
        'progres_eleves': progres_eleves,
        'progression_classe': defi.progression_classe(),
        'pourcentage_classe': int((defi.progression_classe() / defi.objectif) * 100) if defi.objectif > 0 else 0,
    })


@login_required
def creer_defi(request):
    """Créer un défi (réservé aux enseignants)"""
    if not request.user.is_enseignant:
        messages.error(request, "Accès non autorisé")
        return redirect('vegetables_fruits:index')

    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        classe_id = request.POST.get('classe_id')
        type_action = request.POST.get('type_action')
        objectif = int(request.POST.get('objectif'))
        points_recompense = int(request.POST.get('points_recompense', 50))
        badge_nom = request.POST.get('badge_nom', '')
        badge_emoji = request.POST.get('badge_emoji', '🏆')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')

        classe = get_object_or_404(Classe, id=classe_id, enseignant=request.user)

        defi = Defi.objects.create(
            titre=titre,
            description=description,
            enseignant=request.user,
            classe=classe,
            type_action=type_action,
            objectif=objectif,
            points_recompense=points_recompense,
            badge_nom=badge_nom,
            badge_emoji=badge_emoji,
            date_debut=date_debut,
            date_fin=date_fin,
        )

        # Créer la progression pour chaque élève
        for eleve in classe.eleves.all():
            ProgresDefi.objects.create(
                eleve=eleve,
                defi=defi,
                valeur_actuelle=0,
                valeur_objectif=objectif,
            )

        messages.success(request, f"Défi '{titre}' créé avec succès !")
        return redirect('vegetables_fruits:defi_detail', defi_id=defi.id)

    classes = Classe.objects.filter(enseignant=request.user)
    return render(request, 'vegetables_fruits/defis/creer.html', {
        'classes': classes,
    })


# ==================== FORUM D'ENTRAIDE ====================

def verifier_acces_forum(user):
    """Vérifie si l'utilisateur a accès au forum (élève avec classe ou enseignant)"""
    if user.is_enseignant:
        return True
    if hasattr(user, 'profil_eleve') and user.profil_eleve.classe:
        return True
    return False

def acces_forum_requis(view_func):
    """Décorateur pour restreindre l'accès au forum aux élèves et enseignants"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Veuillez vous connecter pour accéder au forum.")
            return redirect('vegetables_fruits:login')
        if not verifier_acces_forum(request.user):
            messages.warning(request, "Le forum est réservé aux écoles. Vous devez être élève (dans une classe) ou enseignant pour y accéder.")
            return redirect('vegetables_fruits:profile')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@acces_forum_requis
def forum_index(request):
    from django.db.models import Count, Q

    # Récupérer toutes les catégories
    categories = CategorieForum.objects.annotate(
        nb_sujets=Count('sujets', filter=Q(sujets__est_supprime=False)),
        nb_messages=Count('sujets__messages'),
        nb_participants=Count('sujets__auteur', distinct=True)
    )

    # ✅ Ajouter le nombre de sujets non lus
    sujets_lus_ids = SujetLu.objects.filter(utilisateur=request.user).values_list('sujet_id', flat=True)

    for cat in categories:
        cat.dernier_sujet = cat.sujets.filter(est_supprime=False).order_by('-date_dernier_message').first()
        cat.sujets_non_lus = cat.sujets.filter(est_supprime=False).exclude(id__in=sujets_lus_ids).count()

    # Derniers sujets avec indication de lecture
    derniers_sujets = SujetForum.objects.filter(est_supprime=False).select_related('categorie', 'auteur').order_by(
        '-date_dernier_message')[:10]

    # ✅ Ajouter une indication de lecture pour chaque sujet
    for sujet in derniers_sujets:
        sujet.est_lu = sujet.id in sujets_lus_ids

    total_sujets = SujetForum.objects.filter(est_supprime=False).count()
    total_messages = MessageForum.objects.count()
    total_participants = SujetForum.objects.filter(est_supprime=False).values('auteur').distinct().count()

    return render(request, 'vegetables_fruits/forum/index.html', {
        'categories': categories,
        'total_sujets': total_sujets,
        'total_messages': total_messages,
        'total_participants': total_participants,
        'derniers_sujets': derniers_sujets,
    })


@login_required
@acces_forum_requis
def forum_categorie(request, categorie_id):
    """Liste des sujets d'une catégorie"""
    categorie = get_object_or_404(CategorieForum, id=categorie_id)
    sujets = categorie.sujets.filter(est_supprime=False)

    # Filtrer par épinglés
    sujets_epingles = sujets.filter(est_epingle=True)
    sujets_normaux = sujets.filter(est_epingle=False)

    paginator = Paginator(sujets_normaux, 20)
    page = request.GET.get('page')
    sujets_normaux_page = paginator.get_page(page)

    return render(request, 'vegetables_fruits/forum/categorie.html', {
        'categorie': categorie,
        'sujets_epingles': sujets_epingles,
        'sujets': sujets_normaux_page,
    })


@login_required
@acces_forum_requis
def forum_sujet(request, sujet_id):
    """Affiche un sujet et ses messages"""
    sujet = get_object_or_404(SujetForum, id=sujet_id, est_supprime=False)

    # Incrémenter le compteur de vues
    if not hasattr(request, '_view_counted'):
        sujet.vues = getattr(sujet, 'vues', 0) + 1
        sujet.save()
        request._view_counted = True

    # Récupérer tous les messages
    liste_messages = sujet.messages.select_related('auteur').all()

    # Récupérer le dernier message lu par l'utilisateur
    sujet_lu = SujetLu.objects.filter(utilisateur=request.user, sujet=sujet).first()

    # ✅ Rediriger vers le dernier message non lu (uniquement si pas de paramètre page)
    if sujet_lu and sujet_lu.dernier_message_lu and not request.GET.get('page'):
        dernier_message_id = sujet_lu.dernier_message_lu.id
        if MessageForum.objects.filter(id=dernier_message_id).exists():
            messages_avant = liste_messages.filter(id__lt=dernier_message_id).count()
            page = (messages_avant // 20) + 1
            return redirect(f"{request.path}?page={page}#message-{dernier_message_id}")

    # Page actuelle
    page = request.GET.get('page', 1)

    # Formulaire de réponse
    if request.method == 'POST' and not sujet.est_ferme:
        contenu = request.POST.get('contenu')
        if contenu:
            nouveau_message = MessageForum.objects.create(
                sujet=sujet,
                auteur=request.user,
                contenu=contenu
            )
            sujet.date_dernier_message = timezone.now()
            sujet.save()

            # ✅ Marquer le sujet comme lu (avec le nouveau message)
            SujetLu.objects.update_or_create(
                utilisateur=request.user,
                sujet=sujet,
                defaults={'dernier_message_lu': nouveau_message}
            )

            messages.success(request, "Votre message a été ajouté !")
            return redirect('vegetables_fruits:forum_sujet', sujet_id=sujet.id)
        else:
            messages.error(request, "Veuillez écrire un message.")

    # Pagination
    paginator = Paginator(liste_messages, 20)
    messages_page = paginator.get_page(page)

    return render(request, 'vegetables_fruits/forum/sujet.html', {
        'sujet': sujet,
        'messages': messages_page,
        'est_enseignant': request.user.is_enseignant,
        'sujet_lu': sujet_lu,
    })


@login_required
@acces_forum_requis
def forum_nouveau_sujet(request, categorie_id):
    """Créer un nouveau sujet"""
    categorie = get_object_or_404(CategorieForum, id=categorie_id)

    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')

        if titre and contenu:
            sujet = SujetForum.objects.create(
                titre=titre,
                contenu=contenu,
                auteur=request.user,
                categorie=categorie
            )
            # Créer le premier message
            MessageForum.objects.create(
                sujet=sujet,
                auteur=request.user,
                contenu=contenu
            )
            messages.success(request, "Votre sujet a été créé !")
            return redirect('vegetables_fruits:forum_sujet', sujet_id=sujet.id)
        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    return render(request, 'vegetables_fruits/forum/nouveau_sujet.html', {
        'categorie': categorie,
    })


@login_required
@acces_forum_requis
def forum_repondre(request, sujet_id):
    """Répondre à un sujet (via AJAX ou formulaire)"""
    sujet = get_object_or_404(SujetForum, id=sujet_id, est_supprime=False)

    if sujet.est_ferme:
        return JsonResponse({'error': 'Ce sujet est fermé'}, status=400)

    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            message = MessageForum.objects.create(
                sujet=sujet,
                auteur=request.user,
                contenu=contenu
            )
            sujet.date_dernier_message = timezone.now()
            sujet.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message_id': message.id})
            else:
                messages.success(request, "Réponse ajoutée !")
                return redirect('vegetables_fruits:forum_sujet', sujet_id=sujet.id)

    return redirect('vegetables_fruits:forum_sujet', sujet_id=sujet.id)


# ==================== MODÉRATION (enseignants) ====================

@login_required
@acces_forum_requis
def forum_moderation(request):
    """Page de modération pour les enseignants"""
    if not request.user.is_enseignant:
        messages.error(request, "Accès non autorisé")
        return redirect('vegetables_fruits:forum_index')

    signalements = SignalementForum.objects.filter(statut='en_attente').order_by('-date_signalement')

    logger.debug(f" {signalements.count()} signalements en attente pour {request.user.username}")


    return render(request, 'vegetables_fruits/forum/moderation.html', {
        'signalements': signalements,
    })


@login_required
@acces_forum_requis
def forum_epingler(request, sujet_id):
    """Épingler/Désépingler un sujet"""
    if not request.user.is_enseignant:
        return JsonResponse({'error': 'Non autorisé'}, status=403)

    sujet = get_object_or_404(SujetForum, id=sujet_id)
    sujet.est_epingle = not sujet.est_epingle
    sujet.save()

    return redirect('vegetables_fruits:forum_categorie', categorie_id=sujet.categorie.id)


@login_required
@acces_forum_requis
def forum_fermer(request, sujet_id):
    """Fermer/Rouvrir un sujet"""
    if not request.user.is_enseignant:
        return JsonResponse({'error': 'Non autorisé'}, status=403)

    sujet = get_object_or_404(SujetForum, id=sujet_id)
    sujet.est_ferme = not sujet.est_ferme
    sujet.save()

    return redirect('vegetables_fruits:forum_sujet', sujet_id=sujet.id)


@login_required
@acces_forum_requis
def forum_supprimer_sujet(request, sujet_id):
    """Supprimer un sujet (soft delete)"""
    if not request.user.is_enseignant:
        return JsonResponse({'error': 'Non autorisé'}, status=403)

    sujet = get_object_or_404(SujetForum, id=sujet_id)
    sujet.est_supprime = True
    sujet.save()

    messages.success(request, "Sujet supprimé")
    return redirect('vegetables_fruits:forum_categorie', categorie_id=sujet.categorie.id)


@login_required
@acces_forum_requis
def forum_supprimer_message(request, message_id):
    """Supprimer un message"""
    if not request.user.is_enseignant:
        return JsonResponse({'error': 'Non autorisé'}, status=403)

    message = get_object_or_404(MessageForum, id=message_id)
    sujet_id = message.sujet.id
    message.delete()

    messages.success(request, "Message supprimé")
    return redirect('vegetables_fruits:forum_sujet', sujet_id=sujet_id)


@login_required
@acces_forum_requis
def forum_signalement(request, sujet_id=None, message_id=None):
    """Signaler un sujet ou un message"""

    # ✅ Récupérer depuis GET si les paramètres sont None
    if not sujet_id:
        sujet_id = request.GET.get('sujet_id')
    if not message_id:
        message_id = request.GET.get('message_id')

    if request.method == 'POST':
        raison = request.POST.get('raison')

        if sujet_id:
            sujet = get_object_or_404(SujetForum, id=sujet_id)
            SignalementForum.objects.create(
                sujet=sujet,
                signaleur=request.user,
                raison=raison
            )
        elif message_id:
            message = get_object_or_404(MessageForum, id=message_id)
            SignalementForum.objects.create(
                message=message,
                signaleur=request.user,
                raison=raison
            )

        messages.success(request, "Merci pour votre signalement. Un modérateur va l'examiner.")
        return redirect('vegetables_fruits:forum_index')

    return render(request, 'vegetables_fruits/forum/signaler.html', {
        'sujet_id': sujet_id,
        'message_id': message_id,
    })


@login_required
@acces_forum_requis
def forum_signalement_traiter(request, signalement_id):
    if not request.user.is_enseignant:
        messages.error(request, "Seuls les enseignants peuvent traiter les signalements.")
        return redirect('vegetables_fruits:forum_index')

    signalement = get_object_or_404(SignalementForum, id=signalement_id)

    if request.method == 'GET':
        return render(request, 'vegetables_fruits/forum/traiter_signalement.html', {
            'signalement': signalement,
        })

    action = request.POST.get('action')
    commentaire = request.POST.get('commentaire', '')

    if action == 'accepter':
        # ✅ NE SUPPRIMER QUE LE MESSAGE DE CE SIGNALEMENT
        if signalement.message:
            message = signalement.message
            message.delete()
            signalement.message = None  # ✅ Détacher la relation

        if signalement.sujet:
            signalement.sujet.est_supprime = True
            signalement.sujet.save()

        signalement.statut = 'traite'

    elif action == 'refuser':
        signalement.statut = 'refuse'

    signalement.moderateur = request.user
    signalement.commentaire_moderation = commentaire
    signalement.save()

    messages.success(request, "Signalement traité")
    return redirect('vegetables_fruits:forum_moderation')


@login_required
@acces_forum_requis
def forum_signalement_detail(request, signalement_id):
    """Afficher les détails d'un signalement (sans le traiter)"""
    if not request.user.is_enseignant:
        messages.error(request, "Accès non autorisé")
        return redirect('vegetables_fruits:forum_index')

    signalement = get_object_or_404(SignalementForum, id=signalement_id)

    return render(request, 'vegetables_fruits/forum/traiter_signalement.html', {
        'signalement': signalement,
    })

# ==================== GALERIE DES JARDINS ====================
from .models import PhotoJardin, CommentairePhoto, models

@login_required
def galerie_index(request):
    """Page d'accueil de la galerie"""
    # Photos à la une
    photos_a_la_une = PhotoJardin.objects.filter(est_a_la_une=True, est_publiee=True, est_validee=True)[:6]

    # Dernières photos
    dernieres_photos = PhotoJardin.objects.filter(est_publiee=True, est_validee=True).select_related('auteur').order_by('-date_creation')[:12]

    # Photos les plus likées
    plus_populaires = PhotoJardin.objects.filter(est_publiee=True, est_validee=True).annotate(
        nb_likes=models.Count('likes')
    ).order_by('-nb_likes')[:6]

    return render(request, 'vegetables_fruits/galerie/index.html', {
        'photos_a_la_une': photos_a_la_une,
        'dernieres_photos': dernieres_photos,
        'plus_populaires': plus_populaires,
    })


@login_required
def galerie_photos(request):
    """Liste de toutes les photos avec pagination"""
    photos = PhotoJardin.objects.filter(est_publiee=True, est_validee=True).order_by('-date_creation')

    paginator = Paginator(photos, 24)
    page = request.GET.get('page')
    photos_page = paginator.get_page(page)

    return render(request, 'vegetables_fruits/galerie/photos.html', {
        'photos': photos_page,
    })


@login_required
def galerie_upload(request):
    """Upload d'une photo avec compression et validation"""
    from PIL import Image as PilImage
    import io
    from django.core.files.base import ContentFile

    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        figure_id = request.POST.get('figure_id')

        # ===== VALIDATIONS =====
        if not image:
            messages.error(request, "Veuillez sélectionner une image")
            return redirect('vegetables_fruits:galerie_upload')

        # ✅ Validation MIME réelle + taille + intégrité
        valide, message_erreur = valider_image_upload(image, taille_max_mo=5)
        if not valide:
            logger.warning(f"Upload refusé ({image.name}) : {message_erreur}")
            messages.error(request, message_erreur)
            return redirect('vegetables_fruits:galerie_upload')

        # Vérifier les dimensions
        try:
            img_check = PilImage.open(image)
            if img_check.width > 5000 or img_check.height > 5000:
                messages.error(request, "L'image ne doit pas dépasser 5000x5000 pixels")
                return redirect('vegetables_fruits:galerie_upload')
        except:
            pass

        if not titre:
            messages.error(request, "Veuillez donner un titre à votre photo")
            return redirect('vegetables_fruits:galerie_upload')

        # ===== RÉCUPÉRATION DE LA PARCELLE =====
        figure = None
        if figure_id:
            figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)

        # ===== CRÉATION DE LA PHOTO (sans image d'abord) =====
        photo = PhotoJardin.objects.create(
            titre=titre,
            description=description,
            auteur=request.user,
            figure=figure,
            est_validee=request.user.is_enseignant  # Auto-validation pour enseignants
        )

        # ===== COMPRESSION ET REDIMENSIONNEMENT =====
        try:
            # Ouvrir l'image
            img = PilImage.open(image)

            # Convertir en RGB si nécessaire (pour PNG avec transparence)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Redimensionner si trop grande (max 1200px)
            max_size = 1200
            if img.width > max_size or img.height > max_size:
                img.thumbnail((max_size, max_size), PilImage.LANCZOS)

            # Compression JPEG (qualité 85)
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)

            # Sauvegarder l'image compressée
            photo.image.save(f"galerie_{photo.id}.jpg", ContentFile(output.read()), save=False)
            photo.save()

            # ✅ LOG DE VÉRIFICATION
            logger.debug(f"📸 Photo {photo.id} sauvegardée")

            logger.debug(f" Image name: {photo.image.name}")

            logger.debug(f" Image URL: {photo.image.url}")

            logger.debug(f" Image existe: {bool(photo.image)}")


        except Exception as e:
            logger.error(f"Erreur compression: {e}")

            # En cas d'erreur, garder l'image originale
            photo.image = image
            photo.save()

        # ===== MESSAGE DE CONFIRMATION =====
        if not request.user.is_enseignant:
            messages.success(request, "📸 Photo envoyée ! Un enseignant doit la valider avant publication.")
        else:
            messages.success(request, "📸 Photo publiée avec succès !")

        return redirect('vegetables_fruits:galerie_photo_detail', photo_id=photo.id)

    # GET : Afficher le formulaire
    figures = GeometricFigure.objects.filter(user=request.user)

    return render(request, 'vegetables_fruits/galerie/upload.html', {
        'figures': figures,
    })


@login_required
def galerie_photo_detail(request, photo_id):
    """Détail d'une photo avec commentaires"""
    photo = get_object_or_404(PhotoJardin, id=photo_id, est_publiee=True)

    # Vérifier si l'utilisateur a déjà liké
    user_liked = photo.likes.filter(id=request.user.id).exists()

    # Gestion des commentaires
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            CommentairePhoto.objects.create(
                photo=photo,
                auteur=request.user,
                contenu=contenu
            )
            if hasattr(request.user, 'profil_eleve'):
                verifier_competences(request.user.profil_eleve)
            messages.success(request, "Commentaire ajouté !")
            return redirect('vegetables_fruits:galerie_photo_detail', photo_id=photo.id)

    commentaires = photo.commentaires.all()
    # verifier_competences(request.user.profil_eleve)

    return render(request, 'vegetables_fruits/galerie/detail.html', {
        'photo': photo,
        'user_liked': user_liked,
        'commentaires': commentaires,
    })


@login_required
def galerie_liker(request, photo_id):
    """Liker/Unliker une photo (AJAX)"""
    photo = get_object_or_404(PhotoJardin, id=photo_id)

    if photo.likes.filter(id=request.user.id).exists():
        photo.likes.remove(request.user)
        liked = False
    else:
        photo.likes.add(request.user)
        liked = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'nb_likes': photo.nb_likes()
        })

    return redirect('vegetables_fruits:galerie_photo_detail', photo_id=photo.id)


# ==================== MODÉRATION GALERIE (enseignants) ====================

@login_required
def galerie_moderation(request):
    """Page de modération des photos (enseignants uniquement)"""
    if not request.user.is_enseignant:
        messages.error(request, "Accès non autorisé")
        return redirect('vegetables_fruits:galerie_index')

    photos_en_attente = PhotoJardin.objects.filter(est_validee=False, est_publiee=True).order_by('-date_creation')

    return render(request, 'vegetables_fruits/galerie/moderation.html', {
        'photos_en_attente': photos_en_attente,
    })


@login_required
def galerie_valider(request, photo_id):
    """Valider une photo (enseignants uniquement)"""
    if not request.user.is_enseignant:
        return JsonResponse({'error': 'Non autorisé'}, status=403)

    photo = get_object_or_404(PhotoJardin, id=photo_id)
    photo.est_validee = True
    photo.moderateur = request.user
    photo.save()

    messages.success(request, f"Photo '{photo.titre}' validée")
    return redirect('vegetables_fruits:galerie_moderation')


@login_required
def galerie_supprimer(request, photo_id):
    """Supprimer une photo (enseignants ou auteur)"""
    photo = get_object_or_404(PhotoJardin, id=photo_id)

    if not request.user.is_enseignant and photo.auteur != request.user:
        messages.error(request, "Vous ne pouvez pas supprimer cette photo")
        return redirect('vegetables_fruits:galerie_photo_detail', photo_id=photo.id)

    if request.method == 'POST':
        photo.delete()
        messages.success(request, "Photo supprimée")
        return redirect('vegetables_fruits:galerie_index')

    return render(request, 'vegetables_fruits/galerie/confirmer_suppression.html', {'photo': photo})


def nettoyer_photos_orphelines():
    """À exécuter quotidiennement (cron)"""
    date_limite = timezone.now() - timedelta(days=30)

    # Photos non validées de plus de 30 jours
    PhotoJardin.objects.filter(
        est_validee=False,
        date_creation__lt=date_limite
    ).delete()


# ==================== CLASSEMENT NATIONAL ====================

@login_required
def classement_national_eleves(request):
    """Classement de tous les élèves de France"""
    from django.db.models import Count, Sum, Avg, Q

    # Récupérer tous les élèves avec leurs infos
    eleves = Eleve.objects.select_related('user', 'classe').order_by('-points')

    # Filtrage par classe (pour les enseignants)
    classe_id = request.GET.get('classe', '')
    page = request.GET.get('page', '1')
    cache_key = f'classement_eleves_{request.user.id}_{page}_{classe_id}'
    cached_response = cache.get(cache_key)

    if cached_response:
        return cached_response


    if classe_id and request.user.is_enseignant:
        eleves = eleves.filter(classe_id=classe_id)

    # Statistiques globales
    stats = {
        'total_eleves': Eleve.objects.count(),
        'total_points': Eleve.objects.aggregate(total=Sum('points'))['total'] or 0,
        'moyenne_points': Eleve.objects.aggregate(moyenne=Avg('points'))['moyenne'] or 0,
        'total_badges': Badge.objects.count(),
        'meilleur_niveau': Eleve.objects.order_by('-niveau').first().niveau if Eleve.objects.exists() else 0,
    }

    # Top 10 (podium)
    top10 = []
    for i, eleve in enumerate(Eleve.objects.select_related('user', 'classe').order_by('-points')[:10], 1):
        top10.append({
            'rang': i,
            'eleve': eleve,
            'points': eleve.points,
            'niveau': eleve.niveau,
            'classe_nom': eleve.classe.nom if eleve.classe else 'Sans classe',
        })

    # Pagination
    paginator = Paginator(eleves, 50)
    page = request.GET.get('page')
    eleves_page = paginator.get_page(page)

    # Ajouter le rang à chaque élève
    classement = []
    start_index = (eleves_page.number - 1) * 50
    for i, eleve in enumerate(eleves_page, start_index + 1):
        classement.append({
            'rang': i,
            'eleve': eleve,
            'points': eleve.points,
            'niveau': eleve.niveau,
            'badge_count': eleve.badges.count(),
            'classe_nom': eleve.classe.nom if eleve.classe else 'Sans classe',
        })

    # Position de l'utilisateur connecté
    position_user = None
    if hasattr(request.user, 'profil_eleve'):
        eleve_user = request.user.profil_eleve
        position = Eleve.objects.filter(points__gt=eleve_user.points).count() + 1
        prochain_niveau = (eleve_user.niveau * 100) - (eleve_user.points % 100)
        position_user = {
            'rang': position,
            'eleve': eleve_user,
            'points': eleve_user.points,
            'niveau': eleve_user.niveau,
            'prochain_niveau': prochain_niveau if prochain_niveau > 0 else 0,
        }

    # Liste des classes pour le filtre (enseignants uniquement)
    classes_list = []
    if request.user.is_enseignant:
        classes_list = Classe.objects.filter(enseignant=request.user)

    response = render(request, 'vegetables_fruits/classement_national_eleves.html', {
        'classement': classement,
        'top10': top10,
        'stats': stats,
        'position_user': position_user,
        'eleves_page': eleves_page,
        'classes_list': classes_list,
        'classe_selectionnee': classe_id,
        'is_enseignant': request.user.is_enseignant,
    })

    cache.set(cache_key, response, 300)
    return response

@login_required
def classement_national_classes(request):
    """Classement des classes par points cumulés"""
    from django.db.models import Sum, Count, Avg

    classes = Classe.objects.annotate(
        points_totaux=Sum('eleves__points'),
        nb_eleves=Count('eleves'),
        moyenne=Avg('eleves__points')
    ).select_related('enseignant').filter(nb_eleves__gt=0).order_by('-points_totaux')

    # Statistiques globales
    stats = {
        'total_classes': classes.count(),
        'total_eleves': Eleve.objects.count(),
        'total_points': classes.aggregate(total=Sum('points_totaux'))['total'] or 0,
        'moyenne_par_classe': classes.aggregate(moyenne=Avg('points_totaux'))['moyenne'] or 0,
    }

    # Top 10 classes (podium)
    top10 = []
    for i, classe in enumerate(classes[:10], 1):
        top10.append({
            'rang': i,
            'classe': classe,
            'points_totaux': classe.points_totaux or 0,
            'nb_eleves': classe.nb_eleves,
            'moyenne': classe.moyenne or 0,
        })

    # Pagination
    paginator = Paginator(classes, 30)
    page = request.GET.get('page')
    classes_page = paginator.get_page(page)

    # Ajouter le rang
    classement_classes = []
    start_index = (classes_page.number - 1) * 30
    for i, classe in enumerate(classes_page, start_index + 1):
        classement_classes.append({
            'rang': i,
            'classe': classe,
            'points_totaux': classe.points_totaux or 0,
            'nb_eleves': classe.nb_eleves,
            'moyenne': classe.moyenne or 0,
            'meilleur_eleve': classe.eleves.order_by('-points').first(),
        })

    # Position de la classe de l'utilisateur
    position_classe = None
    if hasattr(request.user, 'profil_eleve') and request.user.profil_eleve.classe:
        classe_user = request.user.profil_eleve.classe
        # Calculer les points totaux de la classe de l'utilisateur
        points_user_classe = classe_user.eleves.aggregate(total=Sum('points'))['total'] or 0

        # Compter les classes avec plus de points
        position = classes.filter(points_totaux__gt=points_user_classe).count() + 1

        position_classe = {
            'rang': position,
            'classe': classe_user,
            'points_totaux': points_user_classe,
            'nb_eleves': classe_user.eleves.count(),
        }

    return render(request, 'vegetables_fruits/classement_national_classes.html', {
        'classement_classes': classement_classes,
        'top10': top10,
        'position_classe': position_classe,
        'stats': stats,
        'classes_page': classes_page,
    })

# ==================== UTILITAIRES POUR MISSIONS ====================

def get_semaine_annee():
    """Retourne le numéro de semaine et l'année"""
    from datetime import date
    aujourdhui = date.today()
    semaine = aujourdhui.isocalendar()[1]
    annee = aujourdhui.isocalendar()[0]
    return semaine, annee

@login_required
def missions_hebdomadaires(request):
    """Page des missions hebdomadaires adaptées à la région"""
    if not hasattr(request.user, 'profil_eleve'):
        messages.warning(request, "Accès réservé aux élèves")
        return redirect('vegetables_fruits:index')

    eleve = request.user.profil_eleve
    semaine, annee = get_semaine_annee()
    region = get_region_utilisateur(request.user)

    # Récupérer les missions adaptées à la région et à la saison
    missions = MissionHebdomadaire.objects.filter(
        est_active=True
    ).filter(
        Q(continent='tous') | Q(continent=region['continent'])
    ).filter(
        Q(saison='toute') | Q(saison=region['saison'])
    )

    # Récupérer les progressions
    progressions = {}
    for mission in missions:
        progression, created = ProgressionMissionHebdo.objects.get_or_create(
            eleve=eleve,
            mission=mission,
            semaine=semaine,
            annee=annee,
            defaults={'progression': 0}
        )
        progressions[mission.id] = progression

    # Statistiques
    stats = {
        'total': missions.count(),
        'completees': sum(1 for p in progressions.values() if p.est_complete),
        'points_gagnes': sum(p.mission.points_recompense for p in progressions.values() if p.est_complete),
    }

    # Streak
    streak, _ = StreakConnexion.objects.get_or_create(eleve=eleve)

    return render(request, 'vegetables_fruits/missions/missions_hebdo.html', {
        'missions': missions,
        'progressions': progressions,
        'stats': stats,
        'streak': streak,
        'semaine': semaine,
        'region': region,
    })


def creer_missions_par_defaut():
    """Crée les missions selon les régions"""

    missions = [
        # Europe - Printemps
        ('🌱 Semis de printemps', 'Plantez des tomates, courgettes ou salades', 'planter', 5, 20, 'Jardinier printanier',
         '🌱', 'europe', 'printemps', 'tomate'),
        ('🌸 Fleurs printanières', 'Plantez des fleurs pollinisatrices', 'fleur', 3, 15, 'Pollinisateur', '🌸', 'europe',
         'printemps', None),

        # Europe - Été
        ('🍅 Récolte d\'été', 'Récoltez vos tomates et courgettes', 'recolter', 10, 25, 'Récolteur estival', '🍅',
         'europe', 'ete', None),
        ('💧 Arrosage', 'Ajoutez 5 notes d\'arrosage', 'journal', 5, 15, 'Arroseur', '💧', 'europe', 'ete', None),

        # Europe - Automne
        ('🍎 Récolte d\'automne', 'Récoltez pommes et poires', 'recolter', 8, 20, 'Cueilleur', '🍎', 'europe', 'automne',
         None),
        ('🍂 Préparation hiver', 'Ajoutez des notes sur la protection des plantes', 'journal', 3, 15, 'Prévoyant', '🍂',
         'europe', 'automne', None),

        # Europe - Hiver
        ('📚 Apprentissage hivernal', 'Faites 5 quiz', 'quiz', 5, 30, 'Savant hivernal', '📚', 'europe', 'hiver', None),
        ('🌱 Semis intérieur', 'Planter des semis en intérieur', 'planter', 3, 20, 'Précurseur', '🌱', 'europe', 'hiver',
         None),

        # Afrique
        ('🌴 Jardin tropical', 'Plantez des légumes tropicaux', 'planter', 5, 25, 'Tropical', '🌴', 'afrique', 'toute',
         None),
        ('💧 Économie d\'eau', 'Ajoutez 3 notes sur l\'arrosage économique', 'journal', 3, 20, 'Économe', '💧', 'afrique',
         'toute', None),

        # Amérique
        ('🌽 Maïs et haricots', 'Plantez maïs ou haricots', 'planter', 5, 25, 'Milpa', '🌽', 'amerique', 'toute', 'mais'),
        ('🦋 Jardin pollinisateur', 'Plantez 5 fleurs pour attirer les papillons', 'fleur', 5, 20, 'Papillon', '🦋',
         'amerique', 'toute', None),

        # Asie
        ('🍚 Riz et légumes', 'Ajoutez 5 notes sur vos cultures', 'journal', 5, 20, 'Riziculteur', '🍚', 'asie', 'toute',
         None),
        ('🥬 Légumes asiatiques', 'Plantez des légumes asiatiques', 'planter', 3, 20, 'Asiatique', '🥬', 'asie', 'toute',
         None),

        # Océanie
        ('🪃 Jardin australien', 'Plantez 5 cultures natives', 'planter', 5, 25, 'Australien', '🪃', 'oceanie', 'toute',
         None),

        # Missions universelles (tous continents)
        ('📸 Paparazzi', 'Publiez 3 photos dans la galerie', 'like', 3, 15, 'Photographe', '📸', 'tous', 'toute', None),
        ('💬 Social', 'Commentez 5 photos', 'commentaire', 5, 20, 'Social', '💬', 'tous', 'toute', None),
        ('🔥 Streak', 'Connectez-vous 7 jours consécutifs', 'connexion', 7, 50, 'Flamme', '🔥', 'tous', 'toute', None),
    ]

    for titre, desc, type_action, obj, pts, badge, emoji, continent, saison, culture in missions:
        MissionHebdomadaire.objects.get_or_create(
            titre=titre,
            defaults={
                'description': desc,
                'type_action': type_action,
                'objectif': obj,
                'points_recompense': pts,
                'badge_nom': badge,
                'badge_emoji': emoji,
                'continent': continent,
                'saison': saison,
                'culture_cible': culture,
            }
        )


def verifier_competences(eleve):
    """Vérifie et débloque les compétences disponibles"""
    from .models import Competence, CompetenceDebloquee

    # Récupérer les compétences déjà débloquées
    debloquees = set(CompetenceDebloquee.objects.filter(eleve=eleve).values_list('competence_id', flat=True))

    # Compétences disponibles (niveau et points requis)
    competences_disponibles = Competence.objects.filter(
        est_active=True,
        niveau_requis__lte=eleve.niveau,
        points_requis__lte=eleve.points
    ).exclude(id__in=debloquees)

    nouvelles = []
    for comp in competences_disponibles:
        # Vérifier les prérequis
        prerequis_ok = True
        for prerequis in comp.prerequis.all():
            if prerequis.id not in debloquees:
                prerequis_ok = False
                break

        if not prerequis_ok:
            continue

        # Vérifier les actions requises
        actions_ok = True
        for action, nb in comp.actions_requises.items():
            # Compter les actions de l'élève
            compteur = 0
            if action == 'planter':
                compteur = eleve.user.geometricfigure_set.count()  # Approximation
            elif action == 'recolter':
                compteur = ChronologieCulture.objects.filter(figure__user=eleve.user, statut='recolte').count()
            elif action == 'quiz':
                compteur = QuizUtilisateur.objects.filter(user=eleve.user).count()
            elif action == 'journal':
                compteur = JournalBord.objects.filter(utilisateur=eleve.user).count()
            elif action == 'fleur':
                compteur = PhotoJardin.objects.filter(auteur=eleve.user, est_validee=True).count()
            elif action == 'connexion':
                streak, _ = StreakConnexion.objects.get_or_create(eleve=eleve)
                compteur = streak.jours_actuel
            elif action == 'like':
                compteur = PhotoJardin.objects.filter(likes=eleve.user).count()
            elif action == 'commentaire':
                compteur = CommentairePhoto.objects.filter(auteur=eleve.user).count()

            if compteur < nb:
                actions_ok = False
                break

        if actions_ok:
            # Débloquer la compétence
            CompetenceDebloquee.objects.create(eleve=eleve, competence=comp)
            nouvelles.append(comp)

            # Ajouter les points de récompense
            eleve.points += comp.points_recompense
            eleve.save()

            # Attribuer le badge
            if comp.badge_nom:
                badge, _ = Badge.objects.get_or_create(
                    nom=comp.badge_nom,
                    defaults={'emoji': comp.badge_emoji}
                )
                eleve.badges.add(badge)

    return nouvelles


@login_required
def arbre_competences(request):
    from .models import Competence, CompetenceDebloquee
    """Page affichant l'arbre des compétences"""
    if not hasattr(request.user, 'profil_eleve'):
        messages.warning(request, "Accès réservé aux élèves")
        return redirect('vegetables_fruits:index')

    eleve = request.user.profil_eleve
    toutes_competences = Competence.objects.filter(est_active=True)
    debloquees = CompetenceDebloquee.objects.filter(eleve=eleve).values_list('competence_id', flat=True)

    # Organiser par niveau
    competences_par_niveau = {}
    for comp in toutes_competences:
        niveau = comp.niveau_requis
        if niveau not in competences_par_niveau:
            competences_par_niveau[niveau] = []
        competences_par_niveau[niveau].append({
            'competence': comp,
            'debloquee': comp.id in debloquees,
            'prochain_niveau': f"Niveau {niveau + 1} requis" if comp.id not in debloquees else None
        })

    # Statistiques
    stats = {
        'total': toutes_competences.count(),
        'debloquees': len(debloquees),
        'pourcentage': int(len(debloquees) / toutes_competences.count() * 100) if toutes_competences.count() > 0 else 0,
    }

    return render(request, 'vegetables_fruits/competences/arbre.html', {
        'competences_par_niveau': competences_par_niveau,
        'stats': stats,
        'eleve': eleve,
    })


@login_required
def calendrier_semis(request):
    from .models import Parcelle, GeometricFigure

    user = request.user

    # ✅ Récupérer UNIQUEMENT les parcelles qui ont une figure
    parcelles = Parcelle.objects.filter(
        utilisateur=user,
        est_active=True,
        figure__isnull=False
    ).distinct()

    # ✅ Si tu veux une parcelle par figure (SQLite compatible)
    figures = GeometricFigure.objects.filter(user=user)
    parcelles_ids = []
    for figure in figures:
        parcelle = Parcelle.objects.filter(figure=figure, utilisateur=user).first()
        if parcelle:
            parcelles_ids.append(parcelle.id)
    parcelles = Parcelle.objects.filter(id__in=parcelles_ids)
    # Parcelle sélectionnée (via GET ou première)
    parcelle_id = request.GET.get('parcelle_id')
    selected_parcelle = None
    region = None

    if parcelle_id:
        try:
            selected_parcelle = parcelles.get(id=parcelle_id)
        except Parcelle.DoesNotExist:
            selected_parcelle = parcelles.first() if parcelles.exists() else None
    else:
        selected_parcelle = parcelles.first() if parcelles.exists() else None

    # ✅ Cascade de résolution du calendrier (Région → Pays → Continent → Tous)
    from .services import resoudre_calendrier_semis
    figure = selected_parcelle.figure if selected_parcelle else None
    calendrier, region, source = resoudre_calendrier_semis(user, figure)
    logger.info(f"📅 calendrier_semis — region={region} source={source} n={calendrier.count()}")

    # Organiser par mois pour l'affichage (gère les intervalles wrap : 11→2)
    from .services import organiser_calendrier_par_mois
    mois_data = organiser_calendrier_par_mois(calendrier)

    return render(request, 'vegetables_fruits/calendrier_semis.html', {
        'parcelles': parcelles,
        'selected_parcelle': selected_parcelle,
        'region': region,
        'mois_data': mois_data,
        'mois_actuel': datetime.now().month,
    })


def get_culture_emoji(self, culture_nom):
    """Retourne l'emoji d'une culture"""
    emojis = {
        'tomate': '🍅', 'carotte': '🥕', 'salade': '🥬', 'courgette': '🥒',
        'poivron': '🫑', 'aubergine': '🍆', 'haricot': '🫘', 'pomme de terre': '🥔',
        'oignon': '🧅', 'ail': '🧄', 'fraise': '🍓', 'pomme': '🍎',
        'poire': '🍐', 'cerise': '🍒', 'pêche': '🍑', 'raisin': '🍇',
    }
    return emojis.get(culture_nom.lower(), '🌱')


@login_required
def autosuffisance(request):
    """Calcule l'autosuffisance de l'utilisateur"""
    from datetime import date, timedelta

    user = request.user

    # ✅ Récupérer TOUTES les parcelles de l'utilisateur
    from .models import Parcelle
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    # ✅ Récupérer la parcelle sélectionnée (via GET)
    parcelle_id = request.GET.get('parcelle_id')
    selected_parcelle = None
    figure_id = None

    if parcelle_id:
        try:
            selected_parcelle = parcelles.get(id=parcelle_id)
            if selected_parcelle and selected_parcelle.figure:
                figure_id = selected_parcelle.figure.id
        except Parcelle.DoesNotExist:
            selected_parcelle = None

    # Si aucune parcelle sélectionnée, prendre la première
    if not selected_parcelle and parcelles.exists():
        selected_parcelle = parcelles.first()
        if selected_parcelle and selected_parcelle.figure:
            figure_id = selected_parcelle.figure.id

    # Récupérer ou créer le profil d'autosuffisance
    autosuffisance, created = Autosuffisance.objects.get_or_create(
        utilisateur=user,
        defaults={'besoin_annuel_kg': 200}
    )

    # ✅ Filtrer les récoltes par parcelle sélectionnée
    date_limite = date.today() - timedelta(days=365)

    if selected_parcelle and selected_parcelle.figure:
        recoltes = ChronologieCulture.objects.filter(
            figure=selected_parcelle.figure,
            statut='recolte',
            date_recolte_effective__gte=date_limite
        )
    else:
        recoltes = ChronologieCulture.objects.filter(
            figure__user=user,
            statut='recolte',
            date_recolte_effective__gte=date_limite
        )

    # Estimation par type de culture (valeurs approximatives en kg)
    poids_estimes = {
        'tomate': 3,
        'carotte': 0.5,
        'pomme de terre': 1,
        'courgette': 2,
        'salade': 0.3,
        'fraise': 0.5,
        'poivron': 0.8,
        'aubergine': 1,
        'concombre': 1.5,
        'haricot': 0.5,
        'petit pois': 0.5,
        'oignon': 0.2,
        'ail': 0.1,
        'betterave': 1,
        'radis': 0.1,
        'poireau': 0.4,
        'chou': 1.5,
        'brocoli': 0.8,
        'céleri': 0.8,
        'épinard': 0.3,
    }

    total_kg = 0
    details_recoltes = []

    for recolte in recoltes:
        culture = recolte.culture_nom.lower()
        poids = poids_estimes.get(culture, 0.5) # 500g par défaut
        total_kg += poids
        details_recoltes.append({
            'culture': recolte.culture_nom,
            'emoji': recolte.culture_emoji,
            'poids_estime': poids,
            'date': recolte.date_recolte_effective,
        })

    # Calcul du pourcentage d'autosuffisance
    besoin = autosuffisance.besoin_annuel_kg
    pourcentage = int((total_kg / besoin) * 100) if besoin > 0 else 0
    pourcentage = min(pourcentage, 100)

    # Progression
    if pourcentage < 25:
        niveau = "🌱 Débutant"
        message = "Continuez, chaque récolte compte !"
        conseil = "Ajoutez plus de légumes feuilles (salades, épinards) pour augmenter votre production."
    elif pourcentage < 50:
        niveau = "🌿 Jardinier en herbe"
        message = "Bon début ! Votre jardin prend forme."
        conseil = "Pensez aux légumes racines (carottes, pommes de terre) plus nourrissants."
    elif pourcentage < 75:
        niveau = "🌳 Jardinier confirmé"
        message = "Impressionnant ! Vous êtes sur la bonne voie."
        conseil = "Ajoutez des fruits et des légumes de saison pour varier."
    elif pourcentage < 100:
        niveau = "🌸 Expert"
        message = "Félicitations ! Vous produisez presque tout ce dont vous avez besoin."
        conseil = "Optimisez l'espace avec la rotation des cultures."
    else:
        niveau = "🏆 Maître jardinier"
        message = "Autosuffisant ! Vous êtes un modèle à suivre."
        conseil = "Partagez vos surplus avec votre communauté."

    return render(request, 'vegetables_fruits/autosuffisance.html', {
        'parcelles': parcelles, # ✅ AJOUTÉ
        'selected_parcelle': selected_parcelle, # ✅ AJOUTÉ
        'figure_id': figure_id, # ✅ AJOUTÉ
        'total_kg': round(total_kg, 1),
        'besoin': besoin,
        'pourcentage': pourcentage,
        'niveau': niveau,
        'message': message,
        'conseil': conseil,
        'details_recoltes': details_recoltes[:10],
        'total_recoltes': recoltes.count(),
    })


@login_required
def suggestions_personnalisees(request):
    """Suggestions de cultures personnalisées - Version mondiale exhaustive"""

    region_info = get_region_utilisateur(request.user)
    saison_actuelle = region_info['saison']
    region = region_info.get('region', 'Non définie').lower()
    pays = region_info.get('pays', 'Non défini').lower()
    continent = region_info.get('continent', 'europe')

    # Récupérer la première parcelle de l'utilisateur
    premiere_figure = GeometricFigure.objects.filter(user=request.user).first()
    figure_id = premiere_figure.id if premiere_figure else None

    # Récupérer les cultures déjà plantées
    cultures_plantees = set()
    for figure in GeometricFigure.objects.filter(user=request.user):
        for crop in figure.crops:
            if 'name' in crop:
                cultures_plantees.add(crop['name'].lower())

    # Récupérer les semis planifiés
    semis_planifies = set()
    for chrono in ChronologieCulture.objects.filter(figure__user=request.user):
        semis_planifies.add(chrono.culture_nom.lower())

    # Éviter les doublons
    cultures_existantes = cultures_plantees.union(semis_planifies)

    # ============================================================ #
    # SUGGESTIONS PAR PAYS/RÉGION (MONDIAL EXHAUSTIF) #
    # ============================================================ #

    suggestions_region = []

    # ==================== ASIE ====================
    if 'mongolie' in pays or 'mongolia' in pays:
        suggestions_region = [
            {'emoji': '🌾', 'culture': 'Millet', 'raison': 'Céréale traditionnelle mongole, résiste au froid',
             'difficulte': 1, 'temps': 90,
             'conseil': 'Semez en pleine terre après les gelées, résiste bien à la sécheresse.'},
            {'emoji': '🐫', 'culture': 'Argousier', 'raison': 'Baie riche en vitamines, résiste aux climats extrêmes',
             'difficulte': 2, 'temps': 365,
             'conseil': 'Plantez en plein soleil, sol bien drainé.'},
            {'emoji': '🍏', 'culture': 'Pommier sibérien', 'raison': 'Variété rustique résistant aux hivers mongols',
             'difficulte': 2, 'temps': 365,
             'conseil': 'Choisissez des variétés adaptées aux climats froids.'},
        ]
    elif 'chine' in pays or 'china' in pays:
        suggestions_region = [
            {'emoji': '🥬', 'culture': 'Chou chinois', 'raison': 'Légume de base en Chine', 'difficulte': 1, 'temps': 60,
             'conseil': 'Arrosez régulièrement, sol riche.'},
            {'emoji': '🍚', 'culture': 'Riz', 'raison': 'Céréale de base en Asie', 'difficulte': 2, 'temps': 150,
             'conseil': 'Maintenez une lame d\'eau permanente.'},
            {'emoji': '🐉', 'culture': 'Dragon (fruit)', 'raison': 'Fruit exotique, tendance en Chine', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Sol bien drainé, exposition ensoleillée.'},
            {'emoji': '🍵', 'culture': 'Thé', 'raison': 'Plante emblématique de Chine', 'difficulte': 2, 'temps': 365,
             'conseil': 'Sol acide, ombre partielle.'},
        ]
    elif 'japon' in pays or 'japan' in pays:
        suggestions_region = [
            {'emoji': '🍣', 'culture': 'Wasabi', 'raison': 'Plante emblématique du Japon', 'difficulte': 3, 'temps': 180,
             'conseil': 'Culture en milieu humide et frais, sol riche.'},
            {'emoji': '🎋', 'culture': 'Bambou', 'raison': 'Croissance rapide, très utile au Japon', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Contenez la croissance, plante envahissante.'},
            {'emoji': '🍑', 'culture': 'Pêche japonaise', 'raison': 'Variété réputée du Japon', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Protégez des gelées de printemps.'},
        ]
    elif 'inde' in pays or 'india' in pays:
        suggestions_region = [
            {'emoji': '🫚', 'culture': 'Gingembre', 'raison': 'Épice de base en Inde', 'difficulte': 1, 'temps': 180,
             'conseil': 'Sol riche et bien drainé, ombre partielle.'},
            {'emoji': '🧡', 'culture': 'Curcuma', 'raison': 'Épice dorée de l\'Inde', 'difficulte': 1, 'temps': 180,
             'conseil': 'Sol bien drainé, ombre partielle.'},
            {'emoji': '🍛', 'culture': 'Piment', 'raison': 'Indispensable dans la cuisine indienne', 'difficulte': 2,
             'temps': 80,
             'conseil': 'Chaleur et soleil nécessaire.'},
        ]
    elif 'thailande' in pays or 'thailand' in pays:
        suggestions_region = [
            {'emoji': '🍌', 'culture': 'Bananier', 'raison': 'Culture emblématique de Thaïlande', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Arrosez abondamment, protégez du vent.'},
            {'emoji': '🥥', 'culture': 'Noix de coco', 'raison': 'Fruit tropical par excellence', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Sol bien drainé, exposition ensoleillée.'},
            {'emoji': '🌿', 'culture': 'Citronnelle', 'raison': 'Aromatique de base en cuisine thaï', 'difficulte': 1,
             'temps': 180,
             'conseil': 'Arrosez régulièrement, plein soleil.'},
        ]
    elif 'vietnam' in pays:
        suggestions_region = [
            {'emoji': '🍚', 'culture': 'Riz', 'raison': 'Céréale de base au Vietnam', 'difficulte': 2, 'temps': 150,
             'conseil': 'Rizière inondée pour meilleure croissance.'},
            {'emoji': '☕', 'culture': 'Café', 'raison': 'Le Vietnam est le 2ème producteur mondial', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Sol bien drainé, ombre partielle.'},
            {'emoji': '🌶️', 'culture': 'Piment oiseau', 'raison': 'Très utilisé au Vietnam', 'difficulte': 2,
             'temps': 80,
             'conseil': 'Exposition ensoleillée, sol riche.'},
        ]
    elif 'coree' in pays or 'korea' in pays:
        suggestions_region = [
            {'emoji': '🥬', 'culture': 'Chou coréen', 'raison': 'Base du kimchi', 'difficulte': 1, 'temps': 70,
             'conseil': 'Arrosez régulièrement, sol riche.'},
            {'emoji': '🍐', 'culture': 'Poire asiatique', 'raison': 'Fruit populaire en Corée', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Sol bien drainé, exposition ensoleillée.'},
        ]

    # ==================== AFRIQUE ====================
    elif 'maroc' in pays or 'morocco' in pays:
        suggestions_region = [
            {'emoji': '🫒', 'culture': 'Olivier', 'raison': 'Culture ancestrale du Maroc', 'difficulte': 2, 'temps': 365,
             'conseil': 'Résiste bien à la sécheresse.'},
            {'emoji': '🍊', 'culture': 'Oranger', 'raison': 'Agrumes emblématiques du Maroc', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Protégez du froid en hiver.'},
            {'emoji': '🌹', 'culture': 'Rose de Damas', 'raison': 'Cultivée pour l\'eau de rose', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Plein soleil, sol bien drainé.'},
        ]
    elif 'senegal' in pays:
        suggestions_region = [
            {'emoji': '🥜', 'culture': 'Arachide', 'raison': 'Culture emblématique du Sénégal', 'difficulte': 1,
             'temps': 120,
             'conseil': 'Sol sableux, exposition ensoleillée.'},
            {'emoji': '🍚', 'culture': 'Riz', 'raison': 'Base de l\'alimentation sénégalaise', 'difficulte': 2,
             'temps': 150,
             'conseil': 'Nécessite une lame d\'eau permanente.'},
        ]
    elif 'nigeria' in pays:
        suggestions_region = [
            {'emoji': '🍠', 'culture': 'Ignames', 'raison': 'Aliment de base au Nigeria', 'difficulte': 2, 'temps': 365,
             'conseil': 'Sol profond et bien drainé.'},
            {'emoji': '🌴', 'culture': 'Palmier à huile', 'raison': 'Culture importante au Nigeria', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Climat tropical humide.'},
        ]
    elif 'kenya' in pays:
        suggestions_region = [
            {'emoji': '☕', 'culture': 'Café', 'raison': 'Café réputé du Kenya', 'difficulte': 2, 'temps': 365,
             'conseil': 'Altitude élevée, sol volcanique.'},
            {'emoji': '🌺', 'culture': 'Hibiscus', 'raison': 'Fleur nationale du Kenya', 'difficulte': 1, 'temps': 180,
             'conseil': 'Arrosez régulièrement, plein soleil.'},
        ]
    elif 'egypte' in pays or 'egypt' in pays:
        suggestions_region = [
            {'emoji': '🌾', 'culture': 'Blé', 'raison': 'Céréale emblématique d\'Égypte', 'difficulte': 1, 'temps': 180,
             'conseil': 'Sol limoneux, irrigation régulière.'},
            {'emoji': '🌴', 'culture': 'Dattier', 'raison': 'Fruit emblématique d\'Égypte', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Résiste bien à la sécheresse.'},
        ]
    elif 'afrique du sud' in pays or 'south africa' in pays:
        suggestions_region = [
            {'emoji': '🍇', 'culture': 'Vigne', 'raison': 'Viticulture réputée en Afrique du Sud', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Climat méditerranéen.'},
            {'emoji': '🌻', 'culture': 'Tournesol', 'raison': 'Grande production en Afrique du Sud', 'difficulte': 1,
             'temps': 90,
             'conseil': 'Plein soleil, sol bien drainé.'},
        ]

    # ==================== AMÉRIQUE ====================
    elif 'bresil' in pays or 'brazil' in pays:
        suggestions_region = [
            {'emoji': '🍫', 'culture': 'Cacao', 'raison': 'Le Brésil est un grand producteur', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Ombre partielle, sol riche.'},
            {'emoji': '☕', 'culture': 'Café', 'raison': 'Le Brésil est le 1er producteur mondial', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Sol bien drainé, altitude.'},
            {'emoji': '🥭', 'culture': 'Mangue', 'raison': 'Fruit tropical emblématique', 'difficulte': 2, 'temps': 365,
             'conseil': 'Climat tropical, sol bien drainé.'},
        ]
    elif 'argentine' in pays or 'argentina' in pays:
        suggestions_region = [
            {'emoji': '🍷', 'culture': 'Vigne', 'raison': 'Viticulture réputée en Argentine', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Climat sec, ensoleillé.'},
            {'emoji': '🌾', 'culture': 'Blé', 'raison': 'Céréale importante en Argentine', 'difficulte': 1, 'temps': 180,
             'conseil': 'Grandes plaines, sol fertile.'},
        ]
    elif 'chili' in pays or 'chile' in pays:
        suggestions_region = [
            {'emoji': '🍷', 'culture': 'Vigne', 'raison': 'Vins réputés du Chili', 'difficulte': 2, 'temps': 365,
             'conseil': 'Climat méditerranéen.'},
            {'emoji': '🥑', 'culture': 'Avocat', 'raison': 'Grand producteur d\'avocats', 'difficulte': 2, 'temps': 365,
             'conseil': 'Sol bien drainé, climat doux.'},
        ]
    elif 'mexique' in pays:
        suggestions_region = [
            {'emoji': '🌽', 'culture': 'Maïs', 'raison': 'Origine du maïs, culture sacrée', 'difficulte': 1,
             'temps': 100,
             'conseil': 'Plantez en carré pour pollinisation.'},
            {'emoji': '🌶️', 'culture': 'Piment jalapeño', 'raison': 'Piment emblématique du Mexique', 'difficulte': 2,
             'temps': 80,
             'conseil': 'Chaleur et soleil nécessaire.'},
            {'emoji': '🍫', 'culture': 'Cacao', 'raison': 'Origine du cacao', 'difficulte': 2, 'temps': 365,
             'conseil': 'Climat tropical humide.'},
        ]
    elif 'perou' in pays or 'peru' in pays:
        suggestions_region = [
            {'emoji': '🥔', 'culture': 'Pomme de terre', 'raison': 'Origine des Andes, milliers de variétés',
             'difficulte': 1, 'temps': 90,
             'conseil': 'Sol bien drainé, altitude.'},
            {'emoji': '🌿', 'culture': 'Quinoa', 'raison': 'Super-aliment andin', 'difficulte': 1, 'temps': 180,
             'conseil': 'Sol bien drainé, résiste à la sécheresse.'},
        ]

    # ==================== OCÉANIE ====================
    elif 'australie' in pays or 'australia' in pays:
        suggestions_region = [
            {'emoji': '🪃', 'culture': 'Eucalyptus', 'raison': 'Arbre emblématique d\'Australie', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Sol bien drainé, exposition ensoleillée.'},
            {'emoji': '🍇', 'culture': 'Vigne', 'raison': 'Viticulture réputée en Australie', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Climat méditerranéen.'},
            {'emoji': '🌾', 'culture': 'Blé', 'raison': 'Grand producteur de blé', 'difficulte': 1, 'temps': 180,
             'conseil': 'Grandes plaines, sol fertile.'},
        ]
    elif 'nouvelle-zelande' in pays or 'new zealand' in pays:
        suggestions_region = [
            {'emoji': '🥝', 'culture': 'Kiwi', 'raison': 'Fruit emblématique de Nouvelle-Zélande', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Plantez un mâle pour 4-5 femelles.'},
            {'emoji': '🍇', 'culture': 'Vigne', 'raison': 'Viticulture réputée', 'difficulte': 2, 'temps': 365,
             'conseil': 'Climat océanique.'},
        ]

    # ==================== EUROPE ====================
    elif 'italie' in pays or 'italy' in pays:
        suggestions_region = [
            {'emoji': '🍅', 'culture': 'Tomate', 'raison': 'Tomate italienne réputée', 'difficulte': 2, 'temps': 90,
             'conseil': 'Plein soleil, tuteurez.'},
            {'emoji': '🌿', 'culture': 'Basilic', 'raison': 'Base de la cuisine italienne', 'difficulte': 1, 'temps': 40,
             'conseil': 'Arrosez régulièrement sans mouiller les feuilles.'},
            {'emoji': '🍇', 'culture': 'Vigne', 'raison': 'Viticulture emblématique', 'difficulte': 2, 'temps': 365,
             'conseil': 'Climat méditerranéen.'},
        ]
    elif 'espagne' in pays or 'spain' in pays:
        suggestions_region = [
            {'emoji': '🫒', 'culture': 'Olivier', 'raison': 'Olive espagnole réputée', 'difficulte': 2, 'temps': 365,
             'conseil': 'Résiste bien à la sécheresse.'},
            {'emoji': '🍊', 'culture': 'Oranger', 'raison': 'Agrumes espagnols', 'difficulte': 2, 'temps': 365,
             'conseil': 'Protégez du froid en hiver.'},
        ]
    elif 'france' in pays:
        suggestions_region = [
            {'emoji': '🍇', 'culture': 'Vigne', 'raison': 'Viticulture française réputée', 'difficulte': 2, 'temps': 365,
             'conseil': 'Climat adapté selon région.'},
            {'emoji': '🌻', 'culture': 'Tournesol', 'raison': 'Champ de tournesols en France', 'difficulte': 1,
             'temps': 90,
             'conseil': 'Plein soleil, sol bien drainé.'},
        ]
    elif 'suisse' in pays or 'switzerland' in pays:
        suggestions_region = [
            {'emoji': '🌿', 'culture': 'Gentiane', 'raison': 'Plante des Alpes suisses', 'difficulte': 2, 'temps': 365,
             'conseil': 'Altitude, sol calcaire.'},
        ]

    # ==================== TROPIQUES ====================
    elif 'tropical' in region or 'hawaï' in pays or 'hawaii' in pays:
        suggestions_region = [
            {'emoji': '🍍', 'culture': 'Ananas', 'raison': 'Fruit tropical par excellence', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Sol bien drainé, exposition ensoleillée.'},
            {'emoji': '🌺', 'culture': 'Hibiscus', 'raison': 'Fleur tropicale emblématique', 'difficulte': 1,
             'temps': 180,
             'conseil': 'Arrosez régulièrement, protégez du froid.'},
            {'emoji': '🍌', 'culture': 'Bananier', 'raison': 'Fruit tropical de base', 'difficulte': 2, 'temps': 365,
             'conseil': 'Arrosez abondamment.'},
            {'emoji': '🥥', 'culture': 'Noix de coco', 'raison': 'Culture tropicale essentielle', 'difficulte': 2,
             'temps': 365,
             'conseil': 'Sol sableux, climat chaud.'},
        ]

    # ============================================================ #
    # SUGGESTIONS PAR SAISON (UNIVERSELLES) #
    # ============================================================ #
    suggestions_saison = []

    if saison_actuelle == 'printemps':
        suggestions_saison = [
            {'emoji': '🫛', 'culture': 'Petits pois', 'raison': 'Idéal pour le printemps', 'difficulte': 1, 'temps': 60,
             'conseil': 'Semez en ligne, tuteurez légèrement.'},
            {'emoji': '🥔', 'culture': 'Pomme de terre', 'raison': 'Se plante au printemps', 'difficulte': 1,
             'temps': 90,
             'conseil': 'Buttez les pieds pour favoriser la croissance.'},
        ]
    elif saison_actuelle == 'ete':
        suggestions_saison = [
            {'emoji': '🍆', 'culture': 'Aubergine', 'raison': 'Parfaite pour l\'été', 'difficulte': 2, 'temps': 80,
             'conseil': 'Chaleur et soleil nécessaire.'},
            {'emoji': '🌽', 'culture': 'Maïs', 'raison': 'Original et gratifiant', 'difficulte': 2, 'temps': 100,
             'conseil': 'Plantez en carré pour favoriser la pollinisation.'},
            {'emoji': '🍉', 'culture': 'Pastèque', 'raison': 'Rafraîchissante pour l\'été', 'difficulte': 2, 'temps': 90,
             'conseil': 'Arrosez régulièrement, sol chaud.'},
        ]
    elif saison_actuelle == 'automne':
        suggestions_saison = [
            {'emoji': '🍎', 'culture': 'Pommier', 'raison': 'À planter en automne', 'difficulte': 2, 'temps': 365,
             'conseil': 'Prévoyez de l\'espace pour la croissance.'},
            {'emoji': '🍓', 'culture': 'Fraisier', 'raison': 'À planter en automne', 'difficulte': 1, 'temps': 180,
             'conseil': 'Paillez pour protéger du froid.'},
        ]
    else:  # hiver
        suggestions_saison = [
            {'emoji': '🥬', 'culture': 'Chou', 'raison': 'Résiste au froid', 'difficulte': 2, 'temps': 120,
             'conseil': 'Protégez du gel avec un voile.'},
            {'emoji': '🧄', 'culture': 'Ail', 'raison': 'À planter avant l\'hiver', 'difficulte': 1, 'temps': 180,
             'conseil': 'Plantez les gousses pointe vers le haut.'},
        ]

    # ============================================================ #
    # FILTRER ET COMBINER #
    # ============================================================ #
    suggestions = []

    # 1. Suggestions régionales (priorité max)
    for s in suggestions_region:
        if s['culture'].lower() not in cultures_existantes:
            suggestions.append(s)

    # 2. Suggestions saisonnières
    for s in suggestions_saison:
        if s['culture'].lower() not in cultures_existantes:
            suggestions.append(s)

    # 3. Suggestions par défaut (si besoin)
    suggestions_defaut = [
        {'emoji': '🥬', 'culture': 'Salade', 'raison': 'Pousse rapide (30j), facile', 'difficulte': 1, 'temps': 30,
         'conseil': 'Semez tous les 15 jours pour des récoltes étalées.'},
        {'emoji': '🥕', 'culture': 'Carotte', 'raison': 'Riche en vitamines, se conserve bien', 'difficulte': 1,
         'temps': 70, 'conseil': 'Éclaircissez à 5cm pour de belles carottes.'},
        {'emoji': '🍅', 'culture': 'Tomate', 'raison': 'Prolifique, idéale pour débuter', 'difficulte': 2, 'temps': 90,
         'conseil': 'Tuteurez dès la plantation.'},
        {'emoji': '🌿', 'culture': 'Basilic', 'raison': 'Aromatique, parfait en pot', 'difficulte': 1, 'temps': 40,
         'conseil': 'Arrosez régulièrement sans mouiller les feuilles.'},
    ]

    for s in suggestions_defaut:
        if s['culture'].lower() not in cultures_existantes:
            suggestions.append(s)

    # Limiter à 8 suggestions
    suggestions = suggestions[:8]

    for s in suggestions:
        s['conseils'] = get_conseils_culture(s['culture'])

    return render(request, 'vegetables_fruits/suggestions.html', {
        'suggestions': suggestions,
        'saison': saison_actuelle,
        'region': region,
        'pays': pays,
        'continent': continent,
        'cultures_plantees': len(cultures_plantees),
        'semis_planifies': len(semis_planifies),
        'figure_id': figure_id,
    })


@login_required
def placer_culture(request, figure_id):
    """Ajoute directement une culture à une parcelle"""
    figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)
    culture_nom = request.GET.get('culture')

    if culture_nom:
        # Chercher si c'est un fruit ou un légume
        fruit = Fruit.objects.filter(nom__icontains=culture_nom).first()
        vegetable = Vegetable.objects.filter(nom__icontains=culture_nom).first()

        culture_data = {
            'name': culture_nom,
            'emoji': fruit.get_emoji() if fruit else (vegetable.get_emoji() if vegetable else '🌱'),
            'lat': figure.adresse_lat or 0,
            'lng': figure.adresse_lng or 0,
            'date_placement': timezone.now().isoformat()
        }

        if fruit:
            culture_data['fruit_id'] = fruit.id
            culture_data['type'] = 'fruit'
        elif vegetable:
            culture_data['vegetable_id'] = vegetable.id
            culture_data['type'] = 'vegetable'

        # Ajouter la culture à la parcelle
        crops = figure.crops or []
        crops.append(culture_data)
        figure.crops = crops
        figure.save()

        messages.success(request, f"🌱 {culture_nom} a été ajouté à votre parcelle '{figure.name}' !")
    else:
        messages.error(request, "Culture non spécifiée")

    return redirect('vegetables_fruits:figure_detail', figure_id=figure.id)


@login_required
def choisir_parcelle(request):
    """Page pour choisir la parcelle où planter la culture"""
    culture_nom = request.GET.get('culture')
    figures = GeometricFigure.objects.filter(user=request.user)

    return render(request, 'vegetables_fruits/choisir_parcelle.html', {
        'figures': figures,
        'culture_nom': culture_nom,
    })


# Configuration des rappels automatiques par mails

@login_required
def mes_rappels(request):


    """Gérer les rappels email"""
    rappels = RappelUtilisateur.objects.filter(utilisateur=request.user)

    if request.method == 'POST':
        type_rappel = request.POST.get('type_rappel')
        culture = request.POST.get('culture')
        date_prochain_rappel = request.POST.get('date_prochain_rappel')
        frequence_jours = request.POST.get('frequence_jours', 7)
        message_personnalise = request.POST.get('message_personnalise', '')

        RappelUtilisateur.objects.create(
            utilisateur=request.user,
            type_rappel=type_rappel,
            culture=culture,
            date_prochain_rappel=date_prochain_rappel,
            frequence_jours=frequence_jours,
            message_personnalise=message_personnalise,
        )
        messages.success(request, "Rappel ajouté avec succès !")
        return redirect('vegetables_fruits:mes_rappels')

    # Récupérer les cultures de l'utilisateur pour le sélecteur
    cultures_user = set()
    for figure in GeometricFigure.objects.filter(user=request.user):
        for crop in figure.crops:
            if 'name' in crop:
                cultures_user.add(crop['name'])

    return render(request, 'vegetables_fruits/rappels.html', {
        'rappels': rappels,
        'cultures_user': sorted(cultures_user),
    })


@login_required
def supprimer_rappel(request, rappel_id):
    """Supprimer un rappel"""
    rappel = get_object_or_404(RappelUtilisateur, id=rappel_id, utilisateur=request.user)
    rappel.delete()
    messages.success(request, "Rappel supprimé")
    return redirect('vegetables_fruits:mes_rappels')


@login_required
def toggle_rappel(request, rappel_id):
    """Activer/Désactiver un rappel"""
    rappel = get_object_or_404(RappelUtilisateur, id=rappel_id, utilisateur=request.user)
    rappel.actif = not rappel.actif
    rappel.save()
    status = "activé" if rappel.actif else "désactivé"
    messages.success(request, f"Rappel {status}")
    return redirect('vegetables_fruits:mes_rappels')


@login_required
def api_enregistrer_calendrier(request):
    logger.debug("🔔 API enregistrer_calendrier appelée !")


    if request.method == 'POST':
        import json
        from datetime import datetime, timedelta
        from .models import CalendrierUser, GeometricFigure, ChronologieCulture

        try:
            data = json.loads(request.body)
            logger.debug(f"📦 Data: {data}")


            culture = data.get('culture')
            date_semis_str = data.get('date_semis')
            date_plantation_str = data.get('date_plantation')
            figure_id = data.get('figure_id')

            figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)

            # Conversion des dates
            date_semis = None
            date_plantation = None
            if date_semis_str:
                date_semis = datetime.strptime(date_semis_str, '%Y-%m-%d').date()
            if date_plantation_str:
                date_plantation = datetime.strptime(date_plantation_str, '%Y-%m-%d').date()

            logger.debug(f"🌱 date_semis: {date_semis}")

            logger.debug(f"🌿 date_plantation: {date_plantation}")


            # ✅ CRÉER LE CALENDRIER
            calendrier, created = CalendrierUser.objects.get_or_create(
                utilisateur=request.user,
                figure=figure,
                culture=culture,
                defaults={
                    'date_semis': date_semis,
                    'date_plantation': date_plantation,
                }
            )
            logger.info(f"📅 Calendrier: {'créé' if created else 'existant'}")

            # ✅ Récupérer la durée réelle de la culture (Fruit > Vegetable > Culture)
            from .models import Fruit, Vegetable, Culture as CultureModel

            jours_recolte_reel = 90  # fallback
            emoji_reel = '🌱'

            fruit = Fruit.objects.filter(nom__iexact=culture).first()
            vegetable = Vegetable.objects.filter(nom__iexact=culture).first()
            culture_obj = CultureModel.objects.filter(nom__iexact=culture).first()

            if fruit and fruit.jours_recolte and fruit.jours_recolte > 0:
                jours_recolte_reel = fruit.jours_recolte
                emoji_reel = fruit.get_emoji()
            elif vegetable and vegetable.jours_recolte and vegetable.jours_recolte > 0:
                jours_recolte_reel = vegetable.jours_recolte
                emoji_reel = vegetable.get_emoji()
            elif culture_obj:
                if culture_obj.jours_pousse and culture_obj.jours_pousse > 0:
                    jours_recolte_reel = culture_obj.jours_pousse
                elif culture_obj.duree_culture_max_jours and culture_obj.duree_culture_max_jours > 0:
                    jours_recolte_reel = culture_obj.duree_culture_max_jours
                emoji_reel = culture_obj.get_emoji() if hasattr(culture_obj, 'get_emoji') else '🌱'

            logger.info(f"🌱 {culture} → {jours_recolte_reel} jours (emoji: {emoji_reel})")

            chrono, chrono_created = ChronologieCulture.objects.get_or_create(
                figure=figure,
                culture_nom__iexact=culture,
                defaults={
                    'culture_nom': culture,
                    'culture_emoji': emoji_reel,
                    'date_semis': date_semis,
                    'date_recolte_prevue': date_semis + timedelta(days=jours_recolte_reel) if date_semis else None,
                    'statut': 'seme',
                    'progression': 0,
                }
            )

            # ✅ Si la chrono existait déjà, recalculer avec la bonne durée
            if not chrono_created and chrono.date_semis:
                chrono.date_recolte_prevue = chrono.date_semis + timedelta(days=jours_recolte_reel)
                if not chrono.culture_emoji or chrono.culture_emoji == '🌱':
                    chrono.culture_emoji = emoji_reel
                chrono.calculer_progression()
                logger.info(f"🔄 Chrono {chrono.id} recalculée → récolte prévue le {chrono.date_recolte_prevue}")


            return JsonResponse({'success': True, 'chrono_created': chrono_created})

        except Exception as e:
            logger.error(f"❌ Erreur: {e}")

            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=400)

@login_required
def api_verifier_saison(request):
    """
    Vérifie si les cultures placées sont dans leur saison.
    POST JSON : { "crops": [...], "figure_id": 12 }
    Retour : { "hors_saison": [...], "region": "...", "total_verifiees": N }
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON invalide'}, status=400)

    crops = data.get('crops', [])
    figure_id = data.get('figure_id')

    figure = None
    if figure_id:
        figure = GeometricFigure.objects.filter(id=figure_id, user=request.user).first()

    from .services import verifier_saison_cultures
    resultat = verifier_saison_cultures(crops, request.user, figure)

    return JsonResponse(resultat)


@login_required
def mes_semis(request):
    """Affiche les semis personnels de l'utilisateur"""
    semis = CalendrierUser.objects.filter(utilisateur=request.user).order_by('-date_semis')

    for semis_item in semis:
        if semis_item.culture:
            semis_item.culture = semis_item.culture.replace('\n', '').strip()

    return render(request, 'vegetables_fruits/mes_semis.html', {
        'semis': semis,
    })

@login_required
def api_supprimer_semis(request, semis_id):
    """Supprimer un semis personnel"""
    if request.method == 'DELETE':
        semis = get_object_or_404(CalendrierUser, id=semis_id, utilisateur=request.user)
        semis.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Méthode non autorisée'}, status=400)


@login_required
def besoins_eau(request):
    """Calcul des besoins en eau pour une parcelle sélectionnée"""
    user = request.user

    # Récupérer toutes les parcelles de l'utilisateur
    figures = GeometricFigure.objects.filter(user=user)

    # Récupérer la parcelle sélectionnée
    figure_id = request.GET.get('figure_id')
    figure = None
    if figure_id:
        try:
            figure = GeometricFigure.objects.get(id=figure_id, user=user)
        except GeometricFigure.DoesNotExist:
            figure = None

    # Récupérer l'unité choisie
    unite = request.GET.get('unite', 'm2')

    # Récupérer la région
    if figure:
        region_info = get_region_utilisateur(user, figure)
    else:
        region_info = get_region_utilisateur(user)
    region = region_info['region']

    # Calculer les besoins pour la parcelle sélectionnée
    besoins_cultures = []
    total_besoins = 0
    cultures = []
    surface_affichee = 0
    unite_affichee = 'm²'
    surface_calcul = 0

    if figure:
        # Récupérer les cultures de la parcelle
        for crop in figure.crops:
            if 'name' in crop:
                cultures.append(crop['name'])

        # Calculer la surface
        if figure.surface_hectares:
            surface_m2 = figure.surface_hectares * 10000
            if unite == 'ha':
                surface_affichee = figure.surface_hectares
                unite_affichee = 'ha'
            else:
                surface_affichee = surface_m2
                unite_affichee = 'm²'
            surface_calcul = surface_m2 # Toujours en m² pour les calculs
        else:
            surface_calcul = 0

        # Calculer les besoins pour chaque culture
        for culture in cultures:
            besoin_data = BesoinsEau.objects.filter(culture__icontains=culture).first()
            if besoin_data:
                # ✅ SÉCURISATION TOTALE DU COEFFICIENT
                coeffs = besoin_data.coefficient_region
                coefficient = 1.0  # Par défaut

                if isinstance(coeffs, dict):
                    # On cherche la région (ex: 'japon')
                    val = coeffs.get(region, 1.0)
                    # Si la valeur trouvée est un nombre, on l'utilise
                    if isinstance(val, (int, float)):
                        coefficient = float(val)
                    # Si c'est encore un dict (nested), on prend la première valeur numérique
                    elif isinstance(val, dict):
                        numeric_vals = [v for v in val.values() if isinstance(v, (int, float))]
                        if numeric_vals:
                            coefficient = float(numeric_vals[0])
                elif isinstance(coeffs, (int, float)):
                    coefficient = float(coeffs)

                # Maintenant on est sûr que coefficient est un float
                besoin_ajuste = besoin_data.besoin_litres_par_m2 * coefficient

                if surface_calcul > 0:
                    besoin_total = besoin_ajuste * surface_calcul
                    total_besoins += besoin_total
                else:
                    besoin_total = 0

                besoins_cultures.append({
                    'culture': culture,
                    'besoin_base': besoin_data.besoin_litres_par_m2,
                    'coefficient': coefficient,
                    'besoin_ajuste': round(besoin_ajuste, 1),
                    'frequence': besoin_data.frequence_arrosage_jours,
                    'periode_sensible': besoin_data.periode_sensible,
                    'besoin_total': round(besoin_total, 1),
                })

    # Message si aucune parcelle sélectionnée
    if not figure and figures.exists():
        message = "Veuillez sélectionner une parcelle."
    elif not figures.exists():
        message = "Vous n'avez pas encore de parcelle. Créez-en une !"
    else:
        message = None

    return render(request, 'vegetables_fruits/besoins_eau.html', {
        'figures': figures,
        'figure': figure,
        'figure_id': figure_id,
        'unite': unite,
        'cultures': cultures,
        'besoins_cultures': besoins_cultures,
        'total_besoins': round(total_besoins, 1),
        'region': region,
        'message': message,
        'surface_affichee': round(surface_affichee, 1),
        'unite_affichee': unite_affichee,
    })



@login_required
def rotation_cultures(request, figure_id=None):
    """Plan de rotation des cultures sur 4 ans (Premium, Enseignant ou Élève en classe)"""

    # ✅ Vérification d'accès : Premium, Enseignant OU Élève dans une classe
    est_eleve = hasattr(request.user, 'profil_eleve') and request.user.profil_eleve and request.user.profil_eleve.classe is not None

    if not est_eleve:
        try:
            abonnement = request.user.abonnement
            if not abonnement.est_actif or abonnement.plan.nom not in ['PREMIUM', 'ENSEIGNANT']:
                messages.warning(request, "🔒 La rotation des cultures est disponible avec l'abonnement Premium.")
                return redirect('vegetables_fruits:tarification')
        except Abonnement.DoesNotExist:
            messages.warning(request, "🔒 La rotation des cultures est disponible avec l'abonnement Premium.")
            return redirect('vegetables_fruits:tarification')

    # Récupérer toutes les parcelles de l'utilisateur
    figures = GeometricFigure.objects.filter(user=request.user)

    # Gérer le paramètre GET (si envoyé via le formulaire)
    if not figure_id and request.GET.get('figure_id'):
        figure_id = request.GET.get('figure_id')

    figure = None
    if figure_id:
        figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)
    elif figures.exists():
        figure = figures.first()

    # Récupérer les cultures de la parcelle
    cultures_parcelle = []
    if figure:
        for crop in figure.crops:
            if 'name' in crop:
                cultures_parcelle.append(crop['name'])

    # Calculer l'année actuelle dans le cycle (0-3)
    from datetime import date
    annee_cycle = date.today().year % 4

    # Récupérer les recommandations pour chaque culture
    recommandations = []
    for culture in cultures_parcelle:
        rotation = RotationCulture.objects.filter(culture__icontains=culture).first()
        if rotation:
            recommandations.append({
                'culture': culture,
                'famille': rotation.famille,
                'plan_annee1': rotation.annee1,
                'plan_annee2': rotation.annee2,
                'plan_annee3': rotation.annee3,
                'plan_annee4': rotation.annee4,
                'conseils': rotation.conseils,
                'recommande': [
                    rotation.annee1, rotation.annee2, rotation.annee3, rotation.annee4
                ][annee_cycle] if annee_cycle < 4 else rotation.annee1,
            })

    # Noms des années pour l'affichage
    noms_annees = ['Année 1', 'Année 2', 'Année 3', 'Année 4']

    return render(request, 'vegetables_fruits/rotation_cultures.html', {
        'figure': figure,
        'figures': figures,
        'cultures_parcelle': cultures_parcelle,
        'recommandations': recommandations,
        'annee_cycle': annee_cycle + 1,
        'noms_annees': noms_annees,
    })



# COMPANION_PLANTING
@login_required
def companion_planting(request, figure_id=None):
    """Guide des associations bénéfiques (Companion planting) (Premium, Enseignant ou Élève en classe)"""

    # ✅ Vérification d'accès : Premium, Enseignant OU Élève dans une classe
    est_eleve = hasattr(request.user, 'profil_eleve') and request.user.profil_eleve and request.user.profil_eleve.classe is not None

    if not est_eleve:
        try:
            abonnement = request.user.abonnement
            if not abonnement.est_actif or abonnement.plan.nom not in ['PREMIUM', 'ENSEIGNANT']:
                messages.warning(request, "🔒 Le compagnonnage est disponible avec l'abonnement Premium.")
                return redirect('vegetables_fruits:tarification')
        except Abonnement.DoesNotExist:
            messages.warning(request, "🔒 Le compagnonnage est disponible avec l'abonnement Premium.")
            return redirect('vegetables_fruits:tarification')

    # Récupérer la région de l'utilisateur
    region_info = get_region_utilisateur(request.user)
    pays = region_info['pays'].lower()
    continent = region_info['continent']

    # Récupérer TOUTES les parcelles de l'utilisateur
    figures = GeometricFigure.objects.filter(user=request.user)

    figure = None
    if figure_id:
        figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)
    elif figures.exists():
        # Si aucune parcelle sélectionnée mais qu'il y en a, prendre la première
        figure = figures.first()

    # Récupérer les cultures de la parcelle
    cultures_parcelle = []
    if figure:
        for crop in figure.crops:
            if 'name' in crop:
                cultures_parcelle.append(crop['name'])

    # Pour chaque culture, trouver les bonnes et mauvaises associations
    associations_result = []
    for culture in cultures_parcelle:
        bonnes = AssociationCulture.objects.filter(
            culture1__icontains=culture,
            type_association='bonne'
        ).filter(pays__in=['tous', pays, continent])

        mauvaises = AssociationCulture.objects.filter(
            culture1__icontains=culture,
            type_association='mauvaise'
        ).filter(pays__in=['tous', pays, continent])

        # Associations où culture est culture2
        bonnes2 = AssociationCulture.objects.filter(
            culture2__icontains=culture,
            type_association='bonne'
        ).filter(pays__in=['tous', pays, continent])

        mauvaises2 = AssociationCulture.objects.filter(
            culture2__icontains=culture,
            type_association='mauvaise'
        ).filter(pays__in=['tous', pays, continent])

        associations_result.append({
            'culture': culture,
            'bonnes': list(bonnes) + list(bonnes2),
            'mauvaises': list(mauvaises) + list(mauvaises2),
        })

    suggestions_fleurs = [
        '🌼 Œillet d\'Inde', '🌸 Capucine', '🌻 Tournesol', '🌿 Lavande',
        '🌸 Bourrache', '🌼 Souci', '🌻 Cosmos', '🌼 Alysse'
    ]

    return render(request, 'vegetables_fruits/companion_planting.html', {
        'figure': figure,
        'figures': figures,
        'associations': associations_result,
        'suggestions_fleurs': suggestions_fleurs,
        'pays': pays,
        'continent': continent,
    })



# Plan d'irrigation d'eau

@login_required
def plan_irrigation(request):
    """Génère un plan d'arrosage hebdomadaire personnalisé avec graphique et rappels"""
    user = request.user
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True).prefetch_related('besoins_eau')

    # Récupérer la parcelle sélectionnée (optionnel)
    selected_parcelle_id = request.GET.get('parcelle_id')
    if selected_parcelle_id:
        parcelles = parcelles.filter(id=selected_parcelle_id)

    # Calculer le plan pour chaque parcelle
    plan_parcelles = []
    total_litres_semaine = 0
    labels_graphique = []
    data_graphique = []

    for parcelle in parcelles:
        besoins = parcelle.besoins_eau.all()
        parcelle_plan = {
            'parcelle': parcelle,
            'cultures': [],
            'total_litres_semaine': 0
        }

        for besoin in besoins:
            # Calcul des besoins hebdomadaires
            litres_semaine = besoin.besoin_litres_par_m2 * parcelle.surface_m2 * 7
            parcelle_plan['total_litres_semaine'] += litres_semaine
            total_litres_semaine += litres_semaine

            # Fréquence d'arrosage
            intervalle = besoin.frequence_arrosage_jours
            if intervalle > 0:
                litres_par_arrosage = litres_semaine / (7 / intervalle)
            else:
                litres_par_arrosage = litres_semaine / 7

            # Jours recommandés
            from datetime import date, timedelta
            aujourdhui = date.today()
            jours_recommandes = []
            for i in range(0, 7, intervalle):
                jours_recommandes.append((aujourdhui + timedelta(days=i)).strftime('%A %d/%m'))

            parcelle_plan['cultures'].append({
                'culture': besoin.culture,
                'litres_semaine': round(litres_semaine, 1),
                'litres_par_arrosage': round(litres_par_arrosage, 1),
                'frequence_jours': intervalle,
                'jours_recommandes': jours_recommandes,
                'periode_sensible': besoin.periode_sensible,
            })

        if parcelle_plan['cultures']:
            plan_parcelles.append(parcelle_plan)
            labels_graphique.append(parcelle.nom)
            data_graphique.append(round(parcelle_plan['total_litres_semaine'], 1))

    # Récupérer toutes les parcelles pour le filtre
    toutes_parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    return render(request, 'vegetables_fruits/plan_irrigation.html', {
        'plan_parcelles': plan_parcelles,
        'toutes_parcelles': toutes_parcelles,
        'selected_parcelle_id': selected_parcelle_id,
        'total_litres_semaine': round(total_litres_semaine, 1),
        'labels_graphique': labels_graphique,
        'data_graphique': data_graphique,
    })


@login_required
def export_plan_irrigation_pdf(request):
    """Exporte le plan d'irrigation au format PDF"""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from datetime import date

    user = request.user
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    # Créer la réponse PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="plan_irrigation_{date.today().strftime("%Y%m%d")}.pdf"'

    # Créer le document
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#28a745'),
        alignment=1  # Centre
    )
    elements.append(Paragraph("💧 Plan d'irrigation hebdomadaire", title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Utilisateur : {user.username}", styles['Normal']))
    elements.append(Paragraph(f"Date : {date.today().strftime('%d/%m/%Y')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    total_litres_semaine = 0

    for parcelle in parcelles:
        besoins = BesoinsEau.objects.filter(parcelle=parcelle)
        if not besoins:
            continue

        # Titre de la parcelle
        elements.append(Paragraph(f"🌱 {parcelle.nom} ({parcelle.surface_m2} m²)", styles['Heading2']))
        elements.append(Spacer(1, 5))

        # Tableau pour cette parcelle
        data = [['Culture', 'Besoins hebdo (L)', 'Par arrosage (L)', 'Fréquence (jours)', 'Jours recommandés']]

        for besoin in besoins:
            litres_semaine = besoin.besoin_litres_par_m2 * parcelle.surface_m2 * 7
            total_litres_semaine += litres_semaine

            intervalle = besoin.frequence_arrosage_jours
            if intervalle > 0:
                litres_par_arrosage = litres_semaine / (7 / intervalle)
            else:
                litres_par_arrosage = litres_semaine / 7

            from datetime import date, timedelta
            aujourdhui = date.today()
            jours = []
            for i in range(0, 7, intervalle):
                jours.append((aujourdhui + timedelta(days=i)).strftime('%A %d/%m'))

            data.append([
                besoin.culture,
                f"{round(litres_semaine, 1)}",
                f"{round(litres_par_arrosage, 1)}",
                f"Tous les {intervalle}",
                ", ".join(jours)
            ])

        # Créer le tableau
        table = Table(data, colWidths=[3 * cm, 3 * cm, 3 * cm, 3 * cm, 5 * cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

    # Total général
    elements.append(
        Paragraph(f"📊 Total des besoins hebdomadaires : {round(total_litres_semaine, 1)} L", styles['Heading3']))

    # Construire le PDF
    doc.build(elements)
    return response


@login_required
def creer_rappel_arrosage(request, parcelle_id):
    """Crée un rappel d'arrosage pour une parcelle"""
    parcelle = get_object_or_404(Parcelle, id=parcelle_id, utilisateur=request.user)

    if request.method == 'POST':
        date_rappel = request.POST.get('date_rappel')
        message_personnalise = request.POST.get('message_personnalise', '')

        RappelUtilisateur.objects.create(
            utilisateur=request.user,
            type_rappel='arrosage',
            culture=request.POST.get('culture', ''),
            message_personnalise=message_personnalise,
            date_prochain_rappel=date_rappel,
            frequence_jours=request.POST.get('frequence_jours', 3),
            actif=True
        )
        messages.success(request, "✅ Rappel d'arrosage créé !")
        return redirect('vegetables_fruits:plan_irrigation')

    # Récupérer les cultures de la parcelle
    besoins = BesoinsEau.objects.filter(parcelle=parcelle)

    return render(request, 'vegetables_fruits/creer_rappel_arrosage.html', {
        'parcelle': parcelle,
        'besoins': besoins,
    })


def a_acces_bilan_carbone(user):
    # Élève en classe
    if hasattr(user, 'profil_eleve') and user.profil_eleve and user.profil_eleve.classe is not None:
        return True

    try:
        abonnement = user.abonnement
        return abonnement.est_actif and abonnement.plan.nom in ['PREMIUM', 'ENSEIGNANT']
    except Abonnement.DoesNotExist:
        return False


@login_required
def bilan_carbone(request, eleve_id=None):
    """Calcule et affiche le bilan carbone des parcelles de l'utilisateur"""
    from .models import Parcelle, BilanCarbone, Production, Eleve, Classe, Abonnement

    user = request.user

    # ✅ Vérification : Est-ce un élève dans une classe ?
    est_eleve_en_classe = False
    if hasattr(user, 'profil_eleve') and user.profil_eleve:
        if user.profil_eleve.classe is not None:
            est_eleve_en_classe = True

    # ✅ Vérification abonnement
    acces_abonnement = a_acces_bilan_carbone(request.user)
    acces = est_eleve_en_classe or acces_abonnement

    if not acces:
        messages.warning(request, "🔒 Le bilan carbone est disponible avec les abonnements Premium ou Enseignant.")
        return redirect('vegetables_fruits:tarification')

    # ✅ Récupérer la parcelle sélectionnée
    parcelle_id = request.GET.get('parcelle_id')
    selected_parcelle = None
    selected_parcelle_id = None

    if parcelle_id:
        try:
            selected_parcelle = Parcelle.objects.get(id=parcelle_id, utilisateur=user, est_active=True)
            selected_parcelle_id = selected_parcelle.id
        except Parcelle.DoesNotExist:
            selected_parcelle = None

    # ✅ Récupérer toutes les parcelles pour le sélecteur
    toutes_parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    # ✅ Filtrer les parcelles pour les calculs
    parcelles = toutes_parcelles
    if selected_parcelle:
        parcelles = parcelles.filter(id=selected_parcelle.id)

    total_emission = 0
    total_sequestration = 0
    total_bilan = 0
    details_parcelles = []
    labels_graphique = []
    data_emission = []
    data_sequestration = []

    parcelles = parcelles.prefetch_related('productions')

    for parcelle in parcelles:
        productions = parcelle.productions.all()
        cultures_count = productions.count()

        emission = cultures_count * 5.0
        sequestration = parcelle.surface_m2 * 0.2

        bilan, created = BilanCarbone.objects.get_or_create(
            parcelle=parcelle,
            defaults={
                'emission_co2_kg': emission,
                'sequestration_co2_kg': sequestration,
                'bilan_net_kg': sequestration - emission,
            }
        )
        if not created:
            bilan.emission_co2_kg = emission
            bilan.sequestration_co2_kg = sequestration
            bilan.bilan_net_kg = sequestration - emission
            bilan.save()

        total_emission += emission
        total_sequestration += sequestration
        total_bilan += bilan.bilan_net_kg

        labels_graphique.append(parcelle.nom)
        data_emission.append(round(emission, 1))
        data_sequestration.append(round(sequestration, 1))

        details_parcelles.append({
            'parcelle': parcelle,
            'emission': round(emission, 1),
            'sequestration': round(sequestration, 1),
            'bilan': round(bilan.bilan_net_kg, 1),
            'cultures': cultures_count,
        })

    # Statut
    if total_bilan > 0:
        statut = {'icone': '🌱', 'message': 'Votre jardin est un puits de carbone !', 'couleur': 'success'}
    elif total_bilan < 0:
        statut = {'icone': '⚠️', 'message': 'Votre jardin émet plus de CO₂ qu\'il n\'en séquestre.', 'couleur': 'warning'}
    else:
        statut = {'icone': '⚖️', 'message': 'Votre jardin est neutre en carbone.', 'couleur': 'info'}

    return render(request, 'vegetables_fruits/bilan_carbone.html', {
        'details_parcelles': details_parcelles,
        'total_emission': round(total_emission, 1),
        'total_sequestration': round(total_sequestration, 1),
        'total_bilan': round(total_bilan, 1),
        'labels_graphique': labels_graphique,
        'data_emission': data_emission,
        'data_sequestration': data_sequestration,
        'statut': statut,
        'a_acces_bilan_carbone': acces,
        'parcelles': toutes_parcelles, # ✅ Toutes pour le sélecteur
        'selected_parcelle_id': selected_parcelle_id, # ✅ Pour pré-sélectionner
    })


@login_required
def export_bilan_carbone_pdf(request):
    """Exporte le bilan carbone au format PDF"""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from datetime import date


    user = request.user
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    # Créer la réponse PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bilan_carbone_{date.today().strftime("%Y%m%d")}.pdf"'

    # Créer le document
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#28a745'),
        alignment=1  # Centre
    )
    elements.append(Paragraph("🌍 Bilan carbone de votre jardin", title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Utilisateur : {user.username}", styles['Normal']))
    elements.append(Paragraph(f"Date : {date.today().strftime('%d/%m/%Y')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Totaux globaux
    total_emission = 0
    total_sequestration = 0
    total_bilan = 0

    for parcelle in parcelles:
        bilan = BilanCarbone.objects.filter(parcelle=parcelle).first()
        if bilan:
            total_emission += bilan.emission_co2_kg
            total_sequestration += bilan.sequestration_co2_kg
            total_bilan += bilan.bilan_net_kg

    # Résumé global
    elements.append(Paragraph("📊 Résumé global", styles['Heading2']))
    elements.append(Spacer(1, 5))

    resume_data = [
        ['Indicateur', 'Valeur'],
        ['Émissions totales', f"{round(total_emission, 1)} kg CO₂"],
        ['Séquestration totale', f"{round(total_sequestration, 1)} kg CO₂"],
        ['Bilan net', f"{round(total_bilan, 1)} kg CO₂"],
    ]

    resume_table = Table(resume_data, colWidths=[6 * cm, 6 * cm])
    resume_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
    ]))
    elements.append(resume_table)
    elements.append(Spacer(1, 20))

    # Détail par parcelle
    elements.append(Paragraph("📋 Détail par parcelle", styles['Heading2']))
    elements.append(Spacer(1, 5))

    for parcelle in parcelles:
        bilan = BilanCarbone.objects.filter(parcelle=parcelle).first()
        if bilan:
            # Titre de la parcelle
            elements.append(Paragraph(f"🌱 {parcelle.nom}", styles['Heading3']))
            elements.append(Spacer(1, 3))

            # Tableau pour cette parcelle
            data = [
                ['Indicateur', 'Valeur'],
                ['Émissions', f"{round(bilan.emission_co2_kg, 1)} kg CO₂"],
                ['Séquestration', f"{round(bilan.sequestration_co2_kg, 1)} kg CO₂"],
                ['Bilan net', f"{round(bilan.bilan_net_kg, 1)} kg CO₂"],
            ]

            table = Table(data, colWidths=[6 * cm, 6 * cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 10))

    # Construire le PDF
    doc.build(elements)
    return response


from django.core.cache import cache
from django.db.models import Count, Sum, Q
from django.http import JsonResponse
from datetime import date, timedelta


# ============================================================
# HELPERS
# ============================================================
def _periode_vers_date(periode):
    """Convertit un code période en date de début."""
    today = date.today()
    if periode == '30j':
        return today - timedelta(days=30)
    elif periode == '6m':
        return today - timedelta(days=180)
    elif periode == '12m':
        return today - timedelta(days=365)
    return None # 'tout'


def _compute_stats(user, figure_id=None, periode='12m'):
    """
    Calcule toutes les stats nécessaires pour le dashboard Bento.
    Retourne un dict prêt à être sérialisé en JSON.
    """
    from .models import (
        GeometricFigure, ChronologieCulture, Parcelle,
        CalendrierUser, JournalBord, AlerteTraitement,
    )

    # ---- Filtres de base ----
    figures_qs = GeometricFigure.objects.filter(user=user)
    if figure_id:
        figures_qs = figures_qs.filter(id=figure_id)

    date_debut = _periode_vers_date(periode)

    # ---- Figures et crops ----
    figures = list(figures_qs)
    nb_parcelles = len(figures)
    surface_totale = sum((f.surface_hectares or 0) * 10000 for f in figures)

    # Récupérer les crops de toutes les figures en mémoire
    tous_les_crops = []
    for f in figures:
        if f.crops:
            for crop in f.crops:
                if crop.get('name'):
                    crop['_figure_id'] = f.id
                    crop['_figure_name'] = f.name
                    tous_les_crops.append(crop)

    nb_cultures_distinctes = len(set(c['name'] for c in tous_les_crops))

    # ---- Chronologies ----
    chronos_qs = ChronologieCulture.objects.filter(figure__in=figures)
    if date_debut:
        chronos_qs = chronos_qs.filter(date_semis__gte=date_debut)

    chronos = list(chronos_qs)

    nb_recoltes = sum(1 for c in chronos if c.statut == 'recolte')

    # États pour le camembert
    statuts_count = {'en_cours': 0, 'a_planifier': 0, 'recoltees': 0}
    for c in chronos:
        if c.statut == 'recolte':
            statuts_count['recoltees'] += 1
        else:
            statuts_count['en_cours'] += 1

    # Compter les crops sans chronologie
    noms_avec_chrono = set()
    for c in chronos:
        if c.culture_nom:
            noms_avec_chrono.add(c.culture_nom.lower())

    for crop in tous_les_crops:
        if crop['name'].lower() not in noms_avec_chrono:
            statuts_count['a_planifier'] += 1

    # ---- Répartition par type de culture ----
    from .models import Fruit, Vegetable, Culture

    # On classe par Fruit/Vegetable/Culture/Autre
    noms_fruits = set(Fruit.objects.values_list('nom', flat=True))
    noms_vegetables = set(Vegetable.objects.values_list('nom', flat=True))

    repartition_types = {'legumes': 0, 'fruits': 0, 'autres': 0}
    for crop in tous_les_crops:
        nom = crop['name']
        if nom in noms_fruits:
            repartition_types['fruits'] += 1
        elif nom in noms_vegetables:
            repartition_types['legumes'] += 1
        else:
            repartition_types['autres'] += 1

    # ---- Répartition surface par parcelle ----
    surfaces_parcelles = [
        {'nom': f.name[:20], 'surface': round((f.surface_hectares or 0) * 10000, 1)}
        for f in figures
    ]

    # ---- Timeline : prochaines actions ----
    timeline = []

    # Semis planifiés
    semis_qs = CalendrierUser.objects.filter(
        utilisateur=user,
        date_semis__gte=date.today(),
    ).order_by('date_semis')[:5]
    for s in semis_qs:
        if figure_id and (not s.figure or s.figure.id != figure_id):
            continue
        timeline.append({
            'date': s.date_semis.strftime('%d %b'),
            'type': 'semis',
            'emoji': '🌱',
            'culture': s.culture,
            'parcelle': s.figure.name if s.figure else '—',
            'date_iso': s.date_semis.isoformat(),
        })

    # Récoltes prévues
    recoltes_qs = ChronologieCulture.objects.filter(
        figure__in=figures,
        date_recolte_prevue__gte=date.today(),
    ).exclude(statut='recolte').order_by('date_recolte_prevue')[:5]
    for r in recoltes_qs:
        timeline.append({
            'date': r.date_recolte_prevue.strftime('%d %b'),
            'type': 'recolte',
            'emoji': r.culture_emoji or '🍅',
            'culture': r.culture_nom,
            'parcelle': r.figure.name,
            'date_iso': r.date_recolte_prevue.isoformat(),
        })

    timeline.sort(key=lambda x: x['date_iso'])
    timeline = timeline[:8]

    # ---- Points totaux ----
    points_totaux = 0
    if hasattr(user, 'profil_eleve') and user.profil_eleve:
        points_totaux = user.profil_eleve.points
    else:
        # Estimation pour les particuliers
        nb_notes = JournalBord.objects.filter(
            utilisateur=user,
            date_note__gte=date_debut if date_debut else date.min,
        ).count()
        nb_alertes = AlerteTraitement.objects.filter(
            utilisateur=user,
            statut='traitee',
        ).count()
        points_totaux = (nb_notes * 5) + (nb_cultures_distinctes * 3) + (nb_recoltes * 5)

    # ---- Historique points (12 mois) ----
    historique = []
    today = date.today()
    for i in range(11, -1, -1):
        mois_date = today - timedelta(days=30 * i)
        mois_str = mois_date.strftime('%b %Y')
        # Simulation - à remplacer par un vrai calcul historique plus tard
        points_mois = max(0, points_totaux // 12 + (i * 3))
        historique.append({'mois': mois_str, 'points': points_mois})

    # ---- Liste compacte des parcelles ----
    parcelles_compactes = []
    for f in figures:
        nb_crops = len(f.crops) if f.crops else 0
        parcelles_compactes.append({
            'id': f.id,
            'nom': f.name[:25],
            'surface': round((f.surface_hectares or 0) * 10000, 1),
            'nb_cultures': nb_crops,
        })

    # ---- Stats journal ----
    nb_notes_journal = JournalBord.objects.filter(
        utilisateur=user,
    ).count()

    # ---- Économie du jardin ----
    from .services_economie import calculer_valeur_jardin
    economie = calculer_valeur_jardin(user, figure_id=figure_id)

    # ---- Historique valeur (12 derniers mois) ----
    from .models import HistoriqueValeurJardin
    historique_valeur = list(
        HistoriqueValeurJardin.objects.filter(
            utilisateur=user,
        ).order_by('mois').values('mois', 'valeur_potentielle', 'valeur_realisee')[:12]
    )
    # Formatter pour Chart.js
    historique_valeur = [
        {
            'mois': h['mois'].strftime('%b %Y') if h['mois'] else '',
            'potentielle': round(h['valeur_potentielle'], 2),
            'realisee': round(h['valeur_realisee'], 2),
        }
        for h in historique_valeur
    ]

    return {
        'stats': {
            'points_totaux': points_totaux,
            'nb_parcelles': nb_parcelles,
            'surface_totale': round(surface_totale, 1),
            'nb_cultures_distinctes': nb_cultures_distinctes,
            'nb_recoltes': nb_recoltes,
            'nb_notes_journal': nb_notes_journal,
        },
        'repartition_types': repartition_types,
        'statuts': statuts_count,
        'surfaces_parcelles': surfaces_parcelles,
        'timeline': timeline,
        'historique_points': historique,
        'parcelles': parcelles_compactes,
        'economie': economie,
        'historique_valeur': historique_valeur,
    }


# ============================================================
# VUE PRINCIPALE
# ============================================================
@login_required
def statistiques_avancees(request):
    """Dashboard Premium : statistiques Bento."""
    # ✅ Vérification d'accès
    est_eleve = (
        hasattr(request.user, 'profil_eleve')
        and request.user.profil_eleve
        and request.user.profil_eleve.classe is not None
    )

    if not est_eleve:
        try:
            abonnement = request.user.abonnement
            if not abonnement.est_actif or abonnement.plan.nom not in ['PREMIUM', 'ENSEIGNANT']:
                messages.warning(request, "🔒 Les statistiques avancées sont disponibles avec l'abonnement Premium.")
                return redirect('vegetables_fruits:tarification')
        except Abonnement.DoesNotExist:
            messages.warning(request, "🔒 Les statistiques avancées sont disponibles avec l'abonnement Premium.")
            return redirect('vegetables_fruits:tarification')

    # ✅ Récupérer les parcelles pour le sélecteur
    from .models import GeometricFigure
    figures = GeometricFigure.objects.filter(user=request.user).order_by('name')

    # ✅ Params de filtre (URL)
    figure_id = request.GET.get('parcelle')
    periode = request.GET.get('periode', '12m')

    # ✅ Cache 5 min
    cache_key = f"stats_bento_{request.user.id}_{figure_id or 'all'}_{periode}"
    data = cache.get(cache_key)

    if not data:
        data = _compute_stats(request.user, figure_id=figure_id, periode=periode)
        cache.set(cache_key, data, 300)

    context = {
        'figures': figures,
        'selected_figure_id': int(figure_id) if figure_id else None,
        'selected_periode': periode,
        'data_json': data, # pour le rendu initial côté template
        **data, # déverse aussi les clés pour accès direct
    }

    return render(request, 'vegetables_fruits/statistiques_avancees.html', context)


# ============================================================
# ENDPOINT AJAX
# ============================================================
@login_required
def api_stats_bento(request):
    """Endpoint AJAX pour recharger les stats sans refresh."""
    # Vérif abonnement
    est_eleve = (
        hasattr(request.user, 'profil_eleve')
        and request.user.profil_eleve
        and request.user.profil_eleve.classe is not None
    )
    if not est_eleve:
        try:
            abonnement = request.user.abonnement
            if not abonnement.est_actif or abonnement.plan.nom not in ['PREMIUM', 'ENSEIGNANT']:
                return JsonResponse({'error': 'Premium requis'}, status=403)
        except Abonnement.DoesNotExist:
            return JsonResponse({'error': 'Premium requis'}, status=403)

    figure_id = request.GET.get('parcelle')
    periode = request.GET.get('periode', '12m')

    cache_key = f"stats_bento_{request.user.id}_{figure_id or 'all'}_{periode}"
    data = cache.get(cache_key)
    if not data:
        data = _compute_stats(request.user, figure_id=figure_id, periode=periode)
        cache.set(cache_key, data, 300)

    return JsonResponse(data)


@login_required
def alertes_meteo_avancees(request):
    from .models import Parcelle, AlerteMeteo, Culture
    from django.conf import settings
    import requests
    from datetime import date, timedelta
    from django.utils import timezone

    user = request.user

    # ✅ Seuils par défaut (si non définis dans la base)
    SEUILS_DEFAUT = {
        'gel': 0,
        'canicule': 35,
        'pluie': 20,
        'vent': 50,
    }

    # Récupérer TOUTES les parcelles
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True).select_related('figure')

    parcelles_meteo = []
    alertes_globales = []

    for parcelle in parcelles:
        meteo_data = None
        alertes_parcelle = []

        if parcelle.figure and parcelle.figure.adresse_lat and parcelle.figure.adresse_lng:
            # ✅ Météo cachée (10 min)
            meteo_data = get_meteo_for_figure(parcelle.figure)

            if meteo_data:
                temperature = meteo_data['temperature']
                conditions = meteo_data['conditions']
                precipitation = meteo_data.get('rain', 0)
                wind_speed = meteo_data['wind_speed']
                humidity = meteo_data['humidity']

                logger.debug(f"🌤️ {parcelle.nom}: {temperature}°C, {conditions}")


                # ✅ Récupérer les cultures de la parcelle
                cultures = []
                if parcelle.figure and parcelle.figure.crops:
                    for crop in parcelle.figure.crops:
                        if 'name' in crop:
                            cultures.append(crop['name'])

                # ✅ Si pas de cultures, ajouter une culture par défaut pour tester
                if not cultures:
                    cultures = ['Tomate'] # Culture de test

                # ✅ Détection des alertes avec seuils par défaut
                for culture_nom in cultures:
                    culture = Culture.objects.filter(nom__icontains=culture_nom).first()

                    # 🔥 Récupérer les seuils (avec valeurs par défaut)
                    gel_seuil = culture.temperature_mingel if culture and culture.temperature_mingel is not None else SEUILS_DEFAUT['gel']
                    canicule_seuil = culture.temperature_max_canicule if culture and culture.temperature_max_canicule is not None else SEUILS_DEFAUT['canicule']
                    pluie_seuil = culture.precipitation_max if culture and culture.precipitation_max is not None else SEUILS_DEFAUT['pluie']
                    vent_seuil = culture.vent_max if culture and culture.vent_max is not None else SEUILS_DEFAUT['vent']

                    logger.debug(f" 📊 {culture_nom}: gel={gel_seuil}°C, canicule={canicule_seuil}°C")


                    # 🔥 Détection GEL
                    if temperature <= gel_seuil:
                        alertes_parcelle.append({
                            'type': 'gel',
                            'culture': culture_nom,
                            'message': f"❄️ Alerte gel ! {culture_nom} ({temperature}°C, seuil: {gel_seuil}°C)"
                        })
                        logger.debug(f" ❄️ ALERTE GEL pour {culture_nom} ({temperature}°C <= {gel_seuil}°C)")


                    # 🔥 Détection CANICULE
                    if temperature >= canicule_seuil:
                        alertes_parcelle.append({
                            'type': 'canicule',
                            'culture': culture_nom,
                            'message': f"🌡️ Alerte canicule ! {culture_nom} ({temperature}°C, seuil: {canicule_seuil}°C)"
                        })
                        logger.debug(f" 🌡️ ALERTE CANICULE pour {culture_nom} ({temperature}°C >= {canicule_seuil}°C)")


                    # 🔥 Détection PLUIE
                    if precipitation >= pluie_seuil:
                        alertes_parcelle.append({
                            'type': 'pluie',
                            'culture': culture_nom,
                            'message': f"🌧️ Alerte forte pluie ! {culture_nom} ({precipitation}mm, seuil: {pluie_seuil}mm)"
                        })
                        logger.debug(f" 🌧️ ALERTE PLUIE pour {culture_nom}")


                    # 🔥 Détection VENT
                    if wind_speed >= vent_seuil:
                        alertes_parcelle.append({
                            'type': 'vent',
                            'culture': culture_nom,
                            'message': f"💨 Alerte vent fort ! {culture_nom} ({wind_speed}km/h, seuil: {vent_seuil}km/h)"
                        })
                        logger.debug(f" 💨 ALERTE VENT pour {culture_nom}")


                    # 🔥 Détection HUMIDITÉ ÉLEVÉE (risque mildiou)
                    if humidity > 85:
                        alertes_parcelle.append({
                            'type': 'humidite',
                            'culture': culture_nom,
                            'message': f"💧 Alerte humidité élevée ! {culture_nom} ({humidity}%, risque de mildiou)"
                        })
                        logger.debug(f" 💧 ALERTE HUMIDITÉ pour {culture_nom} ({humidity}%)")


                # ✅ Sauvegarder les alertes en base
                aujourdhui = date.today()
                for alerte in alertes_parcelle:
                    alerte_existante = AlerteMeteo.objects.filter(
                        utilisateur=user,
                        figure=parcelle.figure,
                        type_alerte=alerte['type'],
                        date_declenchement__date=aujourdhui
                    ).exists()

                    if not alerte_existante:
                        AlerteMeteo.objects.create(
                            utilisateur=user,
                            figure=parcelle.figure,
                            type_alerte=alerte['type'],
                            message=alerte['message'],
                            temperature=temperature,
                            date_declenchement=timezone.now(),
                            statut='en_attente'
                        )
                        logger.info(f" ✅ Alerte sauvegardée en base")


        parcelles_meteo.append({
            'parcelle': parcelle,
            'meteo': meteo_data,
            'alertes': alertes_parcelle,
            'has_coords': parcelle.figure and parcelle.figure.adresse_lat and parcelle.figure.adresse_lng,
        })

        alertes_globales.extend(alertes_parcelle)

    # Alertes récentes
    date_limite = date.today() - timedelta(days=7)
    alertes_recentes = AlerteMeteo.objects.filter(
        utilisateur=user,
        date_declenchement__date__gte=date_limite
    ).order_by('-date_declenchement')[:20]

    stats = {
        'total_parcelles': parcelles.count(),
        'parcelles_avec_meteo': sum(1 for p in parcelles_meteo if p['meteo'] is not None),
        'alertes_actives': len(alertes_globales),
        'gel': sum(1 for a in alertes_globales if a['type'] == 'gel'),
        'canicule': sum(1 for a in alertes_globales if a['type'] == 'canicule'),
        'pluie': sum(1 for a in alertes_globales if a['type'] == 'pluie'),
        'vent': sum(1 for a in alertes_globales if a['type'] == 'vent'),
        'humidity': sum(1 for a in alertes_globales if a['type'] == 'humidite'),
    }

    return render(request, 'vegetables_fruits/alertes_meteo_avancees.html', {
        'parcelles_meteo': parcelles_meteo,
        'alertes_globales': alertes_globales,
        'alertes_recentes': alertes_recentes,
        'stats': stats,
        'user_has_parcelles': parcelles.exists(),
        'now': timezone.now(),
    })

# ============================================
# FONCTION UTILITAIRE : CLIMAT MONDIAL
# ============================================

def get_climat_mondial(lat, lng):
    """
    Détermine le type de climat en fonction des coordonnées.
    Retourne : 'arctique', 'subpolaire', 'desertique', 'tropical', 'mediterraneen',
               'montagnard', 'continental', 'subtropical', 'tempere'
    """
    # 1. Zones arctiques / polaires
    if abs(lat) > 66.5:
        return 'arctique'
    if abs(lat) > 60:
        return 'subpolaire'

    # 2. Zones désertiques (approximation)
    desert_zones = [
        (-30, -10, 15, 35),  # Sahara
        (20, 40, -10, 30),  # Moyen-Orient
        (-40, -20, 140, 155),  # Australie
        (30, 45, -125, -110),  # Amérique du Nord (sud-ouest)
        (-30, -15, -70, -55),  # Amérique du Sud (Atacama)
    ]
    for lat_min, lat_max, lng_min, lng_max in desert_zones:
        if lat_min <= lat <= lat_max and lng_min <= lng <= lng_max:
            return 'desertique'

    # 3. Zones tropicales (entre -23.5° et 23.5°)
    if -23.5 <= lat <= 23.5:
        return 'tropical'

    # 4. Zones méditerranéennes (approximation)
    mediterranean_zones = [
        (30, 45, -10, 40),  # Bassin méditerranéen
        (30, 40, -125, -115),  # Californie
        (30, 40, 115, 125),  # Chine du sud
        (-40, -30, 145, 155),  # Australie du sud
    ]
    for lat_min, lat_max, lng_min, lng_max in mediterranean_zones:
        if lat_min <= lat <= lat_max and lng_min <= lng <= lng_max:
            return 'mediterraneen'

    # 5. Zones montagnardes (altitude > 1500m approximée par latitude)
    if abs(lat) > 45 and abs(lat) < 60:
        return 'montagnard'

    # 6. Zones continentales (au-delà de 40°)
    if abs(lat) > 40:
        return 'continental'

    # 7. Zones subtropicales (23.5° à 30°)
    if 23.5 <= abs(lat) <= 30:
        return 'subtropical'

    # 8. Par défaut : tempéré
    return 'tempere'


from difflib import get_close_matches
import requests
from django.core.cache import cache
from django.conf import settings


def get_conseils_personnalises(user, figure):
    """
    Retourne des conseils personnalisés pour une parcelle
    Version mondiale avec fallback intelligent, météo réelle et cache
    """
    # 🔥 CACHE GLOBAL - Valable 1 heure
    cache_key_global = f"conseils_complets_{user.id}_{figure.id}"
    conseils_caches = cache.get(cache_key_global)

    if conseils_caches:
        logger.debug(f"📦 Cache hit pour les conseils de {figure.name}")

        return conseils_caches

    logger.debug(f"🔄 Génération des conseils pour {figure.name}...")


    conseils = {
        'arrosage': [],
        'fertilisation': [],
        'protection': [],
        'plantation': [],
        'climat_info': '',
        'alertes_meteo': [],
        'conseils_par_culture': [],
        'exposition': {},
        'meteo_actuelle': None,
        'saison': '',
        'region': '',
    }

    # 1️⃣ Récupérer la région et la saison
    region_info = get_region_utilisateur(user, figure)
    pays = region_info.get('pays', 'France')
    region = region_info.get('region', 'iledefrance')
    saison = region_info.get('saison', 'printemps')
    conseils['saison'] = saison
    conseils['region'] = region

    # 2️⃣ Récupérer le climat
    climat = 'tempere'
    if figure and figure.adresse_lat and figure.adresse_lng:
        climat = get_climat_mondial(figure.adresse_lat, figure.adresse_lng)

    # 3️⃣ Récupérer la météo RÉELLE (avec cache séparé)
    meteo = None
    if figure and figure.adresse_lat and figure.adresse_lng:
        cache_key_meteo = f"meteo_conseils_{figure.id}_{figure.adresse_lat}_{figure.adresse_lng}"
        meteo = cache.get(cache_key_meteo)

        if not meteo:
            try:
                api_key = settings.OPENWEATHER_API_KEY
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={figure.adresse_lat}&lon={figure.adresse_lng}&units=metric&lang=fr&appid={api_key}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    meteo = {
                        'temperature': round(data['main']['temp'], 1),
                        'conditions': data['weather'][0]['description'],
                        'icon': data['weather'][0]['icon'],
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed'],
                        'rain': data.get('rain', {}).get('1h', 0),
                        'feels_like': round(data['main']['feels_like'], 1),
                    }
                    cache.set(cache_key_meteo, meteo, 600)  # 10 minutes
                    logger.info(f"🌤️ Météo récupérée pour {figure.name}: {meteo['temperature']}°C")

                else:
                    logger.error(f"❌ Erreur météo: {response.status_code}")

            except Exception as e:
                logger.error(f"❌ Erreur météo: {e}")


    conseils['meteo_actuelle'] = meteo

    # 4️⃣ Alertes météo (si météo disponible)
    if meteo:
        if meteo['temperature'] > 35:
            conseils['alertes_meteo'].append({
                'type': 'canicule',
                'emoji': '🔥',
                'message': f"Canicule ! {meteo['temperature']}°C - Arrosez ce soir"
            })
        if meteo['temperature'] < 0:
            conseils['alertes_meteo'].append({
                'type': 'gel',
                'emoji': '❄️',
                'message': f"Gel ! {meteo['temperature']}°C - Protégez vos plantes"
            })
        if meteo['wind_speed'] > 50:
            conseils['alertes_meteo'].append({
                'type': 'vent',
                'emoji': '💨',
                'message': f"Vent fort ! {meteo['wind_speed']}km/h - Protégez les cultures"
            })
        if meteo['rain'] > 20:
            conseils['alertes_meteo'].append({
                'type': 'pluie',
                'emoji': '🌧️',
                'message': f"Fortes pluies ! {meteo['rain']}mm - Surveillez le drainage"
            })
        if meteo['humidity'] > 85:
            conseils['alertes_meteo'].append({
                'type': 'humidite',
                'emoji': '💧',
                'message': f"Humidité élevée ! {meteo['humidity']}% - Risque de mildiou"
            })

    # 5️⃣ Informations climatiques
    climats_fr = {
        'mediterraneen': '🌞 Climat méditerranéen (été chaud et sec, hiver doux)',
        'continental': '❄️ Climat continental (hiver froid, été chaud)',
        'oceanique': '🌊 Climat océanique (hiver doux, été frais)',
        'montagnard': '🏔️ Climat montagnard (hiver froid, été frais)',
        'tropical': '🌴 Climat tropical (chaud et humide toute l\'année)',
        'desertique': '🏜️ Climat désertique (très sec, grandes amplitudes)',
        'arctique': '❄️ Climat arctique (très froid)',
        'subpolaire': '🌨️ Climat subpolaire (hiver long et froid)',
        'subtropical': '🌺 Climat subtropical (chaud, humide en été)',
        'tempere': '🌿 Climat tempéré (4 saisons bien marquées)',
    }
    conseils['climat_info'] = climats_fr.get(climat, '🌿 Climat tempéré')

    # 6️⃣ Conseils de base par climat (simplifiés ici, garde ton code existant)
    conseils_climat = {
        'mediterraneen': {
            'arrosage': ["Arrosez le matin pour limiter l'évaporation.",
                         "Installez un goutte-à-goutte pour économiser l'eau."],
            'protection': ["Protégez les jeunes plants du soleil avec un voile d'ombrage."],
            'plantation': ["Plantez des cultures adaptées à la sécheresse (olivier, lavande, romarin)."],
            'fertilisation': ["Apportez du compost en automne."]
        },
        'continental': {
            'protection': ["Attention aux gelées tardives (avril-mai)."],
            'plantation': ["Plantez après les dernières gelées (mi-mai)."],
            'fertilisation': ["Apportez du compost en automne pour préparer le sol."],
            'arrosage': ["Arrosez modérément."]
        },
        'oceanique': {
            'arrosage': ["Arrosez moins fréquemment, l'humidité naturelle est suffisante."],
            'protection': ["Protégez du vent dominant."],
            'plantation': ["Plantez des cultures qui aiment l'humidité."],
            'fertilisation': ["Apportez du compost au printemps."]
        },
        'tropical': {
            'arrosage': ["Arrosez abondamment mais espacez les arrosages.",
                         "Arrosez tôt le matin pour éviter les maladies."],
            'protection': ["Paillez épais pour garder l'humidité.", "Protégez du soleil intense."],
            'fertilisation': ["Apportez de la matière organique régulièrement."],
            'plantation': ["Plantez en saison des pluies."]
        },
        'desertique': {
            'arrosage': ["Arrosez fréquemment en petites quantités.",
                         "Utilisez un système d'irrigation goutte-à-goutte."],
            'protection': ["Paillez pour protéger du soleil et garder l'humidité."],
            'plantation': ["Plantez des cultures adaptées aux climats secs.", "Plantez en cuvette pour retenir l'eau."],
            'fertilisation': ["Utilisez un engrais soluble dans l'eau d'arrosage."]
        },
        'arctique': {
            'protection': ["Protégez les plantes du gel avec un voile d'hivernage."],
            'plantation': ["Plantez en serre ou sous châssis.", "Choisissez des variétés à cycle court."],
            'fertilisation': ["Apportez du compost pour enrichir le sol."],
            'arrosage': ["Arrosez modérément."]
        },
        'subpolaire': {
            'protection': ["Protégez les plantes du gel avec un voile d'hivernage."],
            'plantation': ["Plantez en serre ou sous châssis.", "Choisissez des variétés à cycle court."],
            'fertilisation': ["Apportez du compost pour enrichir le sol."],
            'arrosage': ["Arrosez modérément."]
        },
        'montagnard': {
            'protection': ["Protégez du vent et du gel."],
            'plantation': ["Plantez des variétés résistantes au froid."],
            'fertilisation': ["Apportez du compost pour améliorer le sol."],
            'arrosage': ["Arrosez modérément."]
        },
        'subtropical': {
            'arrosage': ["Arrosez régulièrement en été."],
            'protection': ["Protégez du soleil intense en été."],
            'plantation': ["Plantez des cultures adaptées aux étés chauds et humides."],
            'fertilisation': ["Apportez du compost en automne."]
        },
        'tempere': {
            'arrosage': ["Arrosez régulièrement sans excès."],
            'protection': ["Paillez pour protéger le sol."],
            'plantation': ["Plantez après les dernières gelées."],
            'fertilisation': ["Apportez du compost au printemps et en automne."]
        }
    }

    for key in ['arrosage', 'fertilisation', 'protection', 'plantation']:
        if climat in conseils_climat and key in conseils_climat[climat]:
            conseils[key].extend(conseils_climat[climat][key])

    # 7️⃣ Conseils par saison
    conseils_saison = {
        'printemps': {
            'plantation': ["C'est la saison des semis ! Tomates, courgettes, haricots."],
            'fertilisation': ["Apportez un engrais riche en azote pour le démarrage."],
            'arrosage': ["Arrosez modérément, la terre est encore humide."],
            'protection': ["Surveillez les gelées tardives."]
        },
        'ete': {
            'arrosage': ["Arrosez tôt le matin ou tard le soir.",
                         "Évitez d'arroser les feuilles pour prévenir les maladies."],
            'protection': ["Installez un ombrage pour les cultures sensibles."],
            'fertilisation': ["Apportez un engrais riche en potassium pour la floraison."],
            'plantation': ["Plantez des cultures résistantes à la chaleur."]
        },
        'automne': {
            'plantation': ["Plantez les bulbes de printemps (ail, oignon).",
                           "Plantez les choux et les légumes d'hiver."],
            'fertilisation': ["Apportez du compost pour préparer le sol."],
            'protection': ["Paillez pour protéger du froid hivernal."],
            'arrosage': ["Arrosez moins fréquemment."]
        },
        'hiver': {
            'protection': ["Protégez les plantes sensibles au gel.", "Paillez les pieds des plantes."],
            'plantation': ["Plantez des engrais verts pour enrichir le sol."],
            'fertilisation': ["Apportez du compost en surface."],
            'arrosage': ["Arrosez très modérément."]
        }
    }

    for key in ['arrosage', 'fertilisation', 'protection', 'plantation']:
        if saison in conseils_saison and key in conseils_saison[saison]:
            conseils[key].extend(conseils_saison[saison][key])

    # 8️⃣ Ajustements météo (si disponible)
    if meteo:
        if meteo['temperature'] > 35:
            conseils['arrosage'].append("🔥 Canicule ! Arrosez abondamment ce soir")
            conseils['protection'].append("☀️ Installez un voile d'ombrage")
        if meteo['temperature'] < 0:
            conseils['protection'].append("❄️ Gel ! Protégez vos plantes avec un voile d'hivernage")
        if meteo['humidity'] > 85:
            conseils['protection'].append("⚠️ Humidité élevée - Surveillez le mildiou")
        if meteo['wind_speed'] > 50:
            conseils['protection'].append("💨 Vent fort - Protégez les cultures sensibles")

    # 9️⃣ Récupérer les cultures de la figure
    cultures_list = []
    if figure and figure.crops:
        for crop in figure.crops:
            if 'name' in crop:
                cultures_list.append(crop['name'])

    # 9️⃣ DICTIONNAIRE DES CONSEILS PAR CULTURE (75+ cultures)
    conseils_cultures = {
        # ==================== LÉGUMES ====================
        'tomate': {
            'emoji': '🍅',
            'type': 'Légume-fruit',
            'hauteur': '50-150 cm',
            'largeur': '40-80 cm',
            'espacement': '50-60 cm',
            'espacement_rangs': '80-100 cm',
            'arrosage': [
                "Arrosez régulièrement mais sans excès pour éviter le pourrissement.",
                "Arrosez au pied, évitez de mouiller les feuilles (risque de mildiou).",
                "En période de forte chaleur, arrosez tous les 2-3 jours."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Fertilisez avec un engrais riche en potassium pendant la fructification.",
                "Apportez du purin d'ortie une fois par mois."
            ],
            'plantation': [
                "Plantez en plein soleil (minimum 6h de soleil).",
                "Espacez les plants de 50 cm en tous sens.",
                "Plantez après les dernières gelées (température du sol > 15°C)."
            ],
            'protection': [
                "Tuteurez les plants pour éviter qu'ils ne cassent.",
                "Protégez du mildiou avec de la bouillie bordelaise.",
                "Paillez pour garder l'humidité et éviter les mauvaises herbes."
            ]
        },
        'carotte': {
            'emoji': '🥕',
            'type': 'Légume-racine',
            'hauteur': '30-40 cm (feuillage)',
            'largeur': '10-15 cm',
            'espacement': '3-5 cm',
            'espacement_rangs': '15-20 cm',
            'arrosage': [
                "Arrosez régulièrement pour éviter que les carottes ne deviennent fibreuses.",
                "Arrosez en pluie fine pour ne pas tasser le sol."
            ],
            'fertilisation': [
                "Évitez les engrais trop riches en azote (favorise le feuillage au détriment de la racine).",
                "Apportez du compost bien décomposé avant le semis."
            ],
            'plantation': [
                "Les carottes aiment les sols légers, profonds et bien drainés.",
                "Semez en place (ne repiquez pas).",
                "Éclaircissez à 3-5 cm pour de belles carottes."
            ],
            'protection': [
                "Protégez des mouches de la carotte avec un voile anti-insectes.",
                "Pratiquez la rotation des cultures."
            ]
        },
        'salade': {
            'emoji': '🥬',
            'type': 'Légume-feuille',
            'hauteur': '20-30 cm',
            'largeur': '20-30 cm',
            'espacement': '25-30 cm',
            'espacement_rangs': '30-40 cm',
            'arrosage': [
                "Arrosez régulièrement pour éviter qu'elles ne montent en graines.",
                "Arrosez le matin de préférence."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote pour favoriser la croissance des feuilles."
            ],
            'plantation': [
                "Plantez à mi-ombre en été.",
                "Semez échelonné (tous les 15 jours) pour des récoltes étalées.",
                "Espacez les plants de 25-30 cm."
            ],
            'protection': [
                "Protégez des limaces.",
                "Paillez pour garder la fraîcheur."
            ]
        },
        'courgette': {
            'emoji': '🥒',
            'type': 'Légume-fruit',
            'hauteur': '40-60 cm',
            'largeur': '80-120 cm',
            'espacement': '80-100 cm',
            'espacement_rangs': '100-120 cm',
            'arrosage': [
                "Arrosez au pied, évitez de mouiller les feuilles (risque d'oïdium).",
                "Arrosez abondamment mais espacé."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Fertilisez avec un engrais riche en potassium pendant la fructification."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Espacez les plants de 1 m en tous sens.",
                "Plantez après les dernières gelées."
            ],
            'protection': [
                "Paillez pour garder l'humidité.",
                "Surveillez l'oïdium et traitez si nécessaire."
            ]
        },
        'haricot': {
            'emoji': '🫘',
            'type': 'Légume-graine',
            'hauteur': '40-60 cm (nain) / 200-300 cm (grimpant)',
            'largeur': '30-40 cm',
            'espacement': '5-10 cm (nain) / 15-20 cm (grimpant)',
            'espacement_rangs': '40-50 cm (nain) / 80-100 cm (grimpant)',
            'arrosage': [
                "Arrosez régulièrement en période de floraison et de formation des gousses.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Les haricots fixent l'azote, pas besoin d'engrais riche en azote.",
                "Apportez un peu de compost au moment du semis."
            ],
            'plantation': [
                "Semez quand le sol est chaud (température > 15°C).",
                "Ne faites pas tremper les graines avant le semis.",
                "Semez en poquets de 3-4 graines."
            ],
            'protection': [
                "Paillez pour garder l'humidité.",
                "Surveillez les pucerons."
            ]
        },
        'pomme de terre': {
            'emoji': '🥔',
            'type': 'Légume-tubercule',
            'hauteur': '40-60 cm',
            'largeur': '30-50 cm',
            'espacement': '30-40 cm',
            'espacement_rangs': '60-80 cm',
            'arrosage': [
                "Arrosez régulièrement en période de tuberisation.",
                "Évitez l'excès d'eau qui favorise le mildiou."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Évitez les engrais trop riches en azote."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Buttez les plants pour favoriser la croissance des tubercules.",
                "Plantez quand le sol est réchauffé (> 10°C)."
            ],
            'protection': [
                "Protégez du mildiou avec de la bouillie bordelaise.",
                "Surveillez le doryphore."
            ]
        },
        'aubergine': {
            'emoji': '🍆',
            'type': 'Légume-fruit',
            'hauteur': '60-100 cm',
            'largeur': '50-70 cm',
            'espacement': '50-60 cm',
            'espacement_rangs': '80-100 cm',
            'arrosage': [
                "Arrosez régulièrement sans excès.",
                "Arrosez au pied, matin ou soir."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol chaud et bien drainé.",
                "Plantez après les dernières gelées."
            ],
            'protection': [
                "Protégez du vent.",
                "Paillez pour garder l'humidité."
            ]
        },
        'poivron': {
            'emoji': '🫑',
            'type': 'Légume-fruit',
            'hauteur': '50-80 cm',
            'largeur': '40-60 cm',
            'espacement': '40-50 cm',
            'espacement_rangs': '60-80 cm',
            'arrosage': [
                "Arrosez régulièrement sans excès.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost avant la plantation."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol chaud, protégez du vent.",
                "Espacez les plants de 40-50 cm."
            ],
            'protection': [
                "Protégez du vent.",
                "Paillez pour garder l'humidité."
            ]
        },
        'concombre': {
            'emoji': '🥒',
            'type': 'Légume-fruit',
            'hauteur': '30-40 cm (rampant)',
            'largeur': '100-150 cm (rampant)',
            'espacement': '30-40 cm',
            'espacement_rangs': '80-100 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied pour éviter les maladies."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Tuteurez pour un gain de place.",
                "Sol riche et bien drainé."
            ],
            'protection': [
                "Protégez de l'oïdium.",
                "Paillez pour garder l'humidité."
            ]
        },
        'oignon': {
            'emoji': '🧅',
            'type': 'Légume-bulbe',
            'hauteur': '30-50 cm (feuillage)',
            'largeur': '10-15 cm (bulbe)',
            'espacement': '10-15 cm',
            'espacement_rangs': '20-30 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrêtez l'arrosage quand les feuilles commencent à jaunir."
            ],
            'fertilisation': [
                "Évitez les engrais trop riches en azote.",
                "Apportez du compost avant la plantation."
            ],
            'plantation': [
                "Plantez en sol léger et bien drainé.",
                "Plantez en plein soleil.",
                "Espacez les bulbes de 10 cm."
            ],
            'protection': [
                "Surveillez le mildiou.",
                "Paillez pour garder l'humidité."
            ]
        },
        'ail': {
            'emoji': '🧄',
            'type': 'Légume-bulbe',
            'hauteur': '30-60 cm',
            'largeur': '10-15 cm',
            'espacement': '10-15 cm',
            'espacement_rangs': '20-30 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrêtez l'arrosage quand les feuilles jaunissent."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation."
            ],
            'plantation': [
                "Plantez en automne ou au printemps selon le climat.",
                "Sol léger et bien drainé.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Surveillez le mildiou.",
                "Paillez pour protéger du froid."
            ]
        },
        'chou': {
            'emoji': '🥬',
            'type': 'Légume-feuille',
            'hauteur': '30-50 cm',
            'largeur': '40-60 cm',
            'espacement': '50-60 cm',
            'espacement_rangs': '60-80 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote.",
                "Compost avant la plantation."
            ],
            'plantation': [
                "Plantez en plein soleil ou mi-ombre.",
                "Sol riche et frais.",
                "Espacez les plants de 50 cm."
            ],
            'protection': [
                "Protégez des chenilles avec un voile.",
                "Paillez pour garder la fraîcheur."
            ]
        },
        'brocoli': {
            'emoji': '🥦',
            'type': 'Légume-fleur',
            'hauteur': '40-70 cm',
            'largeur': '40-60 cm',
            'espacement': '50-60 cm',
            'espacement_rangs': '60-80 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote.",
                "Compost avant la plantation."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol riche et frais.",
                "Espacez les plants de 50 cm."
            ],
            'protection': [
                "Protégez des chenilles.",
                "Paillez pour garder la fraîcheur."
            ]
        },
        'épinard': {
            'emoji': '🥬',
            'type': 'Légume-feuille',
            'hauteur': '15-30 cm',
            'largeur': '15-20 cm',
            'espacement': '5-10 cm',
            'espacement_rangs': '20-30 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote."
            ],
            'plantation': [
                "Plantez à mi-ombre en été.",
                "Sol frais et riche.",
                "Semez en place."
            ],
            'protection': [
                "Protégez des limaces.",
                "Paillez pour garder la fraîcheur."
            ]
        },
        'betterave': {
            'emoji': '🌿',
            'type': 'Légume-racine',
            'hauteur': '30-40 cm (feuillage)',
            'largeur': '10-15 cm (racine)',
            'espacement': '10-15 cm',
            'espacement_rangs': '20-30 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez en pluie fine."
            ],
            'fertilisation': [
                "Apportez du compost avant le semis.",
                "Évitez les engrais trop riches en azote."
            ],
            'plantation': [
                "Sol léger et bien drainé.",
                "Semez en place.",
                "Éclaircissez à 10 cm."
            ],
            'protection': [
                "Paillez pour garder l'humidité."
            ]
        },
        'radis': {
            'emoji': '🌿',
            'type': 'Légume-racine',
            'hauteur': '15-20 cm (feuillage)',
            'largeur': '3-5 cm (radis)',
            'espacement': '2-3 cm',
            'espacement_rangs': '10-15 cm',
            'arrosage': [
                "Arrosez régulièrement pour éviter que les radis ne deviennent piquants.",
                "Arrosez en pluie fine."
            ],
            'fertilisation': [
                "Sol frais et riche."
            ],
            'plantation': [
                "Semez en place.",
                "Semez échelonné pour des récoltes étalées.",
                "Sol léger."
            ],
            'protection': [
                "Protégez des altises."
            ]
        },
        'poireau': {
            'emoji': '🌿',
            'type': 'Légume-bulbe',
            'hauteur': '40-60 cm',
            'largeur': '3-5 cm',
            'espacement': '15-20 cm',
            'espacement_rangs': '30-40 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Fertilisez avec un engrais riche en azote."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol riche et bien drainé.",
                "Espacez les plants de 15 cm."
            ],
            'protection': [
                "Paillez pour garder l'humidité."
            ]
        },
        'céleri': {
            'emoji': '🌿',
            'type': 'Légume-tige',
            'hauteur': '40-60 cm',
            'largeur': '30-40 cm',
            'espacement': '30-40 cm',
            'espacement_rangs': '40-50 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Fertilisez avec un engrais riche en azote."
            ],
            'plantation': [
                "Plantez en plein soleil ou mi-ombre.",
                "Sol riche et frais.",
                "Espacez les plants de 30 cm."
            ],
            'protection': [
                "Paillez pour garder la fraîcheur."
            ]
        },
        'artichaut': {
            'emoji': '🌿',
            'type': 'Légume-fleur',
            'hauteur': '100-150 cm',
            'largeur': '80-120 cm',
            'espacement': '80-100 cm',
            'espacement_rangs': '100-120 cm',
            'arrosage': [
                "Arrosez régulièrement."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol riche et bien drainé.",
                "Espacez les plants de 1 m."
            ],
            'protection': [
                "Paillez pour garder l'humidité."
            ]
        },
        'asperge': {
            'emoji': '🌿',
            'type': 'Légume-tige',
            'hauteur': '100-150 cm (feuillage)',
            'largeur': '40-60 cm',
            'espacement': '40-50 cm',
            'espacement_rangs': '100-120 cm',
            'arrosage': [
                "Arrosez régulièrement en période de croissance."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Sol léger et bien drainé.",
                "Plantez en plein soleil.",
                "Plantez les griffes à 15 cm de profondeur."
            ],
            'protection': [
                "Paillez pour protéger du froid."
            ]
        },
        'potiron': {
            'emoji': '🎃',
            'type': 'Légume-fruit',
            'hauteur': '40-60 cm',
            'largeur': '200-500 cm (rampant)',
            'espacement': '100-150 cm',
            'espacement_rangs': '200-300 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol riche et bien drainé.",
                "Laissez beaucoup d'espace pour les tiges rampantes."
            ],
            'protection': [
                "Paillez pour garder l'humidité.",
                "Protégez de l'oïdium."
            ]
        },
        'citrouille': {
            'emoji': '🎃',
            'type': 'Légume-fruit',
            'hauteur': '40-60 cm',
            'largeur': '200-500 cm (rampant)',
            'espacement': '100-150 cm',
            'espacement_rangs': '200-300 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol riche et bien drainé.",
                "Laissez beaucoup d'espace pour les tiges rampantes."
            ],
            'protection': [
                "Paillez pour garder l'humidité.",
                "Protégez de l'oïdium."
            ]
        },
        'melon': {
            'emoji': '🍈',
            'type': 'Légume-fruit',
            'hauteur': '40-60 cm',
            'largeur': '100-200 cm (rampant)',
            'espacement': '80-100 cm',
            'espacement_rangs': '150-200 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol chaud et bien drainé.",
                "Laissez de l'espace pour les tiges."
            ],
            'protection': [
                "Paillez pour garder l'humidité.",
                "Protégez de l'oïdium."
            ]
        },
        'pastèque': {
            'emoji': '🍉',
            'type': 'Légume-fruit',
            'hauteur': '40-60 cm',
            'largeur': '200-400 cm (rampant)',
            'espacement': '100-150 cm',
            'espacement_rangs': '200-300 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol chaud et bien drainé.",
                "Laissez beaucoup d'espace."
            ],
            'protection': [
                "Paillez pour garder l'humidité.",
                "Protégez de l'oïdium."
            ]
        },
        'piment': {
            'emoji': '🌶️',
            'type': 'Légume-fruit',
            'hauteur': '40-80 cm',
            'largeur': '30-50 cm',
            'espacement': '40-50 cm',
            'espacement_rangs': '60-80 cm',
            'arrosage': [
                "Arrosez régulièrement sans excès.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost avant la plantation."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol chaud et bien drainé.",
                "Plantez après les dernières gelées."
            ],
            'protection': [
                "Protégez du vent.",
                "Paillez pour garder l'humidité."
            ]
        },
        'topinambour': {
            'emoji': '🌿',
            'type': 'Légume-racine',
            'hauteur': '150-250 cm',
            'largeur': '50-80 cm',
            'espacement': '40-50 cm',
            'espacement_rangs': '80-100 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost avant la plantation."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Attention : peut devenir envahissant."
            ],
            'protection': [
                "Paillez pour garder l'humidité."
            ]
        },
        'panais': {
            'emoji': '🌿',
            'type': 'Légume-racine',
            'hauteur': '30-40 cm (feuillage)',
            'largeur': '10-15 cm (racine)',
            'espacement': '10-15 cm',
            'espacement_rangs': '20-30 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez en pluie fine."
            ],
            'fertilisation': [
                "Apportez du compost avant le semis.",
                "Évitez les engrais trop riches en azote."
            ],
            'plantation': [
                "Sol léger et bien drainé.",
                "Semez en place.",
                "Éclaircissez à 10-15 cm."
            ],
            'protection': [
                "Paillez pour garder l'humidité."
            ]
        },
        'salsifis': {
            'emoji': '🌿',
            'type': 'Légume-racine',
            'hauteur': '30-40 cm (feuillage)',
            'largeur': '5-8 cm (racine)',
            'espacement': '10-15 cm',
            'espacement_rangs': '20-30 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez en pluie fine."
            ],
            'fertilisation': [
                "Apportez du compost avant le semis."
            ],
            'plantation': [
                "Sol léger et bien drainé.",
                "Semez en place.",
                "Éclaircissez à 10-15 cm."
            ],
            'protection': [
                "Paillez pour garder l'humidité."
            ]
        },
        'chou-fleur': {
            'emoji': '🥦',
            'type': 'Légume-fleur',
            'hauteur': '40-60 cm',
            'largeur': '40-60 cm',
            'espacement': '50-60 cm',
            'espacement_rangs': '60-80 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote.",
                "Compost avant la plantation."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol riche et frais.",
                "Espacez les plants de 50 cm."
            ],
            'protection': [
                "Protégez des chenilles.",
                "Paillez pour garder la fraîcheur."
            ]
        },
        'chou-rave': {
            'emoji': '🌿',
            'type': 'Légume-tige',
            'hauteur': '30-40 cm',
            'largeur': '20-30 cm',
            'espacement': '30-40 cm',
            'espacement_rangs': '40-50 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote.",
                "Compost avant la plantation."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol riche et frais.",
                "Espacez les plants de 30 cm."
            ],
            'protection': [
                "Protégez des chenilles.",
                "Paillez pour garder la fraîcheur."
            ]
        },
        'navet': {
            'emoji': '🌿',
            'type': 'Légume-racine',
            'hauteur': '20-30 cm (feuillage)',
            'largeur': '5-10 cm (racine)',
            'espacement': '10-15 cm',
            'espacement_rangs': '20-30 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez en pluie fine."
            ],
            'fertilisation': [
                "Apportez du compost avant le semis.",
                "Évitez les engrais trop riches en azote."
            ],
            'plantation': [
                "Sol léger et bien drainé.",
                "Semez en place.",
                "Éclaircissez à 10-15 cm."
            ],
            'protection': [
                "Paillez pour garder l'humidité.",
                "Protégez des altises."
            ]
        },
        'rutabaga': {
            'emoji': '🌿',
            'type': 'Légume-racine',
            'hauteur': '30-40 cm (feuillage)',
            'largeur': '10-15 cm (racine)',
            'espacement': '15-20 cm',
            'espacement_rangs': '30-40 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez en pluie fine."
            ],
            'fertilisation': [
                "Apportez du compost avant le semis.",
                "Évitez les engrais trop riches en azote."
            ],
            'plantation': [
                "Sol léger et bien drainé.",
                "Semez en place.",
                "Éclaircissez à 15-20 cm."
            ],
            'protection': [
                "Paillez pour garder l'humidité."
            ]
        },

        # ==================== FRUITS ====================
        'fraise': {
            'emoji': '🍓',
            'type': 'Fruit',
            'hauteur': '15-30 cm',
            'largeur': '30-50 cm',
            'espacement': '30-40 cm',
            'espacement_rangs': '40-60 cm',
            'arrosage': [
                "Arrosez régulièrement sans excès.",
                "Arrosez au pied pour éviter de mouiller les fruits."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost avant la plantation."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Espacez les plants de 30 cm."
            ],
            'protection': [
                "Paillez pour protéger les fruits du contact avec le sol.",
                "Protégez des limaces.",
                "Renouvelez les plants tous les 3-4 ans."
            ]
        },
        'pomme': {
            'emoji': '🍎',
            'type': 'Fruit',
            'hauteur': '200-400 cm (selon porte-greffe)',
            'largeur': '200-400 cm (selon porte-greffe)',
            'espacement': '300-500 cm (haute tige) / 150-200 cm (basse tige)',
            'espacement_rangs': '400-600 cm (haute tige) / 200-300 cm (basse tige)',
            'arrosage': [
                "Arrosez en période de sécheresse.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost en automne.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Plantez 2 variétés différentes pour la pollinisation."
            ],
            'protection': [
                "Traitez contre la tavelure.",
                "Protégez du carpocapse.",
                "Taillez en hiver."
            ]
        },
        'poire': {
            'emoji': '🍐',
            'type': 'Fruit',
            'hauteur': '200-400 cm (selon porte-greffe)',
            'largeur': '200-400 cm',
            'espacement': '300-500 cm (haute tige) / 150-200 cm (basse tige)',
            'espacement_rangs': '400-600 cm (haute tige) / 200-300 cm (basse tige)',
            'arrosage': [
                "Arrosez en période de sécheresse.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost en automne.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Plantez plusieurs variétés pour la pollinisation."
            ],
            'protection': [
                "Traitez contre la tavelure.",
                "Protégez du psylle.",
                "Taillez en hiver."
            ]
        },
        'pêche': {
            'emoji': '🍑',
            'type': 'Fruit',
            'hauteur': '200-400 cm',
            'largeur': '200-400 cm',
            'espacement': '300-500 cm',
            'espacement_rangs': '400-600 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost en automne.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Protégez du vent."
            ],
            'protection': [
                "Protégez des gelées de printemps.",
                "Traitez contre la cloque du pêcher.",
                "Taillez en hiver."
            ]
        },
        'abricot': {
            'emoji': '🍑',
            'type': 'Fruit',
            'hauteur': '200-400 cm',
            'largeur': '200-400 cm',
            'espacement': '300-500 cm',
            'espacement_rangs': '400-600 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost en automne.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Protégez du vent."
            ],
            'protection': [
                "Protégez des gelées de printemps.",
                "Taillez en hiver."
            ]
        },
        'cerise': {
            'emoji': '🍒',
            'type': 'Fruit',
            'hauteur': '400-800 cm (haute tige) / 200-300 cm (basse tige)',
            'largeur': '300-600 cm',
            'espacement': '500-800 cm (haute tige) / 150-200 cm (basse tige)',
            'espacement_rangs': '600-900 cm (haute tige) / 200-300 cm (basse tige)',
            'arrosage': [
                "Arrosez en période de sécheresse.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost en automne.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Plantez plusieurs variétés pour la pollinisation."
            ],
            'protection': [
                "Protégez de la mouche de la cerise.",
                "Taillez en hiver."
            ]
        },
        'vigne': {
            'emoji': '🍇',
            'type': 'Fruit',
            'hauteur': '150-300 cm (palissée)',
            'largeur': '100-200 cm',
            'espacement': '100-150 cm',
            'espacement_rangs': '150-250 cm',
            'arrosage': [
                "Arrosez modérément, la vigne résiste à la sécheresse.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Protégez du vent."
            ],
            'protection': [
                "Traitez contre le mildiou et l'oïdium.",
                "Taillez en hiver.",
                "Protégez du gel."
            ]
        },
        'olivier': {
            'emoji': '🫒',
            'type': 'Fruit',
            'hauteur': '300-800 cm',
            'largeur': '300-600 cm',
            'espacement': '500-800 cm',
            'espacement_rangs': '600-900 cm',
            'arrosage': [
                "Arrosez modérément, l'olivier résiste à la sécheresse.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Protégez du vent."
            ],
            'protection': [
                "Protégez du froid en hiver.",
                "Taillez après la récolte."
            ]
        },
        'citronnier': {
            'emoji': '🍋',
            'type': 'Fruit',
            'hauteur': '200-400 cm',
            'largeur': '200-300 cm',
            'espacement': '300-400 cm',
            'espacement_rangs': '400-500 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Climat méditerranéen ou tropical.",
                "Sol bien drainé.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Protégez du froid en hiver.",
                "Protégez des pucerons."
            ]
        },
        'oranger': {
            'emoji': '🍊',
            'type': 'Fruit',
            'hauteur': '300-600 cm',
            'largeur': '300-500 cm',
            'espacement': '400-600 cm',
            'espacement_rangs': '500-700 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Climat méditerranéen ou tropical.",
                "Sol bien drainé.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Protégez du froid en hiver.",
                "Protégez des pucerons."
            ]
        },
        'pamplemousse': {
            'emoji': '🍊',
            'type': 'Fruit',
            'hauteur': '300-600 cm',
            'largeur': '300-500 cm',
            'espacement': '400-600 cm',
            'espacement_rangs': '500-700 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Climat tropical ou subtropical.",
                "Sol bien drainé.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Protégez du froid en hiver."
            ]
        },
        'avocat': {
            'emoji': '🥑',
            'type': 'Fruit',
            'hauteur': '400-1000 cm',
            'largeur': '300-600 cm',
            'espacement': '500-800 cm',
            'espacement_rangs': '600-900 cm',
            'arrosage': [
                "Arrosez régulièrement sans excès.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Climat tropical ou subtropical.",
                "Sol bien drainé.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Protégez du vent.",
                "Protégez du froid."
            ]
        },
        'kiwi': {
            'emoji': '🥝',
            'type': 'Fruit',
            'hauteur': '300-600 cm (palissé)',
            'largeur': '200-400 cm (palissé)',
            'espacement': '300-500 cm',
            'espacement_rangs': '400-600 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Climat tempéré.",
                "Sol bien drainé.",
                "Protégez du vent.",
                "Plantez un mâle pour 4-5 femelles."
            ],
            'protection': [
                "Protégez des gelées de printemps.",
                "Taillez en hiver."
            ]
        },
        'framboise': {
            'emoji': '🫐',
            'type': 'Fruit',
            'hauteur': '150-200 cm',
            'largeur': '50-100 cm',
            'espacement': '50-70 cm',
            'espacement_rangs': '150-200 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost.",
                "Fertilisez avec un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil ou mi-ombre.",
                "Sol frais et bien drainé.",
                "Espacez les plants de 50 cm."
            ],
            'protection': [
                "Tuteurez les plants.",
                "Paillez pour garder l'humidité."
            ]
        },
        'myrtille': {
            'emoji': '🫐',
            'type': 'Fruit',
            'hauteur': '100-200 cm',
            'largeur': '100-150 cm',
            'espacement': '100-150 cm',
            'espacement_rangs': '150-200 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez avec de l'eau non calcaire."
            ],
            'fertilisation': [
                "Apportez un engrais acide.",
                "Compost de feuilles de chêne."
            ],
            'plantation': [
                "Sol acide (pH 4.5-5.5).",
                "Climat tempéré.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Paillez avec des aiguilles de pin.",
                "Protégez des oiseaux."
            ]
        },
        'bananier': {
            'emoji': '🍌',
            'type': 'Fruit',
            'hauteur': '200-800 cm',
            'largeur': '200-400 cm',
            'espacement': '300-500 cm',
            'espacement_rangs': '400-600 cm',
            'arrosage': [
                "Arrosez abondamment.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez beaucoup de matière organique.",
                "Fertilisez régulièrement."
            ],
            'plantation': [
                "Climat tropical.",
                "Sol riche et bien drainé.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Protégez du vent.",
                "Protégez du froid."
            ]
        },
        'manguier': {
            'emoji': '🥭',
            'type': 'Fruit',
            'hauteur': '400-1000 cm',
            'largeur': '300-600 cm',
            'espacement': '500-800 cm',
            'espacement_rangs': '600-900 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Climat tropical.",
                "Sol bien drainé.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Protégez du vent.",
                "Protégez des maladies fongiques."
            ]
        },
        'ananas': {
            'emoji': '🍍',
            'type': 'Fruit',
            'hauteur': '60-100 cm',
            'largeur': '60-100 cm',
            'espacement': '50-70 cm',
            'espacement_rangs': '80-100 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Climat tropical.",
                "Sol bien drainé.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Protégez du froid."
            ]
        },
        'papaye': {
            'emoji': '🥭',
            'type': 'Fruit',
            'hauteur': '300-600 cm',
            'largeur': '200-300 cm',
            'espacement': '300-400 cm',
            'espacement_rangs': '400-500 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Climat tropical.",
                "Sol bien drainé.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Protégez du vent.",
                "Protégez du froid."
            ]
        },
        'fruit de la passion': {
            'emoji': '🌿',
            'type': 'Fruit',
            'hauteur': '300-600 cm (grimpant)',
            'largeur': '200-300 cm',
            'espacement': '200-300 cm',
            'espacement_rangs': '300-400 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Climat tropical ou subtropical.",
                "Sol bien drainé.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Tuteurez la plante.",
                "Protégez du froid."
            ]
        },
        'litchi': {
            'emoji': '🌿',
            'type': 'Fruit',
            'hauteur': '400-800 cm',
            'largeur': '300-500 cm',
            'espacement': '500-700 cm',
            'espacement_rangs': '600-800 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Climat tropical ou subtropical.",
                "Sol bien drainé.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Protégez du vent.",
                "Protégez du froid."
            ]
        },
        'cacao': {
            'emoji': '🍫',
            'type': 'Fruit',
            'hauteur': '400-800 cm',
            'largeur': '300-500 cm',
            'espacement': '300-400 cm',
            'espacement_rangs': '400-500 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez de la matière organique.",
                "Fertilisez régulièrement."
            ],
            'plantation': [
                "Climat tropical humide.",
                "Ombre partielle.",
                "Sol riche."
            ],
            'protection': [
                "Protégez du vent.",
                "Protégez des maladies."
            ]
        },
        'cafeier': {
            'emoji': '☕',
            'type': 'Fruit',
            'hauteur': '200-400 cm',
            'largeur': '200-300 cm',
            'espacement': '200-300 cm',
            'espacement_rangs': '300-400 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez de la matière organique.",
                "Fertilisez régulièrement."
            ],
            'plantation': [
                "Climat tropical.",
                "Ombre partielle.",
                "Sol riche."
            ],
            'protection': [
                "Protégez du vent.",
                "Protégez des maladies."
            ]
        },
        'vanille': {
            'emoji': '🌿',
            'type': 'Fruit',
            'hauteur': '300-600 cm (grimpant)',
            'largeur': '100-200 cm',
            'espacement': '100-150 cm',
            'espacement_rangs': '200-300 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez de la matière organique.",
                "Fertilisez régulièrement."
            ],
            'plantation': [
                "Climat tropical humide.",
                "Ombre partielle.",
                "Sol riche."
            ],
            'protection': [
                "Tuteurez la plante.",
                "Protégez du vent."
            ]
        },
        'gingembre': {
            'emoji': '🫚',
            'type': 'Épice',
            'hauteur': '60-100 cm',
            'largeur': '40-60 cm',
            'espacement': '30-40 cm',
            'espacement_rangs': '50-60 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost.",
                "Fertilisez régulièrement."
            ],
            'plantation': [
                "Climat tropical ou subtropical.",
                "Sol bien drainé.",
                "Ombre partielle."
            ],
            'protection': [
                "Paillez pour garder l'humidité."
            ]
        },
        'curcuma': {
            'emoji': '🧡',
            'type': 'Épice',
            'hauteur': '60-100 cm',
            'largeur': '40-60 cm',
            'espacement': '30-40 cm',
            'espacement_rangs': '50-60 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez du compost.",
                "Fertilisez régulièrement."
            ],
            'plantation': [
                "Climat tropical ou subtropical.",
                "Sol bien drainé.",
                "Ombre partielle."
            ],
            'protection': [
                "Paillez pour garder l'humidité."
            ]
        },
        'cannelle': {
            'emoji': '🌿',
            'type': 'Épice',
            'hauteur': '300-600 cm',
            'largeur': '200-300 cm',
            'espacement': '200-300 cm',
            'espacement_rangs': '300-400 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez de la matière organique.",
                "Fertilisez régulièrement."
            ],
            'plantation': [
                "Climat tropical.",
                "Sol riche.",
                "Ombre partielle."
            ],
            'protection': [
                "Protégez du vent.",
                "Protégez des maladies."
            ]
        },
        'poivre': {
            'emoji': '🌿',
            'type': 'Épice',
            'hauteur': '300-600 cm (grimpant)',
            'largeur': '100-200 cm',
            'espacement': '100-150 cm',
            'espacement_rangs': '200-300 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez de la matière organique.",
                "Fertilisez régulièrement."
            ],
            'plantation': [
                "Climat tropical.",
                "Sol bien drainé.",
                "Ombre partielle."
            ],
            'protection': [
                "Tuteurez la plante.",
                "Protégez du vent."
            ]
        },

        # ==================== CÉRÉALES ====================
        'riz': {
            'emoji': '🍚',
            'type': 'Céréale',
            'hauteur': '80-150 cm',
            'largeur': '30-50 cm',
            'espacement': '15-20 cm',
            'espacement_rangs': '20-30 cm',
            'arrosage': [
                "Maintenez une lame d'eau permanente.",
                "Inondez les rizières pendant la croissance."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote.",
                "Fertilisez en plusieurs fois."
            ],
            'plantation': [
                "Climat tropical ou subtropical.",
                "Sol inondé.",
                "Semez en pépinière puis repiquez."
            ],
            'protection': [
                "Surveillez les maladies fongiques.",
                "Protégez des oiseaux."
            ]
        },
        'maïs': {
            'emoji': '🌽',
            'type': 'Céréale',
            'hauteur': '150-300 cm',
            'largeur': '50-80 cm',
            'espacement': '30-40 cm',
            'espacement_rangs': '70-80 cm',
            'arrosage': [
                "Arrosez régulièrement en période de croissance.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote.",
                "Fertilisez en plusieurs fois."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Plantez en carré pour favoriser la pollinisation."
            ],
            'protection': [
                "Protégez des oiseaux.",
                "Surveillez la pyrale du maïs."
            ]
        },
        'blé': {
            'emoji': '🌾',
            'type': 'Céréale',
            'hauteur': '60-120 cm',
            'largeur': '20-30 cm',
            'espacement': '5-10 cm',
            'espacement_rangs': '15-20 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote au démarrage.",
                "Fertilisez en plusieurs fois."
            ],
            'plantation': [
                "Semez en automne ou au printemps selon le climat.",
                "Sol bien drainé.",
                "Semez en ligne."
            ],
            'protection': [
                "Surveillez les maladies fongiques.",
                "Protégez des oiseaux."
            ]
        },
        'orge': {
            'emoji': '🌾',
            'type': 'Céréale',
            'hauteur': '60-100 cm',
            'largeur': '20-30 cm',
            'espacement': '5-10 cm',
            'espacement_rangs': '15-20 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote au démarrage."
            ],
            'plantation': [
                "Semez en automne ou au printemps.",
                "Sol bien drainé.",
                "Semez en ligne."
            ],
            'protection': [
                "Surveillez les maladies fongiques."
            ]
        },
        'avoine': {
            'emoji': '🌾',
            'type': 'Céréale',
            'hauteur': '80-120 cm',
            'largeur': '20-30 cm',
            'espacement': '5-10 cm',
            'espacement_rangs': '15-20 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote au démarrage."
            ],
            'plantation': [
                "Semez en automne ou au printemps.",
                "Sol bien drainé.",
                "Semez en ligne."
            ],
            'protection': [
                "Surveillez les maladies fongiques."
            ]
        },
        'seigle': {
            'emoji': '🌾',
            'type': 'Céréale',
            'hauteur': '80-150 cm',
            'largeur': '20-30 cm',
            'espacement': '5-10 cm',
            'espacement_rangs': '15-20 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote au démarrage."
            ],
            'plantation': [
                "Semez en automne.",
                "Sol bien drainé.",
                "Semez en ligne."
            ],
            'protection': [
                "Surveillez les maladies fongiques."
            ]
        },
        'millet': {
            'emoji': '🌾',
            'type': 'Céréale',
            'hauteur': '100-200 cm',
            'largeur': '30-50 cm',
            'espacement': '15-20 cm',
            'espacement_rangs': '30-40 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote."
            ],
            'plantation': [
                "Climat tropical ou subtropical.",
                "Sol bien drainé.",
                "Semez en ligne."
            ],
            'protection': [
                "Protégez des oiseaux."
            ]
        },
        'sorgho': {
            'emoji': '🌾',
            'type': 'Céréale',
            'hauteur': '100-300 cm',
            'largeur': '30-50 cm',
            'espacement': '15-20 cm',
            'espacement_rangs': '30-40 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en azote."
            ],
            'plantation': [
                "Climat tropical ou subtropical.",
                "Sol bien drainé.",
                "Semez en ligne."
            ],
            'protection': [
                "Protégez des oiseaux.",
                "Surveillez les maladies fongiques."
            ]
        },

        # ==================== FLEURS POLLINISATRICES ====================
        'lavande': {
            'emoji': '🌸',
            'type': 'Fleur pollinisatrice',
            'hauteur': '30-60 cm',
            'largeur': '30-50 cm',
            'espacement': '30-40 cm',
            'espacement_rangs': '40-50 cm',
            'arrosage': [
                "Arrosez modérément, la lavande résiste à la sécheresse.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Peu d'engrais nécessaire.",
                "Apportez un peu de compost en automne."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Espacez les plants de 30 cm."
            ],
            'protection': [
                "Taillez après la floraison.",
                "Protégez de l'humidité excessive."
            ]
        },
        'romarin': {
            'emoji': '🌿',
            'type': 'Fleur pollinisatrice',
            'hauteur': '50-150 cm',
            'largeur': '50-150 cm',
            'espacement': '50-80 cm',
            'espacement_rangs': '80-100 cm',
            'arrosage': [
                "Arrosez modérément, le romarin résiste à la sécheresse.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Peu d'engrais nécessaire.",
                "Apportez un peu de compost en automne."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Espacez les plants de 50 cm."
            ],
            'protection': [
                "Taillez après la floraison.",
                "Protégez du froid intense."
            ]
        },
        'thym': {
            'emoji': '🌿',
            'type': 'Fleur pollinisatrice',
            'hauteur': '15-30 cm',
            'largeur': '20-40 cm',
            'espacement': '20-30 cm',
            'espacement_rangs': '30-40 cm',
            'arrosage': [
                "Arrosez modérément, le thym résiste à la sécheresse.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Peu d'engrais nécessaire."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Espacez les plants de 30 cm."
            ],
            'protection': [
                "Taillez après la floraison."
            ]
        },
        'sauge': {
            'emoji': '🌿',
            'type': 'Fleur pollinisatrice',
            'hauteur': '30-60 cm',
            'largeur': '30-50 cm',
            'espacement': '30-40 cm',
            'espacement_rangs': '40-50 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Peu d'engrais nécessaire."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Espacez les plants de 40 cm."
            ],
            'protection': [
                "Taillez après la floraison."
            ]
        },
        'tournesol': {
            'emoji': '🌻',
            'type': 'Fleur pollinisatrice',
            'hauteur': '100-300 cm',
            'largeur': '50-80 cm',
            'espacement': '30-40 cm',
            'espacement_rangs': '50-60 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Espacez les plants de 50 cm."
            ],
            'protection': [
                "Protégez des oiseaux.",
                "Tuteurez si nécessaire."
            ]
        },
        'rose': {
            'emoji': '🌹',
            'type': 'Fleur pollinisatrice',
            'hauteur': '50-200 cm',
            'largeur': '50-150 cm',
            'espacement': '50-80 cm',
            'espacement_rangs': '80-100 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied, évitez de mouiller les feuilles."
            ],
            'fertilisation': [
                "Apportez un engrais spécial rosiers.",
                "Compost en automne."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Espacez les plants de 50 cm."
            ],
            'protection': [
                "Taillez en hiver.",
                "Traitez contre les pucerons.",
                "Protégez du froid."
            ]
        },
        'tulipe': {
            'emoji': '🌷',
            'type': 'Fleur pollinisatrice',
            'hauteur': '20-60 cm',
            'largeur': '10-20 cm',
            'espacement': '10-15 cm',
            'espacement_rangs': '15-20 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Plantez en automne.",
                "Sol bien drainé.",
                "Plantez en plein soleil."
            ],
            'protection': [
                "Protégez des rongeurs.",
                "Protégez du froid."
            ]
        },
        'orchidée': {
            'emoji': '🌺',
            'type': 'Fleur pollinisatrice',
            'hauteur': '20-100 cm',
            'largeur': '20-40 cm',
            'espacement': '20-30 cm',
            'espacement_rangs': '30-40 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais spécial orchidées.",
                "Fertilisez régulièrement."
            ],
            'plantation': [
                "Climat tropical ou subtropical.",
                "Ombre partielle.",
                "Écorce de pin ou fibre de coco."
            ],
            'protection': [
                "Protégez du froid.",
                "Évitez l'excès d'eau."
            ]
        },
        'jasmin': {
            'emoji': '🌸',
            'type': 'Fleur pollinisatrice',
            'hauteur': '200-400 cm (grimpant)',
            'largeur': '100-200 cm',
            'espacement': '100-150 cm',
            'espacement_rangs': '150-200 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Climat méditerranéen ou tropical.",
                "Sol bien drainé.",
                "Plantez en plein soleil ou mi-ombre."
            ],
            'protection': [
                "Taillez après la floraison.",
                "Protégez du froid."
            ]
        },
        'hortensia': {
            'emoji': '💐',
            'type': 'Fleur pollinisatrice',
            'hauteur': '100-200 cm',
            'largeur': '100-200 cm',
            'espacement': '100-150 cm',
            'espacement_rangs': '150-200 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais acide.",
                "Compost en automne."
            ],
            'plantation': [
                "Sol acide.",
                "Mi-ombre.",
                "Protégez du vent."
            ],
            'protection': [
                "Protégez du gel.",
                "Taillez après la floraison."
            ]
        },
        'pivoine': {
            'emoji': '🌺',
            'type': 'Fleur pollinisatrice',
            'hauteur': '60-100 cm',
            'largeur': '60-100 cm',
            'espacement': '60-80 cm',
            'espacement_rangs': '80-100 cm',
            'arrosage': [
                "Arrosez régulièrement.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Espacez les plants de 60 cm."
            ],
            'protection': [
                "Protégez du froid.",
                "Taillez après la floraison."
            ]
        },
        'iris': {
            'emoji': '🌸',
            'type': 'Fleur pollinisatrice',
            'hauteur': '30-90 cm',
            'largeur': '20-40 cm',
            'espacement': '20-30 cm',
            'espacement_rangs': '30-40 cm',
            'arrosage': [
                "Arrosez modérément.",
                "Arrosez au pied."
            ],
            'fertilisation': [
                "Apportez un engrais riche en potassium.",
                "Compost en automne."
            ],
            'plantation': [
                "Plantez en plein soleil.",
                "Sol bien drainé.",
                "Plantez en automne ou au printemps."
            ],
            'protection': [
                "Protégez des limaces.",
                "Divisez les touffes tous les 3-4 ans."
            ]
        },
    }

    # 1️⃣1️⃣ CONSTRUCTION DES CONSEILS PAR CULTURE AVEC FALLBACK
    conseils_par_culture = []

    for culture_nom in cultures_list:
        culture_lower = culture_nom.lower()
        culture_conseils = None
        culture_key = None

        # 1. Correspondance exacte
        if culture_lower in conseils_cultures:
            culture_key = culture_lower
            culture_conseils = conseils_cultures[culture_lower]

        # 2. Correspondance partielle
        if not culture_conseils:
            for key, value in conseils_cultures.items():
                if key in culture_lower or culture_lower in key:
                    culture_key = key
                    culture_conseils = value
                    break

        # 3. Correspondance floue
        if not culture_conseils:
            matches = get_close_matches(culture_lower, list(conseils_cultures.keys()), n=1, cutoff=0.6)
            if matches:
                culture_key = matches[0]
                culture_conseils = conseils_cultures[culture_key]

        # 4. FALLBACK INTELLIGENT
        if not culture_conseils:
            culture_conseils = get_fallback_conseils(culture_nom, climat, meteo)

        # 5. Adaptation au climat
        adaptation = get_adaptation_climat(culture_nom, climat)

        culture_data = {
            'nom': culture_nom,
            'emoji': culture_conseils.get('emoji', '🌱'),
            'type': culture_conseils.get('type', 'Culture'),
            'hauteur': culture_conseils.get('hauteur', ''),
            'largeur': culture_conseils.get('largeur', ''),
            'espacement': culture_conseils.get('espacement', ''),
            'espacement_rangs': culture_conseils.get('espacement_rangs', ''),
            'arrosage': culture_conseils.get('arrosage', []),
            'fertilisation': culture_conseils.get('fertilisation', []),
            'plantation': culture_conseils.get('plantation', []),
            'protection': culture_conseils.get('protection', []),
            'adaptation': adaptation,
        }

        if meteo:
            if meteo['temperature'] > 35:
                culture_data['arrosage'].append("🔥 Canicule ! Arrosez abondamment ce soir")
            if meteo['temperature'] < 0:
                culture_data['protection'].append("❄️ Gel ! Protégez vos plantes")
            if meteo['humidity'] > 85:
                culture_data['protection'].append("⚠️ Humidité élevée - Risque de mildiou")

        conseils_par_culture.append(culture_data)

    conseils['conseils_par_culture'] = conseils_par_culture

    # 1️⃣2️⃣ EXPOSITION AU SOLEIL / OMBRE
    from .models import Parcelle
    parcelle = Parcelle.objects.filter(figure=figure).first()

    exposition_conseils = {
        'plein_soleil': {
            'emoji': '☀️',
            'nom': 'Plein soleil',
            'description': 'Cette parcelle reçoit plus de 6 heures de soleil par jour.',
            'conseils': [
                "🌱 Idéal pour les tomates, poivrons, aubergines, courgettes.",
                "💧 Arrosez plus souvent en période de forte chaleur.",
                "🌿 Paillez pour garder l'humidité.",
                "☀️ Surveillez les coups de soleil sur les jeunes plants."
            ]
        },
        'mi_ombre': {
            'emoji': '🌤️',
            'nom': 'Mi-ombre',
            'description': 'Cette parcelle reçoit entre 4 et 6 heures de soleil par jour.',
            'conseils': [
                "🥬 Parfait pour les salades, épinards, choux, brocolis.",
                "🌿 Idéal pour les fraisiers et les herbes aromatiques.",
                "💧 Arrosez modérément.",
                "🌱 Protégez les cultures sensibles du vent."
            ]
        },
        'ombre': {
            'emoji': '🌥️',
            'nom': 'Ombre',
            'description': 'Cette parcelle reçoit moins de 4 heures de soleil par jour.',
            'conseils': [
                "🍄 Idéal pour les champignons et les fougères.",
                "🌿 Plantez des hostas, des astilbes ou des impatientes.",
                "💧 Arrosez moins fréquemment.",
                "🌱 Surveillez l'humidité excessive."
            ]
        },
        'non_defini': {
            'emoji': '❓',
            'nom': 'Non défini',
            'description': "L'exposition de cette parcelle n'est pas encore définie.",
            'conseils': [
                "📏 Définissez l'exposition dans les paramètres de la parcelle.",
                "☀️ Observez la parcelle à différentes heures de la journée.",
                "🌿 Une bonne exposition est essentielle pour vos cultures."
            ]
        }
    }

    if parcelle and parcelle.exposition:
        expo = exposition_conseils.get(parcelle.exposition, exposition_conseils['non_defini'])
        conseils['exposition'] = {
            'emoji': expo['emoji'],
            'nom': expo['nom'],
            'description': expo['description'],
            'conseils': expo['conseils'],
        }
    else:
        conseils['exposition'] = exposition_conseils['non_defini']

    # ✅ Conseils selon le type de terrain
    if figure.figure_type:
        conseils_type = CONSEILS_PAR_TYPE_TERRAIN.get(figure.figure_type, {})
        if conseils_type:
            conseils['type_terrain'] = {
                'emoji': conseils_type.get('emoji', '🌱'),
                'titre': conseils_type.get('titre', 'Conseils'),
                'conseils': conseils_type.get('conseils', []),
            }
            logger.info(f"✅ Conseils type terrain ajoutés : {figure.figure_type}")

        else:
            conseils['type_terrain'] = None
    else:
        conseils['type_terrain'] = None

    # 🔥 ENREGISTRER DANS LE CACHE GLOBAL
    cache.set(cache_key_global, conseils, 3600)  # 1 heure
    logger.info(f"✅ Conseils mis en cache pour {figure.name}")


    return conseils


def get_fallback_conseils(culture_nom, climat, meteo=None):
    """
    Génère des conseils génériques adaptés au climat pour une culture inconnue
    """
    base = {
        'emoji': '🌱',
        'type': 'Culture',
        'hauteur': 'Variété selon culture',
        'largeur': 'Variété selon culture',
        'espacement': '30-50 cm',
        'espacement_rangs': '40-60 cm',
        'arrosage': [],
        'fertilisation': [],
        'plantation': [],
        'protection': [],
    }

    # Conseils selon le climat
    climats_conseils = {
        'tropical': {
            'arrosage': ["Arrosez abondamment mais espacez les arrosages (2-3x/semaine).", "Arrosez tôt le matin."],
            'fertilisation': ["Apportez de la matière organique chaque mois.", "Fertilisez avec du compost."],
            'plantation': ["Plantez en saison des pluies.", "Protégez du soleil intense avec un voile d'ombrage."],
            'protection': ["Paillez épais (10-15 cm) pour garder l'humidité.", "Surveillez les maladies fongiques."]
        },
        'desertique': {
            'arrosage': ["Arrosez tous les jours en petites quantités.", "Utilisez un goutte-à-goutte."],
            'fertilisation': ["Utilisez un engrais soluble dans l'eau d'arrosage.", "Apportez du compost."],
            'plantation': ["Plantez en cuvette pour retenir l'eau.", "Plantez à l'abri du vent."],
            'protection': ["Paillez épais (15 cm) pour limiter l'évaporation.", "Protégez du vent."]
        },
        'mediterraneen': {
            'arrosage': ["Arrosez le matin pour limiter l'évaporation.", "Installez un goutte-à-goutte."],
            'fertilisation': ["Apportez du compost en automne et au printemps.", "Fertilisez avec du potassium."],
            'plantation': ["Plantez en automne ou au printemps.", "Choisissez des cultures résistantes à la sécheresse."],
            'protection': ["Installez un voile d'ombrage en été.", "Paillez pour garder l'humidité."]
        },
        'continental': {
            'arrosage': ["Arrosez modérément.", "Arrosez au pied pour éviter le mildiou."],
            'fertilisation': ["Apportez du compost en automne pour préparer l'hiver.", "Fertilisez au printemps."],
            'plantation': ["Plantez après les dernières gelées (mai).", "Choisissez des variétés rustiques."],
            'protection': ["Protégez du gel avec un voile d'hivernage.", "Paillez pour protéger les racines."]
        },
        'oceanique': {
            'arrosage': ["Arrosez moins fréquemment, l'humidité naturelle est suffisante."],
            'fertilisation': ["Apportez du compost au printemps.", "Fertilisez avec un engrais équilibré."],
            'plantation': ["Plantez toute l'année, éviter le gel.", "Choisissez des cultures qui aiment l'humidité."],
            'protection': ["Protégez du vent dominant.", "Surveillez les maladies fongiques."]
        },
        'montagnard': {
            'arrosage': ["Arrosez modérément.", "Arrosez au pied."],
            'fertilisation': ["Apportez du compost pour améliorer le sol.", "Fertilisez au printemps."],
            'plantation': ["Plantez des variétés résistantes au froid.", "Plantez après les dernières gelées."],
            'protection': ["Protégez du vent et du gel.", "Paillez pour protéger les racines."]
        },
        'subtropical': {
            'arrosage': ["Arrosez régulièrement en été.", "Arrosez tôt le matin."],
            'fertilisation': ["Apportez du compost en automne.", "Fertilisez au printemps."],
            'plantation': ["Plantez des cultures adaptées aux étés chauds et humides."],
            'protection': ["Protégez du soleil intense en été.", "Paillez pour garder l'humidité."]
        },
        'tempere': {
            'arrosage': ["Arrosez régulièrement sans excès.", "Arrosez au pied."],
            'fertilisation': ["Apportez du compost au printemps et en automne.", "Fertilisez avec un engrais équilibré."],
            'plantation': ["Plantez après les dernières gelées.", "Espacez les plants de 30-50 cm."],
            'protection': ["Paillez pour protéger le sol.", "Surveillez les ravageurs."]
        }
    }

    # Ajouter les conseils climatiques
    if climat in climats_conseils:
        for key in ['arrosage', 'fertilisation', 'plantation', 'protection']:
            if key in climats_conseils[climat]:
                base[key].extend(climats_conseils[climat][key])

    # Ajustements météo
    if meteo:
        if meteo['temperature'] > 35:
            base['arrosage'].append("🔥 Canicule ! Arrosez abondamment ce soir")
            base['protection'].append("☀️ Installez un voile d'ombrage")
        if meteo['temperature'] < 0:
            base['protection'].append("❄️ Gel ! Protégez vos plantes")
        if meteo['humidity'] > 85:
            base['protection'].append("⚠️ Humidité élevée - Risque de mildiou")
        if meteo['wind_speed'] > 50:
            base['protection'].append("💨 Vent fort - Protégez les cultures")

    return base


def get_adaptation_climat(culture_nom, climat):
    """
    Retourne une note d'adaptation de la culture au climat
    """
    culture_lower = culture_nom.lower()

    # Cultures adaptées par climat
    adaptations = {
        'tropical': ['banane', 'mangue', 'ananas', 'cacao', 'cafe', 'manioc', 'igname', 'papaye', 'goyave', 'litchi',
                     'fruit de la passion', 'gingembre', 'curcuma', 'vanille', 'cannelle', 'poivre', 'riz'],
        'desertique': ['datte', 'olivier', 'figue', 'grenade', 'amandier', 'caroubier', 'pistache'],
        'mediterraneen': ['olivier', 'tomate', 'aubergine', 'poivron', 'lavande', 'romarin', 'thym', 'sauge', 'vigne',
                          'amandier', 'abricot', 'figue', 'grenade'],
        'continental': ['pomme', 'poire', 'cerise', 'fraise', 'framboise', 'pomme de terre', 'carotte', 'chou', 'ble',
                        'orge'],
        'oceanique': ['pomme', 'poire', 'fraise', 'salade', 'epinard', 'concombre', 'courgette', 'haricot'],
        'montagnard': ['pomme', 'framboise', 'pomme de terre', 'chou', 'carotte', 'seigle', 'avoine'],
        'subtropical': ['avocat', 'kiwi', 'citronnier', 'oranger', 'pamplemousse', 'mandarine', 'lime', 'kumquat'],
        'tempere': ['tomate', 'carotte', 'salade', 'pomme', 'fraise', 'haricot', 'courgette', 'poivron', 'aubergine']
    }

    for adapte in adaptations.get(climat, []):
        if adapte in culture_lower or culture_lower in adapte:
            return "✅ Parfaitement adaptée à ce climat"

    # Vérifier si la culture est adaptée à d'autres climats
    for other_climat, cultures in adaptations.items():
        for adapte in cultures:
            if adapte in culture_lower or culture_lower in adapte:
                return f"🟡 Peut s'adapter avec des soins particuliers (mieux en {other_climat})"

    return "⚠️ Nécessite une protection spéciale et des soins attentifs"


def get_culture_emoji(culture_nom):
    """Retourne l'emoji d'une culture"""
    emojis = {
        'tomate': '🍅', 'carotte': '🥕', 'salade': '🥬', 'courgette': '🥒',
        'poivron': '🫑', 'aubergine': '🍆', 'haricot': '🫘', 'pomme de terre': '🥔',
        'oignon': '🧅', 'ail': '🧄', 'fraise': '🍓', 'pomme': '🍎',
        'poire': '🍐', 'cerise': '🍒', 'pêche': '🍑', 'abricot': '🍑',
        'vigne': '🍇', 'raisin': '🍇', 'olivier': '🫒', 'citronnier': '🍋',
        'oranger': '🍊', 'pamplemousse': '🍊', 'bananier': '🍌', 'manguier': '🥭',
        'ananas': '🍍', 'avocat': '🥑', 'kiwi': '🥝', 'framboise': '🫐',
        'myrtille': '🫐', 'cacao': '🍫', 'cafeier': '☕', 'vanille': '🌿',
        'gingembre': '🫚', 'curcuma': '🧡', 'manioc': '🌿', 'igname': '🌿',
        'patate douce': '🍠', 'riz': '🍚', 'maïs': '🌽', 'blé': '🌾',
        'concombre': '🥒', 'melon': '🍈', 'pastèque': '🍉', 'chou': '🥬',
        'brocoli': '🥦', 'épinard': '🥬', 'laitue': '🥬', 'basilic': '🌿',
        'menthe': '🌿', 'persil': '🌿', 'coriandre': '🌿', 'aneth': '🌿',
        'romarin': '🌿', 'thym': '🌿', 'sauge': '🌿', 'lavande': '🌸',
        'tournesol': '🌻', 'rose': '🌹', 'tulipe': '🌷', 'orchidée': '🌺',
    }
    return emojis.get(culture_nom.lower(), '🌱')

@login_required
def plan_fertilisation(request):
    """Affiche le plan de fertilisation personnalisé (Premium, Enseignant ou Élève en classe)"""
    from .models import Parcelle, GeometricFigure, RecommandationFertilisation, Abonnement
    from django.db.models import Q
    import requests
    from django.conf import settings

    # ✅ Vérification d'accès : Premium, Enseignant OU Élève dans une classe
    est_eleve = hasattr(request.user, 'profil_eleve') and request.user.profil_eleve and request.user.profil_eleve.classe is not None

    if not est_eleve:
        try:
            abonnement = request.user.abonnement
            if not abonnement.est_actif or abonnement.plan.nom not in ['PREMIUM', 'ENSEIGNANT']:
                messages.warning(request, "🔒 Le plan de fertilisation est disponible avec l'abonnement Premium.")
                return redirect('vegetables_fruits:tarification')
        except Abonnement.DoesNotExist:
            messages.warning(request, "🔒 Le plan de fertilisation est disponible avec l'abonnement Premium.")
            return redirect('vegetables_fruits:tarification')

    user = request.user

    # Récupérer toutes les parcelles pour le sélecteur
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    # Déterminer la parcelle sélectionnée
    selected_parcelle_id = request.GET.get('parcelle_id')
    if selected_parcelle_id:
        selected_parcelle = parcelles.filter(id=selected_parcelle_id).first()
    else:
        selected_parcelle = parcelles.first()

    # Récupérer la région de la parcelle sélectionnée
    region = 'iledefrance'
    pays = 'France'
    if selected_parcelle and selected_parcelle.figure and selected_parcelle.figure.adresse_lat and selected_parcelle.figure.adresse_lng:
        try:
            lat = selected_parcelle.figure.adresse_lat
            lng = selected_parcelle.figure.adresse_lng
            url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{lng},{lat}.json?access_token={settings.MAPBOX_TOKEN}&language=fr"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                features = data.get('features', [])
                for feature in features:
                    if 'country' in feature.get('place_type', []):
                        pays = feature.get('text', 'France')
                    if 'region' in feature.get('place_type', []):
                        region = feature.get('text', '').lower().replace(' ', '')
        except Exception as e:
            logger.error(f"Erreur géocodage: {e}")


    # Récupérer les cultures de la parcelle sélectionnée
    cultures_parcelle = []
    if selected_parcelle and selected_parcelle.figure:
        for crop in selected_parcelle.figure.crops:
            if 'name' in crop:
                cultures_parcelle.append(crop['name'].lower())

    # Récupérer les recommandations pour ces cultures (avec région)
    recommandations = []
    for culture in cultures_parcelle:
        rec = RecommandationFertilisation.objects.filter(
            culture__icontains=culture,
            type_sol__in=[selected_parcelle.type_sol, 'tous'] if selected_parcelle else [],
            saison__in=[get_saison_actuelle(), 'toute']
        ).first()
        if rec:
            recommandations.append({
                'culture': culture.capitalize(),
                'engrais': rec.engrais_recommande,
                'quantite': rec.quantite_recommandee,
                'frequence': rec.frequence,
                'conseils': rec.conseils,
            })

    # Statistiques
    stats = {
        'nb_parcelles': parcelles.count(),
        'surface_totale': sum([p.surface_m2 for p in parcelles]),
        'nb_cultures': len(cultures_parcelle),
    }

    return render(request, 'vegetables_fruits/plan_fertilisation.html', {
        'parcelles': parcelles,
        'selected_parcelle': selected_parcelle,
        'cultures_parcelle': cultures_parcelle,
        'recommandations': recommandations,
        'stats': stats,
        'region': region,
    })



@login_required
def gestion_maladies(request):
    """Affiche la page de gestion des maladies avec détection par symptômes (Premium, Enseignant ou Élève en classe)"""
    from .models import Parcelle, GeometricFigure, Maladie, Abonnement
    from django.db.models import Q
    from django.db import connection
    import json

    # ✅ Vérification d'accès : Premium, Enseignant OU Élève dans une classe
    est_eleve = hasattr(request.user, 'profil_eleve') and request.user.profil_eleve and request.user.profil_eleve.classe is not None

    if not est_eleve:
        try:
            abonnement = request.user.abonnement
            if not abonnement.est_actif or abonnement.plan.nom != 'PREMIUM':
                messages.warning(request, "🔒 La gestion des maladies est disponible avec l'abonnement Premium.")
                return redirect('vegetables_fruits:tarification')
        except Abonnement.DoesNotExist:
            messages.warning(request, "🔒 La gestion des maladies est disponible avec l'abonnement Premium.")
            return redirect('vegetables_fruits:tarification')

    user = request.user

    # ✅ Récupérer toutes les parcelles de l'utilisateur
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    # ✅ Récupérer la parcelle sélectionnée (via GET)
    parcelle_id = request.GET.get('parcelle_id')
    selected_parcelle = None
    if parcelle_id:
        try:
            selected_parcelle = parcelles.get(id=parcelle_id)
        except Parcelle.DoesNotExist:
            selected_parcelle = None

    # Si aucune parcelle n'est sélectionnée, prendre la première
    if not selected_parcelle and parcelles.exists():
        selected_parcelle = parcelles.first()

    # Récupérer la région et le pays de la parcelle sélectionnée
    region = 'iledefrance'
    pays = 'France'
    if selected_parcelle and selected_parcelle.figure and selected_parcelle.figure.adresse_lat and selected_parcelle.figure.adresse_lng:
        import requests
        from django.conf import settings
        try:
            lat = selected_parcelle.figure.adresse_lat
            lng = selected_parcelle.figure.adresse_lng
            url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{lng},{lat}.json?access_token={settings.MAPBOX_TOKEN}&language=fr"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                features = data.get('features', [])
                for feature in features:
                    if 'country' in feature.get('place_type', []):
                        pays = feature.get('text', 'France')
                    if 'region' in feature.get('place_type', []):
                        region = feature.get('text', '').lower().replace(' ', '')
        except Exception as e:
            logger.error(f"Erreur géocodage: {e}")


    # Récupérer les cultures plantées sur la parcelle sélectionnée
    cultures_plantees = set()
    if selected_parcelle and selected_parcelle.figure:
        for crop in selected_parcelle.figure.crops:
            if 'name' in crop:
                cultures_plantees.add(crop['name'].lower())

    # Traitement POST (détection par symptômes)
    resultats_detection = []
    symptomes_selectionnes = request.POST.getlist('symptomes')

    if request.method == 'POST' and symptomes_selectionnes:
        # Récupérer les maladies pour la région
        if connection.vendor == 'sqlite':
            maladies = Maladie.objects.filter(
                Q(regions__icontains=region) | Q(regions__icontains='tous') | Q(regions__icontains='europe')
            ).filter(
                Q(pays__icontains=pays) | Q(pays__icontains='tous')
            )
        else:
            maladies = Maladie.objects.filter(
                Q(regions__contains=region) | Q(regions__contains='tous') | Q(regions__contains='europe')
            ).filter(
                Q(pays__contains=pays) | Q(pays__contains='tous')
            )

        # Pour chaque maladie, calculer le score de correspondance
        for maladie in maladies:
            symptomes_maladie = maladie.symptomes
            correspondances = sum(1 for s in symptomes_selectionnes if s in symptomes_maladie)

            if correspondances > 0:
                taux = correspondances / len(symptomes_selectionnes)
                resultats_detection.append({
                    'maladie': maladie,
                    'correspondances': correspondances,
                    'taux': round(taux * 100, 1),
                    'confiance': 'forte' if taux >= 0.8 else ('moyenne' if taux >= 0.5 else 'faible'),
                })

        # Trier par taux de correspondance
        resultats_detection.sort(key=lambda x: x['taux'], reverse=True)

        # Si aucun résultat, proposer une maladie générique
        if not resultats_detection:
            maladie_generique = Maladie.objects.filter(
                Q(regions__icontains='tous')
            ).first()
            if maladie_generique:
                resultats_detection.append({
                    'maladie': maladie_generique,
                    'confiance': 'faible',
                    'message': "Aucune maladie spécifique détectée. Voici une maladie courante à surveiller."
                })

    # Maladies connues (pour l'affichage)
    maladies_connues = Maladie.objects.all()[:5]

    return render(request, 'vegetables_fruits/gestion_maladies.html', {
        'parcelles': parcelles,
        'selected_parcelle': selected_parcelle,
        'region': region,
        'pays': pays,
        'cultures_plantees': list(cultures_plantees),
        'resultats_detection': resultats_detection,
        'maladies_connues': maladies_connues,
        'symptomes_selectionnes': symptomes_selectionnes,
    })


@login_required
def planification_semis(request):
    from .models import Parcelle, CalendrierUser, Culture, PreconisationMondiale
    from datetime import timedelta, date

    user = request.user

    # ✅ Vérification : Élève dans une classe
    est_eleve = hasattr(user, 'profil_eleve') and user.profil_eleve and user.profil_eleve.classe is not None

    if not est_eleve:
        try:
            abonnement = request.user.abonnement
            if not abonnement.est_actif or abonnement.plan.nom not in ['PREMIUM', 'ENSEIGNANT']:
                messages.warning(request, "🔒 Le planification des semis est disponible avec l'abonnement Premium.")
                return redirect('vegetables_fruits:tarification')
        except Abonnement.DoesNotExist:
            messages.warning(request, "🔒 Le plan de fertilisation est disponible avec l'abonnement Premium.")
            return redirect('vegetables_fruits:tarification')


    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    # Récupérer la région climatique de l'utilisateur (via la première parcelle)
    region_climatique = 'tempere' # Par défaut
    # (ici tu peux ajouter une logique pour détecter la région via les coordonnées)

    parcelle_id = request.GET.get('parcelle_id')
    selected_parcelle = None
    if parcelle_id:
        try:
            selected_parcelle = parcelles.get(id=parcelle_id)
        except Parcelle.DoesNotExist:
            selected_parcelle = None

    if selected_parcelle:
        semis = CalendrierUser.objects.filter(
            utilisateur=user,
            figure=selected_parcelle.figure
        ).order_by('date_semis', 'date_plantation')
    else:
        semis = CalendrierUser.objects.filter(utilisateur=user).order_by('date_semis', 'date_plantation')

    today = date.today()

    for semis_item in semis:
        culture = Culture.objects.filter(nom__icontains=semis_item.culture).first()
        jours_pousse = culture.jours_pousse if culture else 60

        # Calculer la date de fin
        if semis_item.date_semis:
            semis_item.date_fin = semis_item.date_semis + timedelta(days=jours_pousse)
        elif semis_item.date_plantation:
            semis_item.date_fin = semis_item.date_plantation + timedelta(days=jours_pousse)

        # Vérifier la préconisation mondiale
        preconisation = PreconisationMondiale.objects.filter(
            culture__icontains=semis_item.culture,
            region_climatique=region_climatique
        ).first()

        if preconisation:
            mois_semis = semis_item.date_semis.month if semis_item.date_semis else None
            mois_plantation = semis_item.date_plantation.month if semis_item.date_plantation else None

            if mois_semis:
                if mois_semis < preconisation.mois_debut_semis:
                    semis_item.statut_semis = "Trop tôt"
                    semis_item.statut_couleur = "warning"
                elif mois_semis > preconisation.mois_fin_semis:
                    semis_item.statut_semis = "Trop tard"
                    semis_item.statut_couleur = "danger"
                else:
                    semis_item.statut_semis = "OK"
                    semis_item.statut_couleur = "success"
            elif mois_plantation:
                if mois_plantation < preconisation.mois_debut_plantation:
                    semis_item.statut_semis = "Trop tôt"
                    semis_item.statut_couleur = "warning"
                elif mois_plantation > preconisation.mois_fin_plantation:
                    semis_item.statut_semis = "Trop tard"
                    semis_item.statut_couleur = "danger"
                else:
                    semis_item.statut_semis = "OK"
                    semis_item.statut_couleur = "success"
            else:
                semis_item.statut_semis = "Non disponible"
                semis_item.statut_couleur = "secondary"
        else:
            semis_item.statut_semis = "Non disponible"
            semis_item.statut_couleur = "secondary"

    return render(request, 'vegetables_fruits/planification_semis.html', {
        'parcelles': parcelles,
        'selected_parcelle': selected_parcelle,
        'semis': semis,
        'region_climatique': region_climatique,
        'today': today,
    })



@login_required
def bilan_carbone_eleve(request, eleve_id):
    """Affiche le bilan carbone d'un élève spécifique (pour l'enseignant)"""
    from .models import Eleve, Parcelle, BilanCarbone, Production

    # Vérification que l'enseignant a accès à cet élève
    eleve = get_object_or_404(Eleve, id=eleve_id, classe__enseignant=request.user)

    parcelles = Parcelle.objects.filter(utilisateur=eleve.user, est_active=True).prefetch_related('productions')

    total_emission = 0
    total_sequestration = 0
    total_bilan = 0
    details_parcelles = []
    labels_graphique = []
    data_emission = []
    data_sequestration = []

    for parcelle in parcelles:
        productions = parcelle.productions.all()
        cultures_count = productions.count()

        emission = cultures_count * 2.5
        sequestration = parcelle.surface_m2 * 0.5

        bilan, created = BilanCarbone.objects.get_or_create(
            parcelle=parcelle,
            defaults={'emission_co2_kg': emission, 'sequestration_co2_kg': sequestration, 'bilan_net_kg': sequestration - emission}
        )
        if not created:
            bilan.emission_co2_kg = emission
            bilan.sequestration_co2_kg = sequestration
            bilan.bilan_net_kg = sequestration - emission
            bilan.save()

        total_emission += emission
        total_sequestration += sequestration
        total_bilan += bilan.bilan_net_kg

        labels_graphique.append(parcelle.nom)
        data_emission.append(round(emission, 1))
        data_sequestration.append(round(sequestration, 1))

        details_parcelles.append({
            'parcelle': parcelle,
            'emission': round(emission, 1),
            'sequestration': round(sequestration, 1),
            'bilan': round(bilan.bilan_net_kg, 1),
            'cultures': cultures_count,
        })

    return render(request, 'vegetables_fruits/bilan_carbone.html', {
        'details_parcelles': details_parcelles,
        'total_emission': round(total_emission, 1),
        'total_sequestration': round(total_sequestration, 1),
        'total_bilan': round(total_bilan, 1),
        'labels_graphique': labels_graphique,
        'data_emission': data_emission,
        'data_sequestration': data_sequestration,
        'titre_page': f"Bilan carbone de {eleve.user.username}",
        'a_acces_bilan_carbone': True,
    })


@login_required
def statistiques_avancees_eleve(request, eleve_id):
    """Affiche les statistiques avancées d'un élève (pour l'enseignant)"""
    from .models import Eleve, GeometricFigure

    # 1. Vérification que l'élève appartient bien à une classe de cet enseignant
    eleve = get_object_or_404(Eleve, id=eleve_id, classe__enseignant=request.user)

    # 2. On récupère l'utilisateur lié à l'élève (c'est LUI qui a les parcelles et les données)
    user_eleve = eleve.user

    # 3. Récupérer les parcelles de L'ÉLÈVE (pas de l'enseignant)
    figures = GeometricFigure.objects.filter(user=user_eleve).order_by('name')

    # 4. Filtres (on lit les paramètres GET de l'URL)
    figure_id = request.GET.get('parcelle')
    periode = request.GET.get('periode', '12m')

    # 5. On utilise le CACHE et la FONCTION EXACTE de la vue normale, mais pour l'élève
    cache_key = f"stats_bento_{user_eleve.id}_{figure_id or 'all'}_{periode}"
    data = cache.get(cache_key)

    if not data:
        # _compute_stats fait tous les calculs complexes et prépare le JSON
        data = _compute_stats(user_eleve, figure_id=figure_id, periode=periode)
        cache.set(cache_key, data, 300)

    # 6. Le contexte est STRICTEMENT le même que pour la vue normale
    context = {
        'figures': figures,
        'selected_figure_id': int(figure_id) if figure_id else None,
        'selected_periode': periode,
        'data_json': data,
        **data,
        'titre_page': f"Statistiques de {eleve.user.username}",
        'est_vue_enseignant': True,
        # On passe l'ID de l'élève pour que le template sache où envoyer les requêtes AJAX
        'eleve_id': eleve.id,
    }

    return render(request, 'vegetables_fruits/statistiques_avancees.html', context)


@login_required
def api_stats_bento_eleve(request, eleve_id):
    from .models import Eleve
    # On vérifie que c'est bien un élève de l'enseignant
    eleve = get_object_or_404(Eleve, id=eleve_id, classe__enseignant=request.user)
    user_eleve = eleve.user

    figure_id = request.GET.get('parcelle')
    periode = request.GET.get('periode', '12m')

    data = _compute_stats(user_eleve, figure_id=figure_id, periode=periode)
    return JsonResponse(data)




@login_required
def planification_semis_eleve(request, eleve_id):
    """Affiche la planification des semis d'un élève (pour l'enseignant)"""
    from .models import Eleve, Parcelle, CalendrierUser, Culture
    from datetime import timedelta, date

    eleve = get_object_or_404(Eleve, id=eleve_id, classe__enseignant=request.user)
    user = eleve.user

    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    semis = CalendrierUser.objects.filter(utilisateur=user).order_by('date_semis', 'date_plantation')

    today = date.today()

    for semis_item in semis:
        culture = Culture.objects.filter(nom__icontains=semis_item.culture).first()
        jours_pousse = culture.jours_pousse if culture else 60

        if semis_item.date_semis:
            semis_item.date_fin = semis_item.date_semis + timedelta(days=jours_pousse)
        elif semis_item.date_plantation:
            semis_item.date_fin = semis_item.date_plantation + timedelta(days=jours_pousse)

        # Pour l'instant, pas de comparaison avec préconisations
        semis_item.statut_semis = "Non disponible"
        semis_item.statut_couleur = "secondary"

    return render(request, 'vegetables_fruits/planification_semis.html', {
        'semis': semis,
        'eleve': eleve,
        'titre_page': f"Planification des semis de {eleve.user.username}",
    })


@login_required
def conseiller_sol(request):
    """Affiche des conseils personnalisés selon le type de sol et les cultures (Premium, Enseignant ou Élève en classe)"""
    from .models import Parcelle, Culture
    from django.contrib import messages

    # ✅ Vérification d'accès : Premium, Enseignant OU Élève dans une classe
    est_eleve = hasattr(request.user, 'profil_eleve') and request.user.profil_eleve and request.user.profil_eleve.classe is not None

    if not est_eleve:
        try:
            abonnement = request.user.abonnement
            if not abonnement.est_actif or abonnement.plan.nom not in ['PREMIUM', 'ENSEIGNANT']:
                messages.warning(request, "🔒 Le Conseiller Sol est disponible avec l'abonnement Premium.")
                return redirect('vegetables_fruits:tarification')
        except Abonnement.DoesNotExist:
            messages.warning(request, "🔒 Le Conseiller Sol est disponible avec l'abonnement Premium.")
            return redirect('vegetables_fruits:tarification')

    user = request.user
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    # Récupérer la parcelle sélectionnée
    parcelle_id = request.GET.get('parcelle_id')
    selected_parcelle = None
    if parcelle_id:
        try:
            selected_parcelle = parcelles.get(id=parcelle_id)
        except Parcelle.DoesNotExist:
            selected_parcelle = None
    else:
        # Si aucune parcelle n'est sélectionnée, prendre la première
        selected_parcelle = parcelles.first()

    # Récupérer les cultures de la parcelle
    cultures_parcelle = []
    if selected_parcelle and selected_parcelle.figure:
        for crop in selected_parcelle.figure.crops:
            if 'name' in crop:
                cultures_parcelle.append(crop['name'])

    # Dictionnaire des conseils par type de sol et culture
    conseils_sol = {
        'argileux': {
            'default': '🌱 Sol argileux : ajoutez du compost et paillez le sol. Évitez de trop arroser.',
            'tomate': '🍅 Sol argileux : aérez la terre avec du sable pour éviter que les racines ne pourrissent.',
            'carotte': '🥕 Sol argileux : ajoutez du sable pour que les carottes poussent droites.',
            'salade': '🥬 Sol argileux : paillez pour garder l\'humidité.',
        },
        'sableux': {
            'default': '🌱 Sol sableux : arrosez plus souvent et ajoutez de la matière organique.',
            'tomate': '🍅 Sol sableux : ajoutez du compost pour retenir l\'eau.',
            'carotte': '🥕 Sol sableux : ajoutez du compost pour éviter que les carottes ne sèchent.',
            'salade': '🥬 Sol sableux : arrosez régulièrement.',
        },
        'limoneux': {
            'default': '🌱 Sol limoneux : fertile et bien drainé. Ajoutez du compost pour maintenir la fertilité.',
            'tomate': '🍅 Sol limoneux : idéal ! Ajoutez simplement du compost.',
            'carotte': '🥕 Sol limoneux : parfait pour les carottes.',
            'salade': '🥬 Sol limoneux : arrosez modérément.',
        },
        'humifère': {
            'default': '🌱 Sol humifère : riche en matière organique. Ajoutez du compost pour maintenir la fertilité.',
            'tomate': '🍅 Sol humifère : excellent pour les tomates.',
            'carotte': '🥕 Sol humifère : idéal pour les carottes.',
            'salade': '🥬 Sol humifère : arrosez modérément.',
        },
        'calcaire': {
            'default': '🌱 Sol calcaire : ajoutez du compost et arrosez régulièrement.',
            'tomate': '🍅 Sol calcaire : ajoutez du compost pour éviter le jaunissement des feuilles.',
            'carotte': '🥕 Sol calcaire : ajoutez du compost pour éviter que les carottes ne se déforment.',
            'salade': '🥬 Sol calcaire : arrosez régulièrement.',
        },
    }

    # Générer les conseils pour les cultures de la parcelle
    conseils = []
    if selected_parcelle:
        type_sol = selected_parcelle.type_sol
        for culture in cultures_parcelle:
            culture_lower = culture.lower()
            conseil = conseils_sol.get(type_sol, {}).get(culture_lower, None)
            if not conseil:
                conseil = conseils_sol.get(type_sol, {}).get('default',
                                                             '🌱 Aucun conseil spécifique pour ce sol. Contactez un spécialiste.')
            conseils.append({
                'culture': culture,
                'conseil': conseil,
            })

    return render(request, 'vegetables_fruits/conseiller_sol.html', {
        'parcelles': parcelles,
        'selected_parcelle': selected_parcelle,
        'conseils': conseils,
        'cultures_parcelle': cultures_parcelle,
    })


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from django.http import HttpResponse

@login_required
def export_fiche_produit_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Fiche_produit_Agriculture2.0.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, textColor=colors.green, alignment=1)
    elements = []

    # Titre
    elements.append(Paragraph("🌱 Agriculture 2.0", title_style))
    elements.append(Paragraph("Fiche produit – Application mobile de jardinage pédagogique", styles['Heading2']))
    elements.append(Spacer(1, 1*cm))

    # Présentation
    elements.append(Paragraph("<b>📌 Présentation</b>", styles['Heading3']))
    elements.append(Paragraph("Agriculture 2.0 est une application web mobile (PWA) qui permet d'apprendre l'agriculture en s'amusant. Que vous soyez particulier, enseignant ou établissement scolaire, Agriculture 2.0 vous accompagne dans la création et le suivi de vos parcelles.", styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))

    # Public cible
    elements.append(Paragraph("<b>🎯 Public cible</b>", styles['Heading3']))
    elements.append(Paragraph("🌱 Particuliers : Apprendre à jardiner, suivre ses cultures, comprendre son sol", styles['Normal']))
    elements.append(Paragraph("🏫 Écoles : Projet pédagogique, éducation à l'environnement", styles['Normal']))
    elements.append(Paragraph("👨‍🏫 Enseignants : Suivi des élèves, création de défis, outils d'animation", styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))

    # Tarifs
    elements.append(Paragraph("<b>💰 Tarifs</b>", styles['Heading3']))
    data = [['Plan', 'Mensuel', 'Annuel', 'Parcelles'],
            ['🌱 Gratuit', '0€', '0€', '3'],
            ['🌿 Basique', '6,99€', '69€', '15'],
            ['🌳 Premium', '14,99€', '149€', '50'],
            ['🏫 Enseignant', '15,99€', '159€', 'Illimité']]
    table = Table(data, colWidths=[4*cm, 3*cm, 3*cm, 4*cm])
    table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.green), ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke), ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('GRID', (0,0), (-1,-1), 1, colors.grey)]))
    elements.append(table)
    elements.append(Spacer(1, 1*cm))

    # Contact
    elements.append(Paragraph("<b>🔗 Liens utiles</b>", styles['Heading3']))
    elements.append(Paragraph("🌐 www.agriculture2.0", styles['Normal']))
    elements.append(Paragraph("📧 contact@agriculture2.0", styles['Normal']))

    doc.build(elements)
    return response


def fiche_produit(request):
    """Page fiche produit"""
    return render(request, 'vegetables_fruits/fiche_produit.html')


# ==================== PAGES DOCUMENTS ====================


def guide_particulier(request):
    return render(request, 'vegetables_fruits/documents/guide_particulier.html')

def guide_enseignant(request):
    return render(request, 'vegetables_fruits/documents/guide_enseignant.html')

def guide_vente_ecoles(request):
    return render(request, 'vegetables_fruits/documents/guide_vente_ecoles.html')

def architecture_technique(request):
    return render(request, 'vegetables_fruits/documents/architecture_technique.html')

def guide_admin(request):
    return render(request, 'vegetables_fruits/documents/guide_admin.html')

def strategie_deploiement(request):
    return render(request, 'vegetables_fruits/documents/strategie_deploiement.html')

def previsionnel_financier(request):
    return render(request, 'vegetables_fruits/documents/previsionnel_financier.html')

def business_plan(request):
    return render(request, 'vegetables_fruits/documents/business_plan.html')


            # SCENARIOS TEST

def plan_test(request):
    return render(request, 'vegetables_fruits/plan_test.html')


@login_required
def alertes_traitements(request):
    """Page des alertes traitements"""
    user = request.user

    # ✅ On récupère l'ID de la parcelle depuis l'URL
    parcelle_id = request.GET.get('parcelle_id')

    # 1. On prépare les requêtes de base
    qs_actives = AlerteTraitement.objects.filter(
        utilisateur=user,
        statut__in=['en_attente', 'envoyee']
    )
    qs_traitees = AlerteTraitement.objects.filter(utilisateur=user, statut='traitee')
    qs_ignorees = AlerteTraitement.objects.filter(utilisateur=user, statut='ignoree')

    # 2. ✅ On applique le filtre si une parcelle est sélectionnée
    if parcelle_id:
        qs_actives = qs_actives.filter(figure_id=parcelle_id)
        qs_traitees = qs_traitees.filter(figure_id=parcelle_id)
        qs_ignorees = qs_ignorees.filter(figure_id=parcelle_id)

    # 3. On prépare les alertes actives pour l'affichage
    alertes_actives = qs_actives.select_related('culture', 'maladie', 'figure').order_by('-date_creation')

    # 4. Calcul des gravités
    alertes_par_gravite = {
        'critique': qs_actives.filter(niveau_risque='critique').count(),
        'elevee': qs_actives.filter(niveau_risque='elevee').count(),
        'moyenne': qs_actives.filter(niveau_risque='moyenne').count(),
        'faible': qs_actives.filter(niveau_risque='faible').count(),
        'contamination': qs_actives.filter(est_contamination=True).count(),  # ✅ Ajouté car présent dans ton template
    }

    # 5. On récupère la liste des parcelles pour un éventuel sélecteur (optionnel)
    from .models import GeometricFigure
    figures = GeometricFigure.objects.filter(user=user)

    context = {
        'alertes_actives': alertes_actives,
        'alertes_traitees': qs_traitees.count(),
        'alertes_ignorees': qs_ignorees.count(),
        'alertes_par_gravite': alertes_par_gravite,
        'total_alertes': qs_actives.count(),
        'figures': figures,  # Si tu veux ajouter le sélecteur dans ce template
        'selected_figure_id': int(parcelle_id) if parcelle_id else None,
    }

    return render(request, 'vegetables_fruits/alertes_traitements.html', context)


@login_required
def traiter_alerte(request, alerte_id):
    alerte = get_object_or_404(AlerteTraitement, id=alerte_id, utilisateur=request.user)
    alerte.marquer_traitee()
    messages.success(request, f"✅ Traitement marqué comme effectué pour {alerte.culture.nom}")

    # ✅ On conserve l'ID de la parcelle dans l'URL de retour
    parcelle_id = request.GET.get('parcelle_id') or request.POST.get('parcelle_id')
    if parcelle_id:
        return redirect(f"{reverse('vegetables_fruits:alertes_traitements')}?parcelle_id={parcelle_id}")
    return redirect('vegetables_fruits:alertes_traitements')

@login_required
def ignorer_alerte_traitement(request, alerte_id):
    alerte = get_object_or_404(AlerteTraitement, id=alerte_id, utilisateur=request.user)
    alerte.marquer_ignoree()
    messages.info(request, f"⏭️ Alerte ignorée pour {alerte.culture.nom}")

    # ✅ On conserve l'ID de la parcelle dans l'URL de retour
    parcelle_id = request.GET.get('parcelle_id') or request.POST.get('parcelle_id')
    if parcelle_id:
        return redirect(f"{reverse('vegetables_fruits:alertes_traitements')}?parcelle_id={parcelle_id}")
    return redirect('vegetables_fruits:alertes_traitements')


from django.views.decorators.http import require_POST


@login_required
@require_POST
def api_marquer_meteo_lue(request, alerte_id):
    """Marque une alerte météo spécifique comme lue (ignorée/traitée)."""
    try:
        alerte = AlerteMeteo.objects.get(id=alerte_id, utilisateur=request.user)

        # On la marque comme ignorée (ou 'envoyee' selon ta logique métier)
        alerte.statut = 'ignoree'
        alerte.save()

        return JsonResponse({'success': True})
    except AlerteMeteo.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Alerte introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



def verifier_compatibilite_plantation(culture_nom, figure_id, maladie_nom=None):
    """
    Vérifie si une culture peut être plantée à proximité d'une culture malade

    Paramètres :
    - culture_nom : nom de la culture à planter
    - figure_id : ID de la parcelle cible
    - maladie_nom : nom de la maladie (optionnel)

    Retourne :
    {
        'compatible': bool,
        'sensible': bool,
        'statut': str, # 'securise', 'a_risque', 'deconseille', 'dangereux'
        'message': str,
        'conseils': str,
        'cultures_voisines': list,
    }
    """
    from .models import GeometricFigure, MaladieCulture, AssociationCulture, Culture

    resultat = {
        'compatible': True,
        'sensible': False,
        'statut': 'securise',
        'message': '',
        'conseils': '',
        'cultures_voisines': [],
    }

    # Récupérer la figure
    try:
        figure = GeometricFigure.objects.get(id=figure_id)
    except GeometricFigure.DoesNotExist:
        resultat['statut'] = 'erreur'
        resultat['message'] = "Parcelle non trouvée"
        return resultat

    # Récupérer toutes les cultures de la parcelle
    cultures_voisines = []
    for crop in figure.crops:
        if 'name' in crop:
            cultures_voisines.append(crop['name'].lower())

    if not cultures_voisines:
        resultat['statut'] = 'securise'
        resultat['message'] = "Aucune culture à proximité. Vous pouvez planter en toute sécurité."
        resultat['conseils'] = "🌱 Profitez-en pour commencer votre jardin !"
        return resultat

    resultat['cultures_voisines'] = cultures_voisines

    # Vérifier les maladies transmissibles
    maladies_sensibles = set()
    for culture_voisine in cultures_voisines:
        # Vérifier si la culture est sensible à la maladie
        if maladie_nom:
            maladies = MaladieCulture.objects.filter(
                cultures_cible__icontains=culture_voisine
            )
            for maladie in maladies:
                if maladie_nom.lower() in maladie.nom.lower():
                    maladies_sensibles.add(culture_voisine)

    # Vérifier les compatibilités (compagnonnage)
    incompatibilites = set()
    compatibilites = set()

    for culture_voisine in cultures_voisines:
        # Vérifier les associations
        associations = AssociationCulture.objects.filter(
            pays__in=['tous', 'france', 'europe']
        )

        for assoc in associations:
            # Vérifier si la culture à planter est incompatible avec une culture voisine
            if (assoc.culture1.lower() == culture_nom.lower() and
                    assoc.culture2.lower() == culture_voisine.lower() and
                    assoc.type_association == 'mauvaise'):
                incompatibilites.add(culture_voisine)

            # Vérifier si la culture à planter est compatible avec une culture voisine
            if (assoc.culture1.lower() == culture_nom.lower() and
                    assoc.culture2.lower() == culture_voisine.lower() and
                    assoc.type_association == 'bonne'):
                compatibilites.add(culture_voisine)

    # Déterminer le statut
    est_sensible = len(maladies_sensibles) > 0
    est_incompatible = len(incompatibilites) > 0

    if est_sensible and est_incompatible:
        resultat['statut'] = 'dangereux'
        resultat['compatible'] = False
        resultat['sensible'] = True
        resultat[
            'message'] = "🚨 DANGEREUX ! Cette culture est incompatible avec les cultures voisines ET sensible à la maladie détectée."
        resultat['conseils'] = (
            "❌ NE PLANTEZ PAS cette culture ici !\n"
            " • Risque de contamination de la maladie\n"
            " • Les cultures voisines sont incompatibles\n"
            " • La culture sera affaiblie et malade\n\n"
            "💡 Alternatives :\n"
            " • Choisissez une autre parcelle\n"
            " • Attendez la guérison des cultures malades\n"
            " • Plantez une culture résistante"
        )
    elif est_sensible:
        resultat['statut'] = 'a_risque'
        resultat['compatible'] = True
        resultat['sensible'] = True
        resultat[
            'message'] = "⚠️ À RISQUE ! Cette culture est sensible à la maladie détectée sur les cultures voisines."
        resultat['conseils'] = (
            "🛡️ PRÉCAUTIONS À PRENDRE :\n"
            " • Éloignez la culture des zones infectées\n"
            " • Appliquez un traitement préventif\n"
            " • Surveillez l'apparition de symptômes\n"
            " • Évitez l'arrosage par aspersion\n\n"
            f"🌿 Cultures sensibles à proximité : {', '.join(maladies_sensibles)}"
        )
    elif est_incompatible:
        resultat['statut'] = 'deconseille'
        resultat['compatible'] = False
        resultat['sensible'] = False
        resultat['message'] = "❌ DÉCONSEILLÉ ! Cette culture est incompatible avec les cultures voisines."
        resultat['conseils'] = (
            "🚫 ÉVITEZ DE PLANTER ICI :\n"
            " • Les cultures voisines ne s'entendent pas bien\n"
            " • Risque de croissance réduite\n"
            " • Possible transmission de maladies\n\n"
            f"🌿 Cultures incompatibles : {', '.join(incompatibilites)}\n\n"
            f"🌱 Cultures compatibles : {', '.join(compatibilites) if compatibilites else 'Aucune trouvée'}"
        )
    else:
        resultat['statut'] = 'securise'
        resultat['compatible'] = True
        resultat['sensible'] = False
        resultat['message'] = "✅ SÉCURISÉ ! Cette culture est compatible avec les cultures voisines."
        resultat['conseils'] = (
            "🌱 VOUS POUVEZ PLANTER :\n"
            " • Cultures compatibles\n"
            " • Pas de sensibilité à la maladie\n"
            " • Bonne croissance assurée\n\n"
            f"🌿 Cultures voisines : {', '.join(cultures_voisines)}"
        )

    return resultat


@login_required
def verifier_plantation(request):
    """Vue pour vérifier si une culture peut être plantée à proximité"""
    if request.method == 'GET':
        culture_nom = request.GET.get('culture')
        figure_id = request.GET.get('figure_id')
        maladie_nom = request.GET.get('maladie', '')

        if not culture_nom or not figure_id:
            return JsonResponse({
                'success': False,
                'error': 'Paramètres manquants'
            }, status=400)

        resultat = verifier_compatibilite_plantation(
            culture_nom,
            figure_id,
            maladie_nom
        )

        return JsonResponse({
            'success': True,
            'data': resultat
        })


from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()


@login_required
def terminer_tutoriel(request):
    """
    Marque le tutoriel comme terminé et redirige l'utilisateur
    """
    if request.method == 'POST':
        try:
            # ✅ Méthode 1 : update direct
            User.objects.filter(id=request.user.id).update(tutoriel_termine=True)
            request.user.refresh_from_db()
        except Exception as e:
            # ✅ Méthode 2 : mise à jour manuelle via SQL (si la première échoue)
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE vegetables_fruits_customuser SET tutoriel_termine = %s WHERE id = %s",
                    [True, request.user.id]
                )
            request.user.refresh_from_db()

        if 'skip' in request.POST:
            messages.info(request, "💡 Tu peux revoir le tutoriel depuis ton profil si tu le souhaites.")
        else:
            messages.success(request, "🎉 Bienvenue dans Agriculture 2.0 !")

        return redirect('vegetables_fruits:profile')

    return redirect('vegetables_fruits:tutoriel')


# views.py

@login_required
def tutoriel(request):
    """
    Page du tutoriel d'onboarding pour les nouveaux utilisateurs
    """
    user = request.user

    if user.tutoriel_termine:
        messages.info(request, "Tu as déjà terminé le tutoriel !")
        return redirect('vegetables_fruits:profile')

    # ✅ AFFICHAGE SANS birth_date
    context = {
        'est_mineur': False,
        'age_majorite': 18,
        'pays': "France",
        'age': None,
    }

    return render(request, 'vegetables_fruits/tutoriel.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import date, timedelta
from .models import GeometricFigure, Culture, AlerteTraitement, ChronologieCulture, AlerteMeteo, CalendrierUser, \
    Parcelle

@login_required(login_url='vegetables_fruits:login')
def dashboard_particulier(request):
    user = request.user

    # ✅ Si mineur → rediriger vers le bon dashboard junior
    if est_mineur(user):
        # A-t-il un profil élève en classe ?
        if hasattr(user, 'profil_eleve') and user.profil_eleve and user.profil_eleve.classe:
            messages.info(request, "Bienvenue dans ton espace élève !")
            return redirect('vegetables_fruits:dashboard_eleve')
        else:
            # Mineur particulier
            messages.info(request, "Bienvenue en mode Junior !")
            return redirect('vegetables_fruits:dashboard_junior')

    # ✅ 1. STATISTIQUES GÉNÉRALES
    parcelles = GeometricFigure.objects.filter(user=user)
    nb_parcelles = parcelles.count()
    surface_totale = parcelles.aggregate(Sum('surface_hectares'))['surface_hectares__sum'] or 0

    # Cultures actives (crops dans les figures)
    cultures_actives = []
    for figure in parcelles:
        if figure.crops:
            for crop in figure.crops:
                if 'name' in crop:
                    cultures_actives.append(crop['name'])

    nb_cultures_actives = len(set(cultures_actives))

    # Alertes actives
    alertes_actives = AlerteTraitement.objects.filter(
        utilisateur=user,
        statut='en_attente'
    ).count()

    # Récoltes du mois
    today = date.today()
    mois_courant = today.month
    recoltes_mois = ChronologieCulture.objects.filter(
        figure__user=user,
        statut='recolte',
        date_recolte_effective__month=mois_courant
    ).count()

    # ✅ 2. MÉTÉO DU JOUR (première parcelle)
    premiere_parcelle = parcelles.filter(
        adresse_lat__isnull=False,
        adresse_lng__isnull=False
    ).first()

    meteo = get_meteo_for_figure(premiere_parcelle) if premiere_parcelle else None


    # ✅ 3. PROCHAINES ACTIONS
    prochaines_actions = []

    # Prochains semis
    prochains_semis = CalendrierUser.objects.filter(
        utilisateur=user,
        date_semis__gte=date.today()
    ).order_by('date_semis')[:3]

    for semis in prochains_semis:
        prochaines_actions.append({
            'date': semis.date_semis,
            'type': 'semis',
            'titre': f"🌱 Semis de {semis.culture}",
            'parcelle': semis.figure.name if semis.figure else 'Non spécifié'
        })

    # Prochaines récoltes
    prochaines_recoltes = ChronologieCulture.objects.filter(
        figure__user=user,
        statut__in=['seme', 'levee', 'croissance', 'floraison', 'fructification', 'pret'],
        date_recolte_prevue__gte=date.today()
    ).order_by('date_recolte_prevue')[:3]

    for recolte in prochaines_recoltes:
        prochaines_actions.append({
            'date': recolte.date_recolte_prevue,
            'type': 'recolte',
            'titre': f"🍅 Récolte de {recolte.culture_nom}",
            'parcelle': recolte.figure.name
        })

    # Trier par date
    prochaines_actions = sorted(prochaines_actions, key=lambda x: x['date'])[:5]

    # ✅ 4. MES CULTURES (avec progression DYNAMIQUE + état)
    mes_cultures = []
    nb_en_cours = 0
    nb_a_planifier = 0
    nb_recoltees = 0

    for figure in parcelles[:5]:
        if not figure.crops:
            continue

        for crop in figure.crops:
            nom_crop = crop.get('name', '')
            if not nom_crop:
                continue

            # ✅ Chercher la chronologie (SANS filtrer sur le statut)
            chrono = ChronologieCulture.objects.filter(
                figure=figure,
                culture_nom__icontains=nom_crop
            ).order_by('-date_semis').first()

            culture_emoji = crop.get('emoji', '🌱')

            if chrono:
                if chrono.statut == 'recolte':
                    # 🧺 RÉCOLTÉE
                    etat = 'recoltee'
                    progression = 100
                    statut = '🧺 Récoltée'
                    date_recolte = chrono.date_recolte_effective
                    nb_recoltees += 1
                else:
                    # 🟢 EN COURS
                    etat = 'en_cours'
                    progression = chrono.calculer_progression()
                    statut = chrono.get_statut_display()
                    date_recolte = chrono.date_recolte_prevue
                    culture_emoji = chrono.culture_emoji or culture_emoji
                    nb_en_cours += 1
            else:
                # 🟠 NON PLANIFIÉE
                etat = 'non_planifiee'
                progression = 0
                statut = '🟠 Non planifiée'
                date_recolte = None
                nb_a_planifier += 1

            mes_cultures.append({
                'nom': nom_crop,
                'emoji': culture_emoji,
                'parcelle': figure.name,
                'figure_id': figure.id,
                'etat': etat,
                'progression': progression,
                'statut': statut,
                'date_recolte': date_recolte,
                'chrono_id': chrono.id if chrono else None,
            })

    # ✅ Compteur global
    stats_mes_cultures = {
        'total': len(mes_cultures),
        'en_cours': nb_en_cours,
        'a_planifier': nb_a_planifier,
        'recoltees': nb_recoltees,
    }

    # ✅ 5. ALERTES RÉCENTES
    alertes_recentes = AlerteTraitement.objects.filter(
        utilisateur=user,
        statut__in=['en_attente', 'envoyee']
    ).order_by('-date_creation')[:3]

    alertes_meteo = AlerteMeteo.objects.filter(
        utilisateur=user
    ).order_by('-date_declenchement')[:2]

    # ✅ 6. NOTIFICATIONS MODÉRATEUR
    notifications_non_lues = 0
    if request.user.is_moderateur_forum:
        notifications_non_lues = ForumAdulteNotification.objects.filter(
            destinataire=request.user,
            est_lue=False
        ).count()

    # ✅ 7. STATISTIQUES RAPIDES
    stats = {
        'total_parcelles': nb_parcelles,
        'surface_totale': round(surface_totale, 2),
        'cultures_actives': nb_cultures_actives,
        'alertes_actives': alertes_actives,
        'recoltes_mois': recoltes_mois,
    }

    context = {
        'stats': stats,
        'meteo': meteo,
        'prochaines_actions': prochaines_actions,
        'mes_cultures': mes_cultures,
        'alertes_recentes': alertes_recentes,
        'alertes_meteo': alertes_meteo,
        'username': user.username,
        'notifications_non_lues': notifications_non_lues,
        'is_moderateur': user.is_moderateur_forum,
        'stats_mes_cultures': stats_mes_cultures,
    }

    return render(request, 'vegetables_fruits/dashboard_particulier.html', context)

@login_required
def planifier_culture(request, figure_id):
    """
    Crée une ChronologieCulture pour un crop existant d'une figure.
    Utilise la durée de cycle depuis Culture/Fruit/Vegetable si dispo,
    sinon fallback 90 jours.
    """
    from datetime import datetime, timedelta
    from .models import Culture, Fruit, Vegetable

    if request.method != 'POST':
        return redirect('vegetables_fruits:figure_detail', figure_id=figure_id)

    figure = get_object_or_404(GeometricFigure, id=figure_id, user=request.user)
    crop_name = (request.POST.get('crop_name') or '').strip()
    date_semis_str = request.POST.get('date_semis')

    # ✅ Validations
    if not crop_name or not date_semis_str:
        messages.error(request, "Date de semis et culture requises.")
        return redirect('vegetables_fruits:figure_detail', figure_id=figure.id)

    try:
        date_semis = datetime.strptime(date_semis_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, "Date invalide.")
        return redirect('vegetables_fruits:figure_detail', figure_id=figure.id)

    # ✅ Vérifier que le crop existe bien dans la figure
    crop_existe = any(c.get('name') == crop_name for c in figure.crops)
    if not crop_existe:
        messages.error(request, f"La culture '{crop_name}' n'est pas sur cette parcelle.")
        return redirect('vegetables_fruits:figure_detail', figure_id=figure.id)

    # ✅ Vérifier qu'il n'y a pas déjà une chronologie active
    deja_planifiee = ChronologieCulture.objects.filter(
        figure=figure,
        culture_nom__icontains=crop_name,
    ).exclude(statut='recolte').exists()

    if deja_planifiee:
        messages.info(request, f"🌱 {crop_name} est déjà planifiée.")
        return redirect('vegetables_fruits:figure_detail', figure_id=figure.id)

    # ✅ Récupérer l'emoji
    emoji = '🌱'
    for c in figure.crops:
        if c.get('name') == crop_name:
            emoji = c.get('emoji', '🌱')
            break

    # ✅ Déterminer la durée de cycle (jours_recolte)
    jours_recolte = None

    # 1. Depuis Culture (le plus fiable)
    culture_obj = Culture.objects.filter(nom__iexact=crop_name).first()
    if culture_obj and culture_obj.jours_pousse:
        jours_recolte = culture_obj.jours_pousse

    # 2. Depuis Fruit
    if not jours_recolte:
        fruit_obj = Fruit.objects.filter(nom__iexact=crop_name).first()
        if fruit_obj and fruit_obj.jours_recolte:
            jours_recolte = fruit_obj.jours_recolte

    # 3. Depuis Vegetable
    if not jours_recolte:
        veg_obj = Vegetable.objects.filter(nom__iexact=crop_name).first()
        if veg_obj and veg_obj.jours_recolte:
            jours_recolte = veg_obj.jours_recolte

    # 4. Fallback
    if not jours_recolte:
        jours_recolte = 90

    # ✅ Créer la chronologie
    chrono = ChronologieCulture.objects.create(
        figure=figure,
        culture_nom=crop_name,
        culture_emoji=emoji,
        date_semis=date_semis,
        date_recolte_prevue=date_semis + timedelta(days=jours_recolte),
    )
    chrono.calculer_progression()

    messages.success(
        request,
        f"🌱 {emoji} {crop_name} planifiée ! Récolte prévue le "
        f"{chrono.date_recolte_prevue.strftime('%d/%m/%Y')}."
    )

    # ✅ Redirection intelligente : d'où vient-on ?
    referer = request.META.get('HTTP_REFERER', '')
    if 'dashboard' in referer:
        return redirect('vegetables_fruits:dashboard_particulier')
    return redirect('vegetables_fruits:figure_detail', figure_id=figure.id)

@login_required
def dashboard_eleve(request):
    user = request.user

    # ✅ Vérifier que l'utilisateur a un profil élève
    if not hasattr(user, 'profil_eleve') or not user.profil_eleve:
        # Si mineur → dashboard junior
        if user.mode_junior:
            messages.info(request, "Bienvenue en mode Junior !")
            return redirect('vegetables_fruits:dashboard_junior')
        # Sinon → dashboard particulier
        messages.warning(request, "Accès réservé aux élèves.")
        return redirect('vegetables_fruits:dashboard_particulier')

    # ✅ Vérifier qu'il est dans une classe
    if not user.profil_eleve.classe:
        if user.mode_junior:
            messages.info(request, "Rejoins une classe pour accéder au dashboard élève.")
            return redirect('vegetables_fruits:dashboard_junior')
        messages.warning(request, "Tu n'es pas dans une classe.")
        return redirect('vegetables_fruits:dashboard_particulier')

    eleve = user.profil_eleve

    # Récupérer les données
    progression = {
        'points': eleve.points,
        'niveau': eleve.niveau,
        'pourcentage': (eleve.points % 100) if eleve.points else 0,
    }

    # Badges récents
    badges = eleve.badges.all()[:4]

    # Missions en cours
    from .models import ProgressionMissionHebdo, MissionHebdomadaire
    missions_en_cours = ProgressionMissionHebdo.objects.filter(
        eleve=eleve,
        est_complete=False
    ).select_related('mission')[:3]

    # Défis de classe
    defis = []
    if eleve.classe:
        from .models import Defi
        defis = Defi.objects.filter(
            classe=eleve.classe,
            statut='actif'
        )[:3]

    # ✅ Parcelles de l'élève
    parcelles = GeometricFigure.objects.filter(user=user)

    # ✅ 4. MES CULTURES (avec progression DYNAMIQUE + état)
    mes_cultures = []
    nb_en_cours = 0
    nb_a_planifier = 0
    nb_recoltees = 0

    for figure in parcelles[:5]:
        if not figure.crops:
            continue

        for crop in figure.crops:
            nom_crop = crop.get('name', '')
            if not nom_crop:
                continue

            # ✅ Chercher la chronologie (SANS filtrer sur le statut)
            chrono = ChronologieCulture.objects.filter(
                figure=figure,
                culture_nom__icontains=nom_crop
            ).order_by('-date_semis').first()

            culture_emoji = crop.get('emoji', '🌱')

            if chrono:
                if chrono.statut == 'recolte':
                    # 🧺 RÉCOLTÉE
                    etat = 'recoltee'
                    progression = 100
                    statut = '🧺 Récoltée'
                    date_recolte = chrono.date_recolte_effective
                    nb_recoltees += 1
                else:
                    # 🟢 EN COURS
                    etat = 'en_cours'
                    progression = chrono.calculer_progression()
                    statut = chrono.get_statut_display()
                    date_recolte = chrono.date_recolte_prevue
                    culture_emoji = chrono.culture_emoji or culture_emoji
                    nb_en_cours += 1
            else:
                # 🟠 NON PLANIFIÉE
                etat = 'non_planifiee'
                progression = 0
                statut = '🟠 Non planifiée'
                date_recolte = None
                nb_a_planifier += 1

            mes_cultures.append({
                'nom': nom_crop,
                'emoji': culture_emoji,
                'parcelle': figure.name,
                'figure_id': figure.id,
                'etat': etat,
                'progression': progression,
                'statut': statut,
                'date_recolte': date_recolte,
                'chrono_id': chrono.id if chrono else None,
            })

    # ✅ Compteur global
    stats_mes_cultures = {
        'total': len(mes_cultures),
        'en_cours': nb_en_cours,
        'a_planifier': nb_a_planifier,
        'recoltees': nb_recoltees,
    }

    context = {
        'eleve': eleve,
        'progression': progression,
        'badges': badges,
        'missions_en_cours': missions_en_cours,
        'defis': defis,
        'parcelles': parcelles[:4],
        'mes_cultures': mes_cultures,
        'classe': eleve.classe,
        'stats_mes_cultures': stats_mes_cultures,
    }

    return render(request, 'vegetables_fruits/dashboard_eleve.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date, timedelta
from calendar import monthcalendar, month_name
from .models import CalendrierUser, ChronologieCulture, AlerteTraitement, GeometricFigure


@login_required
def calendrier_agricole(request, year=None, month=None):
    from datetime import date
    """
    Calendrier agricole interactif
    """
    user = request.user

    # ✅ Redirection vers le calendrier junior si mineur
    if est_mineur(user):
        today = date.today()
        # Utiliser les valeurs fournies ou la date actuelle
        redirect_year = year if year is not None else today.year
        redirect_month = month if month is not None else today.month
        return redirect('vegetables_fruits:calendrier_agricole_junior',
                        year=redirect_year,
                        month=redirect_month)

    # Année et mois
    today = date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month

    # ✅ Récupérer les événements du mois
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)

    evenements = []

    # 1. Semis
    semis = CalendrierUser.objects.filter(
        utilisateur=user,
        date_semis__gte=start_date,
        date_semis__lte=end_date
    )
    for s in semis:
        evenements.append({
            'date': s.date_semis,
            'type': 'semis',
            'titre': f"🌱 Semis de {s.culture}",
            'culture': s.culture,
            'parcelle': s.figure.name if s.figure else 'Non spécifié',
            'parcelle_id': s.figure.id if s.figure else None,
            'emoji': '🌱',
            'couleur': '#28a745',
        })

    # 2. Récoltes
    recoltes = ChronologieCulture.objects.filter(
        figure__user=user,
        date_recolte_prevue__gte=start_date,
        date_recolte_prevue__lte=end_date,
        statut='en_croissance'
    )
    for r in recoltes:
        evenements.append({
            'date': r.date_recolte_prevue,
            'type': 'recolte',
            'titre': f"🍅 Récolte de {r.culture_nom}",
            'culture': r.culture_nom,
            'parcelle': r.figure.name,
            'parcelle_id': r.figure.id,
            'emoji': '🍅',
            'couleur': '#17a2b8',
        })

    # 3. Traitements (alertes)
    traitements = AlerteTraitement.objects.filter(
        utilisateur=user,
        date_creation__gte=start_date,
        date_creation__lte=end_date,
        statut='en_attente'
    )
    for t in traitements:
        evenements.append({
            'date': t.date_creation.date(),
            'type': 'traitement',
            'titre': f"🧪 {t.maladie.nom} - {t.culture.nom}",
            'culture': t.culture.nom,
            'parcelle': t.figure.name,
            'parcelle_id': t.figure.id,
            'emoji': '🧪',
            'couleur': '#dc3545',
        })

    # 4. Irrigation (depuis les rappels)
    from .models import RappelUtilisateur
    irrigations = RappelUtilisateur.objects.filter(
        utilisateur=user,
        type_rappel='arrosage',
        date_prochain_rappel__gte=start_date,
        date_prochain_rappel__lte=end_date,
        actif=True
    )
    for i in irrigations:
        evenements.append({
            'date': i.date_prochain_rappel,
            'type': 'irrigation',
            'titre': f"💧 Arrosage - {i.culture or 'Jardin'}",
            'culture': i.culture or 'Jardin',
            'parcelle': 'Non spécifié',
            'parcelle_id': None,
            'emoji': '💧',
            'couleur': '#ffc107',
        })

    # ✅ Construction du calendrier
    cal = monthcalendar(year, month)
    mois_nom = month_name[month]
    jours_semaine = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

    # Compter les événements par jour
    evenements_par_jour = {}
    for evt in evenements:
        jour = evt['date'].day
        if jour not in evenements_par_jour:
            evenements_par_jour[jour] = []
        evenements_par_jour[jour].append(evt)

    context = {
        'evenements_par_jour': evenements_par_jour,
        'cal': cal,
        'mois_nom': mois_nom,
        'annee': year,
        'mois': month,
        'jours_semaine': jours_semaine,
        'mois_precedent': month - 1 if month > 1 else 12,
        'annee_precedente': year if month > 1 else year - 1,
        'mois_suivant': month + 1 if month < 12 else 1,
        'annee_suivante': year if month < 12 else year + 1,
        'aujourdhui': today.day if today.month == month and today.year == year else None,
        'total_evenements': len(evenements),
    }

    return render(request, 'vegetables_fruits/calendrier_agricole.html', context)


@login_required
def calendrier_agricole_junior(request, year=None, month=None):
    """
    Calendrier agricole adapté pour les mineurs (mode Junior)
    """
    user = request.user

    # Vérifier que l'utilisateur est bien un élève
    if not hasattr(user, 'profil_eleve'):
        messages.warning(request, "Accès réservé aux élèves.")
        return redirect('vegetables_fruits:dashboard_particulier')

    # Année et mois
    today = date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month

    # Récupérer les événements du mois
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)

    evenements = []

    # 1. Semis (uniquement ceux de l'élève)
    semis = CalendrierUser.objects.filter(
        utilisateur=user,
        date_semis__gte=start_date,
        date_semis__lte=end_date
    )
    for s in semis:
        evenements.append({
            'date': s.date_semis,
            'type': 'semis',
            'titre': f"🌱 Semis de {s.culture}",
            'culture': s.culture,
            'parcelle': s.figure.name if s.figure else 'Mon jardin',
            'parcelle_id': s.figure.id if s.figure else None,
            'emoji': '🌱',
            'couleur': '#28a745',
            'points': 10,  # Points gagnés pour un semis
        })

    # 2. Récoltes
    recoltes = ChronologieCulture.objects.filter(
        figure__user=user,
        date_recolte_prevue__gte=start_date,
        date_recolte_prevue__lte=end_date,
        statut='en_croissance'
    )
    for r in recoltes:
        evenements.append({
            'date': r.date_recolte_prevue,
            'type': 'recolte',
            'titre': f"🍅 Récolte de {r.culture_nom}",
            'culture': r.culture_nom,
            'parcelle': r.figure.name,
            'parcelle_id': r.figure.id,
            'emoji': '🍅',
            'couleur': '#17a2b8',
            'points': 20,  # Points gagnés pour une récolte
        })

    # 3. Missions hebdomadaires
    from .models import ProgressionMissionHebdo
    missions = ProgressionMissionHebdo.objects.filter(
        eleve=user.profil_eleve,
        est_complete=False
    ).select_related('mission')

    for m in missions:
        if m.mission.date_fin and m.mission.date_fin >= start_date and m.mission.date_fin <= end_date:
            evenements.append({
                'date': m.mission.date_fin,
                'type': 'mission',
                'titre': f"🎯 {m.mission.titre}",
                'culture': '',
                'parcelle': '',
                'parcelle_id': None,
                'emoji': '🎯',
                'couleur': '#ff6b35',
                'points': m.mission.points_recompense,
            })

    # Construction du calendrier
    cal = monthcalendar(year, month)
    mois_nom = month_name[month]
    jours_semaine = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

    # Compter les événements par jour
    evenements_par_jour = {}
    for evt in evenements:
        jour = evt['date'].day
        if jour not in evenements_par_jour:
            evenements_par_jour[jour] = []
        evenements_par_jour[jour].append(evt)

    # Récupérer les points totaux de l'élève
    eleve = user.profil_eleve
    points_totaux = eleve.points

    context = {
        'evenements_par_jour': evenements_par_jour,
        'cal': cal,
        'mois_nom': mois_nom,
        'annee': year,
        'mois': month,
        'jours_semaine': jours_semaine,
        'mois_precedent': month - 1 if month > 1 else 12,
        'annee_precedente': year if month > 1 else year - 1,
        'mois_suivant': month + 1 if month < 12 else 1,
        'annee_suivante': year if month < 12 else year + 1,
        'aujourdhui': today.day if today.month == month and today.year == year else None,
        'total_evenements': len(evenements),
        'points_totaux': points_totaux,
        'est_junior': True,
    }

    return render(request, 'vegetables_fruits/calendrier_agricole_junior.html', context)


@login_required
def cultures_tabs(request, tab_name):
    """
    Charge le contenu d'un onglet de la page Cultures via AJAX
    """
    user = request.user

    # ✅ Vérification d'accès : Premium, Enseignant OU Élève dans une classe
    est_eleve = hasattr(request.user,'profil_eleve') and request.user.profil_eleve and request.user.profil_eleve.classe is not None

    # 🔒 Définition des restrictions par onglet
    tab_restrictions = {
        'calendrier': {'required': None, 'name': 'Calendrier des semis'},
        'mes-semis': {'required': None, 'name': 'Mes semis'},
        'planification': {'required': 'PREMIUM', 'name': 'Planification des semis'},
    }

    # ✅ Vérification de l'abonnement avec exception pour les élèves en classe
    restriction = tab_restrictions.get(tab_name, {})
    if restriction.get('required'):
        # ✅ Élève en classe → accès autorisé
        if not est_eleve:
            acces, message = verifier_acces_abonnement(user, restriction['required'])
            if not acces:
                return HttpResponse(render_restriction_html(restriction['required'], restriction['name']), status=403)

    # ✅ Récupérer la parcelle sélectionnée
    from .models import GeometricFigure, CalendrierUser, ChronologieCulture, Culture
    parcelle_id = request.GET.get('parcelle_id')
    selected_figure = None
    if parcelle_id:
        try:
            selected_figure = GeometricFigure.objects.get(id=parcelle_id, user=user)
        except GeometricFigure.DoesNotExist:
            pass

    # 🔹 Onglet "calendrier"
    if tab_name == 'calendrier':
        from datetime import date
        import calendar
        from .models import Parcelle, CalendrierSemis

        today = date.today()
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))

        # Récupérer les événements du mois
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

        evenements = []

        # ✅ Récupérer la parcelle sélectionnée
        selected_parcelle = None
        if selected_figure:
            selected_parcelle = Parcelle.objects.filter(figure=selected_figure).first()

        # ✅ Cascade de résolution du calendrier
        from .services import resoudre_calendrier_semis
        calendrier_semaines, region, source = resoudre_calendrier_semis(user, selected_figure)

        # On garde pays et saison pour le contexte du template
        region_info = get_region_utilisateur(user, selected_figure)
        pays = region_info.get('pays', 'France')
        saison = region_info.get('saison', 'printemps')

        logger.info(f"📅 cultures_tabs (calendrier) — region={region} source={source} n={calendrier_semaines.count()}")

        if not calendrier_semaines.exists():
            calendrier_semaines = CalendrierSemis.objects.filter(
                region='tous'
            ).order_by('mois_debut_semis')

        # ✅ Organiser les conseils par mois (gère les intervalles wrap : 11→2)
        from .services import organiser_calendrier_par_mois
        conseils_par_mois = organiser_calendrier_par_mois(calendrier_semaines)

        # Semis
        if selected_figure:
            semis = CalendrierUser.objects.filter(
                utilisateur=user,
                figure=selected_figure,
                date_semis__gte=start_date,
                date_semis__lt=end_date
            ).select_related('figure')
        else:
            semis = CalendrierUser.objects.filter(
                utilisateur=user,
                date_semis__gte=start_date,
                date_semis__lt=end_date
            ).select_related('figure')

        for s in semis:
            evenements.append({
                'date': s.date_semis,
                'type': 'semis',
                'titre': f"🌱 Semis de {s.culture}",
                'culture': s.culture,
                'parcelle': s.figure.name if s.figure else 'Non spécifié',
                'emoji': '🌱',
                'couleur': '#28a745',
            })

        # Récoltes
        if selected_figure:
            recoltes = ChronologieCulture.objects.filter(
                figure=selected_figure,
                date_recolte_prevue__gte=start_date,
                date_recolte_prevue__lt=end_date,
                statut='en_croissance'
            ).select_related('figure')
        else:
            recoltes = ChronologieCulture.objects.filter(
                figure__user=user,
                date_recolte_prevue__gte=start_date,
                date_recolte_prevue__lt=end_date,
                statut='en_croissance'
            ).select_related('figure')

        for r in recoltes:
            evenements.append({
                'date': r.date_recolte_prevue,
                'type': 'recolte',
                'titre': f"🍅 Récolte de {r.culture_nom}",
                'culture': r.culture_nom,
                'parcelle': r.figure.name,
                'emoji': '🍅',
                'couleur': '#17a2b8',
            })

        # ✅ Construire evenements_par_jour
        evenements_par_jour = {}
        for evt in evenements:
            jour = evt['date'].day
            if jour not in evenements_par_jour:
                evenements_par_jour[jour] = []
            evenements_par_jour[jour].append(evt)

        # Construction du calendrier
        cal = calendar.monthcalendar(year, month)
        mois_nom = calendar.month_name[month]
        jours_semaine = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

        context = {
            'evenements': evenements,
            'evenements_par_jour': evenements_par_jour,
            'cal': cal,
            'mois_nom': mois_nom,
            'annee': year,
            'mois': month,
            'jours_semaine': jours_semaine,
            'aujourdhui': today.day if today.month == month and today.year == year else None,
            'selected_figure': selected_figure,
            'selected_parcelle': selected_parcelle,
            'region': region,
            'pays': pays,
            'saison': saison,
            'conseils_par_mois': conseils_par_mois,
            'mois_actuel': today.month,
        }
        return render(request, 'vegetables_fruits/tabs/calendrier_tab.html', context)

    # 🔹 Onglet "mes-semis"
    elif tab_name == 'mes-semis':
        if selected_figure:
            semis = CalendrierUser.objects.filter(
                utilisateur=user,
                figure=selected_figure
            ).order_by('-date_semis')
        else:
            semis = CalendrierUser.objects.filter(
                utilisateur=user
            ).order_by('-date_semis')

        context = {
            'semis': semis,
            'selected_figure': selected_figure,
        }
        return render(request, 'vegetables_fruits/tabs/mes_semis_tab.html', context)

    # 🔹 Onglet "planification"
    elif tab_name == 'planification':
        from datetime import date, timedelta
        from .models import CalendrierUser, ChronologieCulture

        parcelle_id = request.GET.get('parcelle_id')
        selected_figure = None

        if parcelle_id:
            try:
                selected_figure = GeometricFigure.objects.get(id=parcelle_id, user=user)
            except GeometricFigure.DoesNotExist:
                pass

        if not selected_figure:
            selected_figure = GeometricFigure.objects.filter(user=user).first()

        cultures_parcelle = []
        today = date.today()

        if selected_figure and selected_figure.crops:
            for crop in selected_figure.crops:
                nom_culture = crop.get('name') or crop.get('nom')
                if not nom_culture:
                    continue

                culture_obj = Culture.objects.filter(nom__icontains=nom_culture).first()

                # ✅ Récupérer les dates depuis CalendrierUser
                calendrier = CalendrierUser.objects.filter(
                    utilisateur=user,
                    figure=selected_figure,
                    culture__icontains=nom_culture
                ).first()

                # ✅ Récupérer la chronologie si elle existe
                chrono = ChronologieCulture.objects.filter(
                    figure=selected_figure,
                    culture_nom__icontains=nom_culture,
                    statut__in=['seme', 'levee', 'croissance', 'floraison', 'fructification', 'pret']
                ).first()

                # ✅ Récupérer les dates
                date_semis = calendrier.date_semis if calendrier else None
                date_plantation = calendrier.date_plantation if calendrier else None
                jours_pousse = culture_obj.jours_pousse if culture_obj else 60

                # ✅ Calcul de la date de récolte prévue
                date_recolte_prevue = None
                if date_plantation:
                    date_recolte_prevue = date_plantation + timedelta(days=jours_pousse)
                elif date_semis:
                    date_recolte_prevue = date_semis + timedelta(days=jours_pousse)

                # ✅ Calcul de la progression
                if chrono:
                    progression = chrono.calculer_progression()
                    statut = chrono.get_statut_display()
                    date_recolte_prevue = chrono.date_recolte_prevue
                elif date_semis or date_plantation:
                    date_debut = date_plantation if date_plantation else date_semis
                    jours_ecoules = (today - date_debut).days

                    if jours_pousse > 0:
                        progression = min(95, max(0, int((jours_ecoules / jours_pousse) * 100)))
                    else:
                        progression = 0

                    if progression >= 95:
                        statut = 'Prêt à récolter'
                    elif progression >= 60:
                        statut = 'Croissance'
                    elif progression >= 30:
                        statut = 'Levée'
                    else:
                        statut = 'Semé'
                else:
                    progression = 0
                    statut = 'Non planifié'

                culture_data = {
                    'nom': culture_obj.nom if culture_obj else nom_culture,
                    'emoji': crop.get('emoji', '🌱'),
                    'statut': statut,
                    'jours_pousse': jours_pousse,
                    'date_semis': date_semis,
                    'date_plantation': date_plantation,
                    'date_recolte_prevue': date_recolte_prevue,
                    'progression': progression,
                }
                cultures_parcelle.append(culture_data)

        context = {
            'cultures': cultures_parcelle,
            'selected_figure': selected_figure,
            'has_cultures': len(cultures_parcelle) > 0,
            'today': today,
        }
        return render(request, 'vegetables_fruits/tabs/planification_tab.html', context)

    return HttpResponse('<div class="alert alert-danger">Onglet non trouvé</div>', status=404)


@login_required
def cultures(request):
    """
    Page principale "Cultures" avec onglets et sélecteur de parcelle
    """
    user = request.user

    # ✅ Récupérer les parcelles de l'utilisateur
    from .models import GeometricFigure
    figures = GeometricFigure.objects.filter(user=user).order_by('name')

    # ✅ Récupérer la parcelle sélectionnée (via GET)
    parcelle_id = request.GET.get('parcelle_id')
    selected_figure_id = None
    if parcelle_id:
        try:
            figure = figures.get(id=parcelle_id)
            selected_figure_id = figure.id
        except GeometricFigure.DoesNotExist:
            selected_figure_id = None

    context = {
        'figures': figures,
        'selected_figure_id': selected_figure_id,
    }

    return render(request, 'vegetables_fruits/cultures.html', context)


@login_required
def guide_cultures(request):
    """
    Page principale "Guide des cultures" avec onglets
    """
    user = request.user

    # ✅ Récupérer les parcelles de l'utilisateur
    from .models import GeometricFigure
    figures = GeometricFigure.objects.filter(user=user).order_by('name')

    # ✅ Récupérer la parcelle sélectionnée (via GET)
    parcelle_id = request.GET.get('parcelle_id')
    selected_figure_id = None
    if parcelle_id:
        try:
            figure = figures.get(id=parcelle_id)
            selected_figure_id = figure.id
        except GeometricFigure.DoesNotExist:
            selected_figure_id = None

    context = {
        'figures': figures,
        'selected_figure_id': selected_figure_id,
    }

    return render(request, 'vegetables_fruits/guide_cultures.html', context)


@login_required
def guide_tabs(request, tab_name):
    """
    Charge le contenu d'un onglet de la page Guide des cultures via AJAX
    """
    user = request.user

    # ✅ Vérification d'accès : Premium, Enseignant OU Élève dans une classe
    est_eleve = hasattr(request.user,'profil_eleve') and request.user.profil_eleve and request.user.profil_eleve.classe is not None

    # 🔒 Définition des restrictions par onglet
    tab_restrictions = {
        'conseiller-sol': {'required': 'PREMIUM', 'name': 'Conseiller Sol'},
        'fertilisation': {'required': 'PREMIUM', 'name': 'Plan de fertilisation'},
        'compagnonnage': {'required': 'PREMIUM', 'name': 'Compagnonnage'},
        'rotation': {'required': 'PREMIUM', 'name': 'Rotation des cultures'},
    }

    # ✅ Vérification de l'abonnement avec exception pour les élèves en classe
    restriction = tab_restrictions.get(tab_name, {})
    if restriction.get('required'):
        # ✅ Élève en classe → accès autorisé
        if not est_eleve:
            acces, message = verifier_acces_abonnement(user, restriction['required'])
            if not acces:
                return HttpResponse(render_restriction_html(restriction['required'], restriction['name']), status=403)

    # ✅ Récupérer la parcelle sélectionnée
    from .models import GeometricFigure, Parcelle, Culture, RecommandationFertilisation, AssociationCulture, RotationCulture
    from datetime import date

    parcelle_id = request.GET.get('parcelle_id')
    selected_figure = None
    if parcelle_id:
        try:
            selected_figure = GeometricFigure.objects.get(id=parcelle_id, user=user)
        except GeometricFigure.DoesNotExist:
            pass

    # Si aucune parcelle sélectionnée, prendre la première
    if not selected_figure:
        selected_figure = GeometricFigure.objects.filter(user=user).first()

    # 🔹 Onglet "conseiller-sol"
    if tab_name == 'conseiller-sol':
        parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

        # Récupérer les cultures de la parcelle
        cultures_parcelle = []
        if selected_figure and selected_figure.crops:
            for crop in selected_figure.crops:
                if 'name' in crop:
                    cultures_parcelle.append(crop['name'])

        # 🌍 DICTIONNAIRE MONDIAL DES CONSEILS PAR TYPE DE SOL
        conseils_sol = {
            # ==================== ARGILEUX ====================
            'argileux': {
                'default': '🌱 Sol argileux : ajoutez du compost et paillez le sol. Évitez de trop arroser.',
                'tomate': '🍅 Sol argileux : aérez la terre avec du sable pour éviter le pourrissement des racines.',
                'carotte': '🥕 Sol argileux : ajoutez du sable pour que les carottes poussent droites.',
                'salade': '🥬 Sol argileux : paillez pour garder l\'humidité.',
                'pomme de terre': '🥔 Sol argileux : aérez bien la terre, buttez les pieds.',
                'haricot': '🫘 Sol argileux : attention à l\'excès d\'eau, semez sur butte.',
                'courgette': '🥒 Sol argileux : plantez sur butte pour éviter l\'excès d\'eau.',
                'aubergine': '🍆 Sol argileux : ajoutez du sable et du compost.',
                'poivron': '🫑 Sol argileux : aérez la terre avec du sable.',
                'concombre': '🥒 Sol argileux : plantez sur butte.',
                'oignon': '🧅 Sol argileux : ajoutez du sable pour faciliter la croissance.',
                'ail': '🧄 Sol argileux : plantez en butte.',
                'fraise': '🍓 Sol argileux : paillez pour protéger les fruits.',
                'pommier': '🍎 Sol argileux : plantez en terrain bien drainé.',
                'poirier': '🍐 Sol argileux : évitez les excès d\'eau.',
                'vigne': '🍇 Sol argileux : bon pour la vigne, attention à l\'eau stagnante.',
                'tournesol': '🌻 Sol argileux : bon pour le tournesol.',
                'maïs': '🌽 Sol argileux : bon pour le maïs.',
            },

            # ==================== SABLEUX ====================
            'sableux': {
                'default': '🌱 Sol sableux : arrosez plus souvent et ajoutez de la matière organique.',
                'tomate': '🍅 Sol sableux : ajoutez du compost pour retenir l\'eau.',
                'carotte': '🥕 Sol sableux : ajoutez du compost pour éviter que les carottes ne sèchent.',
                'salade': '🥬 Sol sableux : arrosez régulièrement.',
                'pomme de terre': '🥔 Sol sableux : idéal pour les pommes de terre.',
                'haricot': '🫘 Sol sableux : arrosez fréquemment.',
                'courgette': '🥒 Sol sableux : arrosez régulièrement.',
                'aubergine': '🍆 Sol sableux : arrosez fréquemment.',
                'poivron': '🫑 Sol sableux : arrosez régulièrement.',
                'concombre': '🥒 Sol sableux : arrosez fréquemment.',
                'oignon': '🧅 Sol sableux : bon pour l\'oignon.',
                'ail': '🧄 Sol sableux : idéal pour l\'ail.',
                'fraise': '🍓 Sol sableux : paillez pour garder l\'humidité.',
                'pommier': '🍎 Sol sableux : arrosez régulièrement.',
                'poirier': '🍐 Sol sableux : arrosez régulièrement.',
                'vigne': '🍇 Sol sableux : bon pour la vigne.',
                'tournesol': '🌻 Sol sableux : bon pour le tournesol.',
                'maïs': '🌽 Sol sableux : arrosez fréquemment.',
                'melon': '🍈 Sol sableux : excellent, chauffe vite.',
                'pastèque': '🍉 Sol sableux : excellent pour les melons et pastèques.',
                'radis': ' Radis : pousse rapide, arrosez régulièrement.',
                'betterave': ' Betterave : bon pour la betterave.',
                'asperge': ' Asperge : idéal, sol bien drainé.',
            },

            # ==================== LIMONEUX ====================
            'limoneux': {
                'default': '🌱 Sol limoneux : fertile et bien drainé. Ajoutez du compost pour maintenir la fertilité.',
                'tomate': '🍅 Sol limoneux : idéal ! Ajoutez simplement du compost.',
                'carotte': '🥕 Sol limoneux : parfait pour les carottes.',
                'salade': '🥬 Sol limoneux : arrosez modérément.',
                'pomme de terre': '🥔 Sol limoneux : excellent pour les pommes de terre.',
                'haricot': '🫘 Sol limoneux : parfait pour les haricots.',
                'courgette': '🥒 Sol limoneux : idéal, arrosez régulièrement.',
                'aubergine': '🍆 Sol limoneux : très bon, apportez du compost.',
                'poivron': '🫑 Sol limoneux : parfait, attention au vent.',
                'concombre': '🥒 Sol limoneux : excellent pour les concombres.',
                'oignon': '🧅 Sol limoneux : parfait pour l\'oignon.',
                'ail': '🧄 Sol limoneux : excellent pour l\'ail.',
                'fraise': '🍓 Sol limoneux : idéal pour les fraises.',
                'pommier': '🍎 Sol limoneux : excellent pour les pommiers.',
                'poirier': '🍐 Sol limoneux : bon pour les poiriers.',
                'vigne': '🍇 Sol limoneux : bon pour la vigne.',
                'tournesol': '🌻 Sol limoneux : bon pour le tournesol.',
                'maïs': '🌽 Sol limoneux : bon pour le maïs.',
                'melon': '🍈 Sol limoneux : bon pour le melon.',
                'pastèque': '🍉 Sol limoneux : bon pour la pastèque.',
                'radis': ' Radis : pousse rapide, sol frais.',
                'betterave': ' Betterave : bon pour la betterave.',
                'asperge': ' Asperge : bon pour l\'asperge.',
                'chou': '🥬 Chou : bon pour le chou.',
                'brocoli': '🥦 Brocoli : bon pour le brocoli.',
                'épinard': ' Épinard : sol frais, arrosez régulièrement.',
            },

            # ==================== HUMIFÈRE ====================
            'humifère': {
                'default': '🌱 Sol humifère : riche en matière organique. Ajoutez du compost pour maintenir la fertilité.',
                'tomate': '🍅 Sol humifère : excellent pour les tomates.',
                'carotte': '🥕 Sol humifère : idéal pour les carottes.',
                'salade': '🥬 Sol humifère : arrosez modérément.',
                'pomme de terre': '🥔 Sol humifère : excellent pour les pommes de terre.',
                'haricot': '🫘 Sol humifère : bon pour les haricots.',
                'courgette': '🥒 Sol humifère : bon pour les courgettes.',
                'aubergine': '🍆 Sol humifère : excellent pour les aubergines.',
                'poivron': '🫑 Sol humifère : bon pour les poivrons.',
                'fraise': '🍓 Sol humifère : excellent pour les fraises.',
                'pommier': '🍎 Sol humifère : bon pour les pommiers.',
                'poirier': '🍐 Sol humifère : bon pour les poiriers.',
                'vigne': '🍇 Sol humifère : bon pour la vigne.',
                'chou': '🥬 Chou : excellent pour les choux.',
                'brocoli': '🥦 Brocoli : bon pour le brocoli.',
            },

            # ==================== CALCAIRE ====================
            'calcaire': {
                'default': '🌱 Sol calcaire : ajoutez du compost et arrosez régulièrement.',
                'tomate': '🍅 Sol calcaire : ajoutez du compost pour éviter le jaunissement des feuilles.',
                'carotte': '🥕 Sol calcaire : ajoutez du compost pour éviter que les carottes ne se déforment.',
                'salade': '🥬 Sol calcaire : arrosez régulièrement.',
                'pomme de terre': '🥔 Sol calcaire : apportez du compost.',
                'haricot': '🫘 Sol calcaire : bon pour les haricots.',
                'courgette': '🥒 Sol calcaire : apportez du compost.',
                'aubergine': '🍆 Sol calcaire : apportez du compost.',
                'poivron': '🫑 Sol calcaire : apportez du compost.',
                'vigne': '🍇 Sol calcaire : idéal pour la vigne !',
                'olivier': '🫒 Sol calcaire : excellent pour l\'olivier.',
                'amandier': '🥜 Sol calcaire : bon pour l\'amandier.',
                'abricotier': '🍑 Sol calcaire : bon pour l\'abricotier.',
                'cerisier': '🍒 Sol calcaire : bon pour le cerisier.',
                'figuier': ' Figuier : bon pour le figuier.',
                'lavande': '🌸 Lavande : idéal pour la lavande.',
                'romarin': '🌿 Romarin : idéal pour le romarin.',
                'thym': '🌿 Thym : idéal pour le thym.',
                'sauge': '🌿 Sauge : bon pour la sauge.',
                'chou': '🥬 Chou : bon pour les choux.',
            },

            # ==================== VOLCANIQUE ====================
            'volcanique': {
                'default': '🌱 Sol volcanique : très fertile, ajoutez du compost pour maintenir la structure.',
                'tomate': '🍅 Sol volcanique : excellent !',
                'pomme de terre': '🥔 Sol volcanique : excellent !',
                'aubergine': '🍆 Sol volcanique : excellent !',
                'poivron': '🫑 Sol volcanique : bon pour les poivrons.',
                'fraise': '🍓 Sol volcanique : excellent pour les fraises.',
                'pommier': '🍎 Sol volcanique : bon pour les pommiers.',
                'poirier': '🍐 Sol volcanique : bon pour les poiriers.',
                'vigne': '🍇 Sol volcanique : excellent pour la vigne !',
                'olivier': '🫒 Sol volcanique : bon pour l\'olivier.',
                'agrumes': '🍊 Agrumes : idéal pour les agrumes.',
            },

            # ==================== TOURBEUX ====================
            'tourbeux': {
                'default': '🌱 Sol tourbeux : acide et humide. Idéal pour les plantes de bruyère.',
                'myrtille': '🫐 Myrtille : idéal pour les myrtilles.',
                'framboise': ' Framboise : bon pour les framboises.',
                'airelle': ' Airelle : idéal pour les airelles.',
                'rhododendron': '🌺 Rhododendron : idéal.',
                'azalée': '🌸 Azalée : idéal.',
                'hortensia': '💐 Hortensia : idéal.',
                'pomme de terre': '🥔 Pomme de terre : acidité moyenne.',
                'fraise': '🍓 Fraise : acidité modérée.',
            },

            # ==================== LATÉRITIQUE ====================
            'lateritique': {
                'default': '🌱 Sol latéritique : riche en fer, pauvre en nutriments. Ajoutez beaucoup de compost.',
                'manioc': ' Manioc : bon pour le manioc.',
                'igname': ' Igname : bon pour l\'igname.',
                'bananier': '🍌 Bananier : bon pour le bananier.',
                'palmier': '🌴 Palmier : bon pour le palmier.',
                'cacaoyer': '🍫 Cacaoyer : bon pour le cacao.',
                'caféier': '☕ Caféier : bon pour le café.',
                'ananas': '🍍 Ananas : bon pour l\'ananas.',
                'papaye': '🥭 Papaye : bon pour la papaye.',
            },

            # ==================== LOESS ====================
            'loess': {
                'default': '🌱 Sol loess : fertile, bien drainé. Ajoutez du compost régulièrement.',
                'blé': '🌾 Blé : excellent pour les céréales.',
                'orge': '🌾 Orge : bon pour l\'orge.',
                'avoine': '🌾 Avoine : bon pour l\'avoine.',
                'maïs': '🌽 Maïs : bon pour le maïs.',
                'tournesol': '🌻 Tournesol : bon pour le tournesol.',
                'pomme de terre': '🥔 Pomme de terre : bonne pour la pomme de terre.',
                'betterave': ' Betterave : bonne pour la betterave.',
            },

            # ==================== DÉSERTIQUE ====================
            'desertique': {
                'default': '🌱 Sol désertique : pauvre en nutriments. Ajoutez beaucoup de compost et arrosez régulièrement.',
                'dattier': '🌴 Dattier : idéal pour le dattier.',
                'olivier': '🫒 Olivier : bon pour l\'olivier.',
                'amandier': '🥜 Amandier : bon pour l\'amandier.',
                'figuier': ' Figuier : bon pour le figuier.',
                'grenadier': '🫐 Grenadier : bon pour le grenadier.',
                'caroubier': ' Caroubier : bon pour le caroubier.',
            },

            # ==================== STEPPIQUE ====================
            'steppique': {
                'default': '🌱 Sol steppique : sec et pauvre. Ajoutez du compost et paillez.',
                'tournesol': '🌻 Tournesol : bon pour le tournesol.',
                'maïs': '🌽 Maïs : bon pour le maïs.',
                'blé': '🌾 Blé : bon pour les céréales.',
                'orge': '🌾 Orge : bon pour l\'orge.',
                'avoine': '🌾 Avoine : bon pour l\'avoine.',
            },

            # ==================== ALLUVIAL ====================
            'alluvial': {
                'default': '🌱 Sol alluvial : très fertile, idéal pour les cultures intensives.',
                'riz': '🍚 Riz : idéal pour le riz.',
                'maïs': '🌽 Maïs : excellent pour le maïs.',
                'blé': '🌾 Blé : excellent pour le blé.',
                'orge': '🌾 Orge : bon pour l\'orge.',
                'avoine': '🌾 Avoine : bon pour l\'avoine.',
                'betterave': ' Betterave : bonne pour la betterave.',
                'canne à sucre': '🍬 Canne à sucre : idéal.',
                'coton': ' Coton : bon pour le coton.',
            },

            # ==================== MÉDITERRANÉEN ====================
            'mediterraneen': {
                'default': '🌱 Sol méditerranéen : sec et fertile. Ajoutez du compost et paillez.',
                'olivier': '🫒 Olivier : idéal !',
                'vigne': '🍇 Vigne : excellente !',
                'amandier': '🥜 Amandier : bon pour l\'amandier.',
                'abricotier': '🍑 Abricotier : bon pour l\'abricotier.',
                'figuier': ' Figuier : bon pour le figuier.',
                'grenadier': '🫐 Grenadier : bon pour le grenadier.',
                'lavande': '🌸 Lavande : idéal pour la lavande.',
                'romarin': '🌿 Romarin : idéal pour le romarin.',
                'thym': '🌿 Thym : idéal pour le thym.',
                'sauge': '🌿 Sauge : bon pour la sauge.',
                'tomate': '🍅 Tomate : bonne pour les tomates.',
                'poivron': '🫑 Poivron : bon pour les poivrons.',
                'aubergine': '🍆 Aubergine : bonne pour les aubergines.',
            },
        }

        # Générer les conseils
        conseils = []
        if selected_figure:
            parcelle = Parcelle.objects.filter(figure=selected_figure).first()
            type_sol = parcelle.type_sol if parcelle else 'limoneux'

            # Nettoyer le type de sol
            type_sol = type_sol.lower().strip() if type_sol else 'limoneux'

            for culture in cultures_parcelle:
                culture_lower = culture.lower().strip()

                # Chercher un conseil spécifique
                conseil = conseils_sol.get(type_sol, {}).get(culture_lower, None)

                # Si pas de conseil spécifique, utiliser le conseil par défaut
                if not conseil:
                    conseil = conseils_sol.get(type_sol, {}).get('default', f'🌱 Aucun conseil spécifique pour {culture} sur ce type de sol.')

                conseils.append({
                    'culture': culture,
                    'conseil': conseil,
                })

        context = {
            'parcelles': parcelles,
            'selected_figure': selected_figure,
            'conseils': conseils,
            'cultures_parcelle': cultures_parcelle,
        }
        return render(request, 'vegetables_fruits/tabs/conseiller_sol_tab.html', context)

    # 🔹 Onglet "fertilisation"
    elif tab_name == 'fertilisation':
        from .models import Parcelle, GeometricFigure, RecommandationFertilisation, Variete, Culture
        from datetime import date

        user = request.user
        parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

        # Récupérer la parcelle sélectionnée
        parcelle_id = request.GET.get('parcelle_id')
        selected_figure = None
        if parcelle_id:
            try:
                selected_figure = GeometricFigure.objects.get(id=parcelle_id, user=user)
            except GeometricFigure.DoesNotExist:
                pass

        if not selected_figure:
            selected_figure = GeometricFigure.objects.filter(user=user).first()

        # ✅ Récupérer les cultures (avec remontée à la culture parente)
        cultures_parcelle = []
        if selected_figure and selected_figure.crops:
            for crop in selected_figure.crops:
                nom_culture = crop.get('name') or crop.get('nom')
                if nom_culture:
                    # ✅ Vérifier si c'est une variété → remonter à la culture parente
                    variete = Variete.objects.filter(nom__icontains=nom_culture).first()
                    if variete and variete.culture:
                        nom_culture = variete.culture.nom
                    else:
                        # ✅ Essayer de trouver une culture correspondante
                        culture = Culture.objects.filter(nom__icontains=nom_culture).first()
                        if culture:
                            nom_culture = culture.nom

                    cultures_parcelle.append(nom_culture.lower())

        # Saison actuelle
        mois_actuel = date.today().month
        saison_map = {
            12: 'hiver', 1: 'hiver', 2: 'hiver',
            3: 'printemps', 4: 'printemps', 5: 'printemps',
            6: 'ete', 7: 'ete', 8: 'ete',
            9: 'automne', 10: 'automne', 11: 'automne',
        }
        saison = saison_map.get(mois_actuel, 'printemps')

        # Type de sol
        parcelle = Parcelle.objects.filter(figure=selected_figure).first()
        type_sol = parcelle.type_sol if parcelle else 'limoneux'

        # Récupérer les recommandations
        recommandations = []
        for culture in cultures_parcelle:
            rec = RecommandationFertilisation.objects.filter(
                culture__icontains=culture,
                type_sol__in=[type_sol, 'tous'],
                saison__in=[saison, 'toute']
            ).first()
            if rec:
                recommandations.append({
                    'culture': culture.capitalize(),
                    'engrais': rec.engrais_recommande,
                    'quantite': rec.quantite_recommandee,
                    'frequence': rec.frequence,
                    'conseils': rec.conseils,
                })

        # Statistiques
        stats = {
            'nb_parcelles': parcelles.count(),
            'surface_totale': sum([p.surface_m2 for p in parcelles]),
            'nb_cultures': len(cultures_parcelle),
        }

        context = {
            'parcelles': parcelles,
            'selected_figure': selected_figure,
            'recommandations': recommandations,
            'saison': saison,
            'type_sol': type_sol,
            'stats': stats,
            'cultures_parcelle': cultures_parcelle,
        }
        return render(request, 'vegetables_fruits/tabs/fertilisation_tab.html', context)

    # 🔹 Onglet "compagnonnage"
    elif tab_name == 'compagnonnage':
        # Récupérer les cultures de la parcelle
        cultures_parcelle = []
        if selected_figure and selected_figure.crops:
            for crop in selected_figure.crops:
                if 'name' in crop:
                    cultures_parcelle.append(crop['name'])

        # Récupérer les associations
        associations_result = []
        for culture in cultures_parcelle:
            bonnes = AssociationCulture.objects.filter(
                culture1__icontains=culture,
                type_association='bonne'
            )
            mauvaises = AssociationCulture.objects.filter(
                culture1__icontains=culture,
                type_association='mauvaise'
            )
            associations_result.append({
                'culture': culture,
                'bonnes': list(bonnes),
                'mauvaises': list(mauvaises),
            })

        context = {
            'selected_figure': selected_figure,
            'associations': associations_result,
            'cultures_parcelle': cultures_parcelle,
        }
        return render(request, 'vegetables_fruits/tabs/compagnonnage_tab.html', context)

    # 🔹 Onglet "rotation"
    elif tab_name == 'rotation':
        from .models import GeometricFigure, RotationCulture, Variete, Culture, ChronologieCulture, CalendrierUser
        from datetime import date
        import json
        import os
        import unicodedata
        from django.conf import settings
        from django.core.cache import cache

        user = request.user

        # ✅ Récupérer la parcelle sélectionnée
        parcelle_id = request.GET.get('parcelle_id')
        selected_figure = None
        if parcelle_id:
            try:
                selected_figure = GeometricFigure.objects.get(id=parcelle_id, user=user)
            except GeometricFigure.DoesNotExist:
                pass

        if not selected_figure:
            selected_figure = GeometricFigure.objects.filter(user=user).first()

        # ============================================================
        # ✅ NORMALISATION
        # ============================================================
        def normaliser(texte):
            if not texte:
                return ''
            return unicodedata.normalize('NFKD', texte).encode('ASCII', 'ignore').decode().lower().strip()

        # ============================================================
        # ✅ CHARGEMENT JSON (cache 1h)
        # ============================================================
        def charger_rotations_json():
            cache_key = 'rotations_json_data'
            data = cache.get(cache_key)
            if data:
                return data

            json_path = os.path.join(settings.BASE_DIR, 'vegetables_fruits', 'data', 'rotations.json')

            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                cache.set(cache_key, data, 3600)
                return data
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logger.warning(f"⚠️ Impossible de charger rotations.json : {e}")

                return {'cultures': {}, 'familles': {}}

        rotations_json = charger_rotations_json()

        # ============================================================
        # ✅ CACHE ROTATIONS EN BASE
        # ============================================================
        toutes_rotations = {
            normaliser(r.culture): r
            for r in RotationCulture.objects.all()
        }

        # ============================================================
        # ✅ RÉCUPÉRER LES CULTURES (remontée variété → culture)
        # ============================================================
        cultures_parcelle = []
        cultures_affichees = []

        if selected_figure and selected_figure.crops:
            noms_crops = [c.get('name') or c.get('nom') for c in selected_figure.crops]
            noms_crops = [n for n in noms_crops if n]

            varietes_dict = {
                normaliser(v.nom): v
                for v in Variete.objects.filter(nom__in=noms_crops).select_related('culture')
            }

            cultures_dict = {
                normaliser(c.nom): c
                for c in Culture.objects.filter(nom__in=noms_crops)
            }

            for crop in selected_figure.crops:
                nom_culture = crop.get('name') or crop.get('nom')
                if not nom_culture:
                    continue

                nom_normalise = normaliser(nom_culture)
                nom_parent = nom_culture

                variete = varietes_dict.get(nom_normalise)
                if variete and variete.culture:
                    nom_parent = variete.culture.nom
                else:
                    culture_obj = cultures_dict.get(nom_normalise)
                    if culture_obj:
                        nom_parent = culture_obj.nom

                cultures_parcelle.append(normaliser(nom_parent))
                cultures_affichees.append(nom_parent)

        # ============================================================
        # ✅ DERNIÈRE RÉCOLTE
        # ============================================================
        derniere_recolte = None
        derniere_recolte_rotation = None

        if selected_figure:
            derniere_recolte = ChronologieCulture.objects.filter(
                figure=selected_figure,
                statut='recolte',
                date_recolte_effective__isnull=False
            ).order_by('-date_recolte_effective').first()

            if derniere_recolte:
                nom_normalise = normaliser(derniere_recolte.culture_nom)
                derniere_recolte_rotation = (
                        toutes_rotations.get(nom_normalise) or
                        rotations_json['cultures'].get(nom_normalise)
                )

        # ============================================================
        # ✅ CYCLE ACTUEL
        # ============================================================
        annee_cycle = date.today().year % 4
        noms_annees = ['Année 1', 'Année 2', 'Année 3', 'Année 4']

        # ============================================================
        # ✅ CONFLITS DE FAMILLE
        # ============================================================
        familles_utilisees = {}
        for culture in cultures_parcelle:
            rotation = toutes_rotations.get(culture)
            famille = None

            if rotation:
                famille = rotation.famille
            else:
                json_data = rotations_json['cultures'].get(culture)
                if json_data:
                    famille = json_data.get('famille')

            if famille:
                familles_utilisees.setdefault(famille, []).append(culture)

        conflits = {
            fam: cults for fam, cults in familles_utilisees.items()
            if len(cults) > 1
        }

        # ============================================================
        # ✅ CONSEILS PAR ANNÉE
        # ============================================================
        conseils_par_annee = {
            1: "🌱 1ère année : le sol est prêt, bonne culture !",
            2: "🌿 2ème année : surveillez les maladies, apportez du compost.",
            3: "🌾 3ème année : le sol s'épuise, prévoyez une jachère.",
            4: "✅ 4ème année : rotation terminée, recommencez le cycle !",
        }

        # ============================================================
        # ✅ RECOMMANDATIONS
        # ============================================================
        recommandations = []
        cultures_sans_donnees = []

        for i, culture in enumerate(cultures_parcelle):
            culture_affichee = cultures_affichees[i]
            rotation = toutes_rotations.get(culture)

            if rotation:
                plans = [rotation.annee1, rotation.annee2, rotation.annee3, rotation.annee4]
                recommandations.append({
                    'culture': culture_affichee,
                    'famille': rotation.famille,
                    'plan_annee1': rotation.annee1,
                    'plan_annee2': rotation.annee2,
                    'plan_annee3': rotation.annee3,
                    'plan_annee4': rotation.annee4,
                    'conseils': rotation.conseils,
                    'conseil_annee': conseils_par_annee.get(annee_cycle + 1, rotation.conseils),
                    'recommande': plans[annee_cycle] if annee_cycle < 4 else rotation.annee1,
                    'prochaine_culture': plans[(annee_cycle + 1) % 4] if len(plans) > 1 else None,
                    'source': 'base',
                })
            else:
                json_data = rotations_json['cultures'].get(culture)

                if json_data:
                    plans = json_data.get('plan', ['?', '?', '?', '?'])
                    recommandations.append({
                        'culture': culture_affichee,
                        'famille': json_data.get('famille', 'Inconnue'),
                        'plan_annee1': plans[0] if len(plans) > 0 else '?',
                        'plan_annee2': plans[1] if len(plans) > 1 else '?',
                        'plan_annee3': plans[2] if len(plans) > 2 else '?',
                        'plan_annee4': plans[3] if len(plans) > 3 else '?',
                        'conseils': json_data.get('conseils', ''),
                        'conseil_annee': conseils_par_annee.get(annee_cycle + 1, ''),
                        'recommande': plans[annee_cycle] if annee_cycle < len(plans) else plans[0],
                        'prochaine_culture': plans[(annee_cycle + 1) % len(plans)] if len(plans) > 1 else None,
                        'source': 'json',
                    })
                else:
                    cultures_sans_donnees.append(culture_affichee)

        # ============================================================
        # ✅ HISTORIQUE PAR ANNÉE (basé sur les vraies dates)
        # ============================================================
        historique_annees = [
            {'numero': 1, 'cultures': [], 'est_courante': False},
            {'numero': 2, 'cultures': [], 'est_courante': False},
            {'numero': 3, 'cultures': [], 'est_courante': False},
            {'numero': 4, 'cultures': [], 'est_courante': False},
        ]

        if selected_figure:
            # ✅ Récupérer TOUTES les chronologies de la parcelle
            # avec une date de semis ou de plantation
            chronos = ChronologieCulture.objects.filter(
                figure=selected_figure
            ).exclude(
                culture_nom__isnull=True
            ).exclude(
                culture_nom=''
            ).order_by('date_semis')

            # ✅ Récupérer aussi les semis planifiés (CalendrierUser)
            semis_planifies = CalendrierUser.objects.filter(
                utilisateur=user,
                figure=selected_figure
            ).order_by('date_semis')

            # ✅ Première année de référence = année de la première plantation
            annee_reference = None

            premier_chrono = chronos.first()
            premier_semis = semis_planifies.first()

            if premier_chrono and premier_chrono.date_semis:
                annee_reference = premier_chrono.date_semis.year
            elif premier_semis and premier_semis.date_semis:
                annee_reference = premier_semis.date_semis.year
            else:
                # Fallback : année en cours
                annee_reference = date.today().year

            # ✅ Peupler chaque année
            cultures_vues = set()  # Éviter les doublons

            for chrono in chronos:
                if not chrono.date_semis:
                    continue

                nom_culture = chrono.culture_nom or ''
                if not nom_culture:
                    continue

                # Éviter les doublons
                cle = f"{nom_culture}_{chrono.date_semis.year}"
                if cle in cultures_vues:
                    continue
                cultures_vues.add(cle)

                # Calculer le décalage (0-3)
                decalage = (chrono.date_semis.year - annee_reference) % 4

                historique_annees[decalage]['cultures'].append(nom_culture)

            for semis in semis_planifies:
                if not semis.date_semis:
                    continue

                nom_culture = semis.culture or ''
                if not nom_culture:
                    continue

                cle = f"{nom_culture}_{semis.date_semis.year}"
                if cle in cultures_vues:
                    continue
                cultures_vues.add(cle)

                decalage = (semis.date_semis.year - annee_reference) % 4
                historique_annees[decalage]['cultures'].append(nom_culture)

            # ✅ Marquer l'année courante
            annee_courante = (date.today().year - annee_reference) % 4
            historique_annees[annee_courante]['est_courante'] = True

        # ============================================================
        # ✅ CONTEXTE
        # ============================================================
        context = {
            'selected_figure': selected_figure,
            'recommandations': recommandations,
            'annee_cycle': annee_cycle + 1,
            'noms_annees': noms_annees,
            'cultures_parcelle': cultures_affichees,
            'derniere_recolte': derniere_recolte,
            'derniere_recolte_rotation': derniere_recolte_rotation,
            'conflits': conflits,
            'conseils_par_annee': conseils_par_annee,
            'cultures_sans_donnees': cultures_sans_donnees,
            'historique_annees': historique_annees,
        }
        return render(request, 'vegetables_fruits/tabs/rotation_tab.html', context)

    return HttpResponse('<div class="alert alert-danger">Onglet non trouvé</div>', status=404)


@login_required
def ecologie_tabs(request, tab_name):
    """
    Charge le contenu d'un onglet de la page Écologie via AJAX
    """
    user = request.user

    # ✅ Vérification : Élève dans une classe
    est_eleve = hasattr(user, 'profil_eleve') and user.profil_eleve and user.profil_eleve.classe is not None

    # 🔒 Définition des restrictions par onglet
    tab_restrictions = {
        'bilan-carbone': {'required': 'PREMIUM', 'name': 'Bilan carbone'},
        'autosuffisance': {'required': None, 'name': 'Autosuffisance'},
    }

    # ✅ Vérification de l'abonnement avec exception pour les élèves en classe
    restriction = tab_restrictions.get(tab_name, {})
    if restriction.get('required'):
        # ✅ Élève en classe → accès autorisé
        if not est_eleve:
            acces, message = verifier_acces_abonnement(user, restriction['required'])
            if not acces:
                return HttpResponse(render_restriction_html(restriction['required'], restriction['name']), status=403)

    from .models import GeometricFigure, Parcelle, BilanCarbone, Autosuffisance, ChronologieCulture
    from datetime import date, timedelta

    # Récupérer la parcelle sélectionnée
    parcelle_id = request.GET.get('parcelle_id')
    selected_figure = None
    if parcelle_id:
        try:
            selected_figure = GeometricFigure.objects.get(id=parcelle_id, user=user)
        except GeometricFigure.DoesNotExist:
            pass

    if not selected_figure:
        selected_figure = GeometricFigure.objects.filter(user=user).first()

    # 🔹 Onglet "bilan-carbone"
    if tab_name == 'bilan-carbone':
        parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

        total_emission = 0
        total_sequestration = 0
        total_bilan = 0
        details_parcelles = []
        labels_graphique = []
        data_emission = []
        data_sequestration = []

        for parcelle in parcelles:
            # ✅ Récupérer les cultures depuis la figure
            nb_cultures_parcelle = 0
            if parcelle.figure and parcelle.figure.crops:
                nb_cultures_parcelle = len(parcelle.figure.crops)

            emission = nb_cultures_parcelle * 5.0
            sequestration = parcelle.surface_m2 * 0.2

            # Créer ou mettre à jour le bilan
            bilan, created = BilanCarbone.objects.get_or_create(
                parcelle=parcelle,
                defaults={
                    'emission_co2_kg': emission,
                    'sequestration_co2_kg': sequestration,
                    'bilan_net_kg': sequestration - emission,
                }
            )
            if not created:
                bilan.emission_co2_kg = emission
                bilan.sequestration_co2_kg = sequestration
                bilan.bilan_net_kg = sequestration - emission
                bilan.save()

            total_emission += emission
            total_sequestration += sequestration
            total_bilan += bilan.bilan_net_kg

            labels_graphique.append(parcelle.nom)
            data_emission.append(round(emission, 1))
            data_sequestration.append(round(sequestration, 1))

            details_parcelles.append({
                'parcelle': parcelle,
                'emission': round(emission, 1),
                'sequestration': round(sequestration, 1),
                'bilan': round(bilan.bilan_net_kg, 1),
                'cultures': nb_cultures_parcelle,
            })

        # Statut
        if total_bilan > 0:
            statut = {'icone': '🌱', 'message': 'Votre jardin est un puits de carbone !', 'couleur': 'success'}
        elif total_bilan < 0:
            statut = {'icone': '⚠️', 'message': 'Votre jardin émet plus de CO₂ qu\'il n\'en séquestre.', 'couleur': 'warning'}
        else:
            statut = {'icone': '⚖️', 'message': 'Votre jardin est neutre en carbone.', 'couleur': 'info'}

        context = {
            'details_parcelles': details_parcelles,
            'total_emission': round(total_emission, 1),
            'total_sequestration': round(total_sequestration, 1),
            'total_bilan': round(total_bilan, 1),
            'labels_graphique': labels_graphique,
            'data_emission': data_emission,
            'data_sequestration': data_sequestration,
            'statut': statut,
            'a_acces_bilan_carbone': True,
            'selected_figure': selected_figure,
        }
        return render(request, 'vegetables_fruits/tabs/bilan_carbone_tab.html', context)

    # 🔹 Onglet "autosuffisance"
    elif tab_name == 'autosuffisance':
        # Récupérer ou créer le profil d'autosuffisance
        autosuffisance, created = Autosuffisance.objects.get_or_create(
            utilisateur=user,
            defaults={'besoin_annuel_kg': 200}
        )

        # Calculer les récoltes des 12 derniers mois
        date_limite = date.today() - timedelta(days=365)
        total_kg = 0
        details_recoltes = []

        recoltes = ChronologieCulture.objects.filter(
            figure__user=user,
            statut='recolte',
            date_recolte_effective__gte=date_limite
        )

        poids_estimes = {
            'tomate': 3, 'carotte': 0.5, 'pomme de terre': 1,
            'courgette': 2, 'salade': 0.3, 'fraise': 0.5,
            'poivron': 0.8, 'aubergine': 1, 'concombre': 1.5,
            'haricot': 0.5, 'oignon': 0.2, 'ail': 0.1,
            'betterave': 1, 'radis': 0.1, 'poireau': 0.4,
            'chou': 1.5, 'brocoli': 0.8, 'céleri': 0.8,
            'épinard': 0.3, 'pomme': 2, 'poire': 2,
            'pêche': 1.5, 'abricot': 1.5, 'cerise': 0.5,
        }

        for recolte in recoltes:
            culture = recolte.culture_nom.lower()
            poids = poids_estimes.get(culture, 0.5)
            total_kg += poids
            details_recoltes.append({
                'culture': recolte.culture_nom,
                'emoji': recolte.culture_emoji,
                'poids_estime': poids,
                'date': recolte.date_recolte_effective,
            })

        besoin = autosuffisance.besoin_annuel_kg
        pourcentage = int((total_kg / besoin) * 100) if besoin > 0 else 0
        pourcentage = min(pourcentage, 100)

        # Niveau
        if pourcentage < 25:
            niveau = "🌱 Débutant"
            message = "Continuez, chaque récolte compte !"
            conseil = "Ajoutez plus de légumes feuilles (salades, épinards)."
        elif pourcentage < 50:
            niveau = "🌿 Jardinier en herbe"
            message = "Bon début ! Votre jardin prend forme."
            conseil = "Pensez aux légumes racines (carottes, pommes de terre)."
        elif pourcentage < 75:
            niveau = "🌳 Jardinier confirmé"
            message = "Impressionnant ! Vous êtes sur la bonne voie."
            conseil = "Ajoutez des fruits et des légumes de saison."
        elif pourcentage < 100:
            niveau = "🌸 Expert"
            message = "Félicitations ! Vous produisez presque tout."
            conseil = "Optimisez l'espace avec la rotation des cultures."
        else:
            niveau = "🏆 Maître jardinier"
            message = "Autosuffisant ! Vous êtes un modèle."
            conseil = "Partagez vos surplus avec votre communauté."

        context = {
            'total_kg': round(total_kg, 1),
            'besoin': besoin,
            'pourcentage': pourcentage,
            'niveau': niveau,
            'message': message,
            'conseil': conseil,
            'details_recoltes': details_recoltes[:5],
            'total_recoltes': recoltes.count(),
            'selected_figure': selected_figure,
        }
        return render(request, 'vegetables_fruits/tabs/autosuffisance_tab.html', context)

    return HttpResponse('<div class="alert alert-danger">Onglet non trouvé</div>', status=404)




@login_required
def ecologie(request):
    """
    Page principale "Écologie & Autonomie" avec onglets
    """
    user = request.user

    from .models import GeometricFigure
    figures = GeometricFigure.objects.filter(user=user).order_by('name')

    parcelle_id = request.GET.get('parcelle_id')
    selected_figure_id = None
    if parcelle_id:
        try:
            figure = figures.get(id=parcelle_id)
            selected_figure_id = figure.id
        except GeometricFigure.DoesNotExist:
            selected_figure_id = None

    context = {
        'figures': figures,
        'selected_figure_id': selected_figure_id,
    }

    return render(request, 'vegetables_fruits/ecologie.html', context)


@login_required
def alertes(request):
    """
    Page principale "Alertes" avec onglets
    """
    user = request.user

    from .models import GeometricFigure
    figures = GeometricFigure.objects.filter(user=user).order_by('name')

    parcelle_id = request.GET.get('parcelle_id')
    selected_figure_id = None
    if parcelle_id:
        try:
            figure = figures.get(id=parcelle_id)
            selected_figure_id = figure.id
        except GeometricFigure.DoesNotExist:
            selected_figure_id = None

    context = {
        'figures': figures,
        'selected_figure_id': selected_figure_id,
    }

    return render(request, 'vegetables_fruits/alertes.html', context)


# views.py

@login_required
def alertes_tabs(request, tab_name):
    """
    Charge le contenu d'un onglet de la page Alertes via AJAX
    """
    user = request.user

    # ✅ Vérification : Élève dans une classe
    est_eleve = hasattr(user, 'profil_eleve') and user.profil_eleve and user.profil_eleve.classe is not None

    # 🔒 Définition des restrictions par onglet
    tab_restrictions = {
        'meteo': {'required': None, 'name': 'Alertes météo'},
        'avancees': {'required': 'PREMIUM', 'name': 'Alertes météo avancées'},
        'traitements': {'required': 'PREMIUM', 'name': 'Alertes traitements'},
    }

    # ✅ Vérification de l'abonnement avec exception pour les élèves en classe
    restriction = tab_restrictions.get(tab_name, {})
    if restriction.get('required'):
        # ✅ Élève en classe → accès autorisé
        if not est_eleve:
            acces, message = verifier_acces_abonnement(user, restriction['required'])
            if not acces:
                return HttpResponse(render_restriction_html(restriction['required'], restriction['name']), status=403)

    from .models import GeometricFigure, AlerteMeteo, AlerteTraitement, Parcelle, Culture
    import requests
    from django.conf import settings
    from django.utils import timezone
    from datetime import date, timedelta

    # Récupérer la parcelle sélectionnée
    parcelle_id = request.GET.get('parcelle_id')
    selected_figure = None
    if parcelle_id:
        try:
            selected_figure = GeometricFigure.objects.get(id=parcelle_id, user=user)
        except GeometricFigure.DoesNotExist:
            pass

    if not selected_figure:
        selected_figure = GeometricFigure.objects.filter(user=user).first()

    # 🔹 Onglet "meteo"
    if tab_name == 'meteo':
        alertes = AlerteMeteo.objects.filter(utilisateur=user).order_by('-date_declenchement')

        parcelle_id = request.GET.get('parcelle_id')
        if parcelle_id:
            alertes = alertes.filter(figure_id=parcelle_id)

        alertes = alertes.order_by('-date_declenchement')

        stats = {
            'total': alertes.count(),
            'gel': alertes.filter(type_alerte='gel').count(),
            'canicule': alertes.filter(type_alerte='canicule').count(),
            'non_lues': alertes.filter(statut='en_attente').count(),
        }

        context = {
            'alertes': alertes[:20],
            'stats': stats,
            'selected_figure': selected_figure,
        }
        return render(request, 'vegetables_fruits/tabs/alertes_meteo_tab.html', context)

    # 🔹 Onglet "avancees"
    elif tab_name == 'avancees':
        parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True).select_related('figure')

        parcelle_id = request.GET.get('parcelle_id')
        if parcelle_id:
            parcelles = parcelles.filter(id=parcelle_id)
        SEUILS_DEFAUT = {'gel': 0, 'canicule': 35, 'pluie': 20, 'vent': 50}

        parcelles_meteo = []
        alertes_globales = []

        for parcelle in parcelles:
            meteo_data = None
            alertes_parcelle = []

            if parcelle.figure and parcelle.figure.adresse_lat and parcelle.figure.adresse_lng:
                # ✅ Météo cachée (10 min)
                meteo_data = get_meteo_for_figure(parcelle.figure)

                if meteo_data:
                    temperature = meteo_data['temperature']
                    conditions = meteo_data['conditions']
                    precipitation = meteo_data.get('rain', 0)
                    wind_speed = meteo_data['wind_speed']
                    humidity = meteo_data['humidity']

                    # Récupérer les cultures
                    cultures = []
                    if parcelle.figure and parcelle.figure.crops:
                        for crop in parcelle.figure.crops:
                            if 'name' in crop:
                                cultures.append(crop['name'])

                    if not cultures:
                        cultures = ['Tomate']

                    for culture_nom in cultures:
                        culture = Culture.objects.filter(nom__icontains=culture_nom).first()

                        gel_seuil = culture.temperature_mingel if culture and culture.temperature_mingel is not None else \
                        SEUILS_DEFAUT['gel']
                        canicule_seuil = culture.temperature_max_canicule if culture and culture.temperature_max_canicule is not None else \
                        SEUILS_DEFAUT['canicule']
                        pluie_seuil = culture.precipitation_max if culture and culture.precipitation_max is not None else \
                        SEUILS_DEFAUT['pluie']
                        vent_seuil = culture.vent_max if culture and culture.vent_max is not None else SEUILS_DEFAUT[
                            'vent']

                        if temperature <= gel_seuil:
                            alertes_parcelle.append({'type': 'gel', 'culture': culture_nom,
                                                     'message': f"❄️ Alerte gel ! {culture_nom} ({temperature}°C)"})
                        if temperature >= canicule_seuil:
                            alertes_parcelle.append({'type': 'canicule', 'culture': culture_nom,
                                                     'message': f"🌡️ Alerte canicule ! {culture_nom} ({temperature}°C)"})
                        if precipitation >= pluie_seuil:
                            alertes_parcelle.append({'type': 'pluie', 'culture': culture_nom,
                                                     'message': f"🌧️ Alerte forte pluie ! {culture_nom}"})
                        if wind_speed >= vent_seuil:
                            alertes_parcelle.append({'type': 'vent', 'culture': culture_nom,
                                                     'message': f"💨 Alerte vent fort ! {culture_nom}"})
                        if humidity > 85:
                            alertes_parcelle.append({'type': 'humidite', 'culture': culture_nom,
                                                     'message': f"💧 Alerte humidité élevée ! {culture_nom} ({humidity}%, risque de mildiou)"})

                    # Sauvegarder les alertes
                    for alerte in alertes_parcelle:
                        alerte_existante = AlerteMeteo.objects.filter(
                            utilisateur=user, figure=parcelle.figure, type_alerte=alerte['type'],
                            date_declenchement__date=date.today()
                        ).exists()
                        if not alerte_existante:
                            AlerteMeteo.objects.create(
                                utilisateur=user, figure=parcelle.figure,
                                type_alerte=alerte['type'], message=alerte['message'],
                                temperature=temperature, date_declenchement=timezone.now(), statut='en_attente'
                            )

            parcelles_meteo.append({
                'parcelle': parcelle,
                'meteo': meteo_data,
                'alertes': alertes_parcelle,
                'has_coords': parcelle.figure and parcelle.figure.adresse_lat and parcelle.figure.adresse_lng
            })
            alertes_globales.extend(alertes_parcelle)

        stats = {
            'total_parcelles': parcelles.count(),
            'parcelles_avec_meteo': sum(1 for p in parcelles_meteo if p['meteo'] is not None),
            'alertes_actives': len(alertes_globales),
            'gel': sum(1 for a in alertes_globales if a['type'] == 'gel'),
            'canicule': sum(1 for a in alertes_globales if a['type'] == 'canicule'),
            'pluie': sum(1 for a in alertes_globales if a['type'] == 'pluie'),
            'vent': sum(1 for a in alertes_globales if a['type'] == 'vent'),
            'humidite': sum(1 for a in alertes_globales if a['type'] == 'humidite'),
        }

        context = {
            'parcelles_meteo': parcelles_meteo,
            'alertes_globales': alertes_globales,
            'stats': stats,
            'user_has_parcelles': parcelles.exists(),
            'now': timezone.now(),
            'selected_figure': selected_figure,
        }
        return render(request, 'vegetables_fruits/tabs/alertes_avancees_tab.html', context)

    # 🔹 Onglet "semis"
    elif tab_name == 'semis':
        from .models import AlerteSemis
        from django.utils import timezone

        # Récupérer les alertes semis de l'utilisateur
        alertes_en_attente = AlerteSemis.objects.filter(
            figure__user=user,
            statut='en_attente'
        ).select_related('figure').order_by('date_declenchement')

        if parcelle_id:
            alertes_en_attente = alertes_en_attente.filter(figure_id=parcelle_id)
        alertes_en_attente = alertes_en_attente.select_related('figure').order_by('date_declenchement')

        alertes_envoyees = AlerteSemis.objects.filter(
            figure__user=user,
            statut='envoyee'
        ).select_related('figure').order_by('-date_envoi')

        if parcelle_id:
            alertes_envoyees = alertes_envoyees.filter(figure_id=parcelle_id)
        alertes_envoyees = alertes_envoyees.select_related('figure').order_by('date_declenchement')

        alertes_ignorees = AlerteSemis.objects.filter(
            figure__user=user,
            statut='ignoree'
        ).select_related('figure').order_by('-date_declenchement')

        if parcelle_id:
            alertes_ignorees = alertes_ignorees.filter(figure_id=parcelle_id)
        alertes_ignorees = alertes_ignorees.select_related('figure').order_by('date_declenchement')

        # Marquer urgente / proche pour l'affichage
        maintenant = timezone.now()
        for alerte in alertes_en_attente:
            jours_restants = (alerte.date_declenchement - maintenant).days
            alerte.est_urgente = jours_restants <= 1
            alerte.est_proche = 1 < jours_restants <= 3

        # Stats
        stats = {
            'en_attente': alertes_en_attente.count(),
            'envoyees': alertes_envoyees.count(),
            'ignorees': alertes_ignorees.count(),
            'prochaines': alertes_en_attente.filter(
                date_declenchement__lte=maintenant + timezone.timedelta(days=7)
            ).count(),
        }

        context = {
            'alertes_en_attente': alertes_en_attente,
            'alertes_envoyees': alertes_envoyees,
            'alertes_ignorees': alertes_ignorees,
            'stats': stats,
            'selected_figure': selected_figure,
        }
        return render(request, 'vegetables_fruits/tabs/alertes_semis_tab.html', context)

    # 🔹 Onglet "traitements"
    elif tab_name == 'traitements':
        # 1. On prépare les requêtes de base
        qs_actives = AlerteTraitement.objects.filter(
            utilisateur=user,
            statut__in=['en_attente', 'envoyee']
        )
        qs_traitees = AlerteTraitement.objects.filter(utilisateur=user, statut='traitee')
        qs_ignorees = AlerteTraitement.objects.filter(utilisateur=user, statut='ignoree')

        # 2. ✅ ON FILTRE PAR PARCELLE AVANT DE COMPTER
        if parcelle_id:
            qs_actives = qs_actives.filter(figure_id=parcelle_id)
            qs_traitees = qs_traitees.filter(figure_id=parcelle_id)
            qs_ignorees = qs_ignorees.filter(figure_id=parcelle_id)

        # 3. Pour l'affichage, on a besoin des objets complets
        alertes_actives = qs_actives.select_related('culture', 'maladie', 'figure').order_by('-date_creation')

        # 4. On prépare le dictionnaire des gravités (on utilise qs_actives qui est déjà filtré)
        alertes_par_gravite = {
            'critique': qs_actives.filter(niveau_risque='critique').count(),
            'elevee': qs_actives.filter(niveau_risque='elevee').count(),
            'moyenne': qs_actives.filter(niveau_risque='moyenne').count(),
            'faible': qs_actives.filter(niveau_risque='faible').count(),
        }

        # 5. On renvoie les entiers pour les compteurs, et le QuerySet pour la liste
        context = {
            'alertes_actives': alertes_actives,
            'alertes_traitees': qs_traitees.count(),  # <-- Le fameux .count() conservé !
            'alertes_ignorees': qs_ignorees.count(),  # <-- Le fameux .count() conservé !
            'alertes_par_gravite': alertes_par_gravite,
            'total_alertes': qs_actives.count(),
            'selected_figure': selected_figure,
            'parcelle_id': parcelle_id,
        }
        return render(request, 'vegetables_fruits/tabs/alertes_traitements_tab.html', context)

    return HttpResponse('<div class="alert alert-danger">Onglet non trouvé</div>', status=404)



from django.views.decorators.http import require_POST
from django.http import JsonResponse

@login_required
@require_POST
def api_acquitter_alertes(request, type_onglet):
    """
    Marque toutes les alertes d'un certain type comme traitées/lues.
    """
    user = request.user
    parcelle_id = request.GET.get('parcelle_id')

    try:
        if type_onglet == 'meteo':
            qs = AlerteMeteo.objects.filter(utilisateur=user, statut='en_attente')
            if parcelle_id: qs = qs.filter(figure_id=parcelle_id)
            qs.update(statut='ignoree') # Ou 'envoyee' selon ta logique

        elif type_onglet == 'avancees':
            # Pour les alertes avancées, on acquitte tout ce qui est "en_attente" sur ces parcelles
            qs = AlerteMeteo.objects.filter(utilisateur=user, statut='en_attente')
            if parcelle_id: qs = qs.filter(figure_id=parcelle_id)
            qs.update(statut='ignoree')

        elif type_onglet == 'traitements':
            qs = AlerteTraitement.objects.filter(utilisateur=user, statut__in=['en_attente', 'envoyee'])
            if parcelle_id: qs = qs.filter(figure_id=parcelle_id)
            qs.update(statut='traitee')

        elif type_onglet == 'semis':
            qs = AlerteSemis.objects.filter(figure__user=user, statut='en_attente')
            if parcelle_id: qs = qs.filter(figure_id=parcelle_id)
            qs.update(statut='ignoree') # On ignore celles qu'on n'a pas traitées

        else:
            return JsonResponse({'success': False, 'error': 'Onglet inconnu'}, status=400)

        return JsonResponse({'success': True, 'message': 'Alertes mises à jour'})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# ============================================================
# IMPORTS NÉCESSAIRES
# ============================================================

from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


# ============================================================
# UTILITAIRE : Validation des uploads d'images
# ============================================================
import magic

MIMES_IMAGES_AUTORISES = {
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/webp': 'webp',
    'image/gif': 'gif',
}


def valider_image_upload(fichier, taille_max_mo=5):
    """
    Valide un fichier uploadé comme image.

    Vérifie :
    - La taille (< taille_max_mo Mo)
    - Le MIME réel (magic bytes, pas juste l'extension)
    - L'intégrité via PIL

    Retourne (valide: bool, message: str)
    """
    if not fichier:
        return False, "Aucun fichier fourni"

    # 1. Taille
    if fichier.size > taille_max_mo * 1024 * 1024:
        return False, f"Image trop lourde ({taille_max_mo} Mo max)"

    # 2. MIME réel via magic bytes
    try:
        mime = magic.from_buffer(fichier.read(2048), mime=True)
        fichier.seek(0) # Remettre le curseur
    except Exception as e:
        logger.warning(f"Impossible de détecter le MIME : {e}")
        return False, "Impossible d'analyser le fichier"

    if mime not in MIMES_IMAGES_AUTORISES:
        logger.warning(f"Upload refusé : MIME={mime}")
        return False, f"Format non autorisé : {mime}"

    # 3. Vérification via PIL (au cas où magic se trompe)
    try:
        img = PilImage.open(fichier)
        img.verify()
        fichier.seek(0)
    except Exception:
        return False, "Image corrompue ou invalide"

    return True, ""

# ============================================================
# 1️⃣ VÉRIFICATIONS D'ACCÈS
# ============================================================

def verifier_acces_forum_adulte(user):
    """
    Vérifie si l'utilisateur a accès au forum adulte
    Retourne: (acces: bool, niveau: str, message: str)
    """


    # ❌ Les enseignants et élèves utilisent le forum école
    if user.is_enseignant:
        return False, None, "Vous avez accès au forum école."

    if hasattr(user, 'profil_eleve') and user.profil_eleve.classe:
        return False, None, "Vous avez accès au forum école."

    # ❌ Vérifier si l'utilisateur est suspendu
    if hasattr(user, 'est_suspendu') and user.est_suspendu:
        return False, None, "Votre compte est actuellement suspendu."

    # ✅ Vérifier l'abonnement
    try:
        abonnement = user.abonnement
        if not abonnement.est_actif:
            return False, None, "Votre abonnement n'est plus actif."

        if abonnement.plan.nom == 'PREMIUM':
            return True, 'premium', "Accès complet au forum Premium"
        elif abonnement.plan.nom == 'BASIQUE':
            return True, 'basique', "Accès limité au forum Basique"
        else:
            return False, None, "Le forum est disponible avec les abonnements Basique et Premium."
    except Abonnement.DoesNotExist:
        return False, None, "Le forum est disponible avec les abonnements Basique et Premium."


def verifier_acces_sujet(user, sujet):
    """Vérifie si l'utilisateur peut voir un sujet"""
    if sujet.est_premium and not user.abonnement.plan.nom == 'PREMIUM':
        return False, "Ce sujet est réservé aux Premium"
    return True, ""


def verifier_quota_sujets(user):
    """Vérifie le quota de sujets pour les utilisateurs Basique (5/mois)"""
    from datetime import date
    debut_mois = date.today().replace(day=1)
    nb_sujets_mois = ForumAdulteSujet.objects.filter(
        auteur=user,
        date_creation__gte=debut_mois,
        est_supprime=False
    ).count()
    return nb_sujets_mois < 5


def verifier_quota_messages(user):
    """Vérifie le quota de messages pour les utilisateurs Basique (50/mois)"""
    from datetime import date
    debut_mois = date.today().replace(day=1)
    nb_messages_mois = MessageForumAdulte.objects.filter(
        auteur=user,
        date_creation__gte=debut_mois,
        est_supprime=False
    ).count()
    return nb_messages_mois < 50


# ============================================================
# 2️⃣ PAGE D'ACCUEIL DU FORUM ADULTE
# ============================================================

@login_required(login_url='vegetables_fruits:login')
def forum_adulte_index(request):
    """Page d'accueil du forum adulte"""

    # ✅ 1. Vérifier que l'utilisateur est connecté (déjà fait par @login_required)

    # ✅ 2. Vérifier que ce n'est pas un enseignant
    if request.user.is_enseignant:
        messages.info(request, "Vous avez accès au forum école.")
        return redirect('vegetables_fruits:forum_ecole_index')

    # ✅ 3. Vérifier que ce n'est pas un élève
    if hasattr(request.user, 'profil_eleve') and request.user.profil_eleve:
        messages.info(request, "Vous avez accès au forum école.")
        return redirect('vegetables_fruits:forum_index')

    # ✅ 4. Vérifier que l'utilisateur n'est pas suspendu
    if hasattr(request.user, 'est_suspendu') and request.user.est_suspendu:
        messages.warning(request, "Votre compte est actuellement suspendu.")
        return redirect('vegetables_fruits:profile')

    # ✅ 5. Vérifier l'abonnement
    try:
        abonnement = request.user.abonnement
        if not abonnement.est_actif:
            messages.warning(request, "Votre abonnement n'est plus actif.")
            return redirect('vegetables_fruits:tarification')

        if abonnement.plan.nom == 'PREMIUM':
            niveau = 'premium'
            est_premium = True
        elif abonnement.plan.nom == 'BASIQUE':
            niveau = 'basique'
            est_premium = False
        else:
            messages.warning(request, "Le forum est disponible avec les abonnements Basique et Premium.")
            return redirect('vegetables_fruits:tarification')

    except Abonnement.DoesNotExist:
        messages.warning(request, "Le forum est disponible avec les abonnements Basique et Premium.")
        return redirect('vegetables_fruits:tarification')

    # ✅ 6. Récupérer les catégories
    if niveau == 'premium':
        categories = ForumAdulteCategorie.objects.filter(est_active=True)
    else:
        categories = ForumAdulteCategorie.objects.filter(est_active=True, est_premium=False)

    # ✅ 7. Ajouter les stats à chaque catégorie
    for cat in categories:
        cat.nb_sujets = cat.nb_sujets()
        cat.nb_messages = cat.nb_messages()
        cat.dernier_sujet = cat.dernier_sujet()

    # ✅ 8. Récupérer les sujets
    if niveau == 'premium':
        sujets = ForumAdulteSujet.objects.filter(est_supprime=False)
    else:
        sujets = ForumAdulteSujet.objects.filter(est_supprime=False, est_premium=False)

    # ✅ 9. Derniers sujets actifs
    derniers_sujets = sujets.select_related('auteur', 'categorie').order_by('-date_dernier_message')[:10]

    # ✅ 10. Sujets populaires
    sujets_populaires = sujets.order_by('-nb_votes')[:5]

    # ✅ 11. Sujets épinglés
    sujets_epingles = sujets.filter(est_epingle=True)[:3]

    # ✅ 12. Statistiques
    from django.db.models import Q
    from django.contrib.auth import get_user_model
    User = get_user_model()

    stats = {
        'total_sujets': sujets.count(),
        'total_messages': MessageForumAdulte.objects.filter(
            sujet__in=sujets,
            est_supprime=False
        ).count(),
        'total_utilisateurs': User.objects.filter(
            Q(sujets_adulte__isnull=False) | Q(messages_adulte__isnull=False)
        ).distinct().count(),
        'sujets_aujourdhui': sujets.filter(date_creation__date=timezone.now().date()).count(),
    }

    # ✅ 13. Quota pour les Basique
    from datetime import date
    debut_mois = date.today().replace(day=1)

    quota = {}
    if niveau == 'basique':
        sujets_utilises = ForumAdulteSujet.objects.filter(
            auteur=request.user,
            date_creation__gte=debut_mois,
            est_supprime=False
        ).count()
        messages_utilises = MessageForumAdulte.objects.filter(
            auteur=request.user,
            date_creation__gte=debut_mois,
            est_supprime=False
        ).count()

        quota = {
            'sujets_utilises': sujets_utilises,
            'sujets_max': 5,
            'sujets_restants': max(0, 5 - sujets_utilises),
            'messages_utilises': messages_utilises,
            'messages_max': 50,
            'messages_restants': max(0, 50 - messages_utilises),
            'pourcentage': min(100, int(((sujets_utilises + messages_utilises / 50) / 10) * 100)),
        }

    # ✅ 14. Nombre de notifications non lues
    notifications_non_lues = ForumAdulteNotification.objects.filter(
        destinataire=request.user,
        est_lue=False
    ).count()

    return render(request, 'vegetables_fruits/forum/adulte/index.html', {
        'categories': categories,
        'derniers_sujets': derniers_sujets,
        'sujets_populaires': sujets_populaires,
        'sujets_epingles': sujets_epingles,
        'stats': stats,
        'quota': quota,
        'niveau': niveau,
        'est_premium': est_premium,
        'notifications_non_lues': notifications_non_lues,
    })


def acces_forum_adulte_requis(view_func):
    """Décorateur pour vérifier l'accès au forum adulte"""

    def wrapper(request, *args, **kwargs):
        # Vérifier enseignant
        if request.user.is_enseignant:
            messages.info(request, "Vous avez accès au forum école.")
            return redirect('vegetables_fruits:forum_ecole_index')

        # Vérifier élève
        if hasattr(request.user, 'profil_eleve') and request.user.profil_eleve:
            messages.info(request, "Vous avez accès au forum école.")
            return redirect('vegetables_fruits:forum_ecole_index')

        # Vérifier abonnement
        try:
            abonnement = request.user.abonnement
            if not abonnement.est_actif:
                messages.warning(request, "Votre abonnement n'est plus actif.")
                return redirect('vegetables_fruits:tarification')

            if abonnement.plan.nom not in ['BASIQUE', 'PREMIUM']:
                messages.warning(request, "Le forum est disponible avec les abonnements Basique et Premium.")
                return redirect('vegetables_fruits:tarification')
        except Abonnement.DoesNotExist:
            messages.warning(request, "Le forum est disponible avec les abonnements Basique et Premium.")
            return redirect('vegetables_fruits:tarification')

        return view_func(request, *args, **kwargs)

    return wrapper


# ============================================================
# 3️⃣ AFFICHER UNE CATÉGORIE
# ============================================================

@login_required
def forum_adulte_categorie(request, categorie_id):
    """Liste des sujets d'une catégorie"""
    acces, niveau, message = verifier_acces_forum_adulte(request.user)

    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    categorie = get_object_or_404(ForumAdulteCategorie, id=categorie_id, est_active=True)

    # ✅ Vérifier l'accès à la catégorie Premium
    if categorie.est_premium and niveau != 'premium':
        messages.warning(request, "Cette catégorie est réservée aux utilisateurs Premium.")
        return redirect('vegetables_fruits:forum_adulte_index')

    # ✅ Récupérer les sujets
    if niveau == 'premium':
        sujets = categorie.sujets.filter(est_supprime=False)
    else:
        sujets = categorie.sujets.filter(est_supprime=False, est_premium=False)

    # ✅ Séparer épinglés / normaux
    sujets_epingles = sujets.filter(est_epingle=True)
    sujets_normaux = sujets.filter(est_epingle=False)

    # ✅ Pagination
    paginator = Paginator(sujets_normaux, 20)
    page = request.GET.get('page')
    sujets_page = paginator.get_page(page)

    return render(request, 'vegetables_fruits/forum/adulte/categorie.html', {
        'categorie': categorie,
        'sujets_epingles': sujets_epingles,
        'sujets': sujets_page,
        'niveau': niveau,
        'est_premium': niveau == 'premium',
    })


# ============================================================
# 4️⃣ AFFICHER UN SUJET
# ============================================================

@login_required
def forum_adulte_sujet(request, sujet_id):
    """Affiche un sujet avec ses messages"""
    acces, niveau, message = verifier_acces_forum_adulte(request.user)

    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    sujet = get_object_or_404(ForumAdulteSujet, id=sujet_id, est_supprime=False)

    # ✅ Vérifier l'accès au sujet Premium
    if sujet.est_premium and niveau != 'premium':
        messages.warning(request, "Ce sujet est réservé aux utilisateurs Premium.")
        return redirect('vegetables_fruits:forum_adulte_index')

    # ✅ Incrémenter les vues
    sujet.vues += 1
    sujet.save()

    # ✅ Récupérer les messages (filtrer Premium selon niveau)
    if niveau == 'premium':
        messages_list = sujet.messages.filter(est_supprime=False)
    else:
        messages_list = sujet.messages.filter(est_supprime=False, est_premium=False)

    # ✅ Gestion des réponses
    if request.method == 'POST':
        if sujet.est_ferme:
            messages.error(request, "Ce sujet est fermé.")
            return redirect('vegetables_fruits:forum_adulte_sujet', sujet_id=sujet.id)

        # ✅ Vérifier le quota pour les Basique
        if niveau == 'basique' and not verifier_quota_messages(request.user):
            messages.warning(request,
                             "Vous avez atteint votre limite de 50 messages par mois. Passez à Premium pour des messages illimités !")
            return redirect('vegetables_fruits:forum_adulte_sujet', sujet_id=sujet.id)

        contenu = request.POST.get('contenu')
        est_premium = request.POST.get('est_premium') == 'on' and niveau == 'premium'

        if contenu and len(contenu.strip()) > 0:
            if len(contenu) < 10:
                messages.error(request, "Votre message doit contenir au moins 10 caractères.")
                return redirect('vegetables_fruits:forum_adulte_sujet', sujet_id=sujet.id)

            # ✅ Créer le message
            message_obj = MessageForumAdulte.objects.create(
                sujet=sujet,
                auteur=request.user,
                contenu=contenu,
                est_premium=est_premium
            )

            # ✅ Mettre à jour le sujet
            sujet.date_dernier_message = timezone.now()
            sujet.save()

            # ✅ Mettre à jour les stats de l'utilisateur
            request.user.nb_messages_forum += 1
            request.user.save()

            # ✅ Notification à l'auteur du sujet (sauf si c'est lui qui répond)
            if sujet.auteur != request.user:
                ForumAdulteNotification.objects.create(
                    destinataire=sujet.auteur,
                    expediteur=request.user,
                    type_notification='reponse',
                    message=f"{request.user.username} a répondu à votre sujet '{sujet.titre}'",
                    lien=f"/forum-adulte/sujet/{sujet.id}/#message-{message_obj.id}"
                )

            # ✅ Notification aux autres participants (sauf l'auteur)
            autres_participants = sujet.messages.filter(
                est_supprime=False
            ).exclude(
                auteur=request.user
            ).exclude(
                auteur=sujet.auteur
            ).values_list('auteur', flat=True).distinct()

            for participant_id in autres_participants:
                if participant_id != request.user.id:
                    ForumAdulteNotification.objects.create(
                        destinataire_id=participant_id,
                        expediteur=request.user,
                        type_notification='reponse',
                        message=f"{request.user.username} a répondu au sujet '{sujet.titre}'",
                        lien=f"/forum-adulte/sujet/{sujet.id}/#message-{message_obj.id}"
                    )

            messages.success(request, "Votre réponse a été ajoutée !")
            return redirect('vegetables_fruits:forum_adulte_sujet', sujet_id=sujet.id)
        else:
            messages.error(request, "Veuillez écrire un message.")

    # ✅ Pagination
    paginator = Paginator(messages_list, 20)
    page = request.GET.get('page')
    messages_page = paginator.get_page(page)

    # ✅ Vérifier si l'utilisateur peut voter (Premium uniquement)
    peut_voter = niveau == 'premium'

    # ✅ Vérifier si l'utilisateur a déjà voté sur chaque message
    if peut_voter:
        message_ids = [m.id for m in messages_page]
        votes_existants = ForumAdulteVote.objects.filter(
            utilisateur=request.user,
            message_id__in=message_ids
        ).values_list('message_id', 'type_vote')
        votes_dict = {v[0]: v[1] for v in votes_existants}
    else:
        votes_dict = {}

    return render(request, 'vegetables_fruits/forum/adulte/sujet.html', {
        'sujet': sujet,
        'messages': messages_page,
        'peut_voter': peut_voter,
        'votes_dict': votes_dict,
        'niveau': niveau,
        'est_premium': niveau == 'premium',
        'est_auteur': sujet.auteur == request.user,
    })


# ============================================================
# 5️⃣ CRÉER UN NOUVEAU SUJET
# ============================================================

@login_required
def forum_adulte_nouveau_sujet(request):
    """Créer un nouveau sujet"""
    acces, niveau, message = verifier_acces_forum_adulte(request.user)

    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    # ✅ Récupérer la catégorie pré-sélectionnée
    categorie_id = request.GET.get('categorie')
    categorie_preselect = None

    if categorie_id:
        try:
            categorie_preselect = ForumAdulteCategorie.objects.get(
                id=categorie_id,
                est_active=True
            )
            if categorie_preselect.est_premium and niveau != 'premium':
                messages.warning(request, "Cette catégorie est réservée aux Premium.")
                return redirect('vegetables_fruits:forum_adulte_index')
        except ForumAdulteCategorie.DoesNotExist:
            pass

    # ✅ Récupérer les catégories disponibles
    if niveau == 'premium':
        categories = ForumAdulteCategorie.objects.filter(est_active=True)
    else:
        categories = ForumAdulteCategorie.objects.filter(est_active=True, est_premium=False)

    # ✅ Vérifier le quota
    if niveau == 'basique' and not verifier_quota_sujets(request.user):
        messages.warning(request, "Vous avez atteint votre limite de 5 sujets par mois.")
        return redirect('vegetables_fruits:forum_adulte_index')

    # ✅ DÉCLARATION DE quota - DOIT ÊTRE AVANT LE BLOC POST
    from datetime import date
    debut_mois = date.today().replace(day=1)

    if niveau == 'basique':
        sujets_utilises = ForumAdulteSujet.objects.filter(
            auteur=request.user,
            date_creation__gte=debut_mois,
            est_supprime=False
        ).count()

        quota = {
            'sujets_utilises': sujets_utilises,
            'sujets_max': 5,
            'sujets_restants': max(0, 5 - sujets_utilises),
            'pourcentage': min(100, int((sujets_utilises / 5) * 100)),
        }
    else:
        # ✅ Premium : quota illimité
        quota = {
            'sujets_utilises': '∞',
            'sujets_max': '∞',
            'sujets_restants': '∞',
            'pourcentage': 0,
        }

    # ============================================================ #
    # BLOC POST #
    # ============================================================ #
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')
        categorie_id = request.POST.get('categorie_id')
        est_premium = request.POST.get('est_premium') == 'on' and niveau == 'premium'

        # ✅ VALIDATIONS
        if not titre or len(titre) < 5:
            messages.error(request, "Le titre doit contenir au moins 5 caractères.")
            return render(request, 'vegetables_fruits/forum/adulte/nouveau_sujet.html', {
                'categories': categories,
                'categorie_preselect': categorie_preselect,
                'niveau': niveau,
                'est_premium': niveau == 'premium',
                'quota': quota,  # ✅ quota est maintenant déclaré
            })

        if not contenu or len(contenu) < 20:
            messages.error(request, "Le contenu doit contenir au moins 20 caractères.")
            return render(request, 'vegetables_fruits/forum/adulte/nouveau_sujet.html', {
                'categories': categories,
                'categorie_preselect': categorie_preselect,
                'niveau': niveau,
                'est_premium': niveau == 'premium',
                'quota': quota,  # ✅ quota est maintenant déclaré
            })

        categorie = get_object_or_404(ForumAdulteCategorie, id=categorie_id)

        if categorie.est_premium and niveau != 'premium':
            messages.error(request, "Cette catégorie est réservée aux Premium.")
            return redirect('vegetables_fruits:forum_adulte_index')

        # ✅ Créer le sujet
        sujet = ForumAdulteSujet.objects.create(
            titre=titre,
            contenu=contenu,
            auteur=request.user,
            categorie=categorie,
            est_premium=est_premium
        )

        MessageForumAdulte.objects.create(
            sujet=sujet,
            auteur=request.user,
            contenu=contenu,
            est_premium=est_premium
        )

        request.user.nb_sujets_forum += 1
        request.user.nb_messages_forum += 1
        request.user.save()

        messages.success(request, f"Sujet '{titre}' créé avec succès !")
        return redirect('vegetables_fruits:forum_adulte_sujet', sujet_id=sujet.id)

    # ✅ GET - Afficher le formulaire avec quota
    return render(request, 'vegetables_fruits/forum/adulte/nouveau_sujet.html', {
        'categories': categories,
        'categorie_preselect': categorie_preselect,
        'niveau': niveau,
        'est_premium': niveau == 'premium',
        'quota': quota,
    })

# ============================================================
# 6️⃣ VOTER POUR UN MESSAGE (Premium uniquement)
# ============================================================

@login_required
@require_POST
def forum_adulte_voter(request, message_id):
    """Voter pour un message (Premium uniquement)"""
    acces, niveau, message = verifier_acces_forum_adulte(request.user)

    if niveau != 'premium':
        return JsonResponse({'error': 'Fonctionnalité réservée aux Premium'}, status=403)

    message_obj = get_object_or_404(MessageForumAdulte, id=message_id, est_supprime=False)
    type_vote = request.POST.get('type_vote')  # 'up' ou 'down'

    if type_vote not in ['up', 'down']:
        return JsonResponse({'error': 'Type de vote invalide'}, status=400)

    # ✅ Vérifier que l'utilisateur ne vote pas pour son propre message
    if message_obj.auteur == request.user:
        return JsonResponse({'error': 'Vous ne pouvez pas voter pour votre propre message'}, status=400)

    # ✅ Vérifier si l'utilisateur a déjà voté
    vote_existant = ForumAdulteVote.objects.filter(
        utilisateur=request.user,
        message=message_obj
    ).first()

    if vote_existant:
        if vote_existant.type_vote == type_vote:
            # ❌ Annuler le vote
            vote_existant.delete()
            if type_vote == 'up':
                message_obj.nb_upvotes -= 1
            else:
                message_obj.nb_downvotes -= 1
            message_obj.save()

            # ✅ Mettre à jour le score du sujet
            sujet = message_obj.sujet
            sujet.nb_votes = sujet.messages.aggregate(
                total=Sum('nb_upvotes') - Sum('nb_downvotes')
            )['total'] or 0
            sujet.save()

            return JsonResponse({
                'success': True,
                'action': 'annule',
                'nb_upvotes': message_obj.nb_upvotes,
                'nb_downvotes': message_obj.nb_downvotes,
                'score': message_obj.score(),
                'total_votes': sujet.nb_votes,
            })
        else:
            # 🔄 Changer de vote
            vote_existant.type_vote = type_vote
            vote_existant.save()

            if type_vote == 'up':
                message_obj.nb_upvotes += 1
                message_obj.nb_downvotes -= 1
            else:
                message_obj.nb_downvotes += 1
                message_obj.nb_upvotes -= 1
            message_obj.save()

            sujet = message_obj.sujet
            sujet.nb_votes = sujet.messages.aggregate(
                total=Sum('nb_upvotes') - Sum('nb_downvotes')
            )['total'] or 0
            sujet.save()

            return JsonResponse({
                'success': True,
                'action': 'change',
                'nb_upvotes': message_obj.nb_upvotes,
                'nb_downvotes': message_obj.nb_downvotes,
                'score': message_obj.score(),
                'total_votes': sujet.nb_votes,
            })
    else:
        # ✅ Nouveau vote
        ForumAdulteVote.objects.create(
            utilisateur=request.user,
            message=message_obj,
            type_vote=type_vote
        )

        if type_vote == 'up':
            message_obj.nb_upvotes += 1
        else:
            message_obj.nb_downvotes += 1
        message_obj.save()

        # ✅ Mettre à jour le score du sujet
        sujet = message_obj.sujet
        sujet.nb_votes = sujet.messages.aggregate(
            total=Sum('nb_upvotes') - Sum('nb_downvotes')
        )['total'] or 0
        sujet.save()

        # ✅ Notification à l'auteur du message (sauf si c'est lui qui vote)
        if message_obj.auteur != request.user:
            ForumAdulteNotification.objects.create(
                destinataire=message_obj.auteur,
                expediteur=request.user,
                type_notification='vote',
                message=f"{request.user.username} a voté {type_vote} pour votre message",
                lien=f"/forum-adulte/sujet/{sujet.id}/#message-{message_obj.id}"
            )

        return JsonResponse({
            'success': True,
            'action': 'nouveau',
            'nb_upvotes': message_obj.nb_upvotes,
            'nb_downvotes': message_obj.nb_downvotes,
            'score': message_obj.score(),
            'total_votes': sujet.nb_votes,
        })

    return JsonResponse({'error': 'Erreur'}, status=400)


# ============================================================
# 7️⃣ MARQUER UNE SOLUTION (Premium uniquement)
# ============================================================

@login_required
@require_POST
def forum_adulte_marquer_solution(request, message_id):
    """Marquer un message comme solution (Premium uniquement)"""
    acces, niveau, message = verifier_acces_forum_adulte(request.user)

    if niveau != 'premium':
        messages.warning(request, "Fonctionnalité réservée aux Premium")
        return redirect('vegetables_fruits:forum_adulte_index')

    message_obj = get_object_or_404(MessageForumAdulte, id=message_id, est_supprime=False)
    sujet = message_obj.sujet

    # ✅ Seul l'auteur du sujet peut marquer une solution
    if sujet.auteur != request.user:
        messages.error(request, "Seul l'auteur du sujet peut marquer une solution.")
        return redirect('vegetables_fruits:forum_adulte_sujet', sujet_id=sujet.id)

    # ✅ Désactiver l'ancienne solution
    MessageForumAdulte.objects.filter(sujet=sujet, est_solution=True).update(est_solution=False)

    # ✅ Marquer la nouvelle solution
    message_obj.est_solution = True
    message_obj.save()

    # ✅ Notification à l'auteur du message
    if message_obj.auteur != request.user:
        ForumAdulteNotification.objects.create(
            destinataire=message_obj.auteur,
            expediteur=request.user,
            type_notification='solution',
            message=f"Votre message a été marqué comme solution dans le sujet '{sujet.titre}'",
            lien=f"/forum-adulte/sujet/{sujet.id}/#message-{message_obj.id}"
        )

    messages.success(request, "Solution marquée avec succès !")
    return redirect('vegetables_fruits:forum_adulte_sujet', sujet_id=sujet.id)


# ============================================================
# 8️⃣ NOTIFICATIONS
# ============================================================

@login_required
def forum_adulte_notifications(request):
    """Afficher les notifications"""
    acces, niveau, message = verifier_acces_forum_adulte(request.user)

    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    notifications = ForumAdulteNotification.objects.filter(
        destinataire=request.user
    ).order_by('-date_creation')

    # ✅ Statistiques
    stats = {
        'non_lues': notifications.filter(est_lue=False).count(),
        'total': notifications.count(),
        'recentes': notifications.filter(date_creation__date=timezone.now().date()).count(),
    }

    # ✅ Pagination
    paginator = Paginator(notifications, 30)
    page = request.GET.get('page')
    notifications_page = paginator.get_page(page)

    return render(request, 'vegetables_fruits/forum/adulte/notifications.html', {
        'notifications': notifications_page,
        'stats': stats,
    })


@login_required
@require_POST
def forum_adulte_notification_lue(request, notification_id):
    """Marquer une notification comme lue"""
    notification = get_object_or_404(ForumAdulteNotification, id=notification_id, destinataire=request.user)
    notification.est_lue = True
    notification.save()
    return JsonResponse({'success': True})


@login_required
@require_POST
def forum_adulte_notifications_toutes_lues(request):
    """Marquer toutes les notifications comme lues"""
    ForumAdulteNotification.objects.filter(destinataire=request.user, est_lue=False).update(est_lue=True)
    return JsonResponse({'success': True})


# ============================================================
# 9️⃣ SIGNALEMENTS
# ============================================================

@login_required
def forum_adulte_signalement(request):
    """Formulaire de signalement"""
    if not verifier_acces_forum_adulte(request.user)[0]:
        messages.warning(request, "Accès non autorisé.")
        return redirect('vegetables_fruits:tarification')

    if request.method == 'POST':
        type_contenu = request.POST.get('type_contenu')
        contenu_id = request.POST.get('contenu_id')
        raison = request.POST.get('raison')
        details = request.POST.get('details', '')

        # ✅ VALIDATIONS
        if not raison or len(raison) < 10:
            messages.error(request, "Veuillez décrire le problème en au moins 10 caractères.")
            return redirect('vegetables_fruits:forum_adulte_signalement')

        # ✅ Récupérer le contenu
        if type_contenu == 'sujet':
            cible = get_object_or_404(ForumAdulteSujet, id=contenu_id, est_supprime=False)
            if cible.auteur == request.user:
                messages.error(request, "Vous ne pouvez pas signaler votre propre sujet.")
                return redirect('vegetables_fruits:forum_adulte_sujet', sujet_id=cible.id)
        else:
            cible = get_object_or_404(MessageForumAdulte, id=contenu_id, est_supprime=False)
            if cible.auteur == request.user:
                messages.error(request, "Vous ne pouvez pas signaler votre propre message.")
                return redirect('vegetables_fruits:forum_adulte_sujet', sujet_id=cible.sujet.id)

        # ✅ Vérifier les signalements en double
        signalement_existant = ForumAdulteSignalement.objects.filter(
            signaleur=request.user,
            type_contenu=type_contenu,
            sujet_id=contenu_id if type_contenu == 'sujet' else None,
            message_id=contenu_id if type_contenu == 'message' else None,
            statut__in=['en_attente', 'en_cours']
        ).exists()

        if signalement_existant:
            messages.warning(request, "Vous avez déjà signalé ce contenu. Un modérateur va l'examiner.")
            return redirect('vegetables_fruits:forum_adulte_index')

        # ✅ CRÉER LE SIGNALEMENT
        signalement = ForumAdulteSignalement.objects.create(
            type_contenu=type_contenu,
            sujet=cible if type_contenu == 'sujet' else None,
            message=cible if type_contenu == 'message' else None,
            signaleur=request.user,
            raison=raison,
            details=details,
            statut='en_attente'
        )

        # ✅ NOTIFICATION AUX MODÉRATEURS
        moderateurs = CustomUser.objects.filter(is_moderateur_forum=True)
        for mod in moderateurs:
            ForumAdulteNotification.objects.create(
                destinataire=mod,
                expediteur=request.user,
                type_notification='signalement',
                message=f"Nouveau signalement de {request.user.username} : {raison[:50]}...",
                lien=f"/forum-adulte/moderateur/signalement/{signalement.id}/"
            )

        # ✅ LOG
        logger.info(f"Signalement #{signalement.id} créé par {request.user.username}")

        messages.success(request,
                         "Merci pour votre signalement. Un modérateur va l'examiner dans les plus brefs délais.")
        return redirect('vegetables_fruits:forum_adulte_index')

    # GET - Afficher le formulaire
    sujet_id = request.GET.get('sujet_id')
    message_id = request.GET.get('message_id')

    sujet = None
    message_obj = None
    type_contenu = None
    contenu_id = None

    if sujet_id:
        sujet = get_object_or_404(ForumAdulteSujet, id=sujet_id)
        type_contenu = 'sujet'
        contenu_id = sujet.id
    elif message_id:
        message_obj = get_object_or_404(MessageForumAdulte, id=message_id)
        type_contenu = 'message'
        contenu_id = message_obj.id

    return render(request, 'vegetables_fruits/forum/adulte/signalement.html', {
        'sujet': sujet,
        'message': message_obj,
        'type_contenu': type_contenu,
        'contenu_id': contenu_id,
    })


# ============================================================
# 🔟 MODÉRATION - LISTE DES SIGNALEMENTS
# ============================================================

@login_required
def forum_adulte_moderation_signalements(request):
    """Liste des signalements pour les modérateurs"""
    if not request.user.is_moderateur_forum:
        messages.error(request, "Accès réservé aux modérateurs.")
        return redirect('vegetables_fruits:forum_adulte_index')

    # ✅ Filtrer par statut
    statut = request.GET.get('statut', 'en_attente')

    if statut == 'en_attente':
        signalements = ForumAdulteSignalement.objects.filter(
            statut='en_attente'
        ).order_by('date_signalement')
    elif statut == 'tous':
        signalements = ForumAdulteSignalement.objects.all().order_by('-date_signalement')
    else:
        signalements = ForumAdulteSignalement.objects.filter(
            statut=statut
        ).order_by('-date_signalement')

    # ✅ Statistiques
    stats = {
        'en_attente': ForumAdulteSignalement.objects.filter(statut='en_attente').count(),
        'en_cours': ForumAdulteSignalement.objects.filter(statut='en_cours').count(),
        'traites': ForumAdulteSignalement.objects.filter(statut='traite').count(),
        'refuses': ForumAdulteSignalement.objects.filter(statut='refuse').count(),
        'total': ForumAdulteSignalement.objects.count(),
    }

    return render(request, 'vegetables_fruits/forum/adulte/moderateur/signalements.html', {
        'signalements': signalements,
        'stats': stats,
        'statut_actuel': statut,
    })


@login_required
def forum_adulte_moderation_signalement_detail(request, signalement_id):
    """Détail et traitement d'un signalement"""
    if not request.user.is_moderateur_forum:
        messages.error(request, "Accès réservé aux modérateurs.")
        return redirect('vegetables_fruits:forum_adulte_index')

    signalement = get_object_or_404(ForumAdulteSignalement, id=signalement_id)

    # ✅ Marquer comme "en cours" si en attente
    if signalement.statut == 'en_attente':
        signalement.statut = 'en_cours'
        signalement.save()

    if request.method == 'POST':
        action = request.POST.get('action')
        commentaire = request.POST.get('commentaire', '')
        sanction = request.POST.get('sanction', '')

        # ✅ TRAITER LE SIGNALEMENT
        if action == 'accepter':
            # Supprimer le contenu
            if signalement.sujet:
                signalement.sujet.est_supprime = True
                signalement.sujet.save()

                # Notification à l'auteur
                ForumAdulteNotification.objects.create(
                    destinataire=signalement.sujet.auteur,
                    expediteur=request.user,
                    type_notification='signalement',
                    message=f"Votre sujet '{signalement.sujet.titre}' a été supprimé suite à un signalement.",
                    lien=f"/forum-adulte/"
                )
            elif signalement.message:
                signalement.message.est_supprime = True
                signalement.message.save()

                ForumAdulteNotification.objects.create(
                    destinataire=signalement.message.auteur,
                    expediteur=request.user,
                    type_notification='signalement',
                    message=f"Votre message a été supprimé suite à un signalement.",
                    lien=f"/forum-adulte/sujet/{signalement.message.sujet.id}/"
                )

            signalement.statut = 'traite'
            message_success = "Contenu supprimé avec succès."

        elif action == 'refuser':
            signalement.statut = 'refuse'
            message_success = "Signalement refusé."

        elif action == 'sanctionner':
            # Sanctionner l'utilisateur
            utilisateur = signalement.sujet.auteur if signalement.sujet else signalement.message.auteur
            sanction_type = request.POST.get('sanction_type', 'avertissement')

            if sanction_type == 'avertissement':
                utilisateur.nb_avertissements = getattr(utilisateur, 'nb_avertissements', 0) + 1
                utilisateur.save()
                message_success = f"Avertissement ajouté à {utilisateur.username}"
            elif sanction_type == 'suspension':
                utilisateur.est_suspendu = True
                utilisateur.date_debut_suspension = timezone.now()
                utilisateur.save()
                message_success = f"{utilisateur.username} suspendu."
            elif sanction_type == 'bannissement':
                utilisateur.is_active = False
                utilisateur.save()
                message_success = f"{utilisateur.username} banni définitivement."

            # 🔥 Créer la sanction dans l'historique
            SanctionUtilisateur.objects.create(
                utilisateur=utilisateur,
                moderateur=request.user,
                type_sanction=sanction_type,
                raison=commentaire or signalement.raison,
                signalement=signalement,
                est_actif=True
            )

            signalement.statut = 'traite'

        # ✅ Mettre à jour le signalement
        signalement.moderateur = request.user
        signalement.commentaire_moderation = commentaire
        signalement.date_traitement = timezone.now()
        signalement.save()

        # ✅ NOTIFIER LE SIGNALEUR
        ForumAdulteNotification.objects.create(
            destinataire=signalement.signaleur,
            expediteur=request.user,
            type_notification='signalement',
            message=f"Votre signalement a été traité : {signalement.get_statut_display()}",
            lien=f"/forum-adulte/mon-compte/signalements/"
        )

        messages.success(request, message_success)
        return redirect('vegetables_fruits:forum_adulte_moderation_signalements')

    return render(request, 'vegetables_fruits/forum/adulte/moderateur/signalement_detail.html', {
        'signalement': signalement,
    })


@login_required
def forum_adulte_recherche(request):
    """Recherche de sujets"""
    acces, niveau, message = verifier_acces_forum_adulte(request.user)
    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    query = request.GET.get('q', '').strip()

    if len(query) < 2:
        messages.warning(request, "La recherche doit contenir au moins 2 caractères.")
        return redirect('vegetables_fruits:forum_adulte_index')

    # Recherche dans les titres et contenus
    if niveau == 'premium':
        sujets = ForumAdulteSujet.objects.filter(
            Q(titre__icontains=query) | Q(contenu__icontains=query),
            est_supprime=False
        )
    else:
        sujets = ForumAdulteSujet.objects.filter(
            Q(titre__icontains=query) | Q(contenu__icontains=query),
            est_supprime=False,
            est_premium=False
        )

    # Pagination
    paginator = Paginator(sujets, 20)
    page = request.GET.get('page')
    sujets_page = paginator.get_page(page)

    return render(request, 'vegetables_fruits/forum/adulte/recherche.html', {
        'results': sujets_page,
        'query': query,
        'niveau': niveau,
        'est_premium': niveau == 'premium',
    })


@login_required
def forum_adulte_profil(request, user_id):
    """Profil d'un utilisateur du forum"""
    acces, niveau, message = verifier_acces_forum_adulte(request.user)
    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    profil_user = get_object_or_404(CustomUser, id=user_id)

    # Statistiques
    stats = {
        'sujets': ForumAdulteSujet.objects.filter(auteur=profil_user, est_supprime=False).count(),
        'messages': MessageForumAdulte.objects.filter(auteur=profil_user, est_supprime=False).count(),
        'solutions': MessageForumAdulte.objects.filter(auteur=profil_user, est_solution=True).count(),
        'votes': MessageForumAdulte.objects.filter(auteur=profil_user).aggregate(
            total=Sum('nb_upvotes') + Sum('nb_downvotes')
        )['total'] or 0,
    }

    # Derniers sujets
    derniers_sujets = ForumAdulteSujet.objects.filter(
        auteur=profil_user,
        est_supprime=False
    ).order_by('-date_creation')[:5]

    # Badges
    badges = ForumBadgeUtilisateur.objects.filter(utilisateur=profil_user).select_related('badge')

    return render(request, 'vegetables_fruits/forum/adulte/profil_forum.html', {
        'profil_user': profil_user,
        'stats': stats,
        'derniers_sujets': derniers_sujets,
        'badges': badges,
        'niveau': niveau,
        'est_premium': niveau == 'premium',
    })


@login_required
def forum_adulte_mes_sujets(request):
    """Liste des sujets de l'utilisateur"""
    acces, niveau, message = verifier_acces_forum_adulte(request.user)
    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    statut = request.GET.get('statut', 'tous')

    sujets = ForumAdulteSujet.objects.filter(
        auteur=request.user,
        est_supprime=False
    )

    if statut == 'actifs':
        sujets = sujets.filter(est_ferme=False)
    elif statut == 'fermes':
        sujets = sujets.filter(est_ferme=True)

    paginator = Paginator(sujets, 20)
    page = request.GET.get('page')
    sujets_page = paginator.get_page(page)

    return render(request, 'vegetables_fruits/forum/adulte/mes_sujets.html', {
        'sujets': sujets_page,
        'statut_actuel': statut,
        'niveau': niveau,
        'est_premium': niveau == 'premium',
    })


@login_required
def forum_adulte_mes_messages(request):
    """Liste des messages de l'utilisateur"""
    acces, niveau, message = verifier_acces_forum_adulte(request.user)
    if not acces:
        messages.warning(request, message)
        return redirect('vegetables_fruits:tarification')

    statut = request.GET.get('statut', 'tous')

    messages_list = MessageForumAdulte.objects.filter(
        auteur=request.user,
        est_supprime=False
    ).select_related('sujet')

    if statut == 'solutions':
        messages_list = messages_list.filter(est_solution=True)

    paginator = Paginator(messages_list, 20)
    page = request.GET.get('page')
    messages_page = paginator.get_page(page)

    return render(request, 'vegetables_fruits/forum/adulte/mes_messages.html', {
        'messages': messages_page,
        'statut_actuel': statut,
        'niveau': niveau,
        'est_premium': niveau == 'premium',
    })


@login_required
def forum_adulte_moderation_statistiques(request):
    """Statistiques de modération"""
    if not request.user.is_moderateur_forum:
        messages.error(request, "Accès réservé aux modérateurs.")
        return redirect('vegetables_fruits:forum_adulte_index')

    from datetime import date, timedelta
    debut_mois = date.today().replace(day=1)

    # Statistiques
    stats = {
        'total': ForumAdulteSignalement.objects.count(),
        'en_attente': ForumAdulteSignalement.objects.filter(statut='en_attente').count(),
        'traites_mois': ForumAdulteSignalement.objects.filter(
            statut='traite',
            date_traitement__date__gte=debut_mois
        ).count(),
        'temps_moyen': '12h',  # À calculer avec une requête plus complexe
    }

    # Sanctions récentes
    sanctions = SanctionUtilisateur.objects.all().order_by('-date_debut')[:10]

    return render(request, 'vegetables_fruits/forum/adulte/moderateur/statistiques.html', {
        'stats': stats,
        'sanctions': sanctions,
    })


@login_required
def forum_adulte_moderation_sanctions(request):
    """Liste des sanctions"""
    if not request.user.is_moderateur_forum:
        messages.error(request, "Accès réservé aux modérateurs.")
        return redirect('vegetables_fruits:forum_adulte_index')

    statut = request.GET.get('statut', 'actif')

    if statut == 'actif':
        sanctions = SanctionUtilisateur.objects.filter(est_actif=True)
    elif statut == 'termine':
        sanctions = SanctionUtilisateur.objects.filter(est_actif=False)
    else:
        sanctions = SanctionUtilisateur.objects.all()

    sanctions = sanctions.order_by('-date_debut')

    paginator = Paginator(sanctions, 20)
    page = request.GET.get('page')
    sanctions_page = paginator.get_page(page)

    return render(request, 'vegetables_fruits/forum/adulte/moderateur/sanctions.html', {
        'sanctions': sanctions_page,
        'statut_actuel': statut,
    })





# ============================================================ #
# 1. FONCTIONS UTILITAIRES #
# ============================================================ #

def get_bilan_carbone_data(user):
    """
    Calcule le bilan carbone d'un utilisateur
    Utilisé par dashboard_climat et bilan_carbone
    """
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    total_emission = 0
    total_sequestration = 0
    total_bilan = 0
    details_parcelles = []

    for parcelle in parcelles:
        # Récupérer les cultures depuis la figure
        nb_cultures_parcelle = 0
        if parcelle.figure and parcelle.figure.crops:
            nb_cultures_parcelle = len(parcelle.figure.crops)

        # Calcul simplifié
        emission = nb_cultures_parcelle * 5.0
        sequestration = parcelle.surface_m2 * 0.2

        # Créer ou mettre à jour le bilan
        bilan, created = BilanCarbone.objects.get_or_create(
            parcelle=parcelle,
            defaults={
                'emission_co2_kg': emission,
                'sequestration_co2_kg': sequestration,
                'bilan_net_kg': sequestration - emission,
            }
        )
        if not created:
            bilan.emission_co2_kg = emission
            bilan.sequestration_co2_kg = sequestration
            bilan.bilan_net_kg = sequestration - emission
            bilan.save()

        total_emission += emission
        total_sequestration += sequestration
        total_bilan += bilan.bilan_net_kg

        details_parcelles.append({
            'parcelle': parcelle,
            'emission': round(emission, 1),
            'sequestration': round(sequestration, 1),
            'bilan': round(bilan.bilan_net_kg, 1),
            'cultures': nb_cultures_parcelle,
        })

    return {
        'total_emission': round(total_emission, 1),
        'total_sequestration': round(total_sequestration, 1),
        'total_bilan': round(total_bilan, 1),
        'details_parcelles': details_parcelles,
        'nb_parcelles': parcelles.count(),
    }


def get_autosuffisance_data(user):
    """
    Calcule l'autosuffisance d'un utilisateur
    Utilisé par dashboard_climat et autosuffisance
    """
    autosuffisance, created = Autosuffisance.objects.get_or_create(
        utilisateur=user,
        defaults={'besoin_annuel_kg': 200}
    )

    date_limite = date.today() - timedelta(days=365)
    total_kg = 0
    details_recoltes = []

    recoltes = ChronologieCulture.objects.filter(
        figure__user=user,
        statut='recolte',
        date_recolte_effective__gte=date_limite
    )

    poids_estimes = {
        'tomate': 3, 'carotte': 0.5, 'pomme de terre': 1,
        'courgette': 2, 'salade': 0.3, 'fraise': 0.5,
        'poivron': 0.8, 'aubergine': 1, 'concombre': 1.5,
        'haricot': 0.5, 'oignon': 0.2, 'ail': 0.1,
        'betterave': 1, 'radis': 0.1, 'poireau': 0.4,
        'chou': 1.5, 'brocoli': 0.8, 'céleri': 0.8,
        'épinard': 0.3, 'pomme': 2, 'poire': 2,
        'pêche': 1.5, 'abricot': 1.5, 'cerise': 0.5,
    }

    for recolte in recoltes:
        culture = recolte.culture_nom.lower()
        poids = poids_estimes.get(culture, 0.5)
        total_kg += poids
        details_recoltes.append({
            'culture': recolte.culture_nom,
            'emoji': recolte.culture_emoji,
            'poids': round(poids, 1),
            'date': recolte.date_recolte_effective,
        })

    besoin = autosuffisance.besoin_annuel_kg
    pourcentage = int((total_kg / besoin) * 100) if besoin > 0 else 0
    pourcentage = min(pourcentage, 100)

    return {
        'total_kg': round(total_kg, 1),
        'besoin': besoin,
        'pourcentage': pourcentage,
        'details_recoltes': details_recoltes[:5],
        'total_recoltes': recoltes.count(),
        'niveau': get_autosuffisance_niveau(pourcentage),
    }


def get_besoins_eau_data(user, parcelle_id=None):
    """
    Calcule les besoins en eau d'un utilisateur
    Utilisé par dashboard_climat et besoins_eau
    """
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    if parcelle_id:
        parcelles = parcelles.filter(id=parcelle_id)

    total_besoins = 0
    details_parcelles = []

    for parcelle in parcelles:
        besoins = BesoinsEau.objects.filter(parcelle=parcelle)
        total_parcelle = 0
        cultures_besoins = []

        for besoin in besoins:
            litres_semaine = besoin.besoin_litres_par_m2 * parcelle.surface_m2 * 7
            total_parcelle += litres_semaine
            cultures_besoins.append({
                'culture': besoin.culture,
                'litres_semaine': round(litres_semaine, 1),
                'frequence': besoin.frequence_arrosage_jours,
            })

        total_besoins += total_parcelle
        details_parcelles.append({
            'parcelle': parcelle,
            'total': round(total_parcelle, 1),
            'cultures': cultures_besoins,
        })

    return {
        'total_besoins': round(total_besoins, 1),
        'details_parcelles': details_parcelles,
        'nb_parcelles': parcelles.count(),
    }


def get_meteo_for_figure(figure):
    """
    Récupère la météo pour une figure spécifique
    Utilisé par dashboard_climat et figure_detail
    """
    if not figure or not figure.adresse_lat or not figure.adresse_lng:
        return None

    cache_key = f"meteo_figure_{figure.id}_{figure.adresse_lat}_{figure.adresse_lng}"
    meteo = cache.get(cache_key)

    if not meteo:
        try:
            api_key = settings.OPENWEATHER_API_KEY
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={figure.adresse_lat}&lon={figure.adresse_lng}&units=metric&lang=fr&appid={api_key}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                meteo = {
                    'temperature': round(data['main']['temp'], 1),
                    'conditions': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'rain': data.get('rain', {}).get('1h', 0),
                    'ville': data.get('name', 'Inconnu'),
                }
                cache.set(cache_key, meteo, 600)  # 10 minutes
            else:
                logger.error(f"❌ Erreur météo: {response.status_code}")

                return None
        except Exception as e:
            logger.error(f"❌ Erreur météo: {e}")

            return None

    return meteo


def get_autosuffisance_niveau(pourcentage):
    """Retourne le niveau d'autosuffisance"""
    if pourcentage < 25:
        return {'label': '🌱 Débutant', 'color': '#6c757d', 'message': 'Continuez, chaque récolte compte !'}
    elif pourcentage < 50:
        return {'label': '🌿 Jardinier en herbe', 'color': '#28a745', 'message': 'Bon début ! Votre jardin prend forme.'}
    elif pourcentage < 75:
        return {'label': '🌳 Jardinier confirmé', 'color': '#17a2b8',
                'message': 'Impressionnant ! Vous êtes sur la bonne voie.'}
    elif pourcentage < 100:
        return {'label': '🌸 Expert', 'color': '#ffc107', 'message': 'Félicitations ! Vous produisez presque tout.'}
    else:
        return {'label': '🏆 Maître jardinier', 'color': '#dc3545', 'message': 'Autosuffisant ! Vous êtes un modèle.'}


def get_bilan_status(total_bilan):
    """Retourne le statut du bilan carbone"""
    if total_bilan < -50:
        return {'label': '✅ Puits de carbone', 'color': '#28a745', 'icon': '🌳'}
    elif total_bilan < 0:
        return {'label': '🌱 Bon bilan', 'color': '#17a2b8', 'icon': '🌿'}
    elif total_bilan < 50:
        return {'label': '⚠️ Bilan neutre', 'color': '#ffc107', 'icon': '⚖️'}
    else:
        return {'label': '🔴 Émetteur net', 'color': '#dc3545', 'icon': '🏭'}


def generer_recommandations(user, stats):
    """
    Génère des recommandations personnalisées
    """
    recommendations = []

    # 1. Bilan carbone
    if stats['total_bilan'] < -50:
        recommendations.append({
            'type': 'success',
            'emoji': '🏆',
            'titre': 'Excellent bilan carbone !',
            'message': f'Votre jardin séquestre {abs(round(stats["total_bilan"], 1))} kg CO₂ de plus qu\'il n\'en émet. Continuez !',
        })
    elif stats['total_bilan'] < 0:
        recommendations.append({
            'type': 'info',
            'emoji': '🌱',
            'titre': 'Bon bilan carbone',
            'message': f'Votre jardin séquestre {abs(round(stats["total_bilan"], 1))} kg CO₂. Ajoutez des arbres pour améliorer.',
        })
    elif stats['total_bilan'] > 0:
        recommendations.append({
            'type': 'warning',
            'emoji': '⚠️',
            'titre': 'Bilan carbone à améliorer',
            'message': f'Votre jardin émet {round(stats["total_bilan"], 1)} kg CO₂. Plantez plus de végétaux et réduisez les intrants.',
        })

    # 2. Autosuffisance
    if stats['autosuffisance'] < 25:
        recommendations.append({
            'type': 'info',
            'emoji': '🌱',
            'titre': 'Améliorez votre autosuffisance',
            'message': f'Vous êtes à {stats["autosuffisance"]}% d\'autosuffisance. Ajoutez des légumes faciles (salades, radis).',
        })
    elif stats['autosuffisance'] < 50:
        recommendations.append({
            'type': 'info',
            'emoji': '🌿',
            'titre': 'Bonne progression',
            'message': f'Vous êtes à {stats["autosuffisance"]}%. Continuez avec des légumes racines (carottes, pommes de terre).',
        })
    elif stats['autosuffisance'] >= 75:
        recommendations.append({
            'type': 'success',
            'emoji': '🏆',
            'titre': 'Autonomie alimentaire !',
            'message': f'Félicitations ! Vous êtes à {stats["autosuffisance"]}% d\'autosuffisance.',
        })

    # 3. Eau
    if stats['besoins_eau'] > 1000:
        recommendations.append({
            'type': 'warning',
            'emoji': '💧',
            'titre': 'Optimisez votre consommation d\'eau',
            'message': f'Vous consommez {round(stats["besoins_eau"], 1)} L/semaine. Installez un goutte-à-goutte pour économiser.',
        })

    return recommendations


# ============================================================ #
# 2. VUE PRINCIPALE - DASHBOARD CLIMAT #
# ============================================================ #

@login_required(login_url='vegetables_fruits:login')
def dashboard_climat(request):
    """
    Dashboard Impact Climatique - Vue consolidée
    Regroupe : Bilan carbone, Autosuffisance, Eau, Météo, Recommandations
    Accessible uniquement aux abonnés Premium et Enseignant
    """

    user = request.user

    # ✅ Vérification d'accès : Premium, Enseignant OU Élève dans une classe
    est_eleve = hasattr(user, 'profil_eleve') and user.profil_eleve and user.profil_eleve.classe is not None

    # ✅ 1. VÉRIFICATION ABONNEMENT
    if not est_eleve:
        try:
            abonnement = user.abonnement
            if not abonnement.est_actif:
                messages.warning(request, "Votre abonnement n'est plus actif.")
                return redirect('vegetables_fruits:tarification')

            if abonnement.plan.nom not in ['PREMIUM', 'ENSEIGNANT']:
                messages.warning(request, "Le Dashboard Climat est disponible avec l'abonnement Premium.")
                return redirect('vegetables_fruits:tarification')
        except Abonnement.DoesNotExist:
            messages.warning(request, "Le Dashboard Climat est disponible avec l'abonnement Premium.")
            return redirect('vegetables_fruits:tarification')

    # ✅ 2. VÉRIFICATION PARCELLES
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)
    figures = GeometricFigure.objects.filter(user=user)

    if not parcelles.exists():
        return render(request, 'vegetables_fruits/dashboard_climat.html', {
            'has_parcelles': False,
        })

    # ✅ 3. RÉCUPÉRATION DE LA PARCELLE SÉLECTIONNÉE
    parcelle_id = request.GET.get('parcelle_id')
    selected_parcelle = None
    selected_figure = None

    if parcelle_id:
        try:
            selected_parcelle = parcelles.get(id=parcelle_id)
            selected_figure = selected_parcelle.figure
        except Parcelle.DoesNotExist:
            pass

    if not selected_parcelle:
        selected_parcelle = parcelles.first()
        if selected_parcelle:
            selected_figure = selected_parcelle.figure

    # ✅ 4. RÉCUPÉRATION DES DONNÉES (sans duplication)
    bilan_data = get_bilan_carbone_data(user)
    autosuffisance_data = get_autosuffisance_data(user)
    eau_data = get_besoins_eau_data(user)

    # ✅ 5. MÉTÉO
    meteo = None
    if selected_figure:
        meteo = get_meteo_for_figure(selected_figure)

    # ✅ 6. AGRÉGATION POUR LE DASHBOARD
    stats = {
        'nb_parcelles': parcelles.count(),
        'surface_totale': round(parcelles.aggregate(Sum('surface_m2'))['surface_m2__sum'] or 0, 1),
        'nb_cultures': sum([len(fig.crops) for fig in figures if fig.crops]),
        'total_emission': bilan_data['total_emission'],
        'total_sequestration': bilan_data['total_sequestration'],
        'total_bilan': bilan_data['total_bilan'],
        'autosuffisance': autosuffisance_data['pourcentage'],
        'besoins_eau': eau_data['total_besoins'],
        'total_kg': autosuffisance_data['total_kg'],
        'besoin_annuel': autosuffisance_data['besoin'],
        'total_recoltes': autosuffisance_data['total_recoltes'],
    }

    # ✅ 7. STATUTS
    bilan_status = get_bilan_status(stats['total_bilan'])
    autosuffisance_niveau = autosuffisance_data['niveau']

    # ✅ 8. RECOMMANDATIONS
    recommendations = generer_recommandations(user, stats)

    # ✅ 9. ÉVOLUTION DES ÉMISSIONS (6 derniers mois)
    evolution_emissions = []
    for i in range(5, -1, -1):
        mois_date = date.today() - timedelta(days=30 * i)
        mois_nom = mois_date.strftime('%b').capitalize()

        # Simulation basée sur les données réelles
        base_emission = stats['total_emission'] / 6
        base_sequestration = stats['total_sequestration'] / 6

        evolution_emissions.append({
            'mois': mois_nom,
            'emission': round(base_emission * (0.8 + (i / 10)), 1),
            'sequestration': round(base_sequestration * (0.7 + (i / 12)), 1),
        })

    # ✅ 10. CONTEXTE POUR LE TEMPLATE
    context = {
        'has_parcelles': True,
        'stats': stats,
        'bilan_status': bilan_status,
        'autosuffisance_niveau': autosuffisance_niveau,
        'meteo': meteo,
        'recommandations': recommendations,
        'evolution_emissions': json.dumps(evolution_emissions),
        'details_parcelles': bilan_data['details_parcelles'],
        'details_recoltes': autosuffisance_data['details_recoltes'],
        'besoins_par_parcelle': eau_data['details_parcelles'],
        'parcelles': parcelles,
        'selected_parcelle': selected_parcelle,
        'selected_figure': selected_figure,
        'now': timezone.now(),
    }

    return render(request, 'vegetables_fruits/dashboard_climat.html', context)


# ============================================================ #
# 3. VUE PRÉVISIONS MÉTÉO #
# ============================================================ #

@login_required(login_url='vegetables_fruits:login')
def previsions_meteo(request):
    """
    Prévisions météo sur 7 jours (OpenWeatherMap /forecast)
    Accessible uniquement aux abonnés Premium et Enseignant
    """

    user = request.user
    # ✅ Vérification d'accès : Premium, Enseignant OU Élève dans une classe
    est_eleve = hasattr(user, 'profil_eleve') and user.profil_eleve and user.profil_eleve.classe is not None

    # ✅ 1. VÉRIFICATION ABONNEMENT
    if not est_eleve:
        try:
            abonnement = user.abonnement
            if not abonnement.est_actif or abonnement.plan.nom not in ['PREMIUM', 'ENSEIGNANT']:
                messages.warning(request, "Les prévisions météo sont disponibles avec l'abonnement Premium.")
                return redirect('vegetables_fruits:tarification')
        except Abonnement.DoesNotExist:
            messages.warning(request, "Les prévisions météo sont disponibles avec l'abonnement Premium.")
            return redirect('vegetables_fruits:tarification')

    # ✅ 2. RÉCUPÉRATION DE LA PARCELLE
    parcelles = Parcelle.objects.filter(utilisateur=user, est_active=True)

    if not parcelles.exists():
        return render(request, 'vegetables_fruits/previsions_meteo.html', {
            'has_parcelles': False,
        })

    parcelle_id = request.GET.get('parcelle_id')
    selected_parcelle = None
    selected_figure = None

    if parcelle_id:
        try:
            selected_parcelle = parcelles.get(id=parcelle_id)
            selected_figure = selected_parcelle.figure
        except Parcelle.DoesNotExist:
            pass

    if not selected_parcelle:
        selected_parcelle = parcelles.first()
        if selected_parcelle:
            selected_figure = selected_parcelle.figure

    # ✅ 3. RÉCUPÉRATION DES PRÉVISIONS
    previsions = None
    if selected_figure and selected_figure.adresse_lat and selected_figure.adresse_lng:
        cache_key = f"previsions_meteo_{selected_figure.id}_{selected_figure.adresse_lat}_{selected_figure.adresse_lng}"
        previsions = cache.get(cache_key)

        if not previsions:
            try:
                api_key = settings.OPENWEATHER_API_KEY
                url = f"https://api.openweathermap.org/data/2.5/forecast?lat={selected_figure.adresse_lat}&lon={selected_figure.adresse_lng}&units=metric&lang=fr&appid={api_key}"
                response = requests.get(url, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    previsions = []

                    # Grouper par jour (7 jours)
                    jours_vus = set()
                    for item in data['list']:
                        date_str = item['dt_txt'].split(' ')[0]
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                        if date_str not in jours_vus and len(previsions) < 7:
                            jours_vus.add(date_str)
                            previsions.append({
                                'date': date_obj,
                                'temperature': round(item['main']['temp'], 1),
                                'conditions': item['weather'][0]['description'],
                                'icon': item['weather'][0]['icon'],
                                'humidity': item['main']['humidity'],
                                'wind_speed': round(item['wind']['speed'], 1),
                                'rain': item.get('rain', {}).get('3h', 0),
                            })

                    cache.set(cache_key, previsions, 3600)  # 1 heure
                    logger.info(f"✅ Prévisions récupérées pour {selected_figure.name}")

                else:
                    logger.error(f"❌ Erreur prévisions: {response.status_code}")

            except Exception as e:
                logger.error(f"❌ Erreur prévisions: {e}")


    return render(request, 'vegetables_fruits/previsions_meteo.html', {
        'has_parcelles': True,
        'parcelles': parcelles,
        'selected_parcelle': selected_parcelle,
        'selected_figure': selected_figure,
        'previsions': previsions,
        'now': timezone.now(),
    })


def verifier_empietement(figure, user, geojson_data):
    """Vérifie l'empietement et retourne un message"""

    parcelles_existantes = Parcelle.objects.filter(
        utilisateur=user,
        est_active=True
    ).exclude(figure=figure).select_related('figure')

    if not parcelles_existantes.exists():
        return True, ""

    # ✅ Vérification simplifiée (approximative)
    # On ne fait pas de calcul complexe, on utilise juste le nom
    for parcelle in parcelles_existantes:
        # Ici, une vérification simple par nom ou par zone approximative
        pass

    return True, ""


@login_required
def analyse_connexions(request):
    """Vue d'analyse des connexions (réservée aux admins)"""

    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('vegetables_fruits:index')

    from .models import ConnexionLog, CustomUser
    from django.db.models import Count
    from datetime import timedelta

    # ✅ Utilisateurs avec le plus d'IP différentes
    il_y_a_7j = timezone.now() - timedelta(days=7)

    utilisateurs_suspects = CustomUser.objects.annotate(
        nb_ips=Count('connexions_log__ip', distinct=True),
        nb_appareils=Count('connexions_log__device_id', distinct=True),
        nb_connexions=Count('connexions_log')
    ).filter(
        connexions_log__date_connexion__gte=il_y_a_7j
    ).order_by('-nb_ips')[:20]

    # ✅ Connexions suspectes récentes
    connexions_suspectes = ConnexionLog.objects.filter(
        est_suspect=True
    ).select_related('utilisateur').order_by('-date_connexion')[:50]

    # ✅ Statistiques
    stats = {
        'total_connexions': ConnexionLog.objects.count(),
        'connexions_suspectes': ConnexionLog.objects.filter(est_suspect=True).count(),
        'utilisateurs_actifs': ConnexionLog.objects.filter(
            date_connexion__gte=il_y_a_7j
        ).values('utilisateur').distinct().count(),
    }

    context = {
        'utilisateurs_suspects': utilisateurs_suspects,
        'connexions_suspectes': connexions_suspectes,
        'stats': stats,
    }

    return render(request, 'vegetables_fruits/admin/analyse_connexions.html', context)

def mentions_legales(request):
    """Page des mentions légales"""
    return render(request, 'vegetables_fruits/mentions_legales.html')


def consentement_parental_attente(request):
    """Page d'attente de validation parentale"""
    from .models import ConsentementRGPD

    # ✅ Récupérer le dernier consentement en attente (via session)
    consentement_id = request.session.get('consentement_id')
    consentement = None

    if consentement_id:
        try:
            consentement = ConsentementRGPD.objects.get(id=consentement_id)
        except ConsentementRGPD.DoesNotExist:
            pass

    # ✅ Si pas de consentement dans la session, rediriger
    if not consentement:
        messages.error(request, "❌ Aucune demande de consentement en cours.")
        return redirect('vegetables_fruits:index')

    # ✅ Si le parent a déjà été renseigné
    if request.method == 'POST':
        parent_email = request.POST.get('parent_email', '')

        if not parent_email:
            messages.error(request, "❌ Veuillez saisir l'email de vos parents.")
        else:
            consentement.representant_legal_email = parent_email
            consentement.save()

            # ✅ Envoyer l'email au parent
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                from django.urls import reverse

                lien_validation = request.build_absolute_uri(
                    reverse('vegetables_fruits:valider_consentement_parental', args=[consentement.token_validation])
                )

                logger.debug(f"📧 Tentative d'envoi à : {parent_email}")

                logger.debug(f"🔗 Lien : {lien_validation}")

                logger.debug(f"📤 From : {settings.DEFAULT_FROM_EMAIL}")


                send_mail(
                    subject="🔒 Consentement parental requis - Agriculture 2.0",
                    message=f"""Bonjour,

Votre enfant {consentement.utilisateur.username} souhaite utiliser Agriculture 2.0.

Pour valider son inscription, merci de cliquer sur le lien suivant :
{lien_validation}

Ce lien est valable 7 jours.

À bientôt,
L'équipe Agriculture 2.0""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[parent_email],
                    fail_silently=False,
                )

                logger.info(f"✅ Email envoyé à {parent_email}")

                messages.success(request, f"✅ Un email a été envoyé à {parent_email}.")


            except Exception as e:
                logger.error(f"❌ ERREUR EMAIL : {type(e).__name__} - {e}")

                import traceback
                traceback.print_exc()
                messages.error(request, f"❌ Erreur : {e}")

    return render(request, 'vegetables_fruits/consentement_parental_attente.html', {
        'consentement': consentement,
    })


def valider_consentement_parental(request, token):
    """Page de validation du consentement parental"""
    from .models import ConsentementRGPD

    try:
        consentement = ConsentementRGPD.objects.get(token_validation=token)
    except ConsentementRGPD.DoesNotExist:
        messages.error(request, "❌ Lien de validation invalide ou expiré.")
        return redirect('vegetables_fruits:index')

    if consentement.statut == 'valide':
        messages.info(request, "✅ Ce consentement a déjà été validé.")
        return redirect('vegetables_fruits:index')

    if request.method == 'POST':
        # ✅ Récupérer les informations du parent
        consentement.representant_legal_nom = request.POST.get('parent_nom', '')
        consentement.representant_legal_prenom = request.POST.get('parent_prenom', '')
        consentement.representant_legal_email = request.POST.get('parent_email', '')
        consentement.representant_legal_telephone = request.POST.get('parent_telephone', '')
        consentement.cgu_acceptees = request.POST.get('cgu') == 'on'
        consentement.politique_confidentialite_acceptee = request.POST.get('confidentialite') == 'on'
        consentement.consentement_donnees = request.POST.get('donnees') == 'on'
        consentement.ip_address = get_client_ip(request)
        consentement.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]

        # ✅ Validation
        if not all([
            consentement.representant_legal_nom,
            consentement.representant_legal_prenom,
            consentement.representant_legal_email,
            consentement.cgu_acceptees,
            consentement.politique_confidentialite_acceptee,
            consentement.consentement_donnees,
        ]):
            messages.error(request, "❌ Veuillez remplir tous les champs obligatoires.")
        else:
            consentement.statut = 'valide'
            consentement.date_consentement_parental = timezone.now()
            consentement.save()

            # ✅ Envoyer un email à l'enfant
            try:
                send_mail(
                    subject="✅ Ton compte est activé !",
                    message=f"Bonjour {consentement.utilisateur.username},\n\nTon parent a validé ton inscription à Agriculture 2.0.\n\nTu peux maintenant te connecter !\n\nÀ bientôt,\nL'équipe Agriculture 2.0",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[consentement.utilisateur.email],
                    fail_silently=True,
                )
            except:
                pass

            messages.success(request, "✅ Consentement validé ! Votre enfant peut maintenant se connecter.")
            return redirect('vegetables_fruits:index')

    return render(request, 'vegetables_fruits/valider_consentement_parental.html', {
        'consentement': consentement,
    })


def get_client_ip(request):
    """Récupère l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def dashboard_junior(request):
    """
    Tableau de bord pour les mineurs en mode Junior SANS classe.

    Affiche les mêmes infos qu'un dashboard particulier
    mais avec une interface adaptée aux enfants.
    """
    user = request.user

    # ✅ Sécurité : rediriger si mal placé
    if not user.mode_junior:
        return redirect('vegetables_fruits:dashboard_particulier')

    # Si l'utilisateur a un profil élève avec classe → dashboard élève
    if hasattr(user, 'profil_eleve') and user.profil_eleve and user.profil_eleve.classe:
        return redirect('vegetables_fruits:dashboard_eleve')

    # ✅ 1. STATISTIQUES GÉNÉRALES
    parcelles = GeometricFigure.objects.filter(user=user)
    nb_parcelles = parcelles.count()
    surface_totale = parcelles.aggregate(Sum('surface_hectares'))['surface_hectares__sum'] or 0

    # Cultures actives
    cultures_actives = []
    for figure in parcelles:
        if figure.crops:
            for crop in figure.crops:
                if 'name' in crop:
                    cultures_actives.append(crop['name'])

    nb_cultures_actives = len(set(cultures_actives))

    # ✅ 2. MÉTÉO DU JOUR (première parcelle)
    premiere_parcelle = parcelles.filter(
        adresse_lat__isnull=False,
        adresse_lng__isnull=False
    ).first()

    meteo = None
    if premiere_parcelle:
        meteo = get_meteo_for_figure(premiere_parcelle)

    # ✅ 3. PROCHAINES ACTIONS (comme dashboard_particulier)
    prochaines_actions = []

    # Prochains semis
    prochains_semis = CalendrierUser.objects.filter(
        utilisateur=user,
        date_semis__gte=date.today()
    ).order_by('date_semis')[:3]

    for semis in prochains_semis:
        prochaines_actions.append({
            'date': semis.date_semis,
            'type': 'semis',
            'titre': f"🌱 Semis de {semis.culture}",
            'parcelle': semis.figure.name if semis.figure else 'Non spécifié'
        })

    # Prochaines récoltes
    prochaines_recoltes = ChronologieCulture.objects.filter(
        figure__user=user,
        statut__in=['seme', 'levee', 'croissance', 'floraison', 'fructification', 'pret'],
        date_recolte_prevue__gte=date.today()
    ).order_by('date_recolte_prevue')[:3]

    for recolte in prochaines_recoltes:
        prochaines_actions.append({
            'date': recolte.date_recolte_prevue,
            'type': 'recolte',
            'titre': f"🍅 Récolte de {recolte.culture_nom}",
            'parcelle': recolte.figure.name
        })

    prochaines_actions = sorted(prochaines_actions, key=lambda x: x['date'])[:5]

    # ✅ 4. MES CULTURES (avec progression DYNAMIQUE + état)
    mes_cultures = []
    nb_en_cours = 0
    nb_a_planifier = 0
    nb_recoltees = 0

    for figure in parcelles[:5]:
        if not figure.crops:
            continue

        for crop in figure.crops:
            nom_crop = crop.get('name', '')
            if not nom_crop:
                continue

            # ✅ Chercher la chronologie (SANS filtrer sur le statut)
            chrono = ChronologieCulture.objects.filter(
                figure=figure,
                culture_nom__icontains=nom_crop
            ).order_by('-date_semis').first()

            culture_emoji = crop.get('emoji', '🌱')

            if chrono:
                if chrono.statut == 'recolte':
                    # 🧺 RÉCOLTÉE
                    etat = 'recoltee'
                    progression = 100
                    statut = '🧺 Récoltée'
                    date_recolte = chrono.date_recolte_effective
                    nb_recoltees += 1
                else:
                    # 🟢 EN COURS
                    etat = 'en_cours'
                    progression = chrono.calculer_progression()
                    statut = chrono.get_statut_display()
                    date_recolte = chrono.date_recolte_prevue
                    culture_emoji = chrono.culture_emoji or culture_emoji
                    nb_en_cours += 1
            else:
                # 🟠 NON PLANIFIÉE
                etat = 'non_planifiee'
                progression = 0
                statut = '🟠 Non planifiée'
                date_recolte = None
                nb_a_planifier += 1

            mes_cultures.append({
                'nom': nom_crop,
                'emoji': culture_emoji,
                'parcelle': figure.name,
                'figure_id': figure.id,
                'etat': etat,
                'progression': progression,
                'statut': statut,
                'date_recolte': date_recolte,
                'chrono_id': chrono.id if chrono else None,
            })

    # ✅ Compteur global
    stats_mes_cultures = {
        'total': len(mes_cultures),
        'en_cours': nb_en_cours,
        'a_planifier': nb_a_planifier,
        'recoltees': nb_recoltees,
    }

    # ✅ 5. ALERTES RÉCENTES
    alertes_recentes = AlerteTraitement.objects.filter(
        utilisateur=user,
        statut__in=['en_attente', 'envoyee']
    ).order_by('-date_creation')[:3]

    alertes_meteo = AlerteMeteo.objects.filter(
        utilisateur=user
    ).order_by('-date_declenchement')[:2]

    # ✅ 6. STATISTIQUES
    stats = {
        'total_parcelles': nb_parcelles,
        'surface_totale': round(surface_totale, 2),
        'cultures_actives': nb_cultures_actives,
        'alertes_actives': AlerteTraitement.objects.filter(
            utilisateur=user, statut='en_attente'
        ).count(),
        'recoltes_mois': ChronologieCulture.objects.filter(
            figure__user=user,
            statut='recolte',
            date_recolte_effective__month=date.today().month
        ).count(),
    }

    context = {
        'stats': stats,
        'meteo': meteo,
        'prochaines_actions': prochaines_actions,
        'mes_cultures': mes_cultures,
        'alertes_recentes': alertes_recentes,
        'alertes_meteo': alertes_meteo,
        'username': user.username,
        'is_junior_sans_classe': True,
        'stats_mes_cultures': stats_mes_cultures,
    }

    return render(request, 'vegetables_fruits/dashboard_junior.html', context)


@login_required
def demander_autorisation_achat(request):
    """
    Le mineur demande à ses parents l'autorisation d'acheter.
    Envoie un email au parent avec un lien de validation.
    """
    user = request.user

    # ✅ Vérifier que l'utilisateur est bien mineur
    if not est_mineur(user):
        messages.info(request, "Vous n'avez pas besoin d'autorisation parentale.")
        return redirect('vegetables_fruits:tarification')

    # ✅ Vérifier que le plan est passé en paramètre
    plan_nom = request.GET.get('plan') or request.POST.get('plan')
    frequence = request.GET.get('frequence') or request.POST.get('frequence', 'MENSUEL')

    if not plan_nom:
        messages.error(request, "Veuillez choisir un plan.")
        return redirect('vegetables_fruits:tarification')

    plan = get_object_or_404(PlanTarification, nom__iexact=plan_nom, actif=True)

    # ✅ Créer la demande
    if request.method == 'POST':
        parent_nom = request.POST.get('parent_nom', '').strip()
        parent_prenom = request.POST.get('parent_prenom', '').strip()
        parent_email = request.POST.get('parent_email', '').strip()
        parent_telephone = request.POST.get('parent_telephone', '').strip()
        cgu = request.POST.get('cgu') == 'on'

        if not all([parent_nom, parent_prenom, parent_email]):
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
        elif not cgu:
            messages.error(request, "Vous devez accepter les conditions.")
        else:
            # Créer la demande
            autorisation = AutorisationAchatMineur.objects.create(
                utilisateur=user,
                plan_souhaite=plan,
                frequence=frequence,
                parent_nom=parent_nom,
                parent_prenom=parent_prenom,
                parent_email=parent_email,
                parent_telephone=parent_telephone,
                cgu_acceptees=True,
            )

            # Envoyer l'email au parent
            envoyer_email_autorisation_parent(autorisation, request)

            messages.success(
                request,
                f"✅ Un email a été envoyé à {parent_email}. "
                f"Ton parent doit valider pour que tu puisses t'abonner."
            )
            return redirect('vegetables_fruits:profile')

    context = {
        'plan': plan,
        'frequence': frequence,
        'est_mineur_jeune': est_mineur(user), # <15 ans ?
    }
    return render(request, 'vegetables_fruits/autorisation_achat_demande.html', context)


def envoyer_email_autorisation_parent(autorisation, request):
    """Envoie l'email au parent pour validation"""
    from django.urls import reverse
    from django.core.mail import send_mail
    from django.conf import settings

    lien_validation = request.build_absolute_uri(
        reverse(
            'vegetables_fruits:valider_autorisation_achat',
            args=[autorisation.token_validation]
        )
    )

    plan_nom = autorisation.plan_souhaite.get_nom_display() if autorisation.plan_souhaite else "?"
    prix = autorisation.plan_souhaite.prix_mensuel if autorisation.frequence == 'MENSUEL' else autorisation.plan_souhaite.prix_annuel

    sujet = f"🔒 Autorisation d'achat pour {autorisation.utilisateur.username} - Agriculture 2.0"

    message = f"""Bonjour {autorisation.parent_prenom} {autorisation.parent_nom},

Votre enfant {autorisation.utilisateur.username} souhaite souscrire à l'abonnement
{plan_nom} sur Agriculture 2.0 ({frequence} - {prix}€).

Pour donner votre autorisation, cliquez sur le lien ci-dessous :
{lien_validation}

Ce lien est valable 7 jours.

Si vous n'êtes pas à l'origine de cette demande, ignorez simplement cet email.

Cordialement,
L'équipe Agriculture 2.0"""

    send_mail(
        subject=sujet,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[autorisation.parent_email],
        fail_silently=False,
    )


def valider_autorisation_achat(request, token):
    """Page où le parent valide ou refuse l'autorisation"""
    autorisation = get_object_or_404(AutorisationAchatMineur, token_validation=token)

    # ✅ Vérifier l'expiration
    if autorisation.est_expiree():
        autorisation.statut = 'expiree'
        autorisation.save()
        return render(request, 'vegetables_fruits/autorisation_achat_expiree.html', {
            'autorisation': autorisation,
        })

    # ✅ Déjà traitée ?
    if autorisation.statut != 'en_attente':
        return render(request, 'vegetables_fruits/autorisation_achat_deja_traitee.html', {
            'autorisation': autorisation,
        })

    if request.method == 'POST':
        action = request.POST.get('action')
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        cgu = request.POST.get('cgu') == 'on'

        if action == 'refuser':
            autorisation.statut = 'refusee'
            autorisation.date_validation = timezone.now()
            autorisation.save()
            return render(request, 'vegetables_fruits/autorisation_achat_refusee.html', {
                'autorisation': autorisation,
            })

        if action == 'accepter':
            if not all([nom, prenom, cgu]):
                messages.error(request, "Veuillez remplir tous les champs.")
            else:
                autorisation.parent_nom = nom
                autorisation.parent_prenom = prenom
                autorisation.statut = 'validee'
                autorisation.autorisation_donnee = True
                autorisation.date_validation = timezone.now()
                autorisation.ip_validation = get_client_ip(request)
                autorisation.user_agent_validation = request.META.get('HTTP_USER_AGENT', '')[:500]
                autorisation.save()

                # ✅ Notifier l'enfant
                send_mail(
                    subject="✅ Autorisation accordée - Agriculture 2.0",
                    message=(
                        f"Bonjour {autorisation.utilisateur.username},\n\n"
                        f"Ton parent a validé ta demande d'abonnement {autorisation.plan_souhaite.get_nom_display()}.\n"
                        f"Tu peux maintenant finaliser ton inscription !\n\n"
                        f"À bientôt,\nL'équipe Agriculture 2.0"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[autorisation.utilisateur.email],
                    fail_silently=True,
                )

                return render(request, 'vegetables_fruits/autorisation_achat_validee.html', {
                    'autorisation': autorisation,
                })

    return render(request, 'vegetables_fruits/autorisation_achat_valider.html', {
        'autorisation': autorisation,
    })

def documentation(request):
    """Page d'accueil de la documentation"""
    return render(request, 'vegetables_fruits/documents/documentation.html')


def guide_eleve(request):
    return render(request, 'vegetables_fruits/documents/guide_eleve.html')

def guide_junior_particulier(request):
    return render(request, 'vegetables_fruits/documents/guide_junior_particulier.html')

def test_particulier(request):
    return render(request, 'vegetables_fruits/documents/tests/test_particulier.html')

def test_enseignant(request):
    return render(request, 'vegetables_fruits/documents/tests/test_enseignant.html')

def test_eleve(request):
    return render(request, 'vegetables_fruits/documents/tests/test_eleve.html')

def test_junior_particulier(request):
    return render(request, 'vegetables_fruits/documents/tests/test_junior_particulier.html')

def test_admin(request):
    return render(request, 'vegetables_fruits/documents/tests/test_admin.html')


# ============================================================
# RGPD : EXPORT DES DONNÉES UTILISATEUR
# ============================================================

@login_required
def exporter_mes_donnees(request):
    """
    Génère un ZIP contenant toutes les données personnelles de l'utilisateur.
    Droit à la portabilité RGPD (article 20).
    """
    import json
    import zipfile
    from io import BytesIO
    from django.http import FileResponse
    from datetime import date

    user = request.user
    buffer = BytesIO()

    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        # ============================================================
        # 1. Profil
        # ============================================================
        profil = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'birth_date': str(user.birth_date) if user.birth_date else None,
            'location': user.location,
            'telephone': user.telephone,
            'date_joined': str(user.date_joined),
            'last_login': str(user.last_login) if user.last_login else None,
            'mode_junior': user.mode_junior,
            'is_enseignant': user.is_enseignant,
            'tutoriel_termine': user.tutoriel_termine,
        }
        zf.writestr('profil.json', json.dumps(profil, indent=2, ensure_ascii=False))

        # ============================================================
        # 2. Figures (parcelles)
        # ============================================================
        figures = list(user.geometricfigure_set.values(
            'name', 'figure_type', 'created_at', 'surface_hectares',
            'nb_points', 'description', 'adresse', 'adresse_formatted',
        ))
        zf.writestr('figures.json', json.dumps(figures, indent=2, ensure_ascii=False, default=str))

        # ============================================================
        # 3. Parcelles
        # ============================================================
        parcelles = list(user.parcelles.values(
            'nom', 'surface_m2', 'type_sol', 'exposition',
            'irrigation_type', 'date_creation', 'est_active',
        ))
        zf.writestr('parcelles.json', json.dumps(parcelles, indent=2, ensure_ascii=False, default=str))

        # ============================================================
        # 4. Journal de bord
        # ============================================================
        notes = list(user.notes_journal.values(
            'titre', 'note', 'date_note', 'tags', 'meteo',
            'temperature', 'date_creation',
        ))
        zf.writestr('journal.json', json.dumps(notes, indent=2, ensure_ascii=False, default=str))

        # ============================================================
        # 5. Chronologies de cultures
        # ============================================================
        chronos = list(user.geometricfigure_set.values(
            'chronologies__culture_nom',
            'chronologies__date_semis',
            'chronologies__date_recolte_prevue',
            'chronologies__date_recolte_effective',
            'chronologies__statut',
            'chronologies__progression',
        ))
        zf.writestr('chronologies.json', json.dumps(chronos, indent=2, ensure_ascii=False, default=str))

        # ============================================================
        # 6. Calendrier (semis planifiés)
        # ============================================================
        calendrier = list(user.calendrier_semis.values(
            'culture', 'date_semis', 'date_plantation',
            'date_recolte_prevue', 'date_creation',
        ))
        zf.writestr('calendrier.json', json.dumps(calendrier, indent=2, ensure_ascii=False, default=str))

        # ============================================================
        # 7. Alertes
        # ============================================================
        alertes_semis = list(user.geometricfigure_set.values(
            'alertes__type_alerte', 'alertes__titre', 'alertes__message',
            'alertes__date_declenchement', 'alertes__statut',
        ))
        zf.writestr('alertes_semis.json', json.dumps(alertes_semis, indent=2, ensure_ascii=False, default=str))

        alertes_meteo = list(user.alertes_meteo.values(
            'type_alerte', 'message', 'temperature',
            'date_declenchement', 'statut',
        ))
        zf.writestr('alertes_meteo.json', json.dumps(alertes_meteo, indent=2, ensure_ascii=False, default=str))

        # ============================================================
        # 8. Quiz
        # ============================================================
        quiz = list(user.quizutilisateur_set.values(
            'date', 'score', 'nb_quiz',
        ))
        zf.writestr('quiz.json', json.dumps(quiz, indent=2, ensure_ascii=False, default=str))

        # ============================================================
        # 9. Consentements RGPD
        # ============================================================
        consentements = list(user.consentements.values(
            'type_consentement', 'statut', 'est_mineur',
            'date_consentement', 'representant_legal_email',
        ))
        zf.writestr('consentements.json', json.dumps(consentements, indent=2, ensure_ascii=False, default=str))

        # ============================================================
        # 10. Abonnement
        # ============================================================
        try:
            abo = user.abonnement
            abo_data = {
                'plan': abo.plan.nom if abo.plan else None,
                'statut': abo.statut,
                'frequence': abo.frequence,
                'date_debut': str(abo.date_debut),
                'date_fin': str(abo.date_fin) if abo.date_fin else None,
            }
        except Abonnement.DoesNotExist:
            abo_data = None
        zf.writestr('abonnement.json', json.dumps(abo_data, indent=2, ensure_ascii=False))

        # ============================================================
        # 11. Photos uploadées
        # ============================================================
        for photo in user.photos_jardin.all():
            if photo.image and photo.image.storage.exists(photo.image.name):
                try:
                    zf.write(photo.image.path, f'photos/{photo.image.name}')
                except Exception as e:
                    logger.warning(f"Impossible d'ajouter la photo {photo.id} : {e}")

        # ============================================================
        # 12. README explicatif
        # ============================================================
        readme = f"""EXPORT DES DONNÉES AGRICULTURE 2.0
========================================

Utilisateur : {user.username}
Date d'export : {date.today().strftime('%d/%m/%Y')}

Ce fichier ZIP contient toutes vos données personnelles
conformément au RGPD (article 20 - droit à la portabilité).

Contenu :
- profil.json : Vos informations de profil
- figures.json : Vos figures/parcelles dessinées
- parcelles.json : Détails de vos parcelles
- journal.json : Vos notes de journal de bord
- chronologies.json : Historique de vos cultures
- calendrier.json : Vos semis planifiés
- alertes_semis.json : Vos alertes de semis
- alertes_meteo.json : Vos alertes météo
- quiz.json : Vos quiz passés
- consentements.json : Vos consentements RGPD
- abonnement.json : Détails de votre abonnement
- photos/ : Vos photos uploadées

Pour toute question : contact@agriculture20.fr
"""
        zf.writestr('README.txt', readme)

    buffer.seek(0)
    logger.info(f"Export RGPD généré pour {user.username}")

    response = FileResponse(
        buffer,
        as_attachment=True,
        filename=f'mes_donnees_agriculture20_{user.username}.zip'
    )
    return response


# ============================================================
# RGPD : SUPPRESSION DU COMPTE UTILISATEUR
# ============================================================

@login_required
def supprimer_mon_compte(request):
    """
    Supprime le compte de l'utilisateur et anonymise ses données.
    Droit à l'effacement RGPD (article 17).
    """
    user = request.user

    # ============================================================
    # 1. VÉRIFICATIONS DE BLOCAGE
    # ============================================================

    # ❌ Enseignant avec classes actives
    if user.is_enseignant:
        nb_classes = user.classes_enseignees.count()
        if nb_classes > 0:
            messages.error(
                request,
                f"❌ Vous avez {nb_classes} classe(s) active(s). "
                "Veuillez les supprimer ou les transférer avant de supprimer votre compte."
            )
            return redirect('vegetables_fruits:profile')

    # ❌ Mineur → besoin accord parental
    if est_mineur(user):
        messages.warning(
            request,
            "🔒 La suppression d'un compte mineur nécessite l'accord parental. "
            "Contactez-nous à contact@agriculture20.fr avec l'email du parent."
        )
        return redirect('vegetables_fruits:profile')

    # ============================================================
    # 2. TRAITEMENT POST
    # ============================================================
    if request.method == 'POST':
        # Confirmation par saisie du mot de passe
        mot_de_passe = request.POST.get('mot_de_passe', '')
        confirmation = request.POST.get('confirmation', '')

        if confirmation != 'SUPPRIMER':
            messages.error(request, "❌ Veuillez taper SUPPRIMER pour confirmer.")
            return redirect('vegetables_fruits:supprimer_mon_compte')

        if not user.check_password(mot_de_passe):
            logger.warning(f"Suppression de compte refusée : mot de passe incorrect pour {user.username}")
            messages.error(request, "❌ Mot de passe incorrect.")
            return redirect('vegetables_fruits:supprimer_mon_compte')

        # Sauvegarder l'username pour le log
        ancien_username = user.username
        ancien_email = user.email

        # ============================================================
        # 3. SUPPRESSION / ANONYMISATION DES DONNÉES
        # ============================================================

        # Supprimer les données personnelles (vraie suppression)
        user.geometricfigure_set.all().delete()
        user.notes_journal.all().delete()
        user.photos_jardin.all().delete()
        user.rappels.all().delete()
        user.consentements.all().delete()
        user.calendrier_semis.all().delete()
        user.alertes_meteo.all().delete()
        user.quizutilisateur_set.all().delete()

        # Parcelles
        user.parcelles.all().delete()

        # Abonnement
        try:
            user.abonnement.delete()
        except Abonnement.DoesNotExist:
            pass

        # Anonymiser le compte
        user.username = f"anonyme_{user.id}"
        user.email = f"deleted_{user.id}@anonyme.local"
        user.first_name = ""
        user.last_name = ""
        user.birth_date = None
        user.location = ""
        user.telephone = ""
        user.bio = ""
        user.is_active = False
        user.save()

        logger.info(f"Compte supprimé : {ancien_username} ({ancien_email}) → anonymisé")

        # Déconnecter
        logout(request)

        messages.success(
            request,
            "✅ Votre compte a été supprimé avec succès. "
            "Merci d'avoir utilisé Agriculture 2.0."
        )
        return redirect('vegetables_fruits:index')

    # ============================================================
    # 4. GET — Afficher la page de confirmation
    # ============================================================
    return render(request, 'vegetables_fruits/supprimer_compte.html')


def offline(request):
    return render(request, 'vegetables_fruits/offline.html')