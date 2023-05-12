#!/bin/bash

# Clone the files from github
sudo apt-get remove -y --purge man-db
sudo apt update
sudo apt install git -y
git clone https://github.com/stephenchenn/pyramid.git
cd pyramid

# GDAL
# Update the package list
sudo apt-get update
# Install GDAL
sudo apt-get install gdal-bin -y

# DOCKER
# Update the package list again
sudo apt-get update
# Install necessary packages for Docker
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common -y
# Add Docker's GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
# Add Docker's repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
# Update the package list again
sudo apt-get update
# Install Docker
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

# PYTHON CLIENT FOR GOOGLE CLOUD STORAGE API
# Install Python3 pip
sudo apt install python3-pip -y
# Install Google Cloud SDK
pip install google.cloud
# Install Google Cloud Storage library
pip install google-cloud-storage

# GEOSERVER
# Pull GeoServer Docker image
sudo docker pull docker.osgeo.org/geoserver:2.22.0
# Create volume to mount on GeoServer container
sudo docker volume create data_dir
# Get image ID
image_id=$(sudo docker images | awk '{if($1=="docker.osgeo.org/geoserver") print $3;}')
# Run container and mount the volume data_dir
sudo docker run -p 80:8080 -itd --name geoserver --mount source=data_dir,target=/opt/geoserver_data/data $image_id

# IMAGE PYRAMID PLUGIN
sudo apt-get update
sudo apt-get install unzip
# URL of the file to download
url="https://ixpeering.dl.sourceforge.net/project/geoserver/GeoServer/2.22.2/extensions/geoserver-2.22.2-pyramid-plugin.zip"
# Download the file using curl
curl -O "$url"
unzip geoserver-2.22.2-pyramid-plugin.zip -d pyramid-plugin
container_id=$(sudo docker ps | awk '{if($2=="'"$image_id"'") print $1;}')
cd pyramid-plugin
sudo docker cp . $container_id:/opt/apache-tomcat-9.0.68/webapps/geoserver/WEB-INF/lib
cd ..
sudo docker restart $container_id