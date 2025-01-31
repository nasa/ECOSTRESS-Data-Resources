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
# from dask.distributed import Client
# from dask import delayed
# import dask.array as da
from colorama import Fore, Back, Style
import multiprocessing
import warnings
from tqdm import tqdm  # Import tqdm for the progress bar


# Suppress the specific UserWarning
warnings.filterwarnings("ignore", message="Creating scratch directories is taking a surprisingly long time.")

# ----------------------------------USER-DEFINED VARIABLES--------------------------------------- #
def get_link(id):
    """This function extract the associated ECO_L1B_GEO URL using date and time information."""
    attempts = 0
    url = ''
    while attempts < 3:
        try:
            response = earthaccess.search_data(short_name="ECO_L1B_GEO",version='002',granule_name = f'*{id}*')
            # print(response)
            # get the L1B_GEO access URL
            url = [granule.data_links(access="external") for granule in response]
            break
        except:
            attempts += 1     
    return(url)

def file_geolocation(url):
    """This function extract the GeolocationAccuracyQA flag from file metadata using xarray."""
    fs = earthaccess.get_fsspec_https_session()
    fp = fs.open(url)
    l1geo = xr.open_dataset(fp, engine='h5netcdf', group='L1GEOMetadata')
    try:
        label = l1geo['GeolocationAccuracyQA'].data.item()
    except:
        label = 'missing'
    return(label)

def dmrpp_geolocation(url):
    """This function extract the GeolocationAccuracyQA flag from .dmrpp metadata file."""
    try:
        response = requests.get(url)
        # print(response.raise_for_status())
        # Decode using ISO-8859-1
        xml_content = response.content.decode("ISO-8859-1")
        # Parse XML
        root = ET.fromstring(xml_content)

        for group in root.iter():
            if "Group" in group.tag:
                group_name = group.attrib.get("name", "Unnamed Group")
                if group_name == "L1GEOMetadata":
                    for elem in group.iter():
                        if "String" in elem.tag:
                            string = elem.attrib.get("name", "Unnamed Attribute")
                            if "GeolocationAccuracyQA" in string and "GeolocationAccuracyQAExplanation" not in string:
                                for e in elem.iter():
                                    encoded_value = e.text.strip()  # Remove extra spaces/newlines
                                    label = base64.b64decode(encoded_value).decode("utf-8", errors="ignore")
    except:
        label = 'failed'
    return(label)  
  

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

    auth = earthaccess.login(persist = True) 
    auth.refresh_tokens()
    # fs = earthaccess.get_fsspec_https_session()
    print(Fore.GREEN + 'Please note: If you just entered your Earthdata Login credentials, your username and password are now stored in a .netrc file located in your home directory on this system.')    
    print(Style.RESET_ALL)

    # ------------------------------------------------------------------------------- #
    def get_geolocation_label(granID_db, f):
        # print(f'Working on {f}')
        
        id = [f for f in f.rsplit('/', 1)[1].rsplit('_') if len(f)==15 and '.' not in f][0]
        # print(id)
        if id in list(granID_db['id']):
            pr = granID_db[granID_db['id'] == id].iloc[0]
            row =  pd.DataFrame({'granule': [f],'L1B_GEO': pr['L1B_GEO'], 'id': [id], 
                                    'GeolocationAccuracyQA': pr['GeolocationAccuracyQA'], 
                                    'note': pr['note']}, index=[0])       
        else:       
            if 'ECOv002_' in f:
                url = get_link(id)
                if url:
                    h5_link = [l for l in url[0] if l.endswith('.h5')][0]     
                    # print(h5_link)
                    dmrpp_link = f'{h5_link}.dmrpp'
                    label = dmrpp_geolocation(dmrpp_link)
                    if label == 'failed':
                        label = file_geolocation(h5_link)
                    # print(label)    
                    row =  pd.DataFrame({'granule': [f],'L1B_GEO': [h5_link.rsplit('/')[-1]], 'id': [id], 
                                         'GeolocationAccuracyQA': [label], 'note': '' })
                else:
                    # print(f'Failed to access ECO_L1B_GEO granule.')   
                    row =  pd.DataFrame({'granule': [],'L1B_GEO': [], 'id': [], 'GeolocationAccuracyQA': [], 
                                         'note': 'Failed to access ECO_L1B_GEO granule' })   
            else:
                print(f'{f} is not associated to the ECOSTRESS version 2 collections.') 
                row = pd.DataFrame() 
        return(row)
   
   
        
    # -----------------------------------------GET THE LIST OF GRANULE ID(S)-------------------------------------- #
    # Initialize an empty DataFrame for granule data
    granID_db = pd.DataFrame(columns=['granule','L1B_GEO','id' ,'GeolocationAccuracyQA', 'note'])

    # Run the script without dask

    # Add a progress bar to the loop
    for f in tqdm(fileList, desc="Processing files", unit="file"):
        if  f:
            row_db = get_geolocation_label(granID_db, f) 
            granID_db = pd.concat([granID_db, row_db], ignore_index=True)

    # ------------------------------------------------------------------------------------------------------------- #
    # # Set up Dask client
    # with Client() as client: #dashboard_address=":0"
    #     get_geolocation_label_parallel = delayed(get_geolocation_label)
    #     tasks = [get_geolocation_label_parallel(granID_db, f) for f in fileList if f]
        
    #     results = da.compute(*tasks)
    #     print(results)
      
    #     granID_db = pd.concat(results, ignore_index=True)

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