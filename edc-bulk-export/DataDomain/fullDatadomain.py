from db.database import all_edc
from props.paramsEdc import (
    EDC_URL,
    EDC_URL_REST_1_DATADOMAIN,
    EDC_URL_REST_2,
    EDC_Auth,
    EDC_headers,
    chars_to_remove,
    pageSizeDD,
)
from props.utils import BeautifulSoup, HTTPAdapter, Retry, datetime, logging, os, pd, requests

session = requests.Session()
retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)

# empty array
csvDataDomainGroup = []
csvDataDomainGroup_X_DataDomain = []
csvDataDomain = []
dataDomainNames = []
csvDataDomain_X_Column = []


# post api with raw data & get response and add to csv
# Function get customDatadomainFile resources, do pagination and generate csv to export
def customDatadomainFile():
    downloaded = 0
    if not os.path.exists("EDC"):
        os.makedirs("EDC")
    # print("Generating RDBMS RESOURCES ....")
    pageSeizeOffset = pageSizeDD
    resp1 = requests.get(EDC_URL_REST_1_DATADOMAIN, headers=EDC_headers, auth=EDC_Auth)
    # db data to be saved
    starting_time = datetime.now()
    # server response time converted in seconds
    response_time = str(resp1.elapsed.total_seconds()) + " s"
    # server response sice converted in kb
    response_size = str(len(resp1.content) / 1024) + " kb"
    response_code = resp1.status_code  # server status code
    # end db data

    if resp1.status_code == 200:
        j_resp_1req = resp1.json()
        hits = j_resp_1req.get("hits")
        totalPage = j_resp_1req["metadata"]["totalCount"]
        newTotal = totalPage + pageSizeDD
        generateCSV(hits, EDC_headers, EDC_Auth)
        if newTotal > pageSeizeOffset:
            while totalPage > pageSeizeOffset:
                # print("Pagination Datadomain RESOURCES: Offset items: -- ",
                #       pageSeizeOffset)
                print("Pagination Datadomain RESOURCES: Offset items: -- ", pageSeizeOffset)
                offsetUrl = offsetUrl = (
                    "/access/2/catalog/data/search?basicQuery=datadomain&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.profiling.DataDomain%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.profiling.DataDomainGroup%22&facet=false&defaultFacets=true&highlight=false&offset="
                    + str(pageSeizeOffset)
                    + "&pageSize="
                    + str(pageSizeDD)
                    + "&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted"
                )
                newUrlMain = EDC_URL + offsetUrl

                respWhile = requests.get(newUrlMain, headers=EDC_headers, auth=EDC_Auth)
                if respWhile.status_code == 200:
                    respWhileData = respWhile.json()
                    hits = respWhileData.get("hits")
                    generateCSV(hits, EDC_headers, EDC_Auth)
                else:
                    logging.error(f"Error pagination on offset: {pageSeizeOffset}")
                pageSeizeOffset += pageSizeDD

        try:
            datacolumnSCV()
        except Exception as e:
            logging.error(f"error in datacolums: {e}")
            return e

        # Generate csv files csvDataDomainGroup
        if csvDataDomainGroup:
            df = pd.DataFrame(csvDataDomainGroup)
            df = df.fillna("")
            for column in df.columns:
                df[column] = df[column].apply(lambda x: BeautifulSoup(x, "lxml").get_text())
                for i in chars_to_remove:
                    df = df.applymap(lambda x: x.replace(i, "") if (isinstance(x, str)) else x)
            df.to_csv(os.path.join("EDC/DATADOMAINGROUPS.csv"), sep=";", index=False)
            downloaded = downloaded + 1

        # Generate csv files csvDataDomainGroup_X_DataDomain
        if csvDataDomainGroup_X_DataDomain:
            df = pd.DataFrame(csvDataDomainGroup_X_DataDomain)
            # df.drop_duplicates (inplace=True)
            df.to_csv(os.path.join("EDC/DATADOMAINGROUPS_x_DATADOMAIN.csv"), sep=";", index=False)
            downloaded = downloaded + 1

        # Generate csv files csvDataDomain
        if csvDataDomain:
            df = pd.DataFrame(csvDataDomain)
            df = df.fillna("")
            for column in df.columns:
                df[column] = df[column].apply(lambda x: BeautifulSoup(x, "lxml").get_text())
                for i in chars_to_remove:
                    df = df.applymap(lambda x: x.replace(i, "") if (isinstance(x, str)) else x)
            df.to_csv(os.path.join("EDC/DATADOMAINS.csv"), sep=";", index=False)
            downloaded = downloaded + 1

        # Generate csv files csvDataDomain_X_Column
        if csvDataDomain_X_Column:
            df = pd.DataFrame(csvDataDomain_X_Column)
            # df.drop_duplicates (inplace=True)
            df.to_csv(os.path.join("EDC/DATADOMAIN_x_COLUMN.csv"), sep=";", index=False)
            downloaded = downloaded + 1

        if not csvDataDomainGroup:
            csvDataDomainGroup.append(
                {
                    "id": "",
                    "Name": "",
                    "Last Modified Time": "",
                    "Data Domain Type": "",
                    "Data Domain Type modifiedBy": "",
                    "Frequency": "",
                    "Frequency modifiedBy": "",
                    "GDPR Data Processing note": "",
                    "GDPR Data Processing note modifiedby": "",
                    "Data User Classification": "",
                    "Data User Classification modifiedBy": "",
                    "Ownership link": "",
                    "Ownership link modifiedBy": "",
                    "Business Description": "",
                    "Business Description modifiedBy": "",
                    "Data Domain Last Modified Time": "",
                }
            )
            df = pd.DataFrame(csvDataDomainGroup)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join("EDC/DATADOMAINGROUPS.csv"), sep=";", index=False, header=True)

        if not csvDataDomainGroup_X_DataDomain:
            csvDataDomainGroup_X_DataDomain.append({"id": "", "Name": "", "DataDomain id": ""})
            df = pd.DataFrame(csvDataDomainGroup_X_DataDomain)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join("EDC/DATADOMAINGROUPS_x_DATADOMAIN.csv"), sep=";", index=False, header=True)

        if not csvDataDomain_X_Column:
            csvDataDomain_X_Column.append({"id": "", "Name": "", "Column id": ""})
            df = pd.DataFrame(csvDataDomain_X_Column)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join("EDC/DATADOMAIN_x_COLUMN.csv"), sep=";", index=False, header=True)

        if not csvDataDomain:
            csvDataDomain.append(
                {
                    "id": "",
                    "Name": "",
                    "Last Modified Time": "",
                    "Data Domain Type": "",
                    "Data Domain Type modifiedBy": "",
                    "GDPR Data Processing note": "",
                    "GDPR Data Processing note modifiedby": "",
                    "Business Description": "",
                    "Business Description modifiedBy": "",
                    "Data Domain Last Modified Time": "",
                }
            )
            df = pd.DataFrame(csvDataDomain)
            df = df.iloc[0:-1]
            df.to_csv(os.path.join("EDC/DATADOMAINS.csv"), sep=";", index=False, header=True)

    else:
        logging.error(f"Main EDC failed with status code: {str(resp1.status_code)}")

    ending_time = datetime.now()  # execution script code time
    resourceName = "DataDomain"
    resourceType = "Standard"
    # db data to be saved
    all_edc(
        resourceName, resourceType, downloaded, response_code, response_size, response_time, starting_time, ending_time
    )

    return downloaded


