from db.database import axon_with_relations, dbGeneral
from facetOptionsWithRel import facets
from props.paramsAxon import chars_to_remove, facetPageLimit, relationsPageLimit
from props.utils import datetime, dt_string, json, logging, os, pd, requests, time

gerenal_time = time.time()

# Get facet items and save to CSV & Database
totalHitsRelated = {}


def createDir():
    # check if has directory, if not create..
    if not os.path.exists("../AXON/"):
        os.makedirs("../AXON/")


def relationFacets(baseurl, infaTokenValue, headerValue, sessionCookies):
    totalFacet = 0  # total number of facets to be saved into database
    createDir()

    # foreach facet in facetOptions make POST request and save csv
    for facet in facets:
        exportedItems = []
        name = facet.get("mainFacet")  # get facet name

        logging.info(f"Working on facets: {name}")
        logging.debug(f"Facet: {facet}")

        facetLimitMain = str(facetPageLimit)
        facetLimitRel = str(relationsPageLimit)
        facetLimitRelSec = str(relationsPageLimit)

        # set token autherization
        headerValue = {"Authorization": infaTokenValue, "Content-Type": "application/json"}
        # convert facet body POST into json
        bodyData = json.dumps(facet)

        # send request with authorization and body data
        r = requests.post(
            baseurl, headers=headerValue, cookies=sessionCookies, stream=True, data=bodyData
        )
        # db data to be saved
        starting_time = datetime.now()
        downloaded = False
        # server response time converted in seconds
        response_time = str(r.elapsed.total_seconds()) + " s"
        # server response sice converted in kb
        response_size = str(len(r.content) / 1024) + " kb"
        response_code = r.status_code  # server status code
        # end db data

        # if success create csv
        if r.status_code == 200:
            l = r.json()  # convert response to json

            getOrgUnitItems = l.get("mainObject")  # get mainObject with items

            # get relatedObjects with items
            getRelatedItems = l.get("relatedObjects")
            mainItems = getOrgUnitItems.get("items")  # get items

            totalHitsMain = getOrgUnitItems["totalHits"]
            totalHitsRel = getRelatedItems[0]["totalHits"]
            relName = getRelatedItems[0]["facetId"]

            totalFacet = totalFacet + 1  # increment total facets number for general table databse

            limitValueMain = int(facetLimitMain)
            limitValueRel = int(facetLimitRel)
            limitValueRelSec = int(facetLimitRelSec)

            exportRel = createArray(name, relName, mainItems, getRelatedItems, exportedItems)

            while totalHitsRel > limitValueRel:
                logging.debug(f"Running relation {name}_x_{relName} -> {limitValueRel}")

                offsetVal = int(limitValueRel)
                relFacet = facet
                relFacet["searchScopes"]["relationships"][0]["properties"]["offset"] = offsetVal

                newFacet = json.dumps(relFacet)

                r2 = requests.post(
                    baseurl, headers=headerValue, cookies=sessionCookies, stream=True, data=newFacet
                )

                # if success create csv
                if r2.status_code == 200:
                    json_resp = r2.json()  # convert response to json
                    # get mainObject with items
                    mainObject2 = json_resp.get("mainObject")
                    # get relatedObjects with items
                    relatedObjects2 = json_resp.get("relatedObjects")
                    offsetItems = mainObject2.get("items")  # get items

                    exportRel = createArray(name, relName, offsetItems, relatedObjects2, exportedItems)

                limitValueRel += relationsPageLimit

            while totalHitsMain > limitValueMain:
                offsetValMain = int(limitValueMain)
                newMainFacet = facet
                newMainFacet["searchScopes"]["mainFacet"]["properties"]["offset"] = offsetValMain
                newMainFacet["searchScopes"]["relationships"][0]["properties"]["offset"] = 0
                # convert facet body POST into json
                bodyData2 = json.dumps(newMainFacet)
                # send request with authorization and body data
                rMain = requests.post(
                    baseurl, headers=headerValue, cookies=sessionCookies, stream=True, data=bodyData2
                )

                # if success create csv
                if rMain.status_code == 200:
                    l3 = rMain.json()  # convert response to json

                    # get mainObject with items
                    getOrgUnitItems2 = l3.get("mainObject")

                    # get relatedObjects with items
                    getRelatedItems2 = l3.get("relatedObjects")
                    mainItems3 = getOrgUnitItems2.get("items")  # get items

                    exportRel = createArray(name, relName, mainItems3, getRelatedItems2, exportedItems)

                    totalHitsRelSec = getRelatedItems2[0]["totalHits"]
                    limitValueRelSec = relationsPageLimit

                    while totalHitsRelSec > limitValueRelSec:
                        offsetVal2 = int(limitValueRelSec)
                        newRelFacet = facet
                        newRelFacet["searchScopes"]["relationships"][0]["properties"]["offset"] = offsetVal2

                        newFacetRel = json.dumps(newRelFacet)

                        r4 = requests.post(
                            baseurl,
                            headers=headerValue,
                            cookies=sessionCookies,
                            stream=True,
                            data=newFacetRel,
                        )

                        # if success create csv
                        if r4.status_code == 200:
                            json_resp4 = r4.json()  # convert response to json
                            # get mainObject with items
                            mainObject4 = json_resp4.get("mainObject")
                            # get relatedObjects with items
                            relatedObjects3 = json_resp4.get("relatedObjects")
                            offsetItems3 = mainObject4.get("items")  # get items

                            exportRel = createArray(name, relName, offsetItems3, relatedObjects3, exportedItems)

                        limitValueRelSec += relationsPageLimit

                else:
                    logging.error(f"{name} failed with status code {str(r.status_code)}")

                limitValueMain += facetPageLimit

            logging.debug(f"relName: {relName}")

            if not exportRel:
                if relName == "ROLE":
                    exportRel.append(
                        {
                            "main_id": "",
                            "name": "",
                            "roleId": "",
                            "roleName": "",
                            "roleTypeId": "",
                            "roleTypeName": "",
                            "peopleId": "",
                            "roleAccepted": "",
                            "dateAccepted": "",
                        }
                    )
                elif relName == "FIELD":
                    exportRel.append(
                        {
                            "main_id": "",
                            "name": "",
                            "child_id": "",
                            "objectId": "",
                            "objectName": "",
                        }
                    )
                else:
                    exportRel.append(
                        {
                            "main_id": "",
                            "name": "",
                            "child_id": "",
                            "relTypeId": "",
                            "relTypeName": "",
                        }
                    )

            df = pd.DataFrame(exportRel)
            df = df.iloc[0:-1]

            for i in chars_to_remove:
                df = df.applymap(lambda x: x.replace(i, "") if (isinstance(x, str)) else x)
                df.to_csv(os.path.join(f"../AXON/{name}_x_{relName}.csv"), sep=";", index=False)

            # set download true for this facet into facet table database
            downloaded = True

        else:
            logging.error(f"{name} failed with status code {str(r.status_code)}")

        ending_time = datetime.now()  # execution script code time

        # save facet data into facet table database
        axon_with_relations(
            str(f"{name}_x_{relName}"),
            response_code,
            response_size,
            response_time,
            downloaded,
            starting_time,
            ending_time,
        )

    # save total facets data into general table database
    dbGeneral(dt_string, totalFacet, 0, (time.time() - gerenal_time))


