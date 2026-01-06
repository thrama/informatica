# START/STOP INFORMATICA SERVICES - AXON

## ABOUT THE PROJECT
Bash scripts to start and stop Informatica service:
- `start` -> stop the domain and services;
- `stop` -> start the domain and services.

The use case is related to the patching install where it is necessary to automatically stop and restart the Informatica products.

## PREREQUISITES
- The script uses the env variable `AXON_BASE` value defined on the node that runs the script itself.
- The script was tested with the version 7.3.x of Informatica Axon, but is written to work also with previous version.
- The script has been written and tested with [Bash](https://www.gnu.org/software/bash/) version 4.2.46.

## INSTALLATION AND EXECUTION
### INSTALL
To install the script, you need to copy this files on the servers:
- `start` and `stop` files on the main server. Usually the infrastructure node.
- `startLocalNode` on all the Informatica node, also the infrastructure one.

The user that runs the scripts should be the one who runs the Axon services.

There are no specific package dependencies or desired paths.

### POST INSTALL CONFIGURATION
In the `start` script, you need to set the state of the variable `EVENT_MONITOR` to:
- `0` -> disabled
- `1` -> enabled

The variable is defined at line 9 of the start script:
```python
EVENT_MONITOR=1
```

The default value is `0`.

For further information, check the link below:
https://docs.informatica.com/data-quality-and-governance/axon-data-governance/7-3-1/data-governance-administrator-guide/monitor-axon/view-usage-statistics.html

### HOW TO RUN THE SCRIPT
The command to run the script to stop the service is:
```sh
$ ./stop
```

The command to run the script to start the service is:
```sh
$ ./start
```

### GENERAL USAGE OF THE SCRIPT
The scripts do not need parameters. 

The files used by the script are:
- `start-<timestamp>.log`: the start script log the information on this file.
- `stop-<timestamp>.log`: the stop script log the information on this file.

### HOW TO READ THE OUTPUT
Based on the eventual problems, the script ends with a different exit code:
- `0` - Exit with success. 
- `1` - Exit with some issue in the services.

Below is an example of output in case of exit code `0`:
```sh
2023-01-17 13:04: (1) N.SERVICES: 0
2023-01-17 13:04: N.SERVICES: 22
All service are up:
  --------------------------------------------------
 |               Axon Component Status              |
  --------------------------------------------------
 | SL  Status Component                         PID |
  --------------------------------------------------
 | 01  #  1 # RABBIT_MQ                  #     5285 |
 | 02  #  1 # POSTGRES                   #     4795 |
 | 03  #  1 # ORIENTDB                   #     4821 |
 | 04  #  1 # MEMCACHED                  #     6511 |
 | 05  #  1 # JOBBER                     #    13894 |
 | 06  #  1 # HTTPD                      #     9065 |
 | 07  #  1 # DAEMONTOOLS                #     6536 |
 | 08  #  1 # CAMUNDA                    #     4880 |
 | 09  #  1 # ODB_CONSUMER               #     9077 |
 | 10  #  1 # NOTIFICATION_MS            #     5859 |
 | 11  #  1 # DOC_UPLOAD_MS              #     5883 |
 | 12  #  1 # CHANGE_REQUEST_MS          #     5870 |
 | 13  #  1 # UNISON_MS                  #    15071 |
 | 14  #  1 # VALUE_LIST_MS              #     9088 |
 | 15  #  1 # BULK_UPLOAD_SRVC           #    13907 |
 | 16  #  1 # BULK_UPLOAD_PRE_VALDTR     #    14354 |
 | 17  #  1 # BULK_UPLOAD_VALDTR         #    14570 |
 | 18  #  1 # BULK_UPLOAD_COMMTR         #    14838 |
 | 19  #  1 # LOGSTASH                   #    16026 |
 | 20  #  1 # ELASTIC_SEARCH             #    16003 |
 | 21  #  1 # MARKETPLACE_MS             #    11996 |
 | 22  #  1 # AUTHORIZATION_MS           #    12941 |
 | 23  #  0 # EVENT_MONITOR              #          |
  --------------------------------------------------
 | Status (0) - Component is NOT running.           |
 | Status (1) - Component is running.               |
 | Status(-1) - Component DEAD but pid file exists. |
  --------------------------------------------------
```

Below is an example of output in case of exit code `1`:
```sh
2023-01-17 13:04: (1) N.SERVICES: 0
2023-01-17 13:04: N.SERVICES: 22
2023-01-17 13:04: Some services report some issue during startup:

  --------------------------------------------------
 |               Axon Component Status              |
  --------------------------------------------------
 | SL  Status Component                         PID |
  --------------------------------------------------
 | 23  #  0 # EVENT_MONITOR              #          |
  --------------------------------------------------
 | Status (0) - Component is NOT running.           |
 | Status (1) - Component is running.               |
 | Status(-1) - Component DEAD but pid file exists. |
  --------------------------------------------------
                                                                                          NOT_ALIVE
```

## CONTACT
Lorenzo Lombardi - [llombardi@informatica.com](mailto:llombardi@informatica.com)
