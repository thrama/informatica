# from ScriptsEdc.RdbmsResources.EmptyCsvRdbmsToExport import csvTableEmpty, csvColumnEmpty
from db.database import all_edc
from props.paramsEdc import (
    EDC_URL,
    EDC_URL_REST_1_RELATIONAL,
    EDC_URL_REST_2,
    EDC_Auth,
    EDC_headers,
    chars_to_remove,
    csv_path,
    pageSize,
    url_lookup_childId,
    val_DGR,
)
from props.utils import BeautifulSoup, HTTPAdapter, Retry, datetime, json, logging, os, pd, requests, time

from .EmptyCsvLookupToExport import csvLookupEmpty

session = requests.Session()
retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
# retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)

pattern = "%Y-%m-%d %H:%M:%S"

csvLookup_data = []
csvTable_data = []
csvColumn_data = []

Last_Run_read = {}
Last_Run_write = {}
resourceName = None

# Opening JSON file
script_dir = os.path.dirname(__file__)
# EDC_dir = os.path.join(os.getcwd(), 'EDC_Scripts\EDC')
file_path = os.path.join(script_dir, "RDBMS_LOOKUP_last_updates.json")
with open(file_path, "r") as f:
    # a dictionary
    Last_Run_read = json.load(f)


# Function get RDBMS resources, do pagination and generate csv to export
def rdbmsResourcesLookup():
    downloaded = 0
    if not os.path.exists("EDC"):
        os.makedirs("EDC")
    # print("Generating  RDBMS_LOOKUP RESOURCES ....")

    pageSeizeOffset = pageSize
    resp1 = session.get(EDC_URL_REST_1_RELATIONAL, headers=EDC_headers, auth=EDC_Auth)
    # db data to be saved
    starting_time = datetime.now()
    # server response time converted in seconds
    response_time = str(resp1.elapsed.total_seconds()) + " s"
    # server response sice converted in kb
    response_size = str(len(resp1.content) / 1024) + " kb"
    response_code = resp1.status_code  # server status code
    # end db data
    if resp1.status_code == 200:
        j_resp_2req = resp1.json()
        hits = j_resp_2req.get("hits")
        totalPage = j_resp_2req["metadata"]["totalCount"]
        newTotal = totalPage + pageSize

        generateCSV(hits, Last_Run_read, EDC_headers, EDC_Auth)
        # New - 14Sept2022
        pageSeizeOffset = pageSize
        if newTotal > pageSeizeOffset:
            while totalPage > pageSeizeOffset:
                # print("Pagination RDBMS_LOOKUP RESOURCES: Offset items: -- ",
                #       pageSeizeOffset)
                offsetUrl = (
                    "/access/2/catalog/data/search?basicQuery=*&tabId=tab.resources&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22JDBC%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Teradata%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Hive%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22IBM%5C%20DB2%5C%20for%5C%20z%5C%2FOS%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Oracle%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Azure%5C%20Microsoft%5C%20SQL%5C%20Server%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Microsoft%20SQL%20Server%22&fq="
                    + val_DGR
                    + "&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize="
                    + str(pageSize)
                    + "&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted"
                )
                newUrlMain = EDC_URL + offsetUrl

                respWhile = requests.get(newUrlMain, headers=EDC_headers, auth=EDC_Auth)
                if respWhile.status_code == 200:
                    respWhileData = respWhile.json()
                    hits = respWhileData.get("hits")
                    generateCSV(hits, Last_Run_read, EDC_headers, EDC_Auth)
                else:
                    logging.error(f"Error pagination on offset: {pageSeizeOffset}")
                pageSeizeOffset += pageSize

        # Generate csv files csvLookup
        if csvLookup_data:
            df = pd.DataFrame(csvLookup_data)
            df.drop_duplicates(inplace=True)
            df.sort_values("createdOn", ascending=True, inplace=True)
            df.to_csv(os.path.join("EDC/RDBMS_LOOKUP.csv"), sep=";", index=False)
            downloaded = downloaded + 1
        else:
            # Generate empty csv files csvLookup
            df = pd.DataFrame(csvLookupEmpty)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join("EDC/RDBMS_LOOKUP.csv"), sep=";", index=False, header=True)

        # Generate csv files csvTable
        if csvTable_data:
            df = pd.DataFrame(csvTable_data)
            df.drop_duplicates(inplace=True)
            # print('df table: ', df)
            df = df.fillna("")
            for column in df.columns:
                df[column] = df[column].apply(lambda x: BeautifulSoup(x, "lxml").get_text())
                for i in chars_to_remove:
                    df = df.applymap(lambda x: x.replace(i, "") if (isinstance(x, str)) else x)
            output_path = os.path.join(csv_path + "/RDBMS_TABLE VIEWS.csv")
            df.to_csv(output_path, mode="a", sep=";", index=False, header=not os.path.exists(output_path))
            downloaded = downloaded + 1

        # Generate csv files csvTable
        if csvColumn_data:
            df = pd.DataFrame(csvColumn_data)
            df.drop_duplicates(inplace=True)
            # print('df csvColumn_data: ', df)
            df = df.fillna("")
            for column in df.columns:
                df[column] = df[column].apply(lambda x: BeautifulSoup(x, "lxml").get_text())
                for i in chars_to_remove:
                    df = df.applymap(lambda x: x.replace(i, "") if (isinstance(x, str)) else x)
            output_path = os.path.join(csv_path + "/RDBMS_COLUMNS.csv")
            df.to_csv(output_path, mode="a", sep=";", index=False, header=not os.path.exists(output_path))
            downloaded = downloaded + 1

        # save json file with update date
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, "RDBMS_LOOKUP_last_updates.json")
        with open(file_path, "w") as outfile:
            json.dump(Last_Run_write, outfile)
    else:
        logging.error(f"Main EDC failed with status code: {str(resp1.status_code)}")

    ending_time = datetime.now()  # execution script code time
    resourceName = "Rdbms"
    resourceType = "Lookup"
    # db data to be saved
    all_edc(
        resourceName, resourceType, downloaded, response_code, response_size, response_time, starting_time, ending_time
    )

    return downloaded


