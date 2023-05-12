from props.utils import os, pd, requests, HTTPAdapter, json, datetime, BeautifulSoup, Retry, parser, logging
from props.paramsEdc import EDC_URL_REST_1_RELATIONAL, EDC_URL_REST_2, EDC_headers, EDC_Auth, pageSize, EDC_URL, chars_to_remove, val_DGR
from .EmptyCsvRdbmsToExport import csvDatabaseEmpty, csvSchemaEmpty, csvTableEmpty, csvColumnEmpty
from db.database import all_edc


session = requests.Session()
retry = Retry(total=5,
              backoff_factor=1,
              status_forcelist=[500, 502, 503, 504])
# retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# empty array

csvDatabase_data = []
csvSchema_data = []
csvTable_data = []
csvColumn_data = []
Last_Run_read = {}
Last_Run_write = {}
resourceName = None

# Opening JSON file
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'full_last_time_run.json')
with open(file_path, 'r') as f:
    # a dictionary
    Last_Run_read = json.load(f)


# Function get RDBMS resources, do pagination and generate csv to export
def rdbmsResourcesFile():
    downloaded = 0
    if not os.path.exists('EDC'):
        os.makedirs('EDC')
    pageSeizeOffset = pageSize
    resp1 = session.get(EDC_URL_REST_1_RELATIONAL,
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
        hits = j_resp_1req.get('hits')
        totalPage = j_resp_1req['metadata']['totalCount']
        newTotal = totalPage + pageSize

        generateCSV(hits, EDC_headers, EDC_Auth)
        # New - 14Sept2022
        pageSeizeOffset = pageSize
        if newTotal > pageSeizeOffset:
            while totalPage > pageSeizeOffset:
                # print("Pagination RDBMS RESOURCES: Offset items: -- ",
                #       pageSeizeOffset)

                offsetUrl = '/2/catalog/data/search?basicQuery=*&tabId=tab.resources&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22JDBC%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Teradata%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Hive%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22IBM%5C%20DB2%5C%20for%5C%20z%5C%2FOS%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Oracle%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Azure%5C%20Microsoft%5C%20SQL%5C%20Server%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Microsoft%20SQL%20Server%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.Resource%22&fq=' + val_DGR + '&facet=false&defaultFacets=true&highlight=false&offset='+str(pageSeizeOffset)+'&pageSize=' +str(pageSize)+'&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'
                
                newUrlMain = EDC_URL + offsetUrl

                respWhile = requests.get(
                    newUrlMain, headers=EDC_headers, auth=EDC_Auth, verify=False)

                if respWhile.status_code == 200:
                    respWhileData = respWhile.json()
                    hits = respWhileData.get('hits')

                    generateCSV(hits, EDC_headers, EDC_Auth)

                else:
                    logging.error(f"Error pagination on offset: {pageSeizeOffset}")

                pageSeizeOffset += pageSize

        # Generate csv files csvDatabase
        if csvDatabase_data:
            # print("csvDatabase_data: " + csvDatabase_data)
            df = pd.DataFrame(csvDatabase_data)
            df = df.fillna('')
            for column in df.columns:
                df[column] = df[column].apply(
                    lambda x: BeautifulSoup(x, 'lxml').get_text())
                for i in chars_to_remove:
                    df = df.applymap(lambda x: x.replace(
                        i, '') if (isinstance(x, str)) else x)
            #print('df RDBMS_DATABASES ....', df.head())
            df.to_csv(os.path.join(
                'EDC/RDBMS_DATABASES.csv'), sep=";", index=False)
            downloaded = downloaded + 1
        else:
            df = pd.DataFrame(csvDatabaseEmpty)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join(
                'EDC/RDBMS_DATABASES.csv'), sep=";", index=False, header=True)

        # Generate csv files csvSchema
        if csvSchema_data:
            # print("csvSchema_data: " + csvSchema_data)
            df = pd.DataFrame(csvSchema_data)
            df = df.fillna('')
            for column in df.columns:
                df[column] = df[column].apply(
                    lambda x: BeautifulSoup(x, 'lxml').get_text())
                for i in chars_to_remove:
                    df = df.applymap(lambda x: x.replace(
                        i, '') if (isinstance(x, str)) else x)
            #print('df RDBMS_SCHEMA ....', df.head())
            df.to_csv(os.path.join(
                'EDC/RDBMS_SCHEMA.csv'), sep=";", index=False)
            downloaded = downloaded + 1
        else:
            df = pd.DataFrame(csvSchemaEmpty)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join(
                'EDC/RDBMS_SCHEMA.csv'), sep=";", index=False, header=True)

        # Generate csv files csvTable
        if csvTable_data:
            #print("csvTable_data: " + csvTable_data)
            df = pd.DataFrame(csvTable_data)
            df = df.fillna('')
            for column in df.columns:
                df[column] = df[column].apply(
                    lambda x: BeautifulSoup(x, 'lxml').get_text())
                for i in chars_to_remove:
                    df = df.applymap(lambda x: x.replace(
                        i, '') if (isinstance(x, str)) else x)
            #print('df RDBMS_TABLE VIEWS ....', df.head())
            df.to_csv(os.path.join(
                'EDC/RDBMS_TABLE VIEWS.csv'), sep=";", index=False)
            downloaded = downloaded + 1
        else:
            df = pd.DataFrame(csvTableEmpty)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join(
                'EDC/RDBMS_TABLE VIEWS.csv'), sep=";", index=False, header=True)
 
        # Generate csv files csvColumn
        if csvColumn_data:
            #print("csvColumn_data: " + csvColumn_data)
            df = pd.DataFrame(csvColumn_data)
            df = df.fillna('')
            for column in df.columns:
                df[column] = df[column].apply(
                    lambda x: BeautifulSoup(x, 'lxml').get_text())
                for i in chars_to_remove:
                    df = df.applymap(lambda x: x.replace(
                        i, '') if (isinstance(x, str)) else x)
            #print('df RDBMS_COLUMNS ....', df.head())
            df.to_csv(os.path.join(
                'EDC/RDBMS_COLUMNS.csv'), sep=";", index=False)
            downloaded = downloaded + 1
        else:
            df = pd.DataFrame(csvColumnEmpty)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join(
                'EDC/RDBMS_COLUMNS.csv'), sep=";", index=False, header=True)

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'full_last_time_run.json')
        with open(file_path, 'w') as outfile:
            json.dump(Last_Run_write, outfile)
    else:
        logging.error(f"Main EDC Failed with status code: {str(resp1.status_code)}")

    ending_time = datetime.now()  # execution script code time
    resourceName = 'Rdbms'
    resourceType = 'Standard'
    # db data to be saved
    all_edc(resourceName, resourceType, downloaded, response_code,
            response_size, response_time, starting_time, ending_time)

    return downloaded


