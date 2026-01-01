import logging

import globalparams
import requests
import urllib3
from requests.auth import HTTPBasicAuth


class Resources:
    ### init #################################################################
    def __init__(self):
        # Disable the warning about the insecure certificate.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.dataDomain = {
            "resourceName": "DataDomain",
            "classFilters": [{"className": "core.IClass", "permission": "READ_WRITE", "canReadData": False}],
        }
        self.dataDomainGroup = {
            "resourceName": "DataDomainGroup",
            "classFilters": [{"className": "core.IClass", "permission": "READ_WRITE", "canReadData": False}],
        }
        self.read = {
            "resourceName": "",
            "classFilters": [
                {"className": "core.Resource", "permission": "READ", "canReadData": False},
                {"className": "core.IClass", "permission": "READ", "canReadData": False},
            ],
        }
        self.readAndWrite = {
            "resourceName": "",
            "classFilters": [
                {"className": "core.Resource", "permission": "READ_WRITE", "canReadData": False},
                {"className": "core.IClass", "permission": "READ_WRITE", "canReadData": False},
            ],
        }
        self.metadataAndDataRead = {
            "resourceName": "",
            "classFilters": [
                {"className": "core.Resource", "permission": "READ", "canReadData": True},
                {"className": "core.IClass", "permission": "READ", "canReadData": True},
            ],
        }
        self.allPermissions = {
            "resourceName": "",
            "classFilters": [
                {"className": "core.Resource", "permission": "READ_WRITE", "canReadData": True},
                {"className": "core.IClass", "permission": "READ_WRITE", "canReadData": True},
            ],
        }
        self.empty = {}

    ### setPermission ########################################################
    def setPermission(self, resourceName, grant, tech):
        # print(f"Grant value [{grant}], technology [{tech}], resource [{resourceName}].")

        if grant.upper() == "READ":
            result = self.read
            result["resourceName"] = resourceName

        elif grant.upper() == "READ AND WRITE":
            result = self.readAndWrite
            result["resourceName"] = resourceName

        elif grant.upper() == "METADATA AND DATA READ" and tech.upper() != "MONGODB":
            result = self.metadataAndDataRead
            result["resourceName"] = resourceName

        elif grant.upper() == "ALL PERMISSION" and tech.upper() != "MONGODB":
            result = self.allPermissions
            result["resourceName"] = resourceName

        else:
            result = self.empty

            print(f"Grant value [{grant}] for technology [{tech}] not in the renge for the resource [{resourceName}].")
            logging.error(
                f"Grant value [{grant}] for technology [{tech}] not in the renge for the resource [{resourceName}]."
            )  # log

        return result

    ### exist ################################################################
    @staticmethod
    def exist(resourceName):
        url = f"https://{globalparams.catalogHost}:{globalparams.catalogPort}/access/1/catalog/resources/{resourceName}"
        # headers = { 'content-type': 'application/json' }
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        try:
            response = requests.get(
                url,
                headers=headers,
                verify=False,
                auth=HTTPBasicAuth(globalparams.catalogUser, globalparams.catalogPassword),
                # auth=(globalparams.catalogUser, globalparams.catalogPassword)
            )

            return response.status_code == 200

        except ConnectionError as e:  # connection error
            print(f"Error: RestAPI error for the resource [{resourceName}]: [{url}]")
            print(e)
            logging.error(f"Error: RestAPI error for the resource [{resourceName}]: [{url}]")  # log
            logging.error(e)  # log

            return -1
