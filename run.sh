#!/bin/bash

# check if argument is passed
if [ $# -eq 0 ]; then
  echo "Usage: $0 <argument>"
  exit 1
fi

# Fetch tasmania aerial images from google cloud bucket
arg=$1
python3 fetch.py $arg
echo "successfully fetched $arg images"

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

# Create tile pyramids of the VRT
gdal_retile.py -v -r cubic -levels 4 -ps 2048 2048 -co "TILED=YES" -co "COMPRESS=LZW" -targetDir mergedPyramid tas_vrts/merged.vrt
echo "successfully created tile pyramids for merged.vrt"

echo "done"