# Function which make the pagination on offset and verify updates of the resources
def generateCSV(hits, EDC_headers, EDC_Auth):
    resourceName = None

    pageSeizeOffset = pageSize
    for val_hits in hits:
        values_hits = val_hits.get('values')
        newResourceFailed = 0
        lastScanStatus = 'NONE'
        lastScanDate = ''

        for val_values in values_hits:
            if val_values.get('attributeId') == 'core.resourceName':
                resourceName = val_values.get('value')
            if val_values.get('attributeId') == 'core.lastScanStatus':
                lastScanStatus = val_values.get('value')
            if val_values.get('attributeId') == 'core.lastScanDate':
                lastScanDate = val_values.get('value')
                lastScanDate = lastScanDate[0:19]

        if not Last_Run_read.get(resourceName):
            lastRun = '1900-01-01T00:00:00'

            if lastScanStatus != 'SUCCESS':
                # print('Last Scan Status Failed ...')
                logging.warning(f"NEW resource  {resourceName} has status not equal to SUCCESS!")
                newResourceFailed = 1
                pass
            else:
                logging.info(f"Found NEW resource! Working on {resourceName}")
                singleURL = EDC_URL_REST_2 + '/2/catalog/data/search?basicQuery=*&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Database%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Schema%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Table%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.View%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Column%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.ViewColumn%22&fq=%7B!tag%3Dresource_name%7Dcore.resourceName%3A%22' + \
                    resourceName + '%22&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize=' + \
                    str(pageSize) + \
                    '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'
                    
                    
                resp2 = requests.get(
                    singleURL, headers=EDC_headers, auth=EDC_Auth, verify=False)
                # print('Response Code: ', resp2.status_code)

                if resp2.status_code == 200:
                    j_resp_2req = resp2.json()
                    totalCount = j_resp_2req['metadata']['totalCount']
                    newTotal = totalCount + pageSize
                    hits = j_resp_2req.get('hits')
                    genAllRdbmsCSVs(hits, EDC_headers, EDC_Auth)
                    
                    # New - 14Sept2022
                    pageSeizeOffset = pageSize
                    if newTotal > pageSeizeOffset:
                        while totalCount > pageSeizeOffset:
                            # print("Pagination ALL RDBMS: Offset items: -- ",
                                #   pageSeizeOffset)
                            logging.info(f"Working on {resourceName} [{pageSeizeOffset} of {totalCount}]")
                            offsetUrl = '/access/2/catalog/data/search?basicQuery=*&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Database%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Schema%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Table%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.View%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Column%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.ViewColumn%22&fq=%7B!tag%3Dresource_name%7Dcore.resourceName%3A%22' + \
                                resourceName+'%22&facet=false&defaultFacets=true&highlight=false&offset=' + \
                                str(pageSeizeOffset)+'&pageSize='+str(pageSize) + \
                                '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'
                            
                            newUrlMain = EDC_URL + offsetUrl

                            newResp = requests.get(
                                newUrlMain, headers=EDC_headers, auth=EDC_Auth, verify=False)

                            if newResp.status_code == 200:
                                newrespeData = newResp.json()
                                hits = newrespeData.get('hits')

                                if lastScanStatus != 'SUCCESS':
                                    logging.warning(f"NEW resource  {resourceName} has status not equal to SUCCESS!")
                                    newResourceFailed = 1
                                    pass
                                else:
                                    genAllRdbmsCSVs(hits, EDC_headers, EDC_Auth)
                            else:
                                logging.error(f"Error rdbms pagination on offset: {pageSeizeOffset}")

                            pageSeizeOffset += pageSize

                else:
                    logging.error("Error generating single resource.")
        else:
            logging.info(f"Working on {resourceName}")
            lastRun = Last_Run_read.get(resourceName)
            fromDate = parser.parse(lastScanDate)
            toDate = parser.parse(lastRun)
            
            if fromDate < toDate: 
                pass
            else:
                if lastScanStatus != 'SUCCESS':
                    logging.error("Last scan status failed...")
                    pass
                else:
                    
                    singleURL = EDC_URL_REST_2 + '/2/catalog/data/search?basicQuery=*&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Schema%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Database%22&fq=%7B!tag%3Dresource_name%7Dcore.resourceName%3A%22' + \
                        resourceName + '%22&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize=' + \
                        str(pageSize) + \
                        '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'
                    resp2 = requests.get(
                        singleURL, headers=EDC_headers, auth=EDC_Auth, verify=False)

                    if resp2.status_code == 200:
                        j_resp_2req = resp2.json()
                        totalCount = j_resp_2req['metadata']['totalCount']
                        newTotal = totalCount + pageSize
                        hits = j_resp_2req.get('hits')

                        genAllRdbmsCSVs(hits, EDC_headers, EDC_Auth)

                        # New - 14Sept2022
                        pageSeizeOffset = pageSize
                        if newTotal > pageSeizeOffset:
                            while totalCount > pageSeizeOffset:
                                # print("Pagination ALL RDBMS: Offset items: -- ",
                                #       pageSeizeOffset)
                                logging.info(f"Working on {resourceName} [{pageSeizeOffset} of {totalCount}]")
                                offsetUrl = '/access/2/catalog/data/search?basicQuery=*&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Schema%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Database%22&fq=%7B!tag%3Dresource_name%7Dcore.resourceName%3A%22' + \
                                    resourceName+'%22&facet=false&defaultFacets=true&highlight=false&offset=' + \
                                    str(pageSeizeOffset)+'&pageSize='+str(pageSize) + \
                                    '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'
                                newUrlMain = EDC_URL + offsetUrl

                                newResp = requests.get(
                                    newUrlMain, headers=EDC_headers, auth=EDC_Auth, verify=False)
                                if newResp.status_code == 200:
                                    newrespeData = newResp.json()
                                    hits = newrespeData.get('hits')

                                    if lastScanStatus != 'SUCCESS':
                                        logging.error("Last scan status failed...")
                                        pass
                                    else:
                                        genAllRdbmsCSVs(hits, EDC_headers, EDC_Auth)
                                else:
                                    logging.error(f"Error rdbms pagination on offset: {pageSeizeOffset}")
                                pageSeizeOffset += pageSize

                    else:
                        logging.error("Error generating single resource.")
        # update timestamp for each resource
        if newResourceFailed == 0 :
           Last_Run_write[resourceName] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
       

