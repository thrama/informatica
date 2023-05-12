import requests
import urllib3
import logging
from requests.auth import HTTPBasicAuth

import globalparams

class RestAPICall:
    """The class contains the function for the API call."""

    ### init #################################################################
    def __init__(self):
    
        # Disable the warning about the insecure certificate.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    ### getResJSON ###########################################################
    @staticmethod
    def getResJSON(resourceName):
        """The function gets the JSON for the input resource."""
        url = f"https://{globalparams.catalogHost}:{globalparams.catalogPort}/access/1/catalog/resources/{resourceName}"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        try:
            response = requests.get(
                url,
                headers=headers,
                verify=False,
                auth=HTTPBasicAuth(globalparams.catalogUser, globalparams.catalogPassword)
            )
            logging.info(f"[getResJSON] - RestAPI for the resource [{resourceName}] answer with status code [{response.status_code}].") # log

            print(response)

            # If the call has success, the function will return the JSON value.
            if response.status_code == 200:
                return response.json()

            return response.status_code

        except ConnectionError as e:  # connection error
            print(f"RestAPI error for the resource [{resourceName}]: [{url}]")
            print(e)
            logging.error(f"RestAPI error for the resource [{resourceName}]: [{url}]") # log
            logging.error(e) # log
            
            return -1

    ### setResJSON ###########################################################
    @staticmethod
    def setResJSON(resourceName, jsonData):
        """The function sets the input resource with a new JSON."""
        url = f"https://{globalparams.catalogHost}:{globalparams.catalogPort}/access/1/catalog/resources/{resourceName}"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        try:               
            response = requests.put(
                url,
                headers=headers,
                json=jsonData,
                verify=False,
                auth=HTTPBasicAuth(globalparams.catalogUser, globalparams.catalogPassword)
            )
            logging.info(f"[setResJSON] - RestAPI for the resource [{resourceName}] answer with status code [{response.status_code}].") # log

            return response.status_code

        except ConnectionError as e:  # connection error
            print(f"Error: RestAPI error for the resource [{resourceName}]: [{url}]")
            print(e)
            logging.error(f"Error: RestAPI error for the resource [{resourceName}]: [{url}]") # log
            logging.error(e) # log
            
            return -1

    ### runResurce ###########################################################
    @staticmethod
    def runResource(resourceName):
        """The function executes the input resource."""
        url = f"https://{globalparams.catalogHost}:{globalparams.catalogPort}/access/1/catalog/resources/{resourceName}/execute"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        try:
            response = requests.post(
                url,
                headers=headers,
                verify=False,
                auth=HTTPBasicAuth(globalparams.catalogUser, globalparams.catalogPassword)
            )
            logging.info(f"[runResource] - RestAPI for the resource [{resourceName}] answer with status code [{response.status_code}].") # log

            # If the call has success, the function will return the JSON value.
            if response.status_code == 200:
                return response.json()

            return response.status_code

        except ConnectionError as e:  # connection error
            print(f"RestAPI error for the resource [{resourceName}]: [{url}]")
            print(e)
            logging.error(f"RestAPI error for the resource [{resourceName}]: [{url}]")  # log
            logging.error(e)  # log

            return -1

    ### getJobStatus #########################################################
    @staticmethod
    def getJobStatus(resourceName, jobId):
        """The function get the status for job with the input jobId. """
        url = f"https://{globalparams.catalogHost}:{globalparams.catalogPort}/access/1/catalog/resources/jobs/{jobId}"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        try:
            response = requests.get(
                url,
                headers=headers,
                verify=False,
                auth=HTTPBasicAuth(globalparams.catalogUser, globalparams.catalogPassword),
            )
            logging.info(f"[getJobStatus] - RestAPI for the resource [{resourceName}] answer with status code [{response.status_code}].") # log

            # If the call has success, the function will return the JSON value.
            if response.status_code == 200:
                return response.json()

            return response.status_code

        except ConnectionError as e:  # connection error
            print(f"RestAPI error for the resource [{resourceName}]: [{url}]")
            print(e)
            logging.error(f"RestAPI error for the resource [{resourceName}]: [{url}]")  # log
            logging.error(e)  # log
            
            return -1
