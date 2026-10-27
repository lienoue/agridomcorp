# vegetables_fruits/management/commands/enrichir_cultures_manquantes.py

from django.core.management.base import BaseCommand
from django.db import transaction
from vegetables_fruits.models import Culture, Vegetable, Fruit


class Command(BaseCommand):
    help = "Crée les cultures suggérées mais absentes de la base (Culture/Vegetable/Fruit)"

    # ============================================================
    # LISTE DES CULTURES SUGGÉRÉES (extraite de suggestions_personnalisees)
    # ============================================================
    CULTURES_A_CREER = [
        # ==================== ASIE ====================
        ('Millet', 'cereale', '🌾'),
        ('Argousier', 'fruit', '🫐'),
        ('Pommier sibérien', 'fruit', '🍏'),
        ('Chou chinois', 'legume', '🥬'),
        ('Riz', 'cereale', '🍚'),
        ('Dragon (fruit)', 'fruit', '🐉'),
        ('Thé', 'aromatique', '🍵'),
        ('Wasabi', 'legume', '🍣'),
        ('Bambou', 'autre', '🎋'),
        ('Pêche japonaise', 'fruit', '🍑'),
        ('Gingembre', 'aromatique', '🫚'),
        ('Curcuma', 'aromatique', '🧡'),
        ('Piment', 'legume', '🌶️'),
        ('Bananier', 'fruit', '🍌'),
        ('Noix de coco', 'fruit', '🥥'),
        ('Citronnelle', 'aromatique', '🌿'),
        ('Café', 'autre', '☕'),
        ('Piment oiseau', 'legume', '🌶️'),
        ('Chou coréen', 'legume', '🥬'),
        ('Poire asiatique', 'fruit', '🍐'),

        # ==================== AFRIQUE ====================
        ('Olivier', 'fruit', '🫒'),
        ('Oranger', 'fruit', '🍊'),
        ('Rose de Damas', 'fleur', '🌹'),
        ('Arachide', 'legume', '🥜'),
        ('Ignames', 'legume', '🍠'),
        ('Palmier à huile', 'autre', '🌴'),
        ('Hibiscus', 'fleur', '🌺'),
        ('Blé', 'cereale', '🌾'),
        ('Dattier', 'fruit', '🌴'),
        ('Vigne', 'fruit', '🍇'),
        ('Tournesol', 'fleur', '🌻'),

        # ==================== AMÉRIQUE ====================
        ('Cacao', 'autre', '🍫'),
        ('Mangue', 'fruit', '🥭'),
        ('Avocat', 'fruit', '🥑'),
        ('Maïs', 'cereale', '🌽'),
        ('Piment jalapeño', 'legume', '🌶️'),
        ('Pomme de terre', 'legume', '🥔'),
        ('Quinoa', 'cereale', '🌾'),

        # ==================== OCÉANIE ====================
        ('Eucalyptus', 'autre', '🪃'),
        ('Kiwi', 'fruit', '🥝'),

        # ==================== EUROPE ====================
        ('Tomate', 'legume', '🍅'),
        ('Basilic', 'aromatique', '🌿'),
        ('Gentiane', 'fleur', '💙'),

        # ==================== TROPIQUES ====================
        ('Ananas', 'fruit', '🍍'),
        ('Papaye', 'fruit', '🥭'),
        ('Goyave', 'fruit', '🍈'),
        ('Litchi', 'fruit', '🌿'),
        ('Mangoustan', 'fruit', '🌿'),
        ('Fruit de la passion', 'fruit', '🌿'),
    ]

    # ============================================================
    # FALLBACKS : si le champ n'existe pas, on cherche des alternatives
    # ============================================================
    CHAMPS_DESCRIPTION_POSSIBLES = [
        'description', 'desc', 'resume', 'notes', 'conseils',
        'description_courte', 'presentation', 'details',
    ]

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            "\n🌱 Enrichissement du catalogue de cultures"
        ))
        self.stdout.write("=" * 60)

        crees = 0
        existants = 0
        erreurs = []

        # Détecter dynamiquement les champs disponibles sur Culture
        champs_culture = {f.name for f in Culture._meta.get_fields()}
        self.stdout.write(f"📋 Champs Culture détectés : {sorted(champs_culture)}\n")

        # Détecter le champ de description disponible (si un existe)
        champ_description = None
        for candidat in self.CHAMPS_DESCRIPTION_POSSIBLES:
            if candidat in champs_culture:
                champ_description = candidat
                break

        if champ_description:
            self.stdout.write(f"✅ Champ description détecté : '{champ_description}'\n")
        else:
            self.stdout.write(
                "⚠️ Aucun champ 'description' trouvé → création avec les champs minimaux\n"
            )

        # Vérifier la présence de type_culture et emoji
        a_type_culture = 'type_culture' in champs_culture
        a_emoji = 'emoji' in champs_culture

        self.stdout.write(f" - type_culture disponible : {a_type_culture}")
        self.stdout.write(f" - emoji disponible : {a_emoji}\n")

        with transaction.atomic():
            for entree in self.CULTURES_A_CREER:
                # Support de tuples (nom, type, emoji) OU simples strings
                if isinstance(entree, tuple):
                    nom, type_culture, emoji = entree
                else:
                    nom, type_culture, emoji = entree, 'legume', '🌱'

                # 1️⃣ Vérifier si la culture existe déjà dans un des 3 modèles
                existe = (
                    Culture.objects.filter(nom__iexact=nom).exists()
                    or Vegetable.objects.filter(nom__iexact=nom).exists()
                    or Fruit.objects.filter(nom__iexact=nom).exists()
                )
                if existe:
                    existants += 1
                    self.stdout.write(f" ℹ️ Déjà existant : {nom}")
                    continue

                # 2️⃣ Construire les kwargs selon les champs disponibles
                kwargs = {'nom': nom}

                # Description
                if champ_description:
                    kwargs[champ_description] = (
                        f"Culture suggérée automatiquement pour la région. "
                        f"Ajoutez une description détaillée via l'admin."
                    )

                # Type de culture (obligatoire sur Culture)
                if a_type_culture:
                    kwargs['type_culture'] = type_culture

                # Emoji
                if a_emoji:
                    kwargs['emoji'] = emoji

                # 3️⃣ Créer
                try:
                    Culture.objects.create(**kwargs)
                    crees += 1
                    self.stdout.write(self.style.SUCCESS(
                        f" ✅ Créé : {emoji} {nom} ({type_culture})"
                    ))
                except Exception as e:
                    erreurs.append((nom, str(e)))
                    self.stdout.write(self.style.ERROR(
                        f" ❌ Échec {nom} : {e}"
                    ))

        # ============================================================
        # RAPPORT FINAL
        # ============================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("📊 RAPPORT FINAL"))
        self.stdout.write("=" * 60)
        self.stdout.write(f" ✅ Créées : {crees}")
        self.stdout.write(f" ℹ️ Existantes : {existants}")
        self.stdout.write(f" ❌ Erreurs : {len(erreurs)}")

        if erreurs:
            self.stdout.write(self.style.WARNING("\n⚠️ Détail des erreurs :"))
            for nom, err in erreurs:
                self.stdout.write(f" - {nom} : {err}")

        if crees > 0:
            self.stdout.write(self.style.SUCCESS(
                "\n👉 Lance maintenant : python manage.py assigner_familles"
            ))
        else:
            self.stdout.write(
                "\nℹ️ Aucune nouvelle culture à créer. Lance : python manage.py assigner_familles"
            )

        # ============================================================
        # VÉRIFICATION DES FAMILLES MANQUANTES
        # ============================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("🔍 Vérification des familles botaniques nécessaires")
        self.stdout.write("=" * 60)

        from vegetables_fruits.models import ConseilsFamille

        familles_necessaires = [
            'Solanacées', 'Fabacées', 'Brassicacées', 'Cucurbitacées',
            'Apiacées', 'Astéracées', 'Liliacées (Alliacées)', 'Chénopodiacées',
            'Poacées (Graminées)', 'Rosacées', 'Lamiacées (Labiées)',
            'Vitacées', 'Oléacées', 'Rubiacées', 'Musacées', 'Myrtacées',
            'Apocynacées', 'Théacées', 'Dioscoréacées', 'Gentianacées',
            'Cactacées', 'Malvacées', 'Arécacées (Palmiers)', 'Lauracées',
            'Amaranthacées', 'Actinidiacées', 'Rutacées', 'Éléagnacées',
            'Passifloracées', 'Clusiacées', 'Anacardiacées', 'Burséracées',
            'Sapotacées', 'Annonacées', 'Sapindacées', 'Caricacées',
            'Myrtacées', 'Zingibéracées', 'Moringacées',
        ]

        existantes = set(
            ConseilsFamille.objects.values_list('nom', flat=True)
        )

        manquantes = [f for f in familles_necessaires if f not in existantes]

        if not manquantes:
            self.stdout.write(self.style.SUCCESS(
                " ✅ Toutes les familles nécessaires existent en base"
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f" ⚠️ {len(manquantes)} famille(s) manquante(s) :"
            ))
            for f in manquantes:
                self.stdout.write(f" - {f}")
            self.stdout.write(
                "\n 💡 Ajoute-les dans familles.json puis lance : "
                "python manage.py charger_familles"
            )

        # Dans la méthode handle(), à la fin :
        from django.core.cache import cache
        cache.delete('tous_noms_cultures_v1')
        self.stdout.write("🔄 Cache noms cultures vidé")