# Function get data and return json data
def genAllRdbmsCSVs(hits, EDC_headers, EDC_Auth):
    # print('hits: ', hits)
    for val in hits:
        if not val in hits:
            pass
        else:
            valHref = val['href']
            valHits = val['values']
            for v in valHits:
                if v['attributeId'] == 'core.classType' and v['value'] == 'com.infa.ldm.relational.Database':
                    databaseURL = EDC_URL_REST_2 + valHref
                    # print('URL Database standard: ', databaseURL)
                    databaseReq = session.get(
                        databaseURL, headers=EDC_headers, auth=EDC_Auth, verify=False)
                    # handle other errors
                    if databaseReq.status_code == 200:
                        if not databaseReq.content:
                            pass
                        else:
                            databaseRes = databaseReq.json()
                            genDatabaseCSV(databaseRes)

                if v['attributeId'] == 'core.classType' and v['value'] == 'com.infa.ldm.relational.Schema':
                    schemaURL = EDC_URL_REST_2 + valHref
                    # print('URL Schema standard: ', schemaURL)
                    schemaReq = session.get(
                        schemaURL, headers=EDC_headers, auth=EDC_Auth, verify=False)

                    if schemaReq.status_code == 200:
                        if not schemaReq.content:
                            pass
                        else:
                            schemaRes = schemaReq.json()
                            genSchemaCSV(schemaRes)
                
                if (v['attributeId'] == 'core.classType' and v['value'] == 'com.infa.ldm.relational.Table') or (v['attributeId'] == 'core.classType' and v['value'] == 'com.infa.ldm.relational.View'):
                    tableURL = EDC_URL_REST_2 + valHref
                    # print('URL Table standard: ', tableURL)
                    tableReq = session.get(
                        tableURL, headers=EDC_headers, auth=EDC_Auth, verify=False)
                    # handle other errors
                    if tableReq.status_code == 200:
                        if not tableReq.content:
                            pass
                        else:
                            tableRes = tableReq.json()
                            genTableCSV(tableRes)
                
                if (v['attributeId'] == 'core.classType' and v['value'] == 'com.infa.ldm.relational.Column') or (v['attributeId'] == 'core.classType' and v['value'] == 'com.infa.ldm.relational.ViewColumn'):
                    columnURL = EDC_URL_REST_2 + valHref
                    # print('Column URL: ', columnURL)
                    columReq = session.get(
                        columnURL, headers=EDC_headers, auth=EDC_Auth)
                    # handle other errors
                    if columReq.status_code == 200:
                        if not columReq.content:
                            pass
                        else:
                            columnRes = columReq.json()
                            genColumnCSV(columnRes)

