import logging
import json
from pathlib import Path

import globalparams
import config
from restapicall import RestAPICall

class Resources:

    ### init #################################################################
    def __init__(self) -> None:
        pass # not implemented yet


    ### getBoolVal ###########################################################
    @staticmethod
    def getBoolVal(x, strFiel):
        """ The function get the boolean value if the Excel cell contains "YES" or "SI". """

        if x.upper() in ("YES", "SI"):
            return "true"

        if x.upper() in ("NO"):
            return "false"

        print(f"Warning: The value [{x}] for the field [{strFiel}] is incorrect. The 'false' value will be used as default.")
        logging.warning(f"Warning: The value [{x}] for the field [{strFiel}] is incorrect. The 'false' value will be used as default.") # log
            
        return "false"


    ### getSecureConnectionName ##############################################
    @staticmethod
    def getSecureConnectionName(connectionName, dsn):
        """ The function creates the infcmd command for the connection. """

        # Maximum length for DSN name is 32 characters.
        # Link: https://datacadamia.com/odbc/dsn
        if len(connectionName) > 32:
            if len(dsn) > 32: 
                print(f"Error: SecureConnectionName [{connectionName}] and DSN [{dsn}] are longer than 32 characters. I will not create the resource.")
                logging.error(f"SecureConnectionName [{connectionName}] and DSN [{dsn}] are longer than 32 characters. I will not create the resource.") # log
                return False

            elif len(dsn) > 0:
                print(f"Warning: SecureConnectionName [{connectionName}] is longer than 32 characters. I will use DSN [{dsn}].")
                logging.warning(f"SecureConnectionName [{connectionName}] is longer than 32 characters. I will use DSN [{dsn}].") # log
                return dsn

            else:
                print(f"Error: SecureConnectionName [{connectionName}] is longer than 32 characters, but you did not provide an alternative for the DSN. I will not create the resource.")
                logging.error(f"SecureConnectionName [{connectionName}] is longer than 32 characters, but you did not provide an alternative for the DSN. I will not create the resource.") # log
                return False
            
        return connectionName


    ### createDB2 ############################################################
    def createDB2(self, arr, tech, jsonSchema):
        """ Maps the record from the Excel file to the JSON for DB2. """

        resultFolder = Path(config.resultFolder)

        # Loads in memory the JSON template.
        with open(jsonSchema) as f:
            jsonTemplate = json.load(f)

        count = 0
        for i in arr:
            
            # Maps the JSON values with the Excel file and the global params.
            jsonTemplate["resourceIdentifier"]["resourceName"] = i[3] #ResourceName

            jsonTemplate["scannerConfigurations"][0]["configOptions"][1]["optionValues"][0] = i[9] #SubSystemID
            jsonTemplate["scannerConfigurations"][0]["configOptions"][2]["optionValues"][0] = i[4] #UserMetadati
            jsonTemplate["scannerConfigurations"][0]["configOptions"][3]["optionValues"][0] = i[8] #Location
            jsonTemplate["scannerConfigurations"][0]["configOptions"][7]["optionValues"][0] = i[10] #Database
            jsonTemplate["scannerConfigurations"][0]["configOptions"][9]["optionValues"][0] = i[5] #PasswordUserMetadati
            jsonTemplate["scannerConfigurations"][0]["enabled"] = bool(i[12]) #EnableSourceMetadata

            jsonTemplate["scannerConfigurations"][2]["configOptions"][3]["optionValues"][0] = i[13] #SamplingOption
            jsonTemplate["scannerConfigurations"][2]["configOptions"][4]["optionValues"][0] = self.getBoolVal(i[19], "RunSimilarityProfile") #RunSimilarityProfile
            jsonTemplate["scannerConfigurations"][2]["configOptions"][5]["optionValues"][0] = int(i[14]) #RandomSamplingRows
            jsonTemplate["scannerConfigurations"][2]["configOptions"][7]["optionValues"][0] = bool(i[15]) #ExcludeViews
            jsonTemplate["scannerConfigurations"][2]["configOptions"][9]["optionValues"][0] = bool(i[16]) #Cumulative
            jsonTemplate["scannerConfigurations"][2]["configOptions"][15]["optionValues"][0] = globalparams.domainName #DomainName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][16]["optionValues"][0] = globalparams.disName #DisName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][17]["optionValues"][0] = globalparams.disUser #DisUser
            jsonTemplate["scannerConfigurations"][2]["configOptions"][18]["optionValues"][0] = globalparams.disHost #DisHost
            jsonTemplate["scannerConfigurations"][2]["configOptions"][19]["optionValues"][0] = globalparams.disPort #DisPort
            jsonTemplate["scannerConfigurations"][2]["configOptions"][21]["optionValues"][0] = i[2] #SourceConnectionName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][25]["optionValues"][0] = i[17] #DataDomainGroups
            jsonTemplate["scannerConfigurations"][2]["configOptions"][26]["optionValues"][0] = bool(i[18]) #ExcludeNullValues
            jsonTemplate["scannerConfigurations"][2]["configOptions"][31]["optionValues"][0] = globalparams.disPassword #DisPassword

            jsonTemplate["scannerConfigurations"][2]["reusableConfigs"][0]["name"] = globalparams.disDefault #DisDefault

            # Create the resources calling the RestAPI.
            # If the return code is not 200 (OK), then the JSON are written on a file.
            apiResource = RestAPICall()
            if apiResource.createResource(jsonTemplate, i[3]) != 200:

                # Writes the JSON files on file system.
                count +=1
                fileName = resultFolder / f"{tech}_{i[3]}.json"
                with open(fileName, 'w') as outfile:
                    json.dump(jsonTemplate, outfile)

                print(f"Write JSON file: {fileName} for the resouce name [{i[3]}].")
                logging.debug(f"Write JSON file: {fileName} for the resouce name [{i[3]}].") # log

            else:            
                logging.info(f"Create the resource by RestAPI with the resouce name [{i[3]}].") # log
   

    ### createSQLS ############################################################
    def createSQLS(self, arr, tech, jsonSchema):
        """ Maps the record from the Excel file to the JSON for SQLS Server. """
        
        resultFolder = Path(config.resultFolder)

        # Loads in memory the JSON template.
        with open(jsonSchema) as f:
            jsonTemplate = json.load(f)

        count = 0
        for i in arr:

            # Check that the connection name or dns is correct
            sourceConnectionName = self.getSecureConnectionName(i[2], i[3])
            if not sourceConnectionName:
                continue
        
            # Maps the JSON values with the Excel file and the global params.
            jsonTemplate["resourceIdentifier"]["resourceName"] = i[4] #ResourceName

            jsonTemplate["scannerConfigurations"][0]["configOptions"][2]["optionValues"][0] = i[8] #Host
            jsonTemplate["scannerConfigurations"][0]["configOptions"][3]["optionValues"][0] = i[10] #HPort
            jsonTemplate["scannerConfigurations"][0]["configOptions"][5]["optionValues"][0] = i[11] #Database
            jsonTemplate["scannerConfigurations"][0]["configOptions"][6]["optionValues"][0] = globalparams.agentURL #AgentURL

            jsonTemplate["scannerConfigurations"][0]["enabled"] = bool(i[11]) #EnableSourceMetadata

            jsonTemplate["scannerConfigurations"][2]["configOptions"][3]["optionValues"][0] = i[13] #SamplingOption
            jsonTemplate["scannerConfigurations"][2]["configOptions"][4]["optionValues"][0] = self.getBoolVal(i[19], "RunSimilarityProfile") #RunSimilarityProfile
            jsonTemplate["scannerConfigurations"][2]["configOptions"][6]["optionValues"][0] = bool(i[15]) #ExcludeViews
            jsonTemplate["scannerConfigurations"][2]["configOptions"][8]["optionValues"][0] = bool(i[16]) #Cumulative
            jsonTemplate["scannerConfigurations"][2]["configOptions"][14]["optionValues"][0] = globalparams.domainName #DomainName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][15]["optionValues"][0] = globalparams.disName #DisName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][16]["optionValues"][0] = globalparams.disUser #DisUser
            jsonTemplate["scannerConfigurations"][2]["configOptions"][17]["optionValues"][0] = globalparams.disHost #DisHost
            jsonTemplate["scannerConfigurations"][2]["configOptions"][18]["optionValues"][0] = globalparams.disPort #DisPort
            jsonTemplate["scannerConfigurations"][2]["configOptions"][20]["optionValues"][0] = i[2] #SourceConnectionName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][21]["optionValues"][0] = int(i[14]) #RandomSamplingRows
            jsonTemplate["scannerConfigurations"][2]["configOptions"][25]["optionValues"][0] = i[17] #DataDomainGroups
            jsonTemplate["scannerConfigurations"][2]["configOptions"][26]["optionValues"][0] = bool(i[18]) #ExcludeNullValues
            jsonTemplate["scannerConfigurations"][2]["configOptions"][31]["optionValues"][0] = globalparams.disPassword #DisPassword
            
            jsonTemplate["scannerConfigurations"][2]["reusableConfigs"][0]["name"] = globalparams.disDefault #DisDefault

            # Create the resources calling the RestAPI.
            # If the return code is not 200 (OK), then the JSON are written on a file.

            apiResource = RestAPICall()
            if apiResource.createResource(jsonTemplate, i[4]) != 200: #ResourceName

                # Writes the JSON files on file system.
                count +=1
                fileName = resultFolder / f"{tech}_{i[4]}.json"
                with open(fileName, 'w') as outfile:
                    json.dump(jsonTemplate, outfile)

                print(f"Write JSON file: [{fileName}] for the resouce name [{i[4]}].")
                logging.debug(f"Write JSON file: [{fileName}] for the resouce name [{i[4]}].") # log

            else:            
                logging.info(f"Create the resource by RestAPI with the resouce name [{i[4]}].") # log

    
    ### createTeradata #######################################################
    def createTeradata(self, arr, tech, jsonSchema):
        """ Maps the record from the Excel file to the JSON for Teradata. """
        
        resultFolder = Path(config.resultFolder)

        # Loads in memory the JSON template.
        with open(jsonSchema) as f:
            jsonTemplate = json.load(f)

        count = 0
        for i in arr:
            
            # Maps the JSON values with the Excel file and the global params.
            jsonTemplate["resourceIdentifier"]["resourceName"] = i[3] #ResourceName

            jsonTemplate["scannerConfigurations"][0]["enabled"] = bool(i[12]) #EnableSourceMetadata

            jsonTemplate["scannerConfigurations"][0]["configOptions"][1]["optionValues"][0] = i[9] #Host
            jsonTemplate["scannerConfigurations"][0]["configOptions"][2]["optionValues"][0] = i[4] #UserMetadati
            jsonTemplate["scannerConfigurations"][0]["configOptions"][10]["optionValues"][0] = i[10] #Database
            jsonTemplate["scannerConfigurations"][0]["configOptions"][11]["optionValues"][0] = i[5] #PasswordUserMetadati

            jsonTemplate["scannerConfigurations"][2]["configOptions"][3]["optionValues"][0] = i[13] #SamplingOption
            jsonTemplate["scannerConfigurations"][2]["configOptions"][4]["optionValues"][0] = self.getBoolVal(i[18], "RunSimilarityProfile") #RunSimilarityProfile
            jsonTemplate["scannerConfigurations"][2]["configOptions"][5]["optionValues"][0] = int(i[14]) #RandomSamplingRows
            jsonTemplate["scannerConfigurations"][2]["configOptions"][9]["optionValues"][0] = bool(i[15]) #Cumulative
            jsonTemplate["scannerConfigurations"][2]["configOptions"][13]["optionValues"][0] = globalparams.domainName #DomainName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][14]["optionValues"][0] = globalparams.disName #DisName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][15]["optionValues"][0] = globalparams.disUser #DisUser
            jsonTemplate["scannerConfigurations"][2]["configOptions"][16]["optionValues"][0] = globalparams.disHost #DisHost
            jsonTemplate["scannerConfigurations"][2]["configOptions"][17]["optionValues"][0] = globalparams.disPort #DisPort
            jsonTemplate["scannerConfigurations"][2]["configOptions"][22]["optionValues"][0] = i[2] #SourceConnectionName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][25]["optionValues"][0] = i[16] #DataDomainGroups
            jsonTemplate["scannerConfigurations"][2]["configOptions"][26]["optionValues"][0] = bool(i[17]) #ExcludeNullRecord 
            jsonTemplate["scannerConfigurations"][2]["configOptions"][31]["optionValues"][0] = globalparams.disPassword #DisPassword

            jsonTemplate["scannerConfigurations"][2]["reusableConfigs"][0]["name"] = globalparams.disDefault #DisDefault

            # Create the resources calling the RestAPI.
            # If the return code is not 200 (OK), then the JSON are written on a file.
            apiResource = RestAPICall()
            if apiResource.createResource(jsonTemplate, i[3]) != 200:

                # Writes the JSON files on file system.
                count +=1
                fileName = resultFolder / f"{tech}_{i[3]}.json"
                with open(fileName, 'w') as outfile:
                    json.dump(jsonTemplate, outfile)

                print(f"Write JSON file: {fileName} for the resouce name [{i[3]}].")
                logging.debug(f"Write JSON file: {fileName} for the resouce name [{i[3]}].") # log

            else:            
                logging.info(f"Create the resource by RestAPI with the resouce name [{i[3]}].") # log


    ### createHive ###########################################################
    def createHive(self, arr, tech, jsonSchema):
        """ Maps the record from the Excel file to the JSON for Hive. """

        resultFolder = Path(config.resultFolder)

        # Loads in memory the JSON template.
        with open(jsonSchema) as f:
            jsonTemplate = json.load(f)

        count = 0
        for i in arr:
            
            # Maps the JSON values with the Excel file and the global params.
            jsonTemplate["resourceIdentifier"]["resourceName"] = i[3] #ResourceName

            jsonTemplate["scannerConfigurations"][0]["configOptions"][1]["optionValues"][0] = i[8] #HadoopDistribution
            jsonTemplate["scannerConfigurations"][0]["configOptions"][2]["optionValues"][0] = i[10] #URL
            jsonTemplate["scannerConfigurations"][0]["configOptions"][4]["optionValues"][0] = i[4] #UserMetadati
            jsonTemplate["scannerConfigurations"][0]["configOptions"][11]["optionValues"][0] = i[11].lower() #Database
            jsonTemplate["scannerConfigurations"][0]["configOptions"][12]["optionValues"][0] = i[5] #PasswordUserMetadati

            jsonTemplate["scannerConfigurations"][0]["enabled"] = bool(i[12]) #EnableSourceMetadata

            jsonTemplate["scannerConfigurations"][2]["configOptions"][3]["optionValues"][0] = i[13] #SamplingOption
            jsonTemplate["scannerConfigurations"][2]["configOptions"][4]["optionValues"][0] = self.getBoolVal(i[18], "RunSimilarityProfile") #RunSimilarityProfile
            jsonTemplate["scannerConfigurations"][2]["configOptions"][5]["optionValues"][0] = int(i[14]) #RandomSamplingRows
            jsonTemplate["scannerConfigurations"][2]["configOptions"][9]["optionValues"][0] = bool(i[15]) #Cumulative
            jsonTemplate["scannerConfigurations"][2]["configOptions"][13]["optionValues"][0] = globalparams.domainName #DomainName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][14]["optionValues"][0] = globalparams.disName #DisName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][15]["optionValues"][0] = globalparams.disUser #DisUser
            jsonTemplate["scannerConfigurations"][2]["configOptions"][16]["optionValues"][0] = globalparams.disHost #DisHost
            jsonTemplate["scannerConfigurations"][2]["configOptions"][17]["optionValues"][0] = globalparams.disPort #DisPort
            jsonTemplate["scannerConfigurations"][2]["configOptions"][19]["optionValues"][0] = i[2] #SourceConnectionName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][22]["optionValues"][0] = i[16] #DataDomainGroups
            jsonTemplate["scannerConfigurations"][2]["configOptions"][23]["optionValues"][0] = bool(i[17]) #ExcludeNullValues
            jsonTemplate["scannerConfigurations"][2]["configOptions"][31]["optionValues"][0] = globalparams.disPassword #DisPassword
            jsonTemplate["scannerConfigurations"][2]["reusableConfigs"][0]["name"] = globalparams.disDefault #DisDefault

            # Create the resources calling the RestAPI.
            # If the return code is not 200 (OK), then the JSON are written on a file.
            apiResource = RestAPICall()
            if apiResource.createResource(jsonTemplate, i[3]) != 200:

                # Writes the JSON files on file system.
                count +=1
                fileName = resultFolder / f"{tech}_{i[3]}.json"
                with open(fileName, 'w') as outfile:
                    json.dump(jsonTemplate, outfile)

                print(f"Write JSON file: {fileName} for the resouce name [{i[3]}].")
                logging.debug(f"Write JSON file: {fileName} for the resouce name [{i[3]}].") # log

            else:            
                logging.info(f"Create the resource by RestAPI with the resouce name [{i[3]}].") # log


    ### createOracle #########################################################
    def createOracle(self, arr, tech, jsonSchema):
        """ Maps the record from the Excel file to the JSON for Oracle. """

        resultFolder = Path(config.resultFolder)

        # Loads in memory the JSON template.
        with open(jsonSchema) as f:
            jsonTemplate = json.load(f)

        count = 0
        for i in arr:
            
            # Maps the JSON values with the Excel file and the global params.
            jsonTemplate["resourceIdentifier"]["resourceName"] = i[3] #ResourceName

            if i[8].upper() == "NO": # FlagConnectString
                jsonTemplate["scannerConfigurations"][0]["configOptions"][1]["optionValues"][0] = i[9] #Host

            elif i[8].upper() in ("YES", "SI"):
                jsonTemplate["scannerConfigurations"][0]["configOptions"][1]["optionValues"][0] = i[12] #ConnectStringResource
            
            else:
                print(f"Error: bad value in the column [FlagConnectString] with value [{i[8]}]")
                logging.error(f"Bad value in the column [FlagConnectString] with value [{i[8]}]") # log

                continue
            
            jsonTemplate["scannerConfigurations"][0]["configOptions"][2]["optionValues"][0] = i[10] #Port
            jsonTemplate["scannerConfigurations"][0]["configOptions"][3]["optionValues"][0] = i[11] #Service
            jsonTemplate["scannerConfigurations"][0]["configOptions"][4]["optionValues"][0] = i[4] #UserMetadati
            jsonTemplate["scannerConfigurations"][0]["configOptions"][14]["optionValues"][0] = i[5] #PasswordUserMetadati
            
            jsonTemplate["scannerConfigurations"][0]["enabled"] = bool(i[15]) #EnableSourceMetadata

            jsonTemplate["scannerConfigurations"][2]["configOptions"][3]["optionValues"][0] = i[16] #SamplingOption
            jsonTemplate["scannerConfigurations"][2]["configOptions"][4]["optionValues"][0] = self.getBoolVal(i[22], "RunSimilarityProfile") #RunSimilarityProfile
            jsonTemplate["scannerConfigurations"][2]["configOptions"][6]["optionValues"][0] = bool(i[18]) #ExcludeViews
            jsonTemplate["scannerConfigurations"][2]["configOptions"][8]["optionValues"][0] = bool(i[19]) #Cumulative
            jsonTemplate["scannerConfigurations"][2]["configOptions"][12]["optionValues"][0] = globalparams.domainName #DomainName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][13]["optionValues"][0] = globalparams.disName #DisName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][14]["optionValues"][0] = globalparams.disUser #DisUser
            jsonTemplate["scannerConfigurations"][2]["configOptions"][15]["optionValues"][0] = globalparams.disHost #DisHost
            jsonTemplate["scannerConfigurations"][2]["configOptions"][16]["optionValues"][0] = globalparams.disPort #DisPort
            jsonTemplate["scannerConfigurations"][2]["configOptions"][18]["optionValues"][0] = i[2] #SourceConnectionName
            jsonTemplate["scannerConfigurations"][2]["configOptions"][22]["optionValues"][0] = int(i[17]) #RandomSamplingRows
            jsonTemplate["scannerConfigurations"][2]["configOptions"][25]["optionValues"][0] = i[20] #DataDomainGroups
            jsonTemplate["scannerConfigurations"][2]["configOptions"][26]["optionValues"][0] = bool(i[21]) #ExcludeNullValues
            jsonTemplate["scannerConfigurations"][2]["configOptions"][31]["optionValues"][0] = globalparams.disPassword #DisPassword
            
            jsonTemplate["scannerConfigurations"][2]["reusableConfigs"][0]["name"] = globalparams.disDefault #DisDefault          

            # Create the resources calling the RestAPI.
            # If the return code is not 200 (OK), then the JSON are written on a file.
            apiResource = RestAPICall()
            if apiResource.createResource(jsonTemplate, i[3]) != 200:

                # Writes the JSON files on file system.
                count +=1
                fileName = resultFolder / f"{tech}_{i[3]}.json"
                with open(fileName, 'w') as outfile:
                    json.dump(jsonTemplate, outfile)

                print(f"Write JSON file: {fileName} for the resouce name [{i[3]}].")
                logging.debug(f"Write JSON file: {fileName} for the resouce name [{i[3]}].") # log

            else:            
                logging.info(f"Create the resource by RestAPI with the resouce name [{i[3]}].") # log


    ### create ###############################################################
    
    # To correctly populate the JSON values, the function needs:
    # - array obtained from Excel File.
    # - file with parameters valid for all the resources.
    def create(self, arr, tech):
        """ Call the correct create function based on the tech parameter. """

        logging.debug(f"Proceding with technology: {tech}") # log

        if tech == "DB2": # DB2
            print("I will work on DB2 technology...")
            self.createDB2(arr, "DB2", config.jsonTemplDB2)

        elif tech == "HIVE": # Hive
            print("I will work on Hive technology...")
            self.createHive(arr, "HIVE", config.jsonTemplHive)
        
        #elif tech == "MONGODB": # MondoDB
        #    print("I will work on MongoDB technology...")

        elif tech == "ORACLE": # Oracle
            print("I will work on Oracle technology...")
            self.createOracle(arr, "ORACLE", config.jsonTemplOracle)

        elif tech == "SQLSRV": # SQL Server
            print("I will work on SQL Server technology...")
            self.createSQLS(arr, "SQLSERVER", config.jsonTemplSQLSRV)
            
        elif tech == "TERADATA": # Teradata
            print("I will work on Teradata technology...")
            self.createTeradata(arr, "TERADATA", config.jsonTemplTeradata)

        else:
            logging.error(f"Cannot match the technology value [{tech}].") # log
            print(f"Error: cannot match the technology value [{tech}].")