def generateCSV(hits, EDC_headers, EDC_Auth):
    for val in hits:
        if not val:
            pass
        else:
            valHref = val["href"]
            valHits = val["values"]
            for v in valHits:
                if v["attributeId"] == "core.classType" and v["value"] == "com.infa.ldm.profiling.DataDomainGroup":
                    dataDomainGroupUrl = EDC_URL_REST_2 + valHref
                    dataDomainGroupReq = session.get(dataDomainGroupUrl, headers=EDC_headers, auth=EDC_Auth)

                    if dataDomainGroupReq.status_code == 200:
                        if not dataDomainGroupReq.content:
                            pass
                        else:
                            dataDomainGroupRes = dataDomainGroupReq.json()
                            genDatadomainGroup(dataDomainGroupRes)

                if v["attributeId"] == "core.classType" and v["value"] == "com.infa.ldm.profiling.DataDomain":
                    dataDomainURL = EDC_URL_REST_2 + valHref
                    dataDomainReq = session.get(dataDomainURL, headers=EDC_headers, auth=EDC_Auth)

                    if dataDomainReq.status_code == 200:
                        if not dataDomainReq.content:
                            pass
                        else:
                            dataDomainRes = dataDomainReq.json()
                            genDataDomainCSVs(dataDomainRes)

                    else:
                        logging.error(f"Error on DataDomain: {dataDomainReq.status_code}")


