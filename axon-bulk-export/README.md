# AXON BULK EXPORT

## ABOUT THE PROJECT
To start a new project on Data Governance, we developed a (Python) script to export data from Informatica Axon.

## PREREQUISITES

### PYTHON VERSION
The script has been written and tested with: [Pyhotn 3.6.8](https://www.python.org/downloads/)

### PYTHON LIBRARIES
As a prerequisite, you need to install the libraries below:
- altgraph==0.17.2
- beautifulsoup4==4.11.1
- bs4==0.0.1
- certifi==2021.10.8
- charset-normalizer==2.0.12
- ez-setup==0.9
- idna==3.3
- importlib-metadata==4.8.3
- lxml==4.8.0
- numpy==1.19.5
- pandas==1.1.5
- psycopg2-binary==2.9.3
- pyinstaller==4.10
- pyinstaller-hooks-contrib==2022.0
- python-dateutil==2.8.2
- python-dotenv==0.20.0
- pytz==2022.1
- PyYAML==6.0
- requests==2.27.1
- six==1.16.0
- soupsieve==2.3.2.post1
- typing_extensions==4.1.1
- urllib3==1.26.9
- zipp==3.6.0

## INSTALLATION

### CREATE OF THE EXECUTABLE
To run the script in the customer environment, you must create the executable with [PyInstaller 4.10](https://pyinstaller.org/en/stable/).

The command to create the executable is:
```sh
$ pyinstaller -D --noconfirm [--log-level=WARN] --distpath <dir> <script name>
```

In the specific case of the Axon script is:
```sh
$ pyinstaller -D --noconfirm --distpath bin/ scripts/runAxon.py
```
This command will create the executable under the folder `bin/`.

### GENERAL USAGE OF THE SCRIPT
```sh
bin/sh runAxon.sh
```
The script does not need parameters. 

The outputs of the script are:
- `out/AXON_<date>.zip`: the ZIP archive that contains the CSV files of the export.
- `logs/runAxon_<date>.log`: the log of the execution of the script (obtained using the Python standard `logging` library).

## CONFIGURATION FILES

### FILE 'paramsAxon.py'
This file contains the parameters for the connection to the DB and the call of API.

## CONTACT
Lorenzo Lombardi - [llombardi@informatica.com](mailto:llombardi@informatica.com)