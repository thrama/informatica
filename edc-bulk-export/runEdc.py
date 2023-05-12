from logging import exception
from props.utils import os, zipfile, dt_zip, shutil, basename, warnings, logging, urllib3
from props.paramsEdc import pathExportZip

# AllResources ScriptsEdc
from allResources import mainAllResourcesFile

# # DataDomain Scripts
from DataDomain.fullDatadomain import mainDatadomain

# # Reference Scripts
from ReferenceResources.referenceResources import mainReferencesFile

# # RDBMS Scripts
from RdbmsResources.rdbmsResources import mainRdbmsResourcesFile
from RdbmsResources.rdbmsResourcesLookup import mainRdbmsResourcesLookup
from RdbmsResources.rdbmsResourcesExtra import mainRdbmsResourcesExtra

# # DataFile Scripts
from DataFile.dataFileFull import mainDatafileResources
from DataFile.dataFileLookup import mainDataFileLookup
from DataFile.dataFileExtra import mainDatafileExtra

# import mailing
from props.config_email import mainSendSuccessEmail

# supress dataFrame warnings

from bs4 import MarkupResemblesLocatorWarning
import warnings
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename="runEdc.log", format='%(asctime)s - %(levelname)s - (%(filename)s, %(funcName)s(), line %(lineno)d) - %(message)s',
                    level=logging.INFO)

runtimeError = []
#warnings.filterwarnings('ignore')


