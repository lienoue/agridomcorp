from django.core.management.base import BaseCommand
from vegetables_fruits.views import verifier_alertes_meteo

class Command(BaseCommand):
    help = 'Vérifie les conditions météo et génère des alertes pour tous les utilisateurs'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Lancement de la vérification des alertes météo...")
        alertes_crees = verifier_alertes_meteo()
        self.stdout.write(self.style.SUCCESS(f"✅ {alertes_crees} alerte(s) créée(s)"))
