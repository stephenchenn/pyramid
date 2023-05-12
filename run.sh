#!/bin/bash

# Check if the script was called with an argument
if [ $# -ne 2 ]; then
  echo "Usage: $0 <x tile index> <y tile index>"
  exit 1
fi

# Store the argument in a variable
x_tile_index="$1"
y_tile_index="$2"

# Fetch tasmania aerial images from google cloud bucket
python3 fetchByZone.py $x_tile_index $y_tile_index
echo "successfully fetched images from tile ($x_tile_index,$y_tile_index) in geographic mercator at zoom level 9"

start_time=$(date +%s)

# Run gdalbuildvrt to create the merged.vrt file
mkdir tas_vrts
gdalbuildvrt tas_vrts/merged.vrt tas_images/*.png
echo "successfully built merge.vrt"

# Run gdal_edit.py with the extracted values
gdal_edit.py -a_srs EPSG:28355 tas_vrts/merged.vrt
# gdalwarp -s_srs EPSG:28355 -t_srs EPSG:4326 tas_vrts/merged.vrt tas_vrts/output.vrt
echo "successfully added the corner coordinates to merge.vrt"

# Prepare an output folder for the pyramid
mkdir mergedPyramid
echo "successfully created target directory mergedPyramid"

# levels=$(python3 find_lvl.py)
# echo "number of levels: $levels"

# Create tile pyramids of the VRT
# -co "COMPRESS=LZW" 
# gdal_retile.py -v -r cubic -levels $levels -ps 2048 2048 -co "TILED=YES" -targetDir mergedPyramid tas_vrts/output.vrt
gdal_retile.py -v -r cubic -levels 4 -ps 2048 2048 -co "TILED=YES" -targetDir mergedPyramid tas_vrts/merged.vrt
echo "successfully created tile pyramids for merged.vrt"

echo "done"

end_time=$(date +%s)
echo "Elapsed time: $((end_time - start_time)) seconds"