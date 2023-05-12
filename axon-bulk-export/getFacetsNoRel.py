from props.utils import os, requests, json, time, start_time, datetime, dt_string, pd, BeautifulSoup, re, logging
from facetOptionsNoRel import facets
from db.database import axon_facets, dbGeneral
from props.paramsAxon import facetPageLimit, chars_to_remove

gerenal_time = time.time()

# Opening AXON_last_updates file to save last update if there is any..
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'AXON_last_updates.json')
with open(file_path, 'r') as f:
# returns JSON object as a dictionary
    dataUpdate = json.load(f)

# Get facet items and save to CSV & Database
def createDir():
    # check if has directory, if not create..
    if not os.path.exists('../AXON/'):
        os.makedirs('../AXON/')


def noRelationFacets(baseurl, infaTokenValue, headerValue, sessionCookies):
    totalFacet = 0  # total number of facets to be saved into database
    createDir()

    # for each facet in facetOptions make POST request and save csv
    for facet in facets:
        toExport = []
        nameFacete = facet.get('mainFacet')  # get facet name

        logging.info(f"Working on facets: {nameFacete}")
        logging.debug(f"Facet: {facet}")

        facetLimitMain = facet["searchScopes"]["mainFacet"]["properties"]["limit"]
        # set token autherization
        headerValue = {'Authorization': infaTokenValue,
                       'Content-Type': 'application/json'}
        # convert facet body POST into json
        bodyData = json.dumps(facet)
        # send request with authorization and body data
        r = requests.post(baseurl, headers=headerValue,
                          verify=False, cookies=sessionCookies, stream=True, data=bodyData)
        # db data to be saved
        starting_time = datetime.now()
        downloaded = False
        # server response time converted in seconds
        response_time = str(r.elapsed.total_seconds()) + ' s'
        # server response sice converted in kb
        response_size = str(len(r.content) / 1024) + ' kb'
        response_code = r.status_code  # server status code
        # end db data

        # if success create csv
        if r.status_code == 200:

            json_data = r.json()  # convert response to json

            getOrgUnitItems = json_data.get(
                "mainObject")  # get mainObject with items
            totalHits = getOrgUnitItems["totalHits"]
            columns = getOrgUnitItems.get('fields')  # get csv columns names
            mainItems = getOrgUnitItems.get("items")  # get items
            limitValue = int(facetLimitMain)
            totalFacet = totalFacet + 1  # increment total facets number for general table databse

            if not mainItems:
                exportEmpty = []

                if nameFacete == 'BUSINESS_AREA':
                    exportEmpty.append({
                        "id": '',
                        "name": '',
                                "parentId": '',
                                "parentName": '',
                                "description": '',
                                "lifecycle": '',
                                "axonStatus": '',
                                "level": '',
                                "accessControl": '',
                                "segments": '',
                                "segmentsName": '',
                                "LongDescription": '',
                                "DocumentLink": '',
                                "Type": '',
                                "OwnershipLink": '',
                    }),
                if nameFacete == 'SYSTEM':
                    exportEmpty.append({
                        "id": '',
                        "name": '',
                        "description": '',
                        "parentId": '',
                                    "parentName": '',
                                    "type": '',
                                    "Url": '',
                                    "external": '',
                                    "axonStatus": '',
                                    "longName": '',
                                    "lifecycle": '',
                                    "classification": '',
                                    "createdBy": '',
                                    "createdById": '',
                                    "createdDate": '',
                                    "lastUpdatedDate": '',
                                    "accessControl": '',
                                    "crating": '',
                                    "irating": '',
                                    "arating": '',
                                    "ciarating": '',
                                    "assetId": '',
                                    "segments": '',
                                    "segmentsName": '',
                                    "lastApprovedDate": '',
                                    "Frequency": '',
                                    "CompilingDate": '',
                                    "ReferenceDate": '',
                                    "UpdatingDate": '',
                                    "ExecutionType": '',
                                    "ProcessPerimeter": '',
                                    "TechnologicalTransformation": '',
                    }),
                if nameFacete == 'DATASET':
                    exportEmpty.append({
                        "id": '',
                        "name": '',
                        "definition": '',
                        "refNumber": '',
                        "type": '',
                        "axonStatus": '',
                        "lifecycle": '',
                        "systemId": '',
                        "systemName": '',
                        "glossaryId": '',
                        "glossaryName": '',
                        "collectionIds": '',
                        "collectionNames": '',
                        "collectionCategoryNames": '',
                        "datasetPublishStatus": '',
                        "createdBy": '',
                        "createdById": '',
                        "createdDate": '',
                        "lastUpdatedDate": '',
                        "accessControl": '',
                        "ciUsage": '',
                        "segments": '',
                        "segmentsName": '',
                        "lastApprovedDate": '',
                        "dqScore": '',
                        "dqGreenTarget": '',
                        "dqAmberTarget": '',
                        "PhaseType": '',
                        "ExecutionType": '',
                    }),
                if nameFacete == 'ATTRIBUTE':
                    exportEmpty.append({
                        "id": '',
                        "name": '',
                        "definition": '',
                        "refNumber": '',
                        "dataSetId": '',
                        "dataSetName": '',
                        "dbName": '',
                        "dbFormat": '',
                        "systemId": '',
                        "systemName": '',
                        "origination": '',
                        "discoveryReviewStatus": '',
                        "confidenceScore": '',
                        "editabilityRole": '',
                        "editability": '',
                        "glossaryId": '',
                        "glossaryName": '',
                        "mandatory": '',
                        "createdBy": '',
                        "createdById": '',
                        "createdDate": '',
                        "lastUpdatedDate": '',
                        "segments": '',
                        "segmentsName": '',
                        "ShortDescription": '',
                        "DocumentLink": '',
                        "DomainFlag": '',
                        "AliasNames": '',
                        "Frequency": '',
                        "Granularity": '',
                        "ManualityFlag": '',
                        "ManualityType": '',
                        "KDE": '',
                        "GlossaryClassification": '',
                    }),
                if nameFacete == 'GLOSSARY':
                    exportEmpty.append({
                        "id": '',
                        "refNumber": '',
                        "name": '',
                        "type": '',
                        "parentId": '',
                                    "parentName": '',
                                    "parentType": '',
                                    "kde": '',
                                    "description": '',
                                    "alias": '',
                                    "lifecycle": '',
                                    "axonStatus": '',
                                    "securityClassification": '',
                                    "level": '',
                                    "createdBy": '',
                                    "createdById": '',
                                    "lastUpdateUser": '',
                                    "lastUpdateUserId": '',
                                    "createdDate": '',
                                    "lastUpdatedDate": '',
                                    "ldm": '',
                                    "businessLogic": '',
                                    "examples": '',
                                    "format": '',
                                    "formatType": '',
                                    "accessControl": '',
                                    "crating": '',
                                    "irating": '',
                                    "arating": '',
                                    "ciarating": '',
                                    "segments": '',
                                    "segmentsName": '',
                                    "lastApprovedDate": '',
                                    "ShortDescription": '',
                    }),
                if nameFacete == 'PEOPLE':
                    exportEmpty.append({
                        "id": '',
                        "fullName": '',
                        "firstName": '',
                        "lastName": '',
                        "email": '',
                        "function": '',
                        "employeeType": '',
                        "orgUnitRef": '',
                        "orgUnitId": '',
                        "orgUnitName": '',
                        "axonStatus": '',
                        "profileId": '',
                        "profileName": '',
                        "lastLogon": '',
                        "lifecycle": '',
                        "lanID": '',
                        "createdDate": '',
                        "lastUpdatedDate": '',
                        "officeLocation": '',
                        "internalMailCode": '',
                        "officeTelephone": '',
                        "mobileTelephone": '',
                    }),
                if nameFacete == 'SYSTEM_INTERFACE':
                    exportEmpty.append({
                        "id": '',
                        "refNumber": '',
                        "name": '',
                        "description": '',
                        "sourceId": '',
                        "sourceName": '',
                        "targetId": '',
                        "targetName": '',
                        "axonStatus": '',
                        "automation": '',
                        "frequency": '',
                        "lifecycle": '',
                        "synchronisation": '',
                        "assetId": '',
                        "classification": '',
                        "createdBy": '',
                        "createdById": '',
                        "createdDate": '',
                        "lastUpdatedDate": '',
                        "accessControl": '',
                        "segments": '',
                        "segmentsName": '',
                        "transfermethod": '',
                        "transferformat": '',

                    }),
                if nameFacete == 'DATAQUALITY':
                    exportEmpty.append({
                        "id": '',
                        "refNumber": '',
                        "name": '',
                        "description": '',
                        "attributeId": '',
                        "attributeName": '',
                        "measuredInId": '',
                        "measuredInName": '',
                        "type": '',
                        "lifecycle": '',
                        "criticality": '',
                        "greenTarget": '',
                        "amberTarget": '',
                        "reportMonth": '',
                        "result": '',
                        "measured": '',
                        "axonStatus": '',
                        "accessControl": '',
                        "technicalDesc": '',
                        "population": '',
                        "measuringMethodDesc": '',
                        "automation": '',
                        "frequency": '',
                        "measuringMethod": '',
                        "segments": '',
                        "segmentsName": '',
                        "reportStatus": '',
                    })

                df = pd.DataFrame(exportEmpty)
                df = df.iloc[0:-1]
                nameFacete = nameFacete.upper()
                # save to csv: facetname + current date
                df.to_csv(os.path.join('../AXON/'+nameFacete+'.csv'),
                          sep=";", index=False)

            else:
                exportData = createArray(
                    mainItems,  toExport)

                while totalHits > limitValue:
                    logging.debug(f'Running facet {nameFacete} -> {limitValue}')

                    offsetVal = int(limitValue)
                    facet["searchScopes"]["mainFacet"]["properties"]["offset"] = offsetVal

                    newFacet = json.dumps(facet)

                    r2 = requests.post(baseurl, headers=headerValue,
                                       verify=False, cookies=sessionCookies, stream=True, data=newFacet)

                    # if success create csv
                    if r2.status_code == 200:
                        json_resp = r2.json()  # convert response to json
                        # get mainObject with items
                        mainObject = json_resp.get("mainObject")
                        offsetItems = mainObject.get("items")  # get items
                        exportData = createArray(
                            offsetItems,  toExport)
                    limitValue += facetPageLimit
             
                if nameFacete == 'ATTRIBUTE':
                    df = pd.DataFrame(exportData, columns = columns)
                    df = df.reindex(['id' ,'name' ,'definition' ,'refNumber' ,'dataSetId' ,'dataSetName' ,'dbName' 
                                             ,'dbFormat' ,'systemId' ,'systemName' ,'origination' ,'discoveryReviewStatus'
                                             ,'confidenceScore' ,'editabilityRole' ,'editability' ,'glossaryId' ,'glossaryName' 
                                             ,'mandatory' ,'createdBy' ,'createdById' ,'createdDate' ,'lastUpdatedDate' ,'segments' 
                                             ,'segmentsName' ,'ShortDescription' ,'DocumentLink' ,'DomainFlag' ,'AliasNames' 
                                             ,'Frequency' ,'Granularity' ,'ManualityFlag' ,'ManualityType' ,'KDE' ,'GlossaryClassification'] , axis=1)
                    
                    for column in df[0:-1].columns:
                        df[column] = df[column].apply(lambda x: BeautifulSoup(x, 'lxml').get_text())

                        for i in chars_to_remove:
                            df = df.applymap(lambda x: x.replace(i, '') if (isinstance(x, str)) else x)
                            
                            # save to csv: facetname + current date
                            df.to_csv(os.path.join('../AXON/'+nameFacete+'.csv'), sep=';', index=False)

                else:
                    if nameFacete != 'ATTRIBUTE':
                        df = pd.DataFrame(exportData, columns = columns)
                                    
                        for column in df[0:-1].columns:
                            df[column] = df[column].apply(lambda x: BeautifulSoup(x, 'lxml').get_text())
                            for i in chars_to_remove:
                                df = df.applymap(lambda x: x.replace(i, '') if (isinstance(x, str)) else x)
                                # save to csv: facetname + current date
                                df.to_csv(os.path.join('../AXON/'+nameFacete+'.csv'), sep=';',
                                            columns=columns, index=False)

            # update current facet in json file with current datetime
            dataUpdate[nameFacete] = str(dt_string)

            # save json file with update date
            script_dir = os.path.dirname(__file__)
            file_path = os.path.join(script_dir, 'AXON_last_updates.json')
            
            with open(file_path, 'w') as outfile:
                json.dump(dataUpdate, outfile)

            # set download true for this facet into facet table database
            downloaded = True

        else:
            logging.error(f"{nameFacete} failed with status code {str(r.status_code)}")

        ending_time = datetime.now()  # execution script code time

        # save facet data into facet table database
        axon_facets(nameFacete, response_code, response_size,
                    response_time, downloaded, starting_time, ending_time)
                    
    # save total facets data into general table database
    dbGeneral(dt_string, totalFacet,
              0, (time.time() - gerenal_time))


def createArray(mainItems, toExport):
    # create dataframe to save into csv
    for val_Iteams in mainItems:
        values = val_Iteams.get('values')
        toExport.append(values)
    return toExport
