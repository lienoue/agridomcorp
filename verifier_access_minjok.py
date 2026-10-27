import os
import django

# ⚙️ Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vegetablesfruits.settings')
django.setup()

from django.contrib.auth import get_user_model
from datetime import date
from vegetables_fruits.models import Eleve, Abonnement, GeometricFigure

User = get_user_model()


# ============================================================
# COULEURS TERMINAL
# ============================================================
class C:
    OK = '\033[92m'
    KO = '\033[91m'
    WARN = '\033[93m'
    INFO = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def titre(txt):
    print(f"\n{C.BOLD}{'=' * 60}{C.END}")
    print(f"{C.BOLD} {txt}{C.END}")
    print(f"{C.BOLD}{'=' * 60}{C.END}")


def ok(txt): print(f" {C.OK}✅ {txt}{C.END}")
def ko(txt): print(f" {C.KO}❌ {txt}{C.END}")
def warn(txt): print(f" {C.WARN}⚠️ {txt}{C.END}")
def info(txt): print(f" {C.INFO}ℹ️ {txt}{C.END}")


# ============================================================
# FONCTIONS DE TEST
# ============================================================

def age(user):
    if not user.birth_date:
        return None
    today = date.today()
    return today.year - user.birth_date.year - (
        (today.month, today.day) < (user.birth_date.month, user.birth_date.day)
    )


def est_eleve_en_classe(user):
    return (
        hasattr(user, 'profil_eleve')
        and user.profil_eleve
        and user.profil_eleve.classe is not None
    )


def test_a_acces_bilan_carbone(user):
    """Reproduit la logique de a_acces_bilan_carbone"""
    if est_eleve_en_classe(user):
        return True, "élève en classe"
    try:
        ab = user.abonnement
        if ab.est_actif and ab.plan.nom in ['PREMIUM', 'ENSEIGNANT']:
            return True, f"abonnement {ab.plan.nom}"
        return False, f"abonnement {ab.plan.nom} non actif"
    except Abonnement.DoesNotExist:
        return False, "aucun abonnement"


def test_verifier_acces_abonnement(user, plan_requis):
    """Reproduit verifier_acces_abonnement"""
    if plan_requis is None:
        return True, None
    try:
        ab = user.abonnement
        if ab.est_actif and ab.plan.nom in ['PREMIUM', 'ENSEIGNANT']:
            return True, None
        if ab.est_actif and ab.plan.nom == plan_requis:
            return True, None
        return False, f"nécessite {plan_requis}"
    except Abonnement.DoesNotExist:
        if plan_requis == 'GRATUIT':
            return True, None
        return False, f"nécessite {plan_requis}"


# ============================================================
# DIAGNOSTIC PRINCIPAL
# ============================================================