# Function which make the pagination on offset and verify updates of the resources, get data and return json data
def generateCSV(hits, Last_Run_read, EDC_headers, EDC_Auth):
    # print(hits)
    pageSeizeOffset = pageSize
    resourceName = None

    for val_hits in hits:
        values_hits = val_hits.get("values")
        newResourceFailed = 0
        lastScanStatus = "NONE"
        lastScanDate = ""

        for val_values in values_hits:
            if val_values.get("attributeId") == "core.resourceName":
                resourceName = val_values.get("value")
            if val_values.get("attributeId") == "core.lastScanStatus":
                lastScanStatus = val_values.get("value")
            if val_values.get("attributeId") == "core.lastScanDate":
                lastScanDate = val_values.get("value")

        lastScan = str(lastScanDate)
        lastRun = Last_Run_read.get(resourceName)
        if not lastRun:
            Last_Run = 631152001000

        else:
            Last_Run = int(Last_Run_read.get(resourceName))

        checkLastRun = datetime.fromtimestamp(Last_Run / 1000).strftime("%Y-%m-%dT%H:%M:%S")

        if lastScanStatus != "SUCCESS" or lastScan < checkLastRun:
            # print('Last Scan Status Failed or Last Scan Date no data...')
            if Last_Run == 631152001000 and lastScanStatus != "SUCCESS":
                newResourceFailed = 1
                logging.warning(f"NEW resource  {resourceName} has status not equal to SUCCESS!")
            pass
        else:
            # Generate Lookup
            if Last_Run_read.get(resourceName) == None:
                logging.info(f"Resource {resourceName} skipped because is never changed since the last run")
                pass
            else:
                logging.info(f"Working on {resourceName}")
                fromDate = Last_Run_read.get(resourceName)

                singleURL = (
                    EDC_URL_REST_2
                    + "/2/catalog/data/app_events?resourceName="
                    + resourceName
                    + "&offset=0&pageSize="
                    + str(pageSize)
                    + "&sortBy=createdOn&responseType=DETAILED&changeType=SOURCE&since="
                    + str(fromDate)
                )
                resp2 = session.get(singleURL, headers=EDC_headers, auth=EDC_Auth)
                # print('rest 19 rdbms lookup: ', singleURL)

                if resp2.status_code == 200:
                    j_resp_2req = resp2.json()
                    hits = j_resp_2req.get("items")
                    totalCount = j_resp_2req["metadata"]["totalCount"]
                    newTotal = totalCount + pageSize
                    genLookupCSV(hits)
                    # New - 14Sept2022
                    pageSeizeOffset = pageSize
                    if newTotal > pageSeizeOffset:
                        while totalCount > pageSeizeOffset:
                            offsetUrl = (
                                "/2/catalog/data/app_events?resourceName="
                                + resourceName
                                + "&offset="
                                + str(pageSeizeOffset)
                                + "&pageSize="
                                + str(pageSize)
                                + "&sortBy=createdOn&responseType=DETAILED&changeType=SOURCE&since="
                                + str(fromDate)
                            )
                            newUrlMain = EDC_URL_REST_2 + offsetUrl
                            newResp = session.get(newUrlMain, headers=EDC_headers, auth=EDC_Auth)
                            if newResp.status_code == 200:
                                newrespeData = newResp.json()
                                hits = newrespeData.get("items")
                                genLookupCSV(hits)
                            else:
                                print("Error rdbms lookup pagination on offset: ", pageSeizeOffset)
                            pageSeizeOffset += pageSize

                else:
                    logging.error(f"Error generating single resource: {str(resp2.status_code)}")

        # update timestamp for each resource
        if newResourceFailed == 0:
            newDate = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            newDate_epoch = int(time.mktime(time.strptime(newDate, pattern)))
            Last_Run_write[resourceName] = str(newDate_epoch) + "000"


