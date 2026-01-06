###
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama
#
# DESCRIPTION:
# Configuration file for EDC automation scripts.
# Defines file paths, templates, and general settings.
###

import os

# =============================================================================
# GENERAL CONFIGURATIONS
# =============================================================================

# Informatica home directory
# Option 1: Use environment variable (recommended)
infaHome = os.getenv("INFA_HOME", "/opt/informatica/edc/10.5.0")

# Option 2: Hardcoded path (update based on your installation)
# infaHome = "/opt/informatica/edc/10.5.0"

# Output folder for generated files (JSON, ODBC configs, etc.)
resultFolder = "resultFile"

# Default Excel sheet name to process
sheetName = "Sheet1"

# =============================================================================
# ODBC CONFIGURATION FILES
# =============================================================================

# ODBC Template Files (input)
# These templates are used to generate ODBC connection configurations

# SQL Server ODBC templates
odbcTemplateSQLSrvSections = "odbcFile/Template_ODBC_SQLSrv_sections.txt"
odbcTemplateSQLSrvHeads = "odbcFile/Template_ODBC_SQLSrv_heads.txt"

# Teradata ODBC templates
odbcTemplateTeradataSections = "odbcFile/Template_ODBC_Teradata_sections.txt"
odbcTemplateTeradataHeads = "odbcFile/Template_ODBC_Teradata_heads.txt"

# ODBC Output Files
# Generated ODBC configurations to be merged into $INFA_HOME/ODBC7.1/odbc.ini

odbcOutSRVSQLSections = "sqlsrv_odbc_sections.txt"
odbcOutSRVSQLHeads = "sqlsrv_odbc_heads.txt"
odbcOutTeradataSections = "teradata_odbc_sections.txt"
odbcOutTeradataHeads = "teradata_odbc_heads.txt"

# =============================================================================
# JSON TEMPLATE FILES
# =============================================================================

# EDC Resource JSON templates for different database technologies
# These templates define the structure for creating EDC resources via API

jsonTemplDB2 = "jsonFile/Template_DB2zos.json"  # IBM DB2 z/OS
jsonTemplSQLSRV = "jsonFile/Template_SQLServer.json"  # Microsoft SQL Server
jsonTemplTeradata = "jsonFile/Template_Teradata.json"  # Teradata
jsonTemplHive = "jsonFile/Template_Hive.json"  # Apache Hive
jsonTemplOracle = "jsonFile/Template_Oracle.json"  # Oracle Database

# =============================================================================
# CONFIGURATION NOTES
# =============================================================================
#
# Directory Structure:
# ├── edc-automation/
# │   ├── config.py (this file)
# │   ├── globalparams.py
# │   ├── main.py
# │   ├── odbcFile/          # ODBC templates
# │   ├── jsonFile/          # JSON templates
# │   └── resultFile/        # Output directory (auto-created)
#
# Template Files:
# - ODBC templates: Define connection string formats
# - JSON templates: Define EDC resource structure
# - Both are parameterized and populated from Excel input
#
# Output Files:
# - All generated files are written to resultFolder
# - ODBC files must be manually merged into odbc.ini
# - JSON files can be used for manual import or API validation
#
# =============================================================================
