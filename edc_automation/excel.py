###
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
###

import logging
import sys

import config
import pyexcel as pe


class Excel:
    ### init #################################################################
    def __init__(self) -> None:
        pass  # not implemented yet

    ### convertToArray #######################################################

    # The function uses the pyexcel library to read the file Excel and create
    # an array where each element is a row of the sheet.
    # Furthermore, the function works only on the first sheet of the Excel
    # file.
    @staticmethod
    def convertToArray(xlsFile):
        """The function reads the information from the Excel file and inserts them into an array."""

        arr = []

        # Read the excel file.
        try:
            sheet = pe.get_sheet(file_name=xlsFile, start_row=1, sheet_name=config.sheetName)

        except Exception as error:
            logging.error(f"ERROR: {error}")  # log
            sys.exit(f"ERROR: {error}")  # exits from the program

        # Trasform the Excel sheet in an array.
        for row in sheet:
            arr.append(row)

        pe.free_resources()
        return arr
