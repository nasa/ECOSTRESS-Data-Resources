"""
===============================================================================
This script contains a workflow to extract the Geolocation Accuracy QA flag 
from ECOSTRESS L1B_GEO file level metadata.

-------------------------------------------------------------------------------                        
Authors: Mahsa Jami, Erik Bolch
Contact: lpdaac@usgs.gov                                                   
Last Updated: 2024-12-27                                    
===============================================================================
"""
# Import necessary packages
import earthaccess
import pandas as pd
import xarray as xr
import argparse
import os
from dask.distributed import Client
from dask import delayed
import dask.array as da
from colorama import Fore, Back, Style
import multiprocessing
import warnings

# Suppress the specific UserWarning
warnings.filterwarnings("ignore", message="Creating scratch directories is taking a surprisingly long time.")

# ----------------------------------USER-DEFINED VARIABLES--------------------------------------- #

if __name__ == "__main__":
    multiprocessing.freeze_support()

    # Set up argument 
    parser = argparse.ArgumentParser(description='Extract the gelocation accuracy QA flag')
    parser.add_argument('-dir', '--directory', required=True, help='Specify directory to save files to')
    parser.add_argument('-f', '--files', required=True, help='A single granule URL, or the location of csv or textfile containing granule URLs')

    args = parser.parse_args()

    saveDir = args.directory  # Set local directory to save file to
    files = args.files        # Define granules that their geolocation flags are needed

    # ---------------------------------SET UP WORKSPACE---------------------------------------------- #

    # Create a list of granule IDs based on input type of files above
    if files.endswith('.txt') or files.endswith('.csv'):
        with open(files, 'r') as f:
            fileList = f.read().splitlines() # If input is text/csv file with file URLs

        out_name = f"{files.rsplit('.',1)[0]}_geolocation_flag.csv"
    elif isinstance(files, str):
        fileList = [files]                       # If input is a single file
        out_name = f"{files.rsplit('/',1)[1].rsplit('.')[0]}_geolocation_flag.csv"

    if not fileList:
        print(Fore.RED + "Error: No granules provided in the input file.")
        exit(1)

    # Check if the directory exists
    if not os.path.isdir(saveDir): 
        os.makedirs(saveDir)

    out_dir = os.path.join(saveDir, out_name)

    # --------------------------------AUTHENTICATION CONFIGURATION----------------------------------- #
    # AUthenticate using earthaccess.login function. 

    earthaccess.login(persist = True) 
    fs = earthaccess.get_fsspec_https_session()
    print(Fore.GREEN + 'Please note: If you just entered your Earthdata Login credentials, your username and password are now stored in a .netrc file located in your home directory on this system.')    
    print(Style.RESET_ALL)

    # ------------------------------------------------------------------------------- #

    def get_geolocation_label(fs, granID_db, f):
        # print(f'Working on {f}')
        if 'ECOv002_' in f:
            id = [f for f in f.rsplit('/', 1)[1].rsplit('_') if len(f)==15 and '.' not in f][0]
            
            if id in list(granID_db['id']):
                pr = granID_db[granID_db['id'] == id].iloc[0]
                row =  pd.DataFrame({'granule': [f],'L1B_GEO': pr['L1B_GEO'], 'id': [id], 
                                    'GeolocationAccuracyQA': pr['GeolocationAccuracyQA']}, index=[0])
            else:
                response = earthaccess.search_data(short_name="ECO_L1B_GEO",version='002',granule_name = f'*{id}*')
                # get the L1B_GEO access URL
                url = [out['URL'] for out in response[0]['umm']['RelatedUrls'] if out['Type']  == 'GET DATA']
                fp = fs.open(url[0])
                l1geo = xr.open_dataset(fp, engine='h5netcdf', group='L1GEOMetadata')
                try:
                    label = l1geo['GeolocationAccuracyQA'].data.item()
                except:
                    label = 'missing'
 
                row =  pd.DataFrame({'granule': [f],'L1B_GEO': [url[0].rsplit('/')[-1]], 'id': [id], 'GeolocationAccuracyQA': [label] })
        else:
            row =  pd.DataFrame()
        
        return(row)
        
    # -----------------------------------------GET THE LIST OF GRANULE ID(S)-------------------------------------- #
    # Initialize an empty DataFrame for granule data
    granID_db = pd.DataFrame(columns=['granule','L1B_GEO','id' ,'GeolocationAccuracyQA'])

    # # Run the script without dask
    # for f in fileList:
    #     granID_db = get_geolocation_label(fs, granID_db, f) 

    # ------------------------------------------------------------------------------------------------------------- #
    # Set up Dask client
    client = Client(dashboard_address=":0")

    # Set up parallel tasks
    get_geolocation_label_parallel = delayed(get_geolocation_label)
    tasks = [get_geolocation_label_parallel(fs, granID_db, f) for f in fileList]

    # Perform computations and combine results
    results = da.compute(*tasks)
    granID_db = pd.concat(results, ignore_index=True)

    # -----------------------------------------SAVE THE DATABASE AS AN OUTPUT-------------------------------------- #
    # Remove 'id' column if it exists
    if 'id' in granID_db.columns:
        del granID_db['id']

    # Check if the DataFrame is empty
    if granID_db.empty:
        print(Fore.RED + "Please note that there is no geolocation accuracy QA flag for your input data. This flag is not available for ECOSTRESS version 1 data collections.")
    else:
        # Save the DataFrame to a CSV file
        granID_db.to_csv(out_dir, index=False)
        print(Fore.RED + f'The output CSV file is stored at: {out_dir}')
        print(Style.RESET_ALL)