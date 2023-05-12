from props.utils import os, pd, requests, HTTPAdapter, json, dt_string, datetime, toDateEdc, Retry, BeautifulSoup, logging
from props.paramsEdc import EDC_URL_REST_1_DATAFILE, EDC_URL_REST_2, EDC_headers, EDC_Auth, pageSize, EDC_URL, chars_to_remove, val_DGR
from .EmptyCsvDatafileToExport import csvFilesPathEmpty, csvFilesFileNameEmpty, csvFilesColumnEmpty
from db.database import all_edc

session = requests.Session()
retry = Retry(total=5,
              backoff_factor=1,
              status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# empty array
csvFilesPath_data = []
csvFilesFileName_data = []
csvFilesColumn_data = []
Last_Run_read = {}
Last_Run_write = {}
# Opening JSON file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'DATAFILE_EXTRA_last_updates.json')
with open(file_path, 'r') as f:
    # a dictionary
    Last_Run_read = json.load(f)

# post api with raw data & get response and add to csv
# Function get DataFile resources, do pagination and generate csv to export
def datafileResourcesExtra():
    downloaded = 0
    if not os.path.exists('EDC'):
        os.makedirs('EDC')
    pageSeizeOffset = pageSize
    resp1 = requests.get(EDC_URL_REST_1_DATAFILE,
                         headers=EDC_headers, auth=EDC_Auth, verify=False)
    # db data to be saved
    starting_time = datetime.now()
    # server response time converted in seconds
    response_time = str(resp1.elapsed.total_seconds()) + ' s'
    # server response sice converted in kb
    response_size = str(len(resp1.content) / 1024) + ' kb'
    response_code = resp1.status_code  # server status code
    # end db data
    if resp1.status_code == 200:
        j_resp_1req = resp1.json()
        # startingTime = str(dt_string)
        hits = j_resp_1req.get('hits')
        totalPage = j_resp_1req['metadata']['totalCount']
        newTotal = totalPage + pageSize
        generateCSV(hits, EDC_headers, EDC_Auth)
        # New - 14Sept2022
        pageSeizeOffset = pageSize
        if newTotal > pageSeizeOffset:
            while totalPage > pageSeizeOffset:
                # print("Pagination EXTRA_DATAFILE RESOURCES: Offset items: -- ", pageSeizeOffset)
                offsetUrl = '/access/2/catalog/data/search?basicQuery=*&tabId=tab.resources&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22DataFile%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.Resource%22&fq=' + val_DGR + '&facet=false&defaultFacets=true&highlight=false&offset='+str(pageSeizeOffset)+'&pageSize=' + str(pageSize) + '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'
                newUrlMain = EDC_URL + offsetUrl

                respWhile = requests.get(
                    newUrlMain, headers=EDC_headers, auth=EDC_Auth, verify=False)

                if respWhile.status_code == 200:
                    respWhileData = respWhile.json()
                    hits = respWhileData.get('hits')
                    generateCSV(
                        hits, EDC_headers, EDC_Auth)
                else:
                    logging.error(f"Error pagination on offset: {pageSeizeOffset}")

                pageSeizeOffset += pageSize

        # Generate csv files csvFilesPath
        if csvFilesPath_data:
            df = pd.DataFrame(csvFilesPath_data)
            df.drop_duplicates(inplace=True)
            df = df.fillna('')
            for column in df.columns:
                if column != "name" and column != "id" and column != "Name":
                    df[column] = df[column].apply( lambda x: BeautifulSoup(x, 'lxml').get_text())
                    for i in chars_to_remove:
                        df = df.applymap(lambda x: x.replace( i, '') if (isinstance(x, str)) else x)
            df.to_csv(os.path.join(
                'EDC/DATAFILE_PATHS_EXTRA.csv'), sep=";", index=False)
            downloaded = downloaded + 1
        else:
            df = pd.DataFrame(csvFilesPathEmpty)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join(
                'EDC/DATAFILE_PATHS_EXTRA.csv'), sep=";", index=False, header=True)

        # Generate csv files csvFilesFileName
        if csvFilesFileName_data:
            df = pd.DataFrame(csvFilesFileName_data)
            df.drop_duplicates(inplace=True)
            df = df.fillna('')
            for column in df.columns:
                if column != "path id" and column != "id" and column != "Name":
                    df[column] = df[column].apply( lambda x: BeautifulSoup(x, 'lxml').get_text())
                    for i in chars_to_remove:
                        df = df.applymap(lambda x: x.replace( i, '') if (isinstance(x, str)) else x)
            df.to_csv(os.path.join(
                'EDC/DATAFILE_FILES_EXTRA.csv'), sep=";", index=False)
            downloaded = downloaded + 1
        else:
            df = pd.DataFrame(csvFilesFileNameEmpty)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join(
                'EDC/DATAFILE_FILES_EXTRA.csv'), sep=";", index=False, header=True)

        # Generate csv files csvFiles
        if csvFilesColumn_data:
            df = pd.DataFrame(csvFilesColumn_data)
            df.drop_duplicates(inplace=True)
            df = df.fillna('')
            for column in df.columns:
                if column != "File id" and column != "id" and column != "name":
                    df[column] = df[column].apply( lambda x: BeautifulSoup(x, 'lxml').get_text())
                    for i in chars_to_remove:
                        df = df.applymap(lambda x: x.replace( i, '') if (isinstance(x, str)) else x)
            df.to_csv(os.path.join(
                'EDC/DATAFILE_FILE_COLUMNS_EXTRA.csv'), sep=";", index=False)
            downloaded = downloaded + 1
        else:
            df = pd.DataFrame(csvFilesColumnEmpty)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join(
                'EDC/DATAFILE_FILE_COLUMNS_EXTRA.csv'), sep=";", index=False, header=True)

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(
            script_dir, 'DATAFILE_EXTRA_last_updates.json')
        with open(file_path, 'w') as outfile:
            json.dump(Last_Run_write, outfile)
    else:
        logging.error(f"Main EDC failed with status code: {str(resp1.status_code)}")

    ending_time = datetime.now()  # execution script code time
    resourceName = 'DataFile'
    resourceType = 'Extra'
    # db data to be saved
    all_edc(resourceName, resourceType, downloaded, response_code,
            response_size, response_time, starting_time, ending_time)
    # print("DEBUG downloaded -- ",downloaded)
    return downloaded


