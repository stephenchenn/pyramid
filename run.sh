#!/bin/bash

# Check if the script was called with an argument
if [ $# -ne 3 ]; then
  echo "Usage: $0 <number of levels> <x tile index> <y tile index>"
  exit 1
fi

# Store the argument in a variable
levels="$1"
x_tile_index="$2"
y_tile_index="$3"

# # Fetch tasmania aerial images from google cloud bucket
python3 fetchByZone.py $x_tile_index $y_tile_index
echo "successfully fetched images from tile ($x_tile_index,$y_tile_index) in geographic mercator at zoom level 9"

# Run gdalbuildvrt to create the merged.vrt file
mkdir tas_vrts
gdalbuildvrt tas_vrts/merged.vrt tas_images/*.png
echo "successfully built merge.vrt"

# Run gdal_edit.py with the extracted values
gdalwarp -s_srs EPSG:28355 -t_srs EPSG:4326 tas_vrts/merged.vrt tas_vrts/output.vrt
echo "successfully added the corner coordinates to merge.vrt"

# # Prepare an output folder for the pyramid
mkdir mergedPyramid
echo "successfully created target directory mergedPyramid"

baseTileSize=$(python3 baseTileSize.py "$levels")
baseTileX=$(echo $baseTileSize | awk '{print $1}')
baseTileY=$(echo $baseTileSize | awk '{print $2}')

# Create tile pyramids of the VRT
gdal_retile.py -v -r cubic -levels $levels -ps $baseTileX $baseTileY -co "COMPRESS=LZW" -co "TILED=YES" -targetDir mergedPyramid tas_vrts/output.vrt
echo "successfully created tile pyramids for merged.vrt"

echo "done"