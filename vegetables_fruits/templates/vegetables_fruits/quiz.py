from vegetables_fruits.models import QuestionQuiz

questions = [
    # ==================== LÉGUMES (20 questions) ====================
    {
        'question': 'Quelle plante fixe l\'azote dans le sol ?',
        'choix_1': 'Tomate',
        'choix_2': 'Haricot',
        'choix_3': 'Carotte',
        'choix_4': 'Salade',
        'bonne_reponse': 2,
        'explication': 'Les légumineuses (haricots, pois) fixent l\'azote grâce à des bactéries symbiotiques.'
    },
    {
        'question': 'Quel légume est le plus riche en vitamine C ?',
        'choix_1': 'Pomme de terre',
        'choix_2': 'Poivron',
        'choix_3': 'Oignon',
        'choix_4': 'Ail',
        'bonne_reponse': 2,
        'explication': 'Le poivron rouge contient plus de vitamine C qu\'une orange !'
    },
    {
        'question': 'Quelle est la saison des fraises ?',
        'choix_1': 'Printemps',
        'choix_2': 'Été',
        'choix_3': 'Automne',
        'choix_4': 'Hiver',
        'bonne_reponse': 1,
        'explication': 'Les fraises sont à leur meilleur au printemps (mai-juin).'
    },
    {
        'question': 'Quel légume se récolte en hiver ?',
        'choix_1': 'Courgette',
        'choix_2': 'Poireau',
        'choix_3': 'Tomate',
        'choix_4': 'Haricot',
        'bonne_reponse': 2,
        'explication': 'Le poireau est un légume d\'hiver très rustique.'
    },
    {
        'question': 'La carotte est-elle un légume-racine ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'La carotte est effectivement un légume-racine, tout comme le radis ou le navet.'
    },
    {
        'question': 'Quel légume contient le plus de potassium ?',
        'choix_1': 'Tomate',
        'choix_2': 'Pomme de terre',
        'choix_3': 'Courgette',
        'choix_4': 'Salade',
        'bonne_reponse': 2,
        'explication': 'La pomme de terre est très riche en potassium, plus qu\'une banane !'
    },
    {
        'question': 'L\'aubergine est-elle un fruit ou un légume ?',
        'choix_1': 'Fruit',
        'choix_2': 'Légume',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Botaniquement, l\'aubergine est un fruit (une baie).'
    },
    {
        'question': 'Quelle est la meilleure période pour semer les tomates ?',
        'choix_1': 'Janvier',
        'choix_2': 'Février-mars',
        'choix_3': 'Avril-mai',
        'choix_4': 'Juin-juillet',
        'bonne_reponse': 3,
        'explication': 'Les tomates se sèment en avril-mai, après les dernières gelées.'
    },
    {
        'question': 'Quel légume est une source de bêta-carotène ?',
        'choix_1': 'Carotte',
        'choix_2': 'Concombre',
        'choix_3': 'Céleri',
        'choix_4': 'Radis',
        'bonne_reponse': 1,
        'explication': 'La carotte est célèbre pour sa richesse en bêta-carotène (provitamine A).'
    },
    {
        'question': 'La courgette est-elle un fruit ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Botaniquement, la courgette est un fruit (c\'est une baie).'
    },
    {
        'question': 'Quelle plante est toxique pour les chats ?',
        'choix_1': 'Basilic',
        'choix_2': 'Menthe',
        'choix_3': 'Oignon',
        'choix_4': 'Persil',
        'bonne_reponse': 3,
        'explication': 'L\'oignon est toxique pour les chats (et les chiens).'
    },
    {
        'question': 'Le chou-fleur est-il une fleur ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Le chou-fleur est composé de bourgeons floraux immatures.'
    },
    {
        'question': 'Quelle est la température idéale pour semer les haricots ?',
        'choix_1': '5°C',
        'choix_2': '10°C',
        'choix_3': '15°C',
        'choix_4': '20°C',
        'bonne_reponse': 3,
        'explication': 'Les haricots germent à partir de 15°C (sol réchauffé).'
    },
    {
        'question': 'Quel légume se mange cru ou cuit ?',
        'choix_1': 'Pomme de terre',
        'choix_2': 'Aubergine',
        'choix_3': 'Carotte',
        'choix_4': 'Haricot vert',
        'bonne_reponse': 3,
        'explication': 'La carotte se mange crue (râpée) ou cuite.'
    },
    {
        'question': 'Quelle est la durée de pousse d\'un radis ?',
        'choix_1': '15 jours',
        'choix_2': '30 jours',
        'choix_3': '45 jours',
        'choix_4': '60 jours',
        'bonne_reponse': 2,
        'explication': 'Un radis peut être récolté en 3 à 4 semaines.'
    },
    {
        'question': 'L\'asperge est-elle une tige ou une racine ?',
        'choix_1': 'Tige',
        'choix_2': 'Racine',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'L\'asperge est une tige souterraine qui émerge du sol.'
    },
    {
        'question': 'Quel légume est un fruit séché ?',
        'choix_1': 'Pois chiche',
        'choix_2': 'Haricot vert',
        'choix_3': 'Lentille',
        'choix_4': 'Arachide',
        'bonne_reponse': 4,
        'explication': 'L\'arachide (cacahuète) est une légumineuse, souvent appelée fruit sec.'
    },
    {
        'question': 'Quelle est la saison des choux ?',
        'choix_1': 'Printemps',
        'choix_2': 'Été',
        'choix_3': 'Automne-hiver',
        'choix_4': 'Toute l\'année',
        'bonne_reponse': 3,
        'explication': 'Les choux se récoltent en automne et en hiver.'
    },
    {
        'question': 'Le fenouil a-t-il un goût d\'anis ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Le fenouil a une saveur anisée caractéristique.'
    },
    {
        'question': 'Quelle plante est utilisée comme engrais vert ?',
        'choix_1': 'Tomate',
        'choix_2': 'Moutarde',
        'choix_3': 'Carotte',
        'choix_4': 'Salade',
        'bonne_reponse': 2,
        'explication': 'La moutarde est souvent utilisée comme engrais vert.'
    },

    # ==================== FRUITS (20 questions) ====================
    {
        'question': 'Quel fruit est en fait une baie ?',
        'choix_1': 'Pomme',
        'choix_2': 'Tomate',
        'choix_3': 'Fraise',
        'choix_4': 'Pêche',
        'bonne_reponse': 3,
        'explication': 'La fraise est un faux-fruit ; les vrais fruits sont les petits akènes.'
    },
    {
        'question': 'L\'avocat est-il un fruit ou un légume ?',
        'choix_1': 'Fruit',
        'choix_2': 'Légume',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'L\'avocat est un fruit (il contient un noyau).'
    },
    {
        'question': 'Quel fruit est le plus riche en vitamine C ?',
        'choix_1': 'Kiwi',
        'choix_2': 'Orange',
        'choix_3': 'Citron',
        'choix_4': 'Goyave',
        'bonne_reponse': 4,
        'explication': 'La goyave est l\'un des fruits les plus riches en vitamine C.'
    },
    {
        'question': 'Quelle est la saison des pommes ?',
        'choix_1': 'Printemps',
        'choix_2': 'Été',
        'choix_3': 'Automne',
        'choix_4': 'Hiver',
        'bonne_reponse': 3,
        'explication': 'Les pommes se récoltent en automne (septembre-octobre).'
    },
    {
        'question': 'Le citron est-il un agrume ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Le citron fait partie des agrumes.'
    },
    {
        'question': 'Quel fruit se conserve le plus longtemps ?',
        'choix_1': 'Fraise',
        'choix_2': 'Banane',
        'choix_3': 'Pomme',
        'choix_4': 'Pêche',
        'bonne_reponse': 3,
        'explication': 'La pomme se conserve plusieurs mois en chambre froide.'
    },
    {
        'question': 'Quelle est la meilleure période pour tailler la vigne ?',
        'choix_1': 'Printemps',
        'choix_2': 'Été',
        'choix_3': 'Automne',
        'choix_4': 'Hiver',
        'bonne_reponse': 4,
        'explication': 'La vigne se taille en hiver (en repos végétatif).'
    },
    {
        'question': 'Le kiwi est-il un fruit exotique ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Le kiwi est originaire de Chine, c\'est un fruit exotique.'
    },
    {
        'question': 'Quel fruit contient le plus de potassium ?',
        'choix_1': 'Banane',
        'choix_2': 'Pomme',
        'choix_3': 'Orange',
        'choix_4': 'Poire',
        'bonne_reponse': 1,
        'explication': 'La banane est très riche en potassium.'
    },
    {
        'question': 'La cerise est-elle une drupe ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'La cerise est une drupe (fruit à noyau).'
    },
    {
        'question': 'Quelle est la saison des agrumes ?',
        'choix_1': 'Printemps',
        'choix_2': 'Été',
        'choix_3': 'Automne',
        'choix_4': 'Hiver',
        'bonne_reponse': 4,
        'explication': 'Les agrumes sont principalement des fruits d\'hiver.'
    },
    {
        'question': 'Le fruit de la passion vient-il d\'une liane ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Le fruit de la passion pousse sur une liane tropicale.'
    },
    {
        'question': 'L\'abricot est-il apparenté à la pêche ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Abricot et pêche appartiennent tous deux au genre Prunus.'
    },
    {
        'question': 'Quelle est la durée de conservation des fraises ?',
        'choix_1': '1-2 jours',
        'choix_2': '1 semaine',
        'choix_3': '2 semaines',
        'choix_4': '1 mois',
        'bonne_reponse': 1,
        'explication': 'Les fraises se conservent 1 à 2 jours au réfrigérateur.'
    },
    {
        'question': 'Le raisin se récolte-t-il en septembre ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'En France, les vendanges ont lieu en septembre-octobre.'
    },
    {
        'question': 'Le pamplemousse est-il un hybride ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Le pamplemousse est un hybride de pomélo et d\'orange douce.'
    },
    {
        'question': 'Quelle est la taille d\'un pommier adulte ?',
        'choix_1': '1-2 m',
        'choix_2': '2-4 m',
        'choix_3': '4-8 m',
        'choix_4': '8-12 m',
        'bonne_reponse': 3,
        'explication': 'Un pommier adulte peut atteindre 4 à 8 mètres.'
    },
    {
        'question': 'Le melon est-il une courge ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Le melon fait partie de la famille des cucurbitacées (courges).'
    },
    {
        'question': 'La pastèque est-elle composée à 90% d\'eau ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'La pastèque est composée à environ 92% d\'eau.'
    },
    {
        'question': 'Quelle est la meilleure période pour planter un pommier ?',
        'choix_1': 'Printemps',
        'choix_2': 'Automne',
        'choix_3': 'Été',
        'choix_4': 'Hiver',
        'bonne_reponse': 2,
        'explication': 'L\'automne est la meilleure période pour planter les arbres fruitiers.'
    },

    # ==================== POLLINISATION & JARDINAGE (20 questions) ====================
    {
        'question': 'Quel insecte est le plus important pollinisateur ?',
        'choix_1': 'Papillon',
        'choix_2': 'Abeille',
        'choix_3': 'Coccinelle',
        'choix_4': 'Guêpe',
        'bonne_reponse': 2,
        'explication': 'L\'abeille domestique est le pollinisateur le plus important.'
    },
    {
        'question': 'Quelle plante attire les pollinisateurs ?',
        'choix_1': 'Lavande',
        'choix_2': 'Tomate',
        'choix_3': 'Pomme de terre',
        'choix_4': 'Salade',
        'bonne_reponse': 1,
        'explication': 'La lavande est très attractive pour les abeilles.'
    },
    {
        'question': 'La pollinisation est-elle nécessaire pour les tomates ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Les tomates ont besoin de pollinisation (par le vent ou les insectes).'
    },
    {
        'question': 'Quel arbre est pollinisé par le vent ?',
        'choix_1': 'Pommier',
        'choix_2': 'Chêne',
        'choix_3': 'Cerisier',
        'choix_4': 'Abricotier',
        'bonne_reponse': 2,
        'explication': 'Le chêne est pollinisé par le vent (anémophile).'
    },
    {
        'question': 'Quelle plante est auto-pollinisatrice ?',
        'choix_1': 'Pomme',
        'choix_2': 'Tomate',
        'choix_3': 'Poire',
        'choix_4': 'Cerise',
        'bonne_reponse': 2,
        'explication': 'La tomate est auto-pollinisatrice (fleurs hermaphrodites).'
    },
    {
        'question': 'Le compagnonnage est-il bénéfique pour le jardin ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Le compagnonnage aide à repousser les nuisibles et à améliorer la croissance.'
    },
    {
        'question': 'Quelle association est bénéfique au potager ?',
        'choix_1': 'Tomate + basilic',
        'choix_2': 'Carotte + aneth',
        'choix_3': 'Haricot + oignon',
        'choix_4': 'Courgette + pomme de terre',
        'bonne_reponse': 1,
        'explication': 'Tomate et basilic s\'associent bien (le basilic repousse les insectes).'
    },
    {
        'question': 'La rotation des cultures permet-elle d\'éviter les maladies ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'La rotation limite les maladies et l\'épuisement du sol.'
    },
    {
        'question': 'Quel engrais est naturel ?',
        'choix_1': 'Compost',
        'choix_2': 'Engrais chimique',
        'choix_3': 'Pesticide',
        'choix_4': 'Herbicide',
        'bonne_reponse': 1,
        'explication': 'Le compost est un engrais naturel issu de déchets organiques.'
    },
    {
        'question': 'Quelle est la fonction du paillage ?',
        'choix_1': 'Garder l\'humidité',
        'choix_2': 'Fertiliser',
        'choix_3': 'Désherber',
        'choix_4': 'Protéger du froid',
        'bonne_reponse': 1,
        'explication': 'Le paillage conserve l\'humidité du sol et limite les mauvaises herbes.'
    },
    {
        'question': 'Le purin d\'ortie est-il un engrais ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Le purin d\'ortie est un engrais naturel riche en azote.'
    },
    {
        'question': 'Quelle plante est une bonne compagne pour la carotte ?',
        'choix_1': 'Poireau',
        'choix_2': 'Tomate',
        'choix_3': 'Oignon',
        'choix_4': 'Persil',
        'bonne_reponse': 3,
        'explication': 'L\'oignon éloigne la mouche de la carotte.'
    },
    {
        'question': 'La bouillie bordelaise est-elle naturelle ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'La bouillie bordelaise est à base de sulfate de cuivre (autorisé en bio).'
    },
    {
        'question': 'Quelle est la meilleure période pour pailler ?',
        'choix_1': 'Printemps',
        'choix_2': 'Été',
        'choix_3': 'Automne',
        'choix_4': 'Hiver',
        'bonne_reponse': 1,
        'explication': 'Le paillage se fait au printemps pour garder l\'humidité.'
    },
    {
        'question': 'Le compost mature est-il prêt en 6 mois ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Un compost peut être mature en 6 à 12 mois.'
    },
    {
        'question': 'Quelle plante est invasive au potager ?',
        'choix_1': 'Menthe',
        'choix_2': 'Basilic',
        'choix_3': 'Persil',
        'choix_4': 'Thym',
        'bonne_reponse': 1,
        'explication': 'La menthe est très envahissante, il faut la planter en pot.'
    },
    {
        'question': 'Les vers de terre sont-ils utiles au jardin ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Les vers de terre aèrent le sol et améliorent sa fertilité.'
    },
    {
        'question': 'La cendre de bois est-elle un bon engrais ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'La cendre est riche en potassium et en calcium.'
    },
    {
        'question': 'Quelle est la meilleure période pour tailler les rosiers ?',
        'choix_1': 'Printemps',
        'choix_2': 'Été',
        'choix_3': 'Automne',
        'choix_4': 'Hiver',
        'bonne_reponse': 1,
        'explication': 'Les rosiers se taillent au printemps (mars).'
    },
    {
        'question': 'Le marc de café est-il bon pour le jardin ?',
        'choix_1': 'Oui',
        'choix_2': 'Non',
        'choix_3': '',
        'choix_4': '',
        'bonne_reponse': 1,
        'explication': 'Le marc de café enrichit le sol et repousse les limaces.'
    },
]

for q in questions:
    QuestionQuiz.objects.create(**q)