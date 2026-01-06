###
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama
#
# DESCRIPTION:
# Excel parsing module for EDC automation.
# Provides functionality to read and convert Excel files into array structures
# for processing EDC connections and resources.
###

import logging
import sys

import config
import pyexcel as pe


class Excel:
    """
    Excel file parser for EDC automation workflows.

    This class handles reading Excel files containing EDC connection and resource
    definitions, converting them into Python data structures for further processing.
    """

    def __init__(self) -> None:
        """Initialize Excel parser."""
        pass  # No initialization needed currently

    @staticmethod
    def convertToArray(xlsFile):
        """
        Read Excel file and convert to array structure.

        The function uses the pyexcel library to read an Excel file and create
        an array where each element represents a row from the specified sheet.

        Args:
            xlsFile (str): Path to the Excel file to process

        Returns:
            list: Array where each element is a row from the Excel sheet

        Raises:
            SystemExit: If Excel file cannot be read or parsed

        Notes:
            - Only processes the sheet specified in config.sheetName
            - Skips the first row (headers) using start_row=1
            - Automatically frees pyexcel resources after reading
        """
        arr = []

        # Read the Excel file
        try:
            sheet = pe.get_sheet(
                file_name=xlsFile,
                start_row=1,  # Skip header row
                sheet_name=config.sheetName,
            )
            logging.info(f"Successfully loaded Excel file: {xlsFile}")

        except Exception as error:
            logging.error(f"ERROR reading Excel file: {error}")
            sys.exit(f"ERROR: Unable to read Excel file '{xlsFile}'. {error}")

        # Transform the Excel sheet into an array
        for row in sheet:
            arr.append(row)

        # Free resources to prevent memory leaks
        pe.free_resources()

        logging.debug(f"Converted {len(arr)} rows from Excel to array")
        return arr
