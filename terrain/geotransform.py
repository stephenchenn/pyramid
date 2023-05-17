from osgeo import gdal, osr
import os

for filename in os.listdir('tas_terrains'):
    dataset = gdal.Open(os.path.join("tas_terrains", filename))

    tileindex = (filename.split("-")[-1]).split(".")[-2]

    with open(os.path.join("tas_pgws", "ortho_TAS_Networks_Campaign_1-" + tileindex + ".pgw")) as f:
        lines = f.readlines()
        geotransform = tuple(map(float, lines))
        geotransform = ([geotransform[4], geotransform[0], geotransform[1], geotransform[5], geotransform[2], geotransform[3]])

    dataset.SetGeoTransform(geotransform)

    # Define the CRS using an EPSG code (e.g., EPSG:4326 for WGS84)
    crs = osr.SpatialReference()
    crs.ImportFromEPSG(28355)

    # Set the CRS of the dataset
    dataset.SetProjection(crs.ExportToWkt())
