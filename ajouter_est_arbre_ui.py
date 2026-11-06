import re
import os

# Chemin vers ton fichier (à adapter si besoin)
FICHIER = 'vegetables_fruits/data/cycles_cultures.py'

# Les cultures à forcer en "Arbre" dans l'UI
CULTURES_A_ARBRES = [
    'bananier', 'banane', 'papayer', 'papaye', 'ananas',
    'safou', 'safoutier', 'prunier d afrique',
    'mangue', 'manguier', 'avocat', 'avocatier',
    'litchi', 'litchier', 'goyave', 'goyavier',
    'cacao', 'cacaoyer', 'café', 'cafe', 'caféier', 'cafeier',
    'noix de coco', 'cocotier', 'datte', 'dattier',
    'vanille', 'vanillier',
    'fruit de la passion', 'passiflore', 'fruit du dragon', 'pitaya'
]

def ajouter_est_arbre():
    if not os.path.exists(FICHIER):
        print(f"❌ Fichier introuvable : {FICHIER}")
        return

    with open(FICHIER, 'r', encoding='utf-8') as f:
        lignes = f.readlines()

    modifiees = 0
    nouvelles_lignes = []

    for ligne in lignes:
        # Si la ligne définit une de nos cultures
        for culture in CULTURES_A_ARBRES:
            # On cherche la clé exacte (ex: 'bananier':)
            if f"'{culture}':" in ligne or f'"{culture}":' in ligne:
                # Si 'est_arbre_ui' n'est pas déjà dans la ligne
                if 'est_arbre_ui' not in ligne:
                    # On injecte la propriété juste après l'accolade {
                    ligne = ligne.replace("{", "{'est_arbre_ui': True, ", 1)
                    modifiees += 1
                    print(f"✅ Modifié : {culture}")
                break # On passe à la ligne suivante
        nouvelles_lignes.append(ligne)

    # Sauvegarde
    with open(FICHIER, 'w', encoding='utf-8') as f:
        f.writelines(nouvelles_lignes)

    print(f"\n🎉 Terminé ! {modifiees} ligne(s) mise(s) à jour.")

if __name__ == "__main__":
    ajouter_est_arbre()