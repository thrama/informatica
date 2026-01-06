###
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama
#
# DESCRIPTION:
# EDC Resource creation module.
#
# This module handles the automated creation of Informatica EDC resources
# for various database technologies. It reads configuration from Excel files,
# populates JSON templates, and creates resources via REST API.
#
# Supported Technologies:
# - IBM DB2 z/OS
# - Microsoft SQL Server
# - Teradata
# - Apache Hive
# - Oracle Database
#
# Workflow:
# 1. Load JSON template for target technology
# 2. Map Excel values to JSON structure
# 3. Attempt resource creation via REST API
# 4. If API call fails, save JSON file for manual import
###

import json
import logging
from pathlib import Path

import config
import globalparams
from restapicall import RestAPICall


class Resources:
    """
    EDC Resource Manager.

    This class automates the creation of EDC resources by mapping Excel-based
    configuration data to Informatica EDC JSON resource definitions and creating
    them via REST API.

    Each database technology has a dedicated method that:
    1. Loads the appropriate JSON template
    2. Maps Excel columns to JSON fields
    3. Creates the resource via API
    4. Falls back to JSON file export if API fails
    """

    def __init__(self) -> None:
        """Initialize Resources manager."""
        pass  # No initialization needed currently

    @staticmethod
    def getBoolVal(x, strField):
        """
        Convert Excel boolean values to JSON boolean strings.

        Accepts "YES", "SI" (Italian), or "NO" from Excel cells and converts
        to JSON "true" or "false" strings.

        Args:
            x (str): Value from Excel cell
            strField (str): Field name for logging purposes

        Returns:
            str: "true" or "false" string for JSON

        Note:
            Returns "false" as default if value is unrecognized
        """
        if x.upper() in ("YES", "SI"):
            return "true"

        if x.upper() == "NO":
            return "false"

        print(f"⚠ Warning: Invalid value '{x}' for field '{strField}'. Using 'false' as default.")
        logging.warning(f"Invalid value '{x}' for field '{strField}'. Using 'false' as default.")

        return "false"

    @staticmethod
    def getSecureConnectionName(connectionName, dsn):
        """
        Validate and return appropriate connection name for resource.

        EDC connection names used in resources must match existing connections.
        For ODBC connections with DSN names longer than 32 characters, use the
        DSN field as a fallback.

        Args:
            connectionName (str): Primary connection name
            dsn (str): Alternative DSN name

        Returns:
            str|bool: Valid connection name, or False if validation fails

        Reference:
            https://datacadamia.com/odbc/dsn
        """
        # Maximum length for DSN name is 32 characters
        if len(connectionName) > 32:
            if len(dsn) > 32:
                print(f"✗ Error: Both connection name [{connectionName}] and DSN [{dsn}] exceed 32 characters")
                logging.error(f"Connection name [{connectionName}] and DSN [{dsn}] exceed 32 characters")
                return False

            elif len(dsn) > 0:
                print(f"⚠ Warning: Connection name [{connectionName}] exceeds 32 characters, using DSN [{dsn}]")
                logging.warning(f"Connection name [{connectionName}] exceeds 32 characters, using DSN [{dsn}]")
                return dsn

            else:
                print(f"✗ Error: Connection name [{connectionName}] exceeds 32 characters, no valid DSN provided")
                logging.error(f"Connection name [{connectionName}] exceeds 32 characters, no valid DSN provided")
                return False

        return connectionName

    def createDB2(self, arr, tech, jsonSchema):
        """
        Create EDC resources for IBM DB2 z/OS databases.

        Maps Excel configuration to DB2 resource JSON template and creates
        resources via EDC REST API.

        Args:
            arr (list): Array of resource parameters from Excel
            tech (str): Technology identifier ("DB2")
            jsonSchema (str): Path to DB2 JSON template file

        Excel Column Mapping:
            [2]: SourceConnectionName
            [3]: ResourceName
            [4]: UserMetadata
            [5]: PasswordUserMetadata
            [8]: Location
            [9]: SubSystemID
            [10]: Database
            [12]: EnableSourceMetadata
            [13]: SamplingOption
            [14]: RandomSamplingRows
            [15-19]: Various profiling options
            [17]: DataDomainGroups

        Output:
            - Creates resources via REST API
            - Generates JSON files for failed API calls
        """
        resultFolder = Path(config.resultFolder)
        resultFolder.mkdir(exist_ok=True)

        # Load JSON template
        with open(jsonSchema) as f:
            jsonTemplate = json.load(f)

        count = 0
        for i in arr:
            # Map Excel values to JSON template
            jsonTemplate["resourceIdentifier"]["resourceName"] = i[3]

            # Source metadata configuration
            jsonTemplate["scannerConfigurations"][0]["configOptions"][1]["optionValues"][0] = i[9]
            jsonTemplate["scannerConfigurations"][0]["configOptions"][2]["optionValues"][0] = i[4]
            jsonTemplate["scannerConfigurations"][0]["configOptions"][3]["optionValues"][0] = i[8]
            jsonTemplate["scannerConfigurations"][0]["configOptions"][7]["optionValues"][0] = i[10]
            jsonTemplate["scannerConfigurations"][0]["configOptions"][9]["optionValues"][0] = i[5]
            jsonTemplate["scannerConfigurations"][0]["enabled"] = bool(i[12])

            # Profiling configuration
            jsonTemplate["scannerConfigurations"][2]["configOptions"][3]["optionValues"][0] = i[13]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][4]["optionValues"][0] = self.getBoolVal(
                i[19], "RunSimilarityProfile"
            )
            jsonTemplate["scannerConfigurations"][2]["configOptions"][5]["optionValues"][0] = int(i[14])
            jsonTemplate["scannerConfigurations"][2]["configOptions"][7]["optionValues"][0] = bool(i[15])
            jsonTemplate["scannerConfigurations"][2]["configOptions"][9]["optionValues"][0] = bool(i[16])

            # Global parameters
            jsonTemplate["scannerConfigurations"][2]["configOptions"][15]["optionValues"][0] = globalparams.domainName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][16]["optionValues"][0] = globalparams.disName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][17]["optionValues"][0] = globalparams.disUser
            jsonTemplate["scannerConfigurations"][2]["configOptions"][18]["optionValues"][0] = globalparams.disHost
            jsonTemplate["scannerConfigurations"][2]["configOptions"][19]["optionValues"][0] = globalparams.disPort
            jsonTemplate["scannerConfigurations"][2]["configOptions"][21]["optionValues"][0] = i[2]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][25]["optionValues"][0] = i[17]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][26]["optionValues"][0] = bool(i[18])
            jsonTemplate["scannerConfigurations"][2]["configOptions"][31]["optionValues"][0] = globalparams.disPassword

            jsonTemplate["scannerConfigurations"][2]["reusableConfigs"][0]["name"] = globalparams.disDefault

            # Create resource via REST API
            apiResource = RestAPICall()
            if apiResource.createResource(jsonTemplate, i[3]) != 200:
                # API failed - write JSON file for manual import
                count += 1
                fileName = resultFolder / f"{tech}_{i[3]}.json"
                with open(fileName, "w") as outfile:
                    json.dump(jsonTemplate, outfile, indent=2)

                print(f"✓ Wrote JSON file: {fileName}")
                logging.debug(f"Created JSON file for resource [{i[3]}]")
            else:
                logging.info(f"Successfully created resource [{i[3]}] via REST API")

    def createSQLS(self, arr, tech, jsonSchema):
        """
        Create EDC resources for Microsoft SQL Server databases.

        Args:
            arr (list): Array of resource parameters from Excel
            tech (str): Technology identifier ("SQLSERVER")
            jsonSchema (str): Path to SQL Server JSON template file
        """
        resultFolder = Path(config.resultFolder)
        resultFolder.mkdir(exist_ok=True)

        with open(jsonSchema) as f:
            jsonTemplate = json.load(f)

        count = 0
        for i in arr:
            # Validate connection name
            sourceConnectionName = self.getSecureConnectionName(i[2], i[3])
            if not sourceConnectionName:
                continue

            # Map Excel values to JSON template
            jsonTemplate["resourceIdentifier"]["resourceName"] = i[4]

            # Source metadata configuration
            jsonTemplate["scannerConfigurations"][0]["configOptions"][1]["optionValues"][0] = i[8]
            jsonTemplate["scannerConfigurations"][0]["configOptions"][2]["optionValues"][0] = i[10]
            jsonTemplate["scannerConfigurations"][0]["configOptions"][3]["optionValues"][0] = i[11]
            jsonTemplate["scannerConfigurations"][0]["enabled"] = bool(i[12])

            # Profiling configuration
            jsonTemplate["scannerConfigurations"][2]["configOptions"][3]["optionValues"][0] = i[13]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][4]["optionValues"][0] = self.getBoolVal(
                i[19], "RunSimilarityProfile"
            )
            jsonTemplate["scannerConfigurations"][2]["configOptions"][5]["optionValues"][0] = int(i[14])
            jsonTemplate["scannerConfigurations"][2]["configOptions"][9]["optionValues"][0] = bool(i[15])

            # Global parameters
            jsonTemplate["scannerConfigurations"][2]["configOptions"][13]["optionValues"][0] = globalparams.domainName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][14]["optionValues"][0] = globalparams.disName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][15]["optionValues"][0] = globalparams.disUser
            jsonTemplate["scannerConfigurations"][2]["configOptions"][16]["optionValues"][0] = globalparams.disHost
            jsonTemplate["scannerConfigurations"][2]["configOptions"][17]["optionValues"][0] = globalparams.disPort
            jsonTemplate["scannerConfigurations"][2]["configOptions"][19]["optionValues"][0] = sourceConnectionName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][22]["optionValues"][0] = i[16]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][23]["optionValues"][0] = bool(i[17])
            jsonTemplate["scannerConfigurations"][2]["configOptions"][31]["optionValues"][0] = globalparams.disPassword

            jsonTemplate["scannerConfigurations"][2]["reusableConfigs"][0]["name"] = globalparams.disDefault

            # Create resource via REST API
            apiResource = RestAPICall()
            if apiResource.createResource(jsonTemplate, i[4]) != 200:
                count += 1
                fileName = resultFolder / f"{tech}_{i[4]}.json"
                with open(fileName, "w") as outfile:
                    json.dump(jsonTemplate, outfile, indent=2)

                print(f"✓ Wrote JSON file: {fileName}")
                logging.debug(f"Created JSON file for resource [{i[4]}]")
            else:
                logging.info(f"Successfully created resource [{i[4]}] via REST API")

    def createTeradata(self, arr, tech, jsonSchema):
        """Create EDC resources for Teradata databases."""
        resultFolder = Path(config.resultFolder)
        resultFolder.mkdir(exist_ok=True)

        with open(jsonSchema) as f:
            jsonTemplate = json.load(f)

        count = 0
        for i in arr:
            jsonTemplate["resourceIdentifier"]["resourceName"] = i[3]

            # Source metadata configuration
            jsonTemplate["scannerConfigurations"][0]["configOptions"][1]["optionValues"][0] = i[9]
            jsonTemplate["scannerConfigurations"][0]["configOptions"][2]["optionValues"][0] = i[11]
            jsonTemplate["scannerConfigurations"][0]["enabled"] = bool(i[12])

            # Profiling configuration
            jsonTemplate["scannerConfigurations"][2]["configOptions"][3]["optionValues"][0] = i[13]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][4]["optionValues"][0] = self.getBoolVal(
                i[18], "RunSimilarityProfile"
            )
            jsonTemplate["scannerConfigurations"][2]["configOptions"][5]["optionValues"][0] = int(i[14])
            jsonTemplate["scannerConfigurations"][2]["configOptions"][9]["optionValues"][0] = bool(i[15])

            # Global parameters
            jsonTemplate["scannerConfigurations"][2]["configOptions"][13]["optionValues"][0] = globalparams.domainName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][14]["optionValues"][0] = globalparams.disName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][15]["optionValues"][0] = globalparams.disUser
            jsonTemplate["scannerConfigurations"][2]["configOptions"][16]["optionValues"][0] = globalparams.disHost
            jsonTemplate["scannerConfigurations"][2]["configOptions"][17]["optionValues"][0] = globalparams.disPort
            jsonTemplate["scannerConfigurations"][2]["configOptions"][19]["optionValues"][0] = i[2]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][22]["optionValues"][0] = i[16]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][23]["optionValues"][0] = bool(i[17])
            jsonTemplate["scannerConfigurations"][2]["configOptions"][31]["optionValues"][0] = globalparams.disPassword
            jsonTemplate["scannerConfigurations"][2]["reusableConfigs"][0]["name"] = globalparams.disDefault

            # Create resource via REST API
            apiResource = RestAPICall()
            if apiResource.createResource(jsonTemplate, i[3]) != 200:
                count += 1
                fileName = resultFolder / f"{tech}_{i[3]}.json"
                with open(fileName, "w") as outfile:
                    json.dump(jsonTemplate, outfile, indent=2)

                print(f"✓ Wrote JSON file: {fileName}")
                logging.debug(f"Created JSON file for resource [{i[3]}]")
            else:
                logging.info(f"Successfully created resource [{i[3]}] via REST API")

    def createHive(self, arr, tech, jsonSchema):
        """Create EDC resources for Apache Hive."""
        resultFolder = Path(config.resultFolder)
        resultFolder.mkdir(exist_ok=True)

        with open(jsonSchema) as f:
            jsonTemplate = json.load(f)

        count = 0
        for i in arr:
            jsonTemplate["resourceIdentifier"]["resourceName"] = i[3]

            # Source metadata configuration
            jsonTemplate["scannerConfigurations"][0]["configOptions"][2]["optionValues"][0] = i[10]
            jsonTemplate["scannerConfigurations"][0]["enabled"] = bool(i[11])

            # Profiling configuration
            jsonTemplate["scannerConfigurations"][2]["configOptions"][3]["optionValues"][0] = i[12]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][4]["optionValues"][0] = self.getBoolVal(
                i[17], "RunSimilarityProfile"
            )
            jsonTemplate["scannerConfigurations"][2]["configOptions"][5]["optionValues"][0] = int(i[13])
            jsonTemplate["scannerConfigurations"][2]["configOptions"][9]["optionValues"][0] = bool(i[14])

            # Global parameters
            jsonTemplate["scannerConfigurations"][2]["configOptions"][13]["optionValues"][0] = globalparams.domainName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][14]["optionValues"][0] = globalparams.disName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][15]["optionValues"][0] = globalparams.disUser
            jsonTemplate["scannerConfigurations"][2]["configOptions"][16]["optionValues"][0] = globalparams.disHost
            jsonTemplate["scannerConfigurations"][2]["configOptions"][17]["optionValues"][0] = globalparams.disPort
            jsonTemplate["scannerConfigurations"][2]["configOptions"][19]["optionValues"][0] = i[2]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][22]["optionValues"][0] = i[15]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][23]["optionValues"][0] = bool(i[16])
            jsonTemplate["scannerConfigurations"][2]["configOptions"][31]["optionValues"][0] = globalparams.disPassword
            jsonTemplate["scannerConfigurations"][2]["reusableConfigs"][0]["name"] = globalparams.disDefault

            # Create resource via REST API
            apiResource = RestAPICall()
            if apiResource.createResource(jsonTemplate, i[3]) != 200:
                count += 1
                fileName = resultFolder / f"{tech}_{i[3]}.json"
                with open(fileName, "w") as outfile:
                    json.dump(jsonTemplate, outfile, indent=2)

                print(f"✓ Wrote JSON file: {fileName}")
                logging.debug(f"Created JSON file for resource [{i[3]}]")
            else:
                logging.info(f"Successfully created resource [{i[3]}] via REST API")

    def createOracle(self, arr, tech, jsonSchema):
        """Create EDC resources for Oracle databases."""
        resultFolder = Path(config.resultFolder)
        resultFolder.mkdir(exist_ok=True)

        with open(jsonSchema) as f:
            jsonTemplate = json.load(f)

        count = 0
        for i in arr:
            jsonTemplate["resourceIdentifier"]["resourceName"] = i[3]

            # Handle connection string based on flag
            if i[8].upper() == "NO":
                jsonTemplate["scannerConfigurations"][0]["configOptions"][1]["optionValues"][0] = i[9]
            elif i[8].upper() in ("YES", "SI"):
                jsonTemplate["scannerConfigurations"][0]["configOptions"][1]["optionValues"][0] = i[12]
            else:
                print(f"✗ Error: Invalid FlagConnectString value [{i[8]}]")
                logging.error(f"Invalid FlagConnectString value [{i[8]}]")
                continue

            # Source metadata configuration
            jsonTemplate["scannerConfigurations"][0]["configOptions"][2]["optionValues"][0] = i[10]
            jsonTemplate["scannerConfigurations"][0]["configOptions"][3]["optionValues"][0] = i[11]
            jsonTemplate["scannerConfigurations"][0]["configOptions"][4]["optionValues"][0] = i[4]
            jsonTemplate["scannerConfigurations"][0]["configOptions"][14]["optionValues"][0] = i[5]
            jsonTemplate["scannerConfigurations"][0]["enabled"] = bool(i[15])

            # Profiling configuration
            jsonTemplate["scannerConfigurations"][2]["configOptions"][3]["optionValues"][0] = i[16]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][4]["optionValues"][0] = self.getBoolVal(
                i[22], "RunSimilarityProfile"
            )
            jsonTemplate["scannerConfigurations"][2]["configOptions"][6]["optionValues"][0] = bool(i[18])
            jsonTemplate["scannerConfigurations"][2]["configOptions"][8]["optionValues"][0] = bool(i[19])
            jsonTemplate["scannerConfigurations"][2]["configOptions"][22]["optionValues"][0] = int(i[17])

            # Global parameters
            jsonTemplate["scannerConfigurations"][2]["configOptions"][12]["optionValues"][0] = globalparams.domainName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][13]["optionValues"][0] = globalparams.disName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][14]["optionValues"][0] = globalparams.disUser
            jsonTemplate["scannerConfigurations"][2]["configOptions"][15]["optionValues"][0] = globalparams.disHost
            jsonTemplate["scannerConfigurations"][2]["configOptions"][16]["optionValues"][0] = globalparams.disPort
            jsonTemplate["scannerConfigurations"][2]["configOptions"][18]["optionValues"][0] = i[2]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][25]["optionValues"][0] = i[20]
            jsonTemplate["scannerConfigurations"][2]["configOptions"][26]["optionValues"][0] = bool(i[21])
            jsonTemplate["scannerConfigurations"][2]["configOptions"][31]["optionValues"][0] = globalparams.disPassword

            jsonTemplate["scannerConfigurations"][2]["reusableConfigs"][0]["name"] = globalparams.disDefault

            # Create resource via REST API
            apiResource = RestAPICall()
            if apiResource.createResource(jsonTemplate, i[3]) != 200:
                count += 1
                fileName = resultFolder / f"{tech}_{i[3]}.json"
                with open(fileName, "w") as outfile:
                    json.dump(jsonTemplate, outfile, indent=2)

                print(f"✓ Wrote JSON file: {fileName}")
                logging.debug(f"Created JSON file for resource [{i[3]}]")
            else:
                logging.info(f"Successfully created resource [{i[3]}] via REST API")

    def create(self, arr, tech):
        """
        Main entry point for resource creation.

        Routes to the appropriate technology-specific creation method.

        Args:
            arr (list): Array of resource parameters from Excel
            tech (str): Technology identifier (DB2, HIVE, ORACLE, SQLSRV, TERADATA)
        """
        logging.debug(f"Processing resources for technology: {tech}")

        if tech == "DB2":
            print("▶ Processing DB2 resources...")
            self.createDB2(arr, "DB2", config.jsonTemplDB2)

        elif tech == "HIVE":
            print("▶ Processing Hive resources...")
            self.createHive(arr, "HIVE", config.jsonTemplHive)

        elif tech == "MONGODB":
            print("⚠ MongoDB resources not yet implemented")
            logging.warning("MongoDB resource creation not implemented")

        elif tech == "ORACLE":
            print("▶ Processing Oracle resources...")
            self.createOracle(arr, "ORACLE", config.jsonTemplOracle)

        elif tech == "SQLSRV":
            print("▶ Processing SQL Server resources...")
            self.createSQLS(arr, "SQLSERVER", config.jsonTemplSQLSRV)

        elif tech == "TERADATA":
            print("▶ Processing Teradata resources...")
            self.createTeradata(arr, "TERADATA", config.jsonTemplTeradata)

        else:
            logging.error(f"Unknown technology: {tech}")
            print(f"✗ Error: Unknown technology [{tech}]")
