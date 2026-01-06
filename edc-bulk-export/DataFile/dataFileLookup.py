# from ScriptsEdc.DataFile.EmptyCsvDatafileToExport import csvFilesFileNameEmpty, csvFilesColumnEmpty
from db.database import all_edc
from props.paramsEdc import (
    EDC_URL_REST_1_DATAFILE,
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

# empty array
csvFilesFileName_data = []
csvFilesColumn_data = []

# Lookup_FileColumns = []
csvLookup_data = []
Last_Run_read = {}
Last_Run_write = {}
# Opening JSON file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "DATAFILE_LOOKUP_last_updates.json")
with open(file_path, "r") as f:
    # a dictionary
    Last_Run_read = json.load(f)


# Function get RDBMS resources, do pagination and generate csv to export
def dataFileLookup():
    downloaded = 0
    if not os.path.exists("EDC"):
        os.makedirs("EDC")
    # print("Generating  DATAFILE_LOOKUP RESOURCES ....")

    pageSeizeOffset = pageSize
    resp1 = session.get(EDC_URL_REST_1_DATAFILE, headers=EDC_headers, auth=EDC_Auth)
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

        for val_hits in hits:
            values_hits = val_hits.get("values")
            for val_values in values_hits:
                if val_values.get("attributeId") == "core.resourceName":
                    resourceName = val_values.get("value")

            newDate = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            newDate_epoch = int(time.mktime(time.strptime(newDate, pattern)))
            Last_Run_write[resourceName] = str(newDate_epoch) + "000"
        generateCSV(hits, EDC_headers, EDC_Auth)
        # New - 14Sept2022
        pageSeizeOffset = pageSize
        if newTotal > pageSeizeOffset:
            while totalPage > pageSeizeOffset:
                # print("Pagination DATAFILE_LOOKUP RESOURCES: Offset items: -- ",
                #       pageSeizeOffset)
                offsetUrl = (
                    "/2/catalog/data/search?basicQuery=*&tabId=tab.resources&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22DataFile%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.Resource%22&fq="
                    + val_DGR
                    + "&facet=false&defaultFacets=true&highlight=false&offset="
                    + str(pageSeizeOffset)
                    + "&pageSize="
                    + str(pageSize)
                    + "&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted"
                )
                newUrlMain = EDC_URL_REST_2 + offsetUrl

                # print("DEBUG newUrlMain -- ", newUrlMain)

                respWhile = requests.get(newUrlMain, headers=EDC_headers, auth=EDC_Auth)
                # print("DEBUG respWhile.status_code -- ", respWhile.status_code)
                if respWhile.status_code == 200:
                    respWhileData = respWhile.json()
                    hits = respWhileData.get("hits")
                    generateCSV(hits, EDC_headers, EDC_Auth)
                else:
                    logging.error(f"Error pagination on offset: {pageSeizeOffset}")
                pageSeizeOffset += pageSize

        # Generate csv files csvLookup
        if csvLookup_data:
            df = pd.DataFrame(csvLookup_data)
            df.drop_duplicates(inplace=True)
            df.sort_values("createdOn", ascending=True, inplace=True)
            df.to_csv(os.path.join("EDC/DATAFILE_LOOKUP.csv"), sep=";", index=False)
            downloaded = downloaded + 1
        else:
            # Generate empty csv files csvLookup
            df = pd.DataFrame(csvLookupEmpty)
            df.drop_duplicates(inplace=True)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join("EDC/DATAFILE_LOOKUP.csv"), sep=";", index=False, header=True)

        # Generate csv files csvFilesFileName
        if csvFilesFileName_data:
            df = pd.DataFrame(csvFilesFileName_data)
            df.drop_duplicates(inplace=True)
            df = df.fillna("")
            for column in df.columns:
                if column != "path id" and column != "id" and column != "Name":
                    df[column] = df[column].apply(lambda x: BeautifulSoup(x, "lxml").get_text())
                    for i in chars_to_remove:
                        df = df.applymap(lambda x: x.replace(i, "") if (isinstance(x, str)) else x)
            output_path = os.path.join(csv_path + "/DATAFILE_FILES.csv")
            df.to_csv(output_path, mode="a", sep=";", index=False, header=not os.path.exists(output_path))
            downloaded = downloaded + 1

        # Generate csv files csvFilesColumn
        if csvFilesColumn_data:
            df = pd.DataFrame(csvFilesColumn_data)
            df.drop_duplicates(inplace=True)
            df = df.fillna("")
            for column in df.columns:
                if column != "File id" and column != "id" and column != "name":
                    df[column] = df[column].apply(lambda x: BeautifulSoup(x, "lxml").get_text())
                    for i in chars_to_remove:
                        df = df.applymap(lambda x: x.replace(i, "") if (isinstance(x, str)) else x)
            output_path = os.path.join(csv_path + "/DATAFILE_FILE_COLUMNS.csv")
            df.to_csv(output_path, mode="a", sep=";", index=False, header=not os.path.exists(output_path))
            downloaded = downloaded + 1

        # save json file with update date
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, "DATAFILE_LOOKUP_last_updates.json")
        with open(file_path, "w") as outfile:
            json.dump(Last_Run_write, outfile)

    else:
        logging.error(f"Main EDC failed with status code: {str(resp1.status_code)}")

    ending_time = datetime.now()  # execution script code time
    resourceName = "DataFile"
    resourceType = "Lookup"
    # db data to be saved
    all_edc(
        resourceName, resourceType, downloaded, response_code, response_size, response_time, starting_time, ending_time
    )

    return downloaded


