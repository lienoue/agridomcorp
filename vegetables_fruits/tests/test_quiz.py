import pytest
from datetime import date
from django.urls import reverse
from vegetables_fruits.models import (
    CustomUser, QuestionQuiz, QuizUtilisateur, PlanTarification, Abonnement
)


@pytest.mark.django_db
class TestQuiz:

    @pytest.fixture
    def user_premium(self):
        """Crée un utilisateur Premium (adulte)"""
        user = CustomUser.objects.create_user(username='quiz_user', email='quiz@test.com', password='Password123!')
        plan, _ = PlanTarification.objects.get_or_create(nom='PREMIUM', defaults={'prix_mensuel': 15})
        Abonnement.objects.create(utilisateur=user, plan=plan, statut='ACTIF')
        return user

    @pytest.fixture
    def user_junior(self):
        """Crée un utilisateur Junior (mineur)"""
        user = CustomUser.objects.create_user(
            username='junior_user',
            email='junior@test.com',
            password='Password123!',
            mode_junior=True  # ✅ Important
        )
        plan, _ = PlanTarification.objects.get_or_create(nom='PREMIUM', defaults={'prix_mensuel': 15})
        Abonnement.objects.create(utilisateur=user, plan=plan, statut='ACTIF')
        return user

    @pytest.fixture
    def questions(self):
        """Crée 5 questions de test (toutes de difficulté 1 pour être sûr qu'elles soient vues)"""
        for i in range(1, 6):
            QuestionQuiz.objects.create(
                question=f"Question {i} ?",
                choix_1="Choix A",
                choix_2="Choix B",
                choix_3="Choix C",
                choix_4="Choix D",
                bonne_reponse=1,
                difficulte=1  # ✅ Difficulté 1 (accessible à tous)
            )
        return list(QuestionQuiz.objects.all())

    def test_quiz_tout_juste(self, client, user_premium, questions):
        """Vérifie qu'un utilisateur qui a tout bon gagne les points + le bonus"""
        client.force_login(user_premium)
        url = reverse('vegetables_fruits:quiz')

        data = {
            'question_ids': ','.join(str(q.id) for q in questions)
        }
        for q in questions:
            data[f'q{q.id}'] = '1'

        response = client.post(url, data)

        assert response.status_code == 200

        quiz_utilisateur = QuizUtilisateur.objects.filter(user=user_premium).first()
        assert quiz_utilisateur is not None
        assert quiz_utilisateur.score == 5

        assert response.context['points_gagnes'] == 15
        assert response.context['bonus_tout_juste'] is True

    def test_quiz_erreurs(self, client, user_premium, questions):
        """Vérifie le calcul des points si l'utilisateur a des erreurs"""
        client.force_login(user_premium)
        url = reverse('vegetables_fruits:quiz')

        data = {
            'question_ids': ','.join(str(q.id) for q in questions)
        }

        for i, q in enumerate(questions):
            data[f'q{q.id}'] = '1' if i < 2 else '2'

        response = client.post(url, data)

        assert response.status_code == 200

        quiz_utilisateur = QuizUtilisateur.objects.filter(user=user_premium).first()
        assert quiz_utilisateur.score == 2

        assert response.context['points_gagnes'] == 4
        assert response.context['bonus_tout_juste'] is False

    def test_quiz_junior_filtre(self, client, user_junior):
        """Vérifie qu'un Junior ne voit QUE les questions de difficulté 1"""
        client.force_login(user_junior)
        url = reverse('vegetables_fruits:quiz')

        # On crée une question difficile (difficulte=3) et une facile (difficulte=1)
        q_facile = QuestionQuiz.objects.create(question="Facile", choix_1="A", choix_2="B", choix_3="C", choix_4="D",
                                               bonne_reponse=1, difficulte=1)
        q_difficile = QuestionQuiz.objects.create(question="Difficile", choix_1="A", choix_2="B", choix_3="C",
                                                  choix_4="D", bonne_reponse=1, difficulte=3)

        response = client.get(url)

        assert response.status_code == 200
        questions_affichees = response.context['questions']

        # On vérifie que la question difficile N'EST PAS dans la liste
        assert q_facile in questions_affichees
        assert q_difficile not in questions_affichees

    def test_quiz_limite_basique(self, client):
        """Vérifie qu'un utilisateur Basique est bloqué après 3 quiz dans la journée"""
        user = CustomUser.objects.create_user(username='basique', email='b@test.com', password='Password123!')
        plan, _ = PlanTarification.objects.get_or_create(nom='BASIQUE', defaults={'prix_mensuel': 5})
        Abonnement.objects.create(utilisateur=user, plan=plan, statut='ACTIF')

        client.force_login(user)
        url = reverse('vegetables_fruits:quiz')

        # On simule qu'il a déjà fait 3 quiz aujourd'hui
        QuizUtilisateur.objects.create(user=user, date=date.today(), score=5, nb_quiz=3, reponses={})

        response = client.get(url)

        assert response.status_code == 302