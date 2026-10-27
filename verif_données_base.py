from vegetables_fruits.models import AssociationCulture, MaladieCulture, Culture, Fruit, Vegetable

print("=== CULTURES ===")
print(f"Cultures: {Culture.objects.count()}")
for c in Culture.objects.all()[:5]:
    print(f"  - {c.nom}")

print("\n=== FRUITS ===")
print(f"Fruits: {Fruit.objects.count()}")
for f in Fruit.objects.all()[:5]:
    print(f"  - {f.nom}")

print("\n=== LÉGUMES ===")
print(f"Légumes: {Vegetable.objects.count()}")
for v in Vegetable.objects.all()[:5]:
    print(f"  - {v.nom}")

print("\n=== ASSOCIATIONS ===")
print(f"Associations: {AssociationCulture.objects.count()}")
for a in AssociationCulture.objects.all():
    print(f"  - {a.culture1} ↔ {a.culture2} ({a.type_association})")

print("\n=== MALADIES ===")
print(f"Maladies: {MaladieCulture.objects.count()}")
for m in MaladieCulture.objects.all():
    print(f"  - {m.nom} → {m.cultures_cibles}")