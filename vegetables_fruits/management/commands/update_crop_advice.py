# ===================================================
# SCRIPT DE MISE À JOUR DES CONSEILS DE CULTURE
# ===================================================
# À sauvegarder dans : vegetables_fruits/management/commands/update_crop_advice.py
# Puis exécuter : python manage.py update_crop_advice
# ===================================================

from django.core.management.base import BaseCommand
from vegetables_fruits.models import Fruit, Vegetable

# --- RÈGLES PAR FAMILLE ---
FAMILY_RULES = {
    'solanacees': {
        'keywords': ['tomate', 'aubergine', 'poivron', 'piment', 'tomatillo', 'coqueret', 'physalis', 'pepino',
                     'tamarillo'],
        'conseils_preparation_sol': 'Sol riche en compost, bien drainé, exposition ensoleillée. Évitez les sols trop humides.',
        'conseils_apres_recolte': 'Arrachez les plants après la récolte. Ne pas composter si présence de maladies (mildiou).',
        'rotation_conseillee': 'Légumineuses (haricots, pois), alliacées (ail, oignon, poireau), cucurbitacées.',
        'rotation_deconseillee': 'Ne pas replanter de solanacées au même endroit pendant 4 ans.',
    },
    'apiacees': {
        'keywords': ['carotte', 'céleri', 'fenouil', 'panais', 'persil', 'cerfeuil', 'coriandre', 'aneth', 'angélique',
                     'livèche', 'maceron'],
        'conseils_preparation_sol': 'Sol léger, profond, sans cailloux ni fumier frais. Évitez les sols trop riches en azote.',
        'conseils_apres_recolte': 'Labourez légèrement pour aérer le sol. Les résidus se décomposent rapidement.',
        'rotation_conseillee': 'Choux, légumineuses (pois, haricots), solanacées.',
        'rotation_deconseillee': 'Ne pas replanter d\'apiacées au même endroit pendant 3 ans.',
    },
    'brassicacees': {
        'keywords': ['chou', 'radis', 'navet', 'roquette', 'moutarde', 'cresson', 'rutabaga', 'brocoli', 'chicon',
                     'endive', 'scorsonère', 'raifort', 'wasabi', 'cima di rapa', 'mizuna', 'pak choï'],
        'conseils_preparation_sol': 'Sol riche, calcaire, bien drainé. Pour les choux, sol bien tassé. Évitez les sols acides.',
        'conseils_apres_recolte': 'Arrachez les racines pour éviter les maladies (hernie du chou). Compostez les feuilles saines.',
        'rotation_conseillee': 'Légumineuses (haricots, pois), solanacées (tomates, aubergines), cucurbitacées.',
        'rotation_deconseillee': 'Ne pas replanter de brassicacées au même endroit pendant 4 ans.',
    },
    'alliacees': {
        'keywords': ['ail', 'oignon', 'échalote', 'poireau', 'ciboule', 'ciboulette', 'rocambole'],
        'conseils_preparation_sol': 'Sol bien drainé, pas de fumier frais. Évitez l\'humidité stagnante.',
        'conseils_apres_recolte': 'Laissez sécher les bulbes au soleil avant stockage. Nettoyez bien les résidus.',
        'rotation_conseillee': 'Légumineuses (haricots, pois), cucurbitacées (courges, concombres), solanacées.',
        'rotation_deconseillee': 'Ne pas replanter d\'alliacées au même endroit pendant 5 ans. Éviter après pommes de terre.',
    },
    'cucurbitacees': {
        'keywords': ['courge', 'concombre', 'melon', 'courgette', 'potiron', 'citrouille', 'pastèque', 'pâtisson',
                     'giromon', 'chayote', 'christophine', 'margose', 'luffa', 'calebasse', 'gourde', 'tinda'],
        'conseils_preparation_sol': 'Sol très riche en matière organique (compost, fumier décomposé), chaud et ensoleillé.',
        'conseils_apres_recolte': 'Compostez les plants sains. Retirez les racines. Paillez pour protéger le sol l\'hiver.',
        'rotation_conseillee': 'Légumineuses (haricots, pois), alliacées (ail, oignon), brassicacées.',
        'rotation_deconseillee': 'Ne pas replanter de cucurbitacées au même endroit pendant 4 ans.',
    },
    'fabacees': {
        'keywords': ['haricot', 'pois', 'fève', 'lentille', 'soja', 'arachide', 'niébé', 'dolique', 'lablab', 'gesse',
                     'pois chiche', 'azuki', 'pois carré'],
        'conseils_preparation_sol': 'Sol meuble, pas trop riche en azote (elles enrichissent naturellement le sol).',
        'conseils_apres_recolte': 'Laissez les racines en terre (elles fixent l\'azote). Broyez les tiges et enfouissez-les.',
        'rotation_conseillee': 'Solanacées (tomates), brassicacées (choux), cucurbitacées (courges).',
        'rotation_deconseillee': 'Ne pas replanter de fabacées au même endroit pendant 3 ans.',
    },
    'rosacees_fruits': {
        'keywords': ['pomme', 'poire', 'cerise', 'pêche', 'abricot', 'prune', 'fraise', 'framboise', 'mûre', 'amande',
                     'coing', 'nèfle', 'griotte', 'brugnon', 'nectarine', 'quetsche', 'mirabelle', 'reine-claude'],
        'conseils_preparation_sol': 'Trou profond (60-80cm), sol bien drainé, riche en matière organique. Exposition ensoleillée.',
        'conseils_apres_recolte': 'Ramassez les fruits tombés pour éviter les maladies. Paillez au pied. Taillez en hiver.',
        'rotation_conseillee': 'Pas de rotation (arbres pérennes). Plantez des légumineuses au pied pour enrichir le sol.',
        'rotation_deconseillee': 'Ne pas replanter un arbre fruitier au même endroit avant 5-7 ans (fatigue du sol).',
    },
    'agrumes': {
        'keywords': ['orange', 'citron', 'pamplemousse', 'mandarine', 'clémentine', 'lime', 'kumquat', 'bergamote',
                     'yuzu', 'pomelo', 'limette', 'cédrat'],
        'conseils_preparation_sol': 'Sol bien drainé, légèrement acide, riche en humus. Protéger du vent et du froid.',
        'conseils_apres_recolte': 'Taillez légèrement après la récolte. Apportez un engrais spécial agrumes au printemps.',
        'rotation_conseillee': 'Pas de rotation (arbustes pérennes). Plantez des aromatiques au pied.',
        'rotation_deconseillee': 'Évitez de replanter un agrume au même endroit avant 5 ans.',
    },
    'tropical_fruits': {
        'keywords': ['mangue', 'ananas', 'banane', 'papaye', 'fruit de la passion', 'goyave', 'litchi', 'kaki', 'figue',
                     'datte', 'avocat', 'noix de coco', 'jacque', 'durian', 'ramboutan', 'mangoustan'],
        'conseils_preparation_sol': 'Sol riche, profond, bien drainé. Climat chaud et humide nécessaire pour la plupart.',
        'conseils_apres_recolte': 'Taillez les branches mortes. Apportez du compost en surface. Protégez du froid si nécessaire.',
        'rotation_conseillee': 'Pas de rotation (arbres pérennes). Associez avec des légumineuses couvre-sol.',
        'rotation_deconseillee': 'Évitez de replanter la même espèce au même endroit.',
    },
    'legumes_feuilles': {
        'keywords': ['salade', 'laitue', 'épinard', 'bette', 'blette', 'mâche', 'scarole', 'frisée', 'chicorée',
                     'roquette', 'cresson', 'pourpier', 'oseille', 'ortie', 'arroche', 'tétragone'],
        'conseils_preparation_sol': 'Sol frais, riche en humus, bien ameubli. Mi-ombre en été pour éviter la montée en graines.',
        'conseils_apres_recolte': 'Arrachez les plants montés. Semez un engrais vert (moutarde, phacélie) pour le sol.',
        'rotation_conseillee': 'Solanacées (tomates), cucurbitacées (courges), fabacées (haricots).',
        'rotation_deconseillee': 'Évitez de cultiver des légumes-feuilles 2 années de suite au même endroit.',
    },
    'tubercules': {
        'keywords': ['pomme de terre', 'patate', 'topinambour', 'igname', 'manioc', 'patate douce', 'taro', 'oca',
                     'crosne', 'hélianthi', 'chervis', 'yacón'],
        'conseils_preparation_sol': 'Sol profond, meuble, bien drainé. Buttez au fur et à mesure de la croissance.',
        'conseils_apres_recolte': 'Retirez tous les tubercules du sol pour éviter les repousses. Labourez profondément.',
        'rotation_conseillee': 'Légumineuses (haricots, pois), brassicacées (choux), alliacées (ail).',
        'rotation_deconseillee': 'Ne pas replanter de tubercules au même endroit pendant 4 ans. Éviter après solanacées.',
    },
    'aromatiques': {
        'keywords': ['basilic', 'menthe', 'thym', 'romarin', 'sauge', 'origan', 'estragon', 'marjolaine', 'cerfeuil',
                     'aneth', 'coriandre', 'shiso', 'périlla'],
        'conseils_preparation_sol': 'Sol bien drainé, plutôt pauvre pour concentrer les arômes. Plein soleil.',
        'conseils_apres_recolte': 'Taillez après la floraison. Protégez les vivaces en hiver (paillage).',
        'rotation_conseillee': 'Plantez près des légumes pour éloigner les ravageurs (compagnonnage).',
        'rotation_deconseillee': 'Certaines (menthe) sont envahissantes, cultivez en pot.',
    },
    # --- CONSEILS GÉNÉRIQUES POUR LES SANS-FAMILLE ---
    'generique_fruit': {
        'keywords': [],
        'conseils_preparation_sol': 'Sol bien drainé, enrichi en compost. Exposition ensoleillée recommandée.',
        'conseils_apres_recolte': 'Ramasser les fruits tombés. Pailler le pied pour l\'hiver.',
        'rotation_conseillee': 'Variez les cultures chaque année pour préserver le sol.',
        'rotation_deconseillee': 'Évitez de replanter la même espèce au même endroit.',
    },
    'generique_legume': {
        'keywords': [],
        'conseils_preparation_sol': 'Sol ameubli, enrichi en matière organique. Désherbez avant plantation.',
        'conseils_apres_recolte': 'Retirez les résidus de culture. Semez un engrais vert pour protéger le sol.',
        'rotation_conseillee': 'Pratiquez la rotation des cultures : alternez les familles de légumes.',
        'rotation_deconseillee': 'Évitez de cultiver la même famille botanique 2 années de suite.',
    },
}


