from google.cloud import storage
import sys
import re
from pyproj import CRS
from pyproj import Transformer
import sys

# check if argument is passed
if len(sys.argv) != 4:
    print("Usage: python3 filter.py origin coordinates in EPSG:28355 (bottom-left corner): <x> <y> <buffer size (metre)>")
    sys.exit(1)

# extract coordinates from user input
origin_x_mercator = float(sys.argv[1])
origin_y_mercator = float(sys.argv[2])
# define the source projection CRS (EPSG:3857 WGS 84 / Pseudo-Mercator)
src_crs = CRS.from_epsg(3857)
# define the target projection CRS (EPSG:28355 GDA94 / MGA zone 55)
des_crs = CRS.from_epsg(28355)
# compute the transformer from the geodetic CRS to the projection CRS
proj = Transformer.from_crs(src_crs, des_crs)
# transform coordinates to EPSG:3857
coordinates_bottom_left = proj.transform(origin_x_mercator, origin_y_mercator)
origin_x_utm_bottom_left = coordinates_bottom_left[0]
origin_y_utm_bottom_left = coordinates_bottom_left[1]

# find upper right corner and convert to 28355 as well
buffer = float(sys.argv[3])
coordinates_upper_right = proj.transform(origin_x_mercator + buffer, origin_y_mercator + buffer)
origin_x_utm_upper_right = coordinates_upper_right[0]
origin_y_utm_upper_right = coordinates_upper_right[1]

print(f"origin coordinates in EPSG:28355: lower left: ( x: {origin_x_utm_bottom_left}, y: {origin_y_utm_bottom_left} ) upper right: ( x: {origin_x_utm_upper_right}, y: {origin_y_utm_upper_right} ) ")
print(f"buffer size: {buffer} metres")

# Create a client object for interacting with the storage API
client = storage.Client()

# Specify the name of the bucket
bucket_name = "eq-c2rw-research"

# Specify the path of the directory within the bucket
directory_path = "TasNetworks/Ortho/RGB/Orthophoto"

# Get a reference to the bucket and the directory within it
bucket = client.get_bucket(bucket_name)
directory = bucket.list_blobs(prefix=directory_path)

limit = 100000
count = 0

for file in directory:
    # use regular expressions to find the numbers in the string
    match = re.search(r'(\d+)_(\d+)\.', file.name)

    # extract the x and y coordinates in EPSG:28355 from the match object
    x_utm = float(match.group(1))
    y_utm = float(match.group(2))

    # print(f"( x: {x_utm}, y: {y_utm} )")

    if (( x_utm >= origin_x_utm_bottom_left ) and ( x_utm <= origin_x_utm_upper_right ) and ( y_utm >= origin_y_utm_bottom_left ) and ( y_utm <= origin_y_utm_upper_right )):
        print (f"({x_utm}, {y_utm})")

    count = count + 1
    if count > limit:
        break
