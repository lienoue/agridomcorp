from django.utils import  timezone
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    devise_preferee = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        help_text="Code ISO 4217 (EUR, USD, XOF…). Auto-détecté si vide.",
        verbose_name="Devise préférée"
    )
    birth_date = models.DateField(null=True, blank=True)
    telephone = models.CharField(max_length=20, blank=True, null=True, help_text="Numéro de téléphone (format international)")
    email = models.EmailField(unique=True)
    mode_junior = models.BooleanField(default=False)
    is_enseignant = models.BooleanField(default=False)
    essai_gratuit_utilise = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    tutoriel_termine = models.BooleanField(default=False)

    # ✅ MODÉRATION FORUM
    is_moderateur_forum = models.BooleanField(default=False)
    nb_avertissements = models.IntegerField(default=0)
    est_suspendu = models.BooleanField(default=False)
    date_suspension = models.DateTimeField(null=True, blank=True)
    date_debut_suspension = models.DateTimeField(null=True, blank=True)

    # ✅ STATS FORUM
    nb_messages_forum = models.IntegerField(default=0)
    nb_sujets_forum = models.IntegerField(default=0)
    nb_signalements = models.IntegerField(default=0)
    points_forum = models.IntegerField(default=0)

    def est_suspendu_actif(self):
        if not self.est_suspendu:
            return False
        if self.date_suspension:
            # Suspension de 7 jours par défaut
            if (timezone.now() - self.date_suspension).days >= 7:
                self.est_suspendu = False
                self.save()
                return False
        return True

    @property
    def est_mineur(self):
        from datetime import date
        if self.birth_date:
            age = (date.today() - self.birth_date).days // 365
            return age < 18
        return False


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique_username')
        ]

    def __str__(self):
        return self.username


# Mode Junior
class Badge(models.Model):
    nom = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=200, blank=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.emoji} {self.nom}"


class Mission(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    action_type = models.CharField(max_length=50)  # 'planter', 'arroser', 'recolter'
    action_valeur = models.IntegerField(default=1)  # nombre requis
    points = models.IntegerField(default=10)

    def __str__(self):
        return self.titre


class ProgressionJunior(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    niveau = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    badges = models.ManyToManyField(Badge, blank=True)
    missions_completed = models.ManyToManyField(Mission, blank=True)

    def __str__(self):
        return f"{self.user.username} - Niveau {self.niveau} ({self.points} pts)"



# -----------------------------------

class Vegetable(models.Model):
    nom = models.CharField(max_length=200)
    # ✅ Lien vers la famille botanique (optionnel)
    famille = models.ForeignKey(
        'ConseilsFamille',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='vegetables',
        verbose_name="Famille botanique"
    )
    # ✅ Surcharges possibles (si différents de la famille)
    temperature_min = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température minimale spécifique (°C)",
        help_text="Si différent de la famille"
    )
    temperature_optimale_min = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température optimale min. spécifique (°C)"
    )
    temperature_optimale_max = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température optimale max. spécifique (°C)"
    )
    temperature_max = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température maximale spécifique (°C)"
    )

    duree_culture_min_jours = models.IntegerField(
        null=True, blank=True,
        verbose_name="Durée minimale spécifique (jours)"
    )
    duree_culture_max_jours = models.IntegerField(
        null=True, blank=True,
        verbose_name="Durée maximale spécifique (jours)"
    )

    methode_plantation = models.CharField(
        max_length=50, blank=True,
        choices=[
            ('graine', '🌰 Graine'),
            ('rhizome', '🫚 Rhizome'),
            ('bulbe', '🧄 Bulbe'),
            ('tubercule', '🥔 Tubercule'),
            ('plant', '🌱 Plant / Semis'),
            ('bouture', '🌿 Bouture'),
            ('greffe', '🌳 Greffe'),
            ('division', '🌾 Division de touffe'),
        ],
        verbose_name="Méthode de plantation spécifique"
    )

    hivernage = models.CharField(
        max_length=50, blank=True,
        choices=[
            ('plein_air', '🌳 Plein air (rustique)'),
            ('serre', '🏠 Serre ou abri'),
            ('interieur', '🏡 Intérieur obligatoire'),
            ('climat_doux', '🌞 Climat doux uniquement'),
        ],
        verbose_name="Hivernage spécifique"
    )

    # ✅ Conseils spécifiques (surcharge la famille)
    conseils_climat = models.TextField(
        blank=True,
        verbose_name="Conseils climat spécifiques"
    )
    conseils_plantation = models.TextField(
        blank=True,
        verbose_name="Conseils plantation spécifiques"
    )
    conseils_arrosage = models.TextField(
        blank=True,
        verbose_name="Conseils arrosage spécifiques"
    )
    conseils_fertilisation = models.TextField(
        blank=True,
        verbose_name="Conseils fertilisation spécifiques"
    )
    conseils_protection = models.TextField(
        blank=True,
        verbose_name="Conseils protection spécifiques"
    )
    conseils_recolte = models.TextField(
        blank=True,
        verbose_name="Conseils récolte spécifiques"
    )
    conseils_conservation = models.TextField(
        blank=True,
        verbose_name="Conseils conservation spécifiques"
    )
    couleur = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    provenance = models.CharField(max_length=200)
    saison = models.CharField(max_length=200)
    plantation = models.CharField(max_length=200)
    recolte = models.CharField(max_length=200)
    varietes = models.CharField(max_length=200)
    varietes_m2m = models.ManyToManyField('Variete', blank=True, related_name='vegetables')
    prix = models.FloatField(default=0)
    bourse = models.BooleanField(default=False)
    AOP = models.BooleanField(default=False)
    IGP = models.BooleanField(default=False)
    url = models.CharField(max_length=400)

    # 🌱 NOUVEAUX CHAMPS POUR LES SEMIS
    semis_interieur = models.CharField(max_length=200, blank=True, null=True)
    semis_exterieur = models.CharField(max_length=200, blank=True, null=True)
    jours_levée = models.IntegerField(default=0, help_text="Nombre de jours avant levée")
    jours_recolte = models.IntegerField(default=0, help_text="Nombre de jours avant récolte")
    temperature_min = models.IntegerField(default=10, help_text="Température minimale de germination (°C)")
    profondeur_semis = models.CharField(max_length=50, blank=True, null=True)
    espacement = models.CharField(max_length=50, blank=True, null=True)

    # 🌱 NOUVEAUX CHAMPS POUR LA POLLINISATION
    pollinisation_type = models.CharField(
        max_length=50,
        choices=[
            ('auto', '🌱 Auto-pollinisation'),
            ('croisee', '🔄 Pollinisation croisée'),
            ('vent', '💨 Pollinisation par le vent'),
            ('insectes', '🐝 Pollinisation par les insectes'),
            ('mixte', '🔄 Mixte')
        ],
        blank=True,
        null=True
    )
    besoin_pollinisateur = models.BooleanField(default=False, help_text="Nécessite un pollinisateur")
    pollinisateurs_conseilles = models.TextField(blank=True, null=True, help_text="Ex: 'Pommetier, variété voisine'")
    distance_pollinisation = models.IntegerField(default=0, help_text="Distance maximale de pollinisation (m)")
    periode_floraison = models.CharField(max_length=200, blank=True, null=True)
    conseils_pollinisation = models.TextField(blank=True, null=True)

    # 🌱 CONSEILS DE CULTURE
    conseils_preparation_sol = models.TextField(blank=True, null=True,
                                                help_text="Comment préparer le sol avant la plantation")
    conseils_apres_recolte = models.TextField(blank=True, null=True, help_text="Que faire du sol après la récolte")
    rotation_conseillee = models.TextField(blank=True, null=True, help_text="Avec quelles cultures alterner (rotation)")
    rotation_deconseillee = models.TextField(blank=True, null=True,
                                             help_text="Cultures à ne pas planter au même endroit l'année suivante")

    def get_emoji(self):
        """Retourne l'émoji correspondant au légume"""
        emojis = {
            # Légumes-racines
            'carotte': '🥕',
            'pomme de terre': '🥔', 'patate': '🥔',
            'betterave': ' betterave → ',
            'radis': ' radis → ',
            'navet': ' navet → ',
            'céleri-rave': ' celeri → ',
            'topinambour': ' topinambour → ',
            'panais': ' panais → ',
            'topinambour': '🥔🌻',
            'panais': '🥕⚪',

            # Légumes-feuilles
            'salade': '🥬', 'laitue': '🥬', 'roquette': '🥬', 'mâche': '🥬',
            'épinard': ' epinard → ',
            'chou': '🥬', 'chou vert': '🥬', 'chou kale': '🥬',
            'chou frisé': '🥬', 'chou pommé': '🥬',
            'chou rouge': '🥬', 'chou blanc': '🥬',
            'chou de bruxelles': ' chou de bruxelles → ',
            'chou-fleur': '🥦',
            'brocoli': '🥦',
            'endive': '🥬⚪',

            # Légumes-fruits
            'tomate': '🍅',
            'concombre': '🥒', 'cornichon': '🥒',
            'courgette': '🥒',
            'aubergine': '🍆',
            'poivron': '🫑', 'piment': '🫑',
            'courge': '🎃', 'potiron': '🎃', 'citrouille': '🎃',
            'potimarron': '🎃',

            # Légumes-bulbes
            'oignon': '🧅', 'échalote': '🧅🟣',
            'ail': '🧄',
            'poireau': ' poireau → ',

            # Légumineuses
            'haricot': '🫘', 'haricot vert': '🫘',
            'petit pois': ' petit pois → ', 'pois': ' petit pois → ',
            'fève': ' feve → ',
            'lentille': ' lentille → ',
            'edamame': '🫛',

            # Champignons
            'champignon': '🍄', 'pleurote': '🍄', 'cèpe': '🍄',

            # Céréales
            'maïs': '🌽', 'blé': '🌾', 'orge': '🌾', 'avoine': '🌾',
            'seigle': '🌾', 'riz': '🌾',

            # Herbes aromatiques
            'persil': '🌿', 'ciboulette': '🌿', 'basilic': '🌿',
            'menthe': '🌿', 'thym': '🌿', 'romarin': '🌿',
            'laurier': '🌿', 'sauge': '🌿', 'aneth': '🌿', 'gingembre': '🫚',


            # Autres
            'artichaut': ' artichaut → ',
            'asperge': ' asperge → ',
            'fenouil': ' fenouil → ',
            'rhubarbe': ' rhubarbe → ',
        }

        nom_lower = self.nom.lower()
        for key, emoji in emojis.items():
            if key in nom_lower:
                return emoji
        return '🥕'  # Emoji par défaut

    def __str__(self):
        return self.nom


class Fruit(models.Model):
    nom = models.CharField(max_length=200)
    # ✅ Lien vers la famille botanique (optionnel)
    famille = models.ForeignKey(
        'ConseilsFamille',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='fruits',
        verbose_name="Famille botanique"
    )
    # ✅ Surcharges possibles (si différents de la famille)
    temperature_min = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température minimale spécifique (°C)",
        help_text="Si différent de la famille"
    )
    temperature_optimale_min = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température optimale min. spécifique (°C)"
    )
    temperature_optimale_max = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température optimale max. spécifique (°C)"
    )
    temperature_max = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température maximale spécifique (°C)"
    )

    duree_culture_min_jours = models.IntegerField(
        null=True, blank=True,
        verbose_name="Durée minimale spécifique (jours)"
    )
    duree_culture_max_jours = models.IntegerField(
        null=True, blank=True,
        verbose_name="Durée maximale spécifique (jours)"
    )

    methode_plantation = models.CharField(
        max_length=50, blank=True,
        choices=[
            ('graine', '🌰 Graine'),
            ('rhizome', '🫚 Rhizome'),
            ('bulbe', '🧄 Bulbe'),
            ('tubercule', '🥔 Tubercule'),
            ('plant', '🌱 Plant / Semis'),
            ('bouture', '🌿 Bouture'),
            ('greffe', '🌳 Greffe'),
            ('division', '🌾 Division de touffe'),
        ],
        verbose_name="Méthode de plantation spécifique"
    )

    hivernage = models.CharField(
        max_length=50, blank=True,
        choices=[
            ('plein_air', '🌳 Plein air (rustique)'),
            ('serre', '🏠 Serre ou abri'),
            ('interieur', '🏡 Intérieur obligatoire'),
            ('climat_doux', '🌞 Climat doux uniquement'),
        ],
        verbose_name="Hivernage spécifique"
    )

    # ✅ Conseils spécifiques (surcharge la famille)
    conseils_climat = models.TextField(
        blank=True,
        verbose_name="Conseils climat spécifiques"
    )
    conseils_plantation = models.TextField(
        blank=True,
        verbose_name="Conseils plantation spécifiques"
    )
    conseils_arrosage = models.TextField(
        blank=True,
        verbose_name="Conseils arrosage spécifiques"
    )
    conseils_fertilisation = models.TextField(
        blank=True,
        verbose_name="Conseils fertilisation spécifiques"
    )
    conseils_protection = models.TextField(
        blank=True,
        verbose_name="Conseils protection spécifiques"
    )
    conseils_recolte = models.TextField(
        blank=True,
        verbose_name="Conseils récolte spécifiques"
    )
    conseils_conservation = models.TextField(
        blank=True,
        verbose_name="Conseils conservation spécifiques"
    )
    couleur = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    provenance = models.CharField(max_length=200)
    saison = models.CharField(max_length=200)
    plantation = models.CharField(max_length=200)
    recolte = models.CharField(max_length=200)
    varietes = models.CharField(max_length=200)
    varietes_m2m = models.ManyToManyField('Variete', blank=True, related_name='fruits')
    prix = models.FloatField(default=0)
    bourse = models.BooleanField(default=False)
    AOP = models.BooleanField(default=False)
    IGP = models.BooleanField(default=False)
    url = models.CharField(max_length=400)

    # 🌱 NOUVEAUX CHAMPS POUR LES SEMIS
    semis_interieur = models.CharField(max_length=200, blank=True, null=True)
    semis_exterieur = models.CharField(max_length=200, blank=True, null=True)
    jours_levée = models.IntegerField(default=0, help_text="Nombre de jours avant levée")
    jours_recolte = models.IntegerField(default=0, help_text="Nombre de jours avant récolte")
    temperature_min = models.IntegerField(default=10, help_text="Température minimale de germination (°C)")
    profondeur_semis = models.CharField(max_length=50, blank=True, null=True)
    espacement = models.CharField(max_length=50, blank=True, null=True)

    # 🌱 NOUVEAUX CHAMPS POUR LA POLLINISATION
    pollinisation_type = models.CharField(
        max_length=50,
        choices=[
            ('auto', '🌱 Auto-pollinisation'),
            ('croisee', '🔄 Pollinisation croisée'),
            ('vent', '💨 Pollinisation par le vent'),
            ('insectes', '🐝 Pollinisation par les insectes'),
            ('mixte', '🔄 Mixte')
        ],
        blank=True,
        null=True
    )
    besoin_pollinisateur = models.BooleanField(default=False, help_text="Nécessite un pollinisateur")
    pollinisateurs_conseilles = models.TextField(blank=True, null=True, help_text="Ex: 'Pommetier, variété voisine'")
    distance_pollinisation = models.IntegerField(default=0, help_text="Distance maximale de pollinisation (m)")
    periode_floraison = models.CharField(max_length=200, blank=True, null=True)
    conseils_pollinisation = models.CharField(max_length=200, blank=True, null=True)

    # 🌱 CONSEILS DE CULTURE
    conseils_preparation_sol = models.TextField(blank=True, null=True,
                                                help_text="Comment préparer le sol avant la plantation")
    conseils_apres_recolte = models.TextField(blank=True, null=True, help_text="Que faire du sol après la récolte")
    rotation_conseillee = models.TextField(blank=True, null=True, help_text="Avec quelles cultures alterner (rotation)")
    rotation_deconseillee = models.TextField(blank=True, null=True,
                                             help_text="Cultures à ne pas planter au même endroit l'année suivante")

    def get_emoji(self):
        """Retourne l'émoji correspondant au fruit"""
        emojis = {
            # Fruits rouges
            'pomme': '🍎', 'pomme golden': '🍏', 'pomme verte': '🍏',
            'poire': '🍐',
            'fraise': '🍓', 'fraise des bois': '🍓',
            'framboise': ' framboise → ',
            'cassis': '🫐', 'myrtille': '🫐', 'bleuet': '🫐',
            'mûre': '🍇⚫',
            'groseille': ' groseille → ',
            'cerise': '🍒', 'griotte': '🍒',
            'canneberge': ' canneberge → ',

            # Fruits à noyau
            'pêche': '🍑', 'peche': '🍑', 'nectarine': '🍑',
            'abricot': ' abricot → ',
            'prune': ' prune → ', 'quetsche': ' prune → ', 'mirabelle': ' prune → ',

            # Agrumes
            'orange': '🍊', 'oranger': '🍊', 'mandarine': '🍊', 'clémentine': '🍊',
            'citron': '🍋', 'citron vert': '🍋🟩', 'limette': '🍋🟩',
            'pamplemousse': ' pamplemousse → ', 'pomelo': ' pamplemousse → ',

            # Fruits exotiques
            'banane': '🍌', 'plantain': '🍌',
            'ananas': '🍍',
            'mangue': '🥭',
            'kiwi': '🥝',
            'litchi': ' litchi → ',
            'fruit de la passion': ' fruit de la passion → ',
            'grenade': ' grenade → ',
            'figue': ' figue → ',
            'datte': ' datte → ',

            # Melons
            'pastèque': '🍉', 'melon d\'eau': '🍉',
            'melon': '🍈', 'cantaloup': '🍈',

            # Fruits à coque
            'noix': ' noix → ', 'noix de pécan': ' noix → ',
            'noisette': ' noisette → ',
            'amande': ' amande → ',
            'châtaigne': '🌰',
            'noix de coco': '🥥',

            # Raisins
            'raisin': '🍇', 'raisin blanc': '🍇', 'raisin noir': '🍇',

            # Autres
            'olive': '🫒',
            'avocat': '🥑',
            'kaki': ' kaki → ',
            'coing': ' coing → ',
        }

        nom_lower = self.nom.lower()
        for key, emoji in emojis.items():
            if key in nom_lower:
                return emoji
        return '🍎'  # Emoji par défaut

    def __str__(self):
        return self.nom