# Function which make the pagination on offset and verify updates of the resources
def generateCSV(hits, EDC_headers, EDC_Auth):

    pageSeizeOffset = pageSize
    for val_hits in hits:
        values_hits = val_hits.get('values')
        resourceName = None

        for val_values in values_hits:
            if val_values.get('attributeId') == 'core.resourceName':
                resourceName = val_values.get('value')

        #print("DEBUG resourceName --",resourceName)

        for key, value in Last_Run_read.items():
            if key == resourceName:
                value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

                searchDate = str(value.isoformat())
                fromDate = searchDate.replace(":", "%3A")
                toDate = toDateEdc.replace(":", "%3A")

                #singleURL = EDC_URL_REST_2 + '/2/catalog/data/search?basicQuery='+resourceName+'&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesPath%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesFileName%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesColumnName%22&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize=' + \
                #str(pageSize) +'&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted&fq=core.lastModified%3A%5B'+fromDate+'.000Z%20TO%20'+toDate+'.000Z%5D'

                singleURL = EDC_URL_REST_2 + '/2/catalog/data/search?basicQuery=*&tabId=all&fq=%7B!tag%3Dresource_name%7Dcore.resourceName%3A%22' + resourceName + '%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesPath%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesFileName%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesColumnName%22&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize=' + str(pageSize) + '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted&fq=core.lastModified%3A%5B'+fromDate+'.000Z%20TO%20'+toDate+'.000Z%5D'

                # print('single url : \n'+singleURL)
                resp2 = requests.get(
                    singleURL, headers=EDC_headers, auth=EDC_Auth, verify=False)
                if resp2.status_code == 200:
                    j_resp_2req = resp2.json()
                    hits = j_resp_2req.get('hits')
                    totalCount = j_resp_2req['metadata']['totalCount']
                    newTotal = totalCount + pageSize                    

                    logging.info(f"Working on {resourceName} with  {totalCount} assets]")
                    for val in hits:
                        if not val in hits:
                            pass
                        else:
                            valHref = val['href']
                            valHits = val['values']
                            
                            generateAlldataFileCSV(
                                resourceName, valHits, valHref, EDC_headers, EDC_Auth)
                    # New - 14Sept2022
                    pageSeizeOffset = pageSize
                    if newTotal > pageSeizeOffset:
                        while totalCount > pageSeizeOffset:                
                            #offsetUrl = '/access/2/catalog/data/search?basicQuery=*&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesPath%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesFileName%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesColumnName%22&facet=false&defaultFacets=true&highlight=false&offset='+str(pageSeizeOffset)+'&pageSize=' + \
                                #str(pageSize) +'&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted&fq=core.lastModified%3A%5B'+fromDate+'.000Z%20TO%20'+toDate+'.000Z%5D'
                            offsetUrl = '/access/2/catalog/data/search?basicQuery=*&tabId=all&fq=%7B!tag%3Dresource_name%7Dcore.resourceName%3A%22' + resourceName + '%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesPath%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesFileName%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesColumnName%22&facet=false&defaultFacets=true&highlight=false&offset=' +str(pageSeizeOffset)+'&pageSize=' + str(pageSize) + '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted&fq=core.lastModified%3A%5B'+fromDate+'.000Z%20TO%20'+toDate+'.000Z%5D'
                                
                            #print('DEBUG offset url : \n'+offsetUrl)
                            newUrlMain = EDC_URL + offsetUrl
                            newResp = requests.get(
                                newUrlMain, headers=EDC_headers, auth=EDC_Auth, verify=False)
                            if newResp.status_code == 200:
                                newrespeData = newResp.json()
                                hits = newrespeData.get('hits')
                                generateAlldataFileCSV(resourceName, valHits, valHref, EDC_headers, EDC_Auth)
                            else:
                                logging.error(f"Error DataFile pagination on offset: {pageSeizeOffset}")
                            pageSeizeOffset += pageSize

                else:
                    logging.error("Error generating single resource.")

        pushToArray(resourceName)

