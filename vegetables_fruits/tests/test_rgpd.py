import pytest
from django.urls import reverse
from vegetables_fruits.models import CustomUser, GeometricFigure


@pytest.mark.django_db
class TestRGPD:

    @pytest.fixture
    def user_rgpd(self, client):
        """Crée un utilisateur de test connecté"""
        user = CustomUser.objects.create_user(
            username='rgpd_user',
            email='rgpd@test.com',
            password='Password123!'
        )
        client.force_login(user)
        return user

    def test_export_donnees_zip(self, client, user_rgpd):
        """Vérifie que l'export génère bien un fichier ZIP"""
        # Créer une fausse parcelle pour l'utilisateur
        GeometricFigure.objects.create(
            user=user_rgpd,
            name="Parcelle Test",
            geojson_data={"type": "FeatureCollection", "features": []}
        )

        url = reverse('vegetables_fruits:exporter_mes_donnees')
        response = client.get(url)

        # On vérifie que c'est un fichier ZIP
        assert response.status_code == 200
        assert response['Content-Type'] in ['application/zip', 'application/x-zip-compressed']
        assert 'attachment; filename=' in response['Content-Disposition']

    def test_supprimer_compte(self, client, user_rgpd):
        """Vérifie que la suppression anonymise bien le compte"""
        url = reverse('vegetables_fruits:supprimer_mon_compte')

        # On simule la soumission du formulaire avec le mot de passe
        response = client.post(url, {
            'mot_de_passe': 'Password123!',
            'confirmation': 'SUPPRIMER'
        })

        # L'utilisateur doit être redirigé vers l'accueil
        assert response.status_code == 302

        # On vérifie en base que le compte a été anonymisé
        user_rgpd.refresh_from_db()
        assert user_rgpd.is_active is False
        assert user_rgpd.username.startswith('anonyme_')
        assert user_rgpd.email.startswith('deleted_')