# Function which make the pagination on offset and verify updates of the resources, get data and return json data
def generateCSV(hits, EDC_headers, EDC_Auth):
    # print("Generate CSV", hits)
    pageSeizeOffset = pageSize
    resourceName = None
    lastScanStatus = ""
    lastScanDate = ""

    for val_hits in hits:
        values_hits = val_hits.get("values")

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
            if lastScanStatus != "SUCCESS":
                logging.warning(f"Resource  {resourceName} has status not equal to SUCCESS!")
            else:
                logging.info(f"Resource {resourceName} skipped because has no updates")
            pass
        else:
            if Last_Run_read.get(resourceName) == None:
                logging.info(f"NEW Resource {resourceName} skipped")
                pass
            else:
                # Generate csv files csvLookup
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
                # print('rest 19 datafile lookup: ', singleURL)

                if resp2.status_code == 200:
                    j_resp_2req = resp2.json()
                    hits = j_resp_2req.get("items")
                    totalCount = j_resp_2req["metadata"]["totalCount"]
                    newTotal = totalCount + pageSize
                    # print(hits)

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
                                logging.error(f"Error DATAFILE_LOOKUP pagination on offset: {pageSeizeOffset}")

                            pageSeizeOffset += pageSize
                else:
                    logging.error(f"Error generating single DATAFILE_LOOKUP resource: {str(resp2.status_code)}")


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
            items["classType"] == "DataFile.Custom.Upload.FilesFileName"
            or items["classType"] == "DataFile.Custom.Upload.FilesColumnName"
        ):
            createdOn = items.get("createdOn")
            classType = items["classType"]
            objectId = items.get("objectId")
            objectLabel = items.get("objectLabel")
            resourceName = items.get("resourceName")
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
                    if childLabel == "FilesColumnName":
                        LookupFileColumnsCSV(childId, EDC_headers, EDC_Auth)

            if facts:
                for val in facts:
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
                            "chilId": "",
                            "childLabel": "",
                            "subType": "",
                        }
                    )
            if classType == "DataFile.Custom.Upload.FilesFileName":
                LookupFileNameCSV(objectId, EDC_headers, EDC_Auth)
            else:
                if classType == "DataFile.Custom.Upload.FilesColumnName":
                    LookupFileColumnsCSV(objectId, EDC_headers, EDC_Auth)

            # LookupFileColumnsCSV(objectId, EDC_headers, EDC_Auth)


def LookupFileNameCSV(childId, EDC_headers, EDC_Auth):
    dstLinksTb = []
    childId = childId.replace("\\", "/")
    idLookup_1 = childId.replace("/", "~2f~")
    idLookup = idLookup_1.replace(":", "~3a~")
    url_lookup = url_lookup_childId + idLookup

    # print("LookupFileNameCSV Id:",childId)

    lookupReq = requests.get(url_lookup, headers=EDC_headers, auth=EDC_Auth)
    if lookupReq.status_code != 200 or not lookupReq.content:
        # print('Error generating lookup data due to Error code: {} OR no data to retrieve: {}'.format(str(lookupReq.status_code), lookupReq.content))
        pass
    else:
        lookupRes = lookupReq.json()
        genFilesFileNameCSV(lookupRes)
        # print(' GENERATING FilesName........')


def LookupFileColumnsCSV(childId, EDC_headers, EDC_Auth):
    dstLinksTb = []
    childId = childId.replace("\\", "/")
    idLookup_1 = childId.replace("/", "~2f~")
    idLookup = idLookup_1.replace(":", "~3a~")
    url_lookup = url_lookup_childId + idLookup

    # print("LookupFileColumnsCSV Id:",childId)

    lookupReq = requests.get(url_lookup, headers=EDC_headers, auth=EDC_Auth)
    if lookupReq.status_code != 200 or not lookupReq.content:
        # print('Error generating lookup data due to Error code: {} OR no data to retrieve: {}'.format(str(lookupReq.status_code), lookupReq.content))
        pass
    else:
        lookupRes = lookupReq.json()
        genFilesColumnCSV(lookupRes)
        # print(' GENERATING FilesColumnName........')


