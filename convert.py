from pyproj import CRS
from pyproj import Transformer

# define the source projection CRS (EPSG:3857 WGS 84 / Pseudo-Mercator )
src_crs = CRS.from_epsg(3857)
# define the target projection CRS (EPSG:28355 GDA94 / MGA zone 55)
des_crs = CRS.from_epsg(28355)
# compute the transformer from the geodetic CRS to the projection CRS
proj = Transformer.from_crs(src_crs, des_crs)
# transform coordinates
coordinates = proj.transform(16280476, -5165920)
# print result
print(coordinates)