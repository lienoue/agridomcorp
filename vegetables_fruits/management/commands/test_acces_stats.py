from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta

from vegetables_fruits.models import CustomUser, PlanTarification, Abonnement


class Command(BaseCommand):
    help = "Teste la logique d'accès aux statistiques avancées"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("🚀 Début du test d'accès aux statistiques...\n"))

        # Nettoyage des anciens comptes de test (par précaution)
        CustomUser.objects.filter(username__startswith='test_stats_').delete()

        # On s'assure que les plans existent
        plan_premium, _ = PlanTarification.objects.get_or_create(
            nom='PREMIUM',
            defaults={'prix_mensuel': 14.99, 'actif': True}
        )
        plan_enseignant, _ = PlanTarification.objects.get_or_create(
            nom='ENSEIGNANT',
            defaults={'prix_mensuel': 15.99, 'actif': True}
        )

        # ✅ On force le nom de serveur pour éviter l'erreur ALLOWED_HOSTS
        client = Client(SERVER_NAME='localhost')
        url = reverse('vegetables_fruits:statistiques_avancees')

        # ============================================================
        # TEST 1 : Mineur (mode_junior)
        # ============================================================
        self.stdout.write("--- TEST 1 : Mineur (mode junior) ---")
        mineur = CustomUser.objects.create_user(
            username='test_stats_mineur',
            password='password123',
            email=f'mineur_{timezone.now().timestamp()}@test.com',  # Email unique
            birth_date=date.today() - timedelta(days=365 * 15)
        )
        mineur.mode_junior = True
        mineur.save()

        client.force_login(mineur)
        response = client.get(url)

        if response.status_code == 302 and 'dashboard' in response.url:
            self.stdout.write(self.style.SUCCESS("✅ OK : Le mineur est redirigé vers son dashboard."))
        else:
            self.stdout.write(self.style.ERROR(
                f"❌ ERREUR : Le mineur a obtenu le code {response.status_code} au lieu d'une redirection."))

        # ============================================================
        # TEST 2 : Adulte Gratuit
        # ============================================================
        self.stdout.write("\n--- TEST 2 : Adulte sans abonnement ---")
        adulte_gratuit = CustomUser.objects.create_user(
            username='test_stats_adulte_gratuit',
            password='password123',
            email=f'gratuit_{timezone.now().timestamp()}@test.com',
            birth_date=date.today() - timedelta(days=365 * 30)
        )

        client.force_login(adulte_gratuit)
        response = client.get(url)

        if response.status_code == 302 and 'tarification' in response.url:
            self.stdout.write(self.style.SUCCESS("✅ OK : L'adulte gratuit est redirigé vers la tarification."))
        else:
            self.stdout.write(self.style.ERROR(
                f"❌ ERREUR : L'adulte gratuit a obtenu le code {response.status_code} au lieu d'être redirigé vers la tarification."))

        # ============================================================
        # TEST 3 : Adulte Premium
        # ============================================================
        self.stdout.write("\n--- TEST 3 : Adulte avec abonnement Premium ---")
        adulte_premium = CustomUser.objects.create_user(
            username='test_stats_adulte_premium',
            password='password123',
            email=f'premium_{timezone.now().timestamp()}@test.com',
            birth_date=date.today() - timedelta(days=365 * 30)
        )
        Abonnement.objects.create(
            utilisateur=adulte_premium,
            plan=plan_premium,
            statut='ACTIF',
            stripe_customer_id='cus_test_premium'
        )

        client.force_login(adulte_premium)
        response = client.get(url)

        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS("✅ OK : L'adulte Premium a bien accès à la page (Code 200)."))
        else:
            self.stdout.write(self.style.ERROR(
                f"❌ ERREUR : L'adulte Premium a obtenu le code {response.status_code} au lieu de 200."))

        # ============================================================
        # TEST 4 : Enseignant (avec abonnement ENSEIGNANT)
        # ============================================================
        self.stdout.write("\n--- TEST 4 : Enseignant ---")
        enseignant = CustomUser.objects.create_user(
            username='test_stats_enseignant',
            password='password123',
            email=f'enseignant_{timezone.now().timestamp()}@test.com',
            birth_date=date.today() - timedelta(days=365 * 40)
        )
        enseignant.is_enseignant = True
        enseignant.save()

        Abonnement.objects.create(
            utilisateur=enseignant,
            plan=plan_enseignant,
            statut='ACTIF',
            stripe_customer_id='cus_test_enseignant'
        )

        client.force_login(enseignant)
        response = client.get(url)

        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS("✅ OK : L'enseignant a bien accès à la page (Code 200)."))
        else:
            self.stdout.write(
                self.style.ERROR(f"❌ ERREUR : L'enseignant a obtenu le code {response.status_code} au lieu de 200."))

        # ============================================================
        # NETTOYAGE
        # ============================================================
        self.stdout.write("\n🧹 Nettoyage des comptes de test...")
        mineur.delete()
        adulte_gratuit.delete()
        adulte_premium.delete()
        enseignant.delete()

        self.stdout.write(self.style.SUCCESS("\n🎉 Tests terminés !"))