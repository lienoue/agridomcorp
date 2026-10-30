import pytest
from django.urls import reverse
from vegetables_fruits.models import (
    CustomUser, CategorieForum, SujetForum, MessageForum, SignalementForum,
    Classe, Eleve, ForumAdulteCategorie, ForumAdulteSujet, MessageForumAdulte,
    PlanTarification, Abonnement
)


@pytest.mark.django_db
class TestForumEcole:
    """Tests pour le forum réservé aux écoles (élèves + enseignants)."""

    @pytest.fixture
    def classe(self):
        """Crée une classe et un enseignant"""
        enseignant = CustomUser.objects.create_user(
            username='prof', email='prof@test.com', password='Password123!', is_enseignant=True
        )
        return Classe.objects.create(nom='Classe Test', enseignant=enseignant)

    @pytest.fixture
    def eleve1(self, classe):
        """Crée un élève dans une classe"""
        user = CustomUser.objects.create_user(username='eleve1', email='e1@test.com', password='Password123!')
        Eleve.objects.create(user=user, classe=classe)
        return user

    @pytest.fixture
    def eleve2(self, classe):
        """Crée un deuxième élève dans la même classe"""
        user = CustomUser.objects.create_user(username='eleve2', email='e2@test.com', password='Password123!')
        Eleve.objects.create(user=user, classe=classe)
        return user

    @pytest.fixture
    def categorie_ecole(self):
        return CategorieForum.objects.create(nom="Jardinage École", description="Pour les élèves")

    def test_creation_sujet_ecole(self, client, eleve1, categorie_ecole):
        """Un élève peut créer un sujet"""
        client.force_login(eleve1)
        url = reverse('vegetables_fruits:forum_nouveau_sujet', args=[categorie_ecole.id])

        response = client.post(url, {
            'titre': 'Mon premier semis',
            'contenu': 'J\'ai planté des tomates aujourd\'hui !'
        })

        assert response.status_code == 302
        sujet = SujetForum.objects.first()
        assert sujet is not None
        assert sujet.titre == 'Mon premier semis'
        assert sujet.auteur == eleve1
        assert MessageForum.objects.filter(sujet=sujet).count() == 1

    def test_reponse_sujet_ecole(self, client, eleve1, eleve2, categorie_ecole):
        """Un élève peut répondre au sujet d'un autre élève"""
        sujet = SujetForum.objects.create(titre="Sujet", contenu="Init", auteur=eleve1, categorie=categorie_ecole)
        MessageForum.objects.create(sujet=sujet, auteur=eleve1, contenu="Init")

        client.force_login(eleve2)
        url = reverse('vegetables_fruits:forum_repondre', args=[sujet.id])

        response = client.post(url, {'contenu': 'Super idée !'})

        assert response.status_code == 302
        assert sujet.messages.count() == 2
        assert sujet.messages.last().contenu == 'Super idée !'

    def test_blocage_particulier_forum_ecole(self, client):
        """Un particulier (sans classe) ne doit pas pouvoir accéder au forum école"""
        particulier = CustomUser.objects.create_user(username='part', email='p@test.com', password='Password123!')
        client.force_login(particulier)

        # On tente d'accéder à l'index du forum école
        url = reverse('vegetables_fruits:forum_index')
        response = client.get(url)

        # Doit rediriger (car pas le droit)
        assert response.status_code == 302


@pytest.mark.django_db
class TestForumAdulte:
    """Tests pour le forum réservé aux adultes (Basique / Premium)."""

    @pytest.fixture
    def user_premium(self):
        """Crée un utilisateur avec abonnement Premium"""
        user = CustomUser.objects.create_user(username='adulte', email='adulte@test.com', password='Password123!')
        plan, _ = PlanTarification.objects.get_or_create(nom='PREMIUM', defaults={'prix_mensuel': 15})
        Abonnement.objects.create(utilisateur=user, plan=plan, statut='ACTIF')
        return user

    @pytest.fixture
    def categorie_adulte(self):
        return ForumAdulteCategorie.objects.create(nom="Conseils Experets", slug="conseils-experts")

    def test_creation_sujet_adulte(self, client, user_premium, categorie_adulte):
        """Un utilisateur Premium peut créer un sujet dans le forum adulte"""
        client.force_login(user_premium)
        url = reverse('vegetables_fruits:forum_adulte_nouveau_sujet')

        response = client.post(url, {
            'titre': 'Problème de mildiou',
            'contenu': 'Mes tomates ont des taches brunes, que faire ?',
            'categorie_id': categorie_adulte.id
        })

        assert response.status_code == 302

        sujet = ForumAdulteSujet.objects.first()
        assert sujet is not None
        assert sujet.titre == 'Problème de mildiou'
        assert sujet.auteur == user_premium
        assert MessageForumAdulte.objects.filter(sujet=sujet).count() == 1

    def test_blocage_eleve_forum_adulte(self, client):
        """Un élève ne doit pas pouvoir accéder au forum adulte"""
        # On crée un élève (même avec une classe)
        user = CustomUser.objects.create_user(username='eleve', email='e@test.com', password='Password123!')
        classe = Classe.objects.create(nom="C", enseignant=user)  # Enseignant bidon
        Eleve.objects.create(user=user, classe=classe)

        client.force_login(user)
        url = reverse('vegetables_fruits:forum_adulte_index')
        response = client.get(url)

        # Redirigé vers le forum école
        assert response.status_code == 302
        assert 'forum' in response.url