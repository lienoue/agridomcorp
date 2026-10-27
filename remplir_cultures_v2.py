from vegetables_fruits.models import Fruit, Vegetable


# ============================================
# FONCTION DE REMPLISSAGE POUR LES FRUITS
# ============================================

def remplir_fruit(fruit):
    nom = fruit.nom.lower()
    modifie = False

    # Déterminer le type de fruit
    if 'agrume' in nom or nom in ['orange', 'citron', 'mandarine', 'clémentine', 'pamplemousse', 'limette', 'kumquat']:
        valeurs = {
            'provenance': 'Asie, Méditerranée',
            'prix': 3,
            'plantation': 'février, mars',
            'saison': 'hiver, printemps',
            'recolte': 'novembre, décembre',
            'pollinisation_type': 'insectes',
            'besoin_pollinisateur': False,
            'distance_pollinisation': 10,
            'periode_floraison': 'printemps',
            'conseils_pollinisation': 'Attire les abeilles, auto-fertile pour la plupart des variétés.',
            'semis_interieur': 'Non',
            'semis_exterieur': 'Non',
            'jours_levée': 30,
            'jours_recolte': 180,
            'profondeur_semis': '2 cm',
            'espacement': '5 m',
            'conseils_preparation_sol': 'Sol bien drainé, légèrement acide.',
            'conseils_apres_recolte': 'Taille légère après récolte.',
            'rotation_conseillee': 'Ne pas planter après d\'autres agrumes.',
            'rotation_deconseillee': 'Éviter après ombellifères.'
        }
    elif 'tropical' in nom or nom in ['banane', 'ananas', 'mangue', 'litchi', 'fruit de la passion', 'papaye',
                                      'goyave']:
        valeurs = {
            'provenance': 'Amérique du Sud, Asie',
            'prix': 4,
            'plantation': 'toute l\'année',
            'saison': 'été',
            'recolte': 'toute l\'année',
            'pollinisation_type': 'croisee',
            'besoin_pollinisateur': True,
            'distance_pollinisation': 50,
            'periode_floraison': 'toute l\'année',
            'conseils_pollinisation': 'Nécessite une autre variété pour la pollinisation croisée.',
            'semis_interieur': 'Non',
            'semis_exterieur': 'Oui',
            'jours_levée': 30,
            'jours_recolte': 365,
            'profondeur_semis': '3 cm',
            'espacement': '4 m',
            'conseils_preparation_sol': 'Sol riche en matière organique.',
            'conseils_apres_recolte': 'Nettoyer et fertiliser.',
            'rotation_conseillee': 'Rotation avec légumineuses.',
            'rotation_deconseillee': 'Éviter après solanacées.'
        }
    elif 'baie' in nom or nom in ['fraise', 'framboise', 'mûre', 'cassis', 'myrtille', 'groseille']:
        valeurs = {
            'provenance': 'Europe, Amérique du Nord',
            'prix': 5,
            'plantation': 'février, mars, avril',
            'saison': 'printemps, été',
            'recolte': 'juin, juillet, août',
            'pollinisation_type': 'insectes',
            'besoin_pollinisateur': False,
            'distance_pollinisation': 5,
            'periode_floraison': 'printemps',
            'conseils_pollinisation': 'Auto-fertile, mais la présence d\'abeilles améliore la production.',
            'semis_interieur': 'Non',
            'semis_exterieur': 'Oui',
            'jours_levée': 20,
            'jours_recolte': 90,
            'profondeur_semis': '1 cm',
            'espacement': '1 m',
            'conseils_preparation_sol': 'Sol acide, riche en humus.',
            'conseils_apres_recolte': 'Tailler les vieux bois.',
            'rotation_conseillee': 'Rotation tous les 3 ans.',
            'rotation_deconseillee': 'Éviter après solanacées.'
        }
    elif 'noyau' in nom or nom in ['pêche', 'abricot', 'cerise', 'prune', 'quetsche', 'mirabelle']:
        valeurs = {
            'provenance': 'Asie, Europe',
            'prix': 4,
            'plantation': 'février, mars',
            'saison': 'été',
            'recolte': 'juillet, août',
            'pollinisation_type': 'insectes',
            'besoin_pollinisateur': True,
            'distance_pollinisation': 20,
            'periode_floraison': 'printemps',
            'conseils_pollinisation': 'Nécessite une variété pollinisatrice pour une bonne production.',
            'semis_interieur': 'Non',
            'semis_exterieur': 'Non',
            'jours_levée': 60,
            'jours_recolte': 180,
            'profondeur_semis': '3 cm',
            'espacement': '5 m',
            'conseils_preparation_sol': 'Sol profond, bien drainé.',
            'conseils_apres_recolte': 'Taille de formation.',
            'rotation_conseillee': 'Rotation avec légumineuses.',
            'rotation_deconseillee': 'Éviter après rosacées.'
        }
    elif 'pomme' in nom or 'poire' in nom or 'coing' in nom:
        valeurs = {
            'provenance': 'Asie centrale, Europe',
            'prix': 2,
            'plantation': 'février, mars',
            'saison': 'automne',
            'recolte': 'septembre, octobre',
            'pollinisation_type': 'insectes',
            'besoin_pollinisateur': True,
            'distance_pollinisation': 30,
            'periode_floraison': 'printemps',
            'conseils_pollinisation': 'Nécessite une variété pollinisatrice pour une bonne fructification.',
            'semis_interieur': 'Non',
            'semis_exterieur': 'Non',
            'jours_levée': 60,
            'jours_recolte': 300,
            'profondeur_semis': '2 cm',
            'espacement': '4 m',
            'conseils_preparation_sol': 'Sol frais, profond, bien drainé.',
            'conseils_apres_recolte': 'Taille d\'entretien.',
            'rotation_conseillee': 'Rotation avec légumineuses.',
            'rotation_deconseillee': 'Éviter après rosacées.'
        }
    elif 'vigne' in nom or 'raisin' in nom:
        valeurs = {
            'provenance': 'Méditerranée, Asie',
            'prix': 3,
            'plantation': 'mars, avril',
            'saison': 'automne',
            'recolte': 'septembre, octobre',
            'pollinisation_type': 'vent',
            'besoin_pollinisateur': False,
            'distance_pollinisation': 100,
            'periode_floraison': 'printemps',
            'conseils_pollinisation': 'Pollinisation par le vent, pas besoin d\'insectes.',
            'semis_interieur': 'Non',
            'semis_exterieur': 'Oui',
            'jours_levée': 15,
            'jours_recolte': 180,
            'profondeur_semis': '2 cm',
            'espacement': '2 m',
            'conseils_preparation_sol': 'Sol calcaire, bien drainé.',
            'conseils_apres_recolte': 'Taille d\'hiver.',
            'rotation_conseillee': 'Rotation tous les 4 ans.',
            'rotation_deconseillee': 'Éviter après vigne.'
        }
    else:
        # Fruit standard (par défaut)
        valeurs = {
            'provenance': 'Monde',
            'prix': 3,
            'plantation': 'février, mars',
            'saison': 'été',
            'recolte': 'août, septembre',
            'pollinisation_type': 'insectes',
            'besoin_pollinisateur': False,
            'distance_pollinisation': 10,
            'periode_floraison': 'printemps',
            'conseils_pollinisation': 'Pollinisation par les insectes, auto-fertile.',
            'semis_interieur': 'Non',
            'semis_exterieur': 'Oui',
            'jours_levée': 30,
            'jours_recolte': 180,
            'profondeur_semis': '2 cm',
            'espacement': '3 m',
            'conseils_preparation_sol': 'Sol ordinaire, bien drainé.',
            'conseils_apres_recolte': 'Taille légère.',
            'rotation_conseillee': 'Rotation avec légumineuses.',
            'rotation_deconseillee': 'Éviter après solanacées.'
        }

    # Appliquer les valeurs uniquement si le champ est égal à "variable" (ou vide)
    for champ, valeur in valeurs.items():
        valeur_actuelle = getattr(fruit, champ, None)
        if valeur_actuelle == 'variable' or valeur_actuelle is None or valeur_actuelle == '' or valeur_actuelle == 0:
            setattr(fruit, champ, valeur)
            modifie = True

    return modifie


