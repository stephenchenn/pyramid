from osgeo import gdal
import math
import sys

if len(sys.argv) < 2:
    print("Usage: python3 script_name.py <number of levels>")
    sys.exit(1)

dataset = gdal.Open('tas_vrts/merged.vrt')

# Get the image size and geospatial information
cols = dataset.RasterXSize
rows = dataset.RasterYSize

levelNum = int(sys.argv[1])

# 16 because 2^4
print("{} {}".format( math.ceil( cols/( 2 ** levelNum )), math.ceil( rows/( 2 ** levelNum )) ) )