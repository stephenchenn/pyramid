import json

f = open('imagery_geoJsonExtent_zoom_9.json')

data = json.load(f)

file = open("count.txt", "w")

for i in data['features']:
    if 'count' in i["properties"]:
        file.write(str(i["properties"]["x"]))
        file.write(",")
        file.write(str(i["properties"]["y"]))
        file.write(": ")
        file.write(str(i["properties"]["count"]))
        file.write("\n")