class GeometricFigure(gis_models.Model):
    # Relation utilisateur
    user = gis_models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_index=True)

    # Champs de base
    name = gis_models.CharField(max_length=100)
    created_at = gis_models.DateTimeField(auto_now_add=True, db_index=True)
    geojson_data = gis_models.JSONField()
    figure_type = gis_models.CharField(max_length=50, db_index=True)

    # ⭐ NOUVEAU : Champ pour stocker les cultures placées avec références
    crops = gis_models.JSONField(default=list, blank=True)
    # Structure attendue :
    # [
    # {
    # "placement_id": 1678456123, # ID unique pour ce placement
    # "fruit_id": 1, # Référence à Fruit(id=1) OU
    # "vegetable_id": 2, # Référence à Vegetable(id=2)
    # "name": "Pomme Golden", # Nom pour affichage rapide
    # "emoji": "🍎", # Emoji
    # "lat": 46.603354, # Latitude
    # "lng": 1.888334, # Longitude
    # "date_placement": "2024-02-24T10:30:00Z" # Date du placement
    # }
    # ]

    # Pour stocker la surface calculée
    surface_hectares = gis_models.FloatField(default=0, blank=True)

    # Pour stocker le nombre de points
    nb_points = gis_models.IntegerField(default=0, blank=True)

    # Description optionnelle
    description = gis_models.TextField(blank=True)

    # ⭐ NOUVEAUX CHAMPS POUR L'ADRESSE
    adresse = gis_models.CharField(max_length=255, blank=True, null=True)
    adresse_lat = gis_models.FloatField(blank=True, null=True)
    adresse_lng = gis_models.FloatField(blank=True, null=True)
    adresse_formatted = gis_models.CharField(max_length=500, blank=True, null=True)

    # NOUVEAU : Unité d'affichage préférée pour les besoins en eau
    unite_surface = models.CharField(
        max_length=10,
        choices=[
            ('m2', 'Mètres carrés (m²)'),
            ('ha', 'Hectares (ha)'),
        ],
        default='m2',
        help_text="Unité d'affichage de la surface"
    )

    def save(self, *args, **kwargs):
        # Calcul automatique de la surface
        if self.geojson_data and not self.surface_hectares:
            try:
                features = self.geojson_data.get('features', [])
                if features:
                    geom = features[0].get('geometry', {})
                    geom_type = geom.get('type')

                    # Calcul simplifié selon le type de géométrie
                    if geom_type == 'Polygon':
                        coords = geom.get('coordinates', [[]])
                        if coords and coords[0]:
                            # Approximation : (nombre de points * 10 m²)
                            nb_points = len(coords[0])
                            surface_m2 = max(nb_points * 10, 10)  # Au moins 10 m²
                            self.surface_hectares = surface_m2 / 10000
                    elif geom_type == 'Point':
                        # Un point = 1 m²
                        self.surface_hectares = 1 / 10000  # 0.0001 ha
                    elif geom_type == 'LineString':
                        coords = geom.get('coordinates', [])
                        if coords:
                            # Une ligne = (longueur approximative * largeur 1m)
                            nb_segments = len(coords) - 1
                            surface_m2 = max(nb_segments * 2, 5)  # 2 m² par segment
                            self.surface_hectares = surface_m2 / 10000
                    else:
                        self.surface_hectares = 0.01  # 100 m² par défaut
                else:
                    self.surface_hectares = 0.01  # 100 m² par défaut
            except Exception as e:
                print(f"Erreur calcul surface: {e}")
                self.surface_hectares = 0.01  # Valeur par défaut

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    def get_crops_with_details(self):
        """
        Retourne la liste des crops avec les détails complets
        depuis les tables Fruit et Vegetable
        """
        enriched_crops = []

        for crop in self.crops:
            crop_copy = crop.copy()

            if 'fruit_id' in crop:
                try:
                    fruit = Fruit.objects.get(id=crop['fruit_id'])
                    crop_copy['details'] = {
                        'id': fruit.id,
                        'nom': fruit.nom,
                        'couleur': fruit.couleur,
                        'prix': fruit.prix,
                        'saison': fruit.saison,
                        'provenance': fruit.provenance,
                        'type': 'fruit',
                        # 🌱 AJOUT DES NOUVEAUX CHAMPS
                        'semis_interieur': fruit.semis_interieur,
                        'semis_exterieur': fruit.semis_exterieur,
                        'jours_levée': fruit.jours_levée,
                        'jours_recolte': fruit.jours_recolte,
                        'temperature_min': fruit.temperature_min,
                        'profondeur_semis': fruit.profondeur_semis,
                        'espacement': fruit.espacement,
                        'pollinisation_type': fruit.pollinisation_type,
                        'besoin_pollinisateur': fruit.besoin_pollinisateur,
                        'pollinisateurs_conseilles': fruit.pollinisateurs_conseilles,
                        'distance_pollinisation': fruit.distance_pollinisation,
                        'periode_floraison': fruit.periode_floraison,
                        'conseils_pollinisation': fruit.conseils_pollinisation,
                    }
                except Fruit.DoesNotExist:
                    crop_copy['details'] = None

            elif 'vegetable_id' in crop:
                try:
                    vegetable = Vegetable.objects.get(id=crop['vegetable_id'])
                    crop_copy['details'] = {
                        'id': vegetable.id,
                        'nom': vegetable.nom,
                        'couleur': vegetable.couleur,
                        'prix': vegetable.prix,
                        'saison': vegetable.saison,
                        'provenance': vegetable.provenance,
                        'type': 'vegetable',
                        # 🌱 AJOUT DES NOUVEAUX CHAMPS
                        'semis_interieur': vegetable.semis_interieur,
                        'semis_exterieur': vegetable.semis_exterieur,
                        'jours_levée': vegetable.jours_levée,
                        'jours_recolte': vegetable.jours_recolte,
                        'temperature_min': vegetable.temperature_min,
                        'profondeur_semis': vegetable.profondeur_semis,
                        'espacement': vegetable.espacement,
                        'pollinisation_type': vegetable.pollinisation_type,
                        'besoin_pollinisateur': vegetable.besoin_pollinisateur,
                        'pollinisateurs_conseilles': vegetable.pollinisateurs_conseilles,
                        'distance_pollinisation': vegetable.distance_pollinisation,
                        'periode_floraison': vegetable.periode_floraison,
                        'conseils_pollinisation': vegetable.conseils_pollinisation,
                    }
                except Vegetable.DoesNotExist:
                    crop_copy['details'] = None

            enriched_crops.append(crop_copy)

        return enriched_crops




class ChronologieCulture(models.Model):
    """Suit la progression d'une culture placée sur une parcelle"""
    STATUTS = [
        ('seme', '🌱 Semé'),
        ('levee', '🌿 Levée'),
        ('croissance', '🌳 En croissance'),
        ('floraison', '🌸 Floraison'),
        ('fructification', '🍅 Fructification'),
        ('pret', '✅ Prêt à récolter'),
        ('recolte', '🧺 Récolté'),
    ]

    figure = models.ForeignKey(GeometricFigure, on_delete=models.CASCADE, related_name='chronologies', db_index=True)
    culture_nom = models.CharField(max_length=200)
    culture_emoji = models.CharField(max_length=10)
    date_semis = models.DateField()
    date_recolte_prevue = models.DateField()
    # ✅ Dates prévues pour chaque étape (calculées automatiquement)
    date_levee_prevue = models.DateField(null=True, blank=True)
    date_croissance_prevue = models.DateField(null=True, blank=True)
    date_floraison_prevue = models.DateField(null=True, blank=True)
    date_fructification_prevue = models.DateField(null=True, blank=True)
    date_recolte_effective = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='seme', db_index=True)
    progression = models.IntegerField(default=0)  # Pourcentage 0-100
    points_gagnes = models.IntegerField(default=0)

    STADES = [
        ('seme', '🌱 Semé'),
        ('levee', '🌿 Levée'),
        ('croissance', '🌳 Croissance'),
        ('floraison', '🌸 Floraison'),
        ('fructification', '🍎 Fructification'),
        ('pret', '✅ Prêt à récolter'),
        ('recolte', '🧺 Récolté'),
    ]

    stade_actuel = models.CharField(
        max_length=20,
        choices=STADES,
        default='seme',
        help_text="Stade actuel de la culture"
    )

    class Meta:
        verbose_name = "Chronologie de culture"
        verbose_name_plural = "Chronologies des cultures"
        ordering = ['date_semis']
        indexes = [
            models.Index(fields=['figure', 'statut']),
        ]

    def __str__(self):
        return f"{self.culture_emoji} {self.culture_nom} - {self.get_statut_display()}"

    def calculer_progression(self):
        """Calcule la progression, met à jour le stade et les dates prévues."""
        from datetime import date, timedelta

        aujourdhui = date.today()

        # ============================================================
        # 1. Calcul des dates prévues pour chaque étape
        # ============================================================
        if self.date_semis and self.date_recolte_prevue:
            duree_totale = (self.date_recolte_prevue - self.date_semis).days

            # Pourcentages indicatifs du cycle
            self.date_levee_prevue = self.date_semis + timedelta(
                days=int(duree_totale * 0.10)
            )
            self.date_croissance_prevue = self.date_semis + timedelta(
                days=int(duree_totale * 0.30)
            )
            self.date_floraison_prevue = self.date_semis + timedelta(
                days=int(duree_totale * 0.60)
            )
            self.date_fructification_prevue = self.date_semis + timedelta(
                days=int(duree_totale * 0.85)
            )

        # ============================================================
        # 2. Calcul de la progression
        # ============================================================
        if self.date_recolte_effective:
            self.progression = 100
            self.statut = 'recolte'
            self.stade_actuel = 'recolte'
        elif aujourdhui >= self.date_recolte_prevue:
            self.progression = 100
            self.statut = 'pret'
            self.stade_actuel = 'pret'
        else:
            jours_total = (self.date_recolte_prevue - self.date_semis).days
            jours_ecoules = (aujourdhui - self.date_semis).days
            if jours_total > 0:
                self.progression = min(95, int((jours_ecoules / jours_total) * 100))

            # Mise à jour du stade selon la progression
            if self.progression < 10:
                self.statut = 'seme'
                self.stade_actuel = 'seme'
            elif self.progression < 30:
                self.statut = 'levee'
                self.stade_actuel = 'levee'
            elif self.progression < 60:
                self.statut = 'croissance'
                self.stade_actuel = 'croissance'
            elif self.progression < 85:
                self.statut = 'floraison'
                self.stade_actuel = 'floraison'
            else:
                self.statut = 'fructification'
                self.stade_actuel = 'fructification'

        self.save()
        return self.progression

    @property
    def get_etapes_timeline(self):
        """
        Retourne la liste des étapes de la timeline avec leur état :
        - 'passee' : ✅ l'étape est derrière nous
        - 'actuelle' : 🔵 c'est l'étape en cours
        - 'future' : ⚪ l'étape est à venir
        """
        from datetime import date

        aujourdhui = date.today()

        etapes_def = [
            ('seme', '🌱', 'Semé', self.date_semis),
            ('levee', '🌿', 'Levée', self.date_levee_prevue),
            ('croissance', '🌳', 'Croissance', self.date_croissance_prevue),
            ('floraison', '🌸', 'Floraison', self.date_floraison_prevue),
            ('fructification', '🍅', 'Fructification', self.date_fructification_prevue),
            ('pret', '✅', 'Récolte', self.date_recolte_prevue),
        ]

        # Si déjà récolté, tout est "passé"
        if self.statut == 'recolte' or self.date_recolte_effective:
            return [
                {
                    'code': code, 'emoji': emoji, 'label': label,
                    'date': dt, 'etat': 'passee',
                }
                for code, emoji, label, dt in etapes_def
            ]

        # Trouver l'index de l'étape actuelle selon le statut
        ordre_statuts = ['seme', 'levee', 'croissance', 'floraison', 'fructification', 'pret']
        try:
            index_actuel = ordre_statuts.index(self.statut)
        except ValueError:
            index_actuel = 0

        etapes = []
        for i, (code, emoji, label, dt) in enumerate(etapes_def):
            if i < index_actuel:
                etat = 'passee'
            elif i == index_actuel:
                etat = 'actuelle'
            else:
                etat = 'future'

            etapes.append({
                'code': code,
                'emoji': emoji,
                'label': label,
                'date': dt,
                'etat': etat,
            })

        return etapes


