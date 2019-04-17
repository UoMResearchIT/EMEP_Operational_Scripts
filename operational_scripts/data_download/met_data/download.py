#!/usr/bin/env python

import time
from datetime import date

# export PYTHONPATH = /usr/bin/ecmwfapi
from ecmwfapi import ECMWFDataServer
 
server = ECMWFDataServer()

# Set dates for data extraction - SAMBBA campaign period
idate = date(2018,8,1)
edate = date(2018,8,31)

while (idate <= edate):

    iyear = idate.year
    imonth = idate.month
    iday = idate.day

    strdate = "%d%02d%02d" % (iyear, imonth, iday)
    print strdate   

    # extract 3D data
    server.retrieve({
        'dataset' : "interim",
        'step'    : "0",
        'levtype' : "pl",
        'levelist': "all",
        'date'    : strdate,
        'time'    : "00/06/12/18",
        'origin'  : "all",
        'type'    : "an",
        'param'   : "129/130/131/132/157",
        'grid'    : "128",
        'target'  : "pl_"+strdate+".grib"
        })

    # extract surface data
    server.retrieve({
        'dataset' : "interim",
        'step'    : "0",
        'levtype' : "sfc",
        'date'    : strdate,
        'time'    : "00/06/12/18",
        'origin'  : "all",
        'type'    : "an",
        'param'   : "172/134/151/165/166/167/168/235/33/34/31/141/139/170/183/236/39/40/41/42",
        'grid'    : "256", # use higher resolution surface data
        'target'  : "sfc_"+strdate+".grib"
        })

    # move to next day
    
    idate = idate.replace(day=idate.day + 1)

print "End."

