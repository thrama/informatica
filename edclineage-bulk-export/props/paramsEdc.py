import os
import logging

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Pagination size
pageSize = 10000 

lineageDomain = 'DD_for_Lineage'

basicQueryFilter = '_Totale'

#ambienteFilter = '%7B!tag%3Dcom_infa_appmodels_ldm_LDM_1be8505e_ea8c_42d4_98c9_9387837dce4e_user_custom_facet%7Dcom.infa.appmodels.ldm.LDM_1be8505e_ea8c_42d4_98c9_9387837dce4e%3A%22DDU%22'
ambienteFilter = os.getenv('EDC_ENV_FLTR')


# EDC Host Details. Expected syntax : http(s)://<host>:<port>
EDC_URL = os.getenv('EDC_FE_URL')
logging.debug(f"La variabile di sistema EDC_FE_URL contiene valore: {EDC_URL}")

# if exist, remove the '/' at the end of the string
if EDC_URL[-1] == '/':
    EDC_URL = EDC_URL.rstrip(EDC_URL[-1])

# EDC_URL_REST_1_LINEAGE = EDC_URL + '/access/2/catalog/data/search?basicQuery=' + lineageDomain + '&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.Column%22&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.relational.ViewColumn%22&facet=false&defaultFacets=true&highlight=false&offset=0&pageSize=' + \
#     str(pageSize)+'&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'

LINEAGE_REST_1 = EDC_URL + '/access/2/catalog/data/search?basicQuery=*' + basicQueryFilter + '&tabId=all&fq=%7B!tag%3Dall_class_type%7Dcore.allclassTypes%3A%22com.infa.ldm.profiling.DataDomain%22&fq=%7B!tag%3Dresource_name%7Dcore.resourceName%3A%22DataDomain%22&fq=' + \
    ambienteFilter + '&facet=true&defaultFacets=true&highlight=false&offset=0&pageSize=' + \
    str(pageSize)+'&includeRefObjects=true&fq=-com.infa.ldm.axon.status:Deleted'


EDC_URL_REST_2 = EDC_URL + '/access'

EDC_headers = {'Content-type': 'application/json',
               'Accept': 'application/json'}

# EDC UI Username Credentials for which the rest query has to be fetched.
# EDC_Auth = (os.getenv('EDC_FE_USER'), os.getenv('EDC_FE_PWD'))
username = os.getenv('EDC_FE_USER')
password = os.getenv('EDC_FE_PWD')

EDC_Auth = (username, password)


# Database connection string
db_url = 'host='+os.getenv('EDC_PS_HOST') + \
    ' port=' + os.getenv('EDC_PS_PORT') + \
    ' dbname='+os.getenv('EDC_PS_DB') + \
    ' user='+os.getenv('EDC_PS_USER') + \
    ' password='+os.getenv('EDC_PS_PWD')
    
# list of all email recivers
emailReceivers = ['fvolpe@informatica.com',
                  'llombardi@informatica.com']

# Change the directory where you want your new zip file to be
pathExportZip = ("../../out/")

# Caracter to remove from dataframe
chars_to_remove = ('\n', '\r', '\t', '"', ';',
                   '<p><span style=color: rgb(51, 51, 51) font-size: 16px white-space: nowrap>', '</span><br></p>')