class AlerteSemis(models.Model):
    """Modèle pour gérer les alertes de semis, récolte, etc."""

    TYPES_ALERTE = [
        ('levee', '🌱 Levée des semis'),
        ('plantation', '🌿 Plantation'),
        ('recolte', '🍅 Récolte'),
        ('arrosage', '💧 Arrosage'),
        ('semis', '📅 Date de semis'),
        ('taille', '✂️ Taille'),
        ('engrais', '🌱 Fertilisation'),
    ]

    STATUTS = [
        ('en_attente', '⏳ En attente'),
        ('envoyee', '✅ Envoyée'),
        ('ignoree', '⏭️ Ignorée'),
    ]

    CANAUX = [
        ('email', '📧 Email'),
        ('sms', '📱 SMS'),
        ('les_deux', '📧📱 Email et SMS'),
    ]

    # Relations
    figure = models.ForeignKey(
        'GeometricFigure',
        on_delete=models.CASCADE,
        related_name='alertes'
    )

    # Données de la culture concernée
    crop_data = models.JSONField(default=dict, help_text="Stocke les infos de la culture")

    # Type et statut
    type_alerte = models.CharField(max_length=20, choices=TYPES_ALERTE)
    canal = models.CharField(max_length=20, choices=CANAUX, default='email')
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')

    # Contenu
    titre = models.CharField(max_length=200)
    message = models.TextField()

    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_declenchement = models.DateTimeField()
    date_envoi = models.DateTimeField(null=True, blank=True)
    date_ignoration = models.DateTimeField(null=True, blank=True)

    # Destinataires
    email_destinataire = models.EmailField(blank=True, null=True)
    telephone_destinataire = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['date_declenchement']
        verbose_name = "Alerte"
        verbose_name_plural = "Alertes"

    def __str__(self):
        return f"{self.titre} - {self.figure.name}"

    def est_urgente(self):
        """Vérifie si l'alerte est urgente (<= 1 jour)"""
        from django.utils import timezone
        jours_restants = (self.date_declenchement - timezone.now()).days
        return jours_restants <= 1

    def est_proche(self):
        """Vérifie si l'alerte est proche (2-3 jours)"""
        from django.utils import timezone
        jours_restants = (self.date_declenchement - timezone.now()).days
        return 1 < jours_restants <= 3

    def envoyer(self):
        """Envoie l'alerte (email ou SMS)"""
        from django.core.mail import send_mail
        from django.conf import settings
        from datetime import datetime

        success = False

        if self.canal in ['email', 'les_deux'] and self.email_destinataire:
            try:
                send_mail(
                    subject=self.titre,
                    message=self.message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[self.email_destinataire],
                    fail_silently=False,
                )
                success = True
            except Exception as e:
                print(f"Erreur envoi email: {e}")

        if self.canal in ['sms', 'les_deux'] and self.telephone_destinataire:
            # Ici, intégration avec un service SMS (Twilio, SMS Partner, etc.)
            print(f"SMS à {self.telephone_destinataire}: {self.message[:160]}")
            success = True

        if success:
            self.statut = 'envoyee'
            self.date_envoi = datetime.now()
            self.save()

        return success


class Classe(models.Model):
    """Une classe créée par un enseignant"""
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, blank=True)
    enseignant = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='classes_enseignees'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.enseignant.username}"

    def sauvegarder_code(self):
        """Génère un code unique pour la classe"""
        import random
        import string
        self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.sauvegarder_code()
        super().save(*args, **kwargs)


class Eleve(models.Model):
    """Un élève lié à une classe"""
    user = models.OneToOneField(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='profil_eleve'
    )
    classe = models.ForeignKey(
        Classe,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='eleves'
    )
    points = models.IntegerField(default=0, db_index=True)
    niveau = models.IntegerField(default=1, db_index=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    badges = models.ManyToManyField(Badge, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.classe.nom if self.classe else 'Sans classe'}"

    def ajouter_points(self, points, action_type=None):
        """Ajoute des points et débloque les badges"""
        self.points += points

        # Mise à jour du niveau (100 points = 1 niveau)
        nouveau_niveau = self.points // 100 + 1
        if nouveau_niveau > self.niveau:
            self.niveau = nouveau_niveau

        # ✅ Débloquer les badges selon le nombre de points
        badges_a_debloquer = Badge.objects.filter(
            points__lte=self.points
        ).exclude(
            id__in=self.badges.all()
        )

        for badge in badges_a_debloquer:
            self.badges.add(badge)
            # Optionnel : envoyer une notification
            print(f"🎉 {self.user.username} a débloqué {badge.emoji} {badge.nom} !")

        self.save()

        # Synchroniser ProgressionJunior si nécessaire
        progression, _ = ProgressionJunior.objects.get_or_create(user=self.user)
        progression.points = self.points
        progression.niveau = self.niveau
        progression.save()
        for badge in self.badges.all():
            progression.badges.add(badge)

    class Meta:
        indexes = [
            models.Index(fields=['-points']),
            models.Index(fields=['classe', '-points']),
        ]

class MissionQuotidienne(models.Model):
    """Mission que les élèves peuvent accomplir chaque jour"""
    titre = models.CharField(max_length=200)
    description = models.TextField()
    points = models.IntegerField(default=10)
    action_type = models.CharField(max_length=50, blank=True)  # 'creer_parcelle', 'planter_culture', etc.
    action_requise = models.IntegerField(default=1)
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"🎯 {self.titre} (+{self.points} pts)"


class MissionEleve(models.Model):
    """Suivi des missions accomplies par un élève"""
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='missions')
    mission = models.ForeignKey(MissionQuotidienne, on_delete=models.CASCADE)
    accomplie = models.BooleanField(default=False)
    progression = models.IntegerField(default=0)
    date_accomplie = models.DateTimeField(null=True, blank=True)
    date_mission = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('eleve', 'mission', 'date_mission')

    def __str__(self):
        status = "✅" if self.accomplie else "⏳"
        return f"{status} {self.eleve.user.username} - {self.mission.titre}"


class NotificationEnseignant(models.Model):
    """Notifications pour les enseignants"""
    TYPES = (
        ('nouvel_eleve', '🎉 Nouvel élève'),
        ('point_fort', '⭐ Point fort'),
        ('alerte', '⚠️ Alerte'),
        ('rappel', '🔔 Rappel'),
        ('succes', '🏆 Succès de classe'),
    )

    enseignant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    type_notification = models.CharField(max_length=20, choices=TYPES)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    lien = models.CharField(max_length=200, blank=True, null=True)
    est_lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} - {self.enseignant.username}"


class PlanTarification(models.Model):
    """Plans d'abonnement disponibles"""
    PLAN_CHOICES = [
        ('GRATUIT', 'Gratuit'),
        ('BASIQUE', 'Basique'),
        ('PREMIUM', 'Premium'),
        ('ENSEIGNANT', 'Enseignant'),
    ]

    nom = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    prix_mensuel = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    prix_annuel = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    stripe_price_id_mensuel = models.CharField(max_length=100, blank=True, null=True)
    stripe_price_id_annuel = models.CharField(max_length=100, blank=True, null=True)

    # Limites
    max_parcelles = models.IntegerField(default=5)
    max_classes = models.IntegerField(default=0)
    max_eleves_par_classe = models.IntegerField(default=0)
    export_csv = models.BooleanField(default=False)
    export_pdf = models.BooleanField(default=False)
    mode_gps = models.BooleanField(default=False)

    # Réduction groupe scolaire (en pourcentage)
    reduction_groupe_scolaire = models.IntegerField(default=0, help_text="Réduction en %")
    description = models.TextField(blank=True, null=True)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    # Nouveaux champs pour le plan Premium
    coach_jardinier = models.BooleanField(default=False,
                                          help_text="Accès au Coach du Jardinier (suggestions intelligentes)")
    rotation_auto = models.BooleanField(default=False, help_text="Rotation des cultures automatique sur 4 ans")
    compagnonnage = models.BooleanField(default=False, help_text="Suggestions de compagnonnage entre plantes")
    alertes_avancees = models.BooleanField(default=False, help_text="Alertes météo et maladies avancées")
    calendrier_avance = models.BooleanField(default=False, help_text="Calendrier lunaire et planning avancé")
    badges_exclusifs = models.BooleanField(default=False, help_text="Badges et récompenses exclusifs")
    conseils_personnalises = models.BooleanField(default=False, help_text="Conseils de culture personnalisés")

    class Meta:
        verbose_name = "Plan tarifaire"
        verbose_name_plural = "Plans tarifaires"

    def __str__(self):
        return f"{self.get_nom_display()} - {self.prix_mensuel}€/mois"


class Abonnement(models.Model):
    """Abonnement d'un utilisateur"""
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('ANNULE', 'Annulé'),
        ('EXPIRE', 'Expiré'),
        ('ESSAI', 'Période d\'essai'),
    ]


    FREQUENCE_CHOICES = [
        ('MENSUEL', 'Mensuel'),
        ('ANNUEL', 'Annuel'),
    ]

    utilisateur = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='abonnement'
    )
    plan = models.ForeignKey(
        PlanTarification,
        on_delete=models.PROTECT,
        related_name='abonnements'
    )
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='ESSAI')
    frequence = models.CharField(max_length=10, choices=FREQUENCE_CHOICES, default='MENSUEL')

    # Stripe
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)

    # Dates
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(blank=True, null=True)
    date_prochain_paiement = models.DateTimeField(blank=True, null=True)

    # Réduction
    est_groupe_scolaire = models.BooleanField(default=False)
    reduction_appliquee = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ✅ Nouveaux champs pour la résiliation programmée
    resiliation_programmee = models.BooleanField(
        default=False,
        verbose_name="Résiliation programmée"
    )
    date_fin_prevue = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de fin prévue"
    )

    class Meta:
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"

    def __str__(self):
        return f"{self.utilisateur.email} - {self.plan.get_nom_display()} ({self.statut})"

    @property
    def est_actif(self):
        return self.statut == 'ACTIF' or self.statut == 'ESSAI'

    @property
    def parcelles_restantes(self):
        compte = self.utilisateur.geometricfigure_set.count()
        return max(0, self.plan.max_parcelles - compte)


class ConsentementRGPD(models.Model):
    """Consentement RGPD (notamment parental)"""

    TYPE_CONSENTEMENT = [
        ('obligatoire', '🔒 Obligatoire (-15 ans)'),
        ('recommande', '⚠️ Recommandé (15-17 ans)'),
        ('personnel', '✅ Personnel (18+)'),
    ]

    STATUT_CHOICES = [
        ('en_attente', '⏳ En attente'),
        ('valide', '✅ Validé'),
        ('refuse', '❌ Refusé'),
        ('expire', '⏰ Expiré'),
    ]

    utilisateur = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='consentements'
    )
    eleve = models.ForeignKey(
        'Eleve',
        on_delete=models.CASCADE,
        related_name='consentements_rgpd',
        blank=True,
        null=True
    )

    # Types de consentement
    cgu_acceptees = models.BooleanField(default=False)
    politique_confidentialite_acceptee = models.BooleanField(default=False)
    consentement_donnees = models.BooleanField(default=False)
    consentement_marketing = models.BooleanField(default=False)

    # ✅ Différenciation de l'âge
    type_consentement = models.CharField(
        max_length=20,
        choices=TYPE_CONSENTEMENT,
        default='personnel',
        help_text="Type de consentement selon l'âge de l'utilisateur"
    )

    # ✅ Statut de validation
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente',
        help_text="Statut du consentement parental"
    )

    # ✅ Token pour validation parentale
    token_validation = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="Token unique pour valider le consentement parental"
    )

    # Consentement parental (pour les mineurs)
    est_mineur = models.BooleanField(default=False)
    representant_legal_nom = models.CharField(max_length=150, blank=True, null=True)
    representant_legal_prenom = models.CharField(max_length=150, blank=True, null=True)
    representant_legal_email = models.EmailField(blank=True, null=True)
    representant_legal_telephone = models.CharField(max_length=20, blank=True, null=True)
    date_consentement_parental = models.DateTimeField(blank=True, null=True)

    ip_address = models.GenericIPAddressField(blank=True, null=True)
    date_consentement = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Consentement RGPD"
        verbose_name_plural = "Consentements RGPD"
        ordering = ['-date_consentement']

    def __str__(self):
        return f"Consentement de {self.utilisateur.email} - {self.get_statut_display()}"

    def save(self, *args, **kwargs):
        # ✅ Générer un token si nécessaire
        if self.type_consentement == 'obligatoire' and not self.token_validation:
            import secrets
            self.token_validation = secrets.token_urlsafe(32)
        super().save(*args, **kwargs)

    def est_valide(self):
        """Le consentement est-il validé ?"""
        return self.statut == 'valide'

    def est_bloquant(self):
        """Le consentement bloque-t-il l'accès ?"""
        return self.type_consentement == 'obligatoire' and self.statut != 'valide'

    def jours_restants(self):
        """Nombre de jours avant expiration (si validé)"""
        from datetime import timedelta
        if self.date_consentement_parental:
            expiration = self.date_consentement_parental + timedelta(days=365)
            return (expiration - timezone.now()).days
        return 0