# Function generating RDBMS LOOKUP attributs
def genLookupCSV(hits):
    # print('hits: ', hits)
    createdOn = ""
    objectId = ""
    objectLabel = ""
    resourceName = ""
    operation = ""
    childId = ""
    childLabel = ""
    subType = ""

    for items in hits:
        if (
            (items["objectLabel"] == "Table")
            or (items["objectLabel"] == "View")
            or (items["objectLabel"] == "Column")
            or (items["objectLabel"] == "ViewColumn")
        ):
            createdOn = items.get("createdOn")
            objectId = items.get("objectId")
            objectLabel = items.get("objectLabel")
            resourceName = items.get("resourceName")
            logging.info(f"Resource Name: {resourceName}")
            operation = items.get("operation")

            objects = items.get("objects")
            facts = items.get("facts")
            if objects:
                for val in objects:
                    childId = val.get("id")
                    childLabel = val.get("label")
                    subType = val.get("subType")

                    csvLookup_data.append(
                        {
                            "createdOn": createdOn,
                            "objectId": objectId,
                            "objectLabel": objectLabel,
                            "resourceName": resourceName,
                            "operation": operation,
                            "chilId": childId,
                            "childLabel": childLabel,
                            "subType": subType,
                        }
                    )
                    if childLabel == "Column" or childLabel == "ViewColumn":
                        genColRdbmsCSVs(childId, EDC_headers, EDC_Auth)

                genTabRdbmsCSVs(objectId, EDC_headers, EDC_Auth)

            if facts:
                for val in facts:
                    csvLookup_data.append(
                        {
                            "createdOn": createdOn,
                            "objectId": objectId,
                            "objectLabel": objectLabel,
                            "resourceName": resourceName,
                            "operation": operation,
                            "chilId": "",
                            "childLabel": "",
                            "subType": "",
                        }
                    )
                if objectLabel == "Column" or objectLabel == "ViewColumn":
                    genColRdbmsCSVs(objectId, EDC_headers, EDC_Auth)
                else:
                    genTabRdbmsCSVs(objectId, EDC_headers, EDC_Auth)


# Function get data and return json data
def genTabRdbmsCSVs(childId, EDC_headers, EDC_Auth):
    idLookup_1 = childId.replace("/", "~2f~")
    idLookup = idLookup_1.replace(":", "~3a~")
    url_lookup = url_lookup_childId + idLookup
    # print('url_lookup Table', url_lookup)

    lookupReq = requests.get(url_lookup, headers=EDC_headers, auth=EDC_Auth)

    if lookupReq.status_code != 200 or not lookupReq.content:
        # print('Error generating lookup data due to Error code: {} OR no data to retrieve: {}'.format(str(lookupReq.status_code), lookupReq.content))
        pass
    else:
        lookupRes = lookupReq.json()
        valHits = lookupRes.get("facts")
        # print('valHits', valHits)
        for v in valHits:
            if (v["attributeId"] == "core.classType" and v["value"] == "com.infa.ldm.relational.Table") or (
                v["attributeId"] == "core.classType" and v["value"] == "com.infa.ldm.relational.View"
            ):
                tableURL = url_lookup
                # print('tableURL: ', tableURL)
                tableReq = session.get(tableURL, headers=EDC_headers, auth=EDC_Auth)
                # handle other errors
                if tableReq.status_code == 200:
                    if not tableReq.content:
                        pass
                    else:
                        tableRes = tableReq.json()
                        # dstLinksTb = tableRes['dstLinks']
                        genTableCSV(tableRes)


