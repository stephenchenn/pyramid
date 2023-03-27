from google.cloud import storage
import os
import math
import sys

# check if argument is passed
if len(sys.argv) != 2:
    print("Usage: python3 fetch.py <number of files>")
    sys.exit(1)

# Create a client object for interacting with the storage API
client = storage.Client()

# Specify the name of the bucket
bucket_name = "eq-c2rw-research"

# Specify the path of the directory within the bucket
directory_path = "TasNetworks/Ortho/RGB/Orthophoto"

# Get a reference to the bucket and the directory within it
bucket = client.get_bucket(bucket_name)
directory = bucket.list_blobs(prefix=directory_path)

# Iterate over all the files in the directory and print their names
count=0
# 400 tiles * 3 = 1200 files (png, pgw, txt)
number_of_files=int(sys.argv[1])*3-1
index=0

# create folder
folder_name = 'tas_images'
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

for file in directory:
    # print(file.name)
    # file_name = file.name
    # Get the blob (file) from the bucket
    # Your code here
    index=math.floor(count/3)

    blob = bucket.blob(file.name)
    extension= ((file.name).split("."))[-1]
    # print(extension)
    # file_name = 'input' + str(index) + "." +extension

    file_name = os.path.join(folder_name, 'input' + str(index) + "." +extension)
    # Download the blob's content and save it to a file
    with open(file_name, 'wb') as file_obj:
        blob.download_to_file(file_obj)

    print(file_name + ' downloaded successfully.')

    count=count+1
    if count > number_of_files:
        break

print('Downloaded ' + str(number_of_files+1) + ' files')