# Function generating Database attributs
def genDatadomainGroup(dataDomainGroup):
    finalId = ""
    DDG_name = ""
    DDG_lastModified = ""
    DDG_DataDomainType = ""
    DDG_DataDomainTypeModifiedBy = ""
    DDG_Frequency = ""
    DDG_FrequencyModifiedBy = ""
    DDG_gdprDataProc = ""
    DDG_gdprDataProcModifiedBy = ""
    DDG_DataUserClassification = ""
    DDG_DataUserClassificationModifiedBy = ""
    DDG_OwnershipLink = ""
    DDG_OwnershipLinkModifiedBy = ""
    DDG_businessDescription = ""
    DDG_businessDescriptionModifiedBy = ""
    DDG_LastModifiedTime = ""

    finalId = dataDomainGroup["id"]
    factsDDG = dataDomainGroup["facts"]
    srcLinksDDG = dataDomainGroup["srcLinks"]
    for val in factsDDG:
        if val.get("attributeId") == "core.name":
            DDG_name = val.get("value")
        if val.get("attributeId") == "core.lastModified":
            DDG_lastModified = val.get("value")
        if val.get("label") == "Data Domain Type":
            DDG_DataDomainType = val.get("value")
        if val.get("label") == "Data Domain Type":
            DDG_DataDomainTypeModifiedBy = val.get("modifiedBy")
        if val.get("label") == "Frequency":
            DDG_Frequency = val.get("value")
        if val.get("label") == "Frequency":
            DDG_FrequencyModifiedBy = val.get("modifiedBy")
        if val.get("label") == "GDPR Data Processing note":
            DDG_gdprDataProc = val.get("value")
        if val.get("label") == "GDPR Data Processing note":
            DDG_gdprDataProcModifiedBy = val.get("modifiedBy")
        if val.get("label") == "Data User Classification":
            DDG_DataUserClassification = val.get("value")
        if val.get("label") == "Data User Classification":
            DDG_DataUserClassificationModifiedBy = val.get("modifiedBy")
        if val.get("label") == "Ownership link":
            DDG_OwnershipLink = val.get("value")
        if val.get("label") == "Ownership link":
            DDG_OwnershipLinkModifiedBy = val.get("modifiedBy")
        if val.get("label") == "Business Description":
            DDG_businessDescription = val.get("value")
        if val.get("label") == "Business Description":
            DDG_businessDescriptionModifiedBy = val.get("modifiedBy")
        if val.get("attributeId") == "com.infa.ldm.profiling.dataDomainLastModifiedTime":
            DDG_LastModifiedTime = val.get("value")

    csvDataDomainGroup.append(
        {
            "id": finalId,
            "Name": DDG_name,
            "Last Modified Time": DDG_lastModified,
            "Data Domain Type": DDG_DataDomainType,
            "Data Domain Type modifiedBy": DDG_DataDomainTypeModifiedBy,
            "Frequency": DDG_Frequency,
            "Frequency modifiedBy": DDG_FrequencyModifiedBy,
            "GDPR Data Processing note": DDG_gdprDataProc,
            "GDPR Data Processing note modifiedby": DDG_gdprDataProcModifiedBy,
            "Data User Classification": DDG_DataUserClassification,
            "Data User Classification modifiedBy": DDG_DataUserClassificationModifiedBy,
            "Ownership link": DDG_OwnershipLink,
            "Ownership link modifiedBy": DDG_OwnershipLinkModifiedBy,
            "Business Description": DDG_businessDescription,
            "Business Description modifiedBy": DDG_businessDescriptionModifiedBy,
            "Data Domain Last Modified Time": DDG_LastModifiedTime,
        }
    )

    for val in srcLinksDDG:
        if val["association"] == "com.infa.ldm.profiling.DataDomain":
            csvDataDomainGroup_X_DataDomain.append({"id": finalId, "Name": DDG_name, "DataDomain id": val["id"]})


def genDataDomainCSVs(dataDomainRes):
    DD_name = ""
    DD_lastModified = ""
    DD_DataDomainType = ""
    DD_DataDomainTypeModifiedBy = ""
    DD_gdprDataProc = ""
    DD_gdprDataProcModifiedBy = ""
    DD_businessDescription = ""
    DD_businessDescriptionModifiedBy = ""
    DD_LastModifiedTime = ""

    finalId = dataDomainRes["id"]
    factsDD = dataDomainRes["facts"]
    for val in factsDD:
        if val.get("attributeId") == "core.name":
            DD_name = val.get("value")
        if val.get("attributeId") == "core.lastModified":
            DD_lastModified = val.get("value")
        if val.get("label") == "Data Domain Type":
            DD_DataDomainType = val.get("value")
        if val.get("label") == "Data Domain Type":
            DD_DataDomainTypeModifiedBy = val.get("modifiedBy")
        if val.get("label") == "GDPR Data Processing note":
            DD_gdprDataProc = val.get("value")
        if val.get("label") == "GDPR Data Processing note":
            DD_gdprDataProcModifiedBy = val.get("modifiedBy")
        if val.get("label") == "Business Description":
            DD_businessDescription = val.get("value")
        if val.get("label") == "Business Description":
            DD_businessDescriptionModifiedBy = val.get("modifiedBy")
        if val.get("attributeId") == "com.infa.ldm.profiling.dataDomainLastModifiedTime":
            DD_LastModifiedTime = val.get("value")

    csvDataDomain.append(
        {
            "id": finalId,
            "Name": DD_name,
            "Last Modified Time": DD_lastModified,
            "Data Domain Type": DD_DataDomainType,
            "Data Domain Type modifiedBy": DD_DataDomainTypeModifiedBy,
            "GDPR Data Processing note": DD_gdprDataProc,
            "GDPR Data Processing note modifiedby": DD_gdprDataProcModifiedBy,
            "Business Description": DD_businessDescription,
            "Business Description modifiedBy": DD_businessDescriptionModifiedBy,
            "Data Domain Last Modified Time": DD_LastModifiedTime,
        }
    )
    dataDomainNames.append({finalId: DD_name})