# Function generating Database attributs
def genDatabaseCSV(databaseRes):
    DB_childId = ''
    DB_name = ''
    DB_lastModified = ''
    DB_gdprDataProc = ''
    DB_gdprDataProcModifiedBy = ''
    DB_architecturalLevel = ''
    DB_architecturalLevelModifiedBy = ''
    DB_businessDescription = ''
    DB_businessDescriptionModifiedBy = ''
    DB_systemCase = ''
    DB_systemType = ''
    DB_SystemMinorVersion = ''
    DB_StoreType = ''
    DB_SystemReleaseVersion = ''
    DB_SystemMajorVersion = ''
    DB_resourceName = ''
    DB_resourceType = ''
    DB_childId = databaseRes['id']
    facetsDb = databaseRes['facts']
    for val in facetsDb:
        if val.get('attributeId') == 'core.name':
            DB_name = val.get('value')
        if val.get('attributeId') == 'core.lastModified':
            DB_lastModified = val.get('value')
        if val.get('label') == 'GDPR Data Processing note':
            DB_gdprDataProc = val.get('value')
        if val.get('label') == 'GDPR Data Processing note':
            DB_gdprDataProcModifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Architectural Level':
            DB_architecturalLevel = val.get('value')
        if val.get('label') == 'Architectural Level':
            DB_architecturalLevelModifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Business Description':
            DB_businessDescription = val.get('value')
        if val.get('label') == 'Business Description':
            DB_businessDescriptionModifiedBy = val.get('modifiedBy')
        if val.get('attributeId') == 'com.infa.ldm.relational.SystemCase':
            DB_systemCase = val.get('value')
        if val.get('attributeId') == 'com.infa.ldm.relational.SystemType':
            DB_systemType = val.get('value')
        if val.get('attributeId') == 'com.infa.ldm.relational.SystemMinorVersion':
            DB_SystemMinorVersion = val.get('value')
        if val.get('attributeId') == 'com.infa.ldm.relational.StoreType':
            DB_StoreType = val.get('value')
        if val.get('attributeId') == 'com.infa.ldm.relational.SystemReleaseVersion':
            DB_SystemReleaseVersion = val.get('value')
        if val.get('attributeId') == 'com.infa.ldm.relational.SystemMajorVersion':
            DB_SystemMajorVersion = val.get('value')
        if val.get('attributeId') == 'core.resourceName':
            DB_resourceName = val.get('value')
        if val.get('attributeId') == 'core.resourceType':
            DB_resourceType = val.get('value')

    csvDatabase_data.append({
        'id': DB_childId,
        'name': DB_name,
        'Last Modified': DB_lastModified,
        'GDPR Data Processing note': DB_gdprDataProc,
        'GDPR Data Processing note modifiedby': DB_gdprDataProcModifiedBy,
        'Architectural Level': DB_architecturalLevel,
        'Architectural Level modifiedBy': DB_architecturalLevelModifiedBy,
        'Business Description': DB_businessDescription,
        'Business Description modifiedBy': DB_businessDescriptionModifiedBy,
        'System Case': DB_systemCase,
        'System Type': DB_systemType,
        'System Minor Version': DB_SystemMinorVersion,
        'Store Type': DB_StoreType,
        'System Release Version': DB_SystemReleaseVersion,
        'System Major Version': DB_SystemMajorVersion,
        'Resource Type': DB_resourceType,
        'Resource Name': DB_resourceName
        })
    logging.info(f"Resource Name: {DB_resourceName}")

