from sre_constants import SUCCESS
from props.utils import os, pd, requests, HTTPAdapter, BeautifulSoup, json, datetime, Retry, logging
from props.paramsEdc import EDC_URL_REST_1_REFERENCE, EDC_URL_REST_2, EDC_headers, EDC_Auth, pageSize, EDC_URL, chars_to_remove, val_DGR
from .EmptyCsvReferenceToExport import csvDatasourceEmpty, csvDatasetEmpty, csvDataElementEmpty
from db.database import all_edc

session = requests.Session()
retry = Retry(total=5,
              backoff_factor=1,
              status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# empty array
csvDataElement_data = []
csvDataset_data  = []
csvDatasource_data  = []

# post api with raw data & get response and add to csv
# Function get RDBMS resources, do pagination and generate csv to export
def genReferencesFile():
    downloaded = 0

    if not os.path.exists('EDC'):
        os.makedirs('EDC')

    # print("Generating REFERENCE RESOURCES ....")
    pageSeizeOffset = pageSize
    resp1 = requests.get(EDC_URL_REST_1_REFERENCE,
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

        if newTotal > pageSeizeOffset:
            while totalPage > pageSeizeOffset:
                logging.debug(f"Pagination REFERENCE RESOURCES: Offset items: {pageSeizeOffset}")

                offsetUrl = '/access/2/catalog/data/search?basicQuery=*&tabId=tab.resources&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Reference%5C%20resource%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.Resource%22&fq='\
                    + val_DGR +'&facet=false&defaultFacets=true&highlight=false&offset='+str(pageSeizeOffset)+'&pageSize=' + \
                    str(pageSize) + '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'
                    
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
                downloaded += 1     
        
        # Generate csv files csvDataset   
        if csvDataset_data:  
            df = pd.DataFrame(csvDataset_data)
            df = df.fillna('')
            for column in df.columns:
                df[column] = df[column].apply(
                    lambda x: BeautifulSoup(x, 'lxml').get_text())
                for i in chars_to_remove:
                    df = df.applymap(lambda x: x.replace(
                        i, '') if (isinstance(x, str)) else x)  
            df.to_csv(os.path.join(
                    'EDC/REFERENCE_DATASET.csv'), sep=";", index=False)
            downloaded = downloaded + 1
        else:
            df = pd.DataFrame(csvDatasetEmpty)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join(
                'EDC/REFERENCE_DATASET.csv'), sep=";", index=False, header=True)
        
        # Generate csv files csvDatasource      
        if csvDatasource_data:
            df = pd.DataFrame(csvDatasource_data)
            df = df.fillna('')
            for column in df.columns:
                df[column] = df[column].apply(
                    lambda x: BeautifulSoup(x, 'lxml').get_text())
                for i in chars_to_remove:
                    df = df.applymap(lambda x: x.replace(
                        i, '') if (isinstance(x, str)) else x) 
            df.to_csv(os.path.join(
                    'EDC/REFERENCE_DATASOURCE.csv'), sep=";", index=False)
            downloaded = downloaded + 1
        else:
            df = pd.DataFrame(csvDatasourceEmpty)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join(
                'EDC/REFERENCE_DATASOURCE.csv'), sep=";", index=False, header=True)    
            
        if csvDataElement_data:
            df = pd.DataFrame(csvDataElement_data)
            df = df.fillna('')
            for column in df.columns:
                df[column] = df[column].apply(
                    lambda x: BeautifulSoup(x, 'lxml').get_text())
                for i in chars_to_remove:
                    df = df.applymap(lambda x: x.replace(
                        i, '') if (isinstance(x, str)) else x)
            df.to_csv(os.path.join(
                'EDC/REFERENCE_DATAELEMENT.csv'), sep=";", index=False)
            downloaded = downloaded + 1
        else: 
            df = pd.DataFrame(csvDataElementEmpty)
            df = df.iloc[0:-1]   
            df.to_csv(os.path.join(
                'EDC/REFERENCE_DATAELEMENT.csv'), sep=";", index=False, header=True)
         
    else:
        logging.error(f"Main EDC Failed: Status Code {str(resp1.status_code)}")
    
    ending_time = datetime.now()  # execution script code time
    resourceName = 'References'
    resourceType = 'Standard'
    # db data to be saved
    all_edc(resourceName, resourceType, downloaded, response_code,
            response_size, response_time, starting_time, ending_time)

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

        singleURL = EDC_URL_REST_2 + '/2/catalog/data/search?basicQuery=*&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.ReferenceDataSource%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.ReferenceDataSet%22&fq=%7B!tag%3Dresource_name%7Dcore.resourceName%3A%22' + \
                    resourceName + '%22&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize='+str(pageSize) + \
                    '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'

        resp2 = requests.get(
            singleURL, headers=EDC_headers, auth=EDC_Auth, verify=False)
        if resp2.status_code == 200:

            j_resp_2req = resp2.json()
            hits = j_resp_2req.get('hits')
            totalCount = j_resp_2req['metadata']['totalCount']
            newTotal = totalCount + pageSize            
            genAllReferenceCSVs(hits, EDC_headers, EDC_Auth)

            if newTotal > pageSeizeOffset:
                while totalCount > pageSeizeOffset:                    
                    offsetUrl = '/access/2/catalog/data/search?basicQuery=*&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.ReferenceDataSource%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.ReferenceDataSet%22&fq=%7B!tag%3Dresource_name%7Dcore.resourceName%3A%22' + \
                                resourceName + '%22&facet=false&defaultFacets=true&highlight=false&offset=' + \
                                str(pageSeizeOffset)+'&pageSize='+str(pageSize) +'&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'
                    
                    newUrlMain = EDC_URL + offsetUrl
                    newResp = requests.get(
                        newUrlMain, headers=EDC_headers, auth=EDC_Auth, verify=False)
                    
                    if newResp.status_code == 200:
                        newrespeData = newResp.json()
                        hits = newrespeData.get('hits')
                        genAllReferenceCSVs(hits, EDC_headers, EDC_Auth)
                    
                    else:
                        logging.error(f"Error rdbms pagination on offset: {pageSeizeOffset}")

                    pageSeizeOffset += pageSize

        else:
            logging.error('Error generating single resource.')


