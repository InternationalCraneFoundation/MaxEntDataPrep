###########################
# maxEntPrep.py
# By Dorn Moore
# Created 2016-09-22
#
# Purpose: Prepare Raster Layers for use in MaxEnt
# Script will prompt user for three items:
# templateRaster - the example raster that all of the subsequent rasters must
# --match as par of the MaxEnt Process.
# inpath - path where all of the rasters needing conversion comefrom
# outpath - pathe to place all of the new asc raster files
#
###########################
# TODO ->
# Reproject the input raster layer to match the templateRaster


# Import Modules
import os
import sys
from osgeo import gdal, ogr, osr


def getBounds(raster):
    # Function to pull the bounding coordinates from an input Raster
    ds = gdal.Open(raster)

    # get the number of columns and rows
    cols = ds.RasterXSize
    rows = ds.RasterYSize

    gt = ds.GetGeoTransform()
    # e-w cell size
    xSize = gt[1]
    # n-s cell size (always a negative)
    ySize = gt[5]
    # gt[0] is the upper left X
    ulX = gt[0]
    # gt[3] is the upper left Y
    ulY = gt[3]
    # calculate the lrX by adding the (Xsize * # of Columns) to the ulX
    lrX = gt[0]+(cols*xSize)
    # calculate the lrY by subtracting the (Ysize * # of Rows) to the ulY
    lrY = gt[3]+(rows*ySize)

    # return it all
    return (ulX, ulY, lrX, lrY, xSize, ySize)
    # Close the raster - not sure if it's necessary but we don't need the
    # template after this step.
    GDALClose(raster)

# Function to check if a path exists. Since we do this for three paths -
# made it a function.


def checkPath(path):
    if os.path.exists(path):
        return True
    else:
        return False


# ---------------------------------------------------------------------

# Preamble for the user
print "\nThis program will resample and clip your input raster layers to match a template raster layer you've already created. \nYou'll need the following information to get started:"
print "\n* A template raster layer already cliped to the appropriate extent and resolution you desire.\n* The path to the folder of raster layers you want transformed. All raster layers in this folder will be transformed. \n* The folder path where you want the new layers stored."

# Gather the key inormation
templateRaster = raw_input(
    "\nWhat is the full path and filename of the template raster layer: ")
inpath = raw_input("\nWhat is the path for the layers you want to transform: ")
outpath = raw_input(
    "\nThe folder where you want the new raster layers stored needs to already exist. \nWhat is the path where you want to store the final raster layers: ")

# Verify the template raster exists.
if checkPath(templateRaster):
    # Get the information needed below to perform gdalwarp.
    ulX, ulY, lrX, lrY, xSize, ySize = getBounds(templateRaster)
else:
    print"\nUnable to find the template raster file you specified."

# Verify the paths are valid.
if checkPath(inpath) and checkPath(outpath):
    in_f = open(inpath, 'r+')
    out_f = open(outpath, 'r+')

    for file in in_f:
        # Need to put the os commands (like gdal ogr etc) in an os.sys() so they are processed correctly.
        # Use gdalwarp to clip and set resolution of file
        os.sys('gdalwarp -r average -multi -overwrite -te ulX lrY lrX ulY -tr xSize ySize -dstnodata -999 file os.path.join(out_f, file+".tif")')
        # Convert the .tif to an asc - needed for maxEnt
        os.sys('gdal_translate -of AAIGrid os.path.join(out_f,file+".tif") os.path.join(out_f, file+".asc")')
        # Delete the temp file
        os.sys('del os.path.join(out_f, file+".tif")')

    print "\nAll done."
    # Close up shop
    in_f.close()
    out_f.close()
else:
    print "\nUnable to access one of the directories you specified. "


# src_srs=osr.SpatialReference()
# src_srs.ImportFromWkt(ds.GetProjection())
# tgt_srs=osr.SpatialReference()
# tgt_srs.ImportFromEPSG(4326)
# tgt_srs = src_srs.CloneGeogCS()
