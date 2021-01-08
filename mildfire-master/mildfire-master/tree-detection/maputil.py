import math

OFFSET = 268435456 # half of the earth circumference's in pixels at zoom level 21
RADIUS = OFFSET / math.pi

def lng_to_x(x):
    return OFFSET + RADIUS * x * math.pi / 180

def lat_to_y(y):
    return OFFSET - RADIUS * math.log((1 + math.sin(y * math.pi / 180))
                                      / (1 - math.sin(y * math.pi / 180))) / 2

def x_to_lng(x):
    return ((round(x) - OFFSET) / RADIUS) * 180 / math.pi

def y_to_lat(y):
    return (math.pi / 2 - 2 * math.atan(math.exp((round(y) - OFFSET)
                                                 / RADIUS))) * 180 / math.pi

def adjust_lng_by_pixels(lng, delta, zoom):
    return x_to_lng(lng_to_x(lng) + (delta * 2 ** (21 - zoom)))

def adjust_lat_by_pixels(lat, delta, zoom):
    return y_to_lat(lat_to_y(lat) + (delta * 2 ** (21 - zoom)))