# Function generating FilesFile attributs
def genFilesFileNameCSV(FilesFileNameRes):
    FF_lastModified = ""
    FF_LoadingMode = ""
    FF_Notes = ""
    FF_DataHistoricization = ""
    FF_Frequency = ""
    FF_FeedingType = ""
    FF_Transformation = ""
    FF_gdprDataProc = ""
    FF_gdprDataProcmodifiedBy = ""
    FF_DataQualityLink = ""
    FF_DataQualityLinkModifiedBy = ""
    FF_businessDescription = ""
    FF_businessDescriptionModifiedBy = ""
    FF_resourceName = ""
    FF_name = ""
    FF_Description = ""
    FF_idRes = ""
    acronym = ""

    FF_Id = FilesFileNameRes["id"]
    FFNfacts = FilesFileNameRes["facts"]
    for val in FFNfacts:
        if val.get("attributeId") == "core.lastModified":
            FF_lastModified = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.LoadingMode":
            FF_LoadingMode = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.Notes":
            FF_Notes = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.DataHistoricization":
            FF_DataHistoricization = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.Frequency":
            FF_Frequency = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.Feeding":
            FF_FeedingType = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.Transformation":
            FF_Transformation = val.get("value")
        if val.get("label") == "GDPR Data Processing note":
            FF_gdprDataProc = val.get("value")
        if val.get("label") == "GDPR Data Processing note":
            FF_gdprDataProcmodifiedBy = val.get("modifiedBy")
        if val.get("label") == "Data Quality Link":
            FF_DataQualityLink = val.get("value")
        if val.get("label") == "Data Quality Link":
            FF_DataQualityLinkModifiedBy = val.get("modifiedBy")
        if val.get("label") == "Business Description":
            FF_businessDescription = val.get("value")
        if val.get("label") == "Business Description":
            FF_businessDescriptionModifiedBy = val.get("modifiedBy")
        if val.get("attributeId") == "core.resourceName":
            FF_resourceName = val.get("value")
        if val.get("attributeId") == "core.name":
            FF_name = val.get("value")
        if val.get("attributeId") == "core.description":
            FF_Description = val.get("value")
        if val.get("label") == "Acronym":
            acronym = val.get("value")

    # FFN_srcLinks = FilesFileNameRes.get('srcLinks')
    # for scr in FFN_srcLinks:
    # if scr.get(
    #'classType') == 'DataFile.Custom.Upload.FilesPath':
    # FF_idRes = scr.get('id')
    csvFilesFileName_data.append(
        {
            "id": FF_Id,
            "Last Modified": FF_lastModified,
            "Loading Mode": FF_LoadingMode,
            "Notes": FF_Notes,
            "Data Historicization": FF_DataHistoricization,
            "Frequency": FF_Frequency,
            "Feeding": FF_FeedingType,
            "Transformation": FF_Transformation,
            "GDPR Data Processing note": FF_gdprDataProc,
            "GDPR Data Processing note modifiedBy": FF_gdprDataProcmodifiedBy,
            "Data Quality Link": FF_DataQualityLink,
            "Data Quality Link modifiedBy": FF_DataQualityLinkModifiedBy,
            "Business Description": FF_businessDescription,
            "Business Description modifiedBy": FF_businessDescriptionModifiedBy,
            "Resource Name": FF_resourceName,
            "Name": FF_name,
            "description": FF_Description,
            "path id": FF_idRes,
            "Acronym": acronym,
        }
    )


