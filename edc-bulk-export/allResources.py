from props.utils import os, pd, requests, HTTPAdapter, BeautifulSoup, Retry, datetime, logging
from props.paramsEdc import EDC_URL_REST_1, EDC_URL_REST_2, EDC_headers, EDC_Auth, pageSize, EDC_URL, chars_to_remove, val_DGR
from db.database import all_edc

session = requests.Session()
retry = Retry(total=5,
              backoff_factor=1,
              status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


# post api with raw data & get response and add to csv
def genAllResourcesFile():
    downloaded = 0
    if not os.path.exists('EDC'):
        os.makedirs('EDC')
    csvResources = []
    pageSeizeOffset = pageSize
    
    logging.debug(f"EDC_URL_REST_1: {EDC_URL_REST_1}")
    resp1 = session.get(EDC_URL_REST_1, headers=EDC_headers, auth=EDC_Auth, verify=False)

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
        totalDownload = generateCSV(hits, EDC_headers, EDC_Auth, csvResources)
        downloaded += totalDownload
        if newTotal > pageSeizeOffset:
            while totalPage > pageSeizeOffset:
                # print("Pagination ALL RESOURCES: Offset items: -- ", pageSeizeOffset)
          
                offsetUrl = '/access/2/catalog/data/search?basicQuery=*&tabId=tab.resources&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22JDBC%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Teradata%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Hive%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22IBM%5C%20DB2%5C%20for%5C%20z%5C%2FOS%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Oracle%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Azure%5C%20Microsoft%5C%20SQL%5C%20Server%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22DataFile%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Microsoft%20SQL%20Server%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22DataFile%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Reference%5C%20resource%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.Resource%22&fq='+val_DGR+'&facet=false&defaultFacets=true&highlight=false&offset='+str(pageSeizeOffset)+'&pageSize=' + \
                            str(pageSize)+'&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'
                newUrlMain = EDC_URL + offsetUrl
                respWhile = requests.get(
                    newUrlMain, headers=EDC_headers, auth=EDC_Auth, verify=False)

                if respWhile.status_code == 200:
                    respWhileData = respWhile.json()
                    hits = respWhileData.get('hits')
                    totalDownload = generateCSV(
                        hits, EDC_headers, EDC_Auth, csvResources)
                    downloaded += totalDownload
                else:
                    logging.error(f"Error pagination on offset ALL RESOURCES: {pageSeizeOffset}")

                pageSeizeOffset += pageSize

    else:
        logging.error(f"Main EDC failed with status code: {str(resp1.status_code)}")

    ending_time = datetime.now()  # execution script code time
    resourceName = 'All Resources'
    resourceType = 'Standard'
    
    # db data to be saved
    all_edc(resourceName, resourceType, downloaded, response_code,
            response_size, response_time, starting_time, ending_time)

    return downloaded


def generateCSV(hits, EDC_headers, EDC_Auth, csvExport):
    downloaded = 0

    for val_hits in hits:
        hurl = val_hits['href']
        resID = val_hits['id']
        values_hits = val_hits.get('values')
        resourceName = None
        resourceType = None
        lastScanStatus = ''
        lastScanDate = ''
        lastModified = ''
        keyDataEle = ''
        keyDataEleModBy = ''
        dataGovRel = ''
        dataGovRelModifiedBy = ''
        gdprDataProc = ''
        gdprDataProcModifiedBy = ''
        acronym = ''
        acronymModifiedBy = ''
        scope = ''
        scopeModifiedBy = ''
        architecturalLevel = ''
        architecturalLevelModifiedBy = ''
        ownershipLink = ''
        ownershipLinkModifiedBy = ''
        resourceLocation = ''
        resourceLocationModifiedBy = ''
        businessDescription = ''
        businessDescriptionModifiedBy = ''
        createdTime = ''
        systemCaseSensitivity = ''
        description = ''

        for val_values in values_hits:
            if val_values.get('attributeId') == 'core.resourceName':
                resourceName = val_values.get('value')
            if val_values.get('attributeId') == 'core.resourceType':
                resourceType = val_values.get('value')

        # print('Generating single resurce : ', resourceName, '...')

        singleURL = EDC_URL_REST_2 + hurl + '?includeRefObjects=true'
        resp2 = requests.get(
            singleURL, headers=EDC_headers, auth=EDC_Auth, verify=False)
            
        if resp2.status_code == 200:
            if not resp2.content:
                csvExport.append({
                    'id': resID,
                    'Resource Name': resourceName,
                    'Resource Type': resourceType,
                    'Last Scan Status': '',
                    'Last Scan Date': '',
                    'Last Modified': '',
                    'Key Data Element': '',
                    'Key Data Element modifiedBy': '',
                    'Data Governance Relevant': '',
                    'Data Governance Relevant modifiedBy': '',
                    'GDPR Data Processing note': '',
                    'GDPR Data Processing note modifiedBy': '',
                    'Acronym': '',
                    'Acronym modifiedBy': '',
                    'Scope': '',
                    'Scope modifiedBy': '',
                    'Architectural Level': '',
                    'Architectural Level modifiedBy': '',
                    'Ownership link': '',
                    'Ownership link modifiedBy': '',
                    'Resource Location': '',
                    'Resource Location modifiedBy': '',
                    'Business Description': '',
                    'Business Description modifiedBy': '',
                    'Created Time': '',
                    'Case Sensitivity': '',
                    'Description': '',
                })

            else:
                # print('Generating single resurce : ', resourceName, '...')
                j_resp_2req = resp2.json()
                facts = j_resp_2req.get('facts')

                for val in facts:
                    if val.get('label') == 'Last Scan Status':
                        lastScanStatus = val.get('value')
                    if val.get('label') == 'Last Scan Date':
                        lastScanDate = val.get('value')
                    if val.get('label') == 'Last Modified':
                        lastModified = val.get('value')
                    if val.get('label') == 'Key Data Element':
                        keyDataEle = val.get('value')
                    if val.get('label') == 'Key Data Element':
                        keyDataEleModBy = val.get('modifiedBy')
                    if val.get('label') == 'Data Governance Relevant':
                        dataGovRel = val.get('value')
                    if val.get('label') == 'Data Governance Relevant':
                        dataGovRelModifiedBy = val.get('modifiedBy')
                    if val.get('label') == 'GDPR Data Processing note':
                        gdprDataProc = val.get('value')
                    if val.get('label') == 'GDPR Data Processing note':
                        gdprDataProcModifiedBy = val.get('modifiedBy')
                    if val.get('label') == 'Acronym':
                        acronym = val.get('value')
                    if val.get('label') == 'Acronym':
                        acronymModifiedBy = val.get('modifiedBy')
                    if val.get('label') == 'Scope':
                        scope = val.get('value')
                    if val.get('label') == 'Scope':
                        scopeModifiedBy = val.get('modifiedBy')
                    if val.get('label') == 'Architectural Level':
                        architecturalLevel = val.get('value')
                    if val.get('label') == 'Architectural Level':
                        architecturalLevelModifiedBy = val.get(
                            'modifiedBy')
                    if val.get('label') == 'Ownership link':
                        ownershipLink = val.get('value')
                    if val.get('label') == 'Ownership link':
                        ownershipLinkModifiedBy = val.get('modifiedBy')
                    if val.get('label') == 'Resource Location':
                        resourceLocation = val.get('value')
                    if val.get('label') == 'Resource Location':
                        resourceLocationModifiedBy = val.get('modifiedBy')
                    if val.get('label') == 'Business Description':
                        businessDescription = val.get('value')
                    if val.get('label') == 'Business Description':
                        businessDescriptionModifiedBy = val.get(
                            'modifiedBy')
                    if val.get('label') == 'Created Time':
                        createdTime = val.get('value')
                    if val.get('label') == 'Case Sensitivity':
                        systemCaseSensitivity = val.get('value')
                    if val.get('label') == 'description':
                        description = val.get('value')

                csvExport.append({
                    'id': resID,
                    'Resource Name': resourceName,
                    'Resource Type': resourceType,
                    'Last Scan Status': lastScanStatus,
                    'Last Scan Date': lastScanDate,
                    'Last Modified': lastModified,
                    'Key Data Element': keyDataEle,
                    'Key Data Element modifiedBy': keyDataEleModBy,
                    'Data Governance Relevant': dataGovRel,
                    'Data Governance Relevant modifiedBy': dataGovRelModifiedBy,
                    'GDPR Data Processing note': gdprDataProc,
                    'GDPR Data Processing note modifiedBy': gdprDataProcModifiedBy,
                    'Acronym': acronym,
                    'Acronym modifiedBy': acronymModifiedBy,
                    'Scope': scope,
                    'Scope modifiedBy': scopeModifiedBy,
                    'Architectural Level': architecturalLevel,
                    'Architectural Level modifiedBy': architecturalLevelModifiedBy,
                    'Ownership link': ownershipLink,
                    'Ownership link modifiedBy': ownershipLinkModifiedBy,
                    'Resource Location': resourceLocation,
                    'Resource Location modifiedBy': resourceLocationModifiedBy,
                    'Business Description': businessDescription,
                    'Business Description modifiedBy': businessDescriptionModifiedBy,
                    'Created Time': createdTime,
                    'Case Sensitivity': systemCaseSensitivity,
                    'Description': description,
                })

                logging.info(f"Resource Name: {resourceName}")
                
                df = pd.DataFrame(csvExport)
                #df = df.fillna('')
                for column in df[0:-1].columns:
                    df[column] = df[column].apply(lambda x: BeautifulSoup(x, 'lxml').get_text())
                    for i in chars_to_remove:
                        df = df.applymap(lambda x: x.replace(
                            i, '') if (isinstance(x, str)) else x)

                df.to_csv(os.path.join('EDC/RESOURCES.csv'),
                            sep=";", index=False)
                            
                downloaded = 1

        else:
            logging.error("Error generating single resource.")

    return downloaded


def mainAllResourcesFile():
    try:
        return genAllResourcesFile()
    except Exception as e:
        return e