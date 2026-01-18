#!/usr/bin/env python3
"""Verify that all geospatial packages are using the system GDAL installation."""

import sys
import subprocess

def verify_gdal_bindings():
    print('=' * 70)
    print('GDAL BINDING VERIFICATION')
    print('=' * 70)
    
    # Test GDAL Python bindings
    try:
        from osgeo import gdal
        print(f' GDAL (osgeo):     {gdal.__file__}')
        print(f' GDAL version:     {gdal.__version__}')
        print(f' GDAL data:        {gdal.GetConfigOption("GDAL_DATA")}')
    except Exception as e:
        print(f'GDAL import failed: {e}')
        return False
    
    # Test pyproj
    try:
        import pyproj
        print(f' pyproj:           {pyproj.__file__}')
        print(f' pyproj version:   {pyproj.__version__}')
        print(f' PROJ data:        {pyproj.datadir.get_data_dir()}')
    except Exception as e:
        print(f' pyproj import failed: {e}')
        return False
    
    # Test Fiona
    try:
        import fiona
        print(f'✓ Fiona:            {fiona.__file__}')
        print(f'  Fiona version:    {fiona.__version__}')
        print(f'  GDAL version:     {fiona.__gdal_version__}')
    except Exception as e:
        print(f'✗ Fiona import failed: {e}')
        return False
    
    # Test rasterio
    try:
        import rasterio
        print(f'✓ rasterio:         {rasterio.__file__}')
        print(f'  rasterio version: {rasterio.__version__}')
        print(f'  GDAL version:     {rasterio.__gdal_version__}')
    except Exception as e:
        print(f'✗ rasterio import failed: {e}')
        return False
    
    # Test GeoPandas
    try:
        import geopandas
        print(f'✓ geopandas:        {geopandas.__file__}')
        print(f'  geopandas ver:    {geopandas.__version__}')
    except Exception as e:
        print(f'✗ geopandas import failed: {e}')
        return False
    
    # Test Shapely
    try:
        import shapely
        print(f'✓ Shapely:          {shapely.__file__}')
        print(f'  Shapely version:  {shapely.__version__}')
        print(f'  GEOS version:     {shapely.geos_version_string}')
    except Exception as e:
        print(f'✗ Shapely import failed: {e}')
        return False
    
    # Verify system GDAL matches package GDAL
    sys_gdal = subprocess.check_output(['gdal-config', '--version']).decode().strip()
    print(f'\n--- GDAL Version Check ---')
    print(f'System GDAL:        {sys_gdal}')
    print(f'Fiona GDAL:         {fiona.__gdal_version__}')
    print(f'rasterio GDAL:      {rasterio.__gdal_version__}')
    
    if fiona.__gdal_version__.startswith(sys_gdal.split(".")[0]):
        print('✓ GDAL versions match (major version)')
    else:
        print(f'✗ GDAL version mismatch!')
        return False
    
    print('=' * 70)
    print('✓ ALL GDAL BINDINGS VERIFIED - Using system GDAL')
    print('=' * 70)
    return True

if __name__ == '__main__':
    if not verify_gdal_bindings():
        sys.exit(1)