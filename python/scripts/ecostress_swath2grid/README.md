
# ECOSTRESS Swath to Grid Conversion Script

## Objective

The ECOSTRESS_swath2grid.py script converts ECOSTRESS swath data products, stored in Hierarchical Data Format version 5 (HDF5, .h5) into projected GeoTIFFs. When executing this script, a user will submit a desired output projection and input directory containing ECOSTRESS swath data products as command line arguments. The script begins by opening any of the ECOSTRESS products listed below that are contained in the input directory. Next, it uses the latitude and longitude arrays from the ECO1BGEO product (except for L3/L4 ALEXI_USDA and ECO1BMAPRAD products) to resample the swath dataset to a grid using nearest neighbor resampling (`Pyresample/kdtree`). Note that you will need to download the ECO1BGEO files that correspond to your higher level product files. From there, the script defines the coordinate reference system (CRS) input by the user (options include UTM Zones and Geographic (EPSG:4326)). There is an optional argument to override the default UTM zone selected by the script (see below) if needed. Ultimately, the script exports the gridded array as a GeoTIFF (`GDAL`). By default, the script will loop through and perform the aforementioned steps for each science dataset (SDS) in the HDF5 file. There is an optional argument that allows you to select a subset of SDS layers within a given product (see details below). There is another optional argument that allows users to convert L1B radiance to brightness temperature. The resulting GeoTIFF files can be imported with spatial reference into GIS and Remote Sensing software programs. The script also will batch process all ECOSTRESS swath files contained in the input directory provided. For ECOSTRESS products that include a scale factor in the metadata, the output will be scaled, and for products that include a fill value in the file metadata, this will be carried over into the GeoTIFF outputs. For layers that do not contain a fill value in the file metadata, the fill value will be defined as the highest possible value for the given datatype of an SDS.  

## Available Products  

### Collection 1  

1. ECO1BGEO  
2. ECO1BMAPRAD (lat/lon arrays contained within, ECO1BGEO not needed; radiance can be converted to brightness temperature)  
3. ECO1BRAD  (radiance can be converted to brightness temperature)
4. ECO2CLD  
5. ECO2LSTE  
6. ECO3ETALEXIU (30 m, in UTM Projection, ECO1BGEO not needed)  
7. ECO3ETPTJPL  
8. ECO3ANCQA  
9. ECO4ESIPTJPL  
10. ECO4ESIALEXIU  (30 m, in UTM Projection, ECO1BGEO not needed)  
11. ECO4WUE  

### Collection 2  

1. ECO_L1B_GEO  
2. ECO_L1B_ATT  
3. ECO_L1B_RAD  
4. ECO_L2_LSTE  
5. ECO_L2_CLOUD  

> Note that you will need to separately download the ECO1BGEO files that correspond to the files you have downloaded for products 2-4, 6-8, and 10 above.  

## Prerequisites

> Disclaimer: Script has been tested on Windows and MacOS using the specifications identified below.  

+ **Python version 3.8**  
  + `GDAL`  
  + `h5py`  
  + `pyproj`  
  + `pyresample`  
  + `numpy`  
  + `pandas`  
  + `scipy`  

