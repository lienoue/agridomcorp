from django.core.management.base import BaseCommand
from vegetables_fruits.models import BesoinsEau, Culture, Vegetable, Fruit, Variete


class Command(BaseCommand):
    help = "Met à jour les fréquences d'arrosage pour TOUTES les cultures en base"

    def handle(self, *args, **kwargs):
        # 1. Dictionnaire des fréquences précises (le plus exhaustif possible)
        frequences_exactes = {
            # Légumes-feuilles (soif rapide, racines courtes)
            'salade': 2, 'laitue': 2, 'épinard': 2, 'mâche': 2, 'roquette': 2,
            'blette': 2, 'chou': 3, 'brocoli': 3, 'chou-fleur': 3,

            # Légumes-fruits (cycle moyen, besoin d'eau régulier)
            'tomate': 3, 'courgette': 3, 'concombre': 3, 'aubergine': 3,
            'poivron': 3, 'piment': 3, 'melon': 3, 'pastèque': 3, 'cornichon': 3,

            # Légumes-racines (puisent en profondeur)
            'carotte': 4, 'betterave': 4, 'navet': 4, 'radis': 3, 'panais': 4,

            # Tubercules & Bulbes (stockent l'eau)
            'pomme de terre': 5, 'patate douce': 5, 'oignon': 6, 'ail': 7,
            'échalote': 6, 'poireau': 4,

            # Légumineuses
            'haricot': 3, 'petit pois': 3, 'fève': 3, 'pois chiche': 4, 'lentille': 5,

            # Aromatiques (résistantes)
            'basilic': 2, 'menthe': 3, 'persil': 3, 'coriandre': 3,
            'romarin': 10, 'thym': 10, 'lavande': 10, 'sauge': 8, 'origan': 8,

            # Arbres fruitiers (racines profondes)
            'pommier': 7, 'poirier': 7, 'cerisier': 7, 'prunier': 7, 'pêcher': 6,
            'abricotier': 7, 'figuier': 10, 'olivier': 12, 'vigne': 8, 'kiwi': 5, 'nashi': 6,

            # Fruits tropicaux
            'bananier': 3, 'manguier': 6, 'ananas': 6, 'papaye': 4, 'litchi': 5,
            'avocat': 5, 'citronnier': 5, 'oranger': 5, 'goyave': 5, 'fruit de la passion': 4,

            # Céréales
            'blé': 7, 'maïs': 4, 'riz': 2, 'orge': 7, 'avoine': 7,
        }

        # 2. Récupérer TOUS les noms uniques de cultures depuis tous les modèles
        noms_cultures = set()
        noms_cultures.update(Culture.objects.values_list('nom', flat=True))
        noms_cultures.update(Vegetable.objects.values_list('nom', flat=True))
        noms_cultures.update(Fruit.objects.values_list('nom', flat=True))
        noms_cultures.update(Variete.objects.values_list('nom', flat=True))
        noms_cultures.update(BesoinsEau.objects.values_list('culture', flat=True))

        modifs = 0
        self.stdout.write(self.style.WARNING(f"🔍 {len(noms_cultures)} cultures uniques trouvées en base. Analyse...\n"))

        for culture_nom in noms_cultures:
            if not culture_nom:
                continue

            culture_lower = culture_nom.lower()
            frequence_finale = None
            source = ""

            # A. Recherche exacte dans notre dictionnaire
            if culture_lower in frequences_exactes:
                frequence_finale = frequences_exactes[culture_lower]
                source = "exacte"
            else:
                # B. Recherche par mot-clé (ex: "Tomate cerise" contient "tomate")
                for mot, freq in frequences_exactes.items():
                    if mot in culture_lower:
                        frequence_finale = freq
                        source = f"mot-clé '{mot}'"
                        break

            # C. Si on n'a rien trouvé, on met une fréquence par défaut "sûre" (3 jours)
            # pour éviter que les cultures inconnues aient 0 jour ou 30 jours.
            if frequence_finale is None:
                frequence_finale = 3
                source = "défaut"

            # 3. Mettre à jour TOUTES les entrées existantes pour cette culture
            besoins_existants = BesoinsEau.objects.filter(culture__iexact=culture_nom)

            if besoins_existants.exists():
                # Si la culture existe déjà (même en double), on met à jour toutes les lignes
                for besoin in besoins_existants:
                    if besoin.frequence_arrosage_jours != frequence_finale:
                        besoin.frequence_arrosage_jours = frequence_finale
                        besoin.save()
                        modifs += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✅ {culture_nom.ljust(25)} → Tous les {frequence_finale} jours ({source})")
                )
            else:
                # Si la culture n'existe pas du tout, on la crée
                BesoinsEau.objects.create(
                    culture=culture_nom,
                    besoin_litres_par_m2=5.0,
                    frequence_arrosage_jours=frequence_finale
                )
                modifs += 1
                self.stdout.write(
                    self.style.SUCCESS(f"➕ {culture_nom.ljust(25)} → Créé (Tous les {frequence_finale} jours)")
                )