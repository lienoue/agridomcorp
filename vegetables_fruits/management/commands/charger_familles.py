import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from vegetables_fruits.models import ConseilsFamille


class Command(BaseCommand):
    help = "Charge les familles botaniques depuis data/familles.json"

    def handle(self, *args, **options):
        json_path = os.path.join(
            settings.BASE_DIR,
            'vegetables_fruits',
            'data',
            'familles.json'
        )

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"❌ Fichier introuvable : {json_path}"))
            return

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                familles = json.load(f)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"❌ Erreur JSON : {e}"))
            return

        self.stdout.write(f"📋 {len(familles)} familles à charger...")

        creees = 0
        mises_a_jour = 0

        for data in familles:
            nom = data.get('nom')
            if not nom:
                self.stdout.write(self.style.WARNING(f"⚠️ Famille sans nom ignorée"))
                continue

            famille, created = ConseilsFamille.objects.update_or_create(
                nom=nom,
                defaults={
                    'emoji': data.get('emoji', ''),
                    'temperature_min': data.get('temperature_min'),
                    'temperature_optimale_min': data.get('temperature_optimale_min'),
                    'temperature_optimale_max': data.get('temperature_optimale_max'),
                    'temperature_max': data.get('temperature_max'),
                    'duree_culture_min_jours': data.get('duree_culture_min_jours'),
                    'duree_culture_max_jours': data.get('duree_culture_max_jours'),
                    'methode_plantation': data.get('methode_plantation', ''),
                    'hivernage': data.get('hivernage', ''),
                    'conseils_climat': data.get('conseils_climat', ''),
                    'conseils_plantation': data.get('conseils_plantation', ''),
                    'conseils_arrosage': data.get('conseils_arrosage', ''),
                    'conseils_fertilisation': data.get('conseils_fertilisation', ''),
                    'conseils_protection': data.get('conseils_protection', ''),
                    'conseils_recolte': data.get('conseils_recolte', ''),
                    'conseils_conservation': data.get('conseils_conservation', ''),
                }
            )

            if created:
                creees += 1
                self.stdout.write(f" ✅ {famille.emoji} {famille.nom} (créée)")
            else:
                mises_a_jour += 1
                self.stdout.write(f" 🔄 {famille.emoji} {famille.nom} (mise à jour)")

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Terminé !"))
        self.stdout.write(f" Créées : {creees}")
        self.stdout.write(f" Mises à jour : {mises_a_jour}")
        self.stdout.write(f" Total en base : {ConseilsFamille.objects.count()}")