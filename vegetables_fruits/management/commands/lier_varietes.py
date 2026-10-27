from django.core.management.base import BaseCommand
from vegetables_fruits.models import Fruit, Vegetable, Variete, Culture


class Command(BaseCommand):
    help = 'Lie les variétés aux fruits et légumes correspondants'

    def handle(self, *args, **options):
        self.stdout.write("🔄 Liaison des variétés aux fruits et légumes...")

        total_liees = 0

        # 🔹 Lier les variétés aux fruits
        for fruit in Fruit.objects.all():
            culture = Culture.objects.filter(fruit=fruit).first()
            if culture:
                varietes = Variete.objects.filter(culture=culture)
                if varietes.exists():
                    for variete in varietes:
                        fruit.varietes_m2m.add(variete)  # ✅ Utiliser le nouveau champ
                        total_liees += 1
                    self.stdout.write(f"✅ {varietes.count()} variété(s) liée(s) à {fruit.nom}")
                else:
                    self.stdout.write(f"⏭️ Aucune variété pour {fruit.nom}")
            else:
                self.stdout.write(f"⚠️ Culture non trouvée pour {fruit.nom}")

        # 🔹 Lier les variétés aux légumes
        for vegetable in Vegetable.objects.all():
            culture = Culture.objects.filter(vegetable=vegetable).first()
            if culture:
                varietes = Variete.objects.filter(culture=culture)
                if varietes.exists():
                    for variete in varietes:
                        vegetable.varietes_m2m.add(variete)  # ✅ Utiliser le nouveau champ
                        total_liees += 1
                    self.stdout.write(f"✅ {varietes.count()} variété(s) liée(s) à {vegetable.nom}")
                else:
                    self.stdout.write(f"⏭️ Aucune variété pour {vegetable.nom}")
            else:
                self.stdout.write(f"⚠️ Culture non trouvée pour {vegetable.nom}")

        self.stdout.write(self.style.SUCCESS(f"\n🎉 {total_liees} variété(s) liée(s) avec succès !"))