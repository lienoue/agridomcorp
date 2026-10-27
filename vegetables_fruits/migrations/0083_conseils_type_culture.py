from django.db import migrations, models


def creer_conseils_defaut(apps, schema_editor):
    ConseilsTypeCulture = apps.get_model('vegetables_fruits', 'ConseilsTypeCulture')

    ConseilsTypeCulture.objects.get_or_create(
        type_culture='arbre_fruitier',
        defaults={
            'emoji': '🌳',
            'conseils_plantation': "Plantez les arbres à racines nues en automne-hiver (hors gel), ou en conteneur au printemps.",
            'conseils_arrosage': "Arrosez copieusement les 2 premières années. Ensuite, arrosez uniquement en cas de forte sécheresse.",
            'conseils_protection': "Taillez en hiver pour aérer la ramure. Surveillez les pucerons et la tavelure au printemps.",
            'conseils_fertilisation': "Apportez du compost en automne. Évitez les engrais trop riches en azote.",
        }
    )
    ConseilsTypeCulture.objects.get_or_create(
        type_culture='arbuste_fruitier',
        defaults={
            'emoji': '🌿',
            'conseils_plantation': "Plantez en automne ou au début du printemps. Espacez les plants de 1m à 1m50.",
            'conseils_arrosage': "Arrosez régulièrement, le système racinaire est superficiel. Paillez pour garder l'humidité.",
            'conseils_protection': "Taillez après la récolte. Protégez les fruits des oiseaux avec un filet.",
            'conseils_fertilisation': "Apportez un engrais riche en potassium au printemps pour favoriser la fructification.",
        }
    )
    ConseilsTypeCulture.objects.get_or_create(
        type_culture='legume_feuille',
        defaults={
            'emoji': '🥬',
            'conseils_plantation': "Semez ou plantez au printemps ou à l'automne selon la variété.",
            'conseils_arrosage': "Arrosez régulièrement pour éviter la montée en graines (surtout en été).",
            'conseils_fertilisation': "Apportez un engrais riche en azote pour favoriser le développement des feuilles.",
        }
    )
    ConseilsTypeCulture.objects.get_or_create(
        type_culture='legume_racine',
        defaults={
            'emoji': '🥕',
            'conseils_plantation': "Semez directement en pleine terre, évitez le repiquage.",
            'conseils_arrosage': "Arrosez en pluie fine et régulièrement pour éviter que les racines ne se fendent.",
            'conseils_fertilisation': "Évitez l'azote qui fait pousser les feuilles au détriment de la racine. Apportez du compost bien décomposé.",
        }
    )
    ConseilsTypeCulture.objects.get_or_create(
        type_culture='legume_fruit',
        defaults={
            'emoji': '🍅',
            'conseils_plantation': "Plantez après les dernières gelées, en plein soleil.",
            'conseils_arrosage': "Arrosez au pied, abondamment mais espacé, pour éviter le mildiou.",
            'conseils_fertilisation': "Apportez un engrais riche en potassium pendant la floraison et la fructification.",
        }
    )


class Migration(migrations.Migration):
    dependencies = [
        ('vegetables_fruits', '0082_tauxchange_customuser_devise_preferee'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConseilsTypeCulture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_culture', models.CharField(
                    choices=[('arbre_fruitier', '🌳 Arbre fruitier'), ('arbuste_fruitier', '🌿 Arbuste fruitier (baies)'),
                             ('legume_feuille', '🥬 Légume-feuille'), ('legume_racine', '🥕 Légume-racine'),
                             ('legume_fruit', '🍅 Légume-fruit'), ('legume_bulbe', '🧅 Légume-bulbe'),
                             ('aromatique', '🌿 Aromatique'), ('cereale', '🌾 Céréale'), ('fleur', '🌸 Fleur')],
                    max_length=50, unique=True, verbose_name='Type de culture')),
                ('emoji', models.CharField(default='🌱', max_length=10)),
                ('temperature_min', models.IntegerField(blank=True, null=True)),
                ('temperature_optimale_min', models.IntegerField(blank=True, null=True)),
                ('temperature_optimale_max', models.IntegerField(blank=True, null=True)),
                ('temperature_max', models.IntegerField(blank=True, null=True)),
                ('duree_culture_min_jours', models.IntegerField(blank=True, null=True)),
                ('duree_culture_max_jours', models.IntegerField(blank=True, null=True)),
                ('methode_plantation', models.CharField(blank=True, max_length=50)),
                ('hivernage', models.CharField(blank=True, max_length=50)),
                ('conseils_climat', models.TextField(blank=True)),
                ('conseils_plantation', models.TextField(blank=True)),
                ('conseils_arrosage', models.TextField(blank=True)),
                ('conseils_fertilisation', models.TextField(blank=True)),
                ('conseils_protection', models.TextField(blank=True)),
                ('conseils_recolte', models.TextField(blank=True)),
                ('conseils_conservation', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Conseils par type de culture',
                'verbose_name_plural': 'Conseils par type de culture',
            },
        ),
        migrations.RunPython(creer_conseils_defaut),
    ]
