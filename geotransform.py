from osgeo import gdal

dataset = gdal.Open("ortho_TAS_Networks_Campaign_1-357000_5452500.png")

geotransform = ([ 356999.5, 0.05, 0, 5453000.5, 0, -0.05 ])

dataset.SetGeoTransform(geotransform)