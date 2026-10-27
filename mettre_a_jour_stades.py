# vegetables_fruits/management/commands/mettre_a_jour_stades.py

from django.core.management.base import BaseCommand
from vegetables_fruits.models import ChronologieCulture


class Command(BaseCommand):
    help = 'Met à jour les stades des chronologies existantes'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🔄 Mise à jour des stades des chronologies..."))

        chronologies = ChronologieCulture.objects.all()
        mises_a_jour = 0

        # Mapping statut → stade
        stade_map = {
            'seme': 'seme',
            'levee': 'levee',
            'croissance': 'croissance',
            'floraison': 'floraison',
            'fructification': 'fructification',
            'pret': 'pret',
            'recolte': 'recolte',
        }

        for chrono in chronologies:
            if not chrono.stade_actuel:
                chrono.stade_actuel = stade_map.get(chrono.statut, 'seme')
                chrono.save()
                mises_a_jour += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {mises_a_jour} chronologie(s) mises à jour"))