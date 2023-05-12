from props.utils import os, pd, requests, HTTPAdapter, Retry, datetime, logging
from props.paramsEdc import LINEAGE_REST_1, EDC_URL_REST_2, EDC_headers, EDC_Auth, pageSize, EDC_URL,  basicQueryFilter, ambienteFilter
from db.database import edc_lineages
# from logging import exception

session = requests.Session()
retry = Retry(total=5,
              backoff_factor=1,
              status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# empty array
csvLineageColumns = []
dataDomainNames = []
# post api with raw data & get response and add to csv


# Function get customDatadomainFile resources, do pagination and generate csv to export
def getLineagesEdc():
    downloaded = 0
    if not os.path.exists('EDC'):
        os.makedirs('EDC')

    pageSeizeOffset = pageSize

    #print('DEBUG LINEAGE_REST_1',LINEAGE_REST_1)

    logging.debug(f"LINEAGE_REST_1: {LINEAGE_REST_1}")
    
    resp1 = requests.get(LINEAGE_REST_1,
                         headers=EDC_headers, auth=EDC_Auth, verify=False)

    # db data to be saved
    starting_time = datetime.now()

    # server response time converted in seconds
    response_time = str(resp1.elapsed.total_seconds()) + ' s'
    # server response sice converted in kb
    response_size = str(len(resp1.content) / 1024) + ' kb'
    response_code = resp1.status_code  # server status code
    # end db data

    # print('first call here : ', LINEAGE_REST_1)
    if resp1.status_code == 200:
        # print('call passed here:')
        j_resp_1req = resp1.json()
        #logging.debug(f"j_resp_1req: {j_resp_1req}")

        hits = j_resp_1req.get('hits')
        logging.debug(f"hits: {hits}")

        totalPage = j_resp_1req['metadata']['totalCount']
        logging.debug(f"totalPage: {totalPage}")

        genLineageAll(hits)

        newTotal = totalPage + pageSize
        logging.debug(f"newTotal: {newTotal}")

        pageSeizeOffset = pageSize

        if newTotal > pageSeizeOffset:
            while newTotal > pageSeizeOffset:
                #print("Pagination Lineage: Offset items: -- ", pageSeizeOffset)
                #print("newTotal: --", newTotal)
                #print("totalPage: -- ", totalPage)
                logging.debug(f"Pagination Lineage: Offset items: {pageSeizeOffset}")

                offsetUrl = '/access/2/catalog/data/search?basicQuery=*' + \
                    basicQueryFilter + '&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.profiling.DataDomain%22&fq=%7B!tag%3Dresource_name%7Dcore.resourceName%3A%22DataDomain%22&fq=' + \
                    ambienteFilter + '&defaultFacets=true&highlight=false&offset=' + \
                    str(pageSeizeOffset) + '&pageSize=' + str(pageSize) + \
                    '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'

                newUrlMain = EDC_URL + offsetUrl

                logging.debug(f"newUrlMain: {newUrlMain}")

                respWhile = requests.get(
                    newUrlMain, headers=EDC_headers, auth=EDC_Auth, verify=False)

                if respWhile.status_code == 200:
                    respWhileData = respWhile.json()
                    hits = respWhileData.get('hits')
                    genLineageAll(hits)

                else:
                    logging.error(f"Error pagination on offset: {pageSeizeOffset}")

                pageSeizeOffset += pageSize

        # Generate csv files csvLineageColumns
        if csvLineageColumns:
            df = pd.DataFrame(csvLineageColumns)
            df.drop_duplicates(inplace=True)
            downloaded += 1
            df.to_csv(os.path.join(
                'EDC/LINEAGE_x_COLUMN.csv'), sep=";", index=False)

        if not csvLineageColumns:
            csvLineageColumns.append({
                "id": '',
                "outResource": '',
                "outId": '',
                "inResource": '',
                "inId": ''
            })
            df = pd.DataFrame(csvLineageColumns)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join(
                'EDC/LINEAGE_x_COLUMN.csv'), sep=";", index=False)

    else:
        logging.error(f"Main EDC Failed with status code: {str(resp1.status_code)}")

    ending_time = datetime.now()  # execution script code time

    # db data to be saved
    edc_lineages(downloaded, response_code, response_size, response_time, starting_time, ending_time)

# Function generating Columns attributs

