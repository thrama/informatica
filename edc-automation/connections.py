###
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama
#
# DESCRIPTION:
# Connection creation module for Informatica EDC.
# Creates EDC connections using infacmd command-line tool and generates
# corresponding ODBC configuration files for various database technologies.
#
# Supported Technologies:
# - IBM DB2 z/OS
# - Microsoft SQL Server
# - Teradata
# - Apache Hive
# - Oracle Database
#
# References:
# - infacmd isp: https://docs.informatica.com/data-catalog/enterprise-data-catalog/10-4-1/command-reference/infacmd-isp-command-reference.html
# - CreateConnection: https://docs.informatica.com/data-catalog/enterprise-data-catalog/10-4-1/command-reference/infacmd-isp-command-reference/createconnection.html
# - ListConnections: https://docs.informatica.com/data-catalog/enterprise-data-catalog/10-4-1/command-reference/infacmd-isp-command-reference/listconnections.html
###

import logging
import os

import config
import globalparams
from odbc import ODBCFile


class Connections:
    """
    EDC Connection Manager.

    This class handles the creation of Informatica EDC connections for various
    database technologies. It generates both the EDC connection (via infacmd)
    and the corresponding ODBC configuration files.
    """

    def __init__(self) -> None:
        """Initialize Connections manager."""
        pass  # No initialization needed currently

    @staticmethod
    def createCommand(connectionName, tech, connectionUserName, connectionPassword, options):
        """
        Generate infacmd command string for connection creation.

        Args:
            connectionName (str): Name of the connection to create
            tech (str): Connection type (DB2Z, SQLSERVER, ODBC, HIVE, ORACLE)
            connectionUserName (str): Database username
            connectionPassword (str): Database password
            options (str): Technology-specific connection options

        Returns:
            str: Complete infacmd command string

        Note:
            The command uses infacmd.sh located at $INFA_HOME/isp/bin/
        """
        command = f'{config.infaHome}/isp/bin/infacmd.sh isp CreateConnection \
            -ConnectionName {connectionName} \
            -ConnectionType {tech} \
            -ConnectionUserName {connectionUserName} \
            -ConnectionPassword "{connectionPassword}" \
            -o {options}'

        return command

    @staticmethod
    def getSecureConnectionName(connectionName, dsn):
        """
        Validate and return appropriate DSN name for ODBC connections.

        ODBC DSN names have a maximum length of 32 characters. This method
        checks the connection name length and uses the provided DSN as a
        fallback if needed.

        Args:
            connectionName (str): Proposed connection name
            dsn (str): Alternative DSN name

        Returns:
            str|bool: Valid DSN name, or False if validation fails

        Reference:
            https://datacadamia.com/odbc/dsn
        """
        # Maximum length for DSN name is 32 characters
        if len(connectionName) > 32:
            if len(dsn) > 32:
                print(f"✗ Error: Both connection name [{connectionName}] and DSN [{dsn}] exceed 32 characters")
                logging.error(f"Connection name [{connectionName}] and DSN [{dsn}] are longer than 32 characters")
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

    def createDB2(self, arr, tech):
        """
        Create IBM DB2 z/OS connections.

        Args:
            arr (list): Array of connection parameters from Excel
                Expected columns: [0-1: metadata, 2: name, ..., 6-7: credentials, 8: location, 9: subsystem]
            tech (str): Technology type ("DB2Z")

        Note:
            DB2 connections require SubsystemID and Location parameters
        """
        for i in arr:
            options = f'"DB2SubsystemID={i[9]} Location={i[8]}"'
            command = self.createCommand(i[2], tech, i[6], i[7], options)
            print(f"Executing: {command}")

            try:
                exc = os.system(command)
                if exc != 0:
                    raise OSError(f"Command failed with exit code {exc}")
                logging.info(f"Successfully created DB2 connection: {i[2]}")

            except OSError as e:
                logging.error(f"Failed to create DB2 connection [{i[2]}]: {e}")
                print(f"✗ Error creating connection: {e}")

    def createSQLS(self, arr, tech):
        """
        Create Microsoft SQL Server connections with ODBC configuration.

        Args:
            arr (list): Array of connection parameters from Excel
                Expected columns: [2: name, 3: dsn, 5-6: credentials, 8: host, 10: port, 11: database]
            tech (str): Technology type ("SQLSERVER")

        Features:
            - Generates ODBC configuration file for SQL Server
            - Uses NTLM authentication via JDBC
            - Configures UTF-8 encoding and quote handling
        """
        truncate = True
        odbcFile = ODBCFile()

        for i in arr:
            # Validate DSN name length
            dsn = self.getSecureConnectionName(i[2], i[3])
            if not dsn:
                continue

            # Build connection options string
            options = (
                f'"CodePage=UTF-8 '
                f"EnableQuotes=true "
                f"QuoteChar=3 "
                f"DataAccessConnectString={dsn} "
                f"UseDSN=true "
                f"MetadataAccessConnectString='jdbc:informatica:sqlserver://{i[8]}:{i[10]};"
                f"SelectMethod=cursor;"
                f"databaseName={i[11]};"
                f"AuthenticationMethod=ntlm2java;"
                f"Domain={globalparams.ldapDomain}'\""
            )

            command = self.createCommand(i[2], tech, i[5], i[6], options)
            print(f"Executing: {command}")

            try:
                exc = os.system(command)
                if exc != 0:
                    raise OSError(f"Command failed with exit code {exc}")

                # Generate ODBC configuration
                odbcFile.appendConSQLSrv(dsn, i[11], globalparams.ldapDomain, i[8], i[10], truncate)
                truncate = False
                logging.info(f"Successfully created SQL Server connection: {i[2]}")

            except OSError as e:
                logging.error(f"Failed to create SQL Server connection [{i[2]}]: {e}")
                print(f"✗ Error creating connection: {e}")

    def createTeradata(self, arr, tech):
        """
        Create Teradata connections with ODBC configuration.

        Args:
            arr (list): Array of connection parameters from Excel
                Expected columns: [2: name, 6-7: credentials, 9: host, 11: database]
            tech (str): Technology type ("ODBC")

        Features:
            - Generates ODBC configuration file for Teradata
            - Enables connection pooling
            - Configures UTF-8 encoding
        """
        truncate = True
        odbcFile = ODBCFile()

        for i in arr:
            # Warn if DSN name exceeds ODBC limit
            if len(i[2]) > 32:
                print(f"⚠ Warning: ODBC DSN name [{i[2]}] exceeds 32 characters")
                logging.warning(f"ODBC DSN name [{i[2]}] exceeds 32 characters")

            options = (
                f'"DataAccessConnectString={i[2]} '
                f"CodePage=UTF-8 "
                f"EnableConnectionPool=true "
                f"EnableQuotes=false "
                f"ODBCProvider='Other'\""
            )

            command = self.createCommand(i[2], tech, i[6], i[7], options)
            print(f"Executing: {command}")

            try:
                exc = os.system(command)
                if exc != 0:
                    raise OSError(f"Command failed with exit code {exc}")

                # Generate ODBC configuration
                odbcFile.appendConTeradata(i[2], i[11], i[9], truncate)
                truncate = False
                logging.info(f"Successfully created Teradata connection: {i[2]}")

            except OSError as e:
                logging.error(f"Failed to create Teradata connection [{i[2]}]: {e}")
                print(f"✗ Error creating connection: {e}")

    def createHive(self, arr, tech):
        """
        Create Apache Hive connections.

        Args:
            arr (list): Array of connection parameters from Excel
                Expected columns: [2: name, 6-7: credentials, 9: cluster_id, 10: jdbc_string]
            tech (str): Technology type ("HIVE")

        Features:
            - Configures Hive cluster connection
            - Uses JDBC for metadata and data access
            - Enables quote handling
        """
        for i in arr:
            options = (
                f'"enableQuotes=true '
                f"clusterConfigId='{i[9]}' "
                f"bypassHiveJDBCServer='false' "
                f"metadataConnString='{i[10]}' "
                f"connectString='{i[10]}'\""
            )

            command = self.createCommand(i[2], tech, i[6], i[7], options)
            print(f"Executing: {command}")

            try:
                exc = os.system(command)
                if exc != 0:
                    raise OSError(f"Command failed with exit code {exc}")
                logging.info(f"Successfully created Hive connection: {i[2]}")

            except OSError as e:
                logging.error(f"Failed to create Hive connection [{i[2]}]: {e}")
                print(f"✗ Error creating connection: {e}")

    def createOracle(self, arr, tech):
        """
        Create Oracle Database connections.

        Args:
            arr (list): Array of connection parameters from Excel
                Expected columns: [2: name, 6-7: credentials, 8: flag, 9: host, 10: port, 11: service, 13: custom_jdbc]
            tech (str): Technology type ("ORACLE")

        Features:
            - Supports both standard and custom JDBC connection strings
            - Uses ServiceName or custom connection string based on flag
            - Configures UTF-8 encoding
        """
        for i in arr:
            # Determine connection string based on flag
            if i[8].upper() == "NO":  # Use standard JDBC string
                options = (
                    f"CodePage=UTF-8 "
                    f"DataAccessConnectString={i[11]} "
                    f"\"MetadataAccessConnectString='jdbc:informatica:oracle://{i[9]}:{i[10]};ServiceName={i[11]}'\""
                )

            elif i[8].upper() == "YES":  # Use custom JDBC string
                options = f"CodePage=UTF-8 DataAccessConnectString={i[11]} \"MetadataAccessConnectString='{i[13]}'\""

            else:
                print(f"✗ Error: Invalid FlagConnectString value [{i[8]}]. Expected YES or NO")
                logging.error(f"Invalid FlagConnectString value [{i[8]}] for connection [{i[2]}]")
                continue

            command = self.createCommand(i[2], tech, i[6], i[7], options)
            print(f"Executing: {command}")

            try:
                exc = os.system(command)
                if exc != 0:
                    raise OSError(f"Command failed with exit code {exc}")
                logging.info(f"Successfully created Oracle connection: {i[2]}")

            except OSError as e:
                logging.error(f"Failed to create Oracle connection [{i[2]}]: {e}")
                print(f"✗ Error creating connection: {e}")

    def create(self, arr, tech):
        """
        Main entry point for connection creation.

        Routes to the appropriate technology-specific creation method based
        on the technology parameter.

        Args:
            arr (list): Array of connection parameters from Excel
            tech (str): Technology identifier (DB2, HIVE, ORACLE, SQLSRV, TERADATA)
        """
        logging.debug(f"Processing connections for technology: {tech}")

        if tech == "DB2":
            print("▶ Processing DB2 connections...")
            self.createDB2(arr, "DB2Z")

        elif tech == "HIVE":
            print("▶ Processing Hive connections...")
            self.createHive(arr, "HIVE")

        elif tech == "MONGODB":
            print("⚠ MongoDB connections not yet implemented")
            logging.warning("MongoDB connection creation not implemented")

        elif tech == "ORACLE":
            print("▶ Processing Oracle connections...")
            self.createOracle(arr, "ORACLE")

        elif tech == "SQLSRV":
            print("▶ Processing SQL Server connections...")
            self.createSQLS(arr, "SQLSERVER")

        elif tech == "TERADATA":
            print("▶ Processing Teradata connections...")
            self.createTeradata(arr, "ODBC")

        else:
            logging.error(f"Unknown technology: {tech}")
            print(f"✗ Error: Unknown technology [{tech}]")
