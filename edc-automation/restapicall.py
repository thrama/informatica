###
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama
#
# DESCRIPTION:
# REST API client module for Informatica EDC Catalog Service.
# Handles resource creation via EDC REST API endpoints.
#
# SECURITY NOTICE:
# - In production, ALWAYS use verify=True and proper certificate validation
# - Consider using requests.Session() for connection pooling
# - Implement retry logic and timeout handling
###

import logging

import globalparams
import requests
import urllib3


class RestAPICall:
    """
    REST API client for Informatica Enterprise Data Catalog.

    This class provides methods to interact with EDC Catalog Service REST API,
    specifically for creating and managing EDC resources.
    """

    def __init__(self) -> None:
        """
        Initialize REST API client.

        WARNING: This disables SSL certificate verification warnings.
        In production environments, use proper SSL certificates and validation.
        """
        # Disable warning about insecure certificate
        # SECURITY: Remove this in production and use verify=True
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @staticmethod
    def createResource(jsonData, resourceName):
        """
        Create an EDC resource via REST API.

        This method calls the EDC Catalog Service REST API to create a new
        resource (database connection, file system, etc.) in the catalog.

        Args:
            jsonData (dict): JSON payload containing resource definition
            resourceName (str): Name of the resource being created

        Returns:
            int: HTTP status code (200=success, 401=unauthorized, 403=forbidden,
                 404=not found, 500=server error, -1=connection error)

        API Endpoint:
            POST https://{host}:{port}/access/1/catalog/resources

        Security Notes:
            - Uses basic authentication (catalogUser, catalogPassword)
            - Consider using API tokens instead of credentials
        """
        # Construct API endpoint URL
        url = f"https://{globalparams.catalogHost}:{globalparams.catalogPort}/access/1/catalog/resources"

        # Set request headers
        headers = {"content-type": "application/json"}

        try:
            # Make POST request to create resource
            # In production: use verify=True or verify='/path/to/ca-bundle.crt'
            response = requests.post(
                url,
                headers=headers,
                json=jsonData,
                auth=(globalparams.catalogUser, globalparams.catalogPassword),
                timeout=30,  # Added timeout for better error handling
            )

            # Process response based on HTTP status code
            if response.status_code == 200:  # OK
                print(f"✓ Successfully created resource: {resourceName}")
                logging.info(f"Successfully created resource [{resourceName}] via REST API")

            elif response.status_code == 401:  # Unauthorized
                print(f"✗ Unauthorized: Check credentials for resource {resourceName}")
                logging.error(f"Unauthorized REST API call for resource [{resourceName}]")

            elif response.status_code == 403:  # Forbidden
                print(f"✗ Forbidden: Insufficient permissions for resource {resourceName}")
                logging.error(f"Forbidden REST API call for resource [{resourceName}]")

            elif response.status_code == 404:  # Not Found
                print(f"✗ Not Found: Invalid API endpoint for resource {resourceName}")
                logging.error(f"REST API endpoint not found for resource [{resourceName}]")

            elif response.status_code == 500:  # Internal Server Error
                print(f"✗ Server Error: Check for conflicts or invalid JSON for resource {resourceName}")
                logging.error(
                    f"Internal server error for resource [{resourceName}]. "
                    f"Possible causes: resource name conflict, invalid JSON structure, "
                    f"missing required fields"
                )

            else:  # Other errors
                print(f"✗ Error {response.status_code}: Failed to create resource {resourceName}")
                logging.error(f"HTTP {response.status_code} error for resource [{resourceName}]")

            return response.status_code

        except requests.exceptions.ConnectionError as e:
            print(f"✗ Connection Error: Cannot reach EDC server for resource {resourceName}")
            logging.error(f"REST API connection error for resource [{resourceName}]: {e}")
            return -1

        except requests.exceptions.Timeout as e:
            print(f"✗ Timeout Error: Request timeout for resource {resourceName}")
            logging.error(f"REST API timeout for resource [{resourceName}]: {e}")
            return -1

        except Exception as e:
            print(f"✗ Unexpected Error: {e} for resource {resourceName}")
            logging.error(f"Unexpected error for resource [{resourceName}]: {e}")
            return -1
