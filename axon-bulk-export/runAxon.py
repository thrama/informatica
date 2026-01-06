#!/usr/bin/env python3
###
# DATA: 19/03/2024
# VERSION: 1.0
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama
#
# DESCRIPTION:
# Main orchestrator for Axon bulk export operations.
# Coordinates authentication, parallel export processes, and ZIP archiving.
#
# Features:
# - Token-based authentication with Axon API
# - Parallel export of facets and relationships
# - Automatic ZIP archive creation
# - PostgreSQL execution logging
###

# Inhouse Python modules
from db.database import dbServer
from getFacetsNoRel import noRelationFacets
from getFacetsWithRel import relationFacets
from getSystemRelEdc import getSystemResources
from props.paramsAxon import baseurl, headers, password, pathExportZip, searchUrl, username
from props.utils import Process, basename, dt_string, dt_zip, json, logging, os, requests, shutil, urllib3, zipfile

# Configure logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    filename="runAxon.log",
    format="%(asctime)s - %(levelname)s - (%(filename)s, %(funcName)s(), line %(lineno)d) - %(message)s",
    level=logging.DEBUG,
)


def generateToken(base_url, username, password):
    """
    Authenticate with Axon API and retrieve bearer token.

    Args:
        base_url (str): Axon base URL (e.g., https://axon.example.com:8080)
        username (str): Axon username
        password (str): Axon password

    Returns:
        tuple: (token, session_cookies) if successful, None otherwise

    Note:
        Logs authentication status to PostgreSQL database via dbServer()
    """
    # Prepare authentication payload
    preAuth_json = {
        "username": username,
        "password": password,
    }
    jsonUserAuthData = json.dumps(preAuth_json)

    # Axon login API endpoint
    loginApiUrl = base_url + "/api/login_check"

    # Send POST request
    # In production, use verify=True or verify='/path/to/ca-bundle.crt'
    r = requests.post(url=loginApiUrl, headers=headers, data=jsonUserAuthData)

    # Process response
    if r.status_code == 200:
        captureAuthentication = json.loads(r.text)
        infaTokenValue = captureAuthentication["token"]
        sessionCookies = r.cookies

        # Log successful authentication
        dbServer(dt_string, r.status_code)
        logging.info("Successfully authenticated with Axon API")

        return infaTokenValue, sessionCookies
    else:
        logging.error(f"Authentication failed with status code: {r.status_code}")
        dbServer(dt_string, r.status_code)
        return None


def main():
    """
    Main execution function.

    Workflow:
    1. Authenticate with Axon API
    2. Launch parallel export processes:
       - Facets without relationships
       - Facets with relationships
       - EDC system resources
    3. Create ZIP archive of exported CSV files
    4. Cleanup temporary files
    """
    # Disable SSL warnings (not recommended for production)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Authenticate and get token
    auth_result = generateToken(baseurl, username, password)

    if not auth_result:
        logging.error("Authentication failed. Exiting.")
        return

    infaToken, sessionCookies = auth_result
    bearerToken = "Bearer " + infaToken

    logging.info("### Starting Axon export process...")

    # Launch parallel export processes
    # Process 1: Export facets without relationships
    logging.info("### Generating no-relation CSV files...")
    p1 = Process(target=noRelationFacets, args=(searchUrl, bearerToken, headers, sessionCookies))
    p1.start()

    # Process 2: Export facets with relationships
    logging.info("### Generating relation CSV files...")
    p2 = Process(target=relationFacets, args=(searchUrl, bearerToken, headers, sessionCookies))
    p2.start()

    # Process 3: Export EDC system resources
    logging.info("### Generating system relationship EDC CSV files...")
    p3 = Process(target=getSystemResources, args=(searchUrl, bearerToken, headers, sessionCookies))
    p3.start()

    # Wait for all processes to complete
    p1.join()
    p2.join()
    p3.join()

    logging.info("### All export processes completed")
    logging.info("### Creating ZIP archive for Axon export...")

    # Create ZIP archive
    path_export = pathExportZip + "AXON_" + dt_zip + ".zip"

    try:
        zf = zipfile.ZipFile(path_export, "w", zipfile.ZIP_DEFLATED)
    except FileNotFoundError:
        logging.error(f"Cannot create ZIP file at: {path_export}")
        raise SystemExit

    # Determine export directory path
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "../AXON/")

    logging.debug(f"Source directory for ZIP archive: {file_path}")

    # Add all CSV files to ZIP archive
    for dirname, subdirs, files in os.walk(file_path):
        for filename in files:
            try:
                zf.write(os.path.join(dirname, filename), basename(filename))
                logging.debug(f"Added to archive: {filename}")
            except FileNotFoundError:
                logging.error(f"File not found: {filename}")
                raise SystemExit

    zf.close()
    logging.info(f"ZIP archive created: {path_export}")

    # Cleanup: Remove temporary CSV directory
    if os.path.exists("../AXON/"):
        shutil.rmtree("../AXON/")
        logging.info("Cleaned up temporary CSV directory")

    logging.info("### Axon export completed successfully")


if __name__ == "__main__":
    main()