class Facture(models.Model):
    """Factures des paiements"""
    STATUT_CHOICES = [
        ('PAYEE', 'Payée'),
        ('EN_ATTENTE', 'En attente'),
        ('ECHOUEE', 'Échouée'),
        ('REMBOURSEE', 'Remboursée'),
    ]

    utilisateur = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='factures'
    )
    abonnement = models.ForeignKey(
        Abonnement,
        on_delete=models.SET_NULL,
        null=True,
        related_name='factures'
    )
    stripe_invoice_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True, null=True)

    montant_ht = models.DecimalField(max_digits=8, decimal_places=2)
    montant_ttc = models.DecimalField(max_digits=8, decimal_places=2)
    reduction = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='EN_ATTENTE')
    description = models.TextField(blank=True, null=True)

    date_emission = models.DateTimeField(auto_now_add=True)
    date_paiement = models.DateTimeField(blank=True, null=True)

    # PDF
    facture_pdf = models.FileField(upload_to='factures/', blank=True, null=True)

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"

    def __str__(self):
        return f"Facture {self.id} - {self.utilisateur.email}"


# CREATION DU QUIZZ

class QuestionQuiz(models.Model):
    question = models.CharField(max_length=500)
    choix_1 = models.CharField(max_length=200)
    choix_2 = models.CharField(max_length=200)
    choix_3 = models.CharField(max_length=200)
    choix_4 = models.CharField(max_length=200)
    bonne_reponse = models.IntegerField(choices=[(1, 'Choix 1'), (2, 'Choix 2'), (3, 'Choix 3'), (4, 'Choix 4')])
    explication = models.TextField(blank=True, null=True, help_text="Pourquoi cette réponse est correcte")
    difficulte = models.IntegerField(default=1, choices=[(1, 'Facile'), (2, 'Moyen'), (3, 'Difficile')])
    categorie = models.CharField(max_length=100, blank=True, null=True)  # 'fruits', 'legumes', 'pollinisation', etc.

    def __str__(self):
        return self.question[:50]


class QuizUtilisateur(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    score = models.IntegerField(default=0)
    reponses = models.JSONField(default=dict)  # Stocke les réponses données
    nb_quiz = models.IntegerField(default=1)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.score} pts"


class JournalBord(models.Model):
    """Journal de bord réservé aux abonnés Basique/Premium/Enseignant"""

    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notes_journal')
    figure = models.ForeignKey(GeometricFigure, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='notes_journal')
    culture = models.JSONField(default=dict, help_text="Stocke les infos de la culture (nom, emoji, type, id)")

    titre = models.CharField(max_length=200)
    note = models.TextField()
    date_note = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to='journal_images/', blank=True, null=True)

    # Météo automatique (optionnelle)
    meteo = models.CharField(max_length=100, blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)

    # Tags simples (optionnel)
    tags = models.CharField(max_length=200, blank=True, help_text="Séparez par des virgules")

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_note', '-date_creation']
        verbose_name = "Note du journal"
        verbose_name_plural = "Notes du journal"
        indexes = [
            models.Index(fields=['utilisateur']),
        ]

    def __str__(self):
        return f"{self.titre} - {self.date_note}"

    def get_culture_display(self):
        emoji = self.culture.get('emoji', '🌱')
        nom = self.culture.get('nom', 'Culture')
        return f"{emoji} {nom}"


class AlerteMeteo(models.Model):
    TYPE_ALERTE = [
        ('gel', '❄️ Alerte gel'),
        ('canicule', '🌡️ Alerte canicule'),
        ('pluie', '🌧️ Alerte forte pluie'),
        ('vent', '💨 Alerte vent fort'),
        ('orage', '⛈️ Alerte orage'),
    ]

    STATUT = [
        ('en_attente', '⏳ En attente'),
        ('envoyee', '✅ Envoyée'),
        ('ignoree', '⏭️ Ignorée'),
    ]

    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='alertes_meteo', db_index=True)
    figure = models.ForeignKey(GeometricFigure, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='alertes_meteo')
    type_alerte = models.CharField(max_length=20, choices=TYPE_ALERTE)
    message = models.TextField()
    temperature = models.FloatField(null=True, blank=True)
    date_declenchement = models.DateTimeField(db_index=True)
    date_envoi = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT, default='en_attente', db_index=True)
    canal = models.CharField(max_length=10, default='email')  # email, sms, les_deux

    class Meta:
        ordering = ['-date_declenchement']

    def __str__(self):
        return f"{self.get_type_alerte_display()} - {self.utilisateur.username}"


class Defi(models.Model):
    STATUT_CHOICES = [
        ('actif', '✅ Actif'),
        ('termine', '🏁 Terminé'),
        ('annule', '❌ Annulé'),
    ]

    TYPE_ACTION = [
        ('planter', '🌱 Planter des cultures'),
        ('recolter', '🍅 Récolter des cultures'),
        ('quiz', '🧠 Faire des quiz'),
        ('journal', '📓 Écrire dans le journal'),
        ('points', '⭐ Gagner des points'),
        ('fleur', '🌸 Planter des fleurs'),
    ]

    # Informations générales
    titre = models.CharField(max_length=200)
    description = models.TextField()
    enseignant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='defis_crees')
    classe = models.ForeignKey('Classe', on_delete=models.CASCADE, related_name='defis')

    # Objectif
    type_action = models.CharField(max_length=20, choices=TYPE_ACTION)
    objectif = models.IntegerField(help_text="Nombre d'actions à réaliser")
    points_recompense = models.IntegerField(default=50, help_text="Points pour la classe")

    # Badge de récompense
    badge_nom = models.CharField(max_length=100, blank=True, null=True)
    badge_emoji = models.CharField(max_length=10, blank=True, null=True)

    # Dates
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    date_creation = models.DateTimeField(auto_now_add=True)

    # Statut
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Défi"
        verbose_name_plural = "Défis"

    def __str__(self):
        return f"{self.titre} - {self.classe.nom}"

    def progression_classe(self):
        """Calcule la progression totale de la classe pour ce défi"""
        progres = ProgresDefi.objects.filter(defi=self)
        total = sum(p.valeur_actuelle for p in progres)
        return min(total, self.objectif)

    def est_termine(self):
        return self.progression_classe() >= self.objectif


class ProgresDefi(models.Model):
    """Suivi de la progression d'un élève pour un défi"""
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='progres_defis')
    defi = models.ForeignKey(Defi, on_delete=models.CASCADE, related_name='progres')
    valeur_actuelle = models.IntegerField(default=0)
    valeur_objectif = models.IntegerField()
    est_complete = models.BooleanField(default=False)
    date_completion = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('eleve', 'defi')

    def __str__(self):
        return f"{self.eleve.user.username} - {self.defi.titre}: {self.valeur_actuelle}/{self.valeur_objectif}"

    def ajouter_progression(self, valeur=1):
        """Ajoute de la progression à l'élève"""
        if not self.est_complete:
            self.valeur_actuelle += valeur
            if self.valeur_actuelle >= self.valeur_objectif:
                self.est_complete = True
                self.date_completion = timezone.now()
            self.save()
            return True
        return False

# FORUM ECOLES
class CategorieForum(models.Model):
    """Catégorie du forum"""
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ordre = models.IntegerField(default=0)
    icone = models.CharField(max_length=10, default='💬')

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


class SujetForum(models.Model):
    """Sujet de discussion"""
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sujets_forum')
    categorie = models.ForeignKey(CategorieForum, on_delete=models.CASCADE, related_name='sujets')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_dernier_message = models.DateTimeField(auto_now_add=True)
    est_epingle = models.BooleanField(default=False)
    est_ferme = models.BooleanField(default=False)
    est_supprime = models.BooleanField(default=False)

    # Pour la modération
    moderateur = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='sujets_moderes')
    raison_moderation = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-est_epingle', '-date_dernier_message']
        verbose_name = "Sujet"
        verbose_name_plural = "Sujets"
        indexes = [
            models.Index(fields=['-date_dernier_message']),
            models.Index(fields=['categorie', '-date_dernier_message']),
        ]



    def __str__(self):
        return self.titre

    def nb_reponses(self):
        return self.messages.count() - 1  # -1 pour le premier message

    def dernier_message(self):
        return self.messages.order_by('-date_creation').first()


class MessageForum(models.Model):
    """Message dans un sujet"""
    sujet = models.ForeignKey(SujetForum, on_delete=models.CASCADE, related_name='messages')
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages_forum')
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    est_modere = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_creation']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message de {self.auteur.username} - {self.date_creation.strftime('%d/%m/%Y')}"


class SignalementForum(models.Model):
    """Signalement d'un sujet ou message"""
    STATUT_CHOICES = [
        ('en_attente', '⏳ En attente'),
        ('traite', '✅ Traité'),
        ('refuse', '❌ Refusé'),
    ]

    sujet = models.ForeignKey(SujetForum, on_delete=models.CASCADE, null=True, blank=True, related_name='signalements')
    message = models.ForeignKey(MessageForum, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='signalements')
    signaleur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='signalements_forum')
    raison = models.TextField()
    date_signalement = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    moderateur = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='signalements_traites')
    commentaire_moderation = models.TextField(blank=True)
    est_lu_par_enseignant = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_signalement']

    def __str__(self):
        if self.sujet:
            cible = self.sujet.titre
        elif self.message:
            cible = f"Message #{self.message.id}"
        else:
            cible = "Signalement (sujet ou message supprimé)"
        return f"Signalement de {cible} par {self.signaleur.username}"

class SujetLu(models.Model):
    """Suivi des sujets lus par un utilisateur"""
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sujets_lus')
    sujet = models.ForeignKey(SujetForum, on_delete=models.CASCADE, related_name='lectures')
    dernier_message_lu = models.ForeignKey(MessageForum, on_delete=models.CASCADE, null=True, blank=True)
    date_derniere_lecture = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('utilisateur', 'sujet')
        ordering = ['-date_derniere_lecture']

    def __str__(self):
        return f"{self.utilisateur.username} - {self.sujet.titre[:30]}"


class PhotoJardin(models.Model):
    """Photo de jardin partagée par un utilisateur"""
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='galerie/jardins/%Y/%m/')
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='photos_jardin')
    figure = models.ForeignKey(GeometricFigure, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    # Métadonnées
    likes = models.ManyToManyField(CustomUser, blank=True, related_name='photos_aimees')
    est_publiee = models.BooleanField(default=True)
    est_a_la_une = models.BooleanField(default=False)

    # Pour la modération
    est_validee = models.BooleanField(default=False)  # Validation par enseignant pour les juniors
    moderateur = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='photos_moderees')

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Photo de jardin"
        verbose_name_plural = "Photos de jardin"
        indexes = [
            models.Index(fields=['-date_creation']),
            models.Index(fields=['est_validee', '-date_creation']),
        ]




    def __str__(self):
        return f"{self.titre} - {self.auteur.username}"

    def nb_likes(self):
        return self.likes.count()

    def nb_commentaires(self):
        return self.commentaires.count()


class CommentairePhoto(models.Model):
    """Commentaire sur une photo"""
    photo = models.ForeignKey(PhotoJardin, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='commentaires_photos')
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    est_modere = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_creation']

    def __str__(self):
        return f"Commentaire de {self.auteur.username} sur {self.photo.titre}"




class MissionHebdomadaire(models.Model):
    """Mission automatique qui se renouvelle chaque semaine"""

    TYPES_MISSION = [
        ('planter', '🌱 Planter des cultures'),
        ('recolter', '🍅 Récolter des cultures'),
        ('quiz', '🧠 Faire des quiz'),
        ('journal', '📓 Écrire dans le journal'),
        ('fleur', '🌸 Planter des fleurs'),
        ('connexion', '🔑 Se connecter'),
        ('like', '❤️ Liker des photos'),
        ('commentaire', '💬 Commenter'),
    ]

    SAISONS = [
        ('printemps', '🌷 Printemps (mars-mai)'),
        ('ete', '☀️ Été (juin-août)'),
        ('automne', '🍂 Automne (sept-nov)'),
        ('hiver', '❄️ Hiver (déc-fév)'),
        ('toute', '🔄 Toute l\'année'),
    ]

    CONTINENTS = [
        ('europe', 'Europe'),
        ('afrique', 'Afrique'),
        ('asie', 'Asie'),
        ('amerique', 'Amérique'),
        ('oceanie', 'Océanie'),
        ('tous', 'Tous les continents'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    type_action = models.CharField(max_length=20, choices=TYPES_MISSION)
    objectif = models.IntegerField(default=5)
    points_recompense = models.IntegerField(default=20)
    badge_nom = models.CharField(max_length=100, blank=True)
    badge_emoji = models.CharField(max_length=10, default='🎯')

    # Géolocalisation
    continent = models.CharField(max_length=20, choices=CONTINENTS, default='tous')
    pays = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)

    # Saisonnalité
    saison = models.CharField(max_length=20, choices=SAISONS, default='toute')

    # Culture spécifique
    culture_cible = models.CharField(max_length=100, blank=True, null=True)

    est_active = models.BooleanField(default=True)
    ordre = models.IntegerField(default=0)

    class Meta:
        ordering = ['continent', 'saison', 'ordre']

    def __str__(self):
        lieu = f"{self.get_continent_display()}"
        if self.pays:
            lieu += f" - {self.pays}"
        return f"{self.titre} ({lieu}) - {self.get_saison_display()}"


class ProgressionMissionHebdo(models.Model):
    """Progression de l'élève sur les missions hebdomadaires"""

    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='missions_hebdo')
    mission = models.ForeignKey(MissionHebdomadaire, on_delete=models.CASCADE)
    semaine = models.IntegerField()  # Numéro de semaine (1-52)
    annee = models.IntegerField()
    progression = models.IntegerField(default=0)
    est_complete = models.BooleanField(default=False)
    date_completion = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('eleve', 'mission', 'semaine', 'annee')

    def __str__(self):
        return f"{self.eleve.user.username} - {self.mission.titre} - Semaine {self.semaine}: {self.progression}/{self.mission.objectif}"


class StreakConnexion(models.Model):
    """Suivi des connexions quotidiennes"""

    eleve = models.OneToOneField('Eleve', on_delete=models.CASCADE, related_name='streak')
    jours_actuel = models.IntegerField(default=0)
    jours_max = models.IntegerField(default=0)
    derniere_connexion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.eleve.user.username} - Streak: {self.jours_actuel} jours"


