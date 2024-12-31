
# Extract ECOSTRESS Geolocation Accuracy QA Flag

## Objective

NASA's Land Processes Distributed Active Archive Center (LP DAAC) is responsible for archiving and distributing ECOSTRESS data products through the LP DAAC Cumulus cloud archive. ECOSTRESS Version 2 data is available in swath, gridded, and tiled formats, provided in both Cloud Optimized GeoTIFF (COG) and HDF5 file formats. ECOSTRESS Swath Geolocation data ([ECO_L1B_GEO v002](https://doi.org/10.5067/ECOSTRESS/ECO_L1B_GEO.002)) includes essential metadata fields, such as the `Geolocation Accuracy QA` flag, which are not carried over to higher-level data products. `Geolocation Accuracy QA` flag provides an indication of geolocation error. The gelocation accuracy for corrected data could be better than 50 meters but the data was processed without correcting the geolocation could have up to 7 km geolocation error. Users of ECOSTRESS data should evaluate the geolocation accuracy and whether larger errors can be tolerated for their applications. Otherwise, data flagged as “Suspect” or “No Match” may not be suitable for you. Additional details are provided in Section 4.2 of the [User Guide](https://lpdaac.usgs.gov/documents/1491/ECO1B_User_Guide_V2.pdf). 

> `Geolocation Accuracy QA` could have four different flags: 

>- **Best**: Image matching was performed for this scene. Good geolocation accuracy.
>- **Good**: Image matching was performed in a nearby scene. Good geolocation accuracy.
>- **Suspect**: Image matching occurred somewhere in the orbit. Expect increased error.
>- **No Match**: No matches in orbit. Expect large geolocation errors.

This Python-based command-line script enables users to retrieve the `Geolocation Accuracy QA` flags for the input data. Input data can be provided as:  
1. A list of download URLs or granule filenames stored in a text or CSV file.
2. A download URL or granule filename as a string for a single file.

The script automates the retrieval process, allowing users to efficiently determine the geolocation accuracy of their ECOSTRESS data products. Retrieved geolocation flags will be stored as a .csv file. 

## Products  

This script works with all the ECOSTRESS version 2 data products.  

## Prerequisites/Setup Instructions  

### Environment Setup 

If you do not have an Environment Manager installed, we recommend [mamba](https://mamba.readthedocs.io/en/latest/) to manage Python packages. Details instruction on how to install an environment manager can be found [here](https://github.com/nasa/LPDAAC-Data-Resources/blob/main/setup/setup_instructions_python.md). Once you have it installed, type the following in your preferred command line interface (command prompt, terminal, cmder, etc.) to create a compatible environment.

```
mamba create -n ecostress_geo python=3.9 earthaccess dask xarray h5netcdf 
```
**If you are using conda, replace the "mamba" with "conda" and be patient.**

Instruction for setting up a compatible environment for all LP DAAC Python resources is available at: <https://github.com/nasa/LPDAAC-Data-Resources/blob/main/setup/setup_instructions_python.md>

### NASA Earthdata Login:

**You will need a NASA Earthdata Login account to access LP DAAC data (and use this script).** To create a NASA Earthdata Login account, go to the [Earthdata Login website](https://urs.earthdata.nasa.gov) and click the “Register” button, which is next to the green “Log In” button under the Password entry box. Fill in the required boxes (indicated with a red asterisk), then click on the “Register for Earthdata Login” green button at the bottom of the page. An email including instructions for activating your profile will be sent to you. Activate your profile to complete the registration process.

### **.netrc file**

The netrc file is needed to download NASA Earthdata science data from a scripting environment like Python. There are multiple methods to [create a .netrc file for authntication](https://github.com/nasa/LPDAAC-Data-Resources/tree/main/guides/create_netrc_file.md). Here, the `earthaccess` package is used to automatically create a `.netrc` file using your Earthdata login credentials. If you do not have a netrc file configured in your home directory, the script will prompt you for input on your NASA Earthdata Login Username and Password. Enter your username and password and hit enter to continue downloading your data. **Please note that your Earthdata Login info, your username, and password, will be stored in a .netrc file located in the Home directory on this system you are using.** You will get the same message when you run the script as a reminder. If you do not trust the machine you are using, make sure to delete the created netrc file.   

## Procedures:

### Getting Started:

#### 1. Save the download URL for your data from  [NASA Earthdata Search](https://search.earthdata.nasa.gov/) for a single file. For multiple files, download the text file containing URLs to files.   

#### 2. Access `ECOSTRESS_geolocation.py` from `ECOSTRESS-Data-Resources` Github Repository.   

You can download the raw file for the script from <https://github.com/nasa/ECOSTRESS-Data-Resources/tree/main/python/scripts/extract_geolocation_flag/ECOSTRESS_geolocation.py> 
   
Additionally, you can download all contents of this repository as a [zip file](https://github.com/nasa/ECOSTRESS-Data-Resources/archive/refs/heads/main.zip). You can also clone the repository by typing the following into command line.

```bash
git clone https://github.com/nasa/ECOSTRESS-Data-Resources.git
```

Afterwards, navigate to `python/scripts/extract_geolocation_flag/ECOSTRESS_geolocation.py`.  

## Script Execution

Activate your MacOS/Windows environment, run the script with the following in your Command Prompt/terminal window:

```cmd
python ECOSTRESS_geolocation.py -dir <insert local directory to save output file to> -f <insert a single granule URL, or the location of a csv or text file containing granule URLs>
```

**Example 1, extracting the geolocation flag for a list of ECOSTESS files:**

```cmd
python C:\User\Downloads\ECOSTRESS_geolocation.py -dir C:\User\downloads -f C:\User\downloads\ECOSTRESS-granule-list.txt
```

**Example 2, extracting the geolocation flags for a single ECOSTRESS file:**

```cmd
python C:\User\Downloads\DAACDataDownload.py  -dir C:\User\downloads -f https://data.lpdaac.earthdatacloud.nasa.gov/lp-prod-protected/ECO_L4T_ESI.002/ECOv002_L4T_ESI_36662_013_07LFK_20241223T220254_0713_01/ECOv002_L4T_ESI_36662_013_07LFK_20241223T220254_0713_01_water.tif
```


---
## Contact Information
### Author: LP DAAC <sup>1</sup>  

**Contact:** LPDAAC@usgs.gov  
**Voice:** +1-866-573-3222  
**Organization:** Land Processes Distributed Active Archive Center (LP DAAC)  
**Website:** <https://lpdaac.usgs.gov/>  
**Date last modified:** 11-21-2022  

<sup>1</sup>LP DAAC Work performed under NASA contract NNG14HH33I.
