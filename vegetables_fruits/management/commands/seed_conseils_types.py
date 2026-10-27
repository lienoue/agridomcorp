from django.core.management.base import BaseCommand
from vegetables_fruits.models import ConseilsTypeCulture

CONSEILS_ENRICHIS = {
    'arbre_fruitier': {
        'emoji': '🌳',
        'temperature_min': -15,
        'temperature_optimale_min': 15,
        'temperature_optimale_max': 25,
        'temperature_max': 35,
        'duree_culture_min_jours': 365,
        'duree_culture_max_jours': 3650,
        'methode_plantation': 'plant',
        'hivernage': 'plein_air',
        'conseils_climat': "Les arbres fruitiers ont besoin d'une période de froid hivernal (vernalisation) pour bien fructifier l'année suivante.",
        'conseils_plantation': "Plantez à racines nues durant le repos végétatif (hiver). Creusez un trou 2 fois plus large que les racines. Tuteurez les jeunes plants. Espacez selon la vigueur (4 à 8 mètres).",
        'conseils_arrosage': "Arrosez copieusement les 2 premières années pour aider les racines à s'installer. Ensuite, l'arbre est résistant et n'a besoin d'eau qu'en cas de sécheresse prolongée. Évitez l'eau stagnante au pied.",
        'conseils_fertilisation': "Apportez du compost mûr en surface à l'automne. Évitez les engrais azotés en fin d'été qui fragilisent l'arbre face au gel.",
        'conseils_protection': "Taillez en hiver (hors périodes de gel) pour aérer le centre de l'arbre. Surveillez les pucerons au printemps et la tavelure. Badigeonnez le tronc à la chaux blanche pour éviter les coups de soleil et les insectes.",
        'conseils_recolte': "Cueillez les fruits à pleine maturité, en les faisant pivoter délicatement avec la main. Ne tirez pas pour ne pas casser les branches.",
        'conseils_conservation': "Conservez les pommes et poires dans un endroit frais, sombre et aéré (cave). Les fruits à noyau (pêches, abricots) se conservent très peu de temps et se congèlent bien."
    },
    'arbuste_fruitier': {
        'emoji': '🌿',
        'temperature_min': -10,
        'temperature_optimale_min': 12,
        'temperature_optimale_max': 22,
        'temperature_max': 30,
        'duree_culture_min_jours': 180,
        'duree_culture_max_jours': 365,
        'methode_plantation': 'plant',
        'hivernage': 'plein_air',
        'conseils_climat': "Les arbustes à petits fruits s'adaptent à de nombreux climats, mais redoutent les gelées printanières qui détruisent les fleurs.",
        'conseils_plantation': "Plantez à l'automne ou au début du printemps. Le système racinaire est superficiel, préparez un sol meuble et riche en matière organique. Paillez abondamment.",
        'conseils_arrosage': "Arrosez très régulièrement, surtout en été. Le sol ne doit jamais sécher complètement. Un goutte-à-goutte est idéal. Arrosez à la base pour éviter les maladies fongiques sur les feuilles.",
        'conseils_fertilisation': "Apportez du compost ou du fumier bien décomposé au printemps. Un engrais riche en potassium est bénéfique au moment de la formation des fruits.",
        'conseils_protection': "Taillez les vieilles branches pour rajeunir la plante. Installez des filets pour protéger les baies des oiseaux. Surveillez l'oïdium et les pucerons.",
        'conseils_recolte': "Cueillez délicatement car les fruits sont très fragiles. Pour les framboises et fraises, récoltez tous les 2 jours à pleine maturité.",
        'conseils_conservation': "Les baies sont très périssables. Consommez-les rapidement, congelez-les ou transformez-les en confitures."
    },
    'legume_feuille': {
        'emoji': '🥬',
        'temperature_min': 5,
        'temperature_optimale_min': 15,
        'temperature_optimale_max': 20,
        'temperature_max': 25,
        'duree_culture_min_jours': 30,
        'duree_culture_max_jours': 90,
        'methode_plantation': 'graine',
        'hivernage': 'plein_air',
        'conseils_climat': "Les légumes-feuilles préfèrent les climats frais et doux. La chaleur excessive (au-dessus de 25°C) les fait monter en graines (floraison) prématurément.",
        'conseils_plantation': "Semez directement en place ou repiquez de jeunes plants. La terre doit être fine et humide. Espacez de 20 à 30 cm selon la variété.",
        'conseils_arrosage': "L'arrosage est crucial. Un stress hydrique rend les feuilles amères ou les fait monter en graines. Arrosez régulièrement et en pluie fine pour ne pas déraciner les jeunes plants.",
        'conseils_fertilisation': "Ces légumes ont besoin d'azote pour produire de belles feuilles. Apportez du compost riche ou du purin d'ortie dilué toutes les 2 semaines.",
        'conseils_protection': "Protégez des limaces (cendre, barrières) et des altises. En été, installez un voile d'ombrage (type P17) pour rafraîchir les plants.",
        'conseils_recolte': "Récoltez au fur et à mesure des besoins. Coupez les feuilles extérieures en laissant le cœur pour que la plante continue de pousser. Récoltez le matin.",
        'conseils_conservation': "Se conservent quelques jours au réfrigérateur dans le bac à légumes, enveloppés dans un linge humide."
    },
    'legume_racine': {
        'emoji': '🥕',
        'temperature_min': 0,
        'temperature_optimale_min': 10,
        'temperature_optimale_max': 18,
        'temperature_max': 25,
        'duree_culture_min_jours': 60,
        'duree_culture_max_jours': 150,
        'methode_plantation': 'graine',
        'hivernage': 'plein_air',
        'conseils_climat': "Les légumes-racines aiment les climats tempérés. Un sol trop chaud ou trop sec fera durcir les racines et les rendra fibreuses.",
        'conseils_plantation': "Semez en ligne dans un sol profond, léger et sans cailloux (sinon les racines fourchent). Éclaircissez impérativement pour laisser de la place aux racines.",
        'conseils_arrosage': "Arrosez en pluie fine et régulièrement. Un manque d'eau ou un arrosage irrégulier fend les racines (ex: les carottes). N'inondez pas le sol.",
        'conseils_fertilisation': "Évitez l'azote frais qui fait pousser des feuilles au détriment de la racine. Privilégiez du compost bien mûr et de la cendre de bois (riche en potassium et phosphore).",
        'conseils_protection': "Protégez du froid intense en hiver avec un paillage. Surveillez la mouche de la carotte et le ver de la racine.",
        'conseils_recolte': "Arrachez avec une fourche-bêche. Beaucoup de racines (carottes, panais) sont meilleures après les premières gelées (le froid convertit l'amidon en sucre).",
        'conseils_conservation': "Conservez dans du sable sec et frais, ou dans le bas du réfrigérateur. Les betteraves et carottes se conservent plusieurs semaines."
    },
    'legume_fruit': {
        'emoji': '🍅',
        'temperature_min': 10,
        'temperature_optimale_min': 20,
        'temperature_optimale_max': 28,
        'temperature_max': 35,
        'duree_culture_min_jours': 60,
        'duree_culture_max_jours': 120,
        'methode_plantation': 'plant',
        'hivernage': 'plein_air',
        'conseils_climat': "Ces légumes sont très frileux (originaires des tropiques). Ils ont besoin de chaleur et de beaucoup de soleil. Ils gèlent à 0°C.",
        'conseils_plantation': "Plantez après la période des dernières gelées. Enterrez la tige jusqu'aux premières feuilles pour développer des racines solides. Tuteurez (tuteurs, cordes) pour éviter que les fruits ne touchent le sol.",
        'conseils_arrosage': "Arrosez uniquement au pied et abondamment (2 fois par semaine en été). Ne mouillez jamais les feuilles pour éviter le mildiou. La régularité évite que les fruits n'éclatent.",
        'conseils_fertilisation': "Très gourmands. Mettez du compost mûr au fond du trou. Utilisez un engrais riche en potassium pendant la floraison (purin de tomate, cendre).",
        'conseils_protection': "Pincez les gourmands (tomates) pour concentrer l'énergie. Surveillez le mildiou (taches brunes) et les pucerons. Retirez les feuilles malades.",
        'conseils_recolte': "Récoltez les fruits à pleine couleur, bien colorés et fermes. Cueillez régulièrement pour stimuler la production de nouveaux fruits.",
        'conseils_conservation': "Les tomates se conservent à température ambiante (jamais au frigo, ça détruit le goût). Les courges (potirons) se conservent plusieurs mois au sec."
    },
    'aromatique': {
        'emoji': '🌿',
        'temperature_min': -5,
        'temperature_optimale_min': 15,
        'temperature_optimale_max': 25,
        'temperature_max': 32,
        'duree_culture_min_jours': 60,
        'duree_culture_max_jours': 365,
        'methode_plantation': 'plant',
        'hivernage': 'plein_air',
        'conseils_climat': "La plupart des aromatiques méditerranéennes (thym, romarin) aiment le soleil et la sécheresse. Les aromatiques asiatiques (coriandre, basilic) préfèrent la fraîcheur.",
        'conseils_plantation': "Plantez dans un sol très bien drainé (surtout pour les plantes méditerranéennes). En pot, utilisez des billes d'argile au fond et de la terre mélangée à du sable.",
        'conseils_arrosage': "Arrosez modérément. Trop d'eau fait pourrir les racines (romarin, thym, sauge). Le basilic et la menthe sont plus gourmands en eau.",
        'conseils_fertilisation': "Un peu de compost suffit. Un excès d'engrais dilue le goût et l'arôme des plantes.",
        'conseils_protection': "Pincez les sommités régulièrement pour empêcher la floraison et favoriser la production de feuilles. Taillez après la floraison pour les vivaces.",
        'conseils_recolte': "Cueillez le matin, à la rosée, quand la concentration en huiles essentielles est la plus forte. Coupez une tige entière au-dessus d'un nœud.",
        'conseils_conservation': "Séchez les bouquets la tête en bas dans un endroit sombre. Conservez dans des bocaux hermétiques ou congelez les feuilles fraîches hachées dans des glaçons."
    },
    'cereale': {
        'emoji': '🌾',
        'temperature_min': 0,
        'temperature_optimale_min': 15,
        'temperature_optimale_max': 25,
        'temperature_max': 35,
        'duree_culture_min_jours': 90,
        'duree_culture_max_jours': 200,
        'methode_plantation': 'graine',
        'hivernage': 'plein_air',
        'conseils_climat': "Les céréales s'adaptent à de nombreux climats mais ont besoin de pleine lumière et d'un sol profond.",
        'conseils_plantation': "Semez à la volée ou en ligne dense, dans un sol bien préparé. Respectez la période de semis (automne pour le blé d'hiver, printemps pour le maïs).",
        'conseils_arrosage': "Les céréales ont besoin d'eau au moment de l'épiaison (formation des grains) et au remplissage. En dehors de ces périodes, elles sont résistantes.",
        'conseils_fertilisation': "Apportez un engrais azoté au démarrage (tallage) et un engrais potassique plus tard pour remplir les grains.",
        'conseils_protection': "Surveillez la rouille et les oiseaux (surtout pour le maïs et le sorgho). Tuteurez le maïs si votre climat est venteux.",
        'conseils_recolte': "Récoltez quand les épis sont secs et les grains durs. Coupez les tiges et battez les épis.",
        'conseils_conservation': "Conservez les grains dans un endroit sec et aéré, à l'abri des rongeurs (grenier, silo)."
    },
    'fleur': {
        'emoji': '🌸',
        'temperature_min': 5,
        'temperature_optimale_min': 15,
        'temperature_optimale_max': 25,
        'temperature_max': 32,
        'duree_culture_min_jours': 60,
        'duree_culture_max_jours': 180,
        'methode_plantation': 'graine',
        'hivernage': 'plein_air',
        'conseils_climat': "Les fleurs pollinisatrices attirent les abeilles et les papillons, essentiels à la pollinisation des fruits et légumes.",
        'conseils_plantation': "Semez ou plantez au printemps après les gelées, en plein soleil. Mélangez-les aux légumes.",
        'conseils_arrosage': "Arrosez régulièrement jusqu'à la levée. Ensuite, un arrosage 1 à 2 fois par semaine suffit.",
        'conseils_fertilisation': "Un apport de compost en automne suffit. Les fleurs sauvages n'ont pas besoin d'engrais.",
        'conseils_protection': "Surveillez les pucerons et les limaces. Ne traitez pas avec des insecticides (pour protéger les abeilles).",
        'conseils_recolte': "Coupez les fleurs fanées pour prolonger la floraison. Laissez quelques fleurs monter en graines à l'automne pour les oiseaux.",
        'conseils_conservation': "Les fleurs coupées se conservent dans l'eau fraîche. Les fleurs séchées se conservent en bouquet."
    }
}

class Command(BaseCommand):
    help = "Initialise les conseils par type de culture avec des données enrichies"

    def handle(self, *args, **options):
        crees = 0
        maj = 0

        for type_culture, data in CONSEILS_ENRICHIS.items():
            obj, created = ConseilsTypeCulture.objects.update_or_create(
                type_culture=type_culture,
                defaults=data
            )
            if created:
                crees += 1
            else:
                maj += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ {crees} créés, {maj} mis à jour. Total : {ConseilsTypeCulture.objects.count()}"
        ))