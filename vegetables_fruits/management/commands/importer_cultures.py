from django.core.management.base import BaseCommand
from vegetables_fruits.models import Culture, Fruit, Vegetable


class Command(BaseCommand):
    help = 'Importe les cultures de base à partir des fruits et légumes existants'

    def handle(self, *args, **options):
        total_importees = 0

        self.stdout.write("🔄 Importation des cultures en cours...")

        # ✅ Importer les fruits existants
        for fruit in Fruit.objects.all():
            culture, created = Culture.objects.get_or_create(
                nom=fruit.nom,
                defaults={
                    'emoji': fruit.get_emoji(),
                    'type_culture': 'fruit',
                    'jours_pousse': fruit.jours_recolte or 60,
                    'saison_plantation': fruit.saison,
                    'conseils': f"Culture issue du fruit '{fruit.nom}'"
                }
            )
            if created:
                culture.fruit = fruit
                culture.save()
                total_importees += 1
                self.stdout.write(f"✅ Culture importée : {fruit.nom} (fruit)")
            else:
                self.stdout.write(f"⏭️ Culture déjà existante : {fruit.nom} (fruit)")

        # ✅ Importer les légumes existants
        for vegetable in Vegetable.objects.all():
            culture, created = Culture.objects.get_or_create(
                nom=vegetable.nom,
                defaults={
                    'emoji': vegetable.get_emoji(),
                    'type_culture': 'legume',
                    'jours_pousse': vegetable.jours_recolte or 60,
                    'saison_plantation': vegetable.saison,
                    'conseils': f"Culture issue du légume '{vegetable.nom}'"
                }
            )
            if created:
                culture.vegetable = vegetable
                culture.save()
                total_importees += 1
                self.stdout.write(f"✅ Culture importée : {vegetable.nom} (légume)")
            else:
                self.stdout.write(f"⏭️ Culture déjà existante : {vegetable.nom} (légume)")

        self.stdout.write(self.style.SUCCESS(f"\n🎉 {total_importees} culture(s) importée(s) avec succès !"))