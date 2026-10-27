"""
Initialise les devises avec des taux par défaut (fallback).
Les taux seront mis à jour par `update_taux_change`.
Usage : python manage.py seed_taux_change
"""
from django.core.management.base import BaseCommand
from vegetables_fruits.models import TauxChange


TAUX_DEFAUT = [
    ('EUR', 1.0, '€', 'apres'),
    ('USD', 1.08, '$', 'avant'),
    ('GBP', 0.85, '£', 'avant'),
    ('CHF', 0.95, 'CHF', 'apres'),
    ('CAD', 1.47, 'C$', 'avant'),
    ('XOF', 655.957, 'CFA', 'apres'),
    ('XAF', 655.957, 'FCFA', 'apres'),
    ('MAD', 10.80, 'DH', 'apres'),
    ('DZD', 145.0, 'DA', 'apres'),
    ('TND', 3.40, 'DT', 'apres'),
    ('JPY', 162.0, '¥', 'avant'),
    ('CNY', 7.80, '¥', 'avant'),
    ('BRL', 6.20, 'R$', 'avant'),
    ('MXN', 21.50, '$', 'avant'),
    ('AUD', 1.65, 'A$', 'avant'),
    ('INR', 91.0, '₹', 'avant'),
    ('ZAR', 19.50, 'R', 'avant'),
]


class Command(BaseCommand):
    help = "Initialise les devises avec des taux par défaut"

    def handle(self, *args, **options):
        crees = 0
        for devise, taux, symbole, position in TAUX_DEFAUT:
            obj, created = TauxChange.objects.get_or_create(
                devise=devise,
                defaults={
                    'taux_vs_eur': taux,
                    'symbole': symbole,
                    'position_symbole': position,
                    'source': 'defaut',
                }
            )
            if created:
                crees += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ {crees} devises initialisées, {TauxChange.objects.count()} au total"
        ))