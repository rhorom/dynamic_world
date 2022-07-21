# dynamic_world
Some sources related to the downloading and processing Dynamic World data from Google Earth Engine

Dynamic World is a 10m near-real-time (NRT) Land Use/Land Cover (LULC) dataset that includes class probabilities and label information for nine classes. Those are water, trees, grass, flooded_vegetation, crops, shrub_and_scrub, built, bare, and snow_and_ice. More information about this data can be found at [DynamicWorld website](https://dynamicworld.app/about) or associated description at the [Google Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1).

`dynamic_world_download.py` is a python script for exporting Dynamic World data globally, tile-by-tile. It reads `globalTile100.csv` that contains the coordinate of 300+ tiles covering lands. Each tile is approximately 10x10 degree square.

## Usage
To perform the export, make sure that you have installed the following packages in your computer.
- numpy (pip install numpy)
- pandas (pip install pandas)
- ee (pip install earthengine-api)

Download both `dynamic_world_download.py` and `globalTile100.csv`. Put them in the same directory.

Set up your google account and get it ready for the use. You may need to visit [Google Earth Engine](https://github.com/rhorom/dynamic_world.git) for this purpose.

After the preparation, you just need to go to the directory and run the script. The inputs required are the band name, year, and the submission mode. These will be prompted on the screen. The available band names for selection are water, trees, grass, flooded_vegetation, crops, shrub_and_scrub, built, bare, and snow_and_ice. The year options are 2016 to the current year. The submission modes are either 'all' or 'part'. If you choose 'all', then the script will submit all 300+ tasks to the Google Earth Engine at once. On the other hand, the script can submit 10 tasks per 30 minutes when you choose 'part'.

You can check the **Tasks** tab on the top right panel of the [code.earthengine.google.com](https://code.earthengine.google.com) for the status of the tasks. The rasters produced will be exported to `dynamic_world_yyyy` folder in your Google Drive.