def find_family(name, rules_dict):
    """Trouve la famille d'une plante selon son nom"""
    name_lower = name.lower().strip()
    for family, rules in rules_dict.items():
        if family in ['generique_fruit', 'generique_legume']:
            continue
        for keyword in rules['keywords']:
            if keyword in name_lower:
                return family, rules
    return None, None


class Command(BaseCommand):
    help = 'Met à jour les conseils de culture pour les fruits et légumes sans famille'

    def handle(self, *args, **options):
        updated_fruits = 0
        updated_vegetables = 0
        generic_fruits = 0
        generic_vegetables = 0

        # --- FRUITS ---
        self.stdout.write('\n🍎 Mise à jour des fruits SANS conseils...')
        fruits_to_update = Fruit.objects.filter(conseils_preparation_sol__isnull=True)

        for fruit in fruits_to_update:
            family, rules = find_family(fruit.nom, FAMILY_RULES)

            if rules:
                fruit.conseils_preparation_sol = rules['conseils_preparation_sol']
                fruit.conseils_apres_recolte = rules['conseils_apres_recolte']
                fruit.rotation_conseillee = rules['rotation_conseillee']
                fruit.rotation_deconseillee = rules['rotation_deconseillee']
                fruit.save()
                updated_fruits += 1
                self.stdout.write(f' ✅ {fruit.nom} → {family}')
            else:
                # Appliquer les conseils génériques
                generic_rules = FAMILY_RULES['generique_fruit']
                fruit.conseils_preparation_sol = generic_rules['conseils_preparation_sol']
                fruit.conseils_apres_recolte = generic_rules['conseils_apres_recolte']
                fruit.rotation_conseillee = generic_rules['rotation_conseillee']
                fruit.rotation_deconseillee = generic_rules['rotation_deconseillee']
                fruit.save()
                generic_fruits += 1
                self.stdout.write(f' 🔶 {fruit.nom} → générique')

        # --- LÉGUMES ---
        self.stdout.write('\n🥕 Mise à jour des légumes SANS conseils...')
        vegetables_to_update = Vegetable.objects.filter(conseils_preparation_sol__isnull=True)

        for vegetable in vegetables_to_update:
            family, rules = find_family(vegetable.nom, FAMILY_RULES)

            if rules:
                vegetable.conseils_preparation_sol = rules['conseils_preparation_sol']
                vegetable.conseils_apres_recolte = rules['conseils_apres_recolte']
                vegetable.rotation_conseillee = rules['rotation_conseillee']
                vegetable.rotation_deconseillee = rules['rotation_deconseillee']
                vegetable.save()
                updated_vegetables += 1
                self.stdout.write(f' ✅ {vegetable.nom} → {family}')
            else:
                # Appliquer les conseils génériques
                generic_rules = FAMILY_RULES['generique_legume']
                vegetable.conseils_preparation_sol = generic_rules['conseils_preparation_sol']
                vegetable.conseils_apres_recolte = generic_rules['conseils_apres_recolte']
                vegetable.rotation_conseillee = generic_rules['rotation_conseillee']
                vegetable.rotation_deconseillee = generic_rules['rotation_deconseillee']
                vegetable.save()
                generic_vegetables += 1
                self.stdout.write(f' 🔶 {vegetable.nom} → générique')

        # --- RÉSUMÉ ---
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS(f'✅ Fruits avec famille : {updated_fruits}'))
        self.stdout.write(self.style.WARNING(f'🔶 Fruits génériques : {generic_fruits}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Légumes avec famille : {updated_vegetables}'))
        self.stdout.write(self.style.WARNING(f'🔶 Légumes génériques : {generic_vegetables}'))
        self.stdout.write('=' * 50)