def createArray(name, relName, mainItems, getRelatedItems, exportedItems):
    if mainItems is None:
        pass

    else:
        for x in mainItems:
            values = x.get("values")
            rel = x.get("relationships")

            if not rel:
                pass

            else:
                for y in rel:
                    relation = y.get("relationships")
                    for val in relation:
                        # if the field with the relation direction exist and it is
                        # equal to INBOUND, it will jump to the next item in the loop...
                        if "relDirection" in val and val["relDirection"] == "INBOUND":
                            logging.debug(
                                f"Relation with ID {val['id']} and direction {val['relDirection']} is skypped."
                            )
                            continue

                        valRelId = val["id"]
                        if "relTypeId" not in val:
                            valReltype = "-1"
                        else:
                            valReltype = val["relTypeId"]

                        for relItems in getRelatedItems:
                            if relItems["facetId"] == relName:
                                relItem = relItems.get("items")
                                if not relItem:
                                    pass
                                else:
                                    for x in relItem:
                                        if x["id"] == valRelId:
                                            relVals = x.get("values")

                                            if relName == "ROLE":
                                                str_datetime = str(relVals[7])
                                                val_date_str = str_datetime[0:10]
                                                exportedItems.append(
                                                    {
                                                        "main_id": values[0],
                                                        "name": values[1],
                                                        "roleId": relVals[1],
                                                        "roleName": relVals[2],
                                                        "roleTypeId": relVals[3],
                                                        "roleTypeName": relVals[4],
                                                        "peopleId": relVals[5],
                                                        "roleAccepted": relVals[6],
                                                        "dateAccepted": val_date_str,
                                                    }
                                                )

                                            elif relName == "FIELD":
                                                exportedItems.append(
                                                    {
                                                        "main_id": values[0],
                                                        "name": values[1],
                                                        "child_id": relVals[0],
                                                        "objectId": relVals[1],
                                                        "objectName": relVals[2],
                                                    }
                                                )

                                            else:
                                                exportedItems.append(
                                                    {
                                                        "main_id": values[0],
                                                        "name": values[1],
                                                        "child_id": valRelId,
                                                        "relTypeId": valReltype,
                                                        "relTypeName": name + "-" + relName,
                                                    }
                                                )
    return exportedItems
