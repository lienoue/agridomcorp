import os
# Remplace par ton chemin exact
os.add_dll_directory(r'E:\PROJET8AGRICULTURE\Agriculture_2.0\OSGeo4W\bin')
import ctypes

# Teste ces trois-là un par un. Lequel bloque ?
#ctypes.CDLL(r'E:\PROJET8AGRICULTURE\Agriculture_2.0\OSGeo4W\bin\libpng16.dll')
#ctypes.CDLL(r'E:\PROJET8AGRICULTURE\Agriculture_2.0\OSGeo4W\bin\proj_9_4.dll')
ctypes.CDLL(r'E:\PROJET8AGRICULTURE\Agriculture_2.0\OSGeo4W\bin\gdal310.dll')