# Function generating Columns attributs
def datacolumnSCV():
    for val in dataDomainNames:
        # print("DEBUG val -->",val)
        for finalId, val2 in val.items():
            # if finalId == 'DataDomain://PROFITABILITY_GIORNALIERA_Totale' :
            dataColumnUrl = (
                EDC_URL_REST_2
                + "/1/catalog/data/search?q=(com.infa.ldm.profiling.dataDomainsAccepted:"
                + val2
                + "%20AND%20core.name:*)&qf=com.infa.ldm.profiling.dataDomainsAccepted&fq=com.infa.ldm.profiling.dataDomainsAccepted:"
                + val2
                + "&related=false&includeRefObjects=false&offset=0&pageSize=1"
            )
            dataColumnRes = ""
            # hits = ""
            totalPage = ""

            dataColumnReq = session.get(dataColumnUrl, headers=EDC_headers, auth=EDC_Auth)
            if dataColumnReq.status_code == 200:
                if not dataColumnReq.content:
                    logging.error(f"no datacolumn response for: {val2}")
                    pass
                else:
                    dataColumnRes = dataColumnReq.json()
                    totalPage = dataColumnRes["totalCount"]
                    # Update del 06/12/2022
                    pageSizeColOffset = 0
                    # print("DEBUG finalId -->",finalId)
                    # print("DEBUG totalPage -->",totalPage)
                    while totalPage > pageSizeColOffset:
                        # print("DEBUG val2 -->",val2)
                        # print("DEBUG pageSizeColOffset -->",pageSizeColOffset)
                        newUrlMain = (
                            EDC_URL_REST_2
                            + "/1/catalog/data/search?q=(com.infa.ldm.profiling.dataDomainsAccepted:"
                            + val2
                            + "%20AND%20core.name:*)&qf=com.infa.ldm.profiling.dataDomainsAccepted&fq=com.infa.ldm.profiling.dataDomainsAccepted:"
                            + val2
                            + "&related=false&includeRefObjects=false&offset="
                            + str(pageSizeColOffset)
                            + "&pageSize="
                            + str(pageSizeDD)
                        )
                        # print("DEBUG newUrlMain.status_code -->",newUrlMain)

                        respWhile = requests.get(newUrlMain, headers=EDC_headers, auth=EDC_Auth)
                        # print("DEBUG respWhile.status_code -->",respWhile.status_code)
                        if respWhile.status_code == 200:
                            respWhileData = respWhile.json()
                            colHits = respWhileData["items"]
                            genDataColumnCSVs(colHits, finalId, val2)
                        else:
                            logging.error(f"Error pagination on offset: {pageSizeColOffset}")
                        # Update del 22/12/2022
                        pageSizeColOffset += pageSizeDD
            else:
                logging.error(f"Error on DataColumn: {dataColumnReq.status_code}")


def genDataColumnCSVs(colhits, colfinalId, colval2):
    # print("DEBUG Running genDataColumnCSVs")
    Cl_resourceName = ""
    val = ""
    valHits = ""
    childId = ""
    # print("DEBUG *************** genDataColumnCSVs ******************")
    for val in colhits:
        if val not in colhits:
            pass
        else:
            childId = val["id"]
            valHits = val["values"]
            loop = 0
            for v in valHits:
                if v.get("id") == "core.name":
                    Cl_resourceName = v.get("value")
                    # print("DEBUG Name -->",Cl_resourceName)
                if loop == 0:
                    if v.get("id") == "com.infa.ldm.profiling.dataDomainsAccepted" and v.get("value") == colval2:
                        csvDataDomain_X_Column.append({"id": colfinalId, "Name": Cl_resourceName, "Column id": childId})
                        # print("DEBUG v -->",v)
                        # print("DEBUG id -->",colfinalId)
                        # print("DEBUG Column id -->",childId)
                        loop = 1


def mainDatadomain():
    try:
        return customDatadomainFile()
    except Exception as e:
        return e
