###
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama
#
# DESCRIPTION:
# Automation script for Informatica Enterprise Data Catalog (EDC).
#
# Features:
# - Automated creation of EDC connections with ODBC configuration
# - Automated creation of EDC resources via REST API
# - Support for multiple database technologies (DB2, Hive, MongoDB, Oracle,
#   SQL Server, Teradata)
# - Excel-based input for bulk operations
#
# The script reads configuration from Excel files and:
# 1. For connections: Creates EDC connections and generates ODBC config files
# 2. For resources: Creates EDC resources via API or generates JSON templates
###

import argparse
import logging

from connections import Connections
from excel import Excel
from resources import Resources

### MAIN ###
if __name__ == "__main__":
    # Variables initialization
    xlsFile = jsonSchema = ""
    errors = []

    # Log definition
    logging.basicConfig(filename="main.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
    logging.info("### Starting EDC automation process ###")

    # Definition of the command line parameters
    parser = argparse.ArgumentParser(
        prog="python main.py",
        usage="\n%(prog)s\n\t\t-t|--tech <db2|hive|mongodb|oracle|sqlsrv|teradata>\n\t\t-x|--xls <excel_file>\n\t\t[-c|--connections]\n\t\t[-r|--resources]",
        description="Use source Excel file to create JSON files and connections for Informatica EDC service.",
    )
    parser.add_argument("-v", "--version", help="show program version", action="store_true")
    parser.add_argument(
        "-t",
        "--tech",
        help="technology to use to create the resource",
        metavar="<technology>",
        choices=["db2", "hive", "mongodb", "oracle", "sqlsrv", "teradata"],
        required=True,
    )
    parser.add_argument("-x", "--xls", help="Excel file (source)", metavar="<excel_file>", required=True)

    # Mutually exclusive group: either connections or resources
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-r", "--resources", help="create resources into the Informatica EDC service", action="store_true"
    )
    group.add_argument(
        "-c", "--connections", help="create connections into the Informatica EDC service", action="store_true"
    )

    # Parse command line parameters
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(f"Error: {e}")
        logging.error(f"Argument parsing error: {e}")
        exit(1)

    logging.debug(f"Arguments: {str(args)}")

    if args.version:
        print("EDC Automation Script v0.1")
        print("Author: Lorenzo Lombardi")
        print("https://github.com/thrama/informatica-automation-examples")

    else:
        # Assign the parameter values
        xlsFile = args.xls
        tech = args.tech.upper()

        # Creates the Excel parser object
        excelArr = Excel()

        # Load the content of the Excel file into an array
        arr = excelArr.convertToArray(xlsFile)
        logging.debug(f"Excel array loaded: {len(arr)} rows")

        # Process resources creation
        if args.resources:
            resources = Resources()
            resources.create(arr, tech)

        # Process connections creation
        elif args.connections:
            cons = Connections()
            cons.create(arr, tech)

        else:
            print("Nothing to do.")
            logging.warning("No action specified")