# Function get data and return json data
def genAllReferenceCSVs(hits, EDC_headers, EDC_Auth):
    for val in hits:
        if not val:
            pass
        else:
            valHits = val['values']
            valHref = val['href']
            for v in valHits:
                if v['attributeId'] == 'core.classType' and v['value'] == 'core.ReferenceDataSource':
                    ReferenceDataSource = EDC_URL_REST_2 + valHref + '?includeRefObjects=true'
                    ReferenceDataSourceReq = session.get(
                        ReferenceDataSource, headers=EDC_headers, auth=EDC_Auth, verify=False)
                    if ReferenceDataSourceReq.status_code == 200:
                        if not ReferenceDataSourceReq.content:
                            # print('1. ReferenceDataSource pass no content')
                            pass
                        else:
                            ReferenceDataSourceRes = ReferenceDataSourceReq.json()
                            genDataSourceCSV(ReferenceDataSourceRes)
                            # print(' GENERATING DataSource........')
                
                if v['attributeId'] == 'core.classType' and v['value'] == 'core.ReferenceDataSet':
                    datasetURL = EDC_URL_REST_2 + valHref + '?includeRefObjects=true'
                    datasetReq = session.get(
                        datasetURL, headers=EDC_headers, auth=EDC_Auth, verify=False)

                    if datasetReq.status_code == 200:
                        if not datasetReq.content:
                            # print('2. ReferenceDataSet pass no content')
                            pass

                        else:
                            datasetRes = datasetReq.json()
                            dstLinksTb = datasetRes['dstLinks']
                            genDatasetCSV(datasetRes)

                            for val in dstLinksTb:
                                if val['classType'] == "core.ReferenceDataElement":
                                    valHref = val['href']
                                    dataset_dstURL = EDC_URL_REST_2 + valHref + '?includeRefObjects=true'
                                    dataset_dstReq = session.get(
                                        dataset_dstURL, headers=EDC_headers, auth=EDC_Auth, verify=False)
                                    # handle other errors
                                    if dataset_dstReq.status_code == 200:
                                        if not dataset_dstReq.content:
                                            pass
                                        else:
                                            dataElementRes = dataset_dstReq.json()
                                            genDataElementCSV(
                                                dataElementRes)


