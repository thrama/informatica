import os
import logging

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

EDC_headers = {'Content-type': 'application/json',
               'Accept': 'application/json'}

# EDC UI Username Credentials for which the rest query has to be fetched.
# EDC_Auth = (os.getenv('EDC_FE_USER'), os.getenv('EDC_FE_PWD'))
username = os.getenv('EDC_FE_USER')
logging.info(f"La variabile di sistema EDC_FE_USER contiene valore: {username}")

password = os.getenv('EDC_FE_PWD')

EDC_Auth = (username, password)

# Database connection string
db_url = 'host='+os.getenv('EDC_PS_HOST') + \
    ' port=' + os.getenv('EDC_PS_PORT') + \
    ' dbname='+os.getenv('EDC_PS_DB') + \
    ' user='+os.getenv('EDC_PS_USER') + \
    ' password='+os.getenv('EDC_PS_PWD')

# list of all email recivers
# emailReceivers = ['test.infa2022@gmail.com']


# Change the directory where you want your new zip file to be
pathExportZip = ("../../out/")

# Caracter to remove from dataframe
chars_to_remove = ('\n', '\r', '\t', '"', ';',
                   '<p><span style=color: rgb(51, 51, 51) font-size: 16px white-space: nowrap>', '</span><br></p>')

# Pagination size
pageSize = 20000

# Pagination size
pageSizeDD = 100000

# Test local
#val_DGR = '%7B!tag%3Dcom_infa_appmodels_ldm_LDM_0c50f596_ab8b_414c_a7b3_35d07025130d_user_custom_facet%7Dcom.infa.appmodels.ldm.LDM_0c50f596_ab8b_414c_a7b3_35d07025130d%3A%22Yes%22'

val_DGR = os.getenv('EDC_VAL_DGR')
logging.debug(f"La variabile di sistema EDC_VAL_DGR contiene valore: {val_DGR}")

csv_path = r'EDC/'

# EDC Host Details. Expected syntax : http(s)://<host>:<port>

EDC_URL = os.getenv('EDC_FE_URL')
logging.debug(f"La variabile di sistema EDC_FE_URL contiene valore: {EDC_URL}")

# if exist, remove the '/' at the end of the string
if EDC_URL[-1] == '/':
    EDC_URL = EDC_URL.rstrip(EDC_URL[-1])

EDC_URL_REST_2 = EDC_URL + '/access'
url_lookup_childId = EDC_URL + '/access/2/catalog/data/objects/'

EDC_URL_resources = EDC_URL + '/access/1/catalog/resources'

EDC_URL_REST_1 = EDC_URL + '/access/2/catalog/data/search?basicQuery=*&tabId=tab.resources&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22JDBC%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Teradata%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Hive%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22IBM%5C%20DB2%5C%20for%5C%20z%5C%2FOS%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Oracle%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Azure%5C%20Microsoft%5C%20SQL%5C%20Server%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22DataFile%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Microsoft%20SQL%20Server%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22DataFile%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Reference%5C%20resource%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.Resource%22&fq=' + \
    val_DGR + '&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize=' + \
    str(pageSize) + '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'

EDC_URL_REST_1_RELATIONAL = EDC_URL + '/access/2/catalog/data/search?basicQuery=*&tabId=tab.resources&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22JDBC%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Teradata%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Hive%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22IBM%5C%20DB2%5C%20for%5C%20z%5C%2FOS%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Oracle%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Azure%5C%20Microsoft%5C%20SQL%5C%20Server%22&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Microsoft%20SQL%20Server%22&fq=' + \
    val_DGR+'&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize=' + \
    str(pageSize) + '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'

EDC_URL_REST_1_DATAFILE = EDC_URL + '/access/2/catalog/data/search?basicQuery=*&tabId=tab.resources&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22DataFile%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.Resource%22&fq=' + \
    val_DGR+'&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize=50000&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'

EDC_URL_REST_1_REFERENCE = EDC_URL + '/access/2/catalog/data/search?basicQuery=*&tabId=tab.resources&fq=%7B!tag%3Dresource_type%7Dcore.resourceType%3A%22Reference%5C%20resource%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22core.Resource%22&fq=' + \
    val_DGR + '&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize=' + \
    str(pageSize) + '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'

EDC_URL_REST_1_DATADOMAIN = EDC_URL + '/access/2/catalog/data/search?basicQuery=datadomain&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.profiling.DataDomain%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.profiling.DataDomainGroup%22&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize=' + \
    str(pageSize) + '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'

EDC_URL_REST_3 = EDC_URL + '/access/2/catalog/data/search?basicQuery=*&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Table%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.View%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Schema%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Database%22&fq=%7B!tag%3Dresource_name%7Dcore.resourceName%3A%22ssaPY_PY999_DB2_DBR637_AFPY_MULTI%22&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize=' + \
    str(pageSize) + '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'

EDC_URL_REST_3Bis = EDC_URL + '/access/2/catalog/data/search?basicQuery=*&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Table%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.View%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Schema%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Database%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Column%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.ViewColumn%22&fq=core.lastModified%3A%5B2022-02-20T00%3A00%3A00.000Z%20TO%202022-02-21T23%3A59%3A59.999Z%5D&fq=%7B!tag%3Dresource_name%7Dcore.resourceName%3A%22ssaPY_PY999_DB2_DBR637_AFPY_MULTI%22&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize=' + \
    str(pageSize) + '&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'
