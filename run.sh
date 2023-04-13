#!/bin/bash

# Fetch tasmania aerial images from google cloud bucket
python3 fetchByZone.py 931 134
echo "successfully fetched images from tile (931,134) in geographic mercator at zoom level 9"

# Run gdalbuildvrt to create the merged.vrt file
mkdir tas_vrts
gdalbuildvrt tas_vrts/merged.vrt tas_images/*.png
echo "successfully built merge.vrt"

# Run the extract.py script and capture its output
output=$(python3 extract.py)
echo "successfully extracted the corner coordinates from the pgw files"

# Extract the four values from the output (assuming they are space-separated)
ulx=$(echo $output | awk '{print $1}')
uly=$(echo $output | awk '{print $2}')
lrx=$(echo $output | awk '{print $3}')
lry=$(echo $output | awk '{print $4}')

# Run gdal_edit.py with the extracted values
gdal_edit.py -a_srs EPSG:28355 -a_ullr $ulx $uly $lrx $lry tas_vrts/merged.vrt
echo "successfully added the corner coordinates to merge.vrt"

# Prepare an output folder for the pyramid
mkdir mergedPyramid
echo "successfully created target directory mergedPyramid"

baseTileSize=$(python3 baseTileSize.py)
baseTileX=$(echo $baseTileSize | awk '{print $1}')
baseTileY=$(echo $baseTileSize | awk '{print $2}')

# Create tile pyramids of the VRT
# -co "COMPRESS=LZW"
gdal_retile.py -v -r cubic -levels 4 -ps $baseTileX $baseTileY -co "TILED=YES" -targetDir mergedPyramid tas_vrts/merged.vrt
echo "successfully created tile pyramids for merged.vrt"

echo "done"