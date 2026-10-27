# test_gdal_fixed.py
import os
import sys


def test_gdal():
    print("=" * 60)
    print("TEST GDAL - AVEC CONFIGURATION MANUELLE")
    print("=" * 60)

    # Configuration manuelle (identique à settings.py)
    if os.name == 'nt':  # Windows
        OSGEO4W_PATHS = [
            r'E:\PROJET8AGRICULTURE\Agriculture_2.0',
            r'C:\OSGeo4W',
            r'C:\Program Files\GDAL',
            r'C:\gdal',
        ]

        gdal_path = None
        for path in OSGEO4W_PATHS:
            if os.path.exists(path):
                gdal_path = path
                break

        if gdal_path:
            print(f"GDAL trouvé dans: {gdal_path}")

            # Configurer l'environnement
            gdal_bin = os.path.join(gdal_path, 'bin')
            os.environ['PATH'] = gdal_bin + os.pathsep + os.environ['PATH']
            os.environ['GDAL_DATA'] = os.path.join(gdal_path, 'share', 'gdal')
            os.environ['PROJ_LIB'] = os.path.join(gdal_path, 'share', 'proj')

            # Ajouter au Python path
            if gdal_bin not in sys.path:
                sys.path.insert(0, gdal_bin)
        else:
            print("❌ GDAL non trouvé")
            return False

    # Maintenant essayer d'importer GDAL
    try:
        from osgeo import gdal, ogr
        print("✅ GDAL importé avec succès!")
        print(f"Version: {gdal.VersionInfo('RELEASE_NAME')}")
        print(f"Version num: {gdal.VersionInfo()}")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import GDAL: {e}")
        print("\nDebug info:")
        print(f"PATH: {os.environ.get('PATH', '')}")
        print(f"GDAL_DATA: {os.environ.get('GDAL_DATA', 'Non défini')}")
        print(f"PROJ_LIB: {os.environ.get('PROJ_LIB', 'Non défini')}")
        return False


if __name__ == "__main__":
    test_gdal()