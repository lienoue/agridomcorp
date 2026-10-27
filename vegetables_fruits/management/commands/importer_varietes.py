from django.core.management.base import BaseCommand
from vegetables_fruits.models import Culture, Variete


class Command(BaseCommand):
    help = 'Importe les variétés de fruits et légumes du monde entier'

    def handle(self, *args, **options):
        # ✅ Données complètes par zone géographique
        varietes_data = {
            # === AFRIQUE ===
            'Mangue': [
                {'nom': 'Alphonso', 'zones': 'Asie,Afrique', 'climat': 'tropical',
                 'description': 'Mangue royale, très sucrée', 'saison': 'Mai-Juin', 'jours': 90},
                {'nom': 'Kent', 'zones': 'Amérique,Afrique', 'climat': 'tropical',
                 'description': 'Grosse, juteuse, peu fibreuse', 'saison': 'Juin-Juillet', 'jours': 85},
                {'nom': 'Tommy Atkins', 'zones': 'Amérique,Afrique,Asie', 'climat': 'tropical',
                 'description': 'Résistante, longue conservation', 'saison': 'Juin-Août', 'jours': 95},
                {'nom': 'Keitt', 'zones': 'Amérique,Asie,Afrique', 'climat': 'tropical',
                 'description': 'Grosse, sucrée, peu fibreuse', 'saison': 'Juillet-Septembre', 'jours': 100},
                {'nom': 'Apple Mango', 'zones': 'Asie,Afrique', 'climat': 'tropical',
                 'description': 'Petite, très sucrée', 'saison': 'Mai-Juin', 'jours': 80},
            ],
            'Papaye': [
                {'nom': 'Solo', 'zones': 'Amérique,Asie,Afrique', 'climat': 'tropical',
                 'description': 'Petite, très sucrée', 'saison': 'Toute l\'année', 'jours': 180},
                {'nom': 'Sunrise', 'zones': 'Amérique,Afrique', 'climat': 'tropical',
                 'description': 'Grosse, chair orange', 'saison': 'Toute l\'année', 'jours': 200},
                {'nom': 'Red Lady', 'zones': 'Amérique,Asie', 'climat': 'tropical',
                 'description': 'Résistante, productive', 'saison': 'Toute l\'année', 'jours': 190},
            ],
            'Banane': [
                {'nom': 'Cavendish', 'zones': 'Asie,Amérique,Afrique', 'climat': 'tropical',
                 'description': 'La plus commune', 'saison': 'Toute l\'année', 'jours': 120},
                {'nom': 'Plantain', 'zones': 'Afrique,Amérique', 'climat': 'tropical',
                 'description': 'Cuite, féculente', 'saison': 'Toute l\'année', 'jours': 150},
                {'nom': 'Gros Michel', 'zones': 'Amérique,Asie', 'climat': 'tropical',
                 'description': 'Ancienne, parfumée', 'saison': 'Toute l\'année', 'jours': 130},
            ],
            'Ananas': [
                {'nom': 'Cayenne', 'zones': 'Amérique,Afrique', 'climat': 'tropical', 'description': 'La plus cultivée',
                 'saison': 'Toute l\'année', 'jours': 365},
                {'nom': 'Queen', 'zones': 'Océanie,Afrique', 'climat': 'tropical', 'description': 'Petite, très sucrée',
                 'saison': 'Toute l\'année', 'jours': 330},
                {'nom': 'Sugarloaf', 'zones': 'Amérique,Afrique', 'climat': 'tropical',
                 'description': 'Chair blanche, très sucrée', 'saison': 'Toute l\'année', 'jours': 350},
            ],
            'Avocat': [
                {'nom': 'Hass', 'zones': 'Amérique,Europe,Océanie,Afrique', 'climat': 'mediterraneen',
                 'description': 'Peau noire, crémeux', 'saison': 'Toute l\'année', 'jours': 365},
                {'nom': 'Fuerte', 'zones': 'Amérique,Europe,Afrique', 'climat': 'mediterraneen',
                 'description': 'Peau verte, fondant', 'saison': 'Automne-Hiver', 'jours': 300},
                {'nom': 'Bacon', 'zones': 'Amérique,Europe', 'climat': 'mediterraneen', 'description': 'Léger, fondant',
                 'saison': 'Hiver', 'jours': 280},
                {'nom': 'Pinkerton', 'zones': 'Amérique,Afrique,Europe', 'climat': 'mediterraneen',
                 'description': 'Allongé, bonne conservation', 'saison': 'Hiver-Printemps', 'jours': 320},
            ],
            'Tomate': [
                {'nom': 'Cœur de Bœuf', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Grosse tomate charnue, peu de graines', 'saison': 'Juillet-Septembre', 'jours': 90},
                {'nom': 'Roma', 'zones': 'Europe,Amérique,Afrique', 'climat': 'tempere',
                 'description': 'Allongée, pour sauce', 'saison': 'Juillet-Septembre', 'jours': 80},
                {'nom': 'San Marzano', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Allongée, pour sauce', 'saison': 'Août-Septembre', 'jours': 85},
                {'nom': 'Cherry', 'zones': 'Europe,Amérique,Asie', 'climat': 'tempere', 'description': 'Petite, sucrée',
                 'saison': 'Juillet-Octobre', 'jours': 70},
                {'nom': 'Andine Cornue', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Allongée, peu de graines', 'saison': 'Août-Septembre', 'jours': 95},
                {'nom': 'Noire de Crimée', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Foncée, saveur intense', 'saison': 'Août-Septembre', 'jours': 100},
                {'nom': 'Green Zebra', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Verte rayée, acidulée', 'saison': 'Août-Septembre', 'jours': 90},
                {'nom': 'Nigerian', 'zones': 'Afrique', 'climat': 'tropical', 'description': 'Résistante à la chaleur',
                 'saison': 'Toute l\'année', 'jours': 75},
                {'nom': 'Roma Africana', 'zones': 'Afrique', 'climat': 'tropical',
                 'description': 'Ronde, bonne conservation', 'saison': 'Toute l\'année', 'jours': 80},
            ],
            'Poivron': [
                {'nom': 'Bell Pepper', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Doux, en cloche', 'saison': 'Juillet-Octobre', 'jours': 75},
                {'nom': 'Jalapeño', 'zones': 'Amérique', 'climat': 'sub-tropical', 'description': 'Piquant, vert',
                 'saison': 'Juillet-Octobre', 'jours': 80},
                {'nom': 'Habanero', 'zones': 'Amérique', 'climat': 'sub-tropical', 'description': 'Très piquant',
                 'saison': 'Août-Octobre', 'jours': 90},
                {'nom': 'Poblano', 'zones': 'Amérique', 'climat': 'sub-tropical', 'description': 'Doux, pour farcir',
                 'saison': 'Août-Octobre', 'jours': 85},
                {'nom': 'Paprika Africain', 'zones': 'Afrique', 'climat': 'tropical', 'description': 'Rouge, doux',
                 'saison': 'Toute l\'année', 'jours': 80},
                {'nom': 'Shishito', 'zones': 'Asie', 'climat': 'tempere', 'description': 'Doux, grillé',
                 'saison': 'Juillet-Octobre', 'jours': 70},
            ],
            'Pomme de terre': [
                {'nom': 'Bintje', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Jaune, farineuse',
                 'saison': 'Juillet-Octobre', 'jours': 120},
                {'nom': 'Charlott', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Jaune, ferme',
                 'saison': 'Juillet-Septembre', 'jours': 100},
                {'nom': 'Ratte', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Allongée, fine',
                 'saison': 'Septembre-Octobre', 'jours': 130},
                {'nom': 'Russet', 'zones': 'Amérique', 'climat': 'tempere', 'description': 'Grosse, farineuse',
                 'saison': 'Septembre-Octobre', 'jours': 140},
                {'nom': 'Yukon Gold', 'zones': 'Amérique', 'climat': 'tempere', 'description': 'Jaune, beurrée',
                 'saison': 'Août-Octobre', 'jours': 110},
            ],
            'Salade': [
                {'nom': 'Batavia', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Feuilles vertes, croustillantes', 'saison': 'Printemps-Automne', 'jours': 60},
                {'nom': 'Romaine', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Feuilles allongées, croquantes', 'saison': 'Printemps-Automne', 'jours': 65},
                {'nom': 'Feuille de chêne', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Feuilles découpées, tendres', 'saison': 'Printemps-Automne', 'jours': 55},
                {'nom': 'Iceberg', 'zones': 'Amérique,Europe', 'climat': 'tempere',
                 'description': 'Feuilles croquantes, pommée', 'saison': 'Printemps-Automne', 'jours': 60},
            ],
            # === AMÉRIQUE ===
            'Orange': [
                {'nom': 'Valencia', 'zones': 'Amérique,Europe,Afrique', 'climat': 'sub-tropical',
                 'description': 'Pour jus, tardive', 'saison': 'Mars-Juin', 'jours': 365},
                {'nom': 'Washington Navel', 'zones': 'Amérique,Europe,Afrique', 'climat': 'sub-tropical',
                 'description': 'À manger, sans pépins', 'saison': 'Novembre-Janvier', 'jours': 300},
                {'nom': 'Hamlin', 'zones': 'Amérique', 'climat': 'sub-tropical', 'description': 'Précoce, juteuse',
                 'saison': 'Octobre-Décembre', 'jours': 280},
                {'nom': 'Pineapple', 'zones': 'Amérique', 'climat': 'sub-tropical', 'description': 'Parfumée, douce',
                 'saison': 'Novembre-Janvier', 'jours': 290},
            ],
            'Citron': [
                {'nom': 'Eureka', 'zones': 'Amérique,Europe', 'climat': 'mediterraneen',
                 'description': 'Classique, acide', 'saison': 'Toute l\'année', 'jours': 365},
                {'nom': 'Lisbon', 'zones': 'Amérique,Europe', 'climat': 'mediterraneen',
                 'description': 'Très acide, productif', 'saison': 'Toute l\'année', 'jours': 365},
                {'nom': 'Meyer', 'zones': 'Amérique', 'climat': 'mediterraneen', 'description': 'Doux, parfumé',
                 'saison': 'Automne-Hiver', 'jours': 300},
            ],
            'Pamplemousse': [
                {'nom': 'Ruby Red', 'zones': 'Amérique', 'climat': 'sub-tropical', 'description': 'Rose, peu amer',
                 'saison': 'Automne-Hiver', 'jours': 365},
                {'nom': 'White Marsh', 'zones': 'Amérique', 'climat': 'sub-tropical', 'description': 'Blanc, amer',
                 'saison': 'Automne-Hiver', 'jours': 365},
                {'nom': 'Pink', 'zones': 'Amérique', 'climat': 'sub-tropical', 'description': 'Rose, doux',
                 'saison': 'Automne-Hiver', 'jours': 365},
            ],
            'Maïs': [
                {'nom': 'Sweet Corn', 'zones': 'Amérique,Europe,Asie', 'climat': 'tempere',
                 'description': 'Jaune, sucré', 'saison': 'Été', 'jours': 75},
                {'nom': 'Silver Queen', 'zones': 'Amérique', 'climat': 'tempere', 'description': 'Blanc, très sucré',
                 'saison': 'Été', 'jours': 85},
            ],
            # === ASIE ===
            'Litchi': [
                {'nom': 'Mauritius', 'zones': 'Asie,Afrique', 'climat': 'tropical', 'description': 'Petit, parfumé',
                 'saison': 'Mai-Juin', 'jours': 90},
                {'nom': 'Brewster', 'zones': 'Asie,Amérique', 'climat': 'tropical', 'description': 'Gros, juteux',
                 'saison': 'Juin-Juillet', 'jours': 95},
                {'nom': 'Bengal', 'zones': 'Asie', 'climat': 'tropical', 'description': 'Très parfumé',
                 'saison': 'Mai-Juin', 'jours': 85},
            ],
            'Durian': [
                {'nom': 'Monthong', 'zones': 'Asie', 'climat': 'tropical', 'description': 'Le plus populaire',
                 'saison': 'Juillet-Août', 'jours': 365},
                {'nom': 'Chanee', 'zones': 'Asie', 'climat': 'tropical', 'description': 'Gros, crémeux',
                 'saison': 'Juillet-Août', 'jours': 365},
                {'nom': 'Musang King', 'zones': 'Asie', 'climat': 'tropical', 'description': 'Très crémeux, amer',
                 'saison': 'Juillet-Août', 'jours': 365},
            ],
            'Ramboutan': [
                {'nom': 'Rongrien', 'zones': 'Asie', 'climat': 'tropical', 'description': 'Rouge, chevelu',
                 'saison': 'Juin-Août', 'jours': 90},
                {'nom': 'Binjai', 'zones': 'Asie', 'climat': 'tropical', 'description': 'Gros, sucré',
                 'saison': 'Juillet-Septembre', 'jours': 95},
            ],
            'Longane': [
                {'nom': 'Kohala', 'zones': 'Asie', 'climat': 'tropical', 'description': 'Brun, doux',
                 'saison': 'Juillet-Août', 'jours': 85},
                {'nom': 'Biew Kiew', 'zones': 'Asie', 'climat': 'tropical', 'description': 'Très sucré',
                 'saison': 'Juillet-Août', 'jours': 90},
            ],
            'Fruit du dragon': [
                {'nom': 'Hylocereus', 'zones': 'Amérique,Asie,Afrique', 'climat': 'tropical',
                 'description': 'Chair blanche', 'saison': 'Toute l\'année', 'jours': 365},
                {'nom': 'Red', 'zones': 'Amérique,Asie', 'climat': 'tropical', 'description': 'Chair rouge',
                 'saison': 'Toute l\'année', 'jours': 365},
            ],
            'Soja': [
                {'nom': 'Edamame', 'zones': 'Asie,Amérique', 'climat': 'tempere', 'description': 'Vert, pour fèves',
                 'saison': 'Été', 'jours': 90},
                {'nom': 'Enrei', 'zones': 'Asie', 'climat': 'tempere', 'description': 'Pour huile, tofu',
                 'saison': 'Été', 'jours': 100},
            ],
            # === EUROPE ===
            'Pomme': [
                {'nom': 'Golden Delicious', 'zones': 'Europe,Amérique,Afrique', 'climat': 'tempere',
                 'description': 'Jaune, sucrée', 'saison': 'Septembre-Octobre', 'jours': 180},
                {'nom': 'Gala', 'zones': 'Europe,Amérique,Océanie', 'climat': 'tempere', 'description': 'Rouge, sucrée',
                 'saison': 'Septembre-Octobre', 'jours': 170},
                {'nom': 'Fuji', 'zones': 'Europe,Amérique,Asie', 'climat': 'tempere',
                 'description': 'Très sucrée, croquante', 'saison': 'Octobre-Novembre', 'jours': 195},
                {'nom': 'Granny Smith', 'zones': 'Europe,Amérique,Océanie', 'climat': 'tempere',
                 'description': 'Verte, acidulée', 'saison': 'Octobre-Novembre', 'jours': 190},
                {'nom': 'Pink Lady', 'zones': 'Europe,Amérique,Océanie', 'climat': 'tempere',
                 'description': 'Rose, sucrée', 'saison': 'Octobre-Novembre', 'jours': 185},
                {'nom': 'Reinette', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Ancienne, parfumée',
                 'saison': 'Octobre-Novembre', 'jours': 180},
                {'nom': 'Cox Orange', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Orange, parfumée',
                 'saison': 'Septembre-Octobre', 'jours': 175},
                {'nom': 'Jonagold', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Jaune-rouge, sucrée', 'saison': 'Septembre-Octobre', 'jours': 185},
            ],
            'Poire': [
                {'nom': 'Williams', 'zones': 'Europe,Amérique', 'climat': 'tempere', 'description': 'Jaune, sucrée',
                 'saison': 'Septembre-Octobre', 'jours': 160},
                {'nom': 'Conference', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Allongée, juteuse', 'saison': 'Octobre', 'jours': 165},
                {'nom': 'Comice', 'zones': 'Europe,Amérique', 'climat': 'tempere', 'description': 'Sucrée, fondante',
                 'saison': 'Octobre-Novembre', 'jours': 170},
                {'nom': 'Abate Fetel', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Allongée, sucrée',
                 'saison': 'Septembre-Octobre', 'jours': 155},
            ],
            'Cerise': [
                {'nom': 'Bigarreau', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Rouge foncé, sucrée', 'saison': 'Juin-Juillet', 'jours': 90},
                {'nom': 'Griotte', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Petite, acide',
                 'saison': 'Juillet-Août', 'jours': 85},
                {'nom': 'Burlat', 'zones': 'Europe,Amérique', 'climat': 'tempere', 'description': 'Précoce, rouge',
                 'saison': 'Mai-Juin', 'jours': 75},
                {'nom': 'Maraska', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Pour kirsch',
                 'saison': 'Juillet', 'jours': 85},
            ],
            'Pêche': [
                {'nom': 'Pêche de vigne', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Blanche, parfumée',
                 'saison': 'Juillet-Août', 'jours': 120},
                {'nom': 'Reine des vergers', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Jaune, sucrée',
                 'saison': 'Juillet-Août', 'jours': 115},
                {'nom': 'Springcrest', 'zones': 'Europe,Amérique', 'climat': 'tempere',
                 'description': 'Précoce, sucrée', 'saison': 'Juin-Juillet', 'jours': 100},
                {'nom': 'Redhaven', 'zones': 'Europe,Amérique', 'climat': 'tempere', 'description': 'Rouge, sucrée',
                 'saison': 'Juillet-Août', 'jours': 110},
            ],
            'Abricot': [
                {'nom': 'Rouge du Roussillon', 'zones': 'Europe', 'climat': 'mediterraneen',
                 'description': 'Rouge, parfumé', 'saison': 'Juin-Juillet', 'jours': 90},
                {'nom': 'Bergeron', 'zones': 'Europe', 'climat': 'mediterraneen', 'description': 'Jaune, sucré',
                 'saison': 'Juillet-Août', 'jours': 95},
                {'nom': 'Goldrich', 'zones': 'Europe,Amérique', 'climat': 'mediterraneen', 'description': 'Gros, sucré',
                 'saison': 'Juillet-Août', 'jours': 100},
            ],
            'Prune': [
                {'nom': 'Reine Claude', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Verte, sucrée',
                 'saison': 'Août-Septembre', 'jours': 110},
                {'nom': 'Mirabelle', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Petite, sucrée',
                 'saison': 'Août-Septembre', 'jours': 100},
                {'nom': 'Quetsche', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Violette, pour tarte',
                 'saison': 'Septembre', 'jours': 115},
                {'nom': 'D\'Agen', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Sèche (pruneau)',
                 'saison': 'Septembre', 'jours': 120},
            ],
            'Fraise': [
                {'nom': 'Gariguette', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Précoce, parfumée',
                 'saison': 'Avril-Mai', 'jours': 60},
                {'nom': 'Mara des Bois', 'zones': 'Europe', 'climat': 'tempere',
                 'description': 'Parfumée, goût de fraise des bois', 'saison': 'Mai-Juin', 'jours': 65},
                {'nom': 'Charlotte', 'zones': 'Europe,Amérique', 'climat': 'tempere', 'description': 'Grosse, sucrée',
                 'saison': 'Juin', 'jours': 70},
                {'nom': 'Ciflorette', 'zones': 'Europe', 'climat': 'tempere', 'description': 'Allongée, sucrée',
                 'saison': 'Mai', 'jours': 55},
                {'nom': 'Albion', 'zones': 'Amérique,Europe', 'climat': 'tempere', 'description': 'Grosse, sucrée',
                 'saison': 'Juillet-Août', 'jours': 75},
                {'nom': 'Chandler', 'zones': 'Amérique,Europe', 'climat': 'tempere', 'description': 'Grosse, sucrée',
                 'saison': 'Juin-Juillet', 'jours': 70},
            ],
            'Raisin': [
                {'nom': 'Chardonnay', 'zones': 'Europe,Amérique', 'climat': 'mediterraneen', 'description': 'Pour vin',
                 'saison': 'Septembre-Octobre', 'jours': 180},
                {'nom': 'Merlot', 'zones': 'Europe,Amérique', 'climat': 'mediterraneen', 'description': 'Pour vin',
                 'saison': 'Septembre-Octobre', 'jours': 185},
                {'nom': 'Cabernet', 'zones': 'Europe,Amérique', 'climat': 'mediterraneen', 'description': 'Pour vin',
                 'saison': 'Octobre', 'jours': 190},
                {'nom': 'Muscat', 'zones': 'Europe,Amérique', 'climat': 'mediterraneen', 'description': 'Parfumé',
                 'saison': 'Août-Septembre', 'jours': 170},
                {'nom': 'Thompson Seedless', 'zones': 'Amérique,Europe', 'climat': 'mediterraneen',
                 'description': 'Blanc, sans pépins', 'saison': 'Août-Septembre', 'jours': 160},
                {'nom': 'Red Globe', 'zones': 'Amérique,Europe', 'climat': 'mediterraneen',
                 'description': 'Rouge, gros', 'saison': 'Septembre-Octobre', 'jours': 175},
            ],
            'Figue': [
                {'nom': 'Brown Turkey', 'zones': 'Europe,Amérique,Asie', 'climat': 'mediterraneen',
                 'description': 'Marron, sucrée', 'saison': 'Août-Septembre', 'jours': 180},
                {'nom': 'Black Mission', 'zones': 'Europe,Amérique', 'climat': 'mediterraneen',
                 'description': 'Noire, très sucrée', 'saison': 'Août-Septembre', 'jours': 185},
                {'nom': 'Figue de Solliès', 'zones': 'Europe', 'climat': 'mediterraneen',
                 'description': 'Violette, parfumée', 'saison': 'Août-Septembre', 'jours': 170},
            ],
            'Olive': [
                {'nom': 'Lucques', 'zones': 'Europe', 'climat': 'mediterraneen', 'description': 'Verte, douce',
                 'saison': 'Octobre-Novembre', 'jours': 365},
                {'nom': 'Nyons', 'zones': 'Europe', 'climat': 'mediterraneen', 'description': 'Noire, fruitée',
                 'saison': 'Novembre-Décembre', 'jours': 365},
                {'nom': 'Picholine', 'zones': 'Europe', 'climat': 'mediterraneen', 'description': 'Verte, croquante',
                 'saison': 'Octobre-Novembre', 'jours': 365},
                {'nom': 'Kalamata', 'zones': 'Europe', 'climat': 'mediterraneen', 'description': 'Noire, salée',
                 'saison': 'Octobre-Novembre', 'jours': 365},
            ],
            # === OCÉANIE ===
            'Kiwi': [
                {'nom': 'Hayward', 'zones': 'Océanie,Europe,Amérique', 'climat': 'tempere',
                 'description': 'Vert, le plus commun', 'saison': 'Novembre-Janvier', 'jours': 240},
                {'nom': 'Zespri Gold', 'zones': 'Océanie,Europe', 'climat': 'tempere', 'description': 'Jaune, doux',
                 'saison': 'Novembre-Janvier', 'jours': 220},
                {'nom': 'SunGold', 'zones': 'Océanie', 'climat': 'tempere', 'description': 'Jaune, très sucré',
                 'saison': 'Novembre-Janvier', 'jours': 230},
            ],
            'Macadamia': [
                {'nom': 'Macadamia', 'zones': 'Océanie,Afrique', 'climat': 'sub-tropical',
                 'description': 'Noix, grasse', 'saison': 'Mai-Juin', 'jours': 365},
            ],
        }

        total_importes = 0

        for culture_nom, varietes in varietes_data.items():
            culture, created = Culture.objects.get_or_create(
                nom=culture_nom,
                defaults={'emoji': '🌱'}
            )

            if created:
                self.stdout.write(f"✅ Culture créée : {culture_nom}")

            for data in varietes:
                variete, created = Variete.objects.get_or_create(
                    culture=culture,
                    nom=data['nom'],
                    defaults={
                        'description': data.get('description', ''),
                        'zones_geographiques': data.get('zones', ''),
                        'climat': data.get('climat', ''),
                        'saison': data.get('saison', ''),
                        'jours_recolte': data.get('jours', None),
                    }
                )

                if created:
                    total_importes += 1
                    self.stdout.write(f" ✅ Variété importée : {variete.nom} ({culture_nom})")
                else:
                    self.stdout.write(f" ⏭️ Variété déjà existante : {variete.nom}")

        self.stdout.write(self.style.SUCCESS(f"\n🎉 {total_importes} variété(s) importée(s) avec succès !"))