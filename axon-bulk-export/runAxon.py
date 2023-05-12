#!/usr/bin/sh python3
# Main run script

# Inhouse Python File :
from props.utils import json, requests, urllib3, dt_string, os, zipfile, dt_zip, shutil, basename, Process, logging
from props.paramsAxon import baseurl, searchUrl, headers, username, password, pathExportZip
from db.database import dbServer
from getFacetsNoRel import noRelationFacets
from getFacetsWithRel import relationFacets
from getSystemRelEdc import getSystemResources

# logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename="runAxon.log", format='%(asctime)s - %(levelname)s - (%(filename)s, %(funcName)s(), line %(lineno)d) - %(message)s',
                    level=logging.DEBUG)

#### Functions #####
# Login and get Bearer token response
def generateToken(base_url, username, password):
    # auth data
    preAuth_json = {
        "username": username,
        "password": password,
    }
    jsonUserAuthData = json.dumps(preAuth_json)

    # login api
    loginApiUrl = base_url + "/api/login_check"

    # send POST request
    r = requests.post(
        url=loginApiUrl, headers=headers, data=jsonUserAuthData, verify=False)

    # if succesfull get token and save server data into database, else save error data into database
    if r.status_code == 200:
        captureAuthentication = json.loads(r.text)
        infaTokenValue = captureAuthentication["token"]  # get token value
        sessionCookies = r.cookies
        dbServer(dt_string, r.status_code)
        return infaTokenValue, sessionCookies

    else:
        logging.error(f"No Response from server, error code: {r.status_code}")
        dbServer(dt_string, r.status_code)
        return

# Run all axon scripts
def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    infaToken, sessionCookies = generateToken(
        baseurl, username, password)
        
    if infaToken:

        bearerToken = 'Bearer ' + infaToken

        logging.info('### Starting Axon export...')

        # Generate CSV for each facet
        logging.info('### Generating no-relation CSV file...')
        p1 = Process(target=noRelationFacets(searchUrl, bearerToken,
                                              headers, sessionCookies))
        p1.start()
        
        logging.info('### Generating relation CSV file...')
        p2 = Process(target=relationFacets(searchUrl, bearerToken,
                                           headers, sessionCookies))
        p2.start()
        
        logging.info('### Generating system relationship EDC CSV file...')
        p3 = Process(target=getSystemResources(searchUrl, bearerToken,
                                               headers, sessionCookies))
        p3.start()
                
        logging.info('### Creating Zip archive for Axon export...')

        # Create zipfile
        path_export = pathExportZip+"AXON_"+dt_zip+".zip"
        try:
            zf = zipfile.ZipFile(path_export, "w", zipfile.ZIP_DEFLATED)
        except FileNotFoundError:
            logging.error(f"File {path_export} not found.")
            raise SystemExit

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, '../AXON/')

        logging.debug(f"File path for the Zip archive: {file_path}")

        for dirname, subdirs, files in os.walk(file_path):
            for filename in files:
                try:
                    zf.write(os.path.join(dirname, filename), basename(filename))
                except FileNotFoundError:
                    logging.error(f"File {path_export} not found.")
                    raise SystemExit

        zf.close()

        logging.info('### Finish')

        # checking whether file exists or not
        if os.path.exists('../AXON/'):
            # removing the file using the shutil.rmtree() method
            shutil.rmtree('../AXON/')
        

# Main program, run only from here
if __name__ == '__main__':
    main()