def genLineageAll(hits):
    #print('starting to generate lineages by hits')
    if not hits:
        pass
    else:
        for val in hits:
            values = val['values']
            #logging.debug(f"values: {values}")
            nameUrl = ''
            
            for v in values:
                if v['attributeId'] == 'core.name':
                    nameUrl = v['value']
                    
            print('DataDomain ID', nameUrl)
            logging.debug(f"DataDomain ID: {nameUrl}")
            
            newUrl = EDC_URL_REST_2 + '/2/catalog/data/search?basicQuery=' + nameUrl + '&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Column%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.ViewColumn%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesColumnName%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.ReferenceDataElement%22&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize='+ str(pageSize) +'&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'
            #print('newUrl', newUrl)
            resp = requests.get(newUrl,
                                headers=EDC_headers, auth=EDC_Auth, verify=False)
            #print('resp', resp)
            if resp.status_code == 200:
                if not resp.content:
                    pass
                else:
                    domain = resp.json()
                    hits = domain['hits']
                    #print('domain', domain)
                    if not hits:
                        pass
                    else:
                        for val in hits:
                            url = val['id']
                            generateColumns(url)
                            # print('url', url)
                    totalPage = domain['metadata']['totalCount']
                    newTotal = totalPage + pageSize
                    pageSeizeOffset = pageSize
                    # print('pageSeizeOffset', pageSeizeOffset)
                    if newTotal >= pageSeizeOffset:
                        while totalPage >= pageSeizeOffset:
                            print(f"Pagination Lineage: Offset items: -- {pageSeizeOffset} ")
                            logging.debug(f"Pagination Lineage: Offset items: -- {pageSeizeOffset} ")
                            offsetUrl = '/access/2/catalog/data/search?basicQuery=' + nameUrl + '&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Column%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.ViewColumn%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22DataFile.Custom.Upload.FilesColumnName%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.ReferenceDataElement%22&facet=false&defaultFacets=true&highlight=false&offset='+ str(pageSeizeOffset) +'&pageSize='+ str(pageSize) +'&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'
                            # print('newUrl', newUrl)
                            newUrlMain = EDC_URL + offsetUrl
                            #print('newUrlMain', newUrlMain)
                            respWhile = requests.get(
                                newUrlMain, headers=EDC_headers, auth=EDC_Auth, verify=False)
                            if respWhile.status_code == 200:
                                if not resp.content:
                                    pass
                                else:
                                    domain = respWhile.json()
                                    hits = domain['hits']
                                    if not hits:
                                        pass
                                    else:
                                        for val in hits:
                                            url = val['id']
                                            generateColumns(url)
                            
                            
                            else:
                                print("Error pagination on offset: ", pageSeizeOffset)
                                logging.error("Error pagination on offset: ", pageSeizeOffset)
                            pageSeizeOffset += pageSize
            else:
                print('Error Getting single domain data')
                logging.error('Error Getting single domain data')


def generateColumns(childId):
    #print('DEBUG Columns ID: ' + childId)
    childId = childId.replace('&','%26amp')
    logging.info('Columns ID: ' + childId)
                  
    lineageColumnUrl = EDC_URL_REST_2 + \
        '/2/catalog/data/relationships?association=core.DataFlow&depth=0&direction=IN&includeRefObjects=true&includeTerms=false&removeDuplicateAggregateLinks=true&seed=' + childId

    #print("DEBUG lineageColumnUrl:",lineageColumnUrl)
    lineageColumnReq = session.get(
        lineageColumnUrl, headers=EDC_headers, auth=EDC_Auth, verify=False)

    if lineageColumnReq.status_code == 200:
        if not lineageColumnReq.content:
            #print('Lineage columns no content')
            logging.info('Lineage columns no content')
            pass
        else:
            lineageColumnRes = lineageColumnReq.json()
            columnItems = lineageColumnRes['items']
            if not columnItems:
                #print('lineage columns no items')
                logging.info('Lineage columns no items')
                pass
            else:
                for val in columnItems:

                    mainId = childId
                    outResource = val['outResource'] or ''
                    outId = val['outId'] or ''
                    inResource = val['inResource'] or ''
                    inId = val['inId'] or ''

                    csvLineageColumns.append({
                        "id": mainId,
                        "outResource": outResource,
                        "outId": outId,
                        "inResource": inResource,
                        "inId": inId
                    })
                    # print('Generating Columns: ', mainId)

    else:
        #print('Error generating lineage columns: ',lineageColumnReq.status_code)
        logging.error(f"Error generating lineage columns: {lineageColumnReq.status_code}")
       
        
def mainLineagesEdc():
    try:
        return getLineagesEdc()

    except Exception as e:
        return e

