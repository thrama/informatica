# EDC AUTOMATIONS

## ABOUT THE PROJECT

To start a new project of Data Governance, this Python script was developed to automate and accelerate common tasks:

- Create new EDC connections
- Create new EDC resources

### BUILT WITH

- [Python 3.x](https://www.python.org/downloads/)

## PREREQUISITES

### PYTHON LIBRARIES

First, install the required libraries:

- [Pyexcel](http://docs.pyexcel.org/en/latest/) - Provides one application programming interface to read, manipulate and write data in various Excel formats.
- [Requests](https://docs.python-requests.org/en/master/) - Allows you to send HTTP/1.1 requests extremely easily.

Installation command:

```sh
$ pip install pyexcel pyexcel-xls pyexcel-xlsx requests
```

#### PROXY CONFIGURATION (if needed)

If you're behind a corporate proxy and encounter connection timeout warnings, export the proxy environment variable:

```sh
$ export https_proxy=http://your-proxy-server:port
```

#### XLRD VERSION

Earlier versions of xlrd do not support .xlsm files. To fix this, install version 1.2.0:

```sh
$ pip uninstall xlrd
$ pip install xlrd==1.2.0
```

### ENV CONFIGURATIONS

If using a Python virtual environment:

```sh
$ cd /path/to/your/python/env
$ source bin/activate
(your-env) [...]$
```

## INSTALLATION

To install the script, copy and unzip the archive file in the correct folder:

```sh
$ unzip Automation.zip
```

### GENERAL USAGE

```sh
usage:
<python> main.py
                -t, --tech <db2|hive|mongo|oracle|sqlsrv|teradata>
                -x, --xls <excel_file>
                [-c, --connections]
                [-r, --resources]
```

Use source Excel file to create JSON files and connections for Informatica service.

```sh
optional arguments:
  -h, --help              show this help message and exit
  -v, --version           show program version
  -t, --tech <technology> technology to use to create the resource
  -x, --xls <excel_file>  Excel file (source)
  -r, --resources         create resources into the Informatica service
  -c, --connections       create connections into the Informatica service
```

### CREATE CONNECTIONS

```sh
<python> main.py --tech <db2|hive|mongo|oracle|sqlsrv|teradata> --xls <excel_file> -c
```

Required parameters:

- `-x, --xls <excel_file>` - Specify the Excel file to read
- `-t, --tech <db2|hive|mongo|oracle|sqlsrv|teradata>` - Define the technology to use
- `-c, --connections` - Create connections

Example:

```sh
$ python main.py -t db2 -x xlsxFile/Test_Template_DB2.xlsx -c
```

The output files are saved in the result folder (see Configuration file). This folder will also contain the ODBC file with configurations that need to be appended to the `$INFA_HOME/ODBC7.1/odbc.ini` file.

### CREATE RESOURCES

```sh
<python> main.py --tech <db2|hive|mongo|oracle|sqlsrv|teradata> --xls <excel_file> -r
```

Required parameters:

- `-x, --xls <excel_file>` - Specify the Excel file to read
- `-t, --tech <db2|hive|mongo|oracle|sqlsrv|teradata>` - Define the technology to use
- `-r, --resources` - Create resources via API requests

The script calls the REST API to create new resources. If it fails, it creates a JSON file in the results folder.

Example:

```sh
$ python main.py -t db2 -x xlsxFile/Test_Template_DB2.xlsx -r
```

## CONFIGURATION FILES

### FILE 'globalparams.py'

The `globalparams.py` file contains environment-specific values (domains, hosts, credentials, etc.).

**IMPORTANT:** It is a best practice to **back up this file before installing a new version** of the script, as it contains your environment-specific configuration.

### FILE 'config.py'

The `config.py` file contains general configuration settings:

- `infaHome` - The same value as the environment variable $INFA_HOME
- `resultFolder` - Directory where results are saved (JSON files, ODBC files, etc.)
- `sheetName` - Name of the Excel sheet to process

## PROJECT STRUCTURE

```
.
├── main.py                 # Main entry point
├── config.py              # General configuration
├── globalparams.py        # Environment-specific parameters
├── connections.py         # Connection management
├── resources.py           # Resource management
├── excel.py               # Excel file handling
├── odbc.py                # ODBC configuration
├── restapicall.py         # REST API calls
├── odbcFile/              # ODBC templates
├── jsonFile/              # JSON templates
├── xlsxFile/              # Input Excel files
└── resultFile/            # Output files

```

## AUTHOR

Lorenzo Lombardi

## LICENSE

This project is provided as-is for educational and professional portfolio purposes.
