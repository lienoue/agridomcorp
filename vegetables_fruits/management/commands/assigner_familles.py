# vegetables_fruits/management/commands/assigner_familles.py

import json
import os
import unicodedata
from difflib import get_close_matches
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from vegetables_fruits.models import (
    Culture, Vegetable, Fruit, ConseilsFamille
)


class Command(BaseCommand):
    help = "Assigne les familles botaniques aux cultures (objectif 100%)"

    def normaliser(self, texte):
        """Normalise : minuscules + suppression accents"""
        if not texte:
            return ''
        return unicodedata.normalize('NFKD', texte).encode('ASCII', 'ignore').decode().lower().strip()

    def trouver_famille_par_motcle(self, nom_culture, mots_cles, familles_dict):
        """Niveau 1 : recherche par mots-clés (du plus long au plus court)"""
        nom_norm = self.normaliser(nom_culture)

        # Trier par longueur décroissante (pour "pomme de terre" avant "pomme")
        for mot_cle in sorted(mots_cles.keys(), key=len, reverse=True):
            if mot_cle in nom_norm:
                nom_famille = mots_cles[mot_cle]
                return familles_dict.get(nom_famille), 'motcle'
        return None, None

    def trouver_famille_par_flou(self, nom_culture, mots_cles, familles_dict):
        """Niveau 2 : recherche floue (si mot-clé similaire)"""
        nom_norm = self.normaliser(nom_culture)

        # Chercher les mots-clés proches (cutoff 0.8 = 80% de similarité)
        matches = get_close_matches(nom_norm, list(mots_cles.keys()), n=1, cutoff=0.8)

        if matches:
            nom_famille = mots_cles[matches[0]]
            return familles_dict.get(nom_famille), f'flou ({matches[0]})'
        return None, None

    def handle(self, *args, **options):
        # ✅ Charger le mapping
        json_path = os.path.join(
            settings.BASE_DIR, 'vegetables_fruits', 'data', 'mapping_familles.json'
        )

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"❌ Fichier introuvable : {json_path}"))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        mots_cles = {self.normaliser(k): v for k, v in data['mots_cles'].items()}

        # ✅ Charger les familles en base
        familles_dict = {f.nom: f for f in ConseilsFamille.objects.all()}
        self.stdout.write(f"📋 {len(familles_dict)} familles disponibles")
        self.stdout.write(f"🔑 {len(mots_cles)} mots-clés à chercher\n")

        # ✅ Statistiques globales
        stats_globales = {'motcle': 0, 'flou': 0, 'non_assignes': 0}
        non_assignes_global = []

        # ✅ Assigner pour chaque modèle
        for model, nom_model in [(Culture, 'Culture'), (Vegetable, 'Vegetable'), (Fruit, 'Fruit')]:
            self.stdout.write(f"\n{'=' * 60}")
            self.stdout.write(f"🔍 {nom_model}")
            self.stdout.write(f"{'=' * 60}")

            assignes_motcle = 0
            assignes_flou = 0
            non_assignes = []

            with transaction.atomic():
                for obj in model.objects.all():
                    # Niveau 1 : mots-clés
                    famille, source = self.trouver_famille_par_motcle(
                        obj.nom, mots_cles, familles_dict
                    )

                    # Niveau 2 : flou
                    if not famille:
                        famille, source = self.trouver_famille_par_flou(
                            obj.nom, mots_cles, familles_dict
                        )
                        if famille:
                            assignes_flou += 1
                            stats_globales['flou'] += 1
                        else:
                            non_assignes.append(obj.nom)
                            stats_globales['non_assignes'] += 1
                    else:
                        assignes_motcle += 1
                        stats_globales['motcle'] += 1

                    # Niveau 3 : assignation
                    if famille:
                        obj.famille = famille
                        obj.save(update_fields=['famille'])
                    else:
                        non_assignes_global.append(f"{nom_model}: {obj.nom}")

            self.stdout.write(f" ✅ Mots-clés : {assignes_motcle}")
            self.stdout.write(f" 🔍 Flou : {assignes_flou}")
            self.stdout.write(f" ⚠️ Non assignés : {len(non_assignes)}")

            if non_assignes:
                self.stdout.write(f"\n 📋 À compléter manuellement :")
                for nom in sorted(non_assignes):
                    self.stdout.write(f" - {nom}")

        # ✅ Rapport final
        self.stdout.write(f"\n{'=' * 60}")
        self.stdout.write(self.style.SUCCESS(f"📊 RAPPORT FINAL"))
        self.stdout.write(f"{'=' * 60}")
        self.stdout.write(f" ✅ Mots-clés : {stats_globales['motcle']}")
        self.stdout.write(f" 🔍 Flou : {stats_globales['flou']}")
        self.stdout.write(f" ⚠️ Non assignés : {stats_globales['non_assignes']}")

        total = sum(stats_globales.values())
        couverture = (stats_globales['motcle'] + stats_globales['flou']) / total * 100 if total > 0 else 0
        self.stdout.write(f" 📈 Couverture : {couverture:.1f}%")

        if non_assignes_global:
            self.stdout.write(f"\n{'=' * 60}")
            self.stdout.write(self.style.WARNING("⚠️ CULTURES NON ASSIGNÉES"))
            self.stdout.write(f"{'=' * 60}")
            for item in non_assignes_global:
                self.stdout.write(f" - {item}")

        if stats_globales['non_assignes'] == 0:
            self.stdout.write(self.style.SUCCESS(f"\n🎉 100% de couverture atteinte !"))