# Function get data and return json data
def pushToArray(resourceName):
    # print('res name here: ', resourceName)
    Last_Run_write[resourceName] = datetime.utcnow().strftime(
        "%Y-%m-%d %H:%M:%S")

def generateAlldataFileCSV(resourceName, valHits, valHref, EDC_headers, EDC_Auth):
    # dstLinksTb = []
    # post api with raw data & get response and add to csv
    if Last_Run_read.get(resourceName) == None:
        pass
    else:        
        for v in valHits:
            if v['attributeId'] == 'core.classType' and v['value'] == 'DataFile.Custom.Upload.FilesPath':
                FilesPathURL = EDC_URL_REST_2 + valHref
                # print('URL File Path extra', FilesPathURL)
                FilesPathReq = session.get(
                    FilesPathURL, headers=EDC_headers, auth=EDC_Auth, verify=False)
                if FilesPathReq.status_code == 200:
                    if not FilesPathReq.content:
                        pass
                    else:
                        FilesPathRes = FilesPathReq.json()
                        genFilePathCSV(FilesPathRes)
                        # print(' GENERATING FilesPath........')

            if v['attributeId'] == 'core.classType' and v['value'] == 'DataFile.Custom.Upload.FilesFileName':
                FilesFileNameURL = EDC_URL_REST_2 + valHref
                # print('URL File Name extra', FilesFileNameURL)
                FilesFileNameReq = session.get(
                    FilesFileNameURL, headers=EDC_headers, auth=EDC_Auth, verify=False)
                if FilesFileNameReq.status_code == 200:
                    if not FilesFileNameReq.content:
                        pass
                    else:
                        FilesFileNameRes = FilesFileNameReq.json()
                        dstLinksTb = FilesFileNameRes['dstLinks']
                        genFilesFileNameCSV(FilesFileNameRes, resourceName)
                        # print(' GENERATING FilesFileName........')

            if v['attributeId'] == 'core.classType' and v['value'] == 'DataFile.Custom.Upload.FilesColumnName':
                 FilesColumnNameURL = EDC_URL_REST_2 + valHref
                 # print('URL File Columns extra', FilesColumnNameURL)
                 FilesColumnNameReq = session.get(
                 FilesColumnNameURL, headers=EDC_headers, auth=EDC_Auth, verify=False)
                 # handle other errors
                 if FilesColumnNameReq.status_code == 200:
                     if not FilesColumnNameReq.content:
                          pass
                     else:
                          FilesColumnNameRes = FilesColumnNameReq.json()
                          genFilesColumnCSV(
                          FilesColumnNameRes, resourceName)
                          # print(' GENERATING COLUMN........')


