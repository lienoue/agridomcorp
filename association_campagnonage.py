from vegetables_fruits.models import AssociationCulture, MaladieCulture

# Associations
associations = [
    ("Tomate", "Basilic", "bonne"),
    ("Tomate", "Fenouil", "mauvaise"),
    ("Carotte", "Oignon", "bonne"),
    ("Carotte", "Aneth", "mauvaise"),
    ("Pomme de terre", "Tomate", "mauvaise"),
    ("Pomme de terre", "Haricot", "bonne"),
    ("Courgette", "Capucine", "bonne"),
    ("Courgette", "Pomme de terre", "mauvaise"),
    ("Salade", "Radis", "bonne"),
    ("Salade", "Fenouil", "mauvaise"),
    ("Fraise", "Ail", "bonne"),
    ("Fraise", "Chou", "mauvaise"),
    ("Haricot", "Tomate", "bonne"),
    ("Poireau", "Carotte", "bonne"),
    ("Poireau", "Haricot", "mauvaise"),
]

for c1, c2, type_assoc in associations:
    AssociationCulture.objects.get_or_create(
        culture1=c1,
        culture2=c2,
        defaults={'type_association': type_assoc, 'pays': 'tous'}
    )

# Maladies
maladies = [
    ("Mildiou", "🟤", "Tomate,Pomme de terre,Concombre", "elevee", 5),
    ("Oïdium", "⚪", "Courgette,Concombre,Fraise", "moyenne", 3),
    ("Pourriture grise", "🟢", "Fraise,Tomate,Courgette", "elevee", 7),
    ("Rouille", "🟠", "Haricot,Poireau", "moyenne", 4),
    ("Taches noires", "⬛", "Tomate,Pomme de terre", "faible", 2),
    ("Anthracnose", "🟣", "Haricot,Tomate", "elevee", 6),
    ("Feu bactérien", "🔥", "Pommier,Poire,Framboisier", "critique", 2),
]

for nom, emoji, cultures, gravite, delai in maladies:
    MaladieCulture.objects.get_or_create(
        nom=nom,
        defaults={
            'emoji': emoji,
            'cultures_cibles': cultures,
            'gravite': gravite,
            'delai_alerte_jours': delai,
            'description': f"Maladie {nom}",
            'traitement_curatif': f"Traitement curatif pour {nom}",
            'traitement_preventif': f"Traitement préventif pour {nom}",
        }
    )

print(f"✅ Associations: {AssociationCulture.objects.count()}")
print(f"✅ Maladies: {MaladieCulture.objects.count()}")