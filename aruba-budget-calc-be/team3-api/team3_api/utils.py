import os
import requests
import json

import logging
import pandas as pd

log = logging.getLogger(__name__)



def get_catalog_dataframe(
        resource_type_list:list=["computing", "container", "networking", "storage"],
    ):
    """
    Returns a pandas dataframe containing pricing of Aruba cloud resources.
    In case a resource type is specified, data get extracted only for that resource.

    Args:
        resource_type_list (list): List containing resource type for which pricing is requested.

    Returns:
        pd.DataFrame: DataFrame containing a flattened view of the catalog.
    """

    # Load resources to pricing path mapping from json file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "collections.json")
    with open(json_file_path, "r") as f:
        catalog_collection = json.load(f)

    # Initialize empty dataframe to be filled iteratively
    df = pd.DataFrame()

    # Get data for each separate url, convert into dataframe and append
    for resource_type, pricing_url in catalog_collection.items():

        # Get pricing only for resources specified in input list
        if resource_type not in resource_type_list:
            continue

        # Request pricing catalog
        response = requests.get(pricing_url)

        # Check request status
        if response.status_code == 200:
            
            log.info(f"{resource_type} - getting data...")
            
            # Convert output to dictionary
            data = response.json()

            log.info(f"{resource_type} - parsing data...")
            
            # Parse dictionary into dataframe
            df_resource = parse_json_catalog_to_dataframe(
                json_catalog=data
            )
            
            df = pd.concat(
                [df, df_resource],
                axis=0
            )
            
        else:
            log.error(f"Error: {response.status_code}")

    return df


def parse_json_catalog_to_dataframe(
        json_catalog: list
    ) -> pd.DataFrame:
    """
    Converts Aruba JSON pricing catalog of resources into a pandas DataFrame, handling all missing or 
    incomplete data by setting appropriate default values where necessary.

    Args:
        json_catalog (list): Aruba JSON catalog containing resource details such as resource info,
                             flavor specifications, reservations, and discount tiers.

    Returns:
        pd.DataFrame: DataFrame containing a flattened view of the catalog.
    """

    records = []

    # Ensure the input is a list of items
    if not isinstance(json_catalog, list):
        print("Warning: Provided JSON catalog is not a list. Returning an empty DataFrame.")
        return pd.DataFrame()

    # Iterate over each item in the JSON to extract details
    for item in json_catalog:
        if not isinstance(item, dict):
            continue  # Skip non-dictionary entries

        # Basic resource information, with default values
        base_info = {
            "Resource ID": item.get("_id", "Unknown"),
            "Resource Name": item.get("resourceName", "Unknown"),
            "Category": item.get("resourceCategory", "Unknown"),
            "Currency": item.get("currencyCode", "Unknown"),
            "Unit of Measure": item.get("unitOfMeasure", "Unknown"),
            "Unit Price": item.get("unitPrice", 0.0)
        }
        
        # Flavor specifications with default values, checking if 'flavor' exists and is a dictionary
        flavor = item.get("flavor", {})
        if not isinstance(flavor, dict):
            flavor = {}  # Reset to an empty dict if 'flavor' is None or not a dictionary
        
        flavor_info = {
            "Flavor ID": flavor.get("id", "N/A"),
            "Flavor Name": flavor.get("name", "N/A"),
            "OS Platform": flavor.get("osPlatform", "N/A"),
            "CPU": flavor.get("cpu", "N/A"),
            "RAM (GB)": flavor.get("ram", "N/A"),
            "Disk (GB)": flavor.get("disk", "N/A")
        }
        
        # Process each reservation term and price, handling missing or non-list 'reservations'
        reservations = item.get("reservations", [])
        if not isinstance(reservations, list) or not reservations:
            reservations = [{"term": "N/A", "price": 0.0}]
        
        for reservation in reservations:
            if not isinstance(reservation, dict):
                reservation = {}  # Reset to an empty dict if not a dictionary

            reservation_info = {
                "Reservation Term": reservation.get("term", "N/A"),
                "Reservation Price": reservation.get("price", 0.0)
            }
            
            # Process each tier category and discount, handling missing or non-list 'tiers'
            tiers = item.get("tiers", [])
            if not isinstance(tiers, list) or not tiers:
                tiers = [{"category": "N/A", "minimumUnits": 0, "percentDiscount": 0.0}]
            
            for tier in tiers:
                if not isinstance(tier, dict):
                    tier = {}  # Reset to an empty dict if not a dictionary
                
                tier_info = {
                    "Tier Category": tier.get("category", "N/A"),
                    "Minimum Units for Tier": tier.get("minimumUnits", 0),
                    "Tier Discount (%)": tier.get("percentDiscount", 0.0)
                }
                
                # Combine all dictionaries into a single record
                record = {**base_info, **flavor_info, **reservation_info, **tier_info}
                records.append(record)

    # Create the DataFrame from the list of records
    df = pd.DataFrame.from_records(records)
    
    return df

