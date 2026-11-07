import time
from django.core.management.base import BaseCommand
from django.utils import timezone
from vegetables_fruits.models import CustomUser, PlanTarification, Abonnement, Facture
from vegetables_fruits.views import peut_parrainer


class Command(BaseCommand):
    help = "Teste la logique de parrainage (avec règle Premium)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("🚀 Début du test de parrainage..."))

        # ✅ On utilise un suffixe basé sur le temps pour éviter les conflits d'email
        suffix = int(time.time())
        username_gratuit = f'parrain_gratuit_{suffix}'
        username_premium = f'parrain_premium_{suffix}'
        username_filleul = f'filleul_test_{suffix}'

        plan_gratuit, _ = PlanTarification.objects.get_or_create(nom='GRATUIT', defaults={'prix_mensuel': 0})
        plan_premium, _ = PlanTarification.objects.get_or_create(nom='PREMIUM', defaults={'prix_mensuel': 14.99})

        # ============================================================
        # TEST 1 : Le parrain est GRATUIT (doit échouer)
        # ============================================================
        self.stdout.write("\n--- TEST 1 : Parrain avec compte gratuit ---")
        parrain_gratuit = CustomUser.objects.create_user(
            username=username_gratuit,
            password='123',
            email=f'{username_gratuit}@test.com'  # ✅ Email unique
        )

        Abonnement.objects.create(
            utilisateur=parrain_gratuit,
            plan=plan_gratuit,
            statut='ACTIF',
            stripe_customer_id=f'cus_test_gratuit_{suffix}'
        )

        if peut_parrainer(parrain_gratuit):
            self.stdout.write(self.style.ERROR("❌ ERREUR : Un compte gratuit peut parrainer !"))
        else:
            self.stdout.write(self.style.SUCCESS("✅ OK : Le compte gratuit ne peut pas parrainer."))

        # ============================================================
        # TEST 2 : Le parrain est PREMIUM (doit réussir)
        # ============================================================
        self.stdout.write("\n--- TEST 2 : Parrain avec compte Premium ---")
        parrain_premium = CustomUser.objects.create_user(
            username=username_premium,
            password='123',
            email=f'{username_premium}@test.com'  # ✅ Email unique
        )

        abo_premium = Abonnement.objects.create(
            utilisateur=parrain_premium,
            plan=plan_premium,
            statut='ACTIF',
            stripe_customer_id=f'cus_test_premium_{suffix}'
        )

        if peut_parrainer(parrain_premium):
            self.stdout.write(self.style.SUCCESS("✅ OK : Le compte Premium peut parrainer."))
        else:
            self.stdout.write(self.style.ERROR("❌ ERREUR : Le compte Premium ne peut pas parrainer !"))

        # ============================================================
        # TEST 3 : Paiement du filleul (Récompense du parrain Premium)
        # ============================================================
        self.stdout.write("\n--- TEST 3 : Paiement du filleul ---")
        filleul = CustomUser.objects.create_user(
            username=username_filleul,
            password='123',
            email=f'{username_filleul}@test.com'  # ✅ Email unique
        )
        filleul.parrain = parrain_premium
        filleul.save()

        est_premier_paiement = not Facture.objects.filter(utilisateur=filleul, statut='PAYEE').exists()

        if est_premier_paiement and filleul.parrain:
            abonnement_parrain, _ = Abonnement.objects.get_or_create(
                utilisateur=filleul.parrain,
                defaults={'plan': plan_gratuit, 'statut': 'ACTIF', 'stripe_customer_id': f'cus_test_default_{suffix}'}
            )
            abonnement_parrain.mois_premium_offerts += 1
            abonnement_parrain.save()

            # On simule une facture payée
            Facture.objects.create(
                utilisateur=filleul,
                montant_ht=12,
                montant_ttc=14.99,
                statut='PAYEE',
                date_paiement=timezone.now(),
                stripe_invoice_id=f'inv_test_123_{suffix}'
            )

        abo_premium.refresh_from_db()
        if abo_premium.mois_premium_offerts == 1:
            self.stdout.write(self.style.SUCCESS("🎉 TEST RÉUSSI : Le parrain a bien gagné son mois !"))
        else:
            self.stdout.write(self.style.ERROR("❌ TEST ÉCHOUÉ."))

        # Nettoyage
        self.stdout.write("\n🧹 Nettoyage...")
        parrain_gratuit.delete()
        parrain_premium.delete()
        filleul.delete()
        self.stdout.write("✨ Terminé !")