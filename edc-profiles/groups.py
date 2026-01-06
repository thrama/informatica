import json
import logging
import os
import time

import config
import globalparams
import requests
import urllib3
from requests.auth import HTTPBasicAuth


class Groups:
    ### init #################################################################
    def __init__(self) -> None:
        # Disable the warning about the insecure certificate.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    ### addRole ##############################################################
    @staticmethod
    def addRole(group, securityDomain, role):
        """The function executes the command to add a role to a resource."""

        # Compose the command to execute.
        command = f'{config.infaHome}/isp/bin/infacmd.sh isp AssignRoleToGroup \
                -DomainName {globalparams.domainName} \
                -GroupSecurityDomain {securityDomain} \
                -GroupName {group} \
                -RoleName "{role}" \
                -ServiceName {globalparams.catalogService}'
        print(command)

        # exCode = 0
        exCode = os.system(command)
        # print(exCode)

        # 65280 -> Error
        if exCode == 65280:
            print(f"Error: Role [{role}] already assigned for group [{group}] .")
            logging.error(f"Error: Role [{role}] already assigned for group [{group}].")  # log
            return False  # error

        return True  # ok

    ### isNewGroup ###########################################################
    @staticmethod
    def isNew(group, groupDomain):
        """The function checks if a group is new."""

        url = f"https://{globalparams.catalogHost}:{globalparams.catalogPort}/access/1/catalog/security/accessFilters/GROUP_{groupDomain}~5c~{group}"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        # print(url)

        try:
            response = requests.get(
                url,
                headers=headers,
                auth=HTTPBasicAuth(globalparams.catalogUser, globalparams.catalogPassword),
                # auth=(globalparams.catalogUser, globalparams.catalogPassword)
            )

            # print(response.json())
            # print(response.status_code)
            return response.json()

        except ConnectionError:  # Connectio Error
            print(f"RestAPI connection error for the group [{group}] in function [isNew].")
            logging.error(f"RestAPI connection error for the group [{group}] in function [isNew].")  # log

            return -1

    ### createNew ############################################################
    @staticmethod
    def createNew(group, groupDomain):
        """The function append a permission to a group permissions list and call the RestAPI."""

        # Create the updated JSON
        jsonData = {
            "memberName": groupDomain + "\\" + group,
            "memberType": "GROUP",
            "permissions": [
                {
                    "resourceName": "DataDomain",
                    "classFilters": [{"className": "core.IClass", "permission": "READ_WRITE", "canReadData": False}],
                },
                {
                    "resourceName": "DataDomainGroup",
                    "classFilters": [{"className": "core.IClass", "permission": "READ_WRITE", "canReadData": False}],
                },
            ],
        }

        url = f"https://{globalparams.catalogHost}:{globalparams.catalogPort}/access/1/catalog/security/accessFilters"
        headers = {"If-Unmodified-Since": str(int(time.time())), "Content-Type": "application/json"}

        try:
            response = requests.put(
                url,
                headers=headers,
                json=jsonData,
                auth=HTTPBasicAuth(globalparams.catalogUser, globalparams.catalogPassword),
                # auth=(globalparams.catalogUser, globalparams.catalogPassword)
            )

            print(f"Successfully update the permissions for the new group [{group}].")
            logging.info(f"Successfully update the permissions for the new group [{group}].")  # log

            # print(response.json)
            return response.status_code

        except ConnectionError:  # Connectio Error
            print(f"RestAPI connection error for the group [{group}] in function [createNew].")
            logging.error(f"RestAPI connection error for the group [{group}] in function [createNew].")  # log

            return -1

    ### appendPermission #####################################################
    @staticmethod
    def appendPermission(jsonOrig, jsonPerms):
        """The function append a permission to a group permissions list and call the RestAPI."""

        # Create the updated JSON
        jsonData = jsonOrig
        jsonData["permissions"].append(jsonPerms)
        # print(f"appendPermission: {jsonData}")

        url = f"https://{globalparams.catalogHost}:{globalparams.catalogPort}/access/1/catalog/security/accessFilters"
        headers = {"If-Unmodified-Since": str(jsonData["lastModified"]), "content-type": "application/json"}

        try:
            response = requests.put(
                url,
                headers=headers,
                json=jsonData,
                auth=HTTPBasicAuth(globalparams.catalogUser, globalparams.catalogPassword),
                # auth=(globalparams.catalogUser, globalparams.catalogPassword)
            )

            print(
                f"Successfully added the permissions for the resource [{jsonPerms['resourceName']}] in group [{jsonOrig['memberName']}]."
            )
            logging.info(
                f"Successfully added the permissions for the resource [{jsonPerms['resourceName']}] in group [{jsonOrig['memberName']}]."
            )  # log

            # print(response.json)
            return response.status_code

        except ConnectionError:  # Connectio Error
            print(
                f"RestAPI connection error for the resource [{jsonPerms['resourceName']}] in function [appendPermission]."
            )
            logging.error(
                f"RestAPI connection error for the resource [{jsonPerms['resourceName']}] in function [appendPermission]."
            )  # log

            return -1

    ### modifyPermission #####################################################
    @staticmethod
    def modifyPermission(jsonOrig, jsonPerms, position):
        """The function modify a permission in a group permissions list and call the RestAPI."""

        # Create the updated JSON
        jsonData = jsonOrig
        jsonData["permissions"][position] = jsonPerms
        # print(f"modifyPermission: {jsonData}")

        url = f"https://{globalparams.catalogHost}:{globalparams.catalogPort}/access/1/catalog/security/accessFilters"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        try:
            response = requests.put(
                url,
                headers=headers,
                json=jsonData,
                auth=HTTPBasicAuth(globalparams.catalogUser, globalparams.catalogPassword),
                # auth=(globalparams.catalogUser, globalparams.catalogPassword)
            )

            print(
                f"Successfully updated the permissions for the resource [{jsonPerms['resourceName']}] in group [{jsonOrig['memberName']}]."
            )
            logging.info(
                f"Successfully updated the permissions for the resource [{jsonPerms['resourceName']}] in group [{jsonOrig['memberName']}]."
            )  # log

            # print(response.json)
            return response.status_code

        except ConnectionError:  # Connectio Error
            print(
                f"RestAPI connection error for the resource [{jsonPerms['resourceName']}] in function [modifyPermission]."
            )
            logging.error(
                f"RestAPI connection error for the resource [{jsonPerms['resourceName']}] in function [modifyPermission]."
            )  # log

            return -1

    ### isNewGroup ###########################################################
    @staticmethod
    def isNewDebug():
        """The function checks if a group is new."""

        jsonStr = '{"metadata":{"processingTime":3},"id":"GROUP_Native05","href":"/1/catalog/security/accessFilters/GROUP_Native~5c~05","memberName":"Native05","memberType":"GROUP","lastModified":1601973838387,"permissions":[{"resourceName":"CompositeDataDomain","classFilters":[{"className":"core.IClass","permission":"READ_WRITE","canReadData":false}]},{"resourceName":"DataDomain","classFilters":[{"className":"core.IClass","permission":"READ_WRITE","canReadData":false}]},{"resourceName":"DomainUsers","classFilters":[{"className":"core.IClass","permission":"READ","canReadData":false}]},{"resourceName":"DataDomainGroup","classFilters":[{"className":"core.IClass","permission":"READ_WRITE","canReadData":false}]}],"resourceConfigPermissions":[]}'
        jsonContent = json.loads(jsonStr)

        return jsonContent
