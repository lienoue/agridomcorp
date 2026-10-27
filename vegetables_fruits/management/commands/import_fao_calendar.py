"""
Management command : import_fao_calendar

Importe le calendrier FAO (Crop Calendar by Country) dans CalendrierSemis.

- Filtre sur les pays/cultures connus (mapping dans fao_mapping.py)
- Parse les periods "Nov 01 - Jan 10" → mois_debut=11, mois_fin=1
- Fusion : ne touche pas aux entrées existantes (get_or_create)
- Utilise cropProcess='Sowing' uniquement (on ignore 'Harvesting')

Usage :
    python manage.py import_fao_calendar --dry-run
    python manage.py import_fao_calendar
    python manage.py import_fao_calendar --csv data/fao_crop_calendar.csv
"""

import csv
import os
import re
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from vegetables_fruits.models import CalendrierSemis
from vegetables_fruits.fao_mapping import (
    PAYS_FAO_VERS_REGION,
    CULTURE_FAO_VERS_FR,
)


MOIS_EN = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
}

# Regex pour parser "Nov 01 - Jan 10"
PERIODE_RE = re.compile(r'^([A-Z][a-z]{2})\s+\d+\s*-\s*([A-Z][a-z]{2})\s+\d+$')


class Command(BaseCommand):
    help = "Importe le calendrier FAO dans CalendrierSemis (fusion)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            default=None,
            help="Chemin du CSV (défaut: BASE_DIR/data/fao_crop_calendar.csv)"
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Simuler sans écrire en base"
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        csv_path = options['csv']

        if not csv_path:
            csv_path = os.path.join(settings.BASE_DIR, 'data', 'fao_crop_calendar.csv')

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"❌ Fichier introuvable : {csv_path}"))
            return

        self.stdout.write(f"📂 Lecture de {csv_path}")

        stats = {
            'lignes_lues': 0,
            'lignes_filtrees_pays': 0,
            'lignes_filtrees_culture': 0,
            'lignes_filtrees_process': 0,
            'lignes_filtrees_periode': 0,
            'crees': 0,
            'ignores': 0,
            'doublons': 0,
        }

        # Déduplication : une culture ne peut apparaître qu'une fois par région
        # (contrainte unique_together culture + region dans le modèle)
        deja_vus = set()

        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            for row in reader:
                stats['lignes_lues'] += 1

                # 1. Filtrer sur Sowing uniquement
                if row.get('cropProcess', '').strip() != 'Sowing':
                    stats['lignes_filtrees_process'] += 1
                    continue

                # 2. Filtrer sur pays connus
                pays_fao = row.get('country_name_en', '').strip()
                region = PAYS_FAO_VERS_REGION.get(pays_fao)
                if not region:
                    stats['lignes_filtrees_pays'] += 1
                    continue

                # 3. Filtrer sur culture connue
                culture_fao = row.get('cropName', '').strip()
                culture_fr = CULTURE_FAO_VERS_FR.get(culture_fao)
                if not culture_fr:
                    stats['lignes_filtrees_culture'] += 1
                    continue

                # 4. Extraire la 1ère période (period1)
                period1 = row.get('period1', '').strip()
                match = PERIODE_RE.match(period1)
                if not match:
                    stats['lignes_filtrees_periode'] += 1
                    continue

                mois_debut = MOIS_EN.get(match.group(1))
                mois_fin = MOIS_EN.get(match.group(2))
                if not mois_debut or not mois_fin:
                    stats['lignes_filtrees_periode'] += 1
                    continue

                # 5. Déduplication
                key = (culture_fr, region)
                if key in deja_vus:
                    stats['doublons'] += 1
                    continue
                deja_vus.add(key)

                # 6. Fusion : on ne touche pas aux entrées existantes
                if dry_run:
                    existe = CalendrierSemis.objects.filter(
                        culture=culture_fr, region=region
                    ).exists()
                    if existe:
                        stats['ignores'] += 1
                    else:
                        stats['crees'] += 1
                    continue

                _, created = CalendrierSemis.objects.get_or_create(
                    culture=culture_fr,
                    region=region,
                    defaults={
                        'mois_debut_semis': mois_debut,
                        'mois_fin_semis': mois_fin,
                        'mois_debut_recolte': mois_debut, # à affiner plus tard
                        'mois_fin_recolte': mois_fin,
                        'type_plantation': 'pleine_terre',
                        'conseils': f"Source : FAO Crop Calendar ({pays_fao})",
                    }
                )
                if created:
                    stats['crees'] += 1
                else:
                    stats['ignores'] += 1

        # Rapport
        prefix = "🔍 [DRY-RUN] " if dry_run else "✅ "
        self.stdout.write(self.style.SUCCESS(f"\n{prefix}Rapport d'import :"))
        self.stdout.write(f" 📄 Lignes lues : {stats['lignes_lues']}")
        self.stdout.write(f" 🌍 Filtrées (pays) : {stats['lignes_filtrees_pays']}")
        self.stdout.write(f" 🌱 Filtrées (culture) : {stats['lignes_filtrees_culture']}")
        self.stdout.write(f" 🔄 Filtrées (process) : {stats['lignes_filtrees_process']}")
        self.stdout.write(f" 📅 Filtrées (période) : {stats['lignes_filtrees_periode']}")
        self.stdout.write(f" ♻️ Doublons écartés : {stats['doublons']}")
        self.stdout.write(self.style.SUCCESS(f" ✅ Créés : {stats['crees']}"))
        self.stdout.write(f" ⏭️ Ignorés (existants): {stats['ignores']}")