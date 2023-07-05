# ECOSTRESS-Data-Resources

Welcome! This repository provides guides, short how-tos, and tutorials to help users access and work with data from the Global Ecosystem Dynamics Investigation (GEDI) mission. In the interest of open science this repository has been made public but is still under active development. All jupyter notebooks and scripts should be functional, however, changes or additions may be made. Contributions from all parties are welcome.


> Please note that in the interest of open science this repository has been made public but is still under active development. 

---

## ECOSTRESS Background  

The Global Ecosystem Dynamics Investigation ([GEDI](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/gedi-overview/)) mission aims to characterize ecosystem structure and dynamics to enable radically improved quantification and understanding of the Earth's carbon cycle and biodiversity. [GEDI](https://gedi.umd.edu/mission/mission-overview/) Level 1 and Level 2 Data Products are distributed by the Land Processes Distributed Active Archive Center ([LP DAAC][https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/gedi-overview/]) and Level 3 and Level 4 Data Products are distributed by the [ORNL DAAC]([https://daac.ornl.gov/cgi-bin/dataset_lister.pl?p=40]).

Search for and download GEDI _Version 2_ data products via a graphical user interface (GUI) using [NASA EarthData Search](https://search.earthdata.nasa.gov/search?q=%22GEDI%22) or programmatically using NASA's [Common Metadata Repository](https://cmr.earthdata.nasa.gov/search) (CMR).


---

## ECOSTRESS V2 Data Products: 

At the time of prepration of this repository the ECOSTRESS V2 data products listed below are publicly available. More V2 data products will become available in the future. View [LP DAAC Search Data Catalog](https://lpdaac.usgs.gov/product_search/?collections=ECOSTRESS&status=Operational&view=cards&sort=title&page=1&per_page=30) for complete list of ECOSTREES data products.

### ECOSTRESS V2 Swath data:

- **ECOSTRESS Swath Attitude and Ephemeris Instantaneous L1B Global - [ECO_L1B_ATT.002](https://doi.org/10.5067/ECOSTRESS/ECO_L1B_ATT.002)**
- **ECOSTRESS Swath Geolocation Instantaneous L1B Global 70 m - [ECO_L1B_GEO.002](https://doi.org/10.5067/ECOSTRESS/ECO_L1B_GEO.002)**
- **ECOSTRESS Swath Top of Atmosphere Calibrated Radiance Instantaneous L1B Global 70 m - [ECO_L1B_RAD.002](https://doi.org/10.5067/ECOSTRESS/ECO_L1B_RAD.002)**
- **ECOSTRESS Swath Cloud Mask Instantaneous L2 Global 70 m - [ECO_L2_CLOUD.002](https://doi.org/10.5067/ECOSTRESS/ECO_L2_CLOUD.002)**
- **ECOSTRESS Swath Land Surface Temperature and Emissivity Instantaneous L2 Global 70 m - [ECO_L2_LSTE.002](https://doi.org/10.5067/ECOSTRESS/ECO_L2_LSTE.002)**


### ECOSTRESS V2 Tiled data:

- **ECOSTRESS Tiled Top of Atmosphere Calibrated Radiance Instantaneous L1C Global 70 m - [ECO_L1CT_RAD.002](https://doi.org/10.5067/ECOSTRESS/ECO_L1CT_RAD.002)**
- **ECOSTRESS Tiled Land Surface Temperature and Emissivity Instantaneous L2 Global 70 m - [ECO_L2T_LSTE.002](https://doi.org/10.5067/ECOSTRESS/ECO_L2T_LSTE.002)**

### ECOSTRESS V2 Gridded data:

- **ECOSTRESS Gridded Top of Atmosphere Calibrated Radiance Instantaneous L1C Global 70 m - [ECO_L1CG_RAD.002](https://doi.org/10.5067/ECOSTRESS/ECO_L1CG_RAD.002)**
- **ECOSTRESS Gridded Cloud Mask Instantaneous L2 Global 70 m - [ECO_L2G_CLOUD.002](https://doi.org/10.5067/ECOSTRESS/ECO_L2G_CLOUD.002)**
- **ECOSTRESS Gridded Land Surface Temperature and Emissivity Instantaneous L2 Global 70 m - [ECO_L2G_LSTE.002](https://doi.org/10.5067/ECOSTRESS/ECO_L2G_LSTE.002)**

---

## Requirements  

+ Earthdata Login Authentication is required to access data. If you do not have an account, create an account [here](https://urs.earthdata.nasa.gov/users/new).

---

## Prerequisites/Setup Instructions  

Instructions for setting up a compatible environment for working with ECOSTRESS data is linked below.
- [`Python` set up instructions](setup/setup_instructions_python.md)

---
## Getting Started  

### Clone or download the [AppEEARS-Data-Resources repository](https://github.com/nasa/AppEEARS-Data-Resources).  

- [Download](https://github.com/nasa/AppEEARS-Data-Resources/archive/refs/heads/main.zip)  
- To clone the repository, type `git clone https://github.com/nasa/AppEEARS-Data-Resources.git` in the command line.  
---

## Repository Contents

Content in this repository includes Python tutorials, how-tos, scripts, defined modules that will be called from the Python resources, and setup instructions. The supporting files for use cases are stored in `Data` folder.  


> Python resources stored in this repositories are listed below:  


| Repository Contents | Type | Summary | 
|----|-----|----|
| **[]()** | Jupyter Notebook | Demonstrates how to 
| **[.ipynb]()** | Jupyter Notebook | Demonstrates how to  


---

## Helpful Links    

+ [ECOSTRESS Collection Overview](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/ecostress-overview/)
+ [ECOSTRESS Website](https://appeears.earthdatacloud.nasa.gov/products)
+ [AppEEARS Website](https://appeears.earthdatacloud.nasa.gov/)
+ [LP DAAC Website](https://lpdaac.usgs.gov/)
+ [LP DAAC GitHub](https://github.com/nasa/LPDAAC-Data-Resources)

---

## Contact Info:  

Email: LPDAAC@usgs.gov  
Voice: +1-866-573-3222  
Organization: Land Processes Distributed Active Archive Center (LP DAAC)¹  
Website: <https://lpdaac.usgs.gov/>  
Date last modified: 7-3-2023  

¹Work performed under USGS contract G15PD00467 for NASA contract NNG14HH33I.  
