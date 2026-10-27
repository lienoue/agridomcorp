"""
Met à jour les taux de change via l'API exchangerate-api.com.
Fallback : garde les taux existants si l'API tombe.
Usage : python manage.py update_taux_change
"""
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from vegetables_fruits.models import TauxChange


API_URL = "https://api.exchangerate-api.com/v4/latest/EUR"


class Command(BaseCommand):
    help = "Met à jour les taux de change via l'API exchangerate-api.com"

    def handle(self, *args, **options):
        self.stdout.write("🔄 Récupération des taux...")

        try:
            resp = requests.get(API_URL, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            rates = data.get('rates', {})
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erreur API : {e}"))
            self.stdout.write(self.style.WARNING("⚠️ Les taux existants sont conservés"))
            return

        # On ne met à jour que les devises qu'on supporte
        devises_supportees = [d[0] for d in TauxChange.DEVISE_CHOICES]

        updated = 0
        skipped = 0

        for devise in devises_supportees:
            if devise == 'EUR':
                continue

            taux = rates.get(devise)
            if not taux:
                skipped += 1
                continue

            # ✅ Update en masse (1 requête SQL au lieu de N)
            count = TauxChange.objects.filter(devise=devise).update(
                taux_vs_eur=taux,
                source='api',
                date_maj=timezone.now(),
            )
            if count:
                updated += 1

        # ✅ Invalider le cache des taux
        from django.core.cache import cache
        for devise in devises_supportees:
            cache.delete(f"taux_change_{devise}")

        self.stdout.write(self.style.SUCCESS(
            f"✅ {updated} devises mises à jour, {skipped} ignorées "
            f"({timezone.now().strftime('%d/%m/%Y %H:%M')})"
        ))
