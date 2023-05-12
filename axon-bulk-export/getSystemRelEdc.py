from props.utils import os, requests, json, pd, BeautifulSoup, logging
from props.paramsAxon import facetPageLimit, baseurl, chars_to_remove


def createDir():
    # check if has directory, if not create..
    if not os.path.exists('../AXON/'):
        os.makedirs('../AXON/')

def getSystemResources(searchUrl, infaTokenValue, headerValue, sessionCookies):
    createDir()
    systemRel = []
    
    logging.debug("Serching in progress for System resources...")

    bodyData = {
        "mainFacet": "SYSTEM",

        "searchScopes": {
            "mainFacet": {
                "facetId": "SYSTEM",
                "fields": [
                    "id",
                    "name",
                    "description",
                    "parentId",
                    "parentName",
                    "type",
                    "Url",
                    "external",
                    "axonStatus",
                    "longName",
                    "lifecycle",
                    "classification",
                    "createdBy",
                    "createdById",
                    "createdDate",
                    "lastUpdatedDate",
                    "accessControl",
                    "crating",
                    "irating",
                    "arating",
                    "ciarating",
                    "assetId",
                    "segments",
                    "segmentsName",
                    "lastApprovedDate",
                    "Frequency",
                    "CompilingDate",
                    "ReferenceDate",
                    "UpdatingDate",
                    "ExecutionType",
                    "ProcessPerimeter",
                    "TechnologicalTransformation"
                ],
                "orderList": [
                    {
                        "field": "id",
                        "type": "ASC"
                    }
                ],
                "properties": {
                    "offset": "0",
                    "limit": str(facetPageLimit)
                }
            }
        }
    }

    # convert facet body POST into json
    body = json.dumps(bodyData)
    headerValue = {'Authorization': infaTokenValue,
                   'Content-Type': 'application/json'}

    r = requests.post(searchUrl, headers=headerValue,
                      verify=False, cookies=sessionCookies, stream=True, data=body)

    # if success create csv
    if r.status_code == 200:
        l = r.json()  # convert response to json

        getOrgUnitItems = l.get("mainObject")  # get mainObject with items
        mainItems = getOrgUnitItems.get("items")  # get items
        totalHits = getOrgUnitItems["totalHits"]

        if not mainItems:
            pass

        else:
            
            # create dataframe to save into csv
            for x in mainItems:
                reliD = x.get('id')

                logging.info(f"Working on system resource with ID: {reliD}")

                # set token autherization
                newurl = baseurl + '/api/v1/referencelinks?sourceIds[]='+reliD + \
                    r'&entityType=Axon\AppBundle\Entity\System&systemIdentifier=Axon&relationshipNames[]=AxonSystemToEICResource'

                systemR = requests.get(newurl, headers=headerValue,
                                       verify=False, cookies=sessionCookies, stream=True)

                if systemR.status_code == 200:
                    systemL = systemR.json()  # convert response to json
                    results = systemL.get('results')
                    
                    if not results:
                        pass

                    else:
                        # create dataframe to save into csv
                        logging.debug(f"Results for SYSTEM relation to EDC for ID: {reliD}")

                        for result in results:
                            link = result.get('links')

                            if not link:
                                pass

                            else:
                                for item in link:
                                    systemRel.append({
                                        'main_objectIdentifier':  result['objectIdentifier'],
                                        'child_objectIdentifier':  item['objectIdentifier'],
                                        'entityType':  item['entityType'],
                                        'ResourceName':  item['properties']['ResourceName'],
                                    })
                else:
                    logging.error(f"Resource ID {reliD} failed with status code: {str(systemR.status_code)}")

        limitValue = facetPageLimit

        while totalHits > limitValue:
            offsetVal = str(limitValue)
            bodyData2 = bodyData
            bodyData2["searchScopes"]["mainFacet"]["properties"]["offset"] = offsetVal

            newFacet = json.dumps(bodyData2)

            rPage = requests.post(searchUrl, headers=headerValue,
                                  verify=False, cookies=sessionCookies,  stream=True, data=newFacet)
            
            # if success create csv
            if rPage.status_code == 200:
                l2 = rPage.json()  # convert response to json

                # get mainObject with items
                getOrgUnitItems2 = l2.get("mainObject")
                mainItems2 = getOrgUnitItems2.get("items")  # get items
                if not mainItems:
                    pass

                else:
                    # create dataframe to save into csv

                    for x in mainItems2:
                        reliD = x.get('id')
                        # set token autherization
                        newurl2 = baseurl + '/api/v1/referencelinks?sourceIds[]='+reliD + \
                            r'&entityType=Axon\AppBundle\Entity\System&systemIdentifier=Axon&relationshipNames[]=AxonSystemToEICResource'

                        systemR2 = requests.get(newurl2, headers=headerValue,
                                                verify=False, stream=True)
                        if systemR2.status_code == 200:
                            systemL2 = systemR2.json()  # convert response to json

                            results = systemL2.get('results')
                            if not results:
                                pass

                            else:
                                # create dataframe to save into csv
                                for result in results:
                                    link = result.get('links')
                                    if not link:
                                        pass

                                    else:
                                        for item in link:
                                            systemRel.append({
                                                'main_objectIdentifier':  result['objectIdentifier'],
                                                'child_objectIdentifier':  item['objectIdentifier'],
                                                'entityType':  item['entityType'],
                                                'ResourceName':  item['properties']['ResourceName'],
                                            })
                        else:
                            logging.error(f"Resource ID {reliD} pagination failed with status code: {str(systemR.status_code)}")
                            
            limitValue += facetPageLimit
            
        if not systemRel:
            systemRel.append({
                            'main_objectIdentifier':  '',
                            'child_objectIdentifier':  '',
                            'entityType':  '',
                            'ResourceName':  '',
                        })
        
        df = pd.DataFrame(systemRel)  
        df=df.iloc[0:-1]     

        for column in df[0:-1].columns:
            df[column] = df[column].apply(lambda x: BeautifulSoup(x, 'lxml').get_text())
        
            for i in chars_to_remove:
                df = df.applymap(lambda x: x.replace(i, '') if (isinstance(x, str)) else x)
                name = "SYSTEM_x_RESOURCE"
                # save to csv: facetname + current date
                df.to_csv(os.path.join('../AXON/'+name+'.csv'), sep=";", index=False)

    else:
        logging.error(f"System EDC resources failed with status code: {str(systemR.status_code)}")