# Run scripts to generate CSV and convert them to ZIP files
def main():

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    logging.info("### Starting EDC export...")
    # gerenal_time = time.time()

    ######### MAIN 
    #print("Generating AllResources ......")
    logging.info("Generating AllResources...")
    try:
        mainAllResourcesFile()
    except Exception as e:
        runtimeError.append('mainAllResourcesFile')
        logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
    else:
        logging.info("Finished generating AllResources.")

    ######### DATADOMAIN
    #print("Generating Datadomain ......")
    logging.info("Generating Datadomain...")
    try:
        mainDatadomain()
    except Exception as e:
        runtimeError.append('mainDatadomain')
        logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
    else:
        logging.info("Finished generating Datadomain.")

    ######### REFERENCE
    #print("Generating ReferenceResources ......")
    logging.info("Generating ReferenceResources...")
    try:
        mainReferencesFile()
    except Exception as e:
        runtimeError.append('mainReferencesFile')
        logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
    else:
        logging.info("Finished generating ReferenceResources.")

    ######### RDBMS STANDARD
    #print("Generating RdbmsResources...")
    logging.info("### Generating RdbmsResources...")
    try:
        mainRdbmsResourcesFile()
    except Exception as e:
        runtimeError.append('mainRdbmsResourcesFile')
        logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
    else:
        logging.info("Finished generating RdbmsResources.")

    ######### RDBMS LOOKUP
    #print("Generating RdbmsResourcesLookup ......")
    logging.info("### Generating RdbmsResourcesLookup...")
    try:
        mainRdbmsResourcesLookup()
    except Exception as e:
        runtimeError.append('mainRdbmsResourcesLookup')
        logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
    else:
        logging.info("Finished generating RdbmsResourcesLookup.")
        
    ######### RDBMS EXTRA
    #print("Generating RdbmsResourcesExtra ......")
    logging.info("### Generating RdbmsResourcesExtra...")
    try:
        mainRdbmsResourcesExtra()
    except Exception as e:
        runtimeError.append('mainRdbmsResourcesExtra')
        logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
    else:
        logging.info("Finished generating RdbmsResourcesExtra.")

    ######### DATAFILE STANDARD
    #print("Generating DataFile ......")
    logging.info("### Generating DataFile...")
    try:
        mainDatafileResources()
    except Exception as e:
        runtimeError.append('mainDatafileResources')
        logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
    else:
        logging.info("Finished generating DataFile.")

    ######### DATAFILE LOOKUP
    #print("Generating DataFileLookup ......")
    logging.info("### Generating DataFileLookup...")
    try:
        mainDataFileLookup()
    except Exception as e:
        runtimeError.append('mainDataFileLookup')
        logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
    else:
        logging.info("Finished generating DataFileLookup.")

    ######### DATAFILE EXTRA
    #print("Generating DataFileExtra ......")
    logging.info("### Generating DataFileExtra...")
    try:
        mainDatafileExtra()
    except Exception as e:
        runtimeError.append('mainDatafileExtra')
        logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
    else:
        logging.info("Finished generating DataFileExtra.")

    # ######### CHECK IF THERE IS AN ERROR ##########
    if not runtimeError:
        print("CREATING ZIP FILES FOR EDC....")
        # Create zipfile
        path_export = pathExportZip+"EDC_"+dt_zip+".zip"
        zf = zipfile.ZipFile(path_export, "w", zipfile.ZIP_DEFLATED)

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'EDC/')

        for dirname, subdirs, files in os.walk(file_path):
            for filename in files:
                zf.write(os.path.join(dirname, filename), basename(filename))
        zf.close()

        # checking whether file exists or not
        if os.path.exists('EDC/'):
            # removing the file using the shutil.rmtree() method
            shutil.rmtree('EDC/')

        # dbGeneral(dt_string, totalDownloaded, (time.time() - gerenal_time))
        logging.info("Zip file generated successfylly.")        
        
    else:

        #print('Checking for errors... \n  ')
        logging.info("Checking for errors...")

        #print('Found ', str(len(runtimeError)), ' errors \n  ')
        logging.error(f"Found {str(len(runtimeError))} errors.")

        #print('Retrying... \n  ')
        logging.info("Retrying ... ")

        for func in runtimeError:

            ######### MAIN RESOURCES
            if func == 'mainAllResourcesFile':
                logging.info("Retrying to generate All Resources...")
                downloaded = mainAllResourcesFile()
                if type(downloaded) == exception(downloaded):
                    #print("Oops! Error occurred: {}".format(str(downloaded)))
                    logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
                else:
                    #print("Finished retrying generating AllResources")
                    logging.info("Finished retrying generating AllResources.")

            ######### DATADOMAIN
            if func == 'mainDatadomain':
                logging.info("Retrying to generate Datadomain...")
                downloaded = mainDatadomain()
                if type(downloaded) == exception(downloaded):
                    #print("Oops! Error occurred: {}".format(str(downloaded)))
                    logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
                else:
                    #print("Finished retrying generating Datadomain")
                    logging.info("Finished retrying generating Datadomain.")
 
            ######### REFERENCE 
            if func == 'mainReferencesFile':
                logging.info("Retrying to generate References Resources...")
                retry = mainReferencesFile()
                if type(downloaded) == exception(downloaded):
                    #print("Oops! Error occurred: {}".format(str(downloaded)))
                    logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
                else:
                    #print("Finished retrying generating ReferenceResources")
                    logging.info("Finished retrying generating ReferenceResources.")
                    
            ######### RDBMS STANDARD
            if func == 'mainRdbmsResourcesFile':
                logging.info("Retrying to generate Rdbms Resources...")
                downloaded = mainRdbmsResourcesFile()
                if type(downloaded) == exception(downloaded):
                    #print("Oops! Error occurred: {}".format(str(downloaded)))
                    logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
                else:
                    #print("Finished retrying generating RdbmsResources")
                    logging.info("Finished retrying generating RdbmsResources.")

            ######### RDBMS LOOKUP
            if func == 'mainRdbmsResourcesLookup':
                logging.info("Retrying to generate Rdbms Resources Lookup...")
                downloaded = mainRdbmsResourcesLookup()
                if type(downloaded) == exception(downloaded):
                    #print("Oops! Error occurred: {}".format(str(downloaded)))
                    logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
                else:
                    #print("Finished retrying generating RdbmsResourcesLookup")
                    logging.info("Finished retrying generating RdbmsResourcesLookup.")

            ######### RDBMS EXTRA
            if func == 'mainRdbmsResourcesExtra':
                logging.info("Retrying to generate Rdbms Resources Extra...")
                downloaded = mainRdbmsResourcesExtra()
                if type(downloaded) == exception(downloaded):
                    #print("Oops! Error occurred: {}".format(str(downloaded)))
                    logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
                else:
                    #print("Finished retrying generating RdbmsResourcesExtra")
                    logging.info("Finished retrying generating RdbmsResourcesExtra.")       
          
            ######### DATAFILE STANDARD     
            if func == 'mainDatafileResources':
                logging.info("Retrying to generate Datafile Resources...")
                downloaded = mainDatafileResources()
                if type(downloaded) == exception(downloaded):
                    #print("Oops! Error occurred: {}".format(str(downloaded)))
                    logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
            else:
                #print("Finished retrying generating DataFile")
                logging.info("Finished retrying generating DataFile.")

            ######### DATAFILE LOOKUP
            if func == 'mainDataFileLookup':
                logging.info("Retrying to generate Datafile Resources Lookup...")
                downloaded = mainDataFileLookup()
                if type(downloaded) == exception(downloaded):
                    #print("Oops! Error occurred: {}".format(str(downloaded)))
                    logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
                else:
                    #print("Finished retrying generating DataFileLookup")
                    logging.info("Finished retrying generating DataFileLookup.")

            ######### DATAFILE EXTRA
            if func == 'mainDatafileExtra':
                logging.info("Retrying to generate Datafile Extra...")
                downloaded = mainDatafileExtra()
                if type(downloaded) == exception(downloaded):
                    #print("Oops! Error occurred: {}".format(str(downloaded)))
                    logging.error('Oops! Error occurred: {}'.format(str(downloaded)))
                else:
                    #print("Finished retrying generating DataFileExtra")
                    logging.info("Finished retrying generating DataFileExtra.")

        #print("CREATING ZIP FILES FOR EDC....")
        logging.info("Zip file generated successfylly.")

        # Create zipfile
        path_export = pathExportZip+"EDC_"+dt_zip+".zip"
        zf = zipfile.ZipFile(path_export, "w", zipfile.ZIP_DEFLATED)

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'EDC/')

        for dirname, subdirs, files in os.walk(file_path):
            for filename in files:
                zf.write(os.path.join(dirname, filename), basename(filename))

        logging.info(f"Zip file generated successfylly with name: {path_export}")
        zf.close()

        # checking whether file exists or not
        if os.path.exists('EDC/'):
            # removing the file usi'/Edc_Scripts/EDC/'ng the shutil.rmtree() method
            shutil.rmtree('EDC/')
    
    try:
        mainSendSuccessEmail()
    except Exception as e:
        logging.error('Oops! Error occurred: {}'.format(email))
    else:
        logging.info("E-mail sent.")
    
    #print("FINISHED EDC... \n  ")
    logging.info(f'### Finish')


# Main program, run only from here
if __name__ == '__main__':
    main()
