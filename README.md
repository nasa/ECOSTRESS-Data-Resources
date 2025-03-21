# ECOSTRESS-Data-Resources

Welcome! This repository provides guides, short how-tos, and tutorials to help users access and work with data from the Ecosystem Spaceborne Thermal Radiometer Experiment on Space Station ([ECOSTRESS](https://ecostress.jpl.nasa.gov/)) mission distributed by the Land Processes Distributed Active Archive Center ([LP DAAC](https://lpdaac.usgs.gov/)). In the interest of open science this repository has been made public but is still under active development. All jupyter notebooks and scripts should be functional, however, changes or additions may be made. Contributions from all parties are welcome.

---

## ECOSTRESS Background  

The ECOsystem Spaceborne Thermal Radiometer Experiment on Space Station ([ECOSTRESS](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/#ECOSTRESS_anchor)) is aboard the International Space Station (ISS) and measures the temperature of plants to better understand how much water plants need and how they respond to stress. ECOSTRESS was launched to the ISS on June 29, 2018. It has a viewing swath width of around 384 km and views the surface of the Earth from 53.6° N latitude to 53.6° S latitude with variable revisit times, dependent on the orbit of the ISS.

ECOSTRESS addresses three overarching science questions: How is the terrestrial biosphere responding to changes in water availability? How do changes in diurnal vegetation water stress impact the global carbon cycle? Can agricultural vulnerability be reduced through advanced monitoring of agricultural water consumptive use and improved drought estimation? ECOSTRESS uses a multispectral thermal infrared radiometer to measure the surface temperature. The radiometer obtains detailed images of the Earth’s surface at ~70 m spatial resolution that can provide information on the temperature of an individual farmer’s field. Learn more on the [ECOSTRESS website](https://ecostress.jpl.nasa.gov/).

ECOSTRESS Data Products are distributed by the [LP DAAC](https://lpdaac.usgs.gov/). Learn more about ECOSTRESS data products from [ECOSTRESS Product Pages](https://lpdaac.usgs.gov/product_search/?query=ECOSTRESS&status=Operational&view=cards&sort=title&page=1&per_page=30) and search for and download ECOSTRESS data products using [NASA EarthData Search](https://search.earthdata.nasa.gov/search?q=ECOSTRESS) or programmatically using NASA's [Common Metadata Repository](https://cmr.earthdata.nasa.gov/search)(CMR).

---

## Prerequisites/Setup Instructions  

Instructions for setting up a compatible environment for working with ECOSTRESS data is linked below.
- [`Python` set up instructions](https://github.com/nasa/LPDAAC-Data-Resources/tree/main/setup/setup_instructions_python.md)

---
## Getting Started  

Clone or download the [ECOSTRESS-Data-Resources repository](https://github.com/nasa/ECOSTRESS-Data-Resources).  

- [Download](https://github.com/nasa/ECOSTRESS-Data-Resources/archive/refs/heads/main.zip)  
- To clone the repository, type `git clone https://github.com/nasa/ECOSTRESS-Data-Resources.git` in the command line.  

---
## Repository Contents

Content in this repository includes Python tutorials, how-tos, scripts, defined modules that will be called from the Python resources, and setup instructions. The supporting files for use cases are stored in `Data` folder.  
> Resources stored in this repository are listed below:  

| Repository Contents | Type | Summary | 
|----|-----|----|
| **[earthdata_search_ecostress.md](/guides/earthdata_search_ecostress.md)** | Markdown Guide | Demonstrates how to work with Earthdata Search to access ECOSTRESS data|
| **[appeears_ecostress.md](/guides/appeears_ecostress.md)** | Markdown Guide | Demonstrates how to work with AppEEARS to access and transform ECOSTRESS data|
| **[how_to_stream_http_access_ecostress_cog.ipynb](/python/how-tos/how_to_stream_http_access_ecostress_cog.ipynb)** | Jupyter Notebook | Demonstrates how to stream ECOSTRESS COG data from the Earthdata Cloud|
| **[how_to_direct_s3_access_ecostress_cog.ipynb](/python/how-tos/how_to_direct_s3_access_ecostress_cog.ipynb)** | Jupyter Notebook | Demonstrates how to directly access ECOSTRESS COG data from the Earthdata Cloud|
| **[ECOSTRESS_Tutorial.ipynb](/python/tutorials/ECOSTRESS_Tutorial.ipynb)** | Jupyter Notebook | Demonstrates how to work with the ECOSTRESS Evapotranspiration PT-JPL Daily L3|
| **[ECOSTRESS_swath2grid.py](/python/scripts/ecostress_swath2grid)** | Command line executable | Demonstrates how to convert ECOSTRESS swath data products into projected GeoTIFFs|
| **[ECOSTRESS_geolocation.py](/python/scripts/extract_geolocation_flag)** | Command line executable | Demonstrates how to extract `GeolocationAccuracyQA` flag for ECOSTRESS version 2 data|

---

## Helpful Links    

+ [ECOSTRESS Collection Overview](https://lpdaac.usgs.gov/data/get-started-data/collection-overview/missions/ecostress-overview/)
+ [2023 ECOSTRESS Science and Applications Team Meeting Workshop Recording](https://ecostress.jpl.nasa.gov/downloads/science_team_meetings/2023/workshopvid.mp4)
+ [ECOSTRESS Website](https://ecostress.jpl.nasa.gov/)
+ [AppEEARS Website](https://appeears.earthdatacloud.nasa.gov/)
+ [LP DAAC Website](https://lpdaac.usgs.gov/)
+ [LP DAAC GitHub](https://github.com/nasa/LPDAAC-Data-Resources)

---

## Contact Info:  

Email: LPDAAC@usgs.gov  
Voice: +1-866-573-3222  
Organization: Land Processes Distributed Active Archive Center (LP DAAC)¹  
Website: <https://lpdaac.usgs.gov/>  
Date last modified: 02-03-2025  

¹Work performed under USGS contract G15PD00467 for NASA contract NNG14HH33I.  
