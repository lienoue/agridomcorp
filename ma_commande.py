from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description de ma commande'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('✅ Commande exécutée !'))