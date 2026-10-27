from vegetables_fruits.models import GeometricFigure
from vegetables_fruits.views import verifier_compatibilite_plantation

print("=== ÉTAPE 3 : TEST DE COMPATIBILITÉ ===")

# Récupérer une figure avec des cultures
figure = GeometricFigure.objects.filter(
    adresse_lat__isnull=False,
    crops__isnull=False
).first()

if not figure:
    print("❌ Aucune figure avec cultures trouvée")
    # Essayer de prendre la première figure et d'y ajouter des cultures
    figure = GeometricFigure.objects.first()
    if figure:
        figure.crops = [
            {'name': 'Tomate', 'emoji': '🍅'},
            {'name': 'Carotte', 'emoji': '🥕'}
        ]
        figure.save()
        print(f"✅ Cultures ajoutées à {figure.name}")
    else:
        print("❌ Aucune figure trouvée du tout")
        exit()

print(f"📌 Figure: {figure.name} (ID: {figure.id})")
print(f"📌 Cultures présentes: {figure.crops}")

# === SCÉNARIO 1 : Tomate près de Basilic (bonne association) ===
print("\n" + "="*50)
print("🔬 SCÉNARIO 1: Tomate près de Basilic")
print("="*50)
resultat = verifier_compatibilite_plantation("Basilic", figure.id)
print(f"Statut: {resultat['statut']}")
print(f"Compatible: {resultat['compatible']}")
print(f"Sensible: {resultat['sensible']}")
print(f"Message: {resultat['message']}")
print(f"Conseils: {resultat['conseils']}")

# === SCÉNARIO 2 : Tomate près de Fenouil (mauvaise association) ===
print("\n" + "="*50)
print("🔬 SCÉNARIO 2: Tomate près de Fenouil")
print("="*50)
resultat = verifier_compatibilite_plantation("Fenouil", figure.id)
print(f"Statut: {resultat['statut']}")
print(f"Compatible: {resultat['compatible']}")
print(f"Sensible: {resultat['sensible']}")
print(f"Message: {resultat['message']}")
print(f"Conseils: {resultat['conseils']}")

# === SCÉNARIO 3 : Pomme de terre près de Tomate avec Mildiou ===
print("\n" + "="*50)
print("🔬 SCÉNARIO 3: Pomme de terre près de Tomate avec Mildiou")
print("="*50)
resultat = verifier_compatibilite_plantation("Pomme de terre", figure.id, "Mildiou")
print(f"Statut: {resultat['statut']}")
print(f"Compatible: {resultat['compatible']}")
print(f"Sensible: {resultat['sensible']}")
print(f"Message: {resultat['message']}")
print(f"Conseils: {resultat['conseils']}")

# === SCÉNARIO 4 : Haricot près de Tomate (bonne association) ===
print("\n" + "="*50)
print("🔬 SCÉNARIO 4: Haricot près de Tomate")
print("="*50)
resultat = verifier_compatibilite_plantation("Haricot", figure.id)
print(f"Statut: {resultat['statut']}")
print(f"Compatible: {resultat['compatible']}")
print(f"Sensible: {resultat['sensible']}")
print(f"Message: {resultat['message']}")
print(f"Conseils: {resultat['conseils']}")

# === SCÉNARIO 5 : Poireau près de Carotte (bonne association) ===
print("\n" + "="*50)
print("🔬 SCÉNARIO 5: Poireau près de Carotte")
print("="*50)
resultat = verifier_compatibilite_plantation("Poireau", figure.id)
print(f"Statut: {resultat['statut']}")
print(f"Compatible: {resultat['compatible']}")
print(f"Sensible: {resultat['sensible']}")
print(f"Message: {resultat['message']}")
print(f"Conseils: {resultat['conseils']}")

print("\n✅ Tous les scénarios testés !")