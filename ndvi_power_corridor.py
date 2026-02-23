import ee
import geemap

ee.Initialize(project='geosentinel-488221')

aoi = ee.Geometry.BBox(-122.5, 47.2, -121.8, 47.8)

s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(aoi)
    .filterDate('2024-06-01', '2024-09-30')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)))

composite = s2.median().clip(aoi)

ndvi = composite.normalizedDifference(['B8', 'B4']).rename('NDVI')

Map = geemap.Map(center=[47.5, -122.2], zoom=10)

Map.addLayer(composite, {
    'bands': ['B4', 'B3', 'B2'],
    'min': 0, 'max': 3000
}, 'True Color')

Map.addLayer(ndvi, {
    'min': -0.2, 'max': 0.8,
    'palette': ['red', 'yellow', 'lightgreen', 'darkgreen']
}, 'NDVI')

Map.addLayerControl()
Map.save('ndvi_map.html')
print('Done! Open ndvi_map.html in your browser.')