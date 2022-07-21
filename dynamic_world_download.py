import numpy as np
import pandas as pd
import ee
import time

def acquiring(bounds, idx='', band='built', year='2018'):
    '''
    Function to acquire dynamic world raster for a specific band,
    year, and rectangular area.
    
    Input:
    bounds : list of geometry bounds [lon_min, lat_min, lon_max, lat_max]
    idx    : index or filename suffix
    band   : band to extract. Alternative bands: water, trees, grass,
             flooded_vegetation, crops, shrub_and_scrub, built, bare, snow_and_ice.
    year   : selected year (between 2016 to current year)
    
    Output:
    task   : a batch export task submitted to GEE.
    raster : The output raster file will be stored in 'dynamic_world_year'
             folder in Google Drive. It is an 8-bit raster containing the
             probability of a class multiplied by 200.
    '''
    
    bands = ['water', 'trees', 'grass', 'flooded_vegetation', 'crops', 'shrub_and_scrub', 'built', 'bare', 'snow_and_ice']
    if not(band in bands):
        print("Check the band name.")
        print("['water', 'trees', 'grass', 'flooded_vegetation', 'crops', 'shrub_and_scrub', 'built', 'bare', 'snow_and_ice']")
        return
    
    if type(year) != str:
        year = str(year)
        
    date_start = year + '-01-01'
    date_end = year + '-12-01'
    description = 'dworld_%s_%s_%s'%(year, band, idx)
    region = ee.Geometry.BBox(bounds[0],bounds[1],bounds[2],bounds[3])
    
    imcol = (ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
             .filterBounds(region)
             .filterDate(date_start, date_end)
             .select(band))
    image = imcol.reduce(ee.Reducer.mean()).multiply(200).uint8()
    image = image.updateMask(image.gt(0))
    task = ee.batch.Export.image.toDrive(image=image,
                                         region=region,
                                         description=description,
                                         folder='dynamic_world_' + year,
                                         fileNamePrefix=description,
                                         scale=100,
                                         maxPixels=1e10,
                                         crs='EPSG:4326')
    task.start()
    print('Submitted task:', description)
    
    return task

bands = ['water', 'trees', 'grass', 'flooded_vegetation', 'crops', 'shrub_and_scrub', 'built', 'bare', 'snow_and_ice']
band = ''
year = '2018'
submission_mode = 'all'

while not(band in bands):
    band = input('Select one band (see spreadsheet): ')
    
year = input('Select year (2016-2021): ')

submission_mode = input('Submission mode (all, part): ')

#Authentication and initialisation of google earth engine python API
#Sign in to google account and give essential authorisations
ee.Authenticate()
ee.Initialize()

tiles = pd.read_csv('globalTile100.csv')
tasks = []
for i in range(len(tiles)):
    if tiles.area_.values[i] < 1e8:
        print('Unsignificant tile', tiles.iloc[i].ID)
        continue

    bounds = tiles.bounds.values[i][1:-1].split(',')
    bounds = [float(a) for a in bounds]
    idx = tiles.ID.values[i]
    t = acquiring(bounds, idx, year=year, band=band)
    tasks.append(t)
    
    if ((submission_mode == 'part') & (i%10 == 9)):
        print('Wait for 30 min after submitting 10 tasks')
        time.sleep(1800)
