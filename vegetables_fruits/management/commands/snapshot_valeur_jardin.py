"""
Prend un snapshot mensuel de la valeur du jardin pour tous les utilisateurs.
À lancer 1x/mois (via cron ou manuellement).
Usage : python manage.py snapshot_valeur_jardin
"""
from datetime import date
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from vegetables_fruits.models import HistoriqueValeurJardin
from vegetables_fruits.services_economie import calculer_valeur_jardin


User = get_user_model()


class Command(BaseCommand):
    help = "Prend un snapshot mensuel de la valeur du jardin pour chaque utilisateur"

    def handle(self, *args, **options):
        # Premier jour du mois courant
        mois_courant = date.today().replace(day=1)

        total_users = User.objects.filter(is_active=True).count()
        traites = 0

        for user in User.objects.filter(is_active=True):
            try:
                data = calculer_valeur_jardin(user)
                HistoriqueValeurJardin.objects.update_or_create(
                    utilisateur=user,
                    mois=mois_courant,
                    defaults={
                        'valeur_potentielle': data['valeur_potentielle'],
                        'valeur_realisee': data['valeur_realisee'],
                        'nb_cultures': len(data.get('details_par_culture', [])),
                    }
                )
                traites += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️ {user.username}: {e}"))

        self.stdout.write(self.style.SUCCESS(
            f"✅ {traites}/{total_users} snapshots créés pour {mois_courant.strftime('%m/%Y')}"
        ))