# Function get data and return json data
def genColRdbmsCSVs(childId, EDC_headers, EDC_Auth):
    dstLinksTb = []
    idLookup_1 = childId.replace("/", "~2f~")
    idLookup = idLookup_1.replace(":", "~3a~")
    url_lookup = url_lookup_childId + idLookup
    # print('url_lookup Column', url_lookup)
    lookupReq = requests.get(url_lookup, headers=EDC_headers, auth=EDC_Auth)

    if lookupReq.status_code != 200 or not lookupReq.content:
        # print('Error generating lookup data due to Error code: {} OR no data to retrieve: {}'.format(str(lookupReq.status_code), lookupReq.content))
        pass
    else:
        lookupRes = lookupReq.json()
        valHits = lookupRes.get("facts")
        # print('valHits', valHits)
        for v in valHits:
            # for val in dstLinksTb:
            if (v["attributeId"] == "core.classType" and v["value"] == "com.infa.ldm.relational.Column") or (
                v["attributeId"] == "core.classType" and v["value"] == "com.infa.ldm.relational.ViewColumn"
            ):
                columUrl = url_lookup
                columReq = session.get(columUrl, headers=EDC_headers, auth=EDC_Auth)
                # handle other errors
                if columReq.status_code == 200:
                    if not columReq.content:
                        pass
                    else:
                        columnRes = columReq.json()
                        genColumnCSV(columnRes)


# Function generating Table View attributs
def genTableCSV(tableRes):
    Tb_childId = ""
    Tb_lastModified = ""
    Tb_gdprDataProc = ""
    Tb_gdprDataProcmodifiedBy = ""
    Tb_DataQualityLink = ""
    Tb_DataQualityLinkModifiedBy = ""
    Tb_businessDescription = ""
    Tb_businessDescriptionModifiedBy = ""
    Tb_NativeType = ""
    Tb_resourceName = ""
    Tb_name = ""
    Tb_SchemaId = ""

    Tb_childId = tableRes["id"]
    facetsTb = tableRes["facts"]
    for val in facetsTb:
        if val.get("attributeId") == "core.lastModified":
            Tb_lastModified = val.get("value")
        if val.get("label") == "GDPR Data Processing note":
            Tb_gdprDataProc = val.get("value")
        if val.get("label") == "GDPR Data Processing note":
            Tb_gdprDataProcmodifiedBy = val.get("modifiedBy")
        if val.get("label") == "Data Quality Link":
            Tb_DataQualityLink = val.get("value")
        if val.get("label") == "Data Quality Link":
            Tb_DataQualityLinkModifiedBy = val.get("modifiedBy")
        if val.get("label") == "Business Description":
            Tb_businessDescription = val.get("value")
        if val.get("label") == "Business Description":
            Tb_businessDescriptionModifiedBy = val.get("modifiedBy")
        if val.get("attributeId") == "com.infa.ldm.relational.NativeType":
            Tb_NativeType = val.get("value")
        if val.get("attributeId") == "core.resourceName":
            Tb_resourceName = val.get("value")
        if val.get("attributeId") == "core.name":
            Tb_name = val.get("value")

    tablesrcLinks = tableRes["srcLinks"]
    for valScr in tablesrcLinks:
        if valScr.get("classType") == "com.infa.ldm.relational.Schema":
            Tb_SchemaId = valScr.get("id")

    csvTable_data.append(
        {
            "id": Tb_childId,
            "Last Modified": Tb_lastModified,
            "GDPR Data Processing note": Tb_gdprDataProc,
            "GDPR Data Processing note modifiedBy": Tb_gdprDataProcmodifiedBy,
            "Data Quality Link": Tb_DataQualityLink,
            "Data Quality Link modifiedBy": Tb_DataQualityLinkModifiedBy,
            "Business Description": Tb_businessDescription,
            "Business Description modifiedBy": Tb_businessDescriptionModifiedBy,
            "Native Type": Tb_NativeType,
            "Resource Name": Tb_resourceName,
            "Name": Tb_name,
            "Schema id": Tb_SchemaId,
        }
    )
    # print('csvTable_data: ', csvTable_data)


