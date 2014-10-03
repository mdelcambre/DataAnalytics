#!/usr/bin/env python
"""Defines the Point Class and function to normalize points"""

__author__ = "Mark Delcambre"
__copyright__ = "Copyright 2014, Mark Delcambre"
__license__ = "GPL"
__version__ = "0.1"

__email__ = "mark@delcambre.com"
__status__ = "Prototype"


class Point():
    """Point class for storing Lat Lon pairs, may want to have ways to output
       values. currently accessed via class.lat or class.lon"""

    def __init__(self,lon,lat):
        self.lat = lat
        self.lon = lon


def normalizePoint(point):
    """Returns a point that has wrapped around the lat and lon (e.g. input lat = -100, output lat = 80)"""

    # Check if the Lat overruns.
    if abs(point.lat)>90:

        # find how many times it wraps around by how much
        rem = abs(point.lat) % 90
        div = abs(point.lat) / 90
        neg = -1 if point.lat < 0 else 1

        # There are four cases that we can have:
        if div % 4 == 0: # We have run all the way around the circle so it is simply the remainder with the same sign
            lat = neg * rem
        if div % 4 == 1: # We have gone into the next quadrant, so we keep the same sign but subtract from 90 (starting at a pole)
            lat = neg * (90 - rem)
        if div % 4 == 2: # We have gone past the equator on the far side, simply the remainder but opposite sign.
            lat = (-1 * neg) * rem
        if div % 4 == 3: # We have run past both poles so it is the opposite sign and subtracted from 90
            lat = (-1 * neg) * (90 - rem)
    else: # no overrun on lat, no normalization needed.
        lat = point.lat

    # Check if the Lon overruns.
    if abs(point.lon)>180:
        # find out how many times it wraps around by how much
        rem = abs(point.lon) % 180
        div = abs(point.lon) / 180
        neg = -1 if point.lon < 0 else 1

        # Lon has only two cases.
        if div % 2 == 0: # we have wrapped around into the same hemisphere , same sign, just remainder
            lon = neg*rem
        if div % 2 == 1: # we have wrapped around into the opposite hemisphere: opposite sign and subtract from 180
            lon = (-1 * neg) * (180-rem)
    else: # no overrun on lon, no normalization needed
        lon = point.lon

    return Point(lon,lat) # return a new point object that has been normalized.