class Competence(models.Model):
    """Compétence à débloquer dans l'arbre"""

    CATEGORIES = [
        ('jardinage', '🌱 Jardinage'),
        ('ecologie', '🌍 Écologie'),
        ('social', '👥 Social'),
        ('savoir', '📚 Savoir'),
        ('special', '⭐ Spécial'),
    ]

    nom = models.CharField(max_length=100)
    description = models.TextField()
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    emoji = models.CharField(max_length=10, default='🌟')
    niveau_requis = models.IntegerField(default=1)  # Niveau minimum
    points_requis = models.IntegerField(default=0)  # Points minimum
    actions_requises = models.JSONField(default=dict)  # {'planter': 10, 'quiz': 5}

    # Prérequis (autres compétences)
    prerequis = models.ManyToManyField('self', symmetrical=False, blank=True)

    # Récompense
    points_recompense = models.IntegerField(default=50)
    badge_nom = models.CharField(max_length=100, blank=True)
    badge_emoji = models.CharField(max_length=10, default='🏅')

    ordre = models.IntegerField(default=0)
    est_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['niveau_requis', 'ordre']

    def __str__(self):
        return f"{self.emoji} {self.nom} (Niv.{self.niveau_requis})"


class CompetenceDebloquee(models.Model):
    """Compétences débloquées par un élève"""

    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='competences')
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    date_deblocage = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('eleve', 'competence')

    def __str__(self):
        return f"{self.eleve.user.username} - {self.competence.nom}"


class PreconisationMondiale(models.Model):
    REGIONS_CLIMATIQUES = [
        ('tropical', '🌴 Tropicale (ex: Amazonie, Congo, Indonésie)'),
        ('tempere', '🌿 Tempérée (ex: France, Allemagne, Japon)'),
        ('mediterraneen', '☀️ Méditerranéenne (ex: Espagne, Italie, Californie)'),
        ('continental', '🌲 Continentale (ex: Russie, Canada, Chine)'),
        ('desertique', '🏜️ Désertique (ex: Sahara, Arizona, Australie)'),
        ('montagnard', '⛰️ Montagnarde (ex: Alpes, Andes, Himalaya)'),
        ('arctique', '❄️ Arctique (ex: Sibérie, Alaska, Groenland)'),
        ('tous', '🌍 Toutes régions'),
    ]

    culture = models.CharField(max_length=100)
    region_climatique = models.CharField(max_length=20, choices=REGIONS_CLIMATIQUES, default='tempere')

    # Semis
    mois_debut_semis = models.IntegerField(help_text="Mois de début recommandé pour le semis (1-12)")
    mois_fin_semis = models.IntegerField(help_text="Mois de fin recommandé pour le semis (1-12)")

    # Plantation
    mois_debut_plantation = models.IntegerField(help_text="Mois de début recommandé pour la plantation (1-12)")
    mois_fin_plantation = models.IntegerField(help_text="Mois de fin recommandé pour la plantation (1-12)")

    # Récolte
    mois_debut_recolte = models.IntegerField(help_text="Mois de début recommandé pour la récolte (1-12)")
    mois_fin_recolte = models.IntegerField(help_text="Mois de fin recommandé pour la récolte (1-12)")

    # Conseils
    conseils = models.TextField(blank=True, help_text="Conseils spécifiques à cette culture dans cette région")

    class Meta:
        unique_together = ('culture', 'region_climatique')
        verbose_name = "Préconisation mondiale"
        verbose_name_plural = "Préconisations mondiales"

    def __str__(self):
        return f"{self.culture} - {self.get_region_climatique_display()}"



class CalendrierSemis(models.Model):
    """Calendrier des semis par région et par culture"""

    culture = models.CharField(max_length=100)  # tomate, carotte, etc.
    region = models.CharField(max_length=100)  # ile-de-france, provence, etc.
    mois_debut_semis = models.IntegerField()  # 1-12
    mois_fin_semis = models.IntegerField()
    mois_debut_recolte = models.IntegerField()
    mois_fin_recolte = models.IntegerField()
    type_plantation = models.CharField(max_length=50, choices=[
        ('pleine_terre', 'Pleine terre'),
        ('sous_abri', 'Sous abri'),
        ('intérieur', 'Intérieur'),
    ], default='pleine_terre')
    conseils = models.TextField(blank=True)

    class Meta:
        unique_together = ('culture', 'region')
        ordering = ['mois_debut_semis']
        indexes = [
            models.Index(fields=['region', 'mois_debut_semis']),
            models.Index(fields=['culture']),
        ]

    def __str__(self):
        return f"{self.culture} - {self.region}"

class Parcelle(models.Model):
    """Parcelle de jardin appartenant à un utilisateur"""
    nom = models.CharField(max_length=100)
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='parcelles', db_index=True)
    figure = models.ForeignKey(GeometricFigure, on_delete=models.SET_NULL, null=True, blank=True)
    surface_m2 = models.FloatField(default=10)
    type_sol = models.CharField(max_length=50, blank=True, choices=[
        ('argileux', 'Argileux'),
        ('sableux', 'Sableux'),
        ('limoneux', 'Limoneux'),
        ('humifère', 'Humifère'),
        ('calcaire', 'Calcaire'),
        ('autre', 'Autre'),
    ])

    irrigation_type = models.CharField(max_length=50, blank=True, choices=[
        ('goutte_a_goutte', 'Goutte-à-goutte'),
        ('aspersion', 'Aspersion'),
        ('manuel', 'Manuel'),
        ('aucun', 'Aucun'),
    ])

    # ✅ EXPOSITION AU SOLEIL / OMBRE
    EXPOSITION_CHOICES = [
        ('plein_soleil', '☀️ Plein soleil (6h+)'),
        ('mi_ombre', '🌤️ Mi-ombre (4-6h)'),
        ('ombre', '🌥️ Ombre (<4h)'),
        ('non_defini', '❓ Non défini'),
    ]

    exposition = models.CharField(
        max_length=20,
        choices=EXPOSITION_CHOICES,
        default='non_defini',
        help_text="Exposition au soleil de la parcelle"
    )

    ombre = models.BooleanField(
        default=False,
        help_text="La parcelle est-elle à l'ombre ?"
    )

    ombre_matin = models.BooleanField(
        default=False,
        help_text="Ombre le matin"
    )

    ombre_apres_midi = models.BooleanField(
        default=False,
        help_text="Ombre l'après-midi"
    )

    date_creation = models.DateTimeField(auto_now_add=True)
    est_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['nom']
        indexes = [
            models.Index(fields=['utilisateur', 'est_active']),
        ]

    def __str__(self):
        return f"{self.nom} - {self.utilisateur.username}"

class Autosuffisance(models.Model):
    """Suivi de l'autosuffisance d'un utilisateur"""

    utilisateur = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='autosuffisance')
    besoin_annuel_kg = models.IntegerField(default=200,
                                           help_text="Estimation des besoins annuels en kg (défaut: 200kg/personne)")
    date_calcul = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.besoin_annuel_kg}kg/an"

    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='autosuffisance_calculs')
    production_totale_kg = models.FloatField(default=0)
    auto_suffisance_pourcentage = models.FloatField(default=0)


class SuggestionCulture(models.Model):
    """Suggestions de cultures personnalisées"""

    SAISONS = [
        ('printemps', 'Printemps'),
        ('ete', 'Été'),
        ('automne', 'Automne'),
        ('hiver', 'Hiver'),
    ]

    culture = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, default='🌱')
    saison = models.CharField(max_length=20, choices=SAISONS)
    difficulte = models.IntegerField(default=1, choices=[(1, 'Facile'), (2, 'Moyen'), (3, 'Difficile')])
    temps_pousse = models.IntegerField(help_text="Temps de pousse en jours", default=60)
    espace_requis = models.CharField(max_length=50, default="1m²")
    conseil = models.TextField(blank=True)
    raison = models.TextField(blank=True, help_text="Pourquoi cette suggestion")

    class Meta:
        ordering = ['saison', 'difficulte']

    def __str__(self):
        return f"{self.emoji} {self.culture} - {self.get_saison_display()}"


# Configuration des rappels automatiques par mails

class RappelUtilisateur(models.Model):
        TYPES_RAPPEL = [
            ('semis', '🌱 Semis'),
            ('arrosage', '💧 Arrosage'),
            ('recolte', '🍅 Récolte'),
            ('taille', '✂️ Taille'),
            ('engrais', '🌿 Fertilisation'),
        ]

        utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rappels')
        type_rappel = models.CharField(max_length=20, choices=TYPES_RAPPEL)
        culture = models.CharField(max_length=100, blank=True, null=True)
        message_personnalise = models.TextField(blank=True)
        date_prochain_rappel = models.DateField()
        frequence_jours = models.IntegerField(default=7, help_text="Fréquence en jours (0 = unique)")
        actif = models.BooleanField(default=True)
        date_creation = models.DateTimeField(auto_now_add=True)
        dernier_envoi = models.DateTimeField(null=True, blank=True)

        class Meta:
            ordering = ['date_prochain_rappel']

        def __str__(self):
            return f"{self.utilisateur.username} - {self.get_type_rappel_display()} - {self.date_prochain_rappel}"


class CalendrierUser(models.Model):
    """Calendrier des semis personnalisé par utilisateur"""

    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='calendrier_semis')
    culture = models.CharField(max_length=100)

    # Dates de semis
    date_semis = models.DateField(null=True, blank=True)
    mois_semis = models.IntegerField(null=True, blank=True)

    # Dates de plantation
    date_plantation = models.DateField(null=True, blank=True)
    mois_plantation = models.IntegerField(null=True, blank=True)

    # Dates de récolte prévue
    date_recolte_prevue = models.DateField(null=True, blank=True)
    mois_recolte = models.IntegerField(null=True, blank=True)

    # Métadonnées
    figure = models.ForeignKey(GeometricFigure, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('utilisateur', 'culture')
        ordering = ['mois_semis', 'culture']

    def __str__(self):
        return f"{self.utilisateur.username} - {self.culture}"

    def save(self, *args, **kwargs):
        # Extraire le mois des dates
        if self.date_semis:
            self.mois_semis = self.date_semis.month
        if self.date_plantation:
            self.mois_plantation = self.date_plantation.month
        if self.date_recolte_prevue:
            self.mois_recolte = self.date_recolte_prevue.month
        super().save(*args, **kwargs)


# Calcul de la quantité d'eau en fonction de la région  d'où se trouve la parcelle



class BesoinsEau(models.Model):
    """Besoins en eau des cultures selon la région"""

    culture = models.CharField(max_length=100)
    besoin_litres_par_m2 = models.FloatField(help_text="Besoins en litres par m² par semaine (base)")

    # Coefficients climatiques par région
    coefficient_region = models.JSONField(default=dict, help_text='{"iledefrance": 1.0, "provence": 1.5, "nord": 0.8}')

    frequence_arrosage_jours = models.IntegerField(default=3, help_text="Fréquence d'arrosage recommandée en jours")
    periode_sensible = models.CharField(max_length=200, blank=True, help_text="Période où l'eau est critique")
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE, null=True, blank=True, related_name='besoins_eau')

    class Meta:
        indexes = [
            models.Index(fields=['parcelle']),
        ]

    def __str__(self):
        return f"{self.culture} - {self.besoin_litres_par_m2} L/m²/semaine"


class RotationCulture(models.Model):
    """Plan de rotation des cultures sur 4 ans"""

    culture = models.CharField(max_length=100)
    famille = models.CharField(max_length=100, help_text="Famille botanique (ex: Solanacées, Légumineuses...)")
    annee1 = models.CharField(max_length=100, blank=True, help_text="Idéal après")
    annee2 = models.CharField(max_length=100, blank=True, help_text="À éviter après")
    annee3 = models.CharField(max_length=100, blank=True, help_text="Bon après")
    annee4 = models.CharField(max_length=100, blank=True, help_text="Idéal avant")
    conseils = models.TextField(blank=True)

    class Meta:
        ordering = ['famille', 'culture']

    def __str__(self):
        return f"{self.culture} ({self.famille})"


class AssociationCulture(models.Model):
    TYPE_ASSOCIATION = [
        ('bonne', '✅ Bonne association'),
        ('mauvaise', '❌ Mauvaise association'),
    ]

    culture1 = models.CharField(max_length=100)
    culture2 = models.CharField(max_length=100)
    type_association = models.CharField(max_length=20, choices=TYPE_ASSOCIATION)
    benefice = models.TextField(blank=True, help_text="Bénéfice de l'association")

    # 🌍 Géolocalisation
    pays = models.CharField(max_length=100, default='tous')
    region = models.CharField(max_length=100, blank=True, null=True)
    climat = models.CharField(max_length=50, blank=True, null=True,
                              choices=[('tropical', 'Tropical'), ('tempere', 'Tempéré'),
                                       ('mediterraneen', 'Méditerranéen'), ('continental', 'Continental'),
                                       ('desertique', 'Désertique'), ('tous', 'Tous')])

    class Meta:
        unique_together = ('culture1', 'culture2', 'pays', 'region')

    def __str__(self):
        lieu = f"{self.pays}"
        if self.region:
            lieu += f" - {self.region}"
        return f"{self.culture1} + {self.culture2} ({lieu}) - {self.get_type_association_display()}"





