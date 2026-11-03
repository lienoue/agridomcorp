# vegetables_fruits/management/commands/recalculer_dates_recolte.py
"""
Recalcule les dates de récolte des ChronologieCulture existantes.

Usage :
    python manage.py recalculer_dates_recolte # dry-run (safe)
    python manage.py recalculer_dates_recolte --apply # applique
    python manage.py recalculer_dates_recolte --apply --figure=42
    python manage.py recalculer_dates_recolte --apply --only-perennes
"""
from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from vegetables_fruits.models import ChronologieCulture, GeometricFigure
from vegetables_fruits.services_dates import (
    calculer_date_recolte,
    determiner_type_cycle,
)


class Command(BaseCommand):
    help = "Recalcule date_recolte_prevue et type_cycle pour les ChronologieCulture existantes."

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply',
            action='store_true',
            help="Applique les modifications (par défaut : dry-run)"
        )
        parser.add_argument(
            '--figure',
            type=int,
            default=None,
            help="Limiter à une figure (ID)"
        )
        parser.add_argument(
            '--only-perennes',
            action='store_true',
            help="Ne traiter que les cultures pérennes (arbres/arbustes)"
        )
        parser.add_argument(
            '--skip-recoltees',
            action='store_true',
            default=True,
            help="Ignorer les cultures déjà récoltées (défaut: True)"
        )
        parser.add_argument(
            '--include-recoltees',
            action='store_true',
            help="Traiter aussi les cultures déjà récoltées"
        )

    def handle(self, *args, **options):
        apply_mode = options['apply']
        figure_id = options['figure']
        only_perennes = options['only_perennes']
        include_recoltees = options['include_recoltees']

        # ============================================================
        # Construction du queryset
        # ============================================================
        qs = ChronologieCulture.objects.select_related('figure', 'figure__user')

        if figure_id:
            qs = qs.filter(figure_id=figure_id)

        if not include_recoltees:
            # Par défaut, on NE touche PAS aux cultures récoltées
            # (la date récolte_prevue est un historique, pas une prédiction)
            qs = qs.exclude(statut='recolte')

        self.stdout.write(self.style.NOTICE(
            f"\n📊 Analyse de {qs.count()} ChronologieCulture(s)"
            f"{f' (figure={figure_id})' if figure_id else ''}"
            f"{' [pérennes uniquement]' if only_perennes else ''}\n"
        ))

        # ============================================================
        # Compteurs
        # ============================================================
        stats = {
            'traitees': 0,
            'inchangees': 0,
            'corrigees': 0,
            'ignorees': 0,
            'recoltees_ignorees': 0,
        }

        a_modifier = []

        # ============================================================
        # Analyse (dans tous les cas, même en dry-run)
        # ============================================================
        for chrono in qs.iterator():
            # Ignorer les cultures récoltées si demandé
            if not include_recoltees and chrono.statut == 'recolte':
                stats['recoltees_ignorees'] += 1
                continue

            # Ignorer si pas de date de semis
            if not chrono.date_semis:
                stats['ignorees'] += 1
                self.stdout.write(self.style.WARNING(
                    f"⚠️ Chrono #{chrono.id} ({chrono.culture_nom}) "
                    f"n'a pas de date_semis → ignorée"
                ))
                continue

            # Filtre pérennes uniquement
            type_theorique = determiner_type_cycle(chrono.culture_nom)
            if only_perennes and type_theorique != 'perenne':
                stats['ignorees'] += 1
                continue

            # Recalcul
            try:
                calc = calculer_date_recolte(chrono.culture_nom, chrono.date_semis)
            except Exception as e:
                stats['ignorees'] += 1
                self.stdout.write(self.style.ERROR(
                    f"❌ Chrono #{chrono.id} ({chrono.culture_nom}) : erreur {e}"
                ))
                continue

            stats['traitees'] += 1

            nouvelle_date = calc['date_recolte']
            nouveau_type_cycle = 'semis' if calc['type_cycle'] != 'perenne' else 'plantation'

            # Déterminer si modification nécessaire
            date_change = chrono.date_recolte_prevue != nouvelle_date
            type_change = chrono.type_cycle != nouveau_type_cycle

            if date_change or type_change:
                a_modifier.append({
                    'chrono': chrono,
                    'ancienne_date': chrono.date_recolte_prevue,
                    'nouvelle_date': nouvelle_date,
                    'ancien_type': chrono.type_cycle,
                    'nouveau_type': nouveau_type_cycle,
                    'source': calc['source'],
                    'type_cycle': calc['type_cycle'],
                })
                stats['corrigees'] += 1
            else:
                stats['inchangees'] += 1

        # ============================================================
        # Rapport détaillé
        # ============================================================
        self.stdout.write(self.style.NOTICE("\n" + "=" * 70))
        self.stdout.write(self.style.NOTICE("📋 DÉTAIL DES MODIFICATIONS"))
        self.stdout.write(self.style.NOTICE("=" * 70 + "\n"))

        if not a_modifier:
            self.stdout.write(self.style.SUCCESS(
                "✅ Aucune modification nécessaire. Toutes les dates sont déjà correctes.\n"
            ))
        else:
            for item in a_modifier:
                chrono = item['chrono']
                emoji = chrono.culture_emoji or '🌱'
                user = chrono.figure.user.username if chrono.figure else '?'
                fig_name = chrono.figure.name if chrono.figure else '?'
                ancien = item['ancienne_date'].strftime('%d/%m/%Y') if item['ancienne_date'] else '—'
                nouveau = item['nouvelle_date'].strftime('%d/%m/%Y')

                # Indicateur visuel
                if item['type_cycle'] == 'perenne':
                    marqueur = "🌳"
                else:
                    marqueur = "🌱"

                self.stdout.write(
                    f"{marqueur} #{chrono.id} {emoji} {chrono.culture_nom} "
                    f"({user} / {fig_name})\n"
                    f" ancienne : {ancien} (type={item['ancien_type']})\n"
                    f" nouvelle : {nouveau} (type={item['nouveau_type']}, source={item['source']})"
                )

        # ============================================================
        # Résumé
        # ============================================================
        self.stdout.write(self.style.NOTICE("\n" + "=" * 70))
        self.stdout.write(self.style.NOTICE("📊 RÉSUMÉ"))
        self.stdout.write(self.style.NOTICE("=" * 70))
        self.stdout.write(f" Traitées : {stats['traitees']}")
        self.stdout.write(f" Inchangées : {stats['inchangees']}")
        self.stdout.write(self.style.WARNING(
            f" À corriger : {stats['corrigees']}"
        ) if stats['corrigees'] else self.style.SUCCESS(
            f" À corriger : {stats['corrigees']}"
        ))
        self.stdout.write(f" Ignorées : {stats['ignorees']}")
        if stats['recoltees_ignorees']:
            self.stdout.write(f" Récoltées (skip) : {stats['recoltees_ignorees']}")

        # ============================================================
        # Application réelle
        # ============================================================
        if not a_modifier:
            return

        if not apply_mode:
            self.stdout.write(self.style.WARNING(
                "\n⚠️ MODE DRY-RUN : aucune modification appliquée."
            ))
            self.stdout.write(self.style.WARNING(
                " Relance avec --apply pour appliquer les changements.\n"
            ))
            return

        # Mode APPLY
        self.stdout.write(self.style.WARNING(
            f"\n⚙️ APPLICATION des {len(a_modifier)} modification(s)...\n"
        ))

        corrigees = 0
        with transaction.atomic():
            for item in a_modifier:
                chrono = item['chrono']
                chrono.date_recolte_prevue = item['nouvelle_date']
                chrono.type_cycle = item['nouveau_type']
                chrono.save(update_fields=['date_recolte_prevue', 'type_cycle'])
                corrigees += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ {corrigees} ChronologieCulture(s) corrigée(s) avec succès.\n"
        ))
