import os

# GENERAL CONFS
#infaHome = "/informatica/edc/10.4.1"
infaHome = os.getenv('INFA_HOME')
resultFolder="resultFile"
sheetName="Sheet1"

### ODBC
# ODBC templates
odbcTemplateSQLSrvSections="odbcFile/Template_ODBC_SQLSrv_sections.txt"
odbcTemplateSQLSrvHeads="odbcFile/Template_ODBC_SQLSrv_heads.txt"
odbcTemplateTeradataSections="odbcFile/Template_ODBC_Teradata_sections.txt"
odbcTemplateTeradataHeads="odbcFile/Template_ODBC_Teradata_heads.txt"
# ODBC out files
odbcOutSRVSQLSections="sqlsrv_odbc_sections.txt"
odbcOutSRVSQLHeads="sqlsrv_odbc_heads.txt"
odbcOutTeradataSections="teradata_odbc_sections.txt"
odbcOutTeradataHeads="teradata_odbc_heads.txt"

### JSON
jsonTemplDB2="jsonFile/Template_DB2zos.json"
jsonTemplSQLSRV="jsonFile/Template_SQLServer.json"
jsonTemplTeradata="jsonFile/Template_Teradata.json"
jsonTemplHive="jsonFile/Template_Hive.json"
jsonTemplOracle="jsonFile/Template_Oracle.json"