# Function generating Datasource attributs
def genDataSourceCSV(ReferenceDataSourceRes): 
    finalId = ''
    DS_name = ''
    DS_lastModified = ''
    DS_gdprDataProc = ''
    DS_gdprDataProcModifiedBy = ''
    DS_architecturalLevel = ''
    DS_architecturalLevelModifiedBy = ''
    DS_businessDescription = ''
    DS_businessDescriptionModifiedBy = ''
    DS_resourceName = ''
    DS_resourceType = ''

    finalId = ReferenceDataSourceRes['id']
    dataSourcesFacts = ReferenceDataSourceRes['facts']

    for val in dataSourcesFacts:
        if val.get('attributeId') == 'core.name':
            DS_name = val.get('value')
        if val.get('attributeId') == 'core.lastModified':
            DS_lastModified = val.get(
                'value')
        if val.get('label') == 'GDPR Data Processing note':
            DS_gdprDataProc = val.get(
                'value')
        if val.get('label') == 'GDPR Data Processing note':
            DS_gdprDataProcModifiedBy = val.get(
                'modifiedBy')
        if val.get('label') == 'Architectural Level':
            DS_architecturalLevel = val.get(
                'value')
        if val.get('label') == 'Architectural Level':
            DS_architecturalLevelModifiedBy = val.get(
                'modifiedBy')
        if val.get(
                'label') == 'Business Description':
            DS_businessDescription = val.get('value')
        if val.get('label') == 'Business Description':
            DS_businessDescriptionModifiedBy = val.get(
                'modifiedBy')
        if val.get('attributeId') == 'core.resourceName':
            DS_resourceName = val.get(
                'value')
        if val.get('attributeId') == 'core.resourceType':
            DS_resourceType = val.get(
                'value')

    csvDatasource_data.append({
        'id': finalId,
        'name': DS_name,
        'Last Modified': DS_lastModified,
        'GDPR Data Processing note': DS_gdprDataProc,
        'GDPR Data Processing note modifiedby': DS_gdprDataProcModifiedBy,
        'Architectural Level': DS_architecturalLevel,
        'Architectural Level modifiedBy': DS_architecturalLevelModifiedBy,
        'Business Description': DS_businessDescription,
        'Business Description modifiedBy': DS_businessDescriptionModifiedBy,        
        'Resource Type': DS_resourceType,
        'Resource Name': DS_resourceName
    })
    logging.info(f"Resource Name: {DS_resourceName}")


# Function generating datasetRes attributs 
def genDatasetCSV(datasetRes): 
    finalId = ''
    D_set_lastModified = ''
    D_set_gdprDataProc = ''
    D_set_gdprDataProcmodifiedBy = ''
    D_set_DataQualityLink = ''
    D_set_DataQualityLinkModifiedBy = ''
    D_set_businessDescription = ''
    D_set_businessDescriptionModifiedBy = ''
    D_set_resourceName = ''
    D_set_name = ''
    D_set_DatasetId = ''

    finalId = datasetRes['id']
    datasetFacts = datasetRes['facts']

    for val in datasetFacts:
        if val.get('attributeId') == 'core.lastModified':
            D_set_lastModified = val.get(
                'value')
        if val.get('label') == 'GDPR Data Processing note':
            D_set_gdprDataProc = val.get(
                'value')
        if val.get('label') == 'GDPR Data Processing note':
            D_set_gdprDataProcmodifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Data Quality Link':
            D_set_DataQualityLink = val.get('value')
        if val.get('label') == 'Data Quality Link':
            D_set_DataQualityLinkModifiedBy = val.get(
                'modifiedBy')
        if val.get(
                'label') == 'Business Description':
            D_set_businessDescription = val.get('value')
        if val.get('label') == 'Business Description':
            D_set_businessDescriptionModifiedBy = val.get(
                'modifiedBy')
        if val.get('attributeId') == 'core.resourceName':
            D_set_resourceName = val.get(
                'value')
        if val.get('attributeId') == 'core.name':
            D_set_name = val.get('value')

    datasetsrcLinks = datasetRes['srcLinks']
    for valScr in datasetsrcLinks:
        if valScr.get('classType') == 'core.ReferenceDataSource':
            D_set_DatasetId = valScr.get('id')

    csvDataset_data.append({
        'id': finalId,
        'Last Modified': D_set_lastModified,
        'GDPR Data Processing note': D_set_gdprDataProc,
        'GDPR Data Processing note modifiedBy': D_set_gdprDataProcmodifiedBy,
        'Data Quality Link': D_set_DataQualityLink,
        'Data Quality Link modifiedBy': D_set_DataQualityLinkModifiedBy,
        'Business Description': D_set_businessDescription,
        'Business Description modifiedBy': D_set_businessDescriptionModifiedBy,
        'Resource Name': D_set_resourceName,
        'Name': D_set_name,
        'DataSource id': D_set_DatasetId
    })

