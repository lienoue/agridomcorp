from django.contrib import admin
from .models import (
    CustomUser, Vegetable, Fruit, GeometricFigure,
    Classe, Eleve, Badge, Mission, ProgressionJunior,
    MissionQuotidienne, MissionEleve,
    NotificationEnseignant, AlerteSemis,
    PlanTarification, Abonnement, ConsentementRGPD, Facture,
    Culture, CalendrierSemis, Parcelle, QuestionQuiz, PhotoJardin, CommentairePhoto, SignalementForum, ConseilsFamille, TauxChange
)



# ============================================
# ADMIN FRUIT
# ============================================
class FruitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'couleur', 'provenance', 'prix', 'saison', 'recolte', 'famille')
    list_filter = ('saison', 'couleur', 'provenance', 'famille')
    search_fields = ('nom', 'provenance')

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'couleur', 'genre', 'provenance', 'prix')
        }),
        ('Culture', {
            'fields': ('saison', 'plantation', 'recolte', 'varietes')
        }),
        ('Semis', {
            'fields': ('semis_interieur', 'semis_exterieur', 'jours_levée', 'jours_recolte',
                       'temperature_min', 'profondeur_semis', 'espacement')
        }),
        ('Pollinisation', {
            'fields': ('pollinisation_type', 'besoin_pollinisateur', 'pollinisateurs_conseilles',
                       'distance_pollinisation', 'periode_floraison', 'conseils_pollinisation')
        }),
        ('Conseils', {
            'fields': ('conseils_preparation_sol', 'conseils_apres_recolte',
                       'rotation_conseillee', 'rotation_deconseillee')
        }),
        ('🌱 Conseils enrichis', {
            'fields': (
                'famille',
                'temperature_optimale_min',
                'temperature_optimale_max',
                'duree_culture_min_jours',
                'duree_culture_max_jours',
                'methode_plantation',
                'hivernage',
                'conseils_climat',
                'conseils_plantation',
                'conseils_arrosage',
                'conseils_fertilisation',
                'conseils_protection',
                'conseils_recolte',
                'conseils_conservation',
            ),
            'classes': ('collapse',),
        }),
        ('Autres', {
            'fields': ('bourse', 'AOP', 'IGP', 'url')
        }),
    )


# ============================================
# ADMIN VEGETABLE
# ============================================
class VegetableAdmin(admin.ModelAdmin):
    list_display = ('nom', 'couleur', 'provenance', 'prix', 'saison', 'recolte', 'famille')
    list_filter = ('saison', 'couleur', 'provenance', 'famille')
    search_fields = ('nom', 'provenance')

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'couleur', 'genre', 'provenance', 'prix')
        }),
        ('Culture', {
            'fields': ('saison', 'plantation', 'recolte', 'varietes')
        }),
        ('Semis', {
            'fields': ('semis_interieur', 'semis_exterieur', 'jours_levée', 'jours_recolte',
                       'temperature_min', 'profondeur_semis', 'espacement')
        }),
        ('Pollinisation', {
            'fields': ('pollinisation_type', 'besoin_pollinisateur', 'pollinisateurs_conseilles',
                       'distance_pollinisation', 'periode_floraison', 'conseils_pollinisation')
        }),
        ('Conseils', {
            'fields': ('conseils_preparation_sol', 'conseils_apres_recolte',
                       'rotation_conseillee', 'rotation_deconseillee')
        }),
        ('🌱 Conseils enrichis', {
            'fields': (
                'famille',
                'temperature_optimale_min',
                'temperature_optimale_max',
                'duree_culture_min_jours',
                'duree_culture_max_jours',
                'methode_plantation',
                'hivernage',
                'conseils_climat',
                'conseils_plantation',
                'conseils_arrosage',
                'conseils_fertilisation',
                'conseils_protection',
                'conseils_recolte',
                'conseils_conservation',
            ),
            'classes': ('collapse',),
        }),
        ('Autres', {
            'fields': ('bourse', 'AOP', 'IGP', 'url')
        }),
    )


# ============================================
# ADMIN CULTURE
# ============================================
class CultureAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_culture', 'emoji', 'famille', 'besoin_eau_litres_jour', 'jours_pousse')
    list_filter = ('type_culture', 'saison_plantation', 'famille')
    search_fields = ('nom',)

    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'type_culture', 'emoji', 'besoin_eau_litres_jour', 'jours_pousse')
        }),
        ('Culture', {
            'fields': ('saison_plantation', 'conseils')
        }),
        ('Seuils météo', {
            'fields': ('temperature_mingel', 'temperature_max_canicule', 'precipitation_max', 'vent_max')
        }),
        ('🌱 Conseils enrichis', {
            'fields': (
                'famille',
                'temperature_min',
                'temperature_optimale_min',
                'temperature_optimale_max',
                'temperature_max',
                'duree_culture_min_jours',
                'duree_culture_max_jours',
                'methode_plantation',
                'hivernage',
                'conseils_climat',
                'conseils_plantation',
                'conseils_arrosage',
                'conseils_fertilisation',
                'conseils_protection',
                'conseils_recolte',
                'conseils_conservation',
            ),
            'classes': ('collapse',),
        }),
    )


# ============================================
# ADMIN POUR CALENDRIER SEMIS
# ============================================

class CalendrierSemisAdmin(admin.ModelAdmin):
    list_display = ('culture', 'region', 'mois_debut_semis', 'mois_fin_semis', 'mois_debut_recolte')
    list_filter = ('region', 'culture')
    search_fields = ('culture', 'region')


# ============================================
# ENREGISTREMENT DES MODÈLES
# ============================================

