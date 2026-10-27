from PIL import Image
import os


# Ouvre ton logo original
img = Image.open('images/AgriDomCorp.png')

# Tailles à générer
tailles = [72, 96, 128, 144, 152, 192, 384, 512]

# Dossier de destination
output_dir = 'static/icons/'
os.makedirs(output_dir, exist_ok=True)

# Génère chaque taille
for taille in tailles:
    img_resized = img.resize((taille, taille), Image.Resampling.LANCZOS)
    img_resized.save(f'{output_dir}icon-{taille}x{taille}.png')
    print(f'✅ icon-{taille}x{taille}.png créé')

print('🎉 Toutes les icônes sont prêtes !')