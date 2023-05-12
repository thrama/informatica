import logging
from pathlib import Path

import config

class ODBCFile:

    ### init #################################################################
    def __init__(self) -> None:
        pass # not implemented yet


    ### appendConSQLSrv ######################################################
    @staticmethod
    def appendConSQLSrv(connectionName, database, ldapDomain, host, port, truncate):
        """ Create the ODBC configuration output files for SQL Server. """
        
        resultFolder = Path(config.resultFolder)
        odbcOutFileHeads = resultFolder / config.odbcOutSRVSQLHeads
        odbcOutFileSections = resultFolder / config.odbcOutSRVSQLSections
        
        logging.debug(f"ODBC heads output file: {odbcOutFileHeads}") # log
        logging.debug(f"ODBC sections output file: {odbcOutFileSections}") # log

        odbcTemplFileHeads = config.odbcTemplateSQLSrvHeads
        odbcTemplFileSections = config.odbcTemplateSQLSrvSections

        # Creates the heads file.
        with open(odbcTemplFileHeads, "r") as finh, open(odbcOutFileHeads, "a") as fouth:

            if truncate: 
                fouth.truncate(0)

            fh = finh.readlines()
            for line in fh:
                if line.find("$SourceConnectionName") != -1:
                    line = line.replace("$SourceConnectionName", connectionName)

                # Write the updated lines to the ODBC file (append)
                fouth.write(f"{line}\n")

            logging.debug(f"Wrote ODBC heads part for connection [{connectionName}].") # log

        # Creates the sections file.
        with open(odbcTemplFileSections, "r") as fins, open(odbcOutFileSections, "a") as fouts:

            if truncate: 
                fouts.truncate(0)

            fs = fins.readlines()
            for line in fs:
                if line.find("$SourceConnectionName") != -1:
                    line = line.replace("$SourceConnectionName", connectionName)
                elif line.find("$Database") != -1:
                    line = line.replace("$Database", database)
                elif line.find("$Host") != -1:
                    line = line.replace("$Host", host)
                elif line.find("$Port") != -1:    
                    line = line.replace("$Port", str(port))
                elif line.find("$ldapDomain") != -1:    
                    line = line.replace("$ldapDomain", ldapDomain)

                # Write the updated lines to the ODBC file (append)
                fouts.write(f"{line}")

            fouts.write("\n")

            logging.debug(f"Wrote ODBC sections part for connection [{connectionName}].") # log


    ### appendConTeradata ####################################################
    @staticmethod
    def appendConTeradata(connectionName, database, host, truncate):
        """ Create the ODBC configuration output files for Teradata. """

        resultFolder = Path(config.resultFolder)
        odbcOutFileHeads = resultFolder / config.odbcOutTeradataHeads
        odbcOutFileSections = resultFolder / config.odbcOutTeradataSections

        logging.debug(f"ODBC heads output file: {odbcOutFileHeads}") # log
        logging.debug(f"ODBC sections output file: {odbcOutFileSections}") # log

        odbcTemplFileHeads = config.odbcTemplateTeradataHeads
        odbcTemplFileSections = config.odbcTemplateTeradataSections
        
        # Creates the heads file.
        with open(odbcTemplFileHeads, "r") as finh, open(odbcOutFileHeads, "a") as fouth:

            if truncate: 
                fouth.truncate(0)

            fh = finh.readlines()
            for line in fh:
                if line.find("$SourceConnectionName") != -1:
                    line = line.replace("$SourceConnectionName", connectionName)

                # Write the updated lines to the ODBC file (append)
                fouth.write(f"{line}\n")

            logging.debug(f"Wrote ODBC heads part for: {connectionName}") # log

        # Creates the sections file.
        with open(odbcTemplFileSections, "r") as fins, open(odbcOutFileSections, "a") as fouts:

            if truncate: 
                fouts.truncate(0)

            fs = fins.readlines()
            for line in fs:
                if line.find("$SourceConnectionName") != -1:
                    line = line.replace("$SourceConnectionName", connectionName)
                elif line.find("$Database") != -1:
                    line = line.replace("$Database", database)
                elif line.find("$Host") != -1:
                    line = line.replace("$Host", host)

                fouts.write(line)

            fouts.write("\n")

            logging.debug(f"Wrote ODBC sections part for connection [{connectionName}].") # log
            