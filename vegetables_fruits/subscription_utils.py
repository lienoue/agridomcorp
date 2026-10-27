from django.utils import timezone
from .models import QuizUtilisateur, Abonnement

def has_quiz_access(user):
    """
    Vérifie si l'utilisateur peut faire un quiz aujourd'hui.
    Retourne (acces, message)
    """
    # ✅ Déterminer le plan effectif (avec fallback gratuit)
    plan = 'GRATUIT' # Par défaut
    try:
        abonnement = user.abonnement
        if abonnement.est_actif:
            plan = abonnement.plan.nom
        # Si abonnement inactif → on garde GRATUIT
    except Abonnement.DoesNotExist:
        # Pas d'abonnement → gratuit par défaut
        pass

    # ✅ Limite selon le plan
    if plan in ['PREMIUM', 'ENSEIGNANT']:
        limite_quotidienne = 5
    elif plan == 'BASIQUE':
        limite_quotidienne = 3
    else: # GRATUIT
        limite_quotidienne = 1

    # Vérifier le nombre de quiz déjà faits aujourd'hui
    quizzes_aujourdhui = QuizUtilisateur.objects.filter(
        user=user,
        date=timezone.now().date()
    ).count()

    if quizzes_aujourdhui >= limite_quotidienne:
        return False, f"Vous avez déjà fait {quizzes_aujourdhui} quiz aujourd'hui. Limite : {limite_quotidienne}."

    return True, ""