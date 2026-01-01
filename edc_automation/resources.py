###
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
###

import json
import logging
from pathlib import Path

import config
from restapicall import RestAPICall


class Resources:
    ### init #################################################################
    def __init__(self) -> None:
        pass  # not implemented yet

    ### createResourceJSON ###################################################
    @staticmethod
    def createResourceJSON(data, tech, resourceName):
        """
        Creates a JSON file for the resource based on the technology template.
        Returns the JSON data structure.
        """

        jsonTemplate = ""

        # Select the appropriate JSON template based on technology
        if tech == "DB2":
            jsonTemplate = config.jsonTemplDB2
        elif tech == "SQLSRV":
            jsonTemplate = config.jsonTemplSQLSRV
        elif tech == "TERADATA":
            jsonTemplate = config.jsonTemplTeradata
        elif tech == "HIVE":
            jsonTemplate = config.jsonTemplHive
        elif tech == "ORACLE":
            jsonTemplate = config.jsonTemplOracle
        else:
            logging.error(f"Unknown technology [{tech}] for JSON template selection.")
            return None

        try:
            # Load the template
            with open(jsonTemplate, "r") as f:
                jsonData = json.load(f)

            # Populate the template with data from the Excel row
            # This is a simplified version - actual implementation would need
            # to map Excel columns to JSON fields based on the template structure

            # Save JSON file if resource creation fails
            resultFolder = Path(config.resultFolder)
            resultFolder.mkdir(exist_ok=True)
            jsonOutFile = resultFolder / f"{resourceName}.json"

            with open(jsonOutFile, "w") as f:
                json.dump(jsonData, f, indent=2)

            logging.info(f"Created JSON file for resource [{resourceName}]: {jsonOutFile}")
            return jsonData

        except FileNotFoundError as e:
            logging.error(f"Template file not found: {e}")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON template: {e}")
            return None

    ### createDB2 ############################################################
    def createDB2(self, arr, tech):
        """Creates DB2 resources in the Informatica service."""

        restAPI = RestAPICall()

        for i in arr:
            resourceName = i[1]  # Assuming column 1 contains resource name

            logging.debug(f"Creating DB2 resource: {resourceName}")

            # Create JSON data
            jsonData = self.createResourceJSON(i, tech, resourceName)

            if jsonData:
                # Try to create resource via REST API
                statusCode = restAPI.createResource(jsonData, resourceName)

                if statusCode != 200:
                    print(f"Failed to create resource [{resourceName}] via API. JSON file saved for manual creation.")
                    logging.warning(f"Failed to create resource [{resourceName}] via API (status: {statusCode}).")

    ### createSQLSrv #########################################################
    def createSQLSrv(self, arr, tech):
        """Creates SQL Server resources in the Informatica service."""

        restAPI = RestAPICall()

        for i in arr:
            resourceName = i[1]

            logging.debug(f"Creating SQL Server resource: {resourceName}")

            jsonData = self.createResourceJSON(i, tech, resourceName)

            if jsonData:
                statusCode = restAPI.createResource(jsonData, resourceName)

                if statusCode != 200:
                    print(f"Failed to create resource [{resourceName}] via API. JSON file saved for manual creation.")
                    logging.warning(f"Failed to create resource [{resourceName}] via API (status: {statusCode}).")

    ### createTeradata #######################################################
    def createTeradata(self, arr, tech):
        """Creates Teradata resources in the Informatica service."""

        restAPI = RestAPICall()

        for i in arr:
            resourceName = i[1]

            logging.debug(f"Creating Teradata resource: {resourceName}")

            jsonData = self.createResourceJSON(i, tech, resourceName)

            if jsonData:
                statusCode = restAPI.createResource(jsonData, resourceName)

                if statusCode != 200:
                    print(f"Failed to create resource [{resourceName}] via API. JSON file saved for manual creation.")
                    logging.warning(f"Failed to create resource [{resourceName}] via API (status: {statusCode}).")

    ### createHive ###########################################################
    def createHive(self, arr, tech):
        """Creates Hive resources in the Informatica service."""

        restAPI = RestAPICall()

        for i in arr:
            resourceName = i[1]

            logging.debug(f"Creating Hive resource: {resourceName}")

            jsonData = self.createResourceJSON(i, tech, resourceName)

            if jsonData:
                statusCode = restAPI.createResource(jsonData, resourceName)

                if statusCode != 200:
                    print(f"Failed to create resource [{resourceName}] via API. JSON file saved for manual creation.")
                    logging.warning(f"Failed to create resource [{resourceName}] via API (status: {statusCode}).")

    ### createOracle #########################################################
    def createOracle(self, arr, tech):
        """Creates Oracle resources in the Informatica service."""

        restAPI = RestAPICall()

        for i in arr:
            resourceName = i[1]

            logging.debug(f"Creating Oracle resource: {resourceName}")

            jsonData = self.createResourceJSON(i, tech, resourceName)

            if jsonData:
                statusCode = restAPI.createResource(jsonData, resourceName)

                if statusCode != 200:
                    print(f"Failed to create resource [{resourceName}] via API. JSON file saved for manual creation.")
                    logging.warning(f"Failed to create resource [{resourceName}] via API (status: {statusCode}).")

    ### create ###############################################################
    def create(self, arr, tech):
        """Creates resources from the Excel file based on technology."""

        logging.debug(f"Processing resources for technology: {tech}")

        if tech == "DB2":
            print("Creating DB2 resources...")
            self.createDB2(arr, tech)

        elif tech == "HIVE":
            print("Creating Hive resources...")
            self.createHive(arr, tech)

        elif tech == "ORACLE":
            print("Creating Oracle resources...")
            self.createOracle(arr, tech)

        elif tech == "SQLSRV":
            print("Creating SQL Server resources...")
            self.createSQLSrv(arr, tech)

        elif tech == "TERADATA":
            print("Creating Teradata resources...")
            self.createTeradata(arr, tech)

        else:
            logging.error(f"Cannot match the technology value [{tech}].")
            print(f"Error: Cannot match the technology value [{tech}].")
