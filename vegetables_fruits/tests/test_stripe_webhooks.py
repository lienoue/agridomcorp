import pytest
import json
from unittest.mock import patch, MagicMock
from django.urls import reverse
from vegetables_fruits.models import CustomUser, PlanTarification, Abonnement


@pytest.mark.django_db
class TestStripeWebhooks:

    @pytest.fixture
    def abonnement_actif(self):
        """Crée un utilisateur avec un abonnement actif"""
        user = CustomUser.objects.create_user(username='abo_user', email='abo@test.com', password='Password123!')
        plan, _ = PlanTarification.objects.get_or_create(nom='PREMIUM', defaults={'prix_mensuel': 15})
        abo = Abonnement.objects.create(
            utilisateur=user,
            plan=plan,
            statut='ACTIF',
            stripe_subscription_id='sub_fake_123',
            stripe_customer_id='cus_fake_123'
        )
        return abo

    @patch('stripe.Webhook.construct_event')
    def test_webhook_annulation_abonnement(self, mock_construct_event, client, abonnement_actif):
        """Vérifie que le webhook d'annulation passe bien l'abonnement en 'ANNULE'"""

        # 1. On simule l'événement Stripe (customer.subscription.deleted)
        mock_event = {
            'type': 'customer.subscription.deleted',
            'data': {
                'object': {
                    'id': 'sub_fake_123'
                }
            }
        }
        mock_construct_event.return_value = mock_event

        # 2. On envoie la requête au webhook
        url = reverse('vegetables_fruits:stripe_webhook')
        response = client.post(
            url,
            data=json.dumps(mock_event),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='fake_signature'
        )

        # 3. On vérifie que le serveur répond 200 (bien reçu)
        assert response.status_code == 200

        # 4. On vérifie que l'abonnement a été annulé en base
        abonnement_actif.refresh_from_db()
        assert abonnement_actif.statut == 'ANNULE'
        assert abonnement_actif.date_fin is not None

    @patch('stripe.Webhook.construct_event')
    def test_webhook_echec_paiement(self, mock_construct_event, client, abonnement_actif):
        """Vérifie que le webhook d'échec de paiement passe l'abonnement en 'EXPIRE'"""

        # 1. On simule l'événement Stripe (invoice.payment_failed)
        mock_event = {
            'type': 'invoice.payment_failed',
            'data': {
                'object': {
                    'subscription': 'sub_fake_123'
                }
            }
        }
        mock_construct_event.return_value = mock_event

        # 2. On envoie la requête
        url = reverse('vegetables_fruits:stripe_webhook')
        response = client.post(
            url,
            data=json.dumps(mock_event),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='fake_signature'
        )

        assert response.status_code == 200

        # 3. On vérifie que l'abonnement est expiré
        abonnement_actif.refresh_from_db()
        assert abonnement_actif.statut == 'EXPIRE'

    @patch('stripe.Webhook.construct_event')
    def test_webhook_resiliation_programmee(self, mock_construct_event, client, abonnement_actif):
        """Vérifie que le webhook de mise à jour détecte une résiliation programmée"""

        # 1. On simule l'événement Stripe (customer.subscription.updated)
        mock_event = {
            'type': 'customer.subscription.updated',
            'data': {
                'object': {
                    'id': 'sub_fake_123',
                    'status': 'active',
                    'cancel_at': 1735689600,  # Un timestamp futur
                    'canceled_at': 1735689600,
                    'items': {
                        'data': [
                            {'current_period_end': 1735689600}
                        ]
                    }
                }
            }
        }
        mock_construct_event.return_value = mock_event

        # 2. On envoie la requête
        url = reverse('vegetables_fruits:stripe_webhook')
        response = client.post(
            url,
            data=json.dumps(mock_event),
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='fake_signature'
        )

        assert response.status_code == 200

        # 3. On vérifie que la résiliation programmée est active
        abonnement_actif.refresh_from_db()
        assert abonnement_actif.resiliation_programmee is True
        assert abonnement_actif.date_fin_prevue is not None