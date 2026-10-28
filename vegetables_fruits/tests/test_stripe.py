import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from vegetables_fruits.models import CustomUser, PlanTarification, Abonnement


@pytest.mark.django_db
class TestStripe:

    @pytest.fixture
    def user_premium(self, client):
        """Crée un utilisateur avec un abonnement Premium actif"""
        user = CustomUser.objects.create_user(username='stripe_user', email='stripe@test.com', password='Password123!')
        plan, _ = PlanTarification.objects.get_or_create(
            nom='PREMIUM',
            defaults={
                'prix_mensuel': 15,
                'max_parcelles': 50,
                'stripe_price_id_mensuel': 'price_fake_123'  # <-- L'ajout est ici
            }
        )
        Abonnement.objects.create(utilisateur=user, plan=plan, statut='ACTIF')
        client.force_login(user)
        return user

    # ✅ On mocke la création de session ET la création du client Stripe
    @patch('stripe.Customer.create')
    @patch('stripe.checkout.Session.create')
    def test_creation_session_paiement(self, mock_stripe_create, mock_customer_create, client, user_premium):
        """Vérifie que la vue de paiement appelle bien Stripe et redirige l'utilisateur"""

        # 1. On simule la création du client Stripe
        mock_customer = MagicMock()
        mock_customer.id = "cus_fake_123"
        mock_customer_create.return_value = mock_customer

        # 2. On simule la réponse de Stripe Checkout
        mock_session = MagicMock()
        mock_session.url = "https://checkout.stripe.com/fake-session"
        mock_stripe_create.return_value = mock_session

        url = reverse('vegetables_fruits:create_checkout_session')

        # 3. On simule le clic sur le bouton "S'abonner"
        response = client.post(url, {
            'plan': 'PREMIUM',
            'frequence': 'MENSUEL'
        })

        # 4. On vérifie que l'utilisateur est redirigé vers Stripe
        assert response.status_code == 302
        assert response.url == "https://checkout.stripe.com/fake-session"

        # 5. On vérifie que Stripe a bien été appelé avec les bons paramètres
        mock_stripe_create.assert_called_once()
        kwargs = mock_stripe_create.call_args.kwargs
        assert kwargs['mode'] == 'subscription'
        assert kwargs['metadata']['user_id'] == user_premium.id

    @patch('stripe.checkout.Session.retrieve')
    def test_abonnement_succes(self, mock_stripe_retrieve, client, user_premium):
        """Vérifie que la page de succès active bien l'abonnement en base"""
        # On supprime l'abonnement pour simuler un premier achat
        Abonnement.objects.filter(utilisateur=user_premium).delete()

        # 1. On simule la réponse de Stripe (paiement réussi)
        mock_session = MagicMock()
        mock_session.payment_status = 'paid'
        mock_session.metadata = {
            'user_id': str(user_premium.id),
            'plan_id': str(PlanTarification.objects.get(nom='PREMIUM').id),
            'frequence': 'MENSUEL'
        }
        mock_session.customer = 'cus_fake123'
        mock_session.subscription = 'sub_fake123'
        mock_stripe_retrieve.return_value = mock_session

        # 2. L'utilisateur arrive sur la page de succès
        url = reverse('vegetables_fruits:abonnement_succes')
        response = client.get(url, {'session_id': 'fake_session_id'})

        # 3. On vérifie qu'il est redirigé vers son profil
        assert response.status_code == 302
        assert reverse('vegetables_fruits:profile') in response.url

        # 4. On vérifie que l'abonnement a bien été créé en base
        assert Abonnement.objects.filter(utilisateur=user_premium, statut='ACTIF').exists()