# ============================================
# FONCTION DE REMPLISSAGE POUR LES LÉGUMES
# ============================================

def remplir_legume(legume):
    nom = legume.nom.lower()
    modifie = False

    if 'racine' in nom or nom in ['carotte', 'betterave', 'radis', 'navet', 'panais', 'topinambour']:
        valeurs = {
            'provenance': 'Europe, Asie',
            'prix': 1,
            'plantation': 'mars, avril, mai',
            'saison': 'été',
            'recolte': 'juillet, août, septembre',
            'pollinisation_type': 'auto',
            'besoin_pollinisateur': False,
            'distance_pollinisation': 0,
            'periode_floraison': 'été',
            'conseils_pollinisation': 'Auto-pollinisation, pas besoin d\'insectes.',
            'semis_interieur': 'Non',
            'semis_exterieur': 'Oui',
            'jours_levée': 10,
            'jours_recolte': 90,
            'profondeur_semis': '1 cm',
            'espacement': '10 cm',
            'conseils_preparation_sol': 'Sol meuble, sans cailloux.',
            'conseils_apres_recolte': 'Ajouter du compost.',
            'rotation_conseillee': 'Rotation avec légumineuses.',
            'rotation_deconseillee': 'Éviter après ombellifères.'
        }
    elif 'feuille' in nom or nom in ['salade', 'laitue', 'roquette', 'mâche', 'épinard', 'chou']:
        valeurs = {
            'provenance': 'Europe, Amérique',
            'prix': 1,
            'plantation': 'mars, avril, mai',
            'saison': 'printemps',
            'recolte': 'mai, juin',
            'pollinisation_type': 'auto',
            'besoin_pollinisateur': False,
            'distance_pollinisation': 0,
            'periode_floraison': 'printemps',
            'conseils_pollinisation': 'Auto-pollinisation, floraison rapide.',
            'semis_interieur': 'Oui',
            'semis_exterieur': 'Oui',
            'jours_levée': 5,
            'jours_recolte': 60,
            'profondeur_semis': '0.5 cm',
            'espacement': '20 cm',
            'conseils_preparation_sol': 'Sol riche en azote.',
            'conseils_apres_recolte': 'Arroser et fertiliser.',
            'rotation_conseillee': 'Rotation avec légumineuses.',
            'rotation_deconseillee': 'Éviter après choux.'
        }
    elif 'fruit' in nom or nom in ['tomate', 'courgette', 'concombre', 'aubergine', 'poivron', 'piment']:
        valeurs = {
            'provenance': 'Amérique du Sud',
            'prix': 2,
            'plantation': 'avril, mai',
            'saison': 'été',
            'recolte': 'juillet, août, septembre',
            'pollinisation_type': 'insectes',
            'besoin_pollinisateur': False,
            'distance_pollinisation': 10,
            'periode_floraison': 'été',
            'conseils_pollinisation': 'Pollinisation par les insectes, peut être améliorée par secouage.',
            'semis_interieur': 'Oui',
            'semis_exterieur': 'Oui',
            'jours_levée': 10,
            'jours_recolte': 90,
            'profondeur_semis': '1 cm',
            'espacement': '50 cm',
            'conseils_preparation_sol': 'Sol riche, bien drainé.',
            'conseils_apres_recolte': 'Ajouter du compost.',
            'rotation_conseillee': 'Rotation avec légumineuses.',
            'rotation_deconseillee': 'Éviter après solanacées.'
        }
    elif 'bulbe' in nom or nom in ['oignon', 'ail', 'échalote', 'poireau']:
        valeurs = {
            'provenance': 'Asie centrale',
            'prix': 1,
            'plantation': 'février, mars',
            'saison': 'été',
            'recolte': 'juillet, août',
            'pollinisation_type': 'insectes',
            'besoin_pollinisateur': False,
            'distance_pollinisation': 5,
            'periode_floraison': 'été',
            'conseils_pollinisation': 'Pollinisation par les insectes, floraison en deuxième année.',
            'semis_interieur': 'Oui',
            'semis_exterieur': 'Oui',
            'jours_levée': 10,
            'jours_recolte': 180,
            'profondeur_semis': '1 cm',
            'espacement': '15 cm',
            'conseils_preparation_sol': 'Sol léger, bien drainé.',
            'conseils_apres_recolte': 'Laisser sécher au soleil.',
            'rotation_conseillee': 'Rotation avec légumineuses.',
            'rotation_deconseillee': 'Éviter après liliacées.'
        }
    else:
        # Légume standard
        valeurs = {
            'provenance': 'Monde',
            'prix': 1,
            'plantation': 'mars, avril',
            'saison': 'été',
            'recolte': 'juillet, août',
            'pollinisation_type': 'auto',
            'besoin_pollinisateur': False,
            'distance_pollinisation': 0,
            'periode_floraison': 'été',
            'conseils_pollinisation': 'Auto-pollinisation.',
            'semis_interieur': 'Oui',
            'semis_exterieur': 'Oui',
            'jours_levée': 10,
            'jours_recolte': 90,
            'profondeur_semis': '1 cm',
            'espacement': '30 cm',
            'conseils_preparation_sol': 'Sol ordinaire.',
            'conseils_apres_recolte': 'Arroser.',
            'rotation_conseillee': 'Rotation avec légumineuses.',
            'rotation_deconseillee': 'Éviter après même famille.'
        }

    # Appliquer les valeurs uniquement si le champ est égal à "variable" (ou vide)
    for champ, valeur in valeurs.items():
        valeur_actuelle = getattr(legume, champ, None)
        if valeur_actuelle == 'Variable' or valeur_actuelle is None or valeur_actuelle == '' or valeur_actuelle == 0:
            setattr(legume, champ, valeur)
            modifie = True

    return modifie


# ============================================
# APPLICATION DU REMPLISSAGE
# ============================================

print("🔍 Remplissage des champs manquants pour les fruits...")
fruit_modifies = 0
for fruit in Fruit.objects.all():
    if remplir_fruit(fruit):
        fruit.save()
        fruit_modifies = fruit_modifies + 1
print("✅ %d fruits ont été modifiés." % fruit_modifies)

print("\n🔍 Remplissage des champs manquants pour les légumes...")
legume_modifies = 0
for legume in Vegetable.objects.all():
    if remplir_legume(legume):
        legume.save()
        legume_modifies = legume_modifies + 1
print("✅ %d légumes ont été modifiés." % legume_modifies)

# ============================================
# RÉSUMÉ
# ============================================

total_fruits = Fruit.objects.count()
total_legumes = Vegetable.objects.count()
print("\n📊 Résumé :")
print(" - Fruits totaux : %d" % total_fruits)
print(" - Fruits modifiés : %d" % fruit_modifies)
print(" - Légumes totaux : %d" % total_legumes)
print(" - Légumes modifiés : %d" % legume_modifies)