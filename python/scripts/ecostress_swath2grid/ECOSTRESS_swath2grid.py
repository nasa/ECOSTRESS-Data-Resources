# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
ECOSTRESS Swath to Grid Conversion Script with Brightness Temperature Conversion Option
Author: LP DAAC
Last Updated: 11/21/2022
See README for additional information:
https://git.earthdata.nasa.gov/projects/LPDUR/repos/ecostress_swath2grid/browse
---------------------------------------------------------------------------------------------------
"""
# Load necessary packages into Python
import h5py
import os
import pyproj
import sys
import argparse
import math
import numpy as np
import warnings
#from pyproj import CRS
warnings.simplefilter(action='ignore', category=UserWarning)
from pyresample import geometry as geom
from pyresample import kd_tree as kdt
from osgeo import gdal, gdal_array, gdalconst, osr
warnings.simplefilter(action='ignore', category=FutureWarning)

# --------------------------COMMAND LINE ARGUMENTS AND ERROR HANDLING---------------------------- #
# Set up argument and error handling
parser = argparse.ArgumentParser(description='Performs ECOSTRESS Swath to Grid Conversion')
parser.add_argument('--proj', required=True, choices=['UTM', 'GEO'], help='Projection desired for output GeoTIFFs')
parser.add_argument('--dir', required=True, help='Local directory containing ECOSTRESS Swath files to be processed')
parser.add_argument('--sds', required=False, help='Specific science datasets (SDS) to extract from ECOSTRESS Granules \
                    (see README for a list of available SDS)')
parser.add_argument('--utmzone', required=False, help='UTM zone (EPSG Code) desired for all outputs--only required if needed to \
                    override default UTM zone which is assigned based on the center location for each ECOSTRESS granule')
parser.add_argument('--bt', required=False, help='Optional argument to convert radiance to brightness temperature \
                    for the L1B products', action='store_true')
args = parser.parse_args()

# --------------------------------SET ARGUMENTS TO VARIABLES------------------------------------- #
# Format and set input/working directory from user-defined arg
if args.dir[-1] != '/' and args.dir[-1] != '\\':
    inDir = args.dir.strip("'").strip('"') + os.sep
else:
    inDir = args.dir

scriptDir = os.getcwd() + os.sep
# Find input directory
try:
    os.chdir(inDir)
except FileNotFoundError:
    print('error: input directory (--dir) provided does not exist or was not found')
    sys.exit(2)

crsIN = args.proj  # Options include 'UTM' or 'GEO'

# -------------------------------------SET UP WORKSPACE------------------------------------------ #
# Create and set output directory
outDir = os.path.normpath((os.path.split(inDir)[0] + os.sep + 'output')) + os.sep
if not os.path.exists(outDir):
    os.makedirs(outDir)

# Create lists of ECOSTRESS HDF-EOS5 files (geo, data) in the directory
geoList = [f for f in os.listdir() if f.startswith('ECO') and f.endswith('.h5') and 'GEO' in f]
ecoList = [f for f in os.listdir() if f.startswith('ECO') and f.endswith('.h5')]

# Check to verify if any ECOSTRESS files are in the directory provided
if len(ecoList) == 0:
    print(f'No ECOSTRESS files found in {inDir}')
    sys.exit(2)
# -------------------------------------DEFINE FUNCTIONS------------------------------------------ #
# Write function to determine which UTM zone to use:
def utmLookup(lat, lon):
    utm = str((math.floor((lon + 180) / 6) % 60) + 1)
    if len(utm) == 1:
        utm = '0' + utm
    if lat >= 0:
        epsg_code = '326' + utm
    else:
        epsg_code = '327' + utm
    return epsg_code


# If brightness temperature is requested, define a function to convert radiance to BT
if args.bt:
    def btConversion(s, ecoSD):
        try:
            # Look up table containing brightness temperature conversions coefficients
            lutFile = h5py.File('EcostressBrightnessTemperatureV01.h5', "r")
        except:
            try:
                lutFile = h5py.File(f'{scriptDir}EcostressBrightnessTemperatureV01.h5', "r")
            except:
                print('Brightness Temp LUT not found, download the table at https://git.earthdata.nasa.gov/projects/LPDUR/repos/ecostress_swath2grid/browse and make sure it is in the same directory as the ECOSTRESS files to be processed or the ECOSTRESS_swath2grid.py script.')
                sys.exit(2)
        # Open the lookup table for the desired radiance band
        lut = lutFile[f"/lut/radiance_{s[-1]}"][()].astype(float) 
        lutFile.close()
        
        # Take the input radiance array, and map to bt conversion coefficient depending on radiance band and value
        ecoSDflat = ecoSD.flatten()
        ecoSDflat = np.where(np.logical_and(0 <= ecoSDflat, ecoSDflat <= 60), ecoSDflat, 0)  # Filter fill values
        indexLUT = np.int32(ecoSDflat / 0.001)

        # Interpolate the LUT values for each radiance based on two nearest LUT values
        bt = np.empty(ecoSDflat.shape, dtype=ecoSDflat.dtype)
        radiance_x0 = indexLUT * 0.001
        radiance_x1 = radiance_x0 + 0.001 
        factor0 = (radiance_x1 - ecoSDflat) / 0.001
        factor1 = (ecoSDflat - radiance_x0) / 0.001     
        bt[:] = (factor0 * lut[indexLUT]) + (factor1 * lut[indexLUT + 1])

        # Set out of range radiance and fill values back to fill value        
        bt = np.where((ecoSDflat != 0), bt, fv)
        bt = bt.reshape(ecoSD.shape)
        return bt

if args.utmzone is not None and args.utmzone[0:3] != '326' and args.utmzone[0:3] != '327':
    parser.error('--utmzone requires the EPSG code (http://spatialreference.org/ref/epsg/) for a UTM zone, and only WGS84 datum is supported')
# ------------------------------------IMPORT ECOSTRESS FILE-------------------------------------- #
# Batch process all files in the input directory
for i, e in enumerate(ecoList):
    i += 1
    print('Processing: {} ({} of {})'.format(e, str(i), str(len(ecoList))))
    f = h5py.File(e, "r")             # Read in ECOSTRESS HDF5-EOS data file
    ecoName = e.split('.h5')[0]       # Keep original filename
    eco_objs = []
    f.visit(eco_objs.append)          # Retrieve list of datasets

    # Search for relevant SDS inside data file
    ecoSDS = [str(o) for o in eco_objs if isinstance(f[o], h5py.Dataset)]

    # Added functionality for dataset subsetting (--sds argument)
    if args.sds is not None:
        sds = args.sds.split(',')
        ecoSDS = [e for e in ecoSDS if e.endswith(tuple(sds))]
        if ecoSDS == []:
            print('No matching SDS layers found for {}'.format(e))
            continue
# ---------------------------------CONVERT SWATH DATA TO GRID------------------------------------ #
    # ALEXI products already gridded, bypass below
    if 'ALEXI_USDA' in e:
        cols, rows, dims = 3000, 3000, (3000, 3000)
        ecoSDS = [s for s in ecoSDS if f[s].shape == dims]  # Omit NA layers/objs
        if ecoSDS == []:
            print('No matching SDS layers found for {}'.format(e))
            continue
    else:
# ---------------------------------IMPORT GEOLOCATION FILE--------------------------------------- #
        geo = [g for g in geoList if e[-37:-10] in g]  # Match GEO filename--updated to exclude build ID
        if len(geo) != 0 or 'L1B_MAP' in e:         # Proceed if GEO/MAP file
            if 'L1B_MAP' in e:
                g = f                               # Map file contains lat/lon
            else:
                g = h5py.File(geo[0], "r")               # Read in GEO file
            geo_objs = []
            g.visit(geo_objs.append)

            # Search for relevant SDS inside data file
            latSD = [str(o) for o in geo_objs if isinstance(g[o], h5py.Dataset) and '/latitude' in o]
            lonSD = [str(o) for o in geo_objs if isinstance(g[o], h5py.Dataset) and '/longitude' in o]
            lat = g[latSD[0]][()].astype(float)  # Open Lat array
            lon = g[lonSD[0]][()].astype(float)  # Open Lon array
            dims = lat.shape
            ecoSDS = [s for s in ecoSDS if f[s].shape == dims]  # Omit NA layers/objs
            if ecoSDS == []:
                print('No matching SDS layers found for {}'.format(e))
                continue
# --------------------------------SWATH TO GEOREFERENCED ARRAYS---------------------------------- #
            swathDef = geom.SwathDefinition(lons=lon, lats=lat)
            midLat, midLon = np.mean(lat), np.mean(lon) 

            if crsIN == 'UTM':
                if args.utmzone is None:
                    epsg = utmLookup(midLat, midLon)  # Determine UTM zone that center of scene is in
                else:
                    epsg = args.utmzone
                epsgConvert = pyproj.Proj("+init=EPSG:{}".format(epsg))
                proj, pName = 'utm', 'Universal Transverse Mercator'
                projDict = {'proj': proj, 'zone': epsg[-2:], 'ellps': 'WGS84', 'datum': 'WGS84', 'units': 'm'}
                if epsg[2] == '7':
                    projDict['south'] = 'True'  # Add for s. hemisphere UTM zones
                llLon, llLat = epsgConvert(np.min(lon), np.min(lat), inverse=False)
                urLon, urLat = epsgConvert(np.max(lon), np.max(lat), inverse=False)
                areaExtent = (llLon, llLat, urLon, urLat)
                ps = 70  # 70 is pixel size (meters)

            if crsIN == 'GEO':
                # Use info from aeqd bbox to calculate output cols/rows/pixel size
                epsgConvert = pyproj.Proj("+proj=aeqd +lat_0={} +lon_0={}".format(midLat, midLon))
                llLon, llLat = epsgConvert(np.min(lon), np.min(lat), inverse=False)
                urLon, urLat = epsgConvert(np.max(lon), np.max(lat), inverse=False)
                areaExtent = (llLon, llLat, urLon, urLat)
                cols = int(round((areaExtent[2] - areaExtent[0])/70))  # 70 m pixel size
                rows = int(round((areaExtent[3] - areaExtent[1])/70))
                '''Use no. rows and columns generated above from the aeqd projection
                to set a representative number of rows and columns, which will then be translated
                to degrees below, then take the smaller of the two pixel dims to determine output size'''
                epsg, proj, pName = '4326', 'longlat', 'Geographic'
                llLon, llLat, urLon, urLat = np.min(lon), np.min(lat), np.max(lon), np.max(lat)
                areaExtent = (llLon, llLat, urLon, urLat)
                projDict = pyproj.CRS("epsg:4326")
                areaDef = geom.AreaDefinition(epsg, pName, proj, projDict, cols, rows, areaExtent)
                ps = np.min([areaDef.pixel_size_x, areaDef.pixel_size_y])  # Square pixels

            cols = int(round((areaExtent[2] - areaExtent[0])/ps))  # Calculate the output cols
            rows = int(round((areaExtent[3] - areaExtent[1])/ps))  # Calculate the output rows
            areaDef = geom.AreaDefinition(epsg, pName, proj, projDict, cols, rows, areaExtent)
            index, outdex, indexArr, distArr = kdt.get_neighbour_info(swathDef, areaDef, 210, neighbours=1)
        else:
            print('ECO1BGEO File not found for {}'.format(e))
            continue

# ------------------LOOP THROUGH SDS CONVERT SWATH2GRID AND APPLY GEOREFERENCING----------------- #
    for s in ecoSDS:
        ecoSD = f[s][()]  # Create array and read dimensions
        
        # Scale factor and add offset attribute names updated in build 6, accounted for below:
        scaleName = [a for a in f[s].attrs if 'scale' in a.lower()] # '_Scale' or 'scale_factor'
        addoffName = [a for a in f[s].attrs if 'offset' in a.lower()]
        
        # Read SDS Attributes if available
        try:
            fv = int(f[s].attrs['_FillValue'])
        except KeyError:
            fv = None
        except ValueError:
            if f[s].attrs['_FillValue'] == b'n/a':
                fv = None
            elif type(f[s].attrs['_FillValue'][0]) == np.float32:
                fv = np.nan
            else:
                fv = f[s].attrs['_FillValue'][0]
        try:
            sf = f[s].attrs[scaleName[0]][0]
        except:
            sf = 1
        try:
            add_off = f[s].attrs[addoffName[0]][0]
        except:
            add_off = 0

        # Convert to brightness temperature if bt argument is set, product is L1B, and SDS is Radiance
        if args.bt and 'RAD' in e:
            if 'radiance' in s:
                ecoSD = btConversion(s, ecoSD)
        
        if 'ALEXI_USDA' in e:  # USDA Contains proj info in metadata
            if 'ET' in e:
                metaName = 'L3_ET_ALEXI Metadata'
            else:
                metaName = 'L4_ESI_ALEXI Metadata'
            gt = f[f"{metaName}/Geotransform"][()]
            proj = f['{}/OGC_Well_Known_Text'.format(metaName)][()].decode('UTF-8')
            sdGEO = ecoSD
        else:
            try:
                # Perform kdtree resampling (swath 2 grid conversion)
                sdGEO = kdt.get_sample_from_neighbour_info('nn', areaDef.shape, ecoSD, index, outdex, indexArr, fill_value=fv)
                ps = np.min([areaDef.pixel_size_x, areaDef.pixel_size_y])
                gt = [areaDef.area_extent[0], ps, 0, areaDef.area_extent[3], 0, -ps]
            except ValueError:
                continue

        # Apply Scale Factor and Add Offset
        sdGEO = sdGEO * sf + add_off

        # Set fill value
        if fv is not None:
            sdGEO[sdGEO == fv * sf + add_off] = fv
                
# -------------------------------------EXPORT GEOTIFFS------------------------------------------- #
        # For USDA, export to UTM, then convert to GEO
        if 'ALEXI_USDA' in e and crsIN == 'GEO':
            tempName = '{}{}_{}_{}.tif'.format(outDir, ecoName, s.rsplit('/')[-1], 'TEMP')
            outName = tempName
        elif args.bt and 'RAD' in e and 'radiance' in s:
            outName = '{}{}_{}_{}.tif'.format(outDir, ecoName, s.rsplit('/')[-1], crsIN).replace('radiance', 'brightnesstemperature')
        else:
            outName = '{}{}_{}_{}.tif'.format(outDir, ecoName, s.rsplit('/')[-1], crsIN)

        # Get driver, specify dimensions, define and set output geotransform
        height, width = sdGEO.shape  # Define geotiff dimensions
        driv = gdal.GetDriverByName('GTiff')
        dataType = gdal_array.NumericTypeCodeToGDALTypeCode(sdGEO.dtype)
        d = driv.Create(outName, width, height, 1, dataType)
        d.SetGeoTransform(gt)

        # Create and set output projection, write output array data
        if 'ALEXI_USDA' in e:
            d.SetProjection(proj)
        else:
            # Define target SRS
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(int(epsg))
            d.SetProjection(srs.ExportToWkt())
        band = d.GetRasterBand(1)
        band.WriteArray(sdGEO)

        # Define fill value if it exists, if not, set to mask fill value
        if fv is not None and fv != 'NaN':
            band.SetNoDataValue(fv)
        else:
            try:
                band.SetNoDataValue(int(sdGEO.fill_value))
            except AttributeError:
                pass
            except TypeError:
                pass
            
        band.FlushCache()
        d, band = None, None

        if 'ALEXI_USDA' in e and crsIN == 'GEO':
            # Define target SRS
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(int('4326'))
            srs = srs.ExportToWkt()

            # Open temp file, get default vals for target dims & geotransform
            dd = gdal.Open(tempName, gdalconst.GA_ReadOnly)
            vrt = gdal.AutoCreateWarpedVRT(dd, None, srs, gdal.GRA_NearestNeighbour, 0.125)

            # Create the final warped raster
            outName = '{}{}_{}_{}.tif'.format(outDir, ecoName, s.rsplit('/')[-1], crsIN)
            d = driv.CreateCopy(outName, vrt)
            dd, d, vrt = None, None, None
            os.remove(tempName)