admin.site.register(Fruit, FruitAdmin)
admin.site.register(Vegetable, VegetableAdmin)
admin.site.register(Culture, CultureAdmin)
admin.site.register(CalendrierSemis, CalendrierSemisAdmin)

# ============================================
# AUTRES MODÈLES (conservés comme avant)
# ============================================

admin.site.register(CustomUser)
admin.site.register(GeometricFigure)
admin.site.register(Classe)
admin.site.register(Eleve)
admin.site.register(Badge)
admin.site.register(Mission)
admin.site.register(ProgressionJunior)
admin.site.register(MissionQuotidienne)
admin.site.register(MissionEleve)
admin.site.register(NotificationEnseignant)
admin.site.register(AlerteSemis)


# ============================================
# PLANS TARIFAIRES, ABONNEMENTS, RGPD, FACTURES
# ============================================

@admin.register(PlanTarification)
class PlanTarificationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix_mensuel', 'prix_annuel', 'max_parcelles', 'actif')
    list_filter = ('actif',)
    search_fields = ('nom',)
    ordering = ('prix_mensuel',)


@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'plan', 'statut', 'frequence', 'date_debut', 'est_actif')
    list_filter = ('statut', 'plan', 'frequence', 'est_groupe_scolaire')
    search_fields = ('utilisateur__email', 'utilisateur__username')
    date_hierarchy = 'date_debut'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ConsentementRGPD)
class ConsentementRGPDAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'date_consentement', 'est_mineur', 'cgu_acceptees')
    list_filter = ('est_mineur', 'cgu_acceptees', 'date_consentement')
    search_fields = ('utilisateur__email', 'representant_legal_email')
    date_hierarchy = 'date_consentement'


@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'montant_ttc', 'statut', 'date_emission', 'date_paiement')
    list_filter = ('statut', 'date_emission')
    search_fields = ('utilisateur__email', 'stripe_invoice_id')
    date_hierarchy = 'date_emission'
    readonly_fields = ('date_emission',)


@admin.register(Parcelle)
class ParcelleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'utilisateur', 'type_sol', 'surface_m2', 'est_active')
    list_filter = ('type_sol', 'est_active')
    search_fields = ('nom', 'utilisateur__username')

# ============================================
# QUIZ
# ============================================

@admin.register(QuestionQuiz)
class QuestionQuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'bonne_reponse', 'categorie', 'difficulte')
    list_filter = ('categorie', 'difficulte')
    search_fields = ('question',)
    ordering = ('question',)


@admin.register(PhotoJardin)
class PhotoJardinAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_creation', 'est_validee', 'est_publiee')
    list_filter = ('est_validee', 'est_publiee', 'date_creation')
    search_fields = ('titre', 'description', 'auteur__username')
    readonly_fields = ('date_creation',)

@admin.register(CommentairePhoto)
class CommentairePhotoAdmin(admin.ModelAdmin):
    list_display = ('photo', 'auteur', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('contenu', 'auteur__username')


@admin.register(SignalementForum)
class SignalementForumAdmin(admin.ModelAdmin):
    list_display = ('sujet', 'message', 'signaleur', 'date_signalement', 'statut')
    list_filter = ('statut', 'date_signalement')
    search_fields = ('raison', 'signaleur__username')
    readonly_fields = ('date_signalement',)





@admin.register(ConseilsFamille)
class ConseilsFamilleAdmin(admin.ModelAdmin):
    list_display = ('emoji', 'nom', 'temperature_min', 'temperature_max', 'duree_culture_min_jours', 'duree_culture_max_jours')
    search_fields = ('nom',)
    list_filter = ('methode_plantation', 'hivernage')
    fieldsets = (
        ('Identité', {
            'fields': ('nom', 'emoji')
        }),
        ('Températures', {
            'fields': (
                'temperature_min',
                'temperature_optimale_min',
                'temperature_optimale_max',
                'temperature_max',
            )
        }),
        ('Culture', {
            'fields': (
                'duree_culture_min_jours',
                'duree_culture_max_jours',
                'methode_plantation',
                'hivernage',
            )
        }),
        ('Conseils détaillés', {
            'fields': (
                'conseils_climat',
                'conseils_plantation',
                'conseils_arrosage',
                'conseils_fertilisation',
                'conseils_protection',
                'conseils_recolte',
                'conseils_conservation',
            )
        }),
    )

from .models import RendementCulture


@admin.register(RendementCulture)
class RendementCultureAdmin(admin.ModelAdmin):
    list_display = ('culture_nom', 'rendement_kg_par_plant', 'region_climatique', 'source', 'est_actif', 'date_modification')
    list_filter = ('region_climatique', 'source', 'est_actif')
    search_fields = ('culture_nom', 'notes')
    list_editable = ('rendement_kg_par_plant', 'est_actif') # édition inline !
    ordering = ('culture_nom',)
    readonly_fields = ('date_creation', 'date_modification')

    fieldsets = (
        ('Culture', {'fields': ('culture_nom', 'culture')}),
        ('Rendement', {'fields': ('rendement_kg_par_plant', 'region_climatique')}),
        ('Métadonnées', {'fields': ('source', 'notes', 'est_actif')}),
        ('Historique', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TauxChange)
class TauxChangeAdmin(admin.ModelAdmin):
    list_display = ('devise', 'taux_vs_eur', 'symbole', 'position_symbole', 'source', 'date_maj', 'est_actif')
    list_filter = ('source', 'est_actif')
    list_editable = ('taux_vs_eur', 'est_actif')
    ordering = ('devise',)
    readonly_fields = ('date_maj',)