"""
Initialise les rendements de référence pour ~80 cultures.
Usage : python manage.py seed_rendements
Idempotent : ne remplace pas les valeurs existantes modifiées à la main.
"""
from django.core.management.base import BaseCommand
from vegetables_fruits.models import RendementCulture


RENDEMENTS = [
    # (nom, kg/plant, région, source)
    # ===== LÉGUMES-FRUITS =====
    ('tomate', 2.5, 'tous', 'fao'),
    ('tomate cerise', 1.8, 'tous', 'estimation'),
    ('courgette', 3.0, 'tous', 'fao'),
    ('concombre', 2.5, 'tous', 'fao'),
    ('cornichon', 1.5, 'tous', 'estimation'),
    ('aubergine', 1.8, 'tous', 'fao'),
    ('poivron', 1.2, 'tous', 'fao'),
    ('piment', 0.3, 'tous', 'estimation'),
    ('melon', 2.0, 'tous', 'fao'),
    ('pastèque', 4.0, 'tous', 'fao'),
    ('potiron', 5.0, 'tous', 'fao'),
    ('citrouille', 5.0, 'tous', 'fao'),
    ('courge', 4.5, 'tous', 'fao'),

    # ===== LÉGUMES-FEUILLES =====
    ('salade', 0.4, 'tous', 'fao'),
    ('laitue', 0.4, 'tous', 'fao'),
    ('mâche', 0.15, 'tous', 'estimation'),
    ('épinard', 0.3, 'tous', 'fao'),
    ('blette', 0.8, 'tous', 'estimation'),
    ('chou', 1.5, 'tous', 'fao'),
    ('chou-fleur', 1.2, 'tous', 'fao'),
    ('brocoli', 0.8, 'tous', 'fao'),
    ('chou de bruxelles', 0.6, 'tous', 'fao'),
    ('roquette', 0.15, 'tous', 'estimation'),
    ('cresson', 0.1, 'tous', 'estimation'),
    ('persil', 0.1, 'tous', 'estimation'),
    ('ciboulette', 0.08, 'tous', 'estimation'),
    ('basilic', 0.15, 'tous', 'estimation'),
    ('coriandre', 0.08, 'tous', 'estimation'),
    ('menthe', 0.2, 'tous', 'estimation'),
    ('thym', 0.05, 'tous', 'estimation'),
    ('romarin', 0.08, 'tous', 'estimation'),
    ('sauge', 0.1, 'tous', 'estimation'),
    ('origan', 0.08, 'tous', 'estimation'),
    ('aneth', 0.06, 'tous', 'estimation'),
    ('estragon', 0.08, 'tous', 'estimation'),

    # ===== LÉGUMES-RACINES =====
    ('carotte', 0.15, 'tous', 'fao'),
    ('pomme de terre', 1.2, 'tous', 'fao'),
    ('patate douce', 1.5, 'tous', 'fao'),
    ('betterave', 0.4, 'tous', 'fao'),
    ('radis', 0.02, 'tous', 'estimation'),
    ('radis noir', 0.15, 'tous', 'estimation'),
    ('navet', 0.3, 'tous', 'fao'),
    ('panais', 0.25, 'tous', 'fao'),
    ('céleri', 0.8, 'tous', 'fao'),
    ('céleri-rave', 0.6, 'tous', 'fao'),
    ('topinambour', 1.5, 'tous', 'estimation'),
    ('salsifis', 0.2, 'tous', 'estimation'),
    ('rutabaga', 0.5, 'tous', 'fao'),

    # ===== LÉGUMES-BULBES =====
    ('oignon', 0.15, 'tous', 'fao'),
    ('oignon rouge', 0.15, 'tous', 'fao'),
    ('ail', 0.05, 'tous', 'fao'),
    ('échalote', 0.08, 'tous', 'fao'),
    ('poireau', 0.25, 'tous', 'fao'),

    # ===== LÉGUMINEUSES =====
    ('haricot', 0.5, 'tous', 'fao'),
    ('haricot vert', 0.4, 'tous', 'fao'),
    ('petit pois', 0.3, 'tous', 'fao'),
    ('pois chiche', 0.2, 'tous', 'fao'),
    ('fève', 0.5, 'tous', 'fao'),
    ('lentille', 0.1, 'tous', 'fao'),

    # ===== FRUITS ROUGES =====
    ('fraise', 0.3, 'tous', 'fao'),
    ('framboise', 0.5, 'tous', 'fao'),
    ('myrtille', 0.8, 'tous', 'fao'),
    ('groseille', 0.7, 'tous', 'fao'),
    ('cassis', 0.6, 'tous', 'fao'),
    ('mûre', 1.0, 'tous', 'estimation'),

    # ===== FRUITS À NOYAU =====
    ('pêche', 15.0, 'tous', 'fao'),
    ('nectarine', 15.0, 'tous', 'fao'),
    ('abricot', 12.0, 'tous', 'fao'),
    ('cerise', 8.0, 'tous', 'fao'),
    ('prune', 10.0, 'tous', 'fao'),
    ('mirabelle', 10.0, 'tous', 'fao'),

    # ===== FRUITS À PÉPINS =====
    ('pomme', 20.0, 'tous', 'fao'),
    ('poire', 18.0, 'tous', 'fao'),
    ('coing', 12.0, 'tous', 'fao'),

    # ===== AGRUMES =====
    ('orange', 25.0, 'mediterraneen', 'fao'),
    ('citron', 20.0, 'mediterraneen', 'fao'),
    ('mandarine', 20.0, 'mediterraneen', 'fao'),
    ('pamplemousse', 25.0, 'mediterraneen', 'fao'),
    ('kiwi', 15.0, 'tous', 'fao'),

    # ===== FRUITS EXOTIQUES =====
    ('ananas', 1.5, 'tropical', 'fao'),
    ('banane', 15.0, 'tropical', 'fao'),
    ('mangue', 30.0, 'tropical', 'fao'),
    ('avocat', 20.0, 'tropical', 'fao'),

    # ===== AROMATIQUES GRANDES =====
    ('lavande', 0.05, 'mediterraneen', 'estimation'),
    ('olivier', 8.0, 'mediterraneen', 'fao'),
    ('figuier', 15.0, 'mediterraneen', 'fao'),
    ('vigne', 3.0, 'tous', 'fao'),
    ('raisin', 3.0, 'tous', 'fao'),
]


class Command(BaseCommand):
    help = "Initialise les rendements de référence pour ~80 cultures"

    def handle(self, *args, **options):
        crees = 0
        ignores = 0

        for nom, rendement, region, source in RENDEMENTS:
            obj, created = RendementCulture.objects.get_or_create(
                culture_nom=nom,
                region_climatique=region,
                defaults={
                    'rendement_kg_par_plant': rendement,
                    'source': source,
                }
            )
            if created:
                crees += 1
            else:
                ignores += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ {crees} rendements créés, {ignores} déjà existants (ignorés)"
        ))
