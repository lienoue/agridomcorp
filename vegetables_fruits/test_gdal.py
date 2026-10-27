import os

print("GEOS_LIBRARY_PATH:", os.environ.get('GEOS_LIBRARY_PATH'))
print("GDAL_LIBRARY_PATH:", os.environ.get('GDAL_LIBRARY_PATH'))
print("PROJ_LIB:", os.environ.get('PROJ_LIB'))
print("GDAL_BIN:", os.environ.get('gdal_bin'))
print("PATH contient OSGeo4W:", "OSGeo4W" in os.environ.get('PATH', ''))
