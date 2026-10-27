"""

Commande Django pour vérifier les conditions météo et générer des alertes traitements.
Utilisation : python manage.py verifier_alertes_traitements [--force]
À exécuter en cron toutes les 6 heures.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import requests
import math


class Command(BaseCommand):
    help = 'Vérifie les conditions météo et génère des alertes traitements'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force la création même si des alertes existent déjà'
        )

    def calculer_distance(self, lat1, lng1, lat2, lng2):
        """
        Calcule la distance en mètres entre deux points GPS
        Formule de Haversine
        """
        R = 6371000 # Rayon de la Terre en mètres

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lng2 - lng1)

        a = math.sin(delta_phi / 2) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def get_cultures_voisines(self, figure, cultures_actuelles, rayon=50):
        """
        Récupère les cultures voisines à moins de X mètres
        """
        voisines = []

        # Récupérer toutes les parcelles de l'utilisateur
        from vegetables_fruits.models import GeometricFigure
        toutes_figures = GeometricFigure.objects.filter(
            user=figure.user,
            adresse_lat__isnull=False,
            adresse_lng__isnull=False
        ).exclude(id=figure.id)

        for autre_figure in toutes_figures:
            distance = self.calculer_distance(
                figure.adresse_lat, figure.adresse_lng,
                autre_figure.adresse_lat, autre_figure.adresse_lng
            )

            if distance <= rayon:
                # Récupérer les cultures de cette parcelle
                cultures_voisines = []
                for crop in autre_figure.crops or []:
                    if 'name' in crop:
                        cultures_voisines.append(crop['name'])

                if cultures_voisines:
                    voisines.append({
                        'figure': autre_figure,
                        'distance': round(distance, 1),
                        'cultures': cultures_voisines
                    })

        return sorted(voisines, key=lambda x: x['distance'])

    def handle(self, *args, **options):
        from vegetables_fruits.models import (
            GeometricFigure,
            AlerteTraitement,
            Culture,
            MaladieCulture
        )
        from django.contrib.auth import get_user_model
        User = get_user_model()

        self.stdout.write("🔍 Vérification des alertes traitements...")
        self.stdout.write(f"📅 {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")

        users = User.objects.all()
        self.stdout.write(f"👤 {users.count()} utilisateur(s)")

        # Dictionnaire des actions par maladie
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

        actions_par_niveau = {
            'faible': "🔍 Inspectez les feuilles une fois par semaine et notez toute évolution.",
            'moyenne': "✂️ Retirez les parties infectées, surveillez l'évolution et préparez un traitement préventif.",
            'elevee': "🧪 Appliquez un traitement fongicide immédiatement. Consultez la notice pour le dosage exact.",
            'critique': (
                "🚨 ACTIONS URGENTES À RÉALISER IMMÉDIATEMENT :\n"
                "1. Isolez immédiatement la culture concernée des autres\n"
                "2. Retirez et brûlez toutes les parties infectées\n"
                "3. Appliquez un traitement d'urgence\n"
                "4. Désinfectez tous vos outils\n"
                "5. Contactez un expert agricole"
            )
        }

        alertes_crees = 0
        alertes_contamination = 0
        total_parcelles_verifiees = 0
        total_erreurs = 0

        for user in users:
            self.stdout.write(f"\n👤 Utilisateur: {user.username} (ID: {user.id})")

            figures = GeometricFigure.objects.filter(
                user=user,
                adresse_lat__isnull=False,
                adresse_lng__isnull=False
            )

            if not figures.exists():
                self.stdout.write(self.style.WARNING(f" ⚠️ Aucune parcelle avec coordonnées"))
                continue

            self.stdout.write(f" 📍 {figures.count()} parcelle(s)")

            for figure in figures:
                total_parcelles_verifiees += 1
                self.stdout.write(f" 🌾 {figure.name}...", ending='')

                try:
                    # Appel API météo
                    url = f"https://api.openweathermap.org/data/2.5/weather?lat={figure.adresse_lat}&lon={figure.adresse_lng}&units=metric&lang=fr&appid={settings.OPENWEATHER_API_KEY}"
                    response = requests.get(url, timeout=10)

                    if response.status_code != 200:
                        self.stdout.write(self.style.WARNING(f" ⚠️ API error {response.status_code}"))
                        total_erreurs += 1
                        continue

                    data = response.json()
                    temp = data['main']['temp']
                    humidite = data['main']['humidity']
                    precipitation = data.get('rain', {}).get('1h', 0)
                    description = data['weather'][0]['description']

                    self.stdout.write(f" 🌡️ {temp}°C, 💧 {humidite}%")

                    crops = figure.crops or []
                    if not crops:
                        self.stdout.write(f" ⚠️ Aucune culture")
                        continue

                    # === VÉRIFICATION DES MALADIES ===
                    for crop in crops:
                        if 'name' not in crop:
                            continue

                        culture_nom = crop['name']
                        culture_obj = Culture.objects.filter(nom__icontains=culture_nom).first()
                        if not culture_obj:
                            continue

                        # Récupérer les maladies pour cette culture
                        try:
                            maladies = MaladieCulture.objects.filter(
                                culture__nom__icontains=culture_nom
                            )
                        except:
                            try:
                                maladies = MaladieCulture.objects.filter(
                                    cultures__nom__icontains=culture_nom
                                )
                            except:
                                maladies = MaladieCulture.objects.all()[:3]

                        if not maladies.exists():
                            maladies = MaladieCulture.objects.all()[:3]

                        for maladie in maladies:
                            # Vérifier si une alerte existe déjà
                            date_limite = timezone.now() - timedelta(hours=24)
                            alerte_existante = AlerteTraitement.objects.filter(
                                figure=figure,
                                culture=culture_obj,
                                maladie=maladie,
                                statut__in=['en_attente', 'envoyee'],
                                date_creation__gte=date_limite
                            ).exists()

                            if alerte_existante and not options['force']:
                                continue

                            # Niveau de risque
                            score = 0
                            if temp > 25:
                                score += 20
                            if temp > 30:
                                score += 15
                            if humidite > 80:
                                score += 30
                            if humidite > 90:
                                score += 20
                            if precipitation > 10:
                                score += 25
                            if precipitation > 20:
                                score += 15

                            if score >= 50:
                                niveau = 'critique' if score >= 80 else ('elevee' if score >= 65 else 'moyenne')
                            else:
                                niveau = 'faible'

                            if niveau == 'faible' and not options['force']:
                                continue

                            # === DÉTECTION DE PROXIMITÉ ===
                            # Vérifier les cultures voisines (rayon de 50m)
                            cultures_voisines = self.get_cultures_voisines(figure, crops, rayon=50)

                            message_contamination = ""
                            if cultures_voisines:
                                # Filtrer les voisines à moins de 20m (risque élevé)
                                voisines_proches = [v for v in cultures_voisines if v['distance'] <= 20]

                                if voisines_proches:
                                    message_contamination = f"\n⚠️ CONTAMINATION POTENTIELLE : {len(voisines_proches)} parcelle(s) voisine(s) à moins de 20m !"
                                    for v in voisines_proches:
                                        message_contamination += f"\n • {v['figure'].name} ({v['distance']}m) - Cultures : {', '.join(v['cultures'])}"

                                    # Alerte de contamination
                                    alerte_contamination = AlerteTraitement.objects.create(
                                        utilisateur=user,
                                        figure=figure,
                                        culture=culture_obj,
                                        maladie=maladie,
                                        niveau_risque='critique',
                                        message=f"🚨 RISQUE DE CONTAMINATION ! {maladie.nom} détecté sur {culture_obj.nom} - Parcelles voisines à risque !",
                                        conseils=f"🚨 ISOLEZ IMMÉDIATEMENT les parcelles suivantes :\n" +
                                                 "\n".join([f" • {v['figure'].name} ({v['distance']}m)" for v in voisines_proches]) +
                                                 "\n\n📋 Actions :\n1. Évitez tout déplacement d'outils entre les parcelles\n2. Désinfectez vos chaussures et outils\n3. Appliquez un traitement préventif sur les parcelles voisines\n4. Surveillez quotidiennement l'apparition de symptômes",
                                        temperature=temp,
                                        humidite=humidite,
                                        precipitation=precipitation,
                                        statut='en_attente',
                                        date_creation=timezone.now(),
                                        date_declenchement=timezone.now()
                                    )
                                    alertes_contamination += 1
                                    self.stdout.write(
                                        self.style.WARNING(
                                            f" ⚠️ ALERTE CONTAMINATION : {maladie.nom} sur {culture_obj.nom} - {len(voisines_proches)} parcelle(s) voisine(s)"
                                        )
                                    )

                            # === CRÉATION DE L'ALERTE PRINCIPALE ===
                            messages = {
                                'faible': f"Surveillance recommandée pour {maladie.nom} sur {culture_obj.nom}.",
                                'moyenne': f"Risque modéré de {maladie.nom} sur {culture_obj.nom}.",
                                'elevee': f"⚠️ Risque élevé de {maladie.nom} sur {culture_obj.nom}.",
                                'critique': f"🚨 RISQUE CRITIQUE ! {maladie.nom} sur {culture_obj.nom}."
                            }

                            nom_maladie_lower = maladie.nom.lower()
                            action_specifique = actions_par_maladie.get(nom_maladie_lower, None)

                            if action_specifique:
                                if niveau == 'critique':
                                    conseils = f"⚠️ ACTION URGENTE SPÉCIFIQUE :\n{action_specifique}\n\n📋 Actions supplémentaires :\n{actions_par_niveau['critique']}"
                                elif niveau == 'elevee':
                                    conseils = f"🔴 ACTION RECOMMANDÉE :\n{action_specifique}\n\n📋 Surveillance : {actions_par_niveau['elevee']}"
                                elif niveau == 'moyenne':
                                    conseils = f"🟡 ACTION PRÉVENTIVE :\n{action_specifique}\n\n📋 Surveillance : {actions_par_niveau['moyenne']}"
                                else:
                                    conseils = f"🟢 SURVEILLANCE :\n{action_specifique}\n\n📋 {actions_par_niveau['faible']}"
                            else:
                                conseils = actions_par_niveau[niveau]

                            # Ajouter le message de contamination si présent
                            if message_contamination:
                                conseils += f"\n\n{message_contamination}"

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
                                date_creation=timezone.now(),
                                date_declenchement=timezone.now()
                            )

                            alertes_crees += 1
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f" ✅ Alerte: {maladie.nom} sur {culture_obj.nom} ({niveau})"
                                )
                            )

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f" ❌ Erreur: {str(e)}"))
                    total_erreurs += 1
                    continue

        # Bilan
        self.stdout.write("\n" + "="*60)
        self.stdout.write(f"📊 Bilan :")
        self.stdout.write(f" - Parcelles vérifiées : {total_parcelles_verifiees}")
        self.stdout.write(f" - Alertes créées : {alertes_crees}")
        self.stdout.write(f" - Alertes contamination : {alertes_contamination}")
        self.stdout.write(f" - Erreurs : {total_erreurs}")
        self.stdout.write("="*60)

        if alertes_crees > 0:
            self.stdout.write(self.style.SUCCESS(f"\n🎉 {alertes_crees} alerte(s) créée(s) !"))
        else:
            self.stdout.write(self.style.WARNING("\n✅ Aucune nouvelle alerte."))