# Function generating dataElementRes attributs
def genDataElementCSV(dataElementRes):
    finalId = ''
    DE_name = ''
    DE_lastModified = ''
    DE_KeyDataElement = ''
    DE_KeyDataElementModifiedBy = ''
    DE_gdprDataProc = ''
    DE_gdprDataProcmodifiedBy = ''
    DE_DataQualityLink = ''
    DE_DataQualityLinkModifiedBy = ''
    DE_AssetClassification = ''
    DE_AssetClassificationModifiedBy = ''
    DE_businessDescription = ''
    DE_businessDescriptionModifiedBy = ''
    DE_resourceName = ''
    DE_id = ''

    dataElementFacts = dataElementRes['facts']
    finalId = dataElementRes['id']
    for val in dataElementFacts:
        if val.get('attributeId') == 'core.name':
            DE_name = val.get('value')
        if val.get('attributeId') == 'core.lastModified':
            DE_lastModified = val.get('value')
        if val.get('label') == 'Key Data Element':
            DE_KeyDataElement = val.get('value')
        if val.get('label') == 'Key Data Element':
            DE_KeyDataElementModifiedBy = val.get('modifiedBy')
        if val.get('label') == 'GDPR Data Processing note':
            DE_gdprDataProc = val.get('value')
        if val.get('label') == 'GDPR Data Processing note':
            DE_gdprDataProcmodifiedBy = val.get('modifiedBy')
        if val.get('label') == 'Data Quality Link':
            DE_DataQualityLink = val.get('value')
        if val.get('label') == 'Data Quality Link':
            DE_DataQualityLinkModifiedBy = val.get(
                'modifiedBy')
        if val.get('label') == 'Asset Classification':
            DE_AssetClassification = val.get('value')
        if val.get('label') == 'Asset Classification':
            DE_AssetClassificationModifiedBy = val.get(
                'modifiedBy')
        if val.get('label') == 'Business Description':
            DE_businessDescription = val.get('value')
        if val.get('label') == 'Business Description':
            DE_businessDescriptionModifiedBy = val.get(
                'modifiedBy')
        if val.get('attributeId') == 'core.resourceName':
            DE_resourceName = val.get('value')

    dataElsrcLinks = dataElementRes['srcLinks']
    for valScr in dataElsrcLinks:
        if valScr.get('classType') == 'core.ReferenceDataSet':
            DE_id = valScr.get('id')

    csvDataElement_data.append({
        'id': finalId,
        'name': DE_name,
        'Last Modified': DE_lastModified,
        'Key Data Element': DE_KeyDataElement,
        'Key Data Element modifiedBy': DE_KeyDataElementModifiedBy,
        'GDPR Data Processing note': DE_gdprDataProc,
        'GDPR Data Processing note modifiedBy': DE_gdprDataProcmodifiedBy,
        'Data Quality Link': DE_DataQualityLink,
        'Data Quality Link modifiedBy': DE_DataQualityLinkModifiedBy,
        'Asset Classification': DE_AssetClassification,
        'Asset Classification modifiedBy': DE_AssetClassificationModifiedBy,
        'Business Description': DE_businessDescription,
        'Business Description modifiedBy': DE_businessDescriptionModifiedBy,
        'Resource Name': DE_resourceName,
        'DataSet id': DE_id
    })

def mainReferencesFile():
    try:
        return genReferencesFile()
    except Exception as e:
        return e