class Culture(models.Model):
    """Culture plantée sur une parcelle"""
    TYPES_CULTURE = [
        ('legume', '🥬 Légume'),
        ('fruit', '🍎 Fruit'),
        ('aromatique', '🌿 Aromatique'),
        ('fleur', '🌸 Fleur'),
        ('cereale', '🌾 Céréale'),
    ]

    nom = models.CharField(max_length=100, db_index=True)
    # ✅ Lien vers la famille botanique (optionnel)
    famille = models.ForeignKey(
        'ConseilsFamille',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='cultures',
        verbose_name="Famille botanique"
    )
    # ✅ Surcharges possibles (si différents de la famille)
    temperature_min = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température minimale spécifique (°C)",
        help_text="Si différent de la famille"
    )
    temperature_optimale_min = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température optimale min. spécifique (°C)"
    )
    temperature_optimale_max = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température optimale max. spécifique (°C)"
    )
    temperature_max = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température maximale spécifique (°C)"
    )

    duree_culture_min_jours = models.IntegerField(
        null=True, blank=True,
        verbose_name="Durée minimale spécifique (jours)"
    )
    duree_culture_max_jours = models.IntegerField(
        null=True, blank=True,
        verbose_name="Durée maximale spécifique (jours)"
    )

    methode_plantation = models.CharField(
        max_length=50, blank=True,
        choices=[
            ('graine', '🌰 Graine'),
            ('rhizome', '🫚 Rhizome'),
            ('bulbe', '🧄 Bulbe'),
            ('tubercule', '🥔 Tubercule'),
            ('plant', '🌱 Plant / Semis'),
            ('bouture', '🌿 Bouture'),
            ('greffe', '🌳 Greffe'),
            ('division', '🌾 Division de touffe'),
        ],
        verbose_name="Méthode de plantation spécifique"
    )

    hivernage = models.CharField(
        max_length=50, blank=True,
        choices=[
            ('plein_air', '🌳 Plein air (rustique)'),
            ('serre', '🏠 Serre ou abri'),
            ('interieur', '🏡 Intérieur obligatoire'),
            ('climat_doux', '🌞 Climat doux uniquement'),
        ],
        verbose_name="Hivernage spécifique"
    )

    # ✅ Conseils spécifiques (surcharge la famille)
    conseils_climat = models.TextField(
        blank=True,
        verbose_name="Conseils climat spécifiques"
    )
    conseils_plantation = models.TextField(
        blank=True,
        verbose_name="Conseils plantation spécifiques"
    )
    conseils_arrosage = models.TextField(
        blank=True,
        verbose_name="Conseils arrosage spécifiques"
    )
    conseils_fertilisation = models.TextField(
        blank=True,
        verbose_name="Conseils fertilisation spécifiques"
    )
    conseils_protection = models.TextField(
        blank=True,
        verbose_name="Conseils protection spécifiques"
    )
    conseils_recolte = models.TextField(
        blank=True,
        verbose_name="Conseils récolte spécifiques"
    )
    conseils_conservation = models.TextField(
        blank=True,
        verbose_name="Conseils conservation spécifiques"
    )
    type_culture = models.CharField(max_length=20, choices=TYPES_CULTURE)
    emoji = models.CharField(max_length=10, default='🌱')

    # Référence aux modèles existants
    vegetable = models.ForeignKey(Vegetable, on_delete=models.SET_NULL, null=True, blank=True)
    fruit = models.ForeignKey(Fruit, on_delete=models.SET_NULL, null=True, blank=True)

    # Informations de culture
    besoin_eau_litres_jour = models.FloatField(default=1)
    jours_pousse = models.IntegerField(default=60)
    saison_plantation = models.CharField(max_length=100, blank=True)
    conseils = models.TextField(blank=True)

    # Nouveau champs pour les seuils meteo
    temperature_mingel = models.IntegerField(default=0, help_text="Température minimale avant gel (°C)")
    temperature_max_canicule = models.IntegerField(default=35, help_text="Température maximale avant canicule (°C)")
    precipitation_max = models.IntegerField(default=20,
                                            help_text="Précipitations maximales avant alerte forte pluie (mm)")
    vent_max = models.IntegerField(default=50, help_text="Vitesse maximale du vent avant alerte vent fort (km/h)")

    # ✅ TAILLE DES PLANTES
    hauteur_min_cm = models.IntegerField(
        null=True, blank=True,
        help_text="Hauteur minimale à maturité (en cm)"
    )
    hauteur_max_cm = models.IntegerField(
        null=True, blank=True,
        help_text="Hauteur maximale à maturité (en cm)"
    )
    largeur_min_cm = models.IntegerField(
        null=True, blank=True,
        help_text="Largeur minimale à maturité (en cm)"
    )
    largeur_max_cm = models.IntegerField(
        null=True, blank=True,
        help_text="Largeur maximale à maturité (en cm)"
    )
    espacement_cm = models.IntegerField(
        null=True, blank=True,
        help_text="Espacement recommandé entre les plants (en cm)"
    )
    espacement_rangs_cm = models.IntegerField(
        null=True, blank=True,
        help_text="Espacement recommandé entre les rangs (en cm)"
    )

    def __str__(self):
        return self.nom

    def get_emoji(self):
        if self.vegetable:
            return self.vegetable.get_emoji()
        elif self.fruit:
            return self.fruit.get_emoji()
        return self.emoji


class Production(models.Model):
    """Production récoltée sur une parcelle"""
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE, related_name='productions')
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE)
    quantite_kg = models.FloatField(default=0)
    date_recolte = models.DateField(default=timezone.now)
    qualite = models.CharField(max_length=20, default='standard', choices=[
        ('excellente', 'Excellente'),
        ('bonne', 'Bonne'),
        ('standard', 'Standard'),
        ('mauvaise', 'Mauvaise'),
    ])
    commentaire = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_recolte']
        indexes = [
            models.Index(fields=['parcelle']),
        ]

    def __str__(self):
        return f"{self.parcelle.nom} - {self.culture.nom} - {self.quantite_kg}kg"


class BilanCarbone(models.Model):
    """Bilan carbone d'une parcelle"""
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE, related_name='bilans_carbone')
    date_calcul = models.DateField(auto_now_add=True)

    # Émissions
    emission_co2_kg = models.FloatField(default=0)
    emission_n2o_kg = models.FloatField(default=0)

    # Séquestration
    sequestration_co2_kg = models.FloatField(default=0)

    # Bilan net
    bilan_net_kg = models.FloatField(default=0)

    # Détails
    details = models.JSONField(default=dict)  # Stocke les détails du calcul

    class Meta:
        ordering = ['-date_calcul']

    def __str__(self):
        return f"{self.parcelle.nom} - {self.date_calcul} - {self.bilan_net_kg} kg"


class RecommandationFertilisation(models.Model):
    """Recommandations de fertilisation selon la culture et le type de sol"""

    culture = models.CharField(max_length=100)
    type_sol = models.CharField(max_length=50, choices=[
        ('argileux', 'Argileux'),
        ('sableux', 'Sableux'),
        ('limoneux', 'Limoneux'),
        ('humifère', 'Humifère'),
        ('calcaire', 'Calcaire'),
        ('tous', 'Tous'),
    ], default='tous')

    saison = models.CharField(max_length=20, choices=[
        ('printemps', 'Printemps'),
        ('ete', 'Été'),
        ('automne', 'Automne'),
        ('hiver', 'Hiver'),
        ('toute', 'Toute l\'année'),
    ], default='toute')

    engrais_recommande = models.CharField(max_length=100, help_text="Ex: 'NPK 10-10-10', 'Fumier composté'")
    quantite_recommandee = models.CharField(max_length=50, help_text="Ex: '30 g/m²', '2 kg/m²'")
    frequence = models.CharField(max_length=50, help_text="Ex: 'Tous les 15 jours', 'Une fois par mois'")
    conseils = models.TextField(blank=True, help_text="Conseils supplémentaires")

    class Meta:
        verbose_name = "Recommandation de fertilisation"
        verbose_name_plural = "Recommandations de fertilisation"
        ordering = ['culture', 'saison']

    def __str__(self):
        return f"{self.culture} - {self.get_type_sol_display()} - {self.get_saison_display()}"


class Maladie(models.Model):
    """Modèle pour les maladies des plantes avec adaptation géographique"""

    nom = models.CharField(max_length=200)
    nom_scientifique = models.CharField(max_length=200, blank=True)
    emoji = models.CharField(max_length=10, default='🦠')

    # Symptômes (stockés sous forme de tags)
    symptomes = models.JSONField(default=list,
                                 help_text="Liste des symptômes (ex: ['taches brunes', 'tache brune', 'taches, 'flétrissure', 'flétri', 'fané', décoloration'])")

    # Cultures concernées
    cultures_cible = models.JSONField(default=list,
                                      help_text="Liste des cultures sensibles (ex: ['tomate', 'pomme de terre'])")

    # Régions où la maladie est présente
    regions = models.JSONField(default=list,
                               help_text="Liste des régions concernées (ex: ['europe', 'afrique', 'iledefrance'])")
    pays = models.JSONField(default=list, help_text="Liste des pays concernés (ex: ['France', 'Espagne'])")
    climat = models.CharField(max_length=50, blank=True, choices=[
        ('tropical', 'Tropical'),
        ('tempere', 'Tempéré'),
        ('mediterraneen', 'Méditerranéen'),
        ('continental', 'Continental'),
        ('desertique', 'Désertique'),
        ('tous', 'Tous'),
    ])

    # Traitements
    traitement_chimique = models.TextField(blank=True, help_text="Traitement chimique recommandé")
    traitement_biologique = models.TextField(blank=True, help_text="Traitement biologique ou naturel recommandé")
    prevention = models.TextField(blank=True, help_text="Mesures préventives")

    # Informations supplémentaires
    gravite = models.CharField(max_length=20, choices=[
        ('faible', 'Faible'),
        ('moyenne', 'Moyenne'),
        ('elevee', 'Élevée'),
    ], default='moyenne')

    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Maladie"
        verbose_name_plural = "Maladies"
        ordering = ['nom']

    def __str__(self):
        return f"{self.emoji} {self.nom}"



from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Eleve
from datetime import date

User = get_user_model()


@receiver(post_save, sender=User)
def activer_mode_junior_pour_mineurs(sender, instance, created, **kwargs):
    """
    Active automatiquement mode_junior pour les utilisateurs mineurs (< 18 ans).

    ⚠️ IMPORTANT : Ne crée PAS de profil Eleve automatiquement.

    Un profil Eleve est créé UNIQUEMENT quand l'utilisateur rejoint
    une classe (voir vues `rejoindre_classe` et `inscription_eleve`).

    Un mineur peut être :
      - Un particulier (jardinier en herbe, pas de classe)
      - Un enfant de particulier (compte créé par un parent)
      - Un élève (inscrit via code de classe par un enseignant)
    """
    # Sécurité : si pas de date de naissance, on ne fait rien
    if not instance.birth_date:
        return

    # Calcul de l'âge exact
    today = date.today()
    age = today.year - instance.birth_date.year - (
            (today.month, today.day) < (instance.birth_date.month, instance.birth_date.day)
    )

    # Si mineur → activer mode_junior
    if age < 18:
        if not instance.mode_junior:
            # ⚠️ Utilisation de update() pour ÉVITER de re-déclencher post_save
            # (sinon boucle infinie)
            User.objects.filter(pk=instance.pk).update(mode_junior=True)
            instance.mode_junior = True  # maj en mémoire
            print(f"🌿 mode_junior activé pour {instance.username} ({age} ans)")

    # Si majeur → désactiver mode_junior s'il était activé par erreur
    elif instance.mode_junior:
        User.objects.filter(pk=instance.pk).update(mode_junior=False)
        instance.mode_junior = False
        print(f"🔓 mode_junior désactivé pour {instance.username} ({age} ans, majeur)")


class MaladieCulture(models.Model):
    """Maladie des cultures avec conditions de développement"""

    GRAVITE_CHOICES = [
        ('faible', '🟢 Faible'),
        ('moyenne', '🟡 Moyenne'),
        ('elevee', '🟠 Élevée'),
        ('critique', '🔴 Critique'),
    ]

    nom = models.CharField(max_length=100)
    nom_scientifique = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    emoji = models.CharField(max_length=10, default='🦠')

    # Cultures concernées (ManyToMany vers Culture)
    cultures = models.ManyToManyField('Culture', related_name='maladies', blank=True)
    # Ou liste de noms si tu préfères
    cultures_cibles = models.JSONField(default=list, help_text="Liste des noms de cultures concernées")

    # Conditions climatiques favorables
    temperature_min = models.FloatField(null=True, blank=True, help_text="Température minimale favorable (°C)")
    temperature_max = models.FloatField(null=True, blank=True, help_text="Température maximale favorable (°C)")
    humidite_min = models.FloatField(null=True, blank=True, help_text="Humidité minimale favorable (%)")
    humidite_max = models.FloatField(null=True, blank=True, help_text="Humidité maximale favorable (%)")
    precipitation_min = models.FloatField(null=True, blank=True, help_text="Précipitations minimales favorables (mm)")
    precipitation_max = models.FloatField(null=True, blank=True, help_text="Précipitations maximales favorables (mm)")

    # Période d'activité
    mois_debut = models.IntegerField(null=True, blank=True, help_text="Mois de début (1-12)")
    mois_fin = models.IntegerField(null=True, blank=True, help_text="Mois de fin (1-12)")

    # Régions concernées
    regions = models.JSONField(default=list, help_text="Liste des régions concernées (ex: ['iledefrance', 'provence'])")

    # Traitements
    traitement_preventif = models.TextField(blank=True, help_text="Traitement préventif recommandé")
    traitement_curatif = models.TextField(blank=True, help_text="Traitement curatif recommandé")
    produits_recommandes = models.JSONField(default=list, blank=True, help_text="Liste des produits recommandés")

    # Délai d'alerte (jours avant le pic de risque)
    delai_alerte_jours = models.IntegerField(default=3, help_text="Nombre de jours avant le pic de risque")

    # Gravité
    gravite = models.CharField(max_length=10, choices=GRAVITE_CHOICES, default='moyenne')

    # Statistiques
    frequence_annuelle = models.IntegerField(default=1, help_text="Nombre d'occurrences par an")

    # 🔥 NOUVEAU : Stades sensibles
    stades_sensibles = models.JSONField(
        default=list,
        help_text="Liste des stades où la maladie est active (ex: ['floraison', 'fructification'])"
    )

    # 🔥 NOUVEAU : Niveau de risque par stade
    risque_par_stade = models.JSONField(
        default=dict,
        help_text="Niveau de risque par stade (ex: {'floraison': 'elevee', 'croissance': 'moyenne'})"
    )

    class Meta:
        verbose_name = "Maladie des cultures"
        verbose_name_plural = "Maladies des cultures"
        ordering = ['nom']

    def __str__(self):
        return f"{self.emoji} {self.nom}"

    def get_cultures_list(self):
        """Retourne la liste des cultures concernées"""
        if self.cultures.exists():
            return list(self.cultures.values_list('nom', flat=True))
        return self.cultures_cibles or []


class AlerteTraitement(models.Model):
    """Alerte de traitement pour une culture spécifique"""

    STATUT_CHOICES = [
        ('en_attente', '⏳ En attente'),
        ('envoyee', '📧 Envoyée'),
        ('traitee', '✅ Traitée'),
        ('ignoree', '⏭️ Ignorée'),
    ]

    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='alertes_traitements')
    figure = models.ForeignKey('GeometricFigure', on_delete=models.CASCADE, related_name='alertes_traitements')
    culture = models.ForeignKey('Culture', on_delete=models.CASCADE, related_name='alertes_traitements')
    maladie = models.ForeignKey(MaladieCulture, on_delete=models.CASCADE, related_name='alertes_traitements')

    message = models.TextField()
    conseils = models.TextField(blank=True, help_text="Conseils pour le traitement")

    date_creation = models.DateTimeField(auto_now_add=True)
    date_declenchement = models.DateTimeField()
    date_traitement = models.DateTimeField(null=True, blank=True)
    date_ignoration = models.DateTimeField(null=True, blank=True)
    date_envoi = models.DateTimeField(null=True, blank=True)

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    # Détails météo au moment du déclenchement
    temperature = models.FloatField(null=True, blank=True)
    humidite = models.FloatField(null=True, blank=True)
    precipitation = models.FloatField(null=True, blank=True)
    vent = models.FloatField(null=True, blank=True)

    # Niveau de risque
    niveau_risque = models.CharField(max_length=20, choices=MaladieCulture.GRAVITE_CHOICES, default='moyenne')

    conditions_meteo = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="conditions meteo"
    )

    # ✅ NOUVEAUX CHAMPS POUR LA CONTAMINATION
    est_contamination = models.BooleanField(default=False, verbose_name="Alerte de contamination")
    message_contamination = models.TextField(blank=True, null=True, verbose_name="Message de contamination")
    parcelles_voisines = models.JSONField(default=list, blank=True, verbose_name="Parcelles voisines")

    class Meta:
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['utilisateur', 'statut']),
            models.Index(fields=['figure', 'statut']),
        ]

    def __str__(self):
        return f"{self.culture.nom} - {self.maladie.nom} ({self.get_statut_display()})"

    def marquer_traitee(self):
        self.statut = 'traitee'
        self.date_traitement = timezone.now()
        self.save()

    def marquer_ignoree(self):
        self.statut = 'ignoree'
        self.date_ignoration = timezone.now()
        self.save()