# Function generating Schema attributs
def genSchemaCSV(schemaRes):
    SCH_childId = ''
    SCH_lastModified = ''
    SCH_name = ''
    SCH_gdprDataProc = ''
    SCH_gdprDataProcmodifiedBy = ''
    SCH_architecturalLevel = ''
    SCH_architecturalLevelModifiedBy = ''
    SCH_businessDescription = ''
    SCH_businessDescriptionModifiedBy = ''
    SCH_resourceName = ''
    SCH_DatabaseId = ''

    SCH_childId = schemaRes['id']
    factsSCH = schemaRes['facts']
    for val in factsSCH:
        if val.get('attributeId') == 'core.name':
            SCH_name = val.get('value')
        if val.get('attributeId') == 'core.lastModified':
            SCH_lastModified = val.get('value')
        if val.get('label') == 'GDPR Data Processing note':
            SCH_gdprDataProc = val.get('value')
        if val.get('label') == 'GDPR Data Processing note':
            SCH_gdprDataProcmodifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Architectural Level':
            SCH_architecturalLevel = val.get('value')
        if val.get('label') == 'Architectural Level':
            SCH_architecturalLevelModifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Business Description':
            SCH_businessDescription = val.get('value')
        if val.get('label') == 'Business Description':
            SCH_businessDescriptionModifiedBy = val.get('modifiedBy')
        if val.get('attributeId') == 'core.resourceName':
            SCH_resourceName = val.get('value')

    schemasrcLinks = schemaRes['srcLinks']
    for valScr in schemasrcLinks:
        if valScr.get('classType') == 'com.infa.ldm.relational.Database':
            SCH_DatabaseId = valScr.get('id')

    csvSchema_data.append({
        'id': SCH_childId,
        'Last Modified': SCH_lastModified,
        'name': SCH_name,
        'GDPR Data Processing note': SCH_gdprDataProc,
        'GDPR Data Processing note modifiedBy': SCH_gdprDataProcmodifiedBy,
        'Architectural Level': SCH_architecturalLevel,
        'Architectural Level modifiedBy': SCH_architecturalLevelModifiedBy,
        'Business Description': SCH_businessDescription,
        'Business Description modifiedBy': SCH_businessDescriptionModifiedBy,
        'Resource Name': SCH_resourceName,
        'Database id': SCH_DatabaseId
    })
    # print('csvSchema_data..........', csvSchema_data)

