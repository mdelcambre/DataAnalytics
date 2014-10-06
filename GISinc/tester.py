#!/usr/bin/env python
"""Tests the normilazing script"""

from normalized import Point, normalizePoint


def Point_str(point):
    return "Point(%d, %d)" % (point.lon, point.lat)



def tester(func, expt):
    func_point = normalizePoint(Point(func[0],func[1]))
    expt_point = Point(expt[0],expt[1])
    func_str = Point_str(func_point)
    expt_str = Point_str(expt_point)
    if expt_point.lat == func_point.lat and expt_point.lon == func_point.lon:
        print "Pass"
    else:
        print "Fail: Func: %s Expt: %s" % (func_str,expt_str)




tester((190,240),(-170,-60))
tester((-210,120),(150,60))
tester((720,-10),(0,-10))
tester((-750,0),(-30,0))
tester((-890,-100),(-170,-80))
tester((920,180),(-160,0))
