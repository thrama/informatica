###
#
# DESCRIPTION: 
# The script's target is to automate the creation of the connections and 
# resources on Informatica EDC.
# Connections: it tries to create the connections and the related ODBC 
# configurations files to copy and paste in the server ODBC file.
# Resources: it tries to create the resources. If it fails, it produces the 
# JSON file for the resource.
#
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
# COMPANY: Informatica LLC
#
###

import logging
import argparse

from excel import Excel 
from resources import Resources
from connections import Connections 


### MAIN ###
if __name__ == "__main__":

    # Variables initialization
    xlsFile = jsonSchema = ""
    errors = []

    # Log definition
    logging.basicConfig(
        filename='main.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    logging.info("### Starting the process... Reading logs with 'tail -f' hurts those around you. ###") # log

    # Definition of the command line parameters
    parser = argparse.ArgumentParser(
        prog="<python> main.py", 
        usage="\n%(prog)s\n\t\t-t|--tech <db2|hive|mongo|oracle|sqlsrv|teradata>\n\t\t-x|--xls <excel_file>\n\t\t[-c|--connections]\n\t\t[-r|--resources]",
        description="Use source Excel file to create JSON files and connections for Informatica service."
    )
    parser.add_argument("-v", "--version", help="show program version", action="store_true")
    parser.add_argument("-t", "--tech",
        help="technology to use to create the resource",
        metavar="<technology>",
        choices=["db2", "hive", "mongodb", "oracle", "sqlsrv", "teradata"],
        required=True
    )
    parser.add_argument("-x", "--xls", help="Excel file (source)", metavar='<excel_file>', required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-r", "--resources", help="create resources into the Informatica service", action="store_true")
    group.add_argument("-c", "--connections", help="create connections into the Informatica service", action="store_true")
    
    # Parse command line parameters
    try: 
        args = parser.parse_args()
    except argparse.ArgumentError:
        print("Error: catching an wrong argument.")
        logging.error("Catching an wrong argument.") # log
        

    logging.debug(f"Arguments: {str(args)}") # log

    if args.version:
        print("Excel-2-JSON v0.1, by Informatica.")

    else:
        # Assign the parameter values
        xlsFile = args.xls
        tech = args.tech.upper()
        #jsonSchema = args.json

        # Creates the object. The class need all the files that the methods 
        # need to work.
        excelArr = Excel()

        # In the first step, the program loads the content of the Excel file 
        # into an array.
        arr = excelArr.convertToArray(xlsFile)
        #print(f"Excel array: {str(arr)}")
        logging.debug(f"Excel array: {str(arr)}") #log

        # If -json arg is in the command line...
        if args.resources:
            resources = Resources()
            resources.create(arr, tech)

        # If -con arg is in the command line...
        elif args.connections:
            cons = Connections()
            cons.create(arr, tech)

        else:
            print("Nothing to do.")
