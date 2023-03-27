import os
from osgeo import gdal
import math

# Get the current working directory
# dir_path = os.getcwd()
dir_path = os.path.join(os.getcwd(), "tas_images")

# corner coordinates
minUlx=math.inf
maxLrx=-math.inf
minLry=math.inf
maxUly=-math.inf

for filename in os.listdir(dir_path):
    if filename.endswith(".png"):
        # Open the image file
        dataset = gdal.Open(os.path.join(dir_path, filename))

        # Get the image size and geospatial information
        rows = dataset.RasterYSize
        cols = dataset.RasterXSize
        transform = dataset.GetGeoTransform()

        # Extract the corner coordinates
        ulx = transform[0]
        uly = transform[3]
        lrx = ulx + transform[1] * cols
        lry = uly + transform[5] * rows

        if ulx < minUlx:
            minUlx = ulx
        if uly > maxUly:
            maxUly = uly
        if lrx > maxLrx:
            maxLrx = lrx
        if lry < minLry:
            minLry = lry

        # Print the corner coordinates
        # print(filename)
        # print("Upper Left: ({}, {})".format(ulx, uly))
        # print("Lower Right: ({}, {})".format(lrx, lry))

print("{} {} {} {}".format(minUlx, maxUly, maxLrx, minLry))
# print("Upper Left: ({}, {})".format(minUlx, maxUly))
# print("Lower Right: ({}, {})".format(maxLrx, minLry))