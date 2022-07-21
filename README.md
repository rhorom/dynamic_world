# dynamic_world
Some sources related to the downloading and processing Dynamic World data from Google Earth Engine

Dynamic World is a 10m near-real-time (NRT) Land Use/Land Cover (LULC) dataset that includes class probabilities and label information for nine classes. Those are water, trees, grass, flooded_vegetation, crops, shrub_and_scrub, built, bare, and snow_and_ice. More information about this data can be found at [DynamicWorld website](https://dynamicworld.app/about) or associated description at the [Google Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1).

`dynamic_world_download.py` is a python script for exporting Dynamic World data globally, tile-by-tile. It reads `globalTile100.csv` that contains the coordinate of 300+ tiles covering lands. Each tile is approximately 10x10 degree square.

## Required packages
- numpy (pip install numpy)
- pandas (pip install pandas)
- ee (pip install earthengine-api)
