import os
import sqlite3
import sys


def test_spatialite():
    # Essayer différents chemins possibles
    possible_paths = [
        r"C:\OSGeo4W\bin",
        r"C:\Program Files\OSGeo4W\bin",
        os.path.join(os.getcwd(), "dlls"),
        ""
    ]

    for path in possible_paths:
        if path and os.path.exists(path):
            os.environ['PATH'] = path + ";" + os.environ['PATH']
            print(f"{path}")

    try:
        conn = sqlite3.connect(':memory:')
        conn.enable_load_extension(True)

        # Essayer différents noms de module
        extensions = ['mod_spatialite', 'spatialite', 'libspatialite']

        for ext in extensions:
            try:
                conn.load_extension(ext)
                print(f"✓ Extension chargée : {ext}")
                break
            except:
                continue
        else:
            raise Exception("Aucune extension spatialite trouvée")

        # Tester
        cursor = conn.cursor()
        cursor.execute("SELECT spatialite_version()")
        version = cursor.fetchone()[0]
        print(f"✓ Version Spatialite : {version}")

        return True

    except Exception as e:
        print(f"✗ Erreur : {e}")
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    test_spatialite()