class CalendrierTraitements(models.Model):
    """Calendrier des traitements préventifs par culture et région"""

    culture = models.CharField(max_length=100)
    mois = models.IntegerField(help_text="Mois du traitement (1-12)")
    traitement = models.TextField()
    maladie_cible = models.CharField(max_length=100, blank=True, help_text="Maladie ciblée")
    region = models.CharField(max_length=100, default='tous')
    produits = models.JSONField(default=list, blank=True, help_text="Produits recommandés")
    conseils = models.TextField(blank=True)

    class Meta:
        unique_together = ('culture', 'mois', 'region')
        ordering = ['mois', 'culture']

    def __str__(self):
        return f"{self.culture} - Mois {self.mois} - {self.region}"



class Variete(models.Model):
    """
        Variété d'une culture (fruit ou légume) avec géolocalisation
        """
    culture = models.ForeignKey(
        Culture,
        on_delete=models.CASCADE,
        related_name='varietes'
    )
    nom = models.CharField(max_length=200)
    nom_scientifique = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    emoji = models.CharField(max_length=10, blank=True, null=True)

    # 🌍 GÉOLOCALISATION
    zones_geographiques = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Zones où cette variété est cultivée (ex: Europe, Asie, Amérique)"
    )
    pays_origine = models.CharField(max_length=200, blank=True, null=True)
    climat = models.CharField(max_length=100, blank=True, null=True,
                              choices=[('tropical', 'Tropical'),
                                       ('tempere', 'Tempéré'),
                                       ('continental', 'Continental'),
                                       ('mediterraneen', 'Méditerranéen'),
                                       ('desertique', 'Désertique'),
                                       ('montagnard', 'Montagnard')])

    # 📊 CARACTÉRISTIQUES
    saison = models.CharField(max_length=100, blank=True, null=True)
    jours_recolte = models.IntegerField(null=True, blank=True)
    temperature_min = models.FloatField(null=True, blank=True)
    temperature_max = models.FloatField(null=True, blank=True)
    resistance_maladies = models.TextField(blank=True, null=True)

    # 🏷️ TAGS
    est_ancienne = models.BooleanField(default=False)
    est_rustique = models.BooleanField(default=False)
    est_productive = models.BooleanField(default=False)
    est_hybride = models.BooleanField(default=False)
    origine = models.CharField(max_length=200, blank=True, null=True)

    # 📷 PHOTOS
    photo = models.ImageField(upload_to='varietes/', blank=True, null=True)

    # ⭐ POPULARITÉ (pour le classement)
    popularite = models.IntegerField(default=0)

    # 📅 DATE
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']
        unique_together = ['culture', 'nom']

    def __str__(self):
        return f"{self.culture.nom} - {self.nom}"


class TauxChange(models.Model):
    """
    Taux de change entre une devise et l'EUR (devise pivot).
    Modifiable manuellement en admin OU mis à jour par API.
    """
    DEVISE_CHOICES = [
        ('EUR', '🇪🇺 Euro (€)'),
        ('USD', '🇺🇸 Dollar américain ($)'),
        ('GBP', '🇬🇧 Livre sterling (£)'),
        ('CHF', '🇨🇭 Franc suisse (CHF)'),
        ('CAD', '🇨🇦 Dollar canadien (C$)'),
        ('XOF', '🌍 Franc CFA BCEAO (CFA)'),
        ('XAF', '🌍 Franc CFA BEAC (FCFA)'),
        ('MAD', '🇲🇦 Dirham marocain (DH)'),
        ('DZD', '🇩🇿 Dinar algérien (DA)'),
        ('TND', '🇹🇳 Dinar tunisien (DT)'),
        ('JPY', '🇯🇵 Yen japonais (¥)'),
        ('CNY', '🇨🇳 Yuan chinois (¥)'),
        ('BRL', '🇧🇷 Réal brésilien (R$)'),
        ('MXN', '🇲🇽 Peso mexicain ($)'),
        ('AUD', '🇦🇺 Dollar australien (A$)'),
        ('INR', '🇮🇳 Roupie indienne (₹)'),
        ('ZAR', '🇿🇦 Rand sud-africain (R)'),
    ]

    SOURCES = [
        ('api', '🤖 API auto'),
        ('manuel', '✍️ Manuel'),
        ('defaut', '📌 Valeur par défaut'),
    ]

    devise = models.CharField(
        max_length=3,
        choices=DEVISE_CHOICES,
        unique=True,
        verbose_name="Code devise"
    )
    taux_vs_eur = models.FloatField(
        help_text="Combien d'unités de cette devise pour 1 EUR (ex: 655.957 pour XOF)",
        verbose_name="Taux de change"
    )
    symbole = models.CharField(
        max_length=10,
        help_text="Symbole affiché (ex: '€', '$', 'CFA')",
        verbose_name="Symbole"
    )
    position_symbole = models.CharField(
        max_length=10,
        choices=[('avant', 'Avant (ex: $10)'), ('apres', 'Après (ex: 10 €)')],
        default='apres',
        verbose_name="Position du symbole"
    )
    source = models.CharField(
        max_length=20,
        choices=SOURCES,
        default='api',
        verbose_name="Source"
    )
    date_maj = models.DateTimeField(auto_now=True)
    est_actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Taux de change"
        verbose_name_plural = "Taux de change"
        ordering = ['devise']

    def __str__(self):
        return f"{self.devise} : {self.taux_vs_eur}"

    def convertir_depuis_eur(self, montant_eur):
        """Convertit un montant en EUR vers cette devise."""
        return round(montant_eur * self.taux_vs_eur, 2)

    def formater(self, montant_eur):
        """Retourne une chaîne formatée (ex: '10,50 €', 'CFA 6 559')."""
        montant = self.convertir_depuis_eur(montant_eur)
        if montant >= 100:
            montant_str = f"{int(round(montant)):,}".replace(',', ' ')
        else:
            montant_str = f"{montant:,.2f}".replace(',', ' ').replace('.', ',')

        if self.position_symbole == 'avant':
            return f"{self.symbole} {montant_str}"
        return f"{montant_str} {self.symbole}"

class RendementCulture(models.Model):
    """
    Rendement de référence par culture (kg par plant/pied).
    Sert à valoriser le jardin et calculer les économies.
    Modifiable via Django admin pour enrichir sans redéployer.
    """
    REGIONS_CLIMATIQUES = [
        ('tous', '🌍 Toutes régions'),
        ('tempere', '🌿 Tempéré'),
        ('mediterraneen', '☀️ Méditerranéen'),
        ('continental', '❄️ Continental'),
        ('tropical', '🌴 Tropical'),
        ('desertique', '🏜️ Désertique'),
        ('montagnard', '🏔️ Montagnard'),
    ]

    SOURCES = [
        ('fao', '📊 FAO'),
        ('inra', '🇫🇷 INRA'),
        ('jardinier', '🧑‍🌾 Retour jardiniers'),
        ('estimation', '📈 Estimation'),
        ('autre', '❓ Autre'),
    ]

    culture_nom = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Nom normalisé (ex: 'tomate', 'carotte')",
        verbose_name="Nom de la culture"
    )
    culture = models.ForeignKey(
        'Culture',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='rendements',
        help_text="Lien optionnel vers la fiche culture détaillée"
    )
    rendement_kg_par_plant = models.FloatField(
        help_text="Rendement moyen en kg par plant/pied",
        verbose_name="Rendement (kg/plant)"
    )
    region_climatique = models.CharField(
        max_length=50,
        choices=REGIONS_CLIMATIQUES,
        default='tous',
        verbose_name="Région climatique"
    )
    source = models.CharField(
        max_length=20,
        choices=SOURCES,
        default='estimation',
        verbose_name="Source"
    )
    notes = models.TextField(
        blank=True,
        help_text="Précisions : variété, conditions, année de référence…"
    )
    est_actif = models.BooleanField(
        default=True,
        help_text="Décocher pour désactiver sans supprimer"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Rendement par culture"
        verbose_name_plural = "Rendements par culture"
        unique_together = [('culture_nom', 'region_climatique')]
        ordering = ['culture_nom', 'region_climatique']
        indexes = [
            models.Index(fields=['culture_nom', 'region_climatique', 'est_actif']),
        ]

    def __str__(self):
        region = f" ({self.get_region_climatique_display()})" if self.region_climatique != 'tous' else ""
        return f"{self.culture_nom} — {self.rendement_kg_par_plant} kg/plant{region}"


class HistoriqueValeurJardin(models.Model):
    """
    Snapshot mensuel de la valeur du jardin d'un utilisateur.
    Permet de tracer une courbe d'évolution.
    """
    utilisateur = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='historique_valeur',
    )
    mois = models.DateField(
        help_text="Premier jour du mois",
        db_index=True,
    )
    valeur_potentielle = models.FloatField(default=0)
    valeur_realisee = models.FloatField(default=0)
    nb_cultures = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historique valeur jardin"
        verbose_name_plural = "Historiques valeur jardin"
        unique_together = [('utilisateur', 'mois')]
        ordering = ['-mois']
        indexes = [
            models.Index(fields=['utilisateur', '-mois']),
        ]

    def __str__(self):
        return f"{self.utilisateur.username} - {self.mois.strftime('%m/%Y')} : {self.valeur_potentielle}€"
# ============================================================
# MODÈLES FORUM ADULTE (indépendants du forum école)
# ============================================================

class ForumAdulteCategorie(models.Model):
    """Catégorie du forum adulte"""
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    icone = models.CharField(max_length=10, default='💬')
    ordre = models.IntegerField(default=0)
    est_active = models.BooleanField(default=True)
    est_premium = models.BooleanField(default=False)

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name_plural = "Catégories forum adulte"

    def __str__(self):
        return f"{self.icone} {self.nom}"

    def nb_sujets(self):
        return self.sujets.filter(est_supprime=False).count()

    def nb_messages(self):
        return MessageForumAdulte.objects.filter(sujet__categorie=self).count()

    def dernier_sujet(self):
        return self.sujets.filter(est_supprime=False).order_by('-date_dernier_message').first()


class ForumAdulteSujet(models.Model):
    """Sujet du forum adulte"""
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sujets_adulte')
    categorie = models.ForeignKey(ForumAdulteCategorie, on_delete=models.CASCADE, related_name='sujets')

    est_epingle = models.BooleanField(default=False)
    est_ferme = models.BooleanField(default=False)
    est_supprime = models.BooleanField(default=False)
    est_premium = models.BooleanField(default=False)

    date_creation = models.DateTimeField(auto_now_add=True)
    date_dernier_message = models.DateTimeField(auto_now=True)
    vues = models.IntegerField(default=0)
    nb_votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-est_epingle', '-date_dernier_message']
        verbose_name_plural = "Sujets forum adulte"

    def __str__(self):
        return f"{'🔒 ' if self.est_premium else ''}{self.titre}"

    def nb_messages(self):
        return self.messages.filter(est_supprime=False).count()

    def get_dernier_message(self):
        return self.messages.filter(est_supprime=False).order_by('-date_creation').first()

    def get_premier_message(self):
        return self.messages.filter(est_supprime=False).order_by('date_creation').first()


class MessageForumAdulte(models.Model):
    """
    ✅ MESSAGE DU FORUM ADULTE
    Cette classe est bien déclarée ici avec toutes ses relations
    """
    sujet = models.ForeignKey(ForumAdulteSujet, on_delete=models.CASCADE, related_name='messages')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_adulte')
    contenu = models.TextField()

    est_premium = models.BooleanField(default=False)
    est_supprime = models.BooleanField(default=False)
    est_solution = models.BooleanField(default=False)

    nb_upvotes = models.IntegerField(default=0)
    nb_downvotes = models.IntegerField(default=0)

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_creation']
        verbose_name_plural = "Messages forum adulte"

    def __str__(self):
        return f"Message de {self.auteur.username} - {self.date_creation.strftime('%d/%m/%Y')}"

    def score(self):
        return self.nb_upvotes - self.nb_downvotes


class ForumAdulteVote(models.Model):
    """Vote sur un message (Premium uniquement)"""
    TYPES_VOTE = [
        ('up', '👍 Upvote'),
        ('down', '👎 Downvote'),
    ]

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.ForeignKey(MessageForumAdulte, on_delete=models.CASCADE, related_name='votes')
    type_vote = models.CharField(max_length=10, choices=TYPES_VOTE)
    date_vote = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['utilisateur', 'message']
        verbose_name_plural = "Votes forum adulte"

    def __str__(self):
        return f"{self.utilisateur.username} → {self.type_vote}"


class ForumAdulteSignalement(models.Model):
    """Signalement de contenu inapproprié"""
    STATUTS = [
        ('en_attente', '⏳ En attente'),
        ('en_cours', '🔍 En cours'),
        ('traite', '✅ Traité'),
        ('refuse', '❌ Refusé'),
        ('archive', '📦 Archivé'),
    ]

    TYPES_CONTENU = [
        ('sujet', 'Sujet'),
        ('message', 'Message'),
    ]

    type_contenu = models.CharField(max_length=10, choices=TYPES_CONTENU)
    sujet = models.ForeignKey(ForumAdulteSujet, on_delete=models.CASCADE, null=True, blank=True)
    message = models.ForeignKey(MessageForumAdulte, on_delete=models.CASCADE, null=True, blank=True)
    signaleur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='signalements_adulte')
    raison = models.TextField()
    details = models.TextField(blank=True)

    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    moderateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='signalements_traites_adulte')
    commentaire_moderation = models.TextField(blank=True)

    date_signalement = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)
    est_notifie_signaleur = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_signalement']
        verbose_name_plural = "Signalements forum adulte"

    def __str__(self):
        contenu = self.sujet.titre if self.sujet else self.message.contenu[:50] if self.message else 'Inconnu'
        return f"Signalement de {self.signaleur.username} - {contenu[:30]}"

    def clean(self):
        if (self.sujet and self.message) or (not self.sujet and not self.message):
            from django.core.exceptions import ValidationError
            raise ValidationError("Sélectionnez soit un sujet, soit un message.")

    def get_contenu_cible(self):
        from django.urls import reverse
        if self.sujet:
            return {
                'type': 'sujet',
                'titre': self.sujet.titre,
                'contenu': self.sujet.contenu,
                'auteur': self.sujet.auteur,
                'url': reverse('forum_adulte_sujet', args=[self.sujet.id])
            }
        elif self.message:
            return {
                'type': 'message',
                'contenu': self.message.contenu,
                'auteur': self.message.auteur,
                'sujet': self.message.sujet.titre,
                'url': reverse('forum_adulte_sujet', args=[self.message.sujet.id]) + f'#message-{self.message.id}'
            }
        return None