# Function generating FilesPath attributs
def genFilePathCSV(FilesPathRes):
    FP_name = ''
    FP_lastModified = ''
    FP_gdprDataProc = ''
    FP_gdprDataProcModifiedBy = ''
    FP_businessDescription = ''
    FP_businessDescriptionModifiedBy = ''
    FP_resourceName = ''
    FP_resourceType = ''
    FP_Description = ''
    FP_Id = FilesPathRes['id']

    #print("DEBUG id --", FP_Id)
    facetsDb = FilesPathRes['facts']
    for val in facetsDb:

        if val.get('attributeId') == 'core.name':
            FP_name = val.get('value')
        if val.get('attributeId') == 'core.lastModified':
            FP_lastModified = val.get(
                'value')
        if val.get('label') == 'GDPR Data Processing note':
            FP_gdprDataProc = val.get(
                'value')
        if val.get('label') == 'GDPR Data Processing note':
            FP_gdprDataProcModifiedBy = val.get(
                'modifiedBy')
        if val.get(
                'label') == 'Business Description':
            FP_businessDescription = val.get('value')
        if val.get('label') == 'Business Description':
            FP_businessDescriptionModifiedBy = val.get(
                'modifiedBy')
        if val.get('attributeId') == 'core.resourceName':
            FP_resourceName = val.get(
                'value')
        if val.get('attributeId') == 'core.resourceType':
            FP_resourceType = val.get(
                'value')
        if val.get('attributeId') == 'core.description':
            FP_Description = val.get(
                'value')

    csvFilesPath_data.append({
        'id': FP_Id,
        'name': FP_name,
        'Last Modified': FP_lastModified,
        'GDPR Data Processing note': FP_gdprDataProc,
        'GDPR Data Processing note modifiedby': FP_gdprDataProcModifiedBy,
        'Business Description': FP_businessDescription,
        'Business Description modifiedBy': FP_businessDescriptionModifiedBy,
        'Resource Type': FP_resourceType,
        'description': FP_Description,
        'Resource Name': FP_resourceName
    })

