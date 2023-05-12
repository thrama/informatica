# Main run script

# Inhouse Python File :
from props.utils import os, zipfile, dt_zip, shutil, basename, warnings, logging
from logging import exception
from getLineages import mainLineagesEdc
from props.paramsEdc import pathExportZip

# import mailing
# from mailing.config import sendSuccessEmail

# logging


warnings.filterwarnings('ignore')


# Run scripts to generate CSV and convert them to ZIP files
def main():

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename='runEdcLineage.log', format='%(asctime)s - %(levelname)s - (%(filename)s, %(funcName)s(), line %(lineno)d) - %(message)s',
                            level=logging.INFO)

    logging.info("Starting EDC lineage export...")
    
    # genAllResourcesFile
    #print("Generating EDC LINEAGES........... \n  ")
    logging.info("Generating EDC LINEAGES...")

    mainLineagesEdc()    
    
    #print("Finished generating EDC LINEAGES")
    logging.info("Finished generating EDC lineage")

    # Create zipfile
    logging.info("Creating Zip archive for EDC lineages...")
    path_export = pathExportZip+"LINEAGE_EDC_"+dt_zip+".zip"
    zf = zipfile.ZipFile(path_export, "w", zipfile.ZIP_DEFLATED)

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'EDC/')

    for dirname, subdirs, files in os.walk(file_path):
        for filename in files:
            zf.write(os.path.join(dirname, filename), basename(filename))

    zf.close()

    # checking whether file exists or not
    # if os.path.exists('EDC/'):
    #     # removing the file usi'/Edc_Scripts/EDC/'ng the shutil.rmtree() method
    #     shutil.rmtree('EDC/')
    
    logging.info("Zip file generated successfully")
    #print("FINISHED EDC LINEAGES...........\n  ")
    logging.info("Finish EDC lineage")

    # sendSuccessEmail()


# Main program, run only from here
if __name__ == '__main__':
    main()

