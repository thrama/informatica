###
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
###

import logging

import globalparams
import requests
import urllib3


class RestAPICall:
    ### init #################################################################
    def __init__(self) -> None:
        # Disable the warning about the insecure certificate.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    ### createResource #######################################################
    @staticmethod
    def createResource(jsonData, resourceName):
        """The function create a resorce calling the RestAPI."""

        url = f"https://{globalparams.catalogHost}:{globalparams.catalogPort}/access/1/catalog/resources"
        headers = {"content-type": "application/json"}

        try:
            response = requests.post(
                url,
                headers=headers,
                json=jsonData,
                verify=False,
                auth=(globalparams.catalogUser, globalparams.catalogPassword),
            )

            # print(response.json)
            if response.status_code == 200:  # OK
                print(f"Successfully created the resource [{resourceName}] by Rest API.")
                logging.info(f"Successfully created the resource [{resourceName}] by Rest API.")  # log

            elif response.status_code == 401:  # Unauthorized
                print(f"Unauthorized RestAPI call for the Resource [{resourceName}].")
                logging.info(f"Unauthorized RestAPI call for the Resource [{resourceName}].")  # log

            elif response.status_code == 403:  # Forbidden
                print(f"Forbidden RestAPI call for the Resource [{resourceName}].")
                logging.info(f"Forbidden RestAPI call for the Resource [{resourceName}].")  # log

            elif response.status_code == 404:  # Not Found
                print(f"RestAPI call not found for the Resource [{resourceName}].")
                logging.info(f"RestAPI call not found for the Resource [{resourceName}].")  # log

            elif response.status_code == 500:
                print(
                    f"Error: General internal server error [{resourceName}]. Check if the resource conflicts with another object or if the values in the JSON file are correct."
                )
                logging.error(
                    f"General internal server error [{resourceName}]. Check if the resource conflicts with another object or if the values in the JSON file are correct."
                )  # log

            else:
                print(f"Error: Generic error for the resource [{resourceName}].")
                logging.error(f"Generic error for the resource [{resourceName}].")  # log

            return response.status_code

        except ConnectionError as e:  # Connectio Error
            print(f"Error: RestAPI error [{e}] for the resource [{resourceName}].")
            logging.error(f"RestAPI error [{e}] for the resource [{resourceName}].")  # log

            return -1
