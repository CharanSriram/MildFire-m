import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('MacOSX')
from requests import get
from deepforest import deepforest
from deepforest import get_data
import os
import staticmaps
import maputil
import cv2
import pandas as pd

# load release model
with open("/tmp/NEON.h5", "wb") as file:
    # get request
    response = get("https://storage.googleapis.com/mildfire.appspot.com/NEON.h5")
    # write to file
    file.write(response.content)

model = deepforest.deepforest(saved_model='/tmp/NEON.h5')
os.remove("/tmp/NEON.h5")
# model.use_release() # uses release model

def get_predictions(lat, lng):
    """
    gets tree location predictions (in lat/lng) from a region surrounding given a lat/lng

    returns array of tuples that represents all predicted trees.
    Each tree tuple is structured as follows:
        (latitude of tree, longitude of tree, radius of tree in px, prediction confidence)
    """
    image_arrays = staticmaps.get_region(lat, lng)

    trees = []

    # go thru each tile
    for (arr, tile_lat, tile_lng, east, north) in image_arrays:
        # returns pandas DataFrame, we want to concatenate TODO: consider different thresholds
        tile_predictions = model.predict_image(numpy_image=cv2.imdecode(arr, -1),
                                                    return_plot=False, score_threshold=0.1)
        
        for _, row in tile_predictions.iterrows():
            tree_center_x = (row['xmin'] + row['xmax']) / 2
            tree_center_y = (row['ymin'] + row['ymax']) / 2

            # radius is average of height and width in pixels
            tree_radius = ((row['xmax'] - row['xmin']) / 2 + (row['ymax'] - row['ymin']) / 2) / 2

            # get tree center in latitude
            tree_center_lat, tree_center_lng = imagewise_pixel_xy_to_latlng(tree_center_x, tree_center_y, tile_lat, tile_lng)

            tree_tuple = (tree_center_lat, tree_center_lng, tree_radius, row['score'])
            trees.append(tree_tuple)
            # print(row['xmin'], row['ymin'], row['xmax'], row['ymax'], row['score'])

    return trees

def imagewise_pixel_xy_to_latlng(x, y, tile_lat, tile_lng):
    x_delta = x - staticmaps.TILE_WIDTH / 2
    y_delta = y - staticmaps.TILE_WIDTH / 2
    tree_lat = maputil.adjust_lat_by_pixels(tile_lat, y_delta, staticmaps.ZOOM)
    tree_lng = maputil.adjust_lng_by_pixels(tile_lng, x_delta, staticmaps.ZOOM)

    return tree_lat, tree_lng


all_trees = get_predictions(37.297251, -121.9012)

for tree in all_trees:
    print(tree)