# Function generating Table View attributs
def genTableCSV(tableRes):
    Tb_childId = ''
    Tb_lastModified = ''
    Tb_gdprDataProc = ''
    Tb_gdprDataProcmodifiedBy = ''
    Tb_DataQualityLink = ''
    Tb_DataQualityLinkModifiedBy = ''
    Tb_businessDescription = ''
    Tb_businessDescriptionModifiedBy = ''
    Tb_NativeType = ''
    Tb_resourceName = ''
    Tb_name = ''
    Tb_SchemaId = ''

    Tb_childId = tableRes['id']
    facetsTb = tableRes['facts']
    for val in facetsTb:
        if val.get('attributeId') == 'core.lastModified':
            Tb_lastModified = val.get('value')
        if val.get('label') == 'GDPR Data Processing note':
            Tb_gdprDataProc = val.get('value')
        if val.get('label') == 'GDPR Data Processing note':
            Tb_gdprDataProcmodifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Data Quality Link':
            Tb_DataQualityLink = val.get('value')
        if val.get('label') == 'Data Quality Link':
            Tb_DataQualityLinkModifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Business Description':
            Tb_businessDescription = val.get('value')
        if val.get('label') == 'Business Description':
            Tb_businessDescriptionModifiedBy = val.get('modifiedBy')
        if val.get('attributeId') == 'com.infa.ldm.relational.NativeType':
            Tb_NativeType = val.get('value')
        if val.get('attributeId') == 'core.resourceName':
            Tb_resourceName = val.get('value')
        if val.get('attributeId') == 'core.name':
            Tb_name = val.get('value')

    tablesrcLinks = tableRes['srcLinks']
    for valScr in tablesrcLinks:
        if valScr.get('classType') == 'com.infa.ldm.relational.Schema':
            Tb_SchemaId = valScr.get('id')

    csvTable_data.append({
        'id': Tb_childId,
        'Last Modified': Tb_lastModified,
        'GDPR Data Processing note': Tb_gdprDataProc,
        'GDPR Data Processing note modifiedBy': Tb_gdprDataProcmodifiedBy,
        'Data Quality Link': Tb_DataQualityLink,
        'Data Quality Link modifiedBy': Tb_DataQualityLinkModifiedBy,
        'Business Description': Tb_businessDescription,
        'Business Description modifiedBy': Tb_businessDescriptionModifiedBy,
        'Native Type': Tb_NativeType,
        'Resource Name': Tb_resourceName,
        'Name': Tb_name,
        'Schema id': Tb_SchemaId
    })
    # print('csvTable_data..........', csvTable_data)