+ A [NASA Earthdata Login](https://urs.earthdata.nasa.gov/) account is required to download the data used in this tutorial. You can create an account at the link provided.  

## Procedures

### Getting Started

1. Download ECOSTRESS higher level products and corresponding ECO1BGEO files (ordered separately) from the [LP DAAC Data Pool](https://e4ftl01.cr.usgs.gov/ECOSTRESS/) or [Earthdata Search Client](https://search.earthdata.nasa.gov/search?fi=ECOSTRESS) to a local directory (see above for applicable products)  
2. Copy/clone/download  [ECOSTRESS_swath2grid.py](https://git.earthdata.nasa.gov/projects/LPDUR/repos/ecostress_swath2grid/browse/ECOSTRESS_swath2grid.py) from LP DAAC Data User Resources Repository  

### Python Environment Setup

1. It is recommended to use [Conda](https://conda.io/docs/), an environment manager to set up a compatible Python environment. Download Conda for your OS here: <https://www.anaconda.com/download/>. Once you have Conda installed, Follow the instructions below to successfully setup a Python environment on MacOS or Windows.  
2. Using your preferred command line interface (command prompt, terminal, cmder, etc.) type the following to successfully create a compatible python environment:  

    ```text
    > conda create -n ecostress -c conda-forge --yes python=3.8 h5py pyproj pyresample gdal pandas scipy  
    > conda activate ecostress  
    ```  

> NOTE: If you are having trouble activating your environment, or loading specific packages once you have activated your environment? Try entering `conda update conda` or `conda update --all`  

[Additional information](https://conda.io/docs/user-guide/tasks/manage-environments.html) on setting up and managing Conda environments.  

If you prefer to not install Conda, the same setup and dependencies can be achieved by using another package manager such as pip.  

Still having trouble getting a compatible Python environment set up? Contact [LP DAAC User Services](https://lpdaac.usgs.gov/lpdaac-contact-us/).  

## Script Execution

Once you have set up your MacOS/Windows environment and it has been activated, run the script with the following in your Command Prompt/terminal window:  

```text
> python ECOSTRESS_swath2grid.py --proj <insert reprojection desired, Options: GEO and UTM> --dir <insert input directory with ECOSTRESS files here>
```  

Where:  

+ GEO = Geographic lat/lon, EPSG code 4326  
+ UTM = Universal Transverse Mercator Zones (north/south) with WGS84 datum  

> NOTE: `--proj` argument is case sensitive  

**Example**  

```text
> python ECOSTRESS_swath2grid.py --proj GEO --dir C:\Users\ECOSTRESS\
```  

If UTM is selected, the script will calculate the UTM zone by using the location of the center of each ECOSTRESS granule. If you prefer to set the UTM zone manually, you can do so by adding the optional argument `--utmzone <insert EPSG code for desired zone>`. This optional argument will override the default functionality for users who desire all ECOSTRESS granules to be in a common UTM projection, regardless of the center location of the granule.  

**Example**  

```text
> python ECOSTRESS_swath2grid.py --proj UTM --dir <insert input directory with ECOSTRESS files here> --utmzone <insert EPSG code for desired UTM zone, e.g. 32610>  
```  

> NOTE: You can look up EPSG codes for UTM zones at: <http://spatialreference.org/>, note that only WGS84 datum is supported, and thus EPSG codes for UTM north zones will begin with `326` and utm south zones with `327`  

The default functionality is to export each science dataset (SDS) layer contained in an ECOSTRESS product as a GeoTIFF. If you prefer to only export one or more layers, you can do so by adding the optional argument `--sds <insert SDS layer names desired>` (comma separated with no spaces, see below for specific SDS layer names by product--note that the input is case sensitive)  

**Example**  

```text
> python ECOSTRESS_swath2grid.py --proj GEO --dir C:\Users\ECOSTRESS\ --sds LST,QC,Emis1  
```

> NOTE: SDS layer names for each product are below in section [Subsetting Layers](#subsetting-layers).  

The default functionality for L1B radiance is to export each layer contained as radiance (W/m^2/sr/um). If you prefer to export the L1B datasets as brightness temperature (K), you can do so by adding the optional argument `--bt` (see section [Radiance to Brightness Temperature Conversion](#radiance-to-brightness-temperature-conversion) for additional information)  

**Example**  

```text
> python ECOSTRESS_swath2grid.py --proj GEO --dir C:\Users\ECOSTRESS\ --bt`  
```  

## Radiance to Brightness Temperature Conversion

To use the `--bt` optional command line argument to convert L1B radiance science datasets (bands 1-5) from radiance (W/m^2/sr/um) to brightness temperature (K), you will need to add the `--bt` argument to your script execution command.
Example:  

```text
> python ECOSTRESS_swath2grid.py --proj GEO --dir C:\Users\ECOSTRESS\ --bt  
```  

> **Note:** You will first need to download the `EcostressBrightnessTemperatureV01.h5` Lookup Table (LUT) and save it to the directory containing your `ECOSTRESS_swath2grid.py` script, or the directory containing the ECOSTRESS L1B files to be processed.  

## Subsetting Layers

To use the `--sds` optional command line argument in order to select a subset of science datasets from an ECOSTRESS granule, you will need to submit 1 or more SDS layers names into the `--sds` argument exactly as they appear in the list below. **The SDS layers must be comma separated, with no spaces between SDS!**

+ Example for a single layer: `--sds LST`  
+ Example for multiple layers: `--sds ETcanopy,ETdaily,ETinst`  

## Available ECOSTRESS Layers

### Collection 1  

1. **ECO1BGEO**  
      + height  
      + land_fraction  
      + latitude  
      + longitude  
      + solar_azimuth  
      + solar_zenith  
      + view_azimuth  
      + view_zenith  

2. **ECO1BMAPRAD**  
      + data_quality_1
      + data_quality_2  
      + data_quality_3  
      + data_quality_4  
      + data_quality_5  
      + height  
      + latitude  
      + longitude  
      + radiance_1  (can be exported to brightnesstemperature_1)  
      + radiance_2  (can be exported to brightnesstemperature_2)  
      + radiance_3  (can be exported to brightnesstemperature_3)  
      + radiance_4  (can be exported to brightnesstemperature_4)  
      + radiance_5  (can be exported to brightnesstemperature_5)  
      + solar_azimuth  
      + solar_zenith  
      + swir_dn  
      + view_azimuth  
      + view_zenith  

3. **ECO1BRAD**  
      + data_quality_1  
      + data_quality_2  
      + data_quality_3  
      + data_quality_4  
      + data_quality_5  
      + radiance_1  (can be exported to brightnesstemperature_1)  
      + radiance_2  (can be exported to brightnesstemperature_2)  
      + radiance_3  (can be exported to brightnesstemperature_3)  
      + radiance_4  (can be exported to brightnesstemperature_4)  
      + radiance_5  (can be exported to brightnesstemperature_5)  
      + swir_dn  

4. **ECO2CLD**  
      + CloudMask  

5. **ECO2LSTE**  
      + Emis1  
      + Emis1_err  
      + Emis2  
      + Emis2_err  
      + Emis3  
      + Emis3_err  
      + Emis4  
      + Emis4_err  
      + Emis5  
      + Emis5_err  
      + EmisWB  
      + LST  
      + LST_err  
      + PWV  
      + QC  

6. **ECO3ETALEXIU**  
      + ETdaily  
      + ETdailyUncertainty  
      + QualityFlag  

7. **ECO3ETPTJPL**  
      + ETcanopy  
      + ETdaily  
      + ETinst  
      + ETinstUncertainty  
      + ETinterception  
      + ETsoil  

8. **ECO3ANCQA**  
      + ECOSTRESS_L2_QC  
      + Landsat8_QC  
      + MCD12Q1_QC  
      + MCD43A3_QC  
      + MOD04_QC  
      + MOD06_1km_QC  
      + MOD06_5km_QC  
      + MOD07_QC  
      + MOD13Q1_QC  
      + MOD17A2H_QC  
      + MOD44W_QC  

9. **ECO4ESIALEXIU**  
      + ESIdaily  
      + ESIdailyUncertainty  
      + QualityFlag  

10. **ECO4ESIPTJPL**  
      + ESIavg  
      + PET  

11. **ECO4WUE**  
      + WUEavg  

### Collection 2  

1. **ECO_L1B_GEO**  
      + height  
      + land_fraction  
      + latitude  
      + line_start_time_j2000  
      + longitude  
      + solar_azimuth  
      + solar_zenith  
      + view_azimuth  
      + view_zenith  

2. **ECO_L1B_ATT**  
      + Attitude quaternion  
      + Attitude time_j2000  
      + Ephemeris eci_position  
      + Ephemeris eci_velocity  
      + Ephemeris time_j2000  
      + Uncorrected Attitude quaternion  
      + Uncorrected Attitude time_j2000  
      + Uncorrected Ephemeris eci_position  
      + Uncorrected Ephemeris eci_velocity  
      + Uncorrected Ephemeris time_j2000  

3. **ECO_L1B_RAD**  
      + radiance_1  
      + radiance_2  
      + radiance_3  
      + radiance_4  
      + radiance_5  
      + data_quality_1  
      + data_quality_2  
      + data_quality_3  
      + data_quality_4  
      + data_quality_5  
      + swir_dn  
      + EncoderValue  
      + line_start_time_j2000  

4. **ECO_L2_LSTE**  
      + LST  
      + QC  
      + Emis1  
      + Emis2  
      + Emis3  
      + Emis4  
      + Emis5  
      + LST_err  
      + Emis1_err  
      + Emis2_err  
      + Emis3_err  
      + Emis4_err  
      + Emis5_err  
      + EmisWB  
      + PWV  
      + cloud_mask  
      + water_mask  
  
5. **ECO_L2_CLOUD**  
      + Cloud_confidence  
      + Cloud_final  

---
## Contact Information
### Author: LP DAAC <sup>1</sup>  

**Contact:** LPDAAC@usgs.gov  
**Voice:** +1-866-573-3222  
**Organization:** Land Processes Distributed Active Archive Center (LP DAAC)  
**Website:** <https://lpdaac.usgs.gov/>  
**Date last modified:** 11-21-2022  

<sup>1</sup>LP DAAC Work performed under NASA contract NNG14HH33I.
