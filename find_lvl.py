import math
from osgeo import gdal

# Open the VRT file
vrt_path = "tas_vrts/output.vrt"
vrt = gdal.Open(vrt_path)

# Get the dimensions
width = vrt.RasterXSize
height = vrt.RasterYSize

larger = max(width, height)

# Close the VRT file
vrt = None

a = larger
c = 2048
b = math.ceil(math.log2(a/c))

print(b)