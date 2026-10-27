import os
import ctypes


def check_dll(dll_name, paths=None):
    if paths is None:
        paths = [os.getcwd(), r"E:\PROJET8AGRICULTURE\Agriculture_2.0\OSGeo4W\bin"]

    for path in paths:
        dll_path = os.path.join(path, dll_name)
        if os.path.exists(dll_path):
            try:
                ctypes.CDLL(dll_path)
                print(f"✓ {dll_name} - TROUVÉ ({path})")
                return True
            except Exception as e:
                print(f"✗ {dll_name} - ERREUR: {e}")
                return False

    print(f"✗ {dll_name} - INTROUVABLE")
    return False


# Liste des DLLs à vérifier
required_dlls = [
    "mod_spatialite.dll",
    "spatialite.dll",
    "sqlite3.dll",
    "geos_c.dll",
    "geos.dll",
    "proj_9_3.dll",
    "libxml2.dll",
    "iconv.dll"
]

print("Vérification des DLLs spatialite...")
for dll in required_dlls:
    check_dll(dll)