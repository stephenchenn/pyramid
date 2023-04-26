import json
from google.cloud import storage
import os
import math
import sys
import re

# check if argument is passed
if len(sys.argv) != 3:
    print("Usage: python3 fetchByZone.py <x tile index> <y tile index>")
    sys.exit(1)

# zoom level: 9
# crs: geographic mercator epsg:4326

# define zone tile index (index 0,0 is at bottom-left)
x = int(sys.argv[1])
y = int(sys.argv[2])

# only geojson file
f = open('imagery_geoJsonExtent_zoom_9.json')

# load it as a dictionary
data = json.load(f)

# initialize file list to fetch
files_to_fetch = []

# loop through the goejson file to find the right tile
# then extract the list of files to fetch
for i in data['features']:
    if i["properties"]["x"] == x and i["properties"]["y"] == y:
        files_to_fetch = i["properties"]["fileNames"]
        break

# close geojson file
f.close()

# Create a client object for interacting with the storage API
client = storage.Client()

# Specify the name of the bucket
bucket_name = "eq-c2rw-research"

# Specify the path of the directory within the bucket
directory_path = "TasNetworksProcessedFiles/Ortho/RGB/Orthophoto"

# Get a reference to the bucket and the directory within it
bucket = client.get_bucket(bucket_name)
directory = bucket.list_blobs(prefix=directory_path)

# Iterate over all the files in the directory and print their names
count = 0
index = 0

# create folder
folder_name = 'tas_images'
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

for file in directory:
    # remove extension
    file_no_extension = ((file.name).split("."))[-2]

    # first assume the image is not within the specified zone
    not_within_zone = 1
    for i in files_to_fetch:
        i_no_extension = (i.split("."))[-2]

        # if the image is found in the list of images to fetch, flip the not_within_zone flag to false
        if (file_no_extension == i_no_extension):
            not_within_zone = 0
            if ((file.name).split("."))[-1] == 'txt':
                files_to_fetch.remove(i)
            break

    # if the image is not within zone, move on to the next
    if not_within_zone == 1:
        continue

    index = math.floor(count/3)

    # Get the blob (file) from the bucket
    blob = bucket.blob(file.name)
    extension = ((file.name).split("."))[-1]

    file_name = os.path.join(folder_name, 'input' +
                             str(index) + "." + extension)
    # Download the blob's content and save it to a file
    with open(file_name, 'wb') as file_obj:
        blob.download_to_file(file_obj)

    count = count+1
    print(file_name + ' downloaded successfully.')

print(f"number of files to fetch: {len(files_to_fetch)} images within the zone")
print(f"downloaded {str(count)}  files")