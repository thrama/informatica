import pyexcel as p
import logging

import config
import sys

class Excel:

    ### init #################################################################
    def __init__(self) -> None:
        pass


    ### getSheetData #########################################################

    # The function uses the pyexcel library to read the file Excel and create 
    # an array where each element is a row of the sheet. 
    # Furthermore, the function works only on the first sheet of the Excel 
    # file.
    @staticmethod
    def getSheetData(xlsFile):
        """ The function reads the information from the Excel file. """
    
        # Read the excel file.
        try: 
            sheet = p.get_records(file_name=xlsFile, sheet_name=config.sheetName)
            return sheet

        except Exception as error:
            logging.error(f"ERROR: {error}") # log
            sys.exit(f"ERROR: {error}") # exits from the program
 
        