# Function generating Columns attributs
def genColumnCSV(columnRes):
    Cl_childId = ''
    Cl_name = ''
    Cl_lastModified = ''
    Cl_KeyDataElement = ''
    Cl_KeyDataElementModifiedBy = ''
    Cl_gdprDataProc = ''
    Cl_gdprDataProcmodifiedBy = ''
    Cl_DataQualityLink = ''
    Cl_DataQualityLinkModifiedBy = ''
    Cl_AssetClassification = ''
    Cl_AssetClassificationModifiedBy = ''
    Cl_businessDescription = ''
    Cl_businessDescriptionModifiedBy = ''
    Cl_DatatypeScale = ''
    Cl_Position = ''
    Cl_Identity = ''
    Cl_NativeType = ''
    Cl_PrimaryKeyColumn = ''
    Cl_Nullable = ''
    Cl_DatatypeLength = ''
    Cl_Datatype = ''
    Cl_resourceName = ''
    Cl_finalId = ''

    factsCols = columnRes['facts']
    Cl_childId = columnRes['id']
    for val in factsCols:
        if val.get('attributeId') == 'core.name':
            Cl_name = val.get('value')
        if val.get('attributeId') == 'core.lastModified':
            Cl_lastModified = val.get('value')
        if val.get('label') == 'Key Data Element':
            Cl_KeyDataElement = val.get('value')
        if val.get('label') == 'Key Data Element':
            Cl_KeyDataElementModifiedBy = val.get('modifiedBy')
        if val.get('label') == 'GDPR Data Processing note':
            Cl_gdprDataProc = val.get('value')
        if val.get('label') == 'GDPR Data Processing note':
            Cl_gdprDataProcmodifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Data Quality Link':
            Cl_DataQualityLink = val.get('value')
        if val.get('label') == 'Data Quality Link':
            Cl_DataQualityLinkModifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Asset Classification':
            Cl_AssetClassification = val.get('value')
        if val.get('label') == 'Asset Classification':
            Cl_AssetClassificationModifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Business Description':
            Cl_businessDescription = val.get('value')
        if val.get('label') == 'Business Description':
            Cl_businessDescriptionModifiedBy = val.get('modifiedBy')
        if val.get('attributeId') == 'com.infa.ldm.relational.DatatypeScale':
            Cl_DatatypeScale = val.get('value')
        if val.get('attributeId') == 'com.infa.ldm.relational.Position':
            Cl_Position = val.get('value')
        if val.get('attributeId') == 'com.infa.ldm.relational.Identity':
            Cl_Identity = val.get('value')
        if val.get('attributeId') == 'com.infa.ldm.relational.NativeType':
            Cl_NativeType = val.get('value')
        if val.get('attributeId') == 'com.infa.ldm.relational.PrimaryKeyColumn':
            Cl_PrimaryKeyColumn = val.get('value')
        if val.get('attributeId') == 'com.infa.ldm.relational.Nullable':
            Cl_Nullable = val.get('value')
        if val.get('attributeId') == 'com.infa.ldm.relational.DatatypeLength':
            Cl_DatatypeLength = val.get('value')
        if val.get('attributeId') == 'com.infa.ldm.relational.Datatype':
            Cl_Datatype = val.get('value')
        if val.get('attributeId') == 'core.resourceName':
            Cl_resourceName = val.get('value')

    tablesrcLinks = columnRes['srcLinks']
    for valScr in tablesrcLinks:
        if valScr.get('classType') == 'com.infa.ldm.relational.Table' or valScr.get('classType') == 'com.infa.ldm.relational.View':
            Cl_finalId = valScr.get('id')

    csvColumn_data.append({
        'id': Cl_childId,
        'name': Cl_name,
        'Last Modified': Cl_lastModified,
        'Key Data Element': Cl_KeyDataElement,
        'Key Data Element modifiedBy': Cl_KeyDataElementModifiedBy,
        'GDPR Data Processing note': Cl_gdprDataProc,
        'GDPR Data Processing note modifiedBy': Cl_gdprDataProcmodifiedBy,
        'Data Quality Link': Cl_DataQualityLink,
        'Data Quality Link modifiedBy': Cl_DataQualityLinkModifiedBy,
        'Asset Classification': Cl_AssetClassification,
        'Asset Classification modifiedBy': Cl_AssetClassificationModifiedBy,
        'Business Description': Cl_businessDescription,
        'Business Description modifiedBy': Cl_businessDescriptionModifiedBy,
        'Datatype Scale': Cl_DatatypeScale,
        'Position': Cl_Position,
        'Identity': Cl_Identity,
        'Native Type': Cl_NativeType,
        'Primary Key Column': Cl_PrimaryKeyColumn,
        'Nullable': Cl_Nullable,
        'Datatype Length': Cl_DatatypeLength,
        'Datatype': Cl_Datatype,
        'Resource Name': Cl_resourceName,
        'TableView id': Cl_finalId
    })
    # print('csvColumn_data..........', csvColumn_data)


def mainRdbmsResourcesFile():
    try:
        return rdbmsResourcesFile()
    except Exception as e:
        return e
