from pyproj import CRS
from pyproj import Transformer
import sys

# check if argument is passed
if len(sys.argv) != 3:
    print("Usage: python3 convert.py <x coordinate> <y coordinate>")
    print("This python program converts coordinates from EPSG:3857 to EPSG:28355")
    sys.exit(1)

# define the source projection CRS (EPSG:3857 WGS 84 / Pseudo-Mercator )
src_crs = CRS.from_epsg(3857)
# define the target projection CRS (EPSG:28355 GDA94 / MGA zone 55)
des_crs = CRS.from_epsg(28355)
# compute the transformer from the geodetic CRS to the projection CRS
proj = Transformer.from_crs(src_crs, des_crs)
# transform coordinates
coordinates = proj.transform(int(sys.argv[1]), int(sys.argv[2]))
# print result
print(coordinates)