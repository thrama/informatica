###
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama
#
# DESCRIPTION:
# ODBC configuration file generator for Informatica EDC connections.
#
# This module generates ODBC INI file sections for database connections
# that can be appended to the system ODBC configuration file (odbc.ini).
#
# Supported Databases:
# - Microsoft SQL Server
# - Teradata
#
# The generated files must be manually merged into:
# $INFA_HOME/ODBC7.1/odbc.ini
###

import logging
from pathlib import Path

import config


class ODBCFile:
    """
    ODBC Configuration File Generator.

    This class generates ODBC connection configuration files by reading
    template files and replacing placeholders with actual connection values.

    Output Files:
        - *_odbc_heads.txt: ODBC data source names section
        - *_odbc_sections.txt: ODBC connection parameters section
    """

    def __init__(self) -> None:
        """Initialize ODBC file generator."""
        pass  # No initialization needed currently

    @staticmethod
    def appendConSQLSrv(connectionName, database, ldapDomain, host, port, truncate):
        """
        Generate ODBC configuration for Microsoft SQL Server connection.

        Creates two output files (heads and sections) by processing templates
        and replacing placeholders with actual connection parameters.

        Args:
            connectionName (str): Name of the ODBC data source
            database (str): SQL Server database name
            ldapDomain (str): LDAP/Active Directory domain for authentication
            host (str): SQL Server hostname or IP address
            port (str/int): SQL Server port (typically 1433)
            truncate (bool): If True, truncate output files before writing

        Generated Files:
            - sqlsrv_odbc_heads.txt: DSN declarations
            - sqlsrv_odbc_sections.txt: DSN connection parameters

        Template Placeholders:
            - $SourceConnectionName: Replaced with connectionName
            - $Database: Replaced with database
            - $Host: Replaced with host
            - $Port: Replaced with port
            - $ldapDomain: Replaced with ldapDomain
        """
        # Prepare output file paths
        resultFolder = Path(config.resultFolder)
        resultFolder.mkdir(exist_ok=True)  # Ensure output directory exists

        odbcOutFileHeads = resultFolder / config.odbcOutSRVSQLHeads
        odbcOutFileSections = resultFolder / config.odbcOutSRVSQLSections

        logging.debug(f"ODBC heads output file: {odbcOutFileHeads}")
        logging.debug(f"ODBC sections output file: {odbcOutFileSections}")

        odbcTemplFileHeads = config.odbcTemplateSQLSrvHeads
        odbcTemplFileSections = config.odbcTemplateSQLSrvSections

        # Generate heads file (DSN list)
        with open(odbcTemplFileHeads, "r") as finh, open(odbcOutFileHeads, "a") as fouth:
            if truncate:
                fouth.truncate(0)

            fh = finh.readlines()
            for line in fh:
                if "$SourceConnectionName" in line:
                    line = line.replace("$SourceConnectionName", connectionName)

                fouth.write(f"{line}\n")

            logging.debug(f"Wrote ODBC heads section for connection [{connectionName}]")

        # Generate sections file (connection parameters)
        with open(odbcTemplFileSections, "r") as fins, open(odbcOutFileSections, "a") as fouts:
            if truncate:
                fouts.truncate(0)

            fs = fins.readlines()
            for line in fs:
                # Replace template placeholders
                if "$SourceConnectionName" in line:
                    line = line.replace("$SourceConnectionName", connectionName)
                elif "$Database" in line:
                    line = line.replace("$Database", database)
                elif "$Host" in line:
                    line = line.replace("$Host", host)
                elif "$Port" in line:
                    line = line.replace("$Port", str(port))
                elif "$ldapDomain" in line:
                    line = line.replace("$ldapDomain", ldapDomain)

                fouts.write(line)

            fouts.write("\n")  # Add blank line between DSN entries

            logging.debug(f"Wrote ODBC sections for connection [{connectionName}]")

    @staticmethod
    def appendConTeradata(connectionName, database, host, truncate):
        """
        Generate ODBC configuration for Teradata connection.

        Creates two output files (heads and sections) by processing templates
        and replacing placeholders with actual connection parameters.

        Args:
            connectionName (str): Name of the ODBC data source
            database (str): Teradata database name
            host (str): Teradata server hostname or IP address
            truncate (bool): If True, truncate output files before writing

        Generated Files:
            - teradata_odbc_heads.txt: DSN declarations
            - teradata_odbc_sections.txt: DSN connection parameters

        Template Placeholders:
            - $SourceConnectionName: Replaced with connectionName
            - $Database: Replaced with database
            - $Host: Replaced with host
        """
        # Prepare output file paths
        resultFolder = Path(config.resultFolder)
        resultFolder.mkdir(exist_ok=True)  # Ensure output directory exists

        odbcOutFileHeads = resultFolder / config.odbcOutTeradataHeads
        odbcOutFileSections = resultFolder / config.odbcOutTeradataSections

        logging.debug(f"ODBC heads output file: {odbcOutFileHeads}")
        logging.debug(f"ODBC sections output file: {odbcOutFileSections}")

        odbcTemplFileHeads = config.odbcTemplateTeradataHeads
        odbcTemplFileSections = config.odbcTemplateTeradataSections

        # Generate heads file (DSN list)
        with open(odbcTemplFileHeads, "r") as finh, open(odbcOutFileHeads, "a") as fouth:
            if truncate:
                fouth.truncate(0)

            fh = finh.readlines()
            for line in fh:
                if "$SourceConnectionName" in line:
                    line = line.replace("$SourceConnectionName", connectionName)

                fouth.write(f"{line}\n")

            logging.debug(f"Wrote ODBC heads section for connection [{connectionName}]")

        # Generate sections file (connection parameters)
        with open(odbcTemplFileSections, "r") as fins, open(odbcOutFileSections, "a") as fouts:
            if truncate:
                fouts.truncate(0)

            fs = fins.readlines()
            for line in fs:
                # Replace template placeholders
                if "$SourceConnectionName" in line:
                    line = line.replace("$SourceConnectionName", connectionName)
                elif "$Database" in line:
                    line = line.replace("$Database", database)
                elif "$Host" in line:
                    line = line.replace("$Host", host)

                fouts.write(line)

            fouts.write("\n")  # Add blank line between DSN entries

            logging.debug(f"Wrote ODBC sections for connection [{connectionName}]")
