"""
Management command : seed_calendrier_semis

Peuple / complète la table CalendrierSemis pour toutes les régions
du monde, avec ~45 cultures par région.

Stratégie : FUSION (get_or_create)
- Si une culture existe déjà pour cette région → on ne touche à RIEN
- Si elle manque → on l'ajoute avec les données par défaut

Usage :
    python manage.py seed_calendrier_semis
    python manage.py seed_calendrier_semis --region iledefrance
    python manage.py seed_calendrier_semis --dry-run
"""

from django.core.management.base import BaseCommand
from vegetables_fruits.models import CalendrierSemis


class Command(BaseCommand):
    help = "Peuple/complète le calendrier des semis pour toutes les régions du monde"

    def add_arguments(self, parser):
        parser.add_argument(
            '--region',
            type=str,
            default=None,
            help="Ne traiter qu'une seule région (ex: iledefrance)"
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Simuler sans écrire en base"
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        region_filtre = options['region']

        # ============================================================
        # CULTURES DE RÉFÉRENCE FRANCE / EUROPE TEMPÉRÉE
        # Format : nom → (mois_semis_debut, mois_semis_fin,
        # mois_recolte_debut, mois_recolte_fin)
        # ============================================================
        CULTURES_TEMPEREES = {
            # Légumes-fruits
            'Tomate': (3, 5, 7, 9),
            'Tomate cerise': (3, 5, 7, 9),
            'Courgette': (4, 6, 7, 9),
            'Concombre': (4, 6, 7, 9),
            'Cornichon': (4, 6, 7, 9),
            'Aubergine': (3, 5, 7, 9),
            'Poivron': (3, 5, 7, 9),
            'Piment': (3, 5, 7, 9),
            'Melon': (4, 5, 7, 9),
            'Pastèque': (4, 5, 8, 9),
            'Potiron': (4, 5, 9, 10),
            'Citrouille': (4, 5, 9, 10),
            'Courge butternut': (4, 5, 9, 10),

            # Légumes-racines
            'Carotte': (3, 7, 6, 10),
            'Radis': (3, 9, 5, 11),
            'Radis noir': (7, 8, 10, 12),
            'Betterave': (4, 6, 7, 10),
            'Navet': (4, 7, 6, 10),
            'Panais': (4, 6, 8, 11),
            'Pomme de terre': (3, 5, 6, 9),
            'Patate douce': (4, 5, 8, 10),
            'Topinambour': (3, 4, 10, 11),
            'Céleri-rave': (3, 4, 10, 11),

            # Légumes-bulbes
            'Oignon': (3, 4, 7, 9),
            'Oignon rouge': (3, 4, 7, 9),
            'Ail': (10, 11, 6, 7),
            'Échalote': (10, 11, 6, 7),
            'Poireau': (3, 5, 9, 12),

            # Légumes-feuilles
            'Salade': (3, 9, 5, 11),
            'Laitue': (3, 9, 5, 11),
            'Épinard': (3, 5, 5, 9),
            'Mâche': (8, 10, 10, 12),
            'Roquette': (4, 8, 6, 10),
            'Blette': (4, 6, 7, 11),
            'Cresson': (4, 8, 6, 10),

            # Choux
            'Chou': (4, 6, 8, 11),
            'Chou-fleur': (4, 6, 9, 11),
            'Brocoli': (4, 6, 9, 11),
            'Chou de Bruxelles': (4, 5, 10, 12),
            'Chou-rave': (4, 6, 8, 10),
            'Chou chinois': (7, 8, 10, 11),

            # Légumineuses
            'Haricot': (5, 7, 7, 9),
            'Haricot vert': (5, 7, 7, 9),
            'Petit pois': (3, 5, 6, 7),
            'Fève': (10, 11, 6, 7),
            'Lentille': (3, 4, 7, 8),
            'Pois chiche': (3, 4, 7, 8),

            # Aromatiques
            'Basilic': (4, 6, 6, 9),
            'Persil': (3, 8, 6, 11),
            'Ciboulette': (3, 5, 6, 10),
            'Thym': (3, 5, 5, 10),
            'Romarin': (3, 5, 5, 10),
            'Menthe': (3, 5, 6, 10),
            'Sauge': (3, 5, 6, 10),
            'Coriandre': (4, 7, 6, 9),
            'Aneth': (4, 7, 6, 9),
            'Estragon': (4, 5, 6, 10),
            'Origan': (4, 5, 6, 10),
            'Lavande': (3, 5, 6, 8),

            # Fruits rouges
            'Fraise': (8, 9, 5, 7),
            'Framboise': (10, 11, 6, 8),
            'Cassis': (10, 11, 7, 8),
            'Groseillier': (10, 11, 7, 8),
            'Myrtille': (10, 11, 7, 8),
            'Mûrier': (10, 11, 7, 8),
            'Airelle': (10, 11, 7, 9),

            # Arbres fruitiers
            'Pommier': (10, 11, 8, 10),
            'Poirier': (10, 11, 9, 10),
            'Cerisier': (10, 11, 6, 7),
            'Prunier': (10, 11, 7, 9),
            'Abricotier': (10, 11, 7, 8),
            'Pêcher': (10, 11, 7, 8),
            'Figuier': (10, 11, 8, 9),
            'Kiwi': (10, 11, 10, 11),
            'Vigne': (10, 11, 9, 10),
            'Noyer': (10, 11, 9, 10),
            'Noisetier': (10, 11, 8, 9),
            'Olivier': (3, 4, 10, 11),
            'Cognassier': (10, 11, 9, 10),
            'Nectarinier': (10, 11, 7, 8),
            'Mirabellier': (10, 11, 8, 9),
        }

        # ============================================================
        # CULTURES ADAPTÉES TROPICAL / SUBTROPICAL
        # ============================================================
        CULTURES_TROPICALES = {
            'Riz': (4, 6, 9, 10),
            'Maïs': (4, 6, 8, 9),
            'Manioc': (3, 5, 10, 12),
            'Igname': (3, 5, 10, 12),
            'Patate douce': (3, 5, 8, 10),
            'Banane': (3, 6, 10, 12),
            'Bananier': (3, 6, 10, 12),
            'Papaye': (3, 6, 9, 12),
            'Mangue': (3, 6, 10, 12),
            'Manguier': (3, 6, 10, 12),
            'Ananas': (3, 6, 10, 12),
            'Cocotier': (1, 12, 1, 12),
            'Avocatier': (3, 5, 10, 12),
            'Goyavier': (3, 5, 10, 12),
            'Litchi': (3, 5, 11, 12),
            'Fruit de la passion': (3, 6, 9, 12),
            'Cacao': (4, 6, 11, 12),
            'Caféier': (4, 6, 11, 12),
            'Vanille': (4, 6, 10, 12),
            'Gingembre': (4, 6, 10, 12),
            'Curcuma': (4, 6, 10, 12),
            'Poivre': (4, 6, 10, 12),
            'Cannelle': (4, 6, 10, 12),
            'Citronnelle': (4, 6, 8, 11),
            'Aubergine': (3, 6, 7, 11),
            'Concombre': (3, 6, 7, 11),
            'Piment': (3, 6, 7, 12),
            'Gombo': (4, 6, 8, 11),
            'Arachide': (4, 6, 9, 11),
            'Sésame': (4, 6, 9, 11),
            'Sorgho': (5, 7, 9, 11),
            'Millet': (5, 7, 9, 11),
            'Taro': (3, 6, 10, 12),
            'Dachine': (3, 6, 10, 12),
        }

        # ============================================================
        # CULTURES ADAPTÉES MÉDITERRANÉEN
        # ============================================================
        CULTURES_MEDITERRANEENNES = {
            'Tomate': (3, 5, 6, 9),
            'Aubergine': (3, 5, 7, 9),
            'Poivron': (3, 5, 7, 9),
            'Courgette': (3, 6, 6, 9),
            'Concombre': (4, 6, 7, 9),
            'Melon': (4, 5, 7, 9),
            'Pastèque': (4, 5, 7, 9),
            'Artichaut': (3, 5, 10, 12),
            'Asperge': (3, 4, 4, 6),
            'Fève': (10, 11, 5, 6),
            'Petit pois': (10, 11, 4, 6),
            'Ail': (10, 12, 5, 7),
            'Oignon': (10, 12, 5, 7),
            'Olivier': (3, 5, 10, 12),
            'Vigne': (2, 4, 8, 10),
            'Figuier': (2, 4, 7, 9),
            'Grenadier': (2, 4, 9, 10),
            'Lavande': (3, 5, 6, 8),
            'Romarin': (3, 5, 5, 10),
            'Thym': (3, 5, 5, 10),
            'Sauge': (3, 5, 5, 10),
            'Origan': (3, 5, 6, 10),
            'Câpre': (3, 5, 6, 9),
            'Citronnier': (3, 5, 10, 12),
            'Oranger': (3, 5, 11, 1),
            'Mandarinier': (3, 5, 11, 1),
            'Pamplemoussier': (3, 5, 11, 1),
            'Amandier': (2, 3, 8, 9),
            'Pistachier': (2, 3, 8, 9),
            'Caroubier': (3, 4, 9, 10),
            'Figue de Barbarie': (4, 6, 8, 10),
            'Kaki': (2, 4, 10, 11),
            'Néflier': (2, 4, 10, 11),
            'Plaqueminier': (2, 4, 10, 11),
            'Fenouil': (3, 8, 6, 11),
            'Céleri': (4, 7, 8, 12),
            'Blette': (3, 6, 6, 11),
            'Épinard': (3, 4, 5, 7),
            'Roquette': (3, 9, 5, 11),
            'Mâche': (9, 11, 11, 1),
            'Radis': (3, 9, 5, 11),
            'Carotte': (3, 7, 6, 10),
        }

        # ============================================================
        # CULTURES ADAPTÉES DÉSERTIQUE / ARIDE
        # ============================================================
        CULTURES_DESERTIQUES = {
            'Dattier': (3, 5, 9, 11),
            'Figuier': (2, 4, 7, 10),
            'Olivier': (3, 5, 10, 12),
            'Grenadier': (2, 4, 9, 11),
            'Amandier': (2, 3, 8, 9),
            'Pistachier': (2, 3, 8, 9),
            'Abricotier': (2, 3, 6, 7),
            'Pêcher': (2, 3, 6, 7),
            'Vigne': (2, 4, 8, 10),
            'Melon': (3, 5, 7, 9),
            'Pastèque': (3, 5, 7, 9),
            'Tomate': (3, 5, 6, 9),
            'Poivron': (3, 5, 7, 9),
            'Aubergine': (3, 5, 7, 9),
            'Piment': (3, 5, 7, 9),
            'Concombre': (3, 5, 7, 9),
            'Courgette': (3, 5, 6, 9),
            'Ail': (10, 12, 5, 7),
            'Oignon': (10, 12, 5, 7),
            'Menthe': (3, 5, 6, 10),
            'Basilic': (3, 5, 6, 9),
            'Persil': (3, 8, 6, 11),
            'Coriandre': (3, 7, 5, 9),
            'Cumin': (3, 5, 6, 8),
            'Fenouil': (3, 8, 6, 11),
            'Carotte': (3, 7, 6, 10),
            'Radis': (3, 9, 5, 11),
            'Betterave': (3, 6, 6, 10),
            'Navet': (3, 6, 6, 10),
            'Laitue': (3, 9, 5, 11),
            'Épinard': (3, 5, 5, 7),
            'Blette': (3, 5, 6, 9),
            'Roquette': (3, 9, 5, 11),
            'Fève': (10, 11, 4, 6),
            'Petit pois': (10, 11, 4, 6),
            'Pois chiche': (10, 11, 4, 6),
            'Lentille': (10, 11, 4, 6),
            'Sésame': (4, 6, 9, 11),
            'Sorgho': (4, 6, 9, 11),
            'Millet': (4, 6, 9, 11),
            'Maïs': (4, 6, 8, 10),
        }

        # ============================================================
        # CULTURES ADAPTÉES CONTINENTAL / FROID
        # ============================================================
        CULTURES_CONTINENTALES = {
            'Pomme de terre': (4, 5, 8, 9),
            'Betterave': (4, 6, 8, 10),
            'Carotte': (4, 6, 7, 10),
            'Navet': (4, 6, 7, 10),
            'Panais': (4, 6, 9, 11),
            'Topinambour': (3, 4, 10, 11),
            'Chou': (4, 6, 9, 11),
            'Chou-fleur': (4, 6, 9, 11),
            'Brocoli': (4, 6, 9, 11),
            'Chou de Bruxelles': (4, 5, 10, 12),
            'Chou-rave': (4, 6, 8, 10),
            'Radis': (4, 8, 6, 10),
            'Épinard': (4, 6, 6, 9),
            'Salade': (4, 8, 6, 10),
            'Laitue': (4, 8, 6, 10),
            'Mâche': (8, 9, 10, 11),
            'Petit pois': (4, 5, 7, 8),
            'Fève': (4, 5, 7, 8),
            'Haricot': (5, 6, 8, 9),
            'Ail': (10, 11, 7, 8),
            'Oignon': (4, 5, 8, 9),
            'Poireau': (4, 5, 9, 11),
            'Pomme': (10, 11, 9, 10),
            'Poire': (10, 11, 9, 10),
            'Cerise': (10, 11, 7, 8),
            'Prune': (10, 11, 8, 9),
            'Fraise': (8, 9, 6, 7),
            'Framboise': (10, 11, 7, 8),
            'Cassis': (10, 11, 7, 8),
            'Groseille': (10, 11, 7, 8),
            'Myrtille': (10, 11, 7, 8),
            'Seigle': (9, 10, 7, 8),
            'Blé': (9, 10, 7, 8),
            'Orge': (9, 10, 7, 8),
            'Avoine': (9, 10, 7, 8),
        }

        # ============================================================
        # MAPPING RÉGIONS → TYPE DE CULTURES
        # ============================================================
        REGIONS_CULTURES = {
            # ---- FRANCE / EUROPE TEMPÉRÉE ----
            'iledefrance': CULTURES_TEMPEREES,
            'provence': CULTURES_MEDITERRANEENNES,
            'bretagne': CULTURES_TEMPEREES,
            'normandie': CULTURES_TEMPEREES,
            'alsace': CULTURES_TEMPEREES,
            'nord': CULTURES_TEMPEREES,
            'occitanie': CULTURES_MEDITERRANEENNES,
            'nouvelle_aquitaine': CULTURES_TEMPEREES,
            'auvergne_rhone_alpes': CULTURES_TEMPEREES,
            'pays_de_la_loire': CULTURES_TEMPEREES,
            'centre_val_de_loire': CULTURES_TEMPEREES,
            'bourgogne_franche_comte': CULTURES_TEMPEREES,
            'corse': CULTURES_MEDITERRANEENNES,
            'paca': CULTURES_MEDITERRANEENNES,

            # ---- EUROPE ----
            'europe_nord': CULTURES_CONTINENTALES,
            'europe_sud': CULTURES_MEDITERRANEENNES,

            # ---- AMÉRIQUE DU NORD ----
            'californie': CULTURES_MEDITERRANEENNES,
            'usa_nord_est': CULTURES_TEMPEREES,
            'canada': CULTURES_CONTINENTALES,
            'mexique': CULTURES_TROPICALES,

            # ---- AMÉRIQUE CENTRALE / SUD ----
            'amerique_centrale': CULTURES_TROPICALES,
            'amazonie': CULTURES_TROPICALES,
            'bresil': CULTURES_TROPICALES,
            'argentine': CULTURES_TEMPEREES,
            'chili': CULTURES_MEDITERRANEENNES,

            # ---- AFRIQUE ----
            'afrique_nord': CULTURES_DESERTIQUES,
            'afrique_ouest': CULTURES_TROPICALES,
            'afrique_est': CULTURES_TROPICALES,
            'afrique_australe': CULTURES_TEMPEREES,

            # ---- ASIE / MOYEN-ORIENT ----
            'chine': CULTURES_TEMPEREES,
            'japon': CULTURES_TEMPEREES,
            'inde': CULTURES_TROPICALES,
            'asie_sud_est': CULTURES_TROPICALES,
            'moyen_orient': CULTURES_DESERTIQUES,

            # ---- OCÉANIE ----
            'australie_sud_est': CULTURES_MEDITERRANEENNES,
            'nouvelle_zelande': CULTURES_TEMPEREES,

            # ---- ZONES POLAIRES ----
            'arctique': CULTURES_CONTINENTALES,

            # ---- FALLBACK MONDIAL ----
            'tous': CULTURES_TEMPEREES,
        }

        # ============================================================
        # TRAITEMENT
        # ============================================================
        total_crees = 0
        total_ignores = 0

        for region, cultures in REGIONS_CULTURES.items():
            if region_filtre and region != region_filtre:
                continue

            for culture, (m1, m2, r1, r2) in cultures.items():
                if dry_run:
                    existe = CalendrierSemis.objects.filter(
                        culture=culture, region=region
                    ).exists()
                    if existe:
                        total_ignores += 1
                    else:
                        total_crees += 1
                    continue

                obj, created = CalendrierSemis.objects.get_or_create(
                    culture=culture,
                    region=region,
                    defaults={
                        'mois_debut_semis': m1,
                        'mois_fin_semis': m2,
                        'mois_debut_recolte': r1,
                        'mois_fin_recolte': r2,
                        'type_plantation': 'pleine_terre',
                        'conseils': '',
                    }
                )
                if created:
                    total_crees += 1
                else:
                    total_ignores += 1

        # ============================================================
        # RAPPORT
        # ============================================================
        prefix = "🔍 [DRY-RUN] " if dry_run else "✅ "
        self.stdout.write(self.style.SUCCESS(
            f"{prefix}{total_crees} entrées créées, "
            f"{total_ignores} entrées conservées (fusion)"
        ))
        self.stdout.write(
            f" Régions traitées : {len(REGIONS_CULTURES) if not region_filtre else 1}"
        )