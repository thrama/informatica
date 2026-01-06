import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

### Variables ( Not to be Updated) ###
headers = {"Content-Type": "application/json"}


### Parameters ( Should be updated according to the Axon environment) ###
# Axon UI Username Credentials for which the rest query has to be fetched.

username = os.getenv("AXON_FE_USER")
password = os.getenv("AXON_FE_PWD")

# Axon Host Details. Expected syntax : http(s)://<host>:<port> , Login to the Informatica Axon URL for checking the Host and port

baseurl = os.getenv("AXON_FE_URL")
searchUrl = f"{os.getenv('AXON_FE_URL')}/unison/v2/facet/_search"

# Change the directory where you want your new zip file to be
pathExportZip = "../../out/"

# Build connection URL using f-string (Python 3.6+)
db_url = (
    f"host={os.getenv('AXON_PS_HOST')} "
    f"port={os.getenv('AXON_PS_PORT')} "
    f"dbname={os.getenv('AXON_PS_DB')} "
    f"user={os.getenv('AXON_PS_USER')} "
    f"password={os.getenv('AXON_PS_PWD')}"
)

facetPageLimit = 100000
relationsPageLimit = 100000

# Caracter to remove from dataframe
chars_to_remove = ("\n", "\r", "\t", '"', ";")
