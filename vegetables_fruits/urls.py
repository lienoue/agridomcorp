from django.urls import path, include
from django.conf import settings
from . import views

app_name = 'vegetables_fruits'

urlpatterns = [
    # =========================================================
    # ✅ NOUVELLES PAGES FUSIONNÉES
    # =========================================================

    # 1. Page Cultures (3 onglets)
    path('cultures/', views.cultures, name='cultures'),
    path('api/tab/cultures/<str:tab_name>/', views.cultures_tabs, name='cultures_tabs'),

    # 2. Page Guide des cultures (4 onglets)
    path('guide-cultures/', views.guide_cultures, name='guide_cultures'),
    path('api/tab/guide/<str:tab_name>/', views.guide_tabs, name='guide_tabs'),

    # 3. Page Écologie (2 onglets)
    path('ecologie/', views.ecologie, name='ecologie'),
    path('api/tab/ecologie/<str:tab_name>/', views.ecologie_tabs, name='ecologie_tabs'),

    # 4. Page Alertes (3 onglets)
    path('alertes/', views.alertes, name='alertes'),
    path('api/tab/alertes/<str:tab_name>/', views.alertes_tabs, name='alertes_tabs'),
    path('ignorer-alerte-semis/<int:alerte_id>/', views.ignorer_alerte_semis, name='ignorer_alerte_semis'),
    path('ignorer-alerte-traitement/<int:alerte_id>/', views.ignorer_alerte_traitement, name='ignorer_alerte_traitement'),
    path('mes-alertes-semis/', views.mes_alertes, name='mes_alertes'),

    # =========================================================
    # AUTRES ROUTES
    # =========================================================

    # Accueil
    path('', views.index, name='index'),

    # Authentification
    path('login/', views.connexion, name='login'),
    path('logout/', views.deconnexion, name='logout'),
    path('signup/', views.creation_compte, name='signup'),
    path('offline/', views.offline, name='offline'),

    # URLS de réinitialisation de mot de passe
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # Profil
    path('profile/', views.profile, name='profile'),
    path('mes-donnees/', views.exporter_mes_donnees, name='exporter_mes_donnees'),
    path('supprimer-compte', views.supprimer_mon_compte, name='supprimer_mon_compte'),
    path('dashboard/', views.dashboard_particulier, name='dashboard_particulier'),
    path('dashboard-eleve/', views.dashboard_eleve, name='dashboard_eleve'),
    path('dashboard-junior/', views.dashboard_junior, name='dashboard_junior'),
    path('planifier-culture/<int:figure_id>/', views.planifier_culture, name='planifier_culture'),


    # Parcelles
    path('view/', views.view_figure, name='view_figure'),
    path('draw/', views.draw_figure, name='draw_figure'),
    path('figure-detail/<int:figure_id>/', views.figure_detail, name='figure_detail'),
    path('edit-figure/<int:figure_id>/', views.edit_figure, name='edit_figure'),
    path('delete-figure/<int:figure_id>/', views.delete_figure, name='delete_figure'),
    path('save-figure/', views.save_figure, name='save_figure'),
    path('save-terrain-figure/', views.save_terrain_figure, name='save_terrain_figure'),
    path('limite-parcelles/', views.limite_parcelles, name='limite_parcelles'),

    # Cultures
    path('recolter-culture/', views.recolter_culture, name='recolter_culture'),
    path('ajouter-chronologie/', views.ajouter_chronologie, name='ajouter_chronologie'),
    path('besoins-eau/', views.besoins_eau, name='besoins_eau'),
    path('ajuster-besoins-annuels/', views.ajuster_besoins_annuels, name='ajuster_besoins_annuels'),
    path('autosuffisance/', views.autosuffisance, name='autosuffisance'),

    # Plan irrigation
    path('plan-irrigation/', views.plan_irrigation, name='plan_irrigation'),
    path('export-plan-irrigation-pdf/', views.export_plan_irrigation_pdf, name='export_plan_irrigation_pdf'),
    path('creer-rappel-arrosage/<int:parcelle_id>/', views.creer_rappel_arrosage, name='creer_rappel_arrosage'),

    # Bilan carbone
    path('bilan-carbone/', views.bilan_carbone, name='bilan_carbone'),
    path('export-bilan-carbone-pdf/', views.export_bilan_carbone_pdf, name='export_bilan_carbone_pdf'),
    path('bilan-carbone-eleve/<int:eleve_id>/', views.bilan_carbone_eleve, name='bilan_carbone_eleve'),

    # Conseiller Sol
    path('conseiller-sol/', views.conseiller_sol, name='conseiller_sol'),

    # Plan fertilisation
    path('plan-fertilisation/', views.plan_fertilisation, name='plan_fertilisation'),

    # Gestion maladies
    path('gestion-maladies/', views.gestion_maladies, name='gestion_maladies'),

    # Rotation cultures
    path('rotation-cultures/', views.rotation_cultures, name='rotation_cultures'),
    path('rotation-cultures/<int:figure_id>/', views.rotation_cultures, name='rotation_cultures'),

    # Compagnonnage
    path('companion-planting/', views.companion_planting, name='companion_planting'),
    path('companion-planting/<int:figure_id>/', views.companion_planting, name='companion_planting_figure'),

    # Suggestions
    path('suggestions-personnalisees/', views.suggestions_personnalisees, name='suggestions_personnalisees'),
    path('placer-culture/<int:figure_id>/', views.placer_culture, name='placer_culture'),
    path('choisir-parcelle/', views.choisir_parcelle, name='choisir_parcelle'),

    # Calendrier
    path('calendrier-semis/', views.calendrier_semis, name='calendrier_semis'),
    path('mes-semis/', views.mes_semis, name='mes_semis'),
    path('planification-semis/', views.planification_semis, name='planification_semis'),

    # Fleurs
    path('ajouter-fleur/<int:figure_id>/', views.ajouter_fleur, name='ajouter_fleur'),

    # Journal
    path('journal/', views.journal_liste, name='journal_liste'),
    path('journal/ajouter/<int:figure_id>', views.journal_ajouter, name='journal_ajouter'),
    path('journal/ajouter/', views.journal_ajouter, name='journal_ajouter_parcelle'),
    path('journal/detail/<int:note_id>/', views.journal_detail, name='journal_detail'),
    path('journal/modifier/<int:note_id>/', views.journal_modifier, name='journal_modifier'),
    path('journal/supprimer/<int:note_id>/', views.journal_supprimer, name='journal_supprimer'),

    # Alertes
    path('alertes-meteo/', views.mes_alertes_meteo, name='mes_alertes_meteo'),
    path('alertes-meteo-avancees/', views.alertes_meteo_avancees, name='alertes_meteo_avancees'),
    path('alertes-traitements/', views.alertes_traitements, name='alertes_traitements'),
    path('traiter-alerte/<int:alerte_id>/', views.traiter_alerte, name='traiter_alerte'),
    path('restaurer-alerte-semis/<int:alerte_id>/', views.restaurer_alerte_semis, name='restaurer_alerte_semis'),
    path('verifier-compatibilite/', views.verifier_compatibilite_plantation, name='verifier_compatibilite_plantation'),

    # 🌍 Écologie & Climat
    path('ecologie/', views.ecologie, name='ecologie'),

    # 🌤️ Dashboard Climat (Premium/Enseignant)
    path('dashboard-climat/', views.dashboard_climat, name='dashboard_climat'),

    # 🌡️ Prévisions météo 5 jours (Premium/Enseignant)
    path('previsions-meteo/', views.previsions_meteo, name='previsions_meteo'),

    # Planification alertes
    path('planifier-alertes/', views.planifier_alertes, name='planifier_alertes'),
    path('mes-rappels/', views.mes_rappels, name='mes_rappels'),
    path('supprimer-rappel/<int:rappel_id>/', views.supprimer_rappel, name='supprimer_rappel'),
    path('toggle-rappel/<int:rappel_id>/', views.toggle_rappel, name='toggle_rappel'),

    # Calendrier utilisateur
    path('api/enregistrer-calendrier/', views.api_enregistrer_calendrier, name='api_enregistrer_calendrier'),
    path('api/supprimer-semis/<int:semis_id>/', views.api_supprimer_semis, name='api_supprimer_semis'),

    # Tarification
    path('tarification/', views.tarification, name='tarification'),
    path('abonnement/succes/', views.abonnement_succes, name='abonnement_succes'),
    path('abonnement/stripe-portal/', views.stripe_portal, name='stripe_portal'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('autorisation-achat/demande/', views.demander_autorisation_achat, name='demander_autorisation_achat'),
    path('autorisation-achat/valider/<str:token>/', views.valider_autorisation_achat, name='valider_autorisation_achat'),
    path('abonnement/reactiver/', views.reactiver_abonnement, name='reactiver_abonnement'),

    # Gamification
    path('quiz/', views.quiz, name='quiz'),
    path('quiz-resultat/<int:quiz_id>/', views.quiz_resultat, name='quiz_resultat'),
    path('missions-hebdomadaires/', views.missions_hebdomadaires, name='missions_hebdomadaires'),
    path('arbre-competences/', views.arbre_competences, name='arbre_competences'),
    path('progression-junior/', views.progression_junior, name='progression_junior'),
    path('toggle-mode-junior/', views.basculer_mode_junior, name='basculer_mode_junior'),
    path('toggle-mode-junior-eleve/<int:eleve_id>/', views.toggle_mode_junior_eleve, name='toggle_mode_junior_eleve'),
    path('supprimer-eleve/<int:eleve_id>/', views.supprimer_eleve, name='supprimer_eleve'),

    # Forum enfant
    path('forum/', views.forum_index, name='forum_index'),
    path('forum/categorie/<int:categorie_id>/', views.forum_categorie, name='forum_categorie'),
    path('forum/sujet/<int:sujet_id>/', views.forum_sujet, name='forum_sujet'),
    path('forum/nouveau-sujet/<int:categorie_id>/', views.forum_nouveau_sujet, name='forum_nouveau_sujet'),
    path('forum/repondre/<int:sujet_id>/', views.forum_repondre, name='forum_repondre'),
    path('forum/moderation/', views.forum_moderation, name='forum_moderation'),
    path('forum/epingler/<int:sujet_id>/', views.forum_epingler, name='forum_epingler'),
    path('forum/fermer/<int:sujet_id>/', views.forum_fermer, name='forum_fermer'),
    path('forum/supprimer-sujet/<int:sujet_id>/', views.forum_supprimer_sujet, name='forum_supprimer_sujet'),
    path('forum/supprimer-message/<int:message_id>/', views.forum_supprimer_message, name='forum_supprimer_message'),
    path('forum/signalement/', views.forum_signalement, name='forum_signalement'),
    path('forum/signalement-traiter/<int:signalement_id>/', views.forum_signalement_traiter,
         name='forum_signalement_traiter'),
    path('forum/marquer-signalements-lus/', views.marquer_signalements_lus, name='marquer_signalements_lus'),
    path('forum/signalement-detail/<int:signalement_id>/', views.forum_signalement_detail, name='forum_signalement_detail'),

    # ============================================================
    # FORUM ADULTE
    # ============================================================

    # 📌 Index du forum
    path('forum-adulte/', views.forum_adulte_index, name='forum_adulte_index'),

    # 📌 Catégories
    path('forum-adulte/categorie/<int:categorie_id>/', views.forum_adulte_categorie, name='forum_adulte_categorie'),

    # 📌 Sujets
    path('forum-adulte/sujet/<int:sujet_id>/', views.forum_adulte_sujet, name='forum_adulte_sujet'),
    path('forum-adulte/nouveau-sujet/', views.forum_adulte_nouveau_sujet, name='forum_adulte_nouveau_sujet'),

    # 📌 Actions sur les messages (Premium)
    path('forum-adulte/voter/<int:message_id>/', views.forum_adulte_voter, name='forum_adulte_voter'),
    path('forum-adulte/solution/<int:message_id>/', views.forum_adulte_marquer_solution,
         name='forum_adulte_marquer_solution'),

    # 📌 Notifications
    path('forum-adulte/notifications/', views.forum_adulte_notifications, name='forum_adulte_notifications'),
    path('forum-adulte/notifications/lue/<int:notification_id>/', views.forum_adulte_notification_lue,
         name='forum_adulte_notification_lue'),
    path('forum-adulte/notifications/toutes-lues/', views.forum_adulte_notifications_toutes_lues,
         name='forum_adulte_notifications_toutes_lues'),

    # 📌 Signalements (utilisateurs)
    path('forum-adulte/signalement/', views.forum_adulte_signalement, name='forum_adulte_signalement'),

    # 📌 Modération (modérateurs uniquement)
    path('forum-adulte/moderateur/signalements/', views.forum_adulte_moderation_signalements,
         name='forum_adulte_moderation_signalements'),
    path('forum-adulte/moderateur/signalement/<int:signalement_id>/', views.forum_adulte_moderation_signalement_detail,
         name='forum_adulte_moderation_signalement_detail'),

    path('forum-adulte/recherche/', views.forum_adulte_recherche, name='forum_adulte_recherche'),
    path('forum-adulte/profil/<int:user_id>/', views.forum_adulte_profil, name='forum_adulte_profil'),
    path('forum-adulte/mes-sujets/', views.forum_adulte_mes_sujets, name='forum_adulte_mes_sujets'),
    path('forum-adulte/mes-messages/', views.forum_adulte_mes_messages, name='forum_adulte_mes_messages'),
    path('forum-adulte/moderateur/statistiques/', views.forum_adulte_moderation_statistiques, name='forum_adulte_moderation_statistiques'),
    path('forum-adulte/moderateur/sanctions/', views.forum_adulte_moderation_sanctions, name='forum_adulte_moderation_sanctions'),


    # Galerie
    path('galerie/', views.galerie_index, name='galerie_index'),
    path('galerie/photos/', views.galerie_photos, name='galerie_photos'),
    path('galerie/upload/', views.galerie_upload, name='galerie_upload'),
    path('galerie/photo/<int:photo_id>/', views.galerie_photo_detail, name='galerie_photo_detail'),
    path('galerie/liker/<int:photo_id>/', views.galerie_liker, name='galerie_liker'),
    path('galerie/moderation/', views.galerie_moderation, name='galerie_moderation'),
    path('galerie/valider/<int:photo_id>/', views.galerie_valider, name='galerie_valider'),
    path('galerie/supprimer/<int:photo_id>/', views.galerie_supprimer, name='galerie_supprimer'),

    # Classements
    path('classement/', views.classement_eleve, name='classement_eleve'),
    path('classement-national-eleves/', views.classement_national_eleves, name='classement_national_eleves'),
    path('classement-national-classes/', views.classement_national_classes, name='classement_national_classes'),

    # Défis
    path('defis/', views.defis_liste, name='defis_liste'),
    path('defi/<int:defi_id>/', views.defi_detail, name='defi_detail'),
    path('creer-defi/', views.creer_defi, name='creer_defi'),

    # Enseignant
    path('dashboard-enseignant/', views.dashboard_enseignant, name='dashboard_enseignant'),
    path('creer-classe/', views.creer_classe, name='creer_classe'),
    path('rejoindre-classe/', views.rejoindre_classe, name='rejoindre_classe'),
    path('inscription-eleve/', views.inscription_eleve, name='inscription_eleve'),
    path('export-csv/<int:classe_id>/', views.export_eleves_csv, name='export_eleves_csv'),
    path('export-pdf/<int:classe_id>/', views.export_eleves_pdf, name='export_eleves_pdf'),
    path('export-eleve-pdf/<int:eleve_id>/', views.export_eleve_pdf, name='export_eleve_pdf'),
    path('notifications/', views.notifications_page, name='notifications'),
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notifications/marquer-lue/<int:notif_id>/', views.marquer_notification_lue,
         name='marquer_notification_lue'),
    path('api/notifications/marquer-toutes-lues/', views.marquer_toutes_notifications_lues,
         name='marquer_toutes_notifications_lues'),

    # Statistiques avancées
    path('statistiques-avancees/', views.statistiques_avancees, name='statistiques_avancees'),
    path('statistiques-avancees-eleve/<int:eleve_id>/', views.statistiques_avancees_eleve,
         name='statistiques_avancees_eleve'),
    path('planification-semis-eleve/<int:eleve_id>/', views.planification_semis_eleve,
         name='planification_semis_eleve'),

    # Tutoriel
    path('tutoriel/', views.tutoriel, name='tutoriel'),
    path('terminer-tutoriel/', views.terminer_tutoriel, name='terminer_tutoriel'),

    # =========================================================
    # DOCUMENTS
    # =========================================================

    # Pages légales
    path('cgu/', views.cgu, name='cgu'),
    path('confidentialite/', views.confidentialite, name='confidentialite'),
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),
    path('consentement-rgpd/', views.consentement_rgpd, name='consentement_rgpd'),

    # Documentation - Page d'accueil
    path('documentation/', views.documentation, name='documentation'),

    # Guides d'utilisation
    path('guide-particulier/', views.guide_particulier, name='guide_particulier'),
    path('guide-enseignant/', views.guide_enseignant, name='guide_enseignant'),
    path('guide-eleve/', views.guide_eleve, name='guide_eleve'),
    path('guide-junior-particulier/', views.guide_junior_particulier, name='guide_junior_particulier'),

    # Plans de test
    path('test-particulier/', views.test_particulier, name='test_particulier'),
    path('test-enseignant/', views.test_enseignant, name='test_enseignant'),
    path('test-eleve/', views.test_eleve, name='test_eleve'),
    path('test-junior-particulier/', views.test_junior_particulier, name='test_junior_particulier'),
    path('test-admin/', views.test_admin, name='test_admin'),

    # Technique
    path('architecture-technique/', views.architecture_technique, name='architecture_technique'),
    path('strategie-deploiement/', views.strategie_deploiement, name='strategie_deploiement'),
    path('guide-admin/', views.guide_admin, name='guide_admin'),

    # Business
    path('business-plan/', views.business_plan, name='business_plan'),
    path('previsionnel-financier/', views.previsionnel_financier, name='previsionnel_financier'),
    path('guide-vente-ecoles/', views.guide_vente_ecoles, name='guide_vente_ecoles'),

    # Fiche produit
    path('fiche-produit/', views.fiche_produit, name='fiche_produit'),
    path('export-fiche-produit-pdf/', views.export_fiche_produit_pdf, name='export_fiche_produit_pdf'),

    # API
    path('api/verifier-plantation/', views.verifier_plantation, name='verifier_plantation'),
    path('api/verifier-saison/', views.api_verifier_saison, name='api_verifier_saison'),
    path('meteo/', views.meteo_mapbox, name='meteo_mapbox'),
    path('api/geocode/', views.geocode_mapbox, name='geocode_mapbox'),
    path('api/stats-bento/', views.api_stats_bento, name='api_stats_bento'),
    path('api/stats-bento/eleve/<int:eleve_id>/', views.api_stats_bento_eleve, name='api_stats_bento_eleve'),


    # Mise à jour coordonnées
    path('mettre-a-jour-coordonnees/', views.mettre_a_jour_coordonnees, name='mettre_a_jour_coordonnees'),

    # Analyse des logs applicatives
    path('analyse-connexions/', views.analyse_connexions, name='analyse_connexions'),

    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),

    # Consentement parental
    path('consentement-parental/attente/', views.consentement_parental_attente, name='consentement_parental_attente'),
    path('consentement-parental/valider/<str:token>/', views.valider_consentement_parental, name='valider_consentement_parental'),

]

# =========================================================
# ✅ SILK - Profiling des requêtes (uniquement en développement)
# =========================================================
if settings.DEBUG:
    urlpatterns += [
      #  path('silk/', include('silk.urls', 'silk')),
    ]