# EDC DISCOVERY CLEAN

## ABOUT THE PROJECT
To start a new project of Data Governance, we developed a (Python) script to automatise and make some actions faster:
- Update the resource with the value "SaveSourceData" to false.
- Update the resource with the value "isCumulative" to true.
- Execute the resources.
- Update the resource with the value "SaveSourceData" to true (original value).

### BUILT WITH
* [Pyhotn 3.6.12](https://www.python.org/downloads/release/python-386/)

## PREREQUISITES

### PYTHON LIBRARIES
At first, you need to install the libraries:
- [Pyexcel](http://docs.pyexcel.org/en/latest/) - Provides one application programming interface to read, manipulate and write data in various Excel formats.
- [Requests](https://docs.python-requests.org/en/master/) - Requests allows you to send HTTP/1.1 requests extremely easily.

This is an example of the command:

```sh
$ pip3 install pyexcel pyexcel-xls pyexcel-xlsx requests
```

If you obtain this warnign:

```
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ConnectTimeoutError(<pip._vendor.urllib3.connection.HTTPSConnection object at 0x7f9a60282a90>, 'Connection to pypi.org timed out. (connect timeout=15)')': /simple/requests/
```

You need to export the env variable for the proxy:

```sh
$ export https_proxy=http://inet.syssede.systest.sanpaoloimi.com:9090
```

### ENV CONFIGURATIONS
The bank prepared an environment where we can install the needed libraries:

```sh
$ cd /opt/python/informatica/
$ source bin/activate
(informatica) [...]$ 
```

## INSTALLATION
To install the script, copy and unzip the archive file in the correct folder:

```sh
$ unzip BulkDelete.zip
```

## GENERAL USAGE
```sh
usage:
<python> main.py
                -x, --xls <excel_file>
```

Use source Excel file to create JSON files and connections for Informatica service.

```
optional arguments:
  -h, --help              show this help message and exit
  -v, --version           show program version
  -x, --xls <excel_file>  Excel file (source)
```

## CONFIGURATION FILES

### FILE 'globalparams.py'
The `globalparams.py` file contains the values for the specific environments.

For this reason, it is a best practice to **back up this file before installing a new version** of the script.

### FILE 'config.py'
In the main folder, it is available a file called `config.py`. In this file, you can change some configurations:
- `infaHome`, the same value of the environment variable $INFA_HOME.
- `resultFolder`, where the script save the results (e.g. JSON files, ODBC files, etc.).
- `sheetName`, the name to assign to the Excel sheet to elaborate.

In the `config.py` are also present the information to send the alert email:

```
smtpHost = "<smtp_host>:<port>"
sender = "<sender_email_address>"
smtpAuth = "login"
smtpAuthUser = "<user_name>"
smtpAuthPassword = "<password>"
to = ["<receiver1_email_address>", ..., "<receiverN_email_address>""]
```

## CONTACT
Lorenzo Lombardi - [llombardi@informatica.com](mailto:llombardi@informatica.com)