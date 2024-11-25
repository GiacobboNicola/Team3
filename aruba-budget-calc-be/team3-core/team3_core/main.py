import logging
import time

import json
import requests

from team3_lib.wamp import WampComponent

log = logging.getLogger(__name__)

PRICING_ENDPOINTS = {
    "computing": "https://catalog.r1-it.storage.cloud.it/catalog_computing.json?time=638658864045684959",
    "container": "https://catalog.r1-it.storage.cloud.it/catalog_container.json?time=638658864243742192",
    "networking": "https://catalog.r1-it.storage.cloud.it/catalog_networking.json?time=638658864438361329",
    "storage": "https://catalog.r1-it.storage.cloud.it/catalog_storage.json?time=638658864736088128",
}



class CoreService(WampComponent):
    def __init__(self, config):
        super().__init__(config)

    #        asyncio.get_event_loop().run_until_complete(database.session.init(config))

    async def onJoin(self, details):
        await super().onJoin(details)

        # register(s)
        await self.register(self.ping, "ping")
        await self.register(self.get_pricing, "get_pricing")


        # subscription(s)
        self.subscribe(self.show_ping, "test.ping")


    # procedures
    async def ping(self):
        log.debug({"message": "ping", "time": time.time()})
        return {"message": "pong", "time": time.time()}


    async def get_pricing(resource_type_list:list) -> dict:
        """
        Returns a flattened json containing pricing of Aruba cloud resources.
        In case a resource type is specified, data get extracted only for that resource.

        Args:
            resource_type_list (list): List containing resource type for which pricing is requested.

        Returns:
            dict: Dict containing Aruba cloud pricing.
        """


        # Initialize empty dict to be filled iteratively
        prices = {}

        # # Get data for each separate url, convert into dataframe and append
        # for resource_type, pricing_url in PRICING_ENDPOINTS.items():

        #     # Get pricing only for resources specified in input list
        #     if resource_type not in resource_type_list:
        #         continue

        #     # Request pricing catalog
        #     response = requests.get(pricing_url)

        #     # Check request status
        #     if response.status_code == 200:
                
        #         log.info(f"{resource_type} - getting data...")
                
        #         # Convert output to dictionary
        #         data = response.json()

        #         log.info(f"{resource_type} - parsing data...")
                
        #         # Ensure the input is a list of items
        #         if not isinstance(data, list):
        #             log.warning("Warning: Provided JSON catalog is not a list. Returning an empty DataFrame.")
        #             return prices

        #         # Iterate over each item in the JSON to extract details
        #         for item in data:
        #             if not isinstance(item, dict):
        #                 continue  # Skip non-dictionary entries

        #             # Basic resource information, with default values
        #             base_info = {
        #                 "Resource ID": item.get("_id", "Unknown"),
        #                 "Resource Name": item.get("resourceName", "Unknown"),
        #                 "Category": item.get("resourceCategory", "Unknown"),
        #                 "Currency": item.get("currencyCode", "Unknown"),
        #                 "Unit of Measure": item.get("unitOfMeasure", "Unknown"),
        #                 "Unit Price": item.get("unitPrice", 0.0)
        #             }
                    
        #             # Flavor specifications with default values, checking if 'flavor' exists and is a dictionary
        #             flavor = item.get("flavor", {})
        #             if not isinstance(flavor, dict):
        #                 flavor = {}  # Reset to an empty dict if 'flavor' is None or not a dictionary
                    
        #             flavor_info = {
        #                 "Flavor ID": flavor.get("id", "N/A"),
        #                 "Flavor Name": flavor.get("name", "N/A"),
        #                 "OS Platform": flavor.get("osPlatform", "N/A"),
        #                 "CPU": flavor.get("cpu", "N/A"),
        #                 "RAM (GB)": flavor.get("ram", "N/A"),
        #                 "Disk (GB)": flavor.get("disk", "N/A")
        #             }
                    
        #             # Process each reservation term and price, handling missing or non-list 'reservations'
        #             reservations = item.get("reservations", [])
        #             if not isinstance(reservations, list) or not reservations:
        #                 reservations = [{"term": "N/A", "price": 0.0}]
                    
        #             for reservation in reservations:
        #                 if not isinstance(reservation, dict):
        #                     reservation = {}  # Reset to an empty dict if not a dictionary

        #                 reservation_info = {
        #                     "Reservation Term": reservation.get("term", "N/A"),
        #                     "Reservation Price": reservation.get("price", 0.0)
        #                 }
                        
        #                 # Process each tier category and discount, handling missing or non-list 'tiers'
        #                 tiers = item.get("tiers", [])
        #                 if not isinstance(tiers, list) or not tiers:
        #                     tiers = [{"category": "N/A", "minimumUnits": 0, "percentDiscount": 0.0}]
                        
        #                 for tier in tiers:
        #                     if not isinstance(tier, dict):
        #                         tier = {}  # Reset to an empty dict if not a dictionary
                            
        #                     tier_info = {
        #                         "Tier Category": tier.get("category", "N/A"),
        #                         "Minimum Units for Tier": tier.get("minimumUnits", 0),
        #                         "Tier Discount (%)": tier.get("percentDiscount", 0.0)
        #                     }
                            
        #                     # Combine all dictionaries into a single record
        #                     record = {**base_info, **flavor_info, **reservation_info, **tier_info}
                
        #         # Add resource type entry with all corresponding resources' pricing
        #         prices[resource_type] = record
                
        #     else:
        #         log.error(f"Error: {response.status_code}")

        return prices

    async def show_ping(self, ping=None):
        log.info(f"from test->core: {ping}")


# ======================
# def create_tables():
#     from .config import get_config

#     asyncio.get_event_loop().run_until_complete(
#         database.session.init(get_config(), create=True)
#     )


def main():
    from .config import get_config

    service = CoreService(get_config())
    service.run()
