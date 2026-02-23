import ee
import geemap

ee.Initialize(project='geosentinel-488221')

# Mt Rainier study area
aoi = ee.Geometry.BBox(-121.9, 46.7, -121.4, 47.0)

# Load Sentinel-2 for two different years to compare
# NDSI works best with late summer imagery when snow is at minimum
def get_snowpack(year):
    return (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterBounds(aoi)
        .filterDate(f'{year}-08-01', f'{year}-09-30')
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        .median()
        .clip(aoi))

# Get imagery for two years
image_2020 = get_snowpack(2020)
image_2024 = get_snowpack(2024)

# Compute NDSI for both years
# NDSI = (Green - SWIR) / (Green + SWIR)
# Band 3 = Green, Band 11 = SWIR
ndsi_2020 = image_2020.normalizedDifference(['B3', 'B11']).rename('NDSI_2020')
ndsi_2024 = image_2024.normalizedDifference(['B3', 'B11']).rename('NDSI_2024')

# Snow = NDSI above 0.4
snow_2020 = ndsi_2020.gt(0.4)
snow_2024 = ndsi_2024.gt(0.4)

# Build map
Map = geemap.Map(center=[46.85, -121.65], zoom=11)

# Snow coverage palette - white=snow, black=no snow
Map.addLayer(snow_2020, {
    'min': 0, 'max': 1,
    'palette': ['black', 'cyan']
}, 'Snow 2020')

Map.addLayer(snow_2024, {
    'min': 0, 'max': 1,
    'palette': ['black', 'white']
}, 'Snow 2024')

# True color for reference
Map.addLayer(image_2024, {
    'bands': ['B4', 'B3', 'B2'],
    'min': 0, 'max': 3000
}, 'True Color 2024')

Map.addLayerControl()
Map.save('glacier_map.html')
print('Done! Open glacier_map.html in your browser.')
print('Toggle between Snow 2020 and Snow 2024 to see glacier change.')