# Function generating Columns attributs
def genColumnCSV(columnRes):
    Cl_childId = ""
    Cl_name = ""
    Cl_lastModified = ""
    Cl_KeyDataElement = ""
    Cl_KeyDataElementModifiedBy = ""
    Cl_gdprDataProc = ""
    Cl_gdprDataProcmodifiedBy = ""
    Cl_DataQualityLink = ""
    Cl_DataQualityLinkModifiedBy = ""
    Cl_AssetClassification = ""
    Cl_AssetClassificationModifiedBy = ""
    Cl_businessDescription = ""
    Cl_businessDescriptionModifiedBy = ""
    Cl_DatatypeScale = ""
    Cl_Position = ""
    Cl_Identity = ""
    Cl_NativeType = ""
    Cl_PrimaryKeyColumn = ""
    Cl_Nullable = ""
    Cl_DatatypeLength = ""
    Cl_Datatype = ""
    Cl_resourceName = ""
    Cl_finalId = ""

    factsCols = columnRes["facts"]
    Cl_childId = columnRes["id"]
    for val in factsCols:
        if val.get("attributeId") == "core.name":
            Cl_name = val.get("value")
        if val.get("attributeId") == "core.lastModified":
            Cl_lastModified = val.get("value")
        if val.get("label") == "Key Data Element":
            Cl_KeyDataElement = val.get("value")
        if val.get("label") == "Key Data Element":
            Cl_KeyDataElementModifiedBy = val.get("modifiedBy")
        if val.get("label") == "GDPR Data Processing note":
            Cl_gdprDataProc = val.get("value")
        if val.get("label") == "GDPR Data Processing note":
            Cl_gdprDataProcmodifiedBy = val.get("modifiedBy")
        if val.get("label") == "Data Quality Link":
            Cl_DataQualityLink = val.get("value")
        if val.get("label") == "Data Quality Link":
            Cl_DataQualityLinkModifiedBy = val.get("modifiedBy")
        if val.get("label") == "Asset Classification":
            Cl_AssetClassification = val.get("value")
        if val.get("label") == "Asset Classification":
            Cl_AssetClassificationModifiedBy = val.get("modifiedBy")
        if val.get("label") == "Business Description":
            Cl_businessDescription = val.get("value")
        if val.get("label") == "Business Description":
            Cl_businessDescriptionModifiedBy = val.get("modifiedBy")
        if val.get("attributeId") == "com.infa.ldm.relational.DatatypeScale":
            Cl_DatatypeScale = val.get("value")
        if val.get("attributeId") == "com.infa.ldm.relational.Position":
            Cl_Position = val.get("value")
        if val.get("attributeId") == "com.infa.ldm.relational.Identity":
            Cl_Identity = val.get("value")
        if val.get("attributeId") == "com.infa.ldm.relational.NativeType":
            Cl_NativeType = val.get("value")
        if val.get("attributeId") == "com.infa.ldm.relational.PrimaryKeyColumn":
            Cl_PrimaryKeyColumn = val.get("value")
        if val.get("attributeId") == "com.infa.ldm.relational.Nullable":
            Cl_Nullable = val.get("value")
        if val.get("attributeId") == "com.infa.ldm.relational.DatatypeLength":
            Cl_DatatypeLength = val.get("value")
        if val.get("attributeId") == "com.infa.ldm.relational.Datatype":
            Cl_Datatype = val.get("value")
        if val.get("attributeId") == "core.resourceName":
            Cl_resourceName = val.get("value")

    tablesrcLinks = columnRes["srcLinks"]
    for valScr in tablesrcLinks:
        if (
            valScr.get("classType") == "com.infa.ldm.relational.Table"
            or valScr.get("classType") == "com.infa.ldm.relational.View"
        ):
            Cl_finalId = valScr.get("id")

    csvColumn_data.append(
        {
            "id": Cl_childId,
            "name": Cl_name,
            "Last Modified": Cl_lastModified,
            "Key Data Element": Cl_KeyDataElement,
            "Key Data Element modifiedBy": Cl_KeyDataElementModifiedBy,
            "GDPR Data Processing note": Cl_gdprDataProc,
            "GDPR Data Processing note modifiedBy": Cl_gdprDataProcmodifiedBy,
            "Data Quality Link": Cl_DataQualityLink,
            "Data Quality Link modifiedBy": Cl_DataQualityLinkModifiedBy,
            "Asset Classification": Cl_AssetClassification,
            "Asset Classification modifiedBy": Cl_AssetClassificationModifiedBy,
            "Business Description": Cl_businessDescription,
            "Business Description modifiedBy": Cl_businessDescriptionModifiedBy,
            "Datatype Scale": Cl_DatatypeScale,
            "Position": Cl_Position,
            "Identity": Cl_Identity,
            "Native Type": Cl_NativeType,
            "Primary Key Column": Cl_PrimaryKeyColumn,
            "Nullable": Cl_Nullable,
            "Datatype Length": Cl_DatatypeLength,
            "Datatype": Cl_Datatype,
            "Resource Name": Cl_resourceName,
            "TableView id": Cl_finalId,
        }
    )
    # print(csvColumn_data)


def mainRdbmsResourcesLookup():
    try:
        return rdbmsResourcesLookup()
    except Exception as e:
        return e
