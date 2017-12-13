#!/usr/bin/python

import urllib2
import os, sys
from gmap_utils import *
from multiprocessing.dummy import Pool as ThreadPool 

import time
import random

zoom=1

def download(location):
    x = location[0]
    y = location[1]
    
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
    headers = { 'User-Agent' : user_agent }
    
    url = "http://mt2.google.cn/vt/lyrs=m&hl=zh-CN&gl=cn&x=%d&s=&y=%d&z=%d" % (x, y, zoom)
    filename = "tiles/%d/%d/%d.png" % (zoom, x, y) 
    
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    
    if not os.path.exists(filename):
        
        bytes = None
        
        try:
            req = urllib2.Request(url, data=None, headers=headers)
            response = urllib2.urlopen(req)
            bytes = response.read()
        except Exception, e:
            print "--", filename, "->", e
            sys.exit(1)
        
        if bytes.startswith("<html>"):
            print "-- forbidden", filename
            sys.exit(1)
        
        print "-- saving", filename
        
        f = open(filename,'wb')
        f.write(bytes)
        f.close()
        
        time.sleep(1 + random.random())

def download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True):

    start_x, start_y = latlon2xy(zoom, lat_start, lon_start)
    stop_x, stop_y = latlon2xy(zoom, lat_stop, lon_stop)
    
    print "x range", start_x, stop_x
    print "y range", start_y, stop_y
    
    locations = []
    for x in xrange(start_x, stop_x):
        for y in xrange(start_y, stop_y):
            locations.append((x,y))
            
    pool = ThreadPool(25) 
    results = pool.map(download, locations)

for zoom in range(5, 11):
    lat_start, lon_start = 31.52, 119.79
    lat_stop, lon_stop = 30.67, 121.58
        
    download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=False)	
