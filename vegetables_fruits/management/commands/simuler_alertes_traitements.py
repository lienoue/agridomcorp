"""
Commande Django pour simuler des alertes traitements.
Utilisation : python manage.py simuler_alertes_traitements [--user=USER] [--nb=N]
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Simule des alertes traitements pour tester le système'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Nom d\'utilisateur (défaut: premier utilisateur)'
        )
        parser.add_argument(
            '--nb',
            type=int,
            default=3,
            help='Nombre d\'alertes à simuler (défaut: 3)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force la création même si des alertes existent'
        )

    def handle(self, *args, **options):
        from vegetables_fruits.models import (
            GeometricFigure,
            AlerteTraitement,
            Culture,
            MaladieCulture
        )

        nb_alertes = options['nb']

        # Récupérer l'utilisateur
        if options['user']:
            try:
                user = User.objects.get(username=options['user'])
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"❌ Utilisateur '{options['user']}' non trouvé"))
                return
        else:
            user = User.objects.first()
            if not user:
                self.stdout.write(self.style.ERROR("❌ Aucun utilisateur trouvé"))
                return

        self.stdout.write(f"👤 Utilisateur: {user.username} (ID: {user.id})")

        # Récupérer les parcelles
        figures = GeometricFigure.objects.filter(user=user)
        if not figures.exists():
            self.stdout.write(self.style.WARNING("⚠️ Aucune parcelle trouvée pour cet utilisateur"))
            return

        # Récupérer les cultures et maladies
        cultures = list(Culture.objects.all())
        maladies = list(MaladieCulture.objects.all())

        if not cultures:
            self.stdout.write(self.style.WARNING("⚠️ Aucune culture trouvée"))
            return

        if not maladies:
            self.stdout.write(self.style.WARNING("⚠️ Aucune maladie trouvée"))
            return

        # ✅ DICTIONNAIRE DES ACTIONS SPÉCIFIQUES PAR MALADIE
        actions_par_maladie = {
            'mildiou': "🌿 Appliquez de la bouillie bordelaise sur les feuilles (20g/L). Renouvelez après 10 jours.",
            'oïdium': "🌿 Pulvérisez du soufre micronisé (15g/L) ou un mélange eau-bicarbonate (1 cuillère/L).",
            'pourriture grise': "🌿 Retirez tous les fruits touchés, aérez la culture et appliquez un fongicide anti-botrytis.",
            'anthracnose': "🌿 Coupez les branches atteintes à 10cm sous la zone infectée. Appliquez un fongicide cuivrique.",
            'rouille': "🌿 Retirez les feuilles infectées. Pulvérisez une décoction de prêle ou soufre.",
            'taches noires': "🌿 Taillez les parties atteintes. Appliquez un traitement fongicide systémique.",
            'fusariose': "🌿 Arrachez et brûlez les plantes infectées. N'utilisez pas le sol pour les cultures sensibles pendant 3 ans.",
            'maladie cryptogamique': "🌿 Pulvérisez de la bouillie bordelaise. Assurez une bonne aération des cultures.",
            'mosaïque': "🌿 Arrachez les plants infectés. Désinfectez vos outils. Éliminez les pucerons vecteurs.",
            'gale': "🌿 Retirez les fruits atteints. Appliquez un traitement à base de cuivre en automne et au printemps.",
            'moniliose': "🌿 Supprimez les fruits momifiés. Taillez les branches mortes. Appliquez un fongicide spécifique.",
            'cloque du pêcher': "🌿 Pulvérisez de la bouillie bordelaise à la chute des feuilles et au débourrement.",
            'feu bactérien': "🚨 ALERTE CRITIQUE ! Coupez et brûlez les branches infectées à 50cm en dessous. Désinfectez les outils.",
            'champignon du sol': "🌿 Aérez le sol. Appliquez un traitement fongicide racinaire. Évitez les excès d'eau.",
        }

        # ✅ ACTIONS PAR NIVEAU DE RISQUE (fallback si maladie non trouvée)
        actions_par_niveau = {
            'faible': "🔍 Inspectez les feuilles une fois par semaine et notez toute évolution.",
            'moyenne': "✂️ Retirez les parties infectées, surveillez l'évolution et préparez un traitement préventif.",
            'elevee': "🧪 Appliquez un traitement fongicide immédiatement. Consultez la notice pour le dosage exact.",
            'critique': (
                "🚨 ACTIONS URGENTES À RÉALISER IMMÉDIATEMENT :\n"
                "1. Isolez immédiatement la culture concernée des autres\n"
                "2. Retirez et brûlez toutes les parties infectées (feuilles, fruits, branches)\n"
                "3. Appliquez un traitement d'urgence (fongicide systémique ou biologique)\n"
                "4. Désinfectez tous vos outils de jardinage (eau de Javel diluée)\n"
                "5. Contactez un expert agricole ou votre service technique si la situation persiste"
            )
        }

        # Niveaux de risque
        niveaux_risque = ['faible', 'moyenne', 'elevee', 'critique']
        poids_niveaux = [1, 2, 3, 2]

        alertes_crees = 0

        for i in range(nb_alertes):
            figure = random.choice(figures)

            # Récupérer les cultures de la figure
            crops = figure.crops or []
            cultures_figure = []
            for crop in crops:
                if 'name' in crop:
                    cultures_figure.append(crop['name'].lower())

            if not cultures_figure:
                culture = random.choice(cultures)
                cultures_figure = [culture.nom.lower()]

            culture_nom = random.choice(cultures_figure)
            culture_obj = Culture.objects.filter(nom__icontains=culture_nom).first()
            if not culture_obj:
                culture_obj = random.choice(cultures)

            maladie = random.choice(maladies)
            niveau = random.choices(niveaux_risque, weights=poids_niveaux, k=1)[0]

            temp = round(random.uniform(15, 35), 1)
            humidite = random.randint(50, 95)
            precipitation = round(random.uniform(0, 20), 1)

            # ✅ Messages par niveau
            messages = {
                'faible': f"Surveillance recommandée pour {maladie.nom} sur {culture_obj.nom}.",
                'moyenne': f"Risque modéré de {maladie.nom} sur {culture_obj.nom}. Une surveillance accrue est conseillée.",
                'elevee': f"⚠️ Risque élevé de {maladie.nom} sur {culture_obj.nom}. Un traitement est recommandé rapidement.",
                'critique': f"🚨 RISQUE CRITIQUE ! {maladie.nom} détecté sur {culture_obj.nom}. Intervention immédiate requise !"
            }

            # ✅ Déterminer l'action spécifique
            nom_maladie_lower = maladie.nom.lower()
            action_specifique = actions_par_maladie.get(nom_maladie_lower, None)

            if action_specifique:
                # Si action spécifique trouvée, on l'utilise
                if niveau == 'critique':
                    conseils = f"⚠️ ACTION URGENTE SPÉCIFIQUE :\n{action_specifique}\n\n📋 Actions supplémentaires :\n{actions_par_niveau['critique']}"
                elif niveau == 'elevee':
                    conseils = f"🔴 ACTION RECOMMANDÉE :\n{action_specifique}\n\n📋 Surveillance : {actions_par_niveau['elevee']}"
                elif niveau == 'moyenne':
                    conseils = f"🟡 ACTION PRÉVENTIVE :\n{action_specifique}\n\n📋 Surveillance : {actions_par_niveau['moyenne']}"
                else:
                    conseils = f"🟢 SURVEILLANCE :\n{action_specifique}\n\n📋 {actions_par_niveau['faible']}"
            else:
                # Fallback sur l'action par niveau
                conseils = actions_par_niveau[niveau]

            maintenant = timezone.now()
            date_declenchement = maintenant - timedelta(hours=random.randint(1, 48))

            alerte = AlerteTraitement.objects.create(
                utilisateur=user,
                figure=figure,
                culture=culture_obj,
                maladie=maladie,
                niveau_risque=niveau,
                message=messages[niveau],
                conseils=conseils,
                temperature=temp,
                humidite=humidite,
                precipitation=precipitation,
                statut='en_attente',
                date_creation=maintenant - timedelta(hours=random.randint(0, 48)),
                date_declenchement=date_declenchement,
            )

            alertes_crees += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Alerte #{i+1}: {maladie.nom} sur {culture_obj.nom} "
                    f"({niveau}) - {figure.name} [ID: {alerte.id}]"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 {alertes_crees} alerte(s) simulée(s) avec succès !"
            )
        )