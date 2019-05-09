
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:16:24 2019

script for extracting topography data from a given wrfout file,
and saving it in a format suitable for EMEP to use.

Usage:
    python create_topography_file.py -i [file in] -o [file out]

@author: mbessdl2
"""


from argparse import ArgumentParser
import netCDF4 as nc

# read in the command line arguments, and check that they exist
parser = ArgumentParser()
parser.add_argument("-i", dest="filein", required=True,
                    help="input file", metavar="FILEIN")
parser.add_argument("-o", dest="fileout", required=True,
                    help="output file", metavar="FILEOUT")

args = parser.parse_args()


## list the dimensions and variables that we want to copy across to the new file
include_dimensions = ['west_east', 'south_north']
include_variables = ['XLAT','XLONG','HGT']

## set the variables for which we wish to change the variable name
var_name_change = {}
var_name_change['HGT'] = 'topography'



with nc.Dataset(args.filein,"r") as src, nc.Dataset(args.fileout,"w",clobber=False) as dst:

    # copy required dimensions
    for name, dimension in src.dimensions.items():
        if name in include_dimensions:
            dst.createDimension(name, len(dimension) if not dimension.isunlimited() else None)
    
    # copy the required variables - checking for ones which need the name changed, 
    #                               and changing the descriptions of these too
    for name, variable in src.variables.items():
        if name in include_variables:
            if name in var_name_change:
                name_out = var_name_change[name]
            else:
                name_out = name
            outVar = dst.createVariable(name_out, variable.datatype, variable.dimensions[1:])
            outVar.setncatts({k: variable.getncattr(k) for k in variable.ncattrs()})
            if name in var_name_change:
                outVar.description = var_name_change[name]
            outVar[:] = variable[0,:,:]
    