def diagnostiquer(username):
    titre(f"DIAGNOSTIC DE : {username}")

    # 1. Récupération de l'utilisateur
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        ko(f"Utilisateur '{username}' introuvable en base")
        return

    print(f"\n{C.BOLD}📋 INFORMATIONS UTILISATEUR{C.END}")
    print(f" ID : {user.id}")
    print(f" Username : {user.username}")
    print(f" Email : {user.email or '(vide)'}")
    print(f" Birth date : {user.birth_date or '(non renseignée)'}")

    a = age(user)
    if a is not None:
        print(f" Âge : {a} ans")
        if a < 18:
            print(f" Statut : {C.WARN}MINEUR{C.END}")
        else:
            print(f" Statut : MAJEUR")
    else:
        print(f" Âge : (inconnu)")

    # 2. Attributs clés
    print(f"\n{C.BOLD}🔑 ATTRIBUTS CLÉS{C.END}")
    print(f" is_enseignant : {user.is_enseignant}")
    print(f" mode_junior : {user.mode_junior}")
    print(f" is_staff : {user.is_staff}")
    print(f" is_active : {user.is_active}")

    # 3. Profil élève
    print(f"\n{C.BOLD}🎓 PROFIL ÉLÈVE{C.END}")
    if hasattr(user, 'profil_eleve'):
        eleve = user.profil_eleve
        ok(f"Profil Eleve existe (id={eleve.id})")
        print(f" Points : {eleve.points}")
        print(f" Niveau : {eleve.niveau}")
        print(f" Classe : {eleve.classe or C.WARN + 'None' + C.END}")
        if eleve.classe:
            print(f" Classe nom : {eleve.classe.nom}")
            print(f" Classe code : {eleve.classe.code}")
    else:
        warn("Pas de profil Eleve")

    # 4. Abonnement
    print(f"\n{C.BOLD}💳 ABONNEMENT{C.END}")
    try:
        ab = user.abonnement
        print(f" Plan : {ab.plan.nom}")
        print(f" Statut : {ab.statut}")
        print(f" Est actif : {ab.est_actif}")
        print(f" Date début : {ab.date_debut}")
        print(f" Date fin : {ab.date_fin or 'N/A'}")
        ab_actif = ab.est_actif and ab.plan.nom in ['PREMIUM', 'ENSEIGNANT']
        if ab_actif:
            ok(f"Abonnement {ab.plan.nom} actif")
        else:
            info(f"Abonnement non premium/enseignant")
    except Abonnement.DoesNotExist:
        info("Aucun abonnement en base (= plan GRATUIT)")

    # 5. Parcelles
    print(f"\n{C.BOLD}🌱 PARCELLES{C.END}")
    nb_figures = GeometricFigure.objects.filter(user=user).count()
    print(f" Nombre de figures : {nb_figures}")

    # ============================================================
    # 6. TESTS D'ACCÈS AUX FONCTIONNALITÉS PREMIUM
    # ============================================================
    titre("TESTS D'ACCÈS AUX FONCTIONNALITÉS PREMIUM")

    eleve_en_classe = est_eleve_en_classe(user)
    print(f"\n{C.BOLD}📌 Statut 'élève en classe' : {C.END}", end="")
    if eleve_en_classe:
        ok("OUI")
    else:
        ko("NON")

    # --- Fonctionnalités testées ---
    tests = []

    # 1. Bilan carbone
    acces, raison = test_a_acces_bilan_carbone(user)
    tests.append(('Bilan carbone', acces, raison))

    # 2. Rotation des cultures
    acces = eleve_en_classe or (hasattr(user, 'abonnement') and
                                user.abonnement.est_actif and
                                user.abonnement.plan.nom in ['PREMIUM', 'ENSEIGNANT'])
    tests.append(('Rotation des cultures', acces, 'élève en classe' if eleve_en_classe else 'abonnement'))

    # 3. Compagnonnage
    tests.append(('Compagnonnage', acces, 'idem rotation'))

    # 4. Plan de fertilisation (⚠️ actuellement : uniquement PREMIUM)
    try:
        ab = user.abonnement
        acces = eleve_en_classe or (ab.est_actif and ab.plan.nom == 'PREMIUM')
    except Abonnement.DoesNotExist:
        acces = eleve_en_classe
    tests.append(('Plan de fertilisation', acces, '⚠️ bug : PREMIUM uniquement'))

    # 5. Planification des semis
    try:
        ab = user.abonnement
        acces = eleve_en_classe or (ab.est_actif and ab.plan.nom == 'PREMIUM')
    except Abonnement.DoesNotExist:
        acces = eleve_en_classe
    tests.append(('Planification des semis', acces, '⚠️ bug : PREMIUM uniquement'))

    # 6. Statistiques avancées (⚠️ pas de test est_eleve)
    try:
        ab = user.abonnement
        acces = ab.est_actif and ab.plan.nom == 'PREMIUM'
    except Abonnement.DoesNotExist:
        acces = False
    tests.append(('Statistiques avancées', acces, '⚠️ bug : pas de test élève'))

    # 7. Gestion des maladies
    try:
        ab = user.abonnement
        acces = eleve_en_classe or (ab.est_actif and ab.plan.nom == 'PREMIUM')
    except Abonnement.DoesNotExist:
        acces = eleve_en_classe
    tests.append(('Gestion des maladies', acces, 'PREMIUM'))

    # 8. Conseiller sol
    try:
        ab = user.abonnement
        acces = eleve_en_classe or (ab.est_actif and ab.plan.nom in ['PREMIUM', 'ENSEIGNANT'])
    except Abonnement.DoesNotExist:
        acces = eleve_en_classe
    tests.append(('Conseiller sol', acces, 'PREMIUM+ENSEIGNANT'))

    # 9. Dashboard climat
    try:
        ab = user.abonnement
        acces = eleve_en_classe or (ab.est_actif and ab.plan.nom in ['PREMIUM', 'ENSEIGNANT'])
    except Abonnement.DoesNotExist:
        acces = eleve_en_classe
    tests.append(('Dashboard climat', acces, 'PREMIUM+ENSEIGNANT'))

    # 10. Prévisions météo
    tests.append(('Prévisions météo', acces, 'idem dashboard'))

    # 11. Forum adulte
    if user.is_enseignant or eleve_en_classe:
        acces = False
        raison = "→ forum école"
    else:
        try:
            ab = user.abonnement
            acces = ab.est_actif and ab.plan.nom in ['BASIQUE', 'PREMIUM']
            raison = ab.plan.nom if acces else "aucun abo"
        except Abonnement.DoesNotExist:
            acces = False
            raison = "aucun abo"
    tests.append(('Forum adulte', acces, raison))

    # ============================================================
    # AFFICHAGE DU TABLEAU
    # ============================================================
    print(f"\n{C.BOLD}{'─' * 70}{C.END}")
    print(f"{C.BOLD}{'Fonctionnalité':<28} {'Accès':<10} {'Détail'}{C.END}")
    print(f"{C.BOLD}{'─' * 70}{C.END}")

    for nom, acces, raison in tests:
        if acces:
            statut = f"{C.OK}✅ OUI{C.END}"
        else:
            statut = f"{C.KO}❌ NON{C.END}"
        print(f" {nom:<28} {statut:<20} {raison}")

    print(f"{C.BOLD}{'─' * 70}{C.END}")

    # ============================================================
    # VERDICT
    # ============================================================
    titre("VERDICT")

    a = age(user)
    est_mineur = a is not None and a < 18

    if est_mineur and not user.mode_junior:
        ko(f"BUG : mineur ({a} ans) mais mode_junior=False")
        info("→ Corrige le signal post_save dans models.py")

    if est_mineur and not eleve_en_classe:
        # Vérifier qu'aucune fonctionnalité Premium n'est accessible
        premium_acces = [nom for nom, acces, _ in tests if acces and
                         nom in ['Bilan carbone', 'Rotation des cultures', 'Compagnonnage',
                                 'Plan de fertilisation', 'Planification des semis',
                                 'Statistiques avancées', 'Gestion des maladies',
                                 'Conseiller sol', 'Dashboard climat', 'Prévisions météo']]
        if premium_acces:
            ko(f"BUG : mineur sans classe a accès à {len(premium_acces)} fonctionnalité(s) Premium")
            for f in premium_acces:
                print(f" - {f}")
            info("→ Vérifie les vues concernées")
        else:
            ok("Aucun accès Premium indu pour cet élève hors classe")

    if eleve_en_classe:
        # Vérifier que l'élève en classe A accès au Premium
        premium_acces = [nom for nom, acces, _ in tests if acces and
                         nom in ['Bilan carbone', 'Rotation des cultures', 'Compagnonnage',
                                 'Plan de fertilisation', 'Planification des semis',
                                 'Statistiques avancées', 'Gestion des maladies',
                                 'Conseiller sol', 'Dashboard climat', 'Prévisions météo']]
        manquants = [nom for nom, acces, _ in tests if not acces and
                     nom in ['Bilan carbone', 'Rotation des cultures', 'Compagnonnage',
                             'Plan de fertilisation', 'Planification des semis',
                             'Statistiques avancées', 'Gestion des maladies',
                             'Conseiller sol', 'Dashboard climat', 'Prévisions météo']]
        if manquants:
            warn(f"Élève en classe : {len(manquants)} fonctionnalité(s) non accessibles")
            for f in manquants:
                print(f" - {f}")
            info("→ À corriger pour cohérence avec les autres élèves")
        else:
            ok("Élève en classe a bien accès à toutes les fonctionnalités Premium")

    print()


# ============================================================
# POINT D'ENTRÉE
# ============================================================

if __name__ == '__main__':
    import sys

    username = sys.argv[1] if len(sys.argv) > 1 else 'minjok'
    diagnostiquer(username)