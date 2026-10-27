import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from vegetables_fruits.views import valider_image_upload
from PIL import Image
import io


class TestValidationUploads:
    """Tests de sécurité pour les uploads d'images (MIME, taille, intégrité)."""

    def test_upload_image_valide(self):
        """Une vraie image PNG doit passer la validation."""
        # On crée une vraie petite image en mémoire
        img_io = io.BytesIO()
        img = Image.new('RGB', (100, 100), color='red')
        img.save(img_io, format='PNG')

        # On simule le fichier uploadé par l'utilisateur
        fichier = SimpleUploadedFile(
            name='test_image.png',
            content=img_io.getvalue(),
            content_type='image/png'
        )

        valide, message = valider_image_upload(fichier, taille_max_mo=5)

        assert valide is True, f"L'image valide a été rejetée : {message}"
        assert message == ""

    def test_upload_faux_fichier(self):
        """Un fichier exécutable (ou texte) renommé en .jpg doit être bloqué."""
        # On simule un script PHP ou un exécutable renommé en jpg
        faux_contenu = b"<?php echo 'hack'; ?>"
        fichier = SimpleUploadedFile(
            name='virus.jpg',  # Le nom fait croire à une image
            content=faux_contenu,
            content_type='image/jpeg'  # L'utilisateur falsifie aussi le content_type
        )

        # Le validateur (via magic et PIL) doit s'en rendre compte
        valide, message = valider_image_upload(fichier, taille_max_mo=5)

        assert valide is False, "Le faux fichier a été accepté (dangereux !)"
        assert "Format non autorisé" in message or "Image corrompue" in message

    def test_upload_fichier_trop_lourd(self):
        """Un fichier de plus de 5 Mo doit être rejeté avant même d'être analysé."""
        # On crée un faux fichier de 6 Mo
        gros_contenu = b"a" * (6 * 1024 * 1024)
        fichier = SimpleUploadedFile(
            name='gros_fichier.jpg',
            content=gros_contenu,
            content_type='image/jpeg'
        )

        valide, message = valider_image_upload(fichier, taille_max_mo=5)

        assert valide is False
        assert "trop lourde" in message