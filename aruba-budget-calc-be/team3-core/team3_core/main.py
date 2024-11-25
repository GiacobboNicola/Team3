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
        await self.register(self.auth_web_login, "auth_web_login")
        await self.register(self.generate_api_key, "generate_api_key")
        await self.register(self.get_client_credentials_access_token, "get_client_credentials_access_token")
        # await self.register(self.create_project, "create_project")
        # await self.register(self.create_vpc, "create_vpc")
        # await self.register(self.create_subnet, "create_subnet")
        # await self.register(self.create_security_group, "create_security_group")
        # await self.register(self.create_security_rules, "create_security_rules")
        # await self.register(self.create_elastic_ip, "create_elastic_ip")
        # await self.register(self.create_kaas, "create_kaas")
        # await self.register(self.create_key_pair, "create_key_pair")
        # await self.register(self.create_cloud_server, "create_cloud_server")
        # await self.register(self.create_cloud_server_ubuntu, "create_cloud_server_ubuntu")
        # await self.register(self.create_block_storage, "create_block_storage")
        await self.register(self.deploy_resource, "deploy_resource")

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


    async def auth_web_login(realm:str, client_id:str, client_secret:str, username:str, password:str):

        url = f"login.aruba.it/auth/realms/{realm}/protocol/openid-connect/token"

        payload = f'client_id={client_id}&client_secret={client_secret}&username={username}&password={password}&grant_type=password'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': '••••••'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def generate_api_key(ingress_url:str, web_auth_token:str):

        url = f"{ingress_url}/profile/api/v1/apikeys"

        payload = json.dumps({
            "name": "aruba-iac2",
            "tags": [
                "string"
            ]
        })
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {web_auth_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def get_client_credentials_access_token(client_id:str, client_secret:str):

        url = "login.aruba.it/auth/realms/cmp-new-apikey/protocol/openid-connect/token"

        payload = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def create_project(api_gateway:str, web_auth_token:str, project_name:str):

        url = f"{api_gateway}/projects"

        payload = json.dumps({
            "metadata": {
                "name": project_name,
                "tags": [
                "string"
                ]
            },
            "properties": {
                "description": "string",
                "default": False
            }
        })
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {web_auth_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def create_vpc(api_gateway:str, project_id:str, web_auth_token:str, vpc_name:str):

        url = "{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs"

        payload = json.dumps({
            "metadata": {
                "name": vpc_name,
                "tags": [
                    "tag-1",
                    "tag-2"
                ],
                "location": {
                    "value": "ITBG-Bergamo"
                }
            }
        })
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {web_auth_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
    
        return response.text


    async def create_subnet(api_gateway:str, project_id:str, web_auth_token:str, vpc_id:str, subnet_name:str):

        url = f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs/{vpc_id}/subnets"

        payload = json.dumps({
            "metadata": {
                "name": subnet_name,
                "tags": [
                    "tag-1",
                    "tag-2"
                ]
            },
            "properties": {
                "type": "Advanced",
                "default": True,
                "network": {
                    "address": "192.168.1.0/25"
                },
                "dhcp": {
                    "enabled": True
                }
            }
        })
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {web_auth_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def create_security_group(api_gateway:str, project_id:str, web_auth_token:str, vpc_id:str, security_group_name:str):
        
        url = f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs/{vpc_id}/securityGroups"

        payload = json.dumps({
            "metadata": {
                "name": security_group_name,
                "tags": [
                    "tag-1",
                    "tag-2"
                ],
                "location": {
                    "value": "ITBG-Bergamo"
                }
            },
            "properties": {
                "default": False
            }
        })
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {web_auth_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def create_security_rules(api_gateway:str, project_id:str, web_auth_token:str, vpc_id:str, security_group_id:str, security_rules_name:str):

        url = f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs/{vpc_id}/securityGroups/{security_group_id}/securityRules"

        payload = json.dumps({
            "metadata": {
                "name": security_rules_name
            },
            "properties": {
                "protocol": "TCP",
                "port": "80-90",
                "direction": "Egress",
                "target": {
                    "kind": "Ip",
                    "value": "0.0.0.0/0"
                }
            }
        })
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {web_auth_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def create_elastic_ip(api_gateway:str, project_id:str, web_auth_token:str, elastic_ip_name:str):

        url = f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/elasticIps"

        payload = json.dumps({
            "metadata": {
                "name": elastic_ip_name,
                "tags": [
                    "tag-1",
                    "tag-2"
                ],
                "location": {
                    "value": "ITBG-Bergamo"
                }
            },
            "properties": {
                "billingPlan": {
                    "billingPeriod": "Hour"
                }
            }
        })
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {web_auth_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def create_kaas(api_gateway:str, project_id:str, web_auth_token:str, vpc_id:str, subnet_id:str, kaas_name:str):

        url = f"{api_gateway}/projects/{project_id}/providers/Aruba.Container/kaas"

        payload = json.dumps({
            "metadata": {
                "name": kaas_name,
                "location": {
                    "value": "ITBG-Bergamo"
                },
                "tags": [
                    "tag1"
                ]
            },
            "properties": {
                "preset": False,
                "vpc": {
                    "uri": f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs/{vpc_id}"
                },
                "kubernetesVersion": {
                    "value": "1.29.2"
                },
                "subnet": {
                    "uri": f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs/{vpc_id}/subnets/{subnet_id}"
                },
                "nodeCidr": {
                    "address": "192.168.59.0/25",
                    "name": "kaas-test-cidr"
                },
                "securityGroup": {
                    "name": "kaas-test-sg"
                },
                "nodePools": [
                    {
                        "name": "nd-1",
                        "nodes": 1,
                        "instance": "K2A4",
                        "dataCenter": "ITBG-1"
                    }
                ],
                "ha": False,
                "billingPlan": {
                    "billingPeriod": "Hour"
                }
            }
        })
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {web_auth_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def create_key_pair(api_gateway:str, project_id:str, web_auth_token:str, key_pair_name:str):

        url = f"{api_gateway}/projects/{project_id}/providers/Aruba.Compute/keyPairs"

        payload = json.dumps({
            "metadata": {
                "name": key_pair_name,
                "location": {
                    "value": "ITBG-Bergamo"
                },
                "tags": [
                    "tag-1"
                ]
            },
            "properties": {
                "value": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC6JqByfkVm64u7emAJMmHx3gNTuorCn/RmLvozgz67MWUCygTtcRHBBS8WAANkSRLCN/r/VDGFBB5N9PzK5V5ONE/VSFGD63V861vu8mslpNHtL6gN2y1mqDzl3vi0ebZv2t6ArsdFKPx1gqsP6kavIAos7ZFgbJsmRNO2V71dK+YPeubxpMPezVBrMxDSLmA0In6z3foFTGB7iZDnQ2Yj0u/Kukf7SfPgaWaegSu/yQVDG+wLQ84d6ti6vdRyjauGvqQjdYldcvdjoG7OlAxC/TRCdwFeq4u6p73IVZoz9Xq99smnOtLu7qGCzW6g/+RNHSPSpz9+R6AKGjUPPFj29+WKJRnesdnb6rRmTyUDsezuu8z/rbthlgDYI3GaT+Sauap9lwuoVcSKKCt1GvMUC180csxVGAMz3MPN0X+pvbAqjNJmGt5lMaRrZ4BROL+PI3PDTTEPniOW+8doQEWZUA3HPthwneQ3emuqGSL3i1W5uJgSvTbAv+nXnrDK2qk="
            }
        })
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {web_auth_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def create_cloud_server(api_gateway:str, project_id:str, web_auth_token:str, vpc_id:str, subnet_id:str, security_group_id:str, cloud_server_name:str):

        url = f"{api_gateway}/projects/{project_id}/providers/Aruba.Compute/cloudServers"

        payload = json.dumps({
            "metadata": {
                "name": cloud_server_name,
                "location": {
                    "value": "ITBG-Bergamo"
                },
                "tags": [
                    "tag-1"
                ]
            },
            "properties": {
                "dataCenter": "ITBG-1",
                "vpc": {
                    "uri": f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs/{vpc_id}"
                },
                "vpcPreset": False,
                "flavorId": "b5052a43-60d0-4041-9d5d-448d30c48f0c",
                "template": {
                    "uri": f"{api_gateway}/providers/Aruba.Compute/templates/65f42d72d82fd1d45ce03b0a"
                },
                "addElasticIp": False,
                "initialPassword": "Aruba2024!",
                "subnets": [
                    {
                        "uri": f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs/{vpc_id}/subnets/{subnet_id}"
                    }
                ],
                "securityGroups": [
                    {
                        "uri": f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs/{vpc_id}/securityGroups/{security_group_id}"
                    }
                ]
            }
        })
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {web_auth_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def create_cloud_server_ubuntu(api_gateway:str, project_id:str, web_auth_token:str, vpc_id:str, subnet_id:str, security_group_id:str, key_pair_id:str, cloud_server_name:str):

        url = f"{api_gateway}/projects/{project_id}/providers/Aruba.Compute/cloudServers"

        payload = json.dumps({
            "metadata": {
                "name": cloud_server_name,
                "location": {
                "value": "ITBG-Bergamo"
                },
                "tags": [
                "tag-1"
                ]
            },
            "properties": {
                "dataCenter": "ITBG-1",
                "vpc": {
                    "uri": f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs/{vpc_id}"
                },
                "vpcPreset": False,
                "flavorId": "ee8e150d-9c47-4d0d-a4f5-34c6166051ed",
                "template": {
                    "uri": "/providers/Aruba.Compute/templates/66045544b146b450ddb90975"
                },
                "addElasticIp": False,
                # "elasticIp": {
                #     "uri": "string"
                # },
                "keyPair": {
                    "uri": f"{api_gateway}/projects/66dac1a6e04c9f5102df7719/providers/Aruba.Compute/keyPairs/{key_pair_id}"
                },
                "initialPassword": "Aruba2024!",
                "subnets": [
                    {
                        "uri": f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs/{vpc_id}/subnets/{subnet_id}"
                    }
                ],
                "securityGroups": [
                    {
                        "uri": f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs/{vpc_id}/securityGroups/{security_group_id}"
                    }
                ]
                # "volumes": [
                #     {
                #         "uri": f"/projects/{{projectIdCreated}}/providers/Aruba.Storage/vpcs/{{vpcIdCreated}}/blockStorages/{{volumeIdCreated}}" 
                #     }
                # ]
            }
        })
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {web_auth_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def create_block_storage(api_gateway:str, project_id:str, web_auth_token:str, block_storage_name:str):

        url = f"{api_gateway}/projects/{project_id}/providers/Aruba.Storage/blockStorages"

        payload = json.dumps({
            "metadata": {
                "name": block_storage_name,
                "location": {
                    "value": "ITBG-Bergamo"
                },
                "tags": [
                    "tag-1"
                ]
            },
            "properties": {
                "sizeGb": 10,
                "billingPeriod": "Hour",
                "dataCenter": "ITBG-1"
            }
        })
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {web_auth_token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def deploy_resource(resources_to_deploy:dict) -> dict:
        """
        Returns a flattened json containing outcomes of Aruba cloud resources deployment.

        Args:
            resources_to_deploy (dict): Dict containing resources to deploy.

        Returns:
            dict: Dict containing deployment outcomes.
        """

        ### TODO: to implement...
        temp = {}


        return temp




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
