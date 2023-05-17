from google.cloud import storage
import os
import sys
import json

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
f = open('geoJsonExtent_zoom_9.json')

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


client = storage.Client()

bucket_name = "eq-c2rw-research"

terrain_directory_path = "TasNetworks/DEM/DTM"

bucket = client.get_bucket(bucket_name)
directory = bucket.list_blobs(prefix=terrain_directory_path)

folder_name = 'tas_terrains'
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

for file in directory:
    for i in files_to_fetch:
        tileindex = (file.name.split("-")[-1]).split(".")[-2]
        zone_tile_index = (i.split("-")[-1]).split(".")[-2]

        if tileindex == zone_tile_index:
            file_name = os.path.join(folder_name, ((file.name).split("/"))[-1])

            blob = bucket.blob(file.name)

            with open(file_name, 'wb') as file_obj:
                blob.download_to_file(file_obj)

            print(file_name + ' downloaded successfully.')
            files_to_fetch.remove(i)
            break

    if not files_to_fetch:
        break

pgw_directory_path = "TasNetworks/Ortho/RGB/Orthophoto/"

folder_name = 'tas_pgws'
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

not_found = 0

for filename in os.listdir('tas_terrains'):
    tileindex = (filename.split("-")[-1]).split(".")[-2]
    pgwFileName = "ortho_TAS_Networks_Campaign_1-" + tileindex + ".pgw"
    blob = bucket.blob(pgw_directory_path + pgwFileName)

    if blob.exists():
        file_name = os.path.join(folder_name, pgwFileName)

        with open(file_name, 'wb') as file_obj:
            blob.download_to_file(file_obj)

        print(file_name + ' downloaded successfully.')
    else:
        not_found+=1
        with open("notfound.txt", "a") as f:
            f.write(filename)

print(f"number of files to fetch: {len(files_to_fetch)} images within the zone")
print('Could not find corresponding pgw files for ' + str(not_found) + ' terrain files')