import urllib.request
import numpy as np
import maputil

TILE_WIDTH = 640
DEFAULT_WIDTH_NUM_TILES = 3
ZOOM = 20

def get_region(center_lat, center_lng, width_num_tiles=DEFAULT_WIDTH_NUM_TILES):
    """
    returns array of numpy arrays containing all image data based on long/lat center
    width_num_tiles: width of region in tiles
    """
    # grab all centers
    centers = []
    for northing in range(-(width_num_tiles//2), width_num_tiles//2 + 1):
        new_lat = maputil.adjust_lat_by_pixels(center_lat, northing * TILE_WIDTH, ZOOM)
        for easting in range(-(width_num_tiles//2), width_num_tiles//2 + 1):
            new_lng = maputil.adjust_lng_by_pixels(center_lng, easting * TILE_WIDTH, ZOOM)
            centers.append((new_lat, new_lng, easting, northing))
    # calculate all centers corresponding a square region of square tiles
    # of size area_width * area_width
    arrays = []
    for (lat, lng, east, north) in centers:
        arrays.append((get_tile(lat, lng), lat, lng, east, north))
    return arrays

def get_tile(latitude, longitude):
    """ returns numpy array containing 640x640 image data based on long/lat center """
    url = ("https://maps.googleapis.com/maps/api/staticmap?center="
           + str(latitude) + ",%20" + str(longitude)
           + "&zoom=20&size=640x640&maptype=satellite&key=AIzaSyAJDptVfsenJ38qgllhdHMWa_Ceznu1w0I")
    print(url)
    req = urllib.request.urlopen(url)
    return np.asarray(bytearray(req.read()), dtype=np.uint8)