class ForumAdulteNotification(models.Model):
    """Notifications pour les utilisateurs"""
    TYPES = [
        ('reponse', 'Réponse à un sujet'),
        ('mention', 'Mention'),
        ('solution', 'Solution marquée'),
        ('vote', 'Vote reçu'),
        ('signalement', 'Signalement traité'),
    ]

    destinataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='notifications_adulte')
    expediteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='notifications_envoyees_adulte', null=True, blank=True)
    type_notification = models.CharField(max_length=20, choices=TYPES)
    message = models.TextField()
    lien = models.CharField(max_length=255)
    est_lue = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name_plural = "Notifications forum adulte"

    def __str__(self):
        return f"Notification pour {self.destinataire.username} - {self.type_notification}"


# ============================================================
# BADGES ET RÉCOMPENSES
# ============================================================

class ForumBadge(models.Model):
    """Badges d'expertise pour le forum"""
    NIVELLES = [
        ('bronze', '🥉 Bronze'),
        ('argent', '🥈 Argent'),
        ('or', '🥇 Or'),
        ('platine', '💎 Platine'),
    ]

    nom = models.CharField(max_length=50)
    description = models.TextField()
    emoji = models.CharField(max_length=10)
    niveau = models.CharField(max_length=20, choices=NIVELLES, default='bronze')
    conditions = models.TextField(help_text="Conditions pour obtenir le badge")
    est_automatique = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.emoji} {self.nom} ({self.get_niveau_display()})"


class ForumBadgeUtilisateur(models.Model):
    """Badges obtenus par un utilisateur"""
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges_forum')
    badge = models.ForeignKey(ForumBadge, on_delete=models.CASCADE)
    date_obtention = models.DateTimeField(auto_now_add=True)
    est_affiche = models.BooleanField(default=True)

    class Meta:
        unique_together = ['utilisateur', 'badge']

    def __str__(self):
        return f"{self.utilisateur.username} → {self.badge.nom}"


# ============================================================
# MODÈLES DE MODÉRATION
# ============================================================

class ModerateurForum(models.Model):
    """Modérateurs du forum adulte"""
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                       related_name='moderateur_forum')
    est_actif = models.BooleanField(default=True)
    date_nomination = models.DateTimeField(auto_now_add=True)
    permissions = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Modérateur : {self.utilisateur.username}"


class SanctionUtilisateur(models.Model):
    """Traçage des sanctions"""
    TYPES = [
        ('avertissement', '⚠️ Avertissement'),
        ('suspension', '⏸️ Suspension'),
        ('bannissement', '🚫 Bannissement'),
    ]

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sanctions')
    moderateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sanctions_donnees')
    type_sanction = models.CharField(max_length=20, choices=TYPES)
    raison = models.TextField()
    signalement = models.ForeignKey(ForumAdulteSignalement, on_delete=models.SET_NULL, null=True, blank=True)
    duree = models.DurationField(null=True, blank=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.utilisateur.username} → {self.get_type_sanction_display()} par {self.moderateur.username}"


class ConseilPersonnalise(models.Model):
    """Conseils personnalisés pour une variété"""

    variete = models.OneToOneField('Variete', on_delete=models.CASCADE, related_name='conseils')

    # Conseils structurés
    conseils_arrosage = models.JSONField(default=list, blank=True)
    conseils_plantation = models.JSONField(default=list, blank=True)
    conseils_fertilisation = models.JSONField(default=list, blank=True)
    conseils_protection = models.JSONField(default=list, blank=True)
    conseils_generaux = models.JSONField(default=list, blank=True)
    conseils_saison = models.JSONField(default=list, blank=True)

    # Métadonnées
    saison = models.CharField(max_length=20, blank=True)
    climat = models.CharField(max_length=50, blank=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conseil personnalisé"
        verbose_name_plural = "Conseils personnalisés"

    def __str__(self):
        return f"Conseils pour {self.variete.nom}"


class ConnexionLog(models.Model):
    """Log des connexions pour détecter les abus de partage de compte"""

    utilisateur = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='connexions_log'
    )
    ip = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    pays = models.CharField(max_length=100, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    device_id = models.CharField(max_length=200, blank=True, null=True)
    date_connexion = models.DateTimeField(auto_now_add=True)
    est_suspect = models.BooleanField(default=False)
    raison_suspicion = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-date_connexion']
        verbose_name = "Log de connexion"
        verbose_name_plural = "Logs de connexion"
        indexes = [
            models.Index(fields=['utilisateur', '-date_connexion']),
            models.Index(fields=['ip']),
        ]

    def __str__(self):
        return f"{self.utilisateur.username} - {self.ip} - {self.date_connexion.strftime('%d/%m/%Y %H:%M')}"


import secrets
from django.utils import timezone
from datetime import timedelta


class AutorisationAchatMineur(models.Model):
    """
    Demande d'autorisation parentale pour qu'un mineur
    puisse souscrire un abonnement payant.
    """
    STATUT_CHOICES = [
        ('en_attente', '⏳ En attente'),
        ('validee', '✅ Validée'),
        ('refusee', '❌ Refusée'),
        ('expiree', '⌛ Expirée'),
    ]

    utilisateur = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='autorisations_achat',
        verbose_name="Mineur"
    )
    plan_souhaite = models.ForeignKey(
        'PlanTarification',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Plan souhaité"
    )
    frequence = models.CharField(
        max_length=20,
        default='MENSUEL',
        choices=[('MENSUEL', 'Mensuel'), ('ANNUEL', 'Annuel')],
        verbose_name="Fréquence"
    )

    # Informations du parent
    parent_nom = models.CharField(max_length=100, blank=True)
    parent_prenom = models.CharField(max_length=100, blank=True)
    parent_email = models.EmailField(blank=True)
    parent_telephone = models.CharField(max_length=20, blank=True)

    # Consentement
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    cgu_acceptees = models.BooleanField(default=False)
    autorisation_donnee = models.BooleanField(default=False)
    date_demande = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(null=True, blank=True)
    date_expiration = models.DateTimeField(null=True, blank=True)

    # Token de validation
    token_validation = models.CharField(max_length=64, unique=True, blank=True)

    # IP et user-agent du parent (preuve légale)
    ip_validation = models.GenericIPAddressField(null=True, blank=True)
    user_agent_validation = models.TextField(blank=True)

    class Meta:
        verbose_name = "Autorisation d'achat (mineur)"
        verbose_name_plural = "Autorisations d'achat (mineurs)"
        ordering = ['-date_demande']

    def save(self, *args, **kwargs):
        if not self.token_validation:
            self.token_validation = secrets.token_urlsafe(48)
        if not self.date_expiration:
            self.date_expiration = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def est_expiree(self):
        return self.date_expiration and timezone.now() > self.date_expiration

    def est_utilisable(self):
        """Retourne True si l'autorisation peut servir à payer"""
        return (
            self.statut == 'validee'
            and not self.est_expiree()
        )

    def __str__(self):
        return f"Autorisation {self.utilisateur.username} → {self.plan_souhaite.nom if self.plan_souhaite else '?'}"


class ConseilsFamille(models.Model):
    """
    Conseils génériques par famille botanique.
    Chaque culture peut être liée à une famille pour hériter de ses conseils.
    """
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la famille"
    )
    emoji = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Emoji représentatif"
    )

    # ✅ Températures
    temperature_min = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température minimale (°C)",
        help_text="Température sous laquelle la plante gèle ou souffre"
    )
    temperature_optimale_min = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température optimale minimum (°C)"
    )
    temperature_optimale_max = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température optimale maximum (°C)"
    )
    temperature_max = models.IntegerField(
        null=True, blank=True,
        verbose_name="Température maximale (°C)",
        help_text="Température au-dessus de laquelle la plante souffre"
    )

    # ✅ Durée de culture
    duree_culture_min_jours = models.IntegerField(
        null=True, blank=True,
        verbose_name="Durée minimale (jours)"
    )
    duree_culture_max_jours = models.IntegerField(
        null=True, blank=True,
        verbose_name="Durée maximale (jours)"
    )

    # ✅ Méthode de plantation
    methode_plantation = models.CharField(
        max_length=50, blank=True,
        choices=[
            ('graine', '🌰 Graine'),
            ('rhizome', '🫚 Rhizome'),
            ('bulbe', '🧄 Bulbe'),
            ('tubercule', '🥔 Tubercule'),
            ('plant', '🌱 Plant / Semis'),
            ('bouture', '🌿 Bouture'),
            ('greffe', '🌳 Greffe'),
            ('division', '🌾 Division de touffe'),
        ],
        verbose_name="Méthode de plantation"
    )

    # ✅ Hivernage
    hivernage = models.CharField(
        max_length=50, blank=True,
        choices=[
            ('plein_air', '🌳 Plein air (rustique)'),
            ('serre', '🏠 Serre ou abri'),
            ('interieur', '🏡 Intérieur obligatoire'),
            ('climat_doux', '🌞 Climat doux uniquement'),
        ],
        verbose_name="Hivernage"
    )

    # ✅ Conseils détaillés
    conseils_climat = models.TextField(
        blank=True,
        verbose_name="Conseils climat",
        help_text="Conseils liés au climat (tropical, tempéré, etc.)"
    )
    conseils_plantation = models.TextField(
        blank=True,
        verbose_name="Conseils plantation",
        help_text="Quand et comment planter"
    )
    conseils_arrosage = models.TextField(
        blank=True,
        verbose_name="Conseils arrosage",
        help_text="Fréquence et méthode d'arrosage"
    )
    conseils_fertilisation = models.TextField(
        blank=True,
        verbose_name="Conseils fertilisation",
        help_text="Engrais et amendements"
    )
    conseils_protection = models.TextField(
        blank=True,
        verbose_name="Conseils protection",
        help_text="Ravageurs, maladies, protection hivernale"
    )
    conseils_recolte = models.TextField(
        blank=True,
        verbose_name="Conseils récolte",
        help_text="Quand et comment récolter"
    )
    conseils_conservation = models.TextField(
        blank=True,
        verbose_name="Conseils conservation",
        help_text="Comment conserver après récolte"
    )

    class Meta:
        verbose_name = "Conseils par famille"
        verbose_name_plural = "Conseils par famille"
        ordering = ['nom']

    def __str__(self):
        return f"{self.emoji} {self.nom}"


class ConseilsTypeCulture(models.Model):
    """
    Conseils agronomiques par grand type de plante (arbre, baie, légume...).
    Remplace l'héritage de la famille botanique pour les conseils de culture.
    """
    TYPE_CHOICES = [
        ('arbre_fruitier', '🌳 Arbre fruitier'),
        ('arbuste_fruitier', '🌿 Arbuste fruitier (baies)'),
        ('legume_feuille', '🥬 Légume-feuille'),
        ('legume_racine', '🥕 Légume-racine'),
        ('legume_fruit', '🍅 Légume-fruit'),
        ('legume_bulbe', '🧅 Légume-bulbe'),
        ('aromatique', '🌿 Aromatique'),
        ('cereale', '🌾 Céréale'),
        ('fleur', '🌸 Fleur'),
    ]

    type_culture = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        unique=True,
        verbose_name="Type de culture"
    )
    emoji = models.CharField(max_length=10, default='🌱')

    # Les mêmes champs que ConseilsFamille
    temperature_min = models.IntegerField(null=True, blank=True)
    temperature_optimale_min = models.IntegerField(null=True, blank=True)
    temperature_optimale_max = models.IntegerField(null=True, blank=True)
    temperature_max = models.IntegerField(null=True, blank=True)

    duree_culture_min_jours = models.IntegerField(null=True, blank=True)
    duree_culture_max_jours = models.IntegerField(null=True, blank=True)

    methode_plantation = models.CharField(max_length=50, blank=True)
    hivernage = models.CharField(max_length=50, blank=True)

    conseils_climat = models.TextField(blank=True)
    conseils_plantation = models.TextField(blank=True)
    conseils_arrosage = models.TextField(blank=True)
    conseils_fertilisation = models.TextField(blank=True)
    conseils_protection = models.TextField(blank=True)
    conseils_recolte = models.TextField(blank=True)
    conseils_conservation = models.TextField(blank=True)

    class Meta:
        verbose_name = "Conseils par type de culture"
        verbose_name_plural = "Conseils par type de culture"

    def __str__(self):
        return f"{self.emoji} {self.get_type_culture_display()}"


# ============================================================
# DIGEST QUOTIDIEN DES ALERTES MÉTÉO
# ============================================================

class DigestMeteo(models.Model):
    """
    Résumé quotidien des alertes météo à envoyer par email.

    Permet de grouper plusieurs alertes météo en 1 seul email par
    utilisateur/jour, au lieu d'envoyer 1 email par alerte.

    Les alertes CRITIQUES (gel sévère, canicule extrême, vent violent)
    sont envoyées immédiatement ET ajoutées au digest pour traçabilité.
    """
    utilisateur = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='digests_meteo'
    )
    date = models.DateField(auto_now_add=True)

    # Liste des alertes météo du jour (dicts)
    # Format : [{'type': 'gel', 'culture': 'Tomate', 'message': '...', 'est_critique': False}, ...]
    alertes = models.JSONField(default=list, blank=True)

    # Nombre d'alertes critiques envoyées immédiatement (pour info)
    nb_critiques_envoyees = models.IntegerField(default=0)

    # État d'envoi du digest
    envoye = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Digest météo journalier"
        verbose_name_plural = "Digests météo journaliers"
        unique_together = ('utilisateur', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"Digest météo {self.utilisateur.username} - {self.date} ({len(self.alertes)} alertes)"

    @property
    def total_alertes(self):
        """Nombre total d'alertes dans ce digest."""
        return len(self.alertes)

    @property
    def est_vide(self):
        """Le digest ne contient aucune alerte."""
        return len(self.alertes) == 0

    @property
    def a_des_critiques(self):
        """Le digest contient au moins une alerte critique."""
        return any(a.get('est_critique', False) for a in self.alertes)