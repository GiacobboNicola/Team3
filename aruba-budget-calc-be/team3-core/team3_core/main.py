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
        await self.register(self.create_project, "create_project")
        await self.register(self.create_vpc, "create_vpc")
        await self.register(self.create_subnet, "create_subnet")
        await self.register(self.create_security_group, "create_security_group")
        await self.register(self.create_security_rules, "create_security_rules")
        await self.register(self.create_elastic_ip, "create_elastic_ip")
        await self.register(self.create_kaas, "create_kaas")
        await self.register(self.create_key_pair, "create_key_pair")
        await self.register(self.create_cloud_server, "create_cloud_server")
        await self.register(self.create_cloud_server_ubuntu, "create_cloud_server_ubuntu")
        await self.register(self.create_block_storage, "create_block_storage")
        await self.register(self.deploy_resources, "deploy_resources")

        # subscription(s)
        self.subscribe(self.show_ping, "test.ping")


    # procedures
    async def ping(self):
        log.debug({"message": "ping", "time": time.time()})
        return {"message": "pong", "time": time.time()}


    async def get_pricing(self,
            resource_type_list:list
        ) -> dict:
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

        # Get data for each separate url, convert into dataframe and append
        for resource_type, pricing_url in PRICING_ENDPOINTS.items():

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
                
                # Ensure the input is a list of items
                if not isinstance(data, list):
                    log.warning("Warning: Provided JSON catalog is not a list. Returning an empty DataFrame.")
                    return prices

                # Iterate over each item in the JSON to extract details
                for item in data:
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
                
                # Add resource type entry with all corresponding resources' pricing
                prices[resource_type] = record
                
            else:
                log.error(f"Error: {response.status_code}")

        return prices


    async def auth_web_login(self,
            realm:str,
            client_id:str,
            client_secret:str,
            username:str,
            password:str
        ):

        url = f"login.aruba.it/auth/realms/{realm}/protocol/openid-connect/token"

        payload = f'client_id={client_id}&client_secret={client_secret}&username={username}&password={password}&grant_type=password'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': '••••••'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def generate_api_key(self,
            ingress_url:str,
            web_auth_token:str
        ):

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


    async def get_client_credentials_access_token(self,
            client_id:str,
            client_secret:str
        ):

        url = "login.aruba.it/auth/realms/cmp-new-apikey/protocol/openid-connect/token"

        payload = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.text


    async def create_project(self,
            api_gateway:str,
            web_auth_token:str,
            project_name:str=None
        ):
        """Python implementation of Aruba Cloud API to create a project"""

        if not project_name:
            # Force default name hard-coded into API collections
            project_name = "project-test-1"

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


    async def create_vpc(self,
            api_gateway:str,
            project_id:str,
            web_auth_token:str,
            vpc_name:str=None
        ):
        """Python implementation of Aruba Cloud API to create a vpc"""

        if not vpc_name:
            # Force default name hard-coded into API collections
            vpc_name = "vpc-test-1"

        url = f"{api_gateway}/projects/{project_id}/providers/Aruba.Network/vpcs"

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


    async def create_subnet(self,
            api_gateway:str,
            project_id:str,
            web_auth_token:str,
            vpc_id:str,
            subnet_name:str=None
        ):
        """Python implementation of Aruba Cloud API to create a subnet"""

        if not subnet_name:
            # Force default name hard-coded into API collections
            subnet_name = "subnet-api-1"

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


    async def create_security_group(self,
            api_gateway:str,
            project_id:str,
            web_auth_token:str,
            vpc_id:str,
            security_group_name:str=None
        ):
        """Python implementation of Aruba Cloud API to create a security group"""

        if not security_group_name:
            # Force default name hard-coded into API collections
            security_group_name = "sg-test-1"

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


    async def create_security_rules(self,
            api_gateway:str,
            project_id:str,
            web_auth_token:str,
            vpc_id:str,
            security_group_id:str,
            security_rules_name:str=None
        ):
        """Python implementation of Aruba Cloud API to create security rules"""

        if not security_rules_name:
            # Force default name hard-coded into API collections
            security_rules_name = "sg-entry-rule-1"

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


    async def create_elastic_ip(self,
            api_gateway:str,
            project_id:str,
            web_auth_token:str,
            elastic_ip_name:str=None
        ):
        """Python implementation of Aruba Cloud API to deploy an elastic ip"""

        if not elastic_ip_name:
            # Force default name hard-coded into API collections
            elastic_ip_name = "ip-test-1"

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


    async def create_kaas(self,
            api_gateway:str,
            project_id:str,
            web_auth_token:str,
            vpc_id:str,
            subnet_id:str,
            kaas_name:str=None
        ):
        """Python implementation of Aruba Cloud API to deploy a kaas"""

        if not kaas_name:
            # Force default name hard-coded into API collections
            kaas_name = "kaas-test-1"

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


    async def create_key_pair(self,
            api_gateway:str,
            project_id:str,
            web_auth_token:str,
            key_pair_name:str
        ):
        """Python implementation of Aruba Cloud API to create a key-pair"""

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


    async def create_cloud_server(self,
            api_gateway:str,
            project_id:str,
            web_auth_token:str,
            vpc_id:str,
            subnet_id:str,
            security_group_id:str,
            cloud_server_name:str=None
        ):
        """Python implementation of Aruba Cloud API to deploy a cloud server"""

        if not cloud_server_name:
            # Force default name hard-coded into API collections
            cloud_server_name = "cloud-server-1-win"

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


    async def create_cloud_server_ubuntu(self,
            api_gateway:str,
            project_id:str,
            web_auth_token:str,
            vpc_id:str,
            subnet_id:str,
            security_group_id:str,
            key_pair_id:str,
            cloud_server_name:str=None
        ):
        """Python implementation of Aruba Cloud API to deploy ubuntu cloud server"""

        if not cloud_server_name:
            # Force default name hard-coded into API collections
            cloud_server_name = "cloud-server-2-ubuntu"

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


    async def create_block_storage(self,
            api_gateway:str,
            project_id:str,
            web_auth_token:str,
            block_storage_name:str=None
        ):
        """Python implementation of Aruba Cloud API to deploy block storage"""

        if not block_storage_name:
            # Force default name hard-coded into API collections
            block_storage_name = "volume-1"

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


    async def deploy_resources(self,
            resources_to_deploy:list,
            api_gateway:str,
            web_auth_token:str,
            project_id:str=None
        ) -> dict:
        """
        Returns a flattened JSON structure summarizing the deployment outcomes of Aruba cloud resources.

        This function processes a list of cloud resources to be deployed and returns a dictionary with the results
        of the deployment. Each deployment's outcome is encapsulated in a flattened JSON format for easier consumption.

        ----------
        Args:
            resources_to_deploy (list): A list of dictionaries, where each dictionary specifies the configuration
            for a resource to deploy. Each dictionary must adhere to the following structure:

            Example Structure:
            [
                {
                    "name": str or None,  # Custom name for the resource. If None, a default name is used.
                    "resource_name": str,  # Type of resource to deploy: 'blockdisk', 'elasticIp', 'kaas', 'cloudServer'.
                    "flavor_name": str or None,  # Flavor or size of the resource. Optional.
                    "os_platform": str or None,  # Operating system: 'linux' or 'windows'. Optional.
                    "cpu": int or None,  # Number of CPUs for the resource. Optional.
                    "ram": int or None,  # Amount of RAM in GB. Optional.
                    "disk": int or None,  # Disk size in GB. Optional.
                    "reservation_term": str or None,  # Term of reservation: '1 Month', '1 Year', '3 Years', or None.
                    "tier_category": str,  # Pricing or support tier: 'Base', 'Partner', or 'Premium'.
                    "additional_resources": dict,  # Nested dictionary with optional supplementary resource information:
                    {
                        "vpc_id": str or None,  # ID of the Virtual Private Cloud. Optional.
                        "subnet_id": str or None,  # ID of the subnet. Optional.
                        "security_group_id": str or None,  # ID of the security group. Optional.
                        "key_pair_id": str or None  # ID of the key pair for SSH access. Optional.
                    }
                },
                ...
            ]

        ------
        Returns:
            dict: A dictionary containing deployment outcomes for each resource.

        """


        # # Here it's not clear if a new project should be created
        # _ = self.create_project(
        #     api_gateway=api_gateway,
        #     web_auth_token=web_auth_token,
        #     project_name=project_id #???
        # )


        # Initialize dict to be filled by api response (per each resource)
        messages = {}

        for resource_to_deploy in resources_to_deploy:

            """
            NOTE:
            Here-after deploy through Aruba Cloud IaaC APIs could be highly
            customized, modifying API bodies to accept parameters like:
                - cpu
                - ram
                - disk
                - reservation_term
                - ...

            """

            if resource_to_deploy["resource_name"] == "blockdisk":
                
                message = self.create_block_storage(
                    api_gateway=api_gateway,
                    project_id=project_id,
                    web_auth_token=web_auth_token,
                    # block_storage_name=resource_to_deploy["name"]
                )

            elif resource_to_deploy["resource_name"] == "elasticIp":
                
                message = self.create_elastic_ip(
                    api_gateway=api_gateway,
                    project_id=project_id,
                    web_auth_token=web_auth_token,
                    # elastic_ip_name=resource_to_deploy["name"]
                )

            elif resource_to_deploy["resource_name"] == "kaas":
                
                # Kaas resources require a vpc and a subnet to be already deployed
                # and ids to be specified in the "additional_resources" sub-dict during API call
                vpc_id = resource_to_deploy["additional_resources"]["vpc_id"]
                subnet_id = resource_to_deploy["additional_resources"]["subnet_id"]

                message = self.create_kaas(
                    api_gateway=api_gateway,
                    project_id=project_id,
                    web_auth_token=web_auth_token,
                    vpc_id=vpc_id,
                    subnet_id=subnet_id,
                    # block_storage_name=resource_to_deploy["name"]
                )

            elif resource_to_deploy["resource_name"] == "cloudServer":
                
                # cloudServer resources require a vpc, a subnet and a security_group to be already deployed
                # and ids to be specified in the "additional_resources" sub-dict during API call
                vpc_id = resource_to_deploy["additional_resources"]["vpc_id"]
                subnet_id = resource_to_deploy["additional_resources"]["subnet_id"]
                security_group_id = resource_to_deploy["additional_resources"]["security_group_id"]

                if resources_to_deploy["os_platform"] == "linux":

                    # Ubuntu servers also require a key-pair id
                    key_pair_id = resource_to_deploy["additional_resources"]["key_pair_id"]

                    message = self.create_cloud_server_ubuntu(
                        api_gateway=api_gateway,
                        project_id=project_id,
                        web_auth_token=web_auth_token,
                        vpc_id=vpc_id,
                        subnet_id=subnet_id,
                        security_group_id=security_group_id,
                        key_pair_id=key_pair_id,
                        # cloud_server_name=resource_to_deploy["name"]
                    )

                elif resources_to_deploy["os_platform"] == "windows":

                    message = self.create_cloud_server(
                        api_gateway=api_gateway,
                        project_id=project_id,
                        web_auth_token=web_auth_token,
                        vpc_id=vpc_id,
                        subnet_id=subnet_id,
                        security_group_id=security_group_id,
                        # cloud_server_name=resource_to_deploy["name"]
                    )

                else:

                    error_text = f"Specified OS '{resource_to_deploy["os_platform"]}' for cloud server resource is not accepted..."
                    log.error(error_text)
                    messages["resource_name"] = error_text
                    continue

            else:

                error_text = f"Specified resource_name '{resource_to_deploy["resource_name"]}' is not accepted..."
                log.error(error_text)
                messages["resource_name"] = message
                continue
            
            # Fill output message from API
            messages["resource_name"] = message


        return messages




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