# Function generating FilesColumn attributs
def genFilesColumnCSV(FilesColumnNameRes):
    FC_name = ""
    FC_lastModified = ""
    FC_FieldPrimaryKey = ""
    FC_FieldOffset = ""
    FC_FieldODBCFormat = ""
    FC_FieldMandatory = ""
    FC_Notes = ""
    FC_Algorithm = ""
    FC_FieldUniqueIndex = ""
    FC_FieldPosition = ""
    FC_RecordType = ""
    FC_FieldLength = ""
    FC_DataFlowType = ""
    FC_FieldDomainTable = ""
    FC_Function = ""
    FC_FieldDataFormat = ""
    FC_FieldDecimals = ""
    FC_KeyDataElement = ""
    FC_KeyDataElementModifiedBy = ""
    FC_gdprDataProc = ""
    FC_gdprDataProcmodifiedBy = ""
    FC_DataQualityLink = ""
    FC_DataQualityLinkModifiedBy = ""
    FC_AssetClassification = ""
    FC_AssetClassificationModifiedBy = ""
    FC_businessDescription = ""
    FC_businessDescriptionModifiedBy = ""
    FC_resourceName = ""
    FC_description = ""
    FC_IdScr = ""

    FC_Id = FilesColumnNameRes["id"]
    facetsTb = FilesColumnNameRes["facts"]

    # print("genFilesColumnCSV facetsTb",facetsTb)
    for val in facetsTb:
        if val.get("attributeId") == "core.name":
            FC_name = val.get("value")
        if val.get("attributeId") == "core.lastModified":
            FC_lastModified = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.FieldPrimaryKey":
            FC_FieldPrimaryKey = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.FieldOffset":
            FC_FieldOffset = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.FieldODBCFormat":
            FC_FieldODBCFormat = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.FieldMandatory":
            FC_FieldMandatory = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.Notes":
            FC_Notes = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.Algorithm":
            FC_Algorithm = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.FieldUniqueIndex":
            FC_FieldUniqueIndex = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.FieldPosition":
            FC_FieldPosition = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.RecordType":
            FC_RecordType = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.FieldLength":
            FC_FieldLength = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.DataFlowType":
            FC_DataFlowType = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.FieldDomainTable":
            FC_FieldDomainTable = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.Function":
            FC_Function = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.FieldDataFormat":
            FC_FieldDataFormat = val.get("value")
        if val.get("attributeId") == "DataFile.Custom.Upload.FieldDecimals":
            FC_FieldDecimals = val.get("value")
        if val.get("label") == "Key Data Element":
            FC_KeyDataElement = val.get("value")
        if val.get("label") == "Key Data Element":
            FC_KeyDataElementModifiedBy = val.get("modifiedBy")
        if val.get("label") == "GDPR Data Processing note":
            FC_gdprDataProc = val.get("value")
        if val.get("label") == "GDPR Data Processing note":
            FC_gdprDataProcmodifiedBy = val.get("modifiedBy")
        if val.get("label") == "Data Quality Link":
            FC_DataQualityLink = val.get("value")
        if val.get("label") == "Data Quality Link":
            FC_DataQualityLinkModifiedBy = val.get("modifiedBy")
        if val.get("label") == "Asset Classification":
            FC_AssetClassification = val.get("value")
        if val.get("label") == "Asset Classification":
            FC_AssetClassificationModifiedBy = val.get("modifiedBy")
        if val.get("label") == "Business Description":
            FC_businessDescription = val.get("value")
        if val.get("label") == "Business Description":
            FC_businessDescriptionModifiedBy = val.get("modifiedBy")
        if val.get("attributeId") == "core.resourceName":
            FC_resourceName = val.get("value")
        if val.get("attributeId") == "core.description":
            FC_description = val.get("value")

    # FFN_srcLinks = FilesColumnNameRes.get('srcLinks')
    # for scr in FFN_srcLinks:

    # if scr.get(
    #'classType') == 'DataFile.Custom.Upload.FilesFileName':
    # FC_IdScr = scr.get('id')

    csvFilesColumn_data.append(
        {
            "id": FC_Id,
            "name": FC_name,
            "Last Modified": FC_lastModified,
            "Field Primary Key": FC_FieldPrimaryKey,
            "Field Offset": FC_FieldOffset,
            "Field ODBC Format": FC_FieldODBCFormat,
            "Field Mandatory": FC_FieldMandatory,
            "Notes": FC_Notes,
            "Algorithm": FC_Algorithm,
            "Field Unique Index": FC_FieldUniqueIndex,
            "Field Position": FC_FieldPosition,
            "Record Type": FC_RecordType,
            "Field Length": FC_FieldLength,
            "Data Flow Type": FC_DataFlowType,
            "Field Domain Table": FC_FieldDomainTable,
            "Function": FC_Function,
            "Field Data Format": FC_FieldDataFormat,
            "Field Decimals": FC_FieldDecimals,
            "Key Data Element": FC_KeyDataElement,
            "Key Data Element modifiedBy": FC_KeyDataElementModifiedBy,
            "GDPR Data Processing note": FC_gdprDataProc,
            "GDPR Data Processing note modifiedBy": FC_gdprDataProcmodifiedBy,
            "Data Quality Link": FC_DataQualityLink,
            "Data Quality Link modifiedBy": FC_DataQualityLinkModifiedBy,
            "Asset Classification": FC_AssetClassification,
            "Asset Classification modifiedBy": FC_AssetClassificationModifiedBy,
            "Business Description": FC_businessDescription,
            "Business Description modifiedBy": FC_businessDescriptionModifiedBy,
            "Resource Name": FC_resourceName,
            "description": FC_description,
            "File id": FC_IdScr,
        }
    )


def mainDataFileLookup():
    try:
        return dataFileLookup()
    except Exception as e:
        return e
