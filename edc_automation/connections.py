###
# ref isp: https://docs.informatica.com/data-catalog/enterprise-data-catalog/10-4-1/command-reference/infacmd-isp-command-reference.html
# ref CreateConnection: https://docs.informatica.com/data-catalog/enterprise-data-catalog/10-4-1/command-reference/infacmd-isp-command-reference/createconnection.html
# ref ListConnections: https://docs.informatica.com/data-catalog/enterprise-data-catalog/10-4-1/command-reference/infacmd-isp-command-reference/listconnections.html
# ref RemoveConnection: https://docs.informatica.com/data-catalog/enterprise-data-catalog/10-4-1/command-reference/infacmd-isp-command-reference/removeconnection.html
#
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
###

import logging
import os

import config
import globalparams
from odbc import ODBCFile


class Connections:
    ### init #################################################################
    def __init__(self) -> None:
        pass  # not implemented yet

    ### createCommand ########################################################
    @staticmethod
    def createCommand(connectionName, tech, connectionUserName, connectionPassword, options):
        """The function creates the infcmd command for the connection."""

        command = f'{config.infaHome}/isp/bin/infacmd.sh isp CreateConnection \
            -ConnectionName {connectionName} \
            -ConnectionType {tech} \
            -ConnectionUserName {connectionUserName} \
            -ConnectionPassword "{connectionPassword}" \
            -o {options}'

        return command

    ### getSecureConnectionName ##############################################
    @staticmethod
    def getSecureConnectionName(connectionName, dsn):
        """The function creates the infcmd command for the connection."""

        # Maximum length for DSN name is 32 characters.
        # Link: https://datacadamia.com/odbc/dsn
        if len(connectionName) > 32:
            if len(dsn) > 32:
                print(
                    f"Error: SecureConnectionName [{connectionName}] and DSN [{dsn}] are longer than 32 characters. I will not create the connection."
                )
                logging.error(
                    f"SecureConnectionName [{connectionName}] and DSN [{dsn}] are longer than 32 characters. I will not create the connection."
                )  # log
                return False

            elif len(dsn) > 0:
                print(
                    f"Warning: SecureConnectionName [{connectionName}] is longer than 32 characters. I will use DSN [{dsn}]."
                )
                logging.warning(
                    f"SecureConnectionName [{connectionName}] is longer than 32 characters. I will use DSN [{dsn}]."
                )  # log
                return dsn

            else:
                print(
                    f"Error: SecureConnectionName [{connectionName}] is longer than 32 characters, but you did not provide an alternative for the DSN. I will not create the connection."
                )
                logging.error(
                    f"SecureConnectionName [{connectionName}] is longer than 32 characters, but you did not provide an alternative for the DSN. I will not create the connection."
                )  # log
                return False

        return connectionName

    ### createDB2 ############################################################
    def createDB2(self, arr, tech):
        """The function executes the command to create DB2 connections on the Informatica service."""

        for i in arr:
            options = f'"DB2SubsystemID={i[9]} Location={i[8]}"'
            command = self.createCommand(
                i[2], tech, i[6], i[7], options
            )  # connectionName, tech, connectionUserName, connectionPassword, options
            print(command)

            try:
                # Execute the command and capturing the exit code.
                exc = os.system(command)
                if exc != 0:
                    raise OSError(f"{exc}")

            except OSError as e:
                logging.error(f"Bad OS result [{e}] for command [{command}].")  # log

    ### createSQLS ###########################################################
    def createSQLS(self, arr, tech):
        """The function executes the command to create SQL Server connections on the Informatica service."""

        truncate = True
        odbcFile = ODBCFile()

        for i in arr:
            # Check that the connection name or dns is correct
            dsn = self.getSecureConnectionName(i[2], i[3])
            if not dsn:
                continue

            options = f"\"CodePage=UTF-8 EnableQuotes=true QuoteChar=3 DataAccessConnectString={dsn} UseDSN=true MetadataAccessConnectString='jdbc:informatica:sqlserver://{i[8]}:{i[10]};SelectMethod=cursor;databaseName={i[11]};AuthenticationMethod=ntlm2java;Domain={globalparams.ldapDomain}'\""
            command = self.createCommand(
                i[2], tech, i[5], i[6], options
            )  # connectionName, tech, connectionUserName, connectionPassword, options)
            print(command)

            try:
                # Execute the command and capturing the exit code.
                exc = os.system(command)
                if exc != 0:
                    raise OSError(f"{exc}")

                odbcFile.appendConSQLSrv(
                    dsn, i[11], globalparams.ldapDomain, i[8], i[10], truncate
                )  # connectionName, database, ldapDomain, host, port, truncate
                truncate = False

            except OSError as e:
                logging.error(f"Bad OS result [{e}] for command [{command}].")  # log

    ### createTeradata #######################################################
    def createTeradata(self, arr, tech):
        """The function executes the command to create Teradata connections on the Informatica service."""

        truncate = True
        odbcFile = ODBCFile()

        for i in arr:
            # Maximum length for DSN name is 32 characters.
            # Link: https://datacadamia.com/odbc/dsn
            if len(i[2]) > 32:  # connectionName
                print(f"Warning: ODBC DSN name [{i[2]}] longer than 32 characters.")
                logging.warning(f"ODBC DSN name [{i[2]}] longer than 32 characters.")  # log

            options = f"\"DataAccessConnectString={i[2]} CodePage=UTF-8 EnableConnectionPool=true EnableQuotes=false ODBCProvider='Other'\""
            command = self.createCommand(
                i[2], tech, i[6], i[7], options
            )  # connectionName, tech, connectionUserName, connectionPassword, options)
            print(command)

            try:
                # Execute the command and capturing the exit code.
                exc = os.system(command)
                if exc != 0:
                    raise OSError(f"{exc}")

                odbcFile.appendConTeradata(i[2], i[11], i[9], truncate)  # connectionName, database, host, truncate
                truncate = False

            except OSError as e:
                logging.error(f"Bad OS result [{e}] for command [{command}].")  # log

    ### createHive ###########################################################
    def createHive(self, arr, tech):
        """The function executes the command to create Hive connections on the Informatica service."""

        for i in arr:
            options = f"\"enableQuotes=true clusterConfigId='{i[9]}' bypassHiveJDBCServer='false' metadataConnString='{i[10]}' connectString='{i[10]}'\""
            command = self.createCommand(
                i[2], tech, i[6], i[7], options
            )  # connectionName, tech, connectionUserName, connectionPassword, options)
            print(command)

            try:
                # Execute the command and capturing the exit code.
                exc = os.system(command)
                if exc != 0:
                    raise OSError(f"{exc}")

            except OSError as e:
                logging.error(f"Bad OS result [{e}] for command [{command}].")  # log

    ### createOracle #########################################################
    def createOracle(self, arr, tech):
        """The function executes the command to create Oracle connections on the Informatica service."""

        for i in arr:
            if i[8].upper() == "NO":  # FlagConnectString
                options = f"CodePage=UTF-8 DataAccessConnectString={i[11]} \"MetadataAccessConnectString='jdbc:informatica:oracle://{i[9]}:{i[10]};ServiceName={i[11]}'\""

            elif i[8].upper() == "YES":
                options = f"CodePage=UTF-8 DataAccessConnectString={i[11]} \"MetadataAccessConnectString='{i[13]}'\""

            else:
                print(f"Error: bad value in the column [FlagConnectString] with value [{i[8]}].")
                logging.error(f"Bad value in the column [FlagConnectString] with value [{i[8]}].")  # log

                continue

            command = self.createCommand(
                i[2], tech, i[6], i[7], options
            )  # connectionName, tech, connectionUserName, connectionPassword, options
            print(command)

            try:
                # Execute the command and capturing the exit code.
                exc = os.system(command)
                if exc != 0:
                    raise OSError(f"{exc}")

            except OSError as e:
                logging.error(f"Bad OS result [{e}] for command [{command}].")  # log

    ### create ###############################################################
    def create(self, arr, tech):
        """Create the connections from the Excel file."""

        logging.debug(f"Proceding with technology: {tech}")  # log

        if tech == "DB2":  # DB2
            print("I will work on DB2 technology...")
            self.createDB2(arr, "DB2Z")

        elif tech == "HIVE":  # Hive
            print("I will work on Hive technology...")
            self.createHive(arr, "HIVE")

        # elif tech == "MONGODB": # MondoDB
        #    print("I will work on MongoDB technology...")

        elif tech == "ORACLE":  # Oracle
            print("I will work on Oracle technology...")
            self.createOracle(arr, "ORACLE")

        elif tech == "SQLSRV":  # SQL Server
            print("I will work on SQL Server technology...")
            self.createSQLS(arr, "SQLSERVER")

        elif tech == "TERADATA":  # Teradata
            print("I will work on Teradata technology...")
            self.createTeradata(arr, "ODBC")

        else:
            logging.error(f"Cannot match the technology value [{tech}].")  # log
            print(f"Error: Cannot match the technology value [{tech}].")
