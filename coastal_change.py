import ee
import geemap

# Connect to GEE — required every script
ee.Initialize(project='geosentinel-488221')

# Puget Sound study area — central sound near Seattle/Tacoma
# BBox order always: (west, south, east, north)
aoi = ee.Geometry.BBox(-122.6, 47.0, -122.2, 47.6)

# Load Sentinel-1 SAR collection
# 'COPERNICUS/S1_GRD' = Ground Range Detected SAR data
# This is already preprocessed by ESA — ready to use
s1 = (ee.ImageCollection('COPERNICUS/S1_GRD')
    .filterBounds(aoi)
    .filterDate('2024-01-01', '2024-03-31')
    # VV = vertical transmit, vertical receive polarization
    # Best for detecting water vs land boundaries
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
    # IW = Interferometric Wide swath mode
    # Standard land observation mode for Sentinel-1
    .filter(ee.Filter.eq('instrumentMode', 'IW'))
    .select('VV')
    .median()
    .clip(aoi))

# SAR values are in decibels (dB)
# Water = very low backscatter (smooth surface reflects signal away)
# Land = higher backscatter (rough surface scatters signal back)
# Threshold of -15 dB separates water from land reliably
water_mask = s1.lt(-15)

# Build map centered on Puget Sound
Map = geemap.Map(center=[47.3, -122.4], zoom=10)

# SAR backscatter — darker = water, brighter = land
Map.addLayer(s1, {
    'min': -25,
    'max': 0,
    'palette': ['black', 'white']
}, 'SAR Backscatter')

# Water mask — blue = water, transparent = land
Map.addLayer(water_mask, {
    'min': 0,
    'max': 1,
    'palette': ['white', 'blue']
}, 'Water Mask')

Map.addLayerControl()
Map.save('coastal_map.html')
print('Done! Open coastal_map.html in your browser.')
print('Dark areas = water (low SAR backscatter)')
print('Bright areas = land (high SAR backscatter)')