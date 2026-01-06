# EDC PROFILE AUTOMATION

## ABOUT THE PROJECT

To start a new project of Data Governance, we developed a (Python) script to automatise the group and the permission on the resources.

### BUILT WITH

- [Pyhotn 3.6.12](https://www.python.org/downloads/release/python-386/)

## PREREQUISITES

### PYTHON LIBRARIES

At first, you need to install the libraries:

- [Pyexcel](http://docs.pyexcel.org/en/latest/) - Provides one application programming interface to read, manipulate and write data in various Excel formats.
- [Requests](https://docs.python-requests.org/en/master/) - Requests allows you to send HTTP/1.1 requests extremely easily.

This is an example of the command:

```sh
$ pip3 install pyexcel pyexcel-xls pyexcel-xlsx requests
```

### ENV CONFIGURATION

The bank prepared an environment where we can install the needed libraries:

```sh
$ cd /opt/python/informatica/
$ source bin/activate
(informatica) [...]$
```

## INSTALLATION

To install the script, copy and unzip the archive file in the correct folder:

```sh
$ unzip Profiles.zip
```

### USAGE

```sh
usage:
<python> main.py --xls <excel_file>
```

Use source Excel file to create JSON files and connections for Informatica service.

```
optional arguments:
  -h, --help              show this help message and exit
  -v, --version           show program version
  -x, --xls <excel_file>  Excel file (source)
```

Example:

```sh
$ python main.py -x xlsxFile/Template_Profilazione_V4.xlsx
```

### NOTES

- The script checks if the **resource** exists; if not, it jumps to the next row in the Excel file.
- The script checks if the **group** exist; if not, it jumps to the next row in the Excel file.

## CONFIGURATION FILES

### FILE 'globalparams.py'

The `globalparams.py` file contains the values for the specific environments.

For this reason, it is a best practice to **back up this file before installing a new version** of the script.

### FILE 'config.py'

In the main folder, it is available a file called `config.py`. In this file, you can change some configurations:

- `infaHome`, the same value of the environment variable $INFA_HOME.
- `resultFolder`, where the script save the results (e.g. JSON files, ODBC files, etc.).
- `sheetName`, the name to assign to the Excel sheet to elaborate.

## CONTACT

**Lorenzo Lombardi**

- LinkedIn: [linkedin.com/in/lorenzolombardi](https://www.linkedin.com/in/lorenzolombardi/)
- GitHub: [github.com/thrama](https://github.com/thrama)
