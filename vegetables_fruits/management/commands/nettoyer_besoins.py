from django.core.management.base import BaseCommand
from vegetables_fruits.models import BesoinsEau
from django.db.models import Count


class Command(BaseCommand):
    help = "Nettoie les doublons dans la table BesoinsEau en préservant les liens aux parcelles"

    def handle(self, *args, **kwargs):
        doublons = BesoinsEau.objects.values('culture').annotate(nb=Count('id')).filter(nb__gt=1)
        total_supprimes = 0
        total_gardes = 0

        self.stdout.write(self.style.WARNING(f"🔍 {doublons.count()} doublons trouvés. Nettoyage...\n"))

        for d in doublons:
            culture = d['culture']
            lignes = list(BesoinsEau.objects.filter(culture=culture).order_by('id'))

            # On sépare les lignes liées à une parcelle et celles globales
            lignes_avec_parcelle = [l for l in lignes if l.parcelle is not None]
            lignes_sans_parcelle = [l for l in lignes if l.parcelle is None]

            # On garde TOUTES les lignes liées à une parcelle
            total_gardes += len(lignes_avec_parcelle)

            # Pour les lignes sans parcelle, on n'en garde qu'une
            if lignes_sans_parcelle:
                a_supprimer = lignes_sans_parcelle[1:]

                for ligne in a_supprimer:
                    ligne.delete()
                    total_supprimes += 1

                self.stdout.write(
                    self.style.SUCCESS(f"✅ {culture.ljust(20)} : {len(a_supprimer)} doublon(s) supprimé(s)."))

        self.stdout.write(self.style.SUCCESS(
            f"\n🎉 Bilan : {total_supprimes} lignes supprimées, {total_gardes} lignes conservées (liées à des parcelles)."))