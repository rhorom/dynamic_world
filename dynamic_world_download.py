import numpy as np
import pandas as pd
import ee
import time

def acquiring(bounds, idx='', year='2018', output='binary'):
    '''
    Function to acquire dynamic world raster for a specific
    year, and rectangular area.
    
    Input:
    bounds : list of geometry bounds [lon_min, lat_min, lon_max, lat_max]
    idx    : index or filename suffix
    year   : selected year (between 2016 to current year)
    
    Output:
    task   : a batch export task submitted to GEE.
    raster : The output raster file will be stored in 'dynamic_world_year'
             folder in Google Drive. It is an 8-bit raster containing the
             probability of a class multiplied by 200.
    '''
    
    def reduceToMean(img, idx):
        ima = (img.eq(ee.Image(ee.Number(idx).uint8()))
               .reduceResolution(reducer=ee.Reducer.mean(), maxPixels=256)
               .reproject(crs='EPSG:4326', crsTransform=[0.00083333333, 0, 0, 0, -0.00083333333, 0])
               .multiply(25)
              )
        return ima
        
    if type(year) != str:
        year = str(year)
        
    date_start = year + '-01-01'
    date_end = year + '-12-01'
    description = 'dworld_%s_%s'%(year, idx)
    region = ee.Geometry.BBox(bounds[0],bounds[1],bounds[2],bounds[3])
    bands = ee.List.sequence(0, 8)
    bandNames = ee.List(['water', 'trees', 'grass', 'flooded_vegetation', 'crops', 'shrub_and_scrub', 'built', 'bare', 'snow_and_ice'])
    
    imcol = (ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
             .filterBounds(region)
             .filterDate(date_start, date_end)
             .select('label')
            )
    
    mostProb = imcol.reduce(ee.Reducer.mode()).clip(region).setDefaultProjection(crs='EPSG:4326', scale=10)
    if (output == 'binary'):
        mostProb = (mostProb
                    .reduceResolution(reducer=ee.Reducer.mode(), maxPixels=256)
                    .reproject(crs='EPSG:4326', crsTransform=[0.00083333333, 0, 0, 0, -0.00083333333, 0])
                   )
        image = bands.map(lambda idx: mostProb.eq(ee.Image(ee.Number(idx).uint8())))
    else:
        image = bands.map(lambda idx: reduceToMean(mostProb, idx))

    image = ee.ImageCollection(image).toBands().rename(bandNames).uint8()
    task = ee.batch.Export.image.toDrive(image=image,
                                         region=region,
                                         description=description,
                                         folder='dynamic_world_' + year,
                                         fileNamePrefix=description,
                                         maxPixels=1e10,
                                         crsTransform=[0.00083333333, 0, 0, 0, -0.00083333333, 0],
                                         crs='EPSG:4326')
    task.start()
    print('Submitted task:', description)
    
    return task

bands = ['water', 'trees', 'grass', 'flooded_vegetation', 'crops', 'shrub_and_scrub', 'built', 'bare', 'snow_and_ice']
year = '2018'
submission_mode = ''

year = input('Select year (2016-2021): ')

while not(submission_mode in ['all', 'part', 'test']):
    submission_mode = input('Submission mode (all/part/test): ')

#Authentication and initialisation of google earth engine python API
#Sign in to google account and give essential authorisations
ee.Authenticate(auth_mode='notebook')
ee.Initialize()

tiles = pd.read_csv('globalTile100.csv')
tasks = []
if (submission_mode == 'test'):
    nrow = 1
else:
    nrow = len(tiles)
    
for i in range(nrow):
    if tiles.area_.values[i] < 1e8:
        print('Unsignificant tile', tiles.iloc[i].ID)
        continue

    bounds = tiles.bounds.values[i][1:-1].split(',')
    bounds = [float(a) for a in bounds]
    idx = tiles.ID.values[i]
    t = acquiring(bounds, idx, year=year, output='binary')
    tasks.append(t)
    
    if ((submission_mode == 'part') & (i%10 == 9)):
        print('Wait for 30 min after submitting 10 tasks')
        time.sleep(1800)
