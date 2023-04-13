from osgeo import gdal
import math

dataset = gdal.Open('tas_vrts/merged.vrt')

# Get the image size and geospatial information
cols = dataset.RasterXSize
rows = dataset.RasterYSize

levelNum = 4

# 16 because 2^4
print("{} {}".format( math.ceil( cols/( 2 ** levelNum )), math.ceil( rows/( 2 ** levelNum )) ) )