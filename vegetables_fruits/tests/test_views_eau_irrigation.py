import pytest
import json
from django.urls import reverse
from vegetables_fruits.models import (
    CustomUser, GeometricFigure, Parcelle, BesoinsEau, PlanTarification, Abonnement
)


@pytest.mark.django_db
class TestBesoinsEauIrrigation:

    @pytest.fixture
    def user_premium(self):
        user = CustomUser.objects.create_user(username='eau_user', email='eau@test.com', password='Password123!')
        plan, _ = PlanTarification.objects.get_or_create(nom='PREMIUM', defaults={'prix_mensuel': 15})
        Abonnement.objects.create(utilisateur=user, plan=plan, statut='ACTIF')
        return user

    @pytest.fixture
    def figure(self, user_premium):
        """Crée une parcelle avec un point GPS et un crop (Tomate)"""
        fig = GeometricFigure.objects.create(
            user=user_premium,
            name="Parcelle Test Eau",
            figure_type="potager",
            geojson_data={"type": "FeatureCollection", "features": []},
            adresse_lat=48.8566,
            adresse_lng=2.3522,
            crops=[
                {"name": "Tomate", "emoji": "🍅", "vegetable_id": 1, "lat": 48.85, "lng": 2.35}
            ]
        )
        # On crée aussi la parcelle associée (nécessaire pour l'irrigation)
        Parcelle.objects.create(
            utilisateur=user_premium,
            figure=fig,
            nom="Parcelle Test Eau",
            surface_m2=10,
            irrigation_type='goutte_a_goutte'
        )
        return fig

    def test_besoins_eau_acces(self, client, user_premium, figure):
        """Vérifie que la page besoins_eau s'affiche pour un Premium"""
        # ✅ On crée d'abord le besoin en eau pour que la vue puisse le trouver
        BesoinsEau.objects.create(
            culture="Tomate",
            besoin_litres_par_m2=5,
            frequence_arrosage_jours=3,
        )

        client.force_login(user_premium)
        url = reverse('vegetables_fruits:besoins_eau') + f"?figure_id={figure.id}"
        response = client.get(url)

        assert response.status_code == 200

        # On vérifie que le contexte contient bien les cultures
        assert 'cultures' in response.context
        # ✅ On vérifie que la Tomate est bien trouvée
        assert 'Tomate' in response.context['cultures']

    def test_plan_irrigation_acces(self, client, user_premium, figure):
        """Vérifie que la page plan_irrigation s'affiche pour un Premium"""
        client.force_login(user_premium)
        url = reverse('vegetables_fruits:plan_irrigation')
        response = client.get(url)

        assert response.status_code == 200
        assert 'plan_parcelles' in response.context

    def test_plan_irrigation_calcul_economie(self, client, user_premium, figure):
        """Vérifie que l'économie d'eau est calculée pour le goutte-à-goutte"""
        # On ajoute un besoin en eau pour la Tomate
        BesoinsEau.objects.create(
            culture="Tomate",
            besoin_litres_par_m2=5,
            frequence_arrosage_jours=3,
            parcelle=Parcelle.objects.filter(utilisateur=user_premium).first()
        )

        client.force_login(user_premium)
        url = reverse('vegetables_fruits:plan_irrigation')
        response = client.get(url)

        # Vérifie que l'économie est calculée (pas None)
        assert response.context.get('economie_totale') is not None
        # Vérifie qu'on a bien trouvé 1 parcelle
        assert len(response.context['plan_parcelles']) == 1
        # Vérifie que la logique d'économie goutte-à-goutte est passée
        assert 'economie_type' in response.context['plan_parcelles'][0]

    def test_plan_irrigation_sans_parcelle(self, client, user_premium):
        """Vérifie que la page s'affiche sans erreur si l'utilisateur n'a aucune parcelle"""
        client.force_login(user_premium)
        url = reverse('vegetables_fruits:plan_irrigation')
        response = client.get(url)

        assert response.status_code == 200
        assert len(response.context['plan_parcelles']) == 0

    @pytest.mark.django_db
    class TestFigureDetail:

        @pytest.fixture
        def user_premium(self):
            user = CustomUser.objects.create_user(username='fig_user', email='fig@test.com', password='Password123!')
            plan, _ = PlanTarification.objects.get_or_create(nom='PREMIUM', defaults={'prix_mensuel': 15})
            Abonnement.objects.create(utilisateur=user, plan=plan, statut='ACTIF')
            return user

        @pytest.fixture
        def figure(self, user_premium):
            """Crée une parcelle simple avec un polygone et une culture"""
            return GeometricFigure.objects.create(
                user=user_premium,
                name="Parcelle Test Detail",
                figure_type="potager",
                geojson_data={
                    "type": "FeatureCollection",
                    "features": [{
                        "type": "Feature",
                        "geometry": {"type": "Polygon",
                                     "coordinates": [[[2.35, 48.85], [2.36, 48.85], [2.36, 48.86], [2.35, 48.85]]]},
                        "properties": {}
                    }]
                },
                adresse_lat=48.8566,
                adresse_lng=2.3522,
                crops=[
                    {"name": "Tomate", "emoji": "🍅", "lat": 48.85, "lng": 2.35, "vegetable_id": 1}
                ]
            )

        def test_figure_detail_acces(self, client, user_premium, figure):
            """Vérifie que la page détail d'une parcelle s'affiche correctement"""
            client.force_login(user_premium)
            url = reverse('vegetables_fruits:figure_detail', args=[figure.id])
            response = client.get(url)

            assert response.status_code == 200
            assert response.context['figure'].id == figure.id
            assert len(response.context['enriched_crops']) == 1
            assert response.context['enriched_crops'][0]['name'] == 'Tomate'

        def test_figure_detail_acces_interdit(self, client, figure):
            """Vérifie qu'un autre utilisateur ne peut pas voir cette parcelle"""
            autre_user = CustomUser.objects.create_user(username='autre', email='autre@test.com',
                                                        password='Password123!')
            client.force_login(autre_user)

            url = reverse('vegetables_fruits:figure_detail', args=[figure.id])
            response = client.get(url)

            # Django renvoie une 404 car get_object_or_404 filtre par user
            assert response.status_code == 404

    @pytest.mark.django_db
    class TestEditFigure:

        @pytest.fixture
        def user_premium(self):
            user = CustomUser.objects.create_user(username='edit_user', email='edit@test.com', password='Password123!')
            plan, _ = PlanTarification.objects.get_or_create(nom='PREMIUM', defaults={'prix_mensuel': 15})
            Abonnement.objects.create(utilisateur=user, plan=plan, statut='ACTIF')
            return user

        @pytest.fixture
        def figure(self, user_premium):
            return GeometricFigure.objects.create(
                user=user_premium,
                name="Parcelle à modifier",
                figure_type="potager",
                geojson_data={"type": "FeatureCollection", "features": []},
                adresse_lat=48.8566,
                adresse_lng=2.3522,
                crops=[]
            )

        def test_edit_figure_get(self, client, user_premium, figure):
            """Vérifie que la page de modification s'affiche bien"""
            client.force_login(user_premium)
            url = reverse('vegetables_fruits:edit_figure', args=[figure.id])
            response = client.get(url)

            assert response.status_code == 200
            assert response.context['figure'].id == figure.id
            assert 'fruits' in response.context
            assert 'vegetables' in response.context

        def test_edit_figure_ajout_culture(self, client, user_premium, figure):
            """Vérifie qu'on peut ajouter une culture via le POST"""
            client.force_login(user_premium)
            url = reverse('vegetables_fruits:edit_figure', args=[figure.id])

            # On simule le POST du formulaire avec une nouvelle culture
            nouvelles_cultures = [
                {"name": "Carotte", "emoji": "🥕", "lat": 48.85, "lng": 2.35, "vegetable_id": 2}
            ]

            response = client.post(url, {
                'name': figure.name,
                'description': 'Ma description',
                'crops_data': json.dumps(nouvelles_cultures),
                'sol_mode': 'manuel',
                'type_sol': 'limoneux',
                'exposition': 'plein_soleil',
            })

            # Doit rediriger vers la page détail
            assert response.status_code == 302

            # On vérifie que la culture a bien été ajoutée en base
            figure.refresh_from_db()
            assert len(figure.crops) == 1
            assert figure.crops[0]['name'] == 'Carotte'