# Function generating FilesFile attributs
def genFilesFileNameCSV(FilesFileNameRes, resourceName):
    FF_lastModified = ''
    FF_LoadingMode = ''
    FF_Notes = ''
    FF_DataHistoricization = ''
    FF_Frequency = ''
    FF_FeedingType = ''
    FF_Transformation = ''
    FF_gdprDataProc = ''
    FF_gdprDataProcmodifiedBy = ''
    FF_DataQualityLink = ''
    FF_DataQualityLinkModifiedBy = ''
    FF_businessDescription = ''
    FF_businessDescriptionModifiedBy = ''
    FF_resourceName = ''
    FF_name = ''
    FF_Description = ''
    FF_idRes = ''
    acronym = ''
    FF_Id = FilesFileNameRes['id']

    #print("DEBUG id --", FF_Id)
    FFNfacts = FilesFileNameRes['facts']
    for val in FFNfacts:
        if val.get('attributeId') == 'core.lastModified':
            FF_lastModified = val.get(
                'value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.LoadingMode':
            FF_LoadingMode = val.get(
                'value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.Notes':
            FF_Notes = val.get(
                'value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.DataHistoricization':
            FF_DataHistoricization = val.get(
                'value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.Frequency':
            FF_Frequency = val.get(
                'value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.Feeding':
            FF_FeedingType = val.get(
                'value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.Transformation':
            FF_Transformation = val.get(
                'value')
        if val.get('label') == 'GDPR Data Processing note':
            FF_gdprDataProc = val.get(
                'value')
        if val.get('label') == 'GDPR Data Processing note':
            FF_gdprDataProcmodifiedBy = val.get('modifiedBy')

        if val.get('label') == 'Data Quality Link':
            FF_DataQualityLink = val.get(
                'value')
        if val.get('label') == 'Data Quality Link':
            FF_DataQualityLinkModifiedBy = val.get(
                'modifiedBy')
        if val.get(
                'label') == 'Business Description':
            FF_businessDescription = val.get('value')
        if val.get('label') == 'Business Description':
            FF_businessDescriptionModifiedBy = val.get(
                'modifiedBy')
        if val.get('attributeId') == 'core.resourceName':
            FF_resourceName = val.get(
                'value')
        if val.get('attributeId') == 'core.name':
            FF_name = val.get('value')
        if val.get('attributeId') == 'core.description':
            FF_Description = val.get(
                'value')        
        if val.get('label') == 'Acronym':
            acronym = val.get('value')

    FFN_srcLinks = FilesFileNameRes.get('srcLinks')
    for scr in FFN_srcLinks:
        if scr.get(
                'classType') == 'DataFile.Custom.Upload.FilesPath':
            FF_idRes = scr.get('id')

    #if FF_lastModified < Last_Run_read[resourceName]:
        #pass
    #else:
            csvFilesFileName_data.append({
                 'id': FF_Id,
                 'Last Modified': FF_lastModified,
                 'Loading Mode': FF_LoadingMode,
                 'Notes': FF_Notes,
                 'Data Historicization': FF_DataHistoricization,
                 'Frequency': FF_Frequency,
                 'Feeding': FF_FeedingType,
                 'Transformation': FF_Transformation,
                 'GDPR Data Processing note': FF_gdprDataProc,
                 'GDPR Data Processing note modifiedBy': FF_gdprDataProcmodifiedBy,
                 'Data Quality Link': FF_DataQualityLink,
                 'Data Quality Link modifiedBy': FF_DataQualityLinkModifiedBy,
                 'Business Description': FF_businessDescription,
                 'Business Description modifiedBy': FF_businessDescriptionModifiedBy,
                 'Resource Name': FF_resourceName,
                 'Name': FF_name,
                 'description': FF_Description,
                 'path id': FF_idRes,
                 'Acronym': acronym
                 })

# Function generating FilesColumn attributs
def genFilesColumnCSV(FilesColumnNameRes, resourceName):

    FC_name = ''
    FC_lastModified = ''
    FC_FieldPrimaryKey = ''
    FC_FieldOffset = ''
    FC_FieldODBCFormat = ''
    FC_FieldMandatory = ''
    FC_Notes = ''
    FC_Algorithm = ''
    FC_FieldUniqueIndex = ''
    FC_FieldPosition = ''
    FC_RecordType = ''
    FC_FieldLength = ''
    FC_DataFlowType = ''
    FC_FieldDomainTable = ''
    FC_Function = ''
    FC_FieldDataFormat = ''
    FC_FieldDecimals = ''
    FC_KeyDataElement = ''
    FC_KeyDataElementModifiedBy = ''
    FC_gdprDataProc = ''
    FC_gdprDataProcmodifiedBy = ''
    FC_DataQualityLink = ''
    FC_DataQualityLinkModifiedBy = ''
    FC_AssetClassification = ''
    FC_AssetClassificationModifiedBy = ''
    FC_businessDescription = ''
    FC_businessDescriptionModifiedBy = ''
    FC_resourceName = ''
    FC_description = ''
    FC_IdScr = ''

    FC_Id = FilesColumnNameRes['id']

    #print("DEBUG id --", FC_Id)
    facetsTb = FilesColumnNameRes['facts']
    for val in facetsTb:
        if val.get('attributeId') == 'core.name':
            FC_name = val.get('value')
        if val.get('attributeId') == 'core.lastModified':
            FC_lastModified = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.FieldPrimaryKey':
            FC_FieldPrimaryKey = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.FieldOffset':
            FC_FieldOffset = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.FieldODBCFormat':
            FC_FieldODBCFormat = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.FieldMandatory':
            FC_FieldMandatory = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.Notes':
            FC_Notes = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.Algorithm':
            FC_Algorithm = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.FieldUniqueIndex':
            FC_FieldUniqueIndex = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.FieldPosition':
            FC_FieldPosition = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.RecordType':
            FC_RecordType = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.FieldLength':
            FC_FieldLength = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.DataFlowType':
            FC_DataFlowType = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.FieldDomainTable':
            FC_FieldDomainTable = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.Function':
            FC_Function = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.FieldDataFormat':
            FC_FieldDataFormat = val.get('value')
        if val.get('attributeId') == 'DataFile.Custom.Upload.FieldDecimals':
            FC_FieldDecimals = val.get('value')
        if val.get('label') == 'Key Data Element':
            FC_KeyDataElement = val.get('value')
        if val.get('label') == 'Key Data Element':
            FC_KeyDataElementModifiedBy = val.get('modifiedBy')
        if val.get('label') == 'GDPR Data Processing note':
            FC_gdprDataProc = val.get('value')
        if val.get('label') == 'GDPR Data Processing note':
            FC_gdprDataProcmodifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Data Quality Link':
            FC_DataQualityLink = val.get('value')
        if val.get('label') == 'Data Quality Link':
            FC_DataQualityLinkModifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Asset Classification':
            FC_AssetClassification = val.get('value')
        if val.get('label') == 'Asset Classification':
            FC_AssetClassificationModifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Business Description':
            FC_businessDescription = val.get('value')
        if val.get('label') == 'Business Description':
            FC_businessDescriptionModifiedBy = val.get('modifiedBy')
        if val.get('attributeId') == 'core.resourceName':
            FC_resourceName = val.get('value')
        if val.get('attributeId') == 'core.description':
            FC_description = val.get('value')

    FFN_srcLinks = FilesColumnNameRes.get('srcLinks')
    for scr in FFN_srcLinks:

        if scr.get(
                'classType') == 'DataFile.Custom.Upload.FilesFileName':
            FC_IdScr = scr.get('id')
    #print(f"FC_lastModified:{FC_lastModified}")
    #print(f"Last_Run_read[resourceName]:{Last_Run_read[resourceName]}")
    #if FC_lastModified < Last_Run_read[resourceName]:
        #pass
    #else:
            csvFilesColumn_data.append({
                 'id': FC_Id,
                 'name': FC_name,
                 'Last Modified': FC_lastModified,
                 'Field Primary Key': FC_FieldPrimaryKey,
                 'Field Offset': FC_FieldOffset,
                 'Field ODBC Format': FC_FieldODBCFormat,
                 'Field Mandatory': FC_FieldMandatory,
                 'Notes': FC_Notes,
                 'Algorithm': FC_Algorithm,
                 'Field Unique Index': FC_FieldUniqueIndex,
                 'Field Position': FC_FieldPosition,
                 'Record Type': FC_RecordType,
                 'Field Length': FC_FieldLength,
                 'Data Flow Type': FC_DataFlowType,
                 'Field Domain Table': FC_FieldDomainTable,
                 'Function': FC_Function,
                 'Field Data Format': FC_FieldDataFormat,
                 'Field Decimals': FC_FieldDecimals,
                 'Key Data Element': FC_KeyDataElement,
                 'Key Data Element modifiedBy': FC_KeyDataElementModifiedBy,
                 'GDPR Data Processing note': FC_gdprDataProc,
                 'GDPR Data Processing note modifiedBy': FC_gdprDataProcmodifiedBy,
                 'Data Quality Link': FC_DataQualityLink,
                 'Data Quality Link modifiedBy': FC_DataQualityLinkModifiedBy,
                 'Asset Classification': FC_AssetClassification,
                 'Asset Classification modifiedBy': FC_AssetClassificationModifiedBy,
                 'Business Description': FC_businessDescription,
                 'Business Description modifiedBy': FC_businessDescriptionModifiedBy,
                 'Resource Name': FC_resourceName,
                 'description': FC_description,
                 'File id': FC_IdScr
                  })  


def mainDatafileExtra():
    try:
        return datafileResourcesExtra()
    except Exception as e:
        return e
