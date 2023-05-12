# START/STOP INFORMATICA SERVICES - EDC e TDM

## ABOUT THE PROJECT
Bash scripts to start and stop Informatica service:
- `stop` -> stop the domain and services;
- `start` -> start the domain and services.

The use case is related to the patching install where it is necessary to automatically stop and restart the Informatica products.

## PREREQUISITES
Some prerequisites should be already applied for the installation of the Informatica domain. However, this is a quick list: 
- All the nodes are reachable (via SSH) with key authentication;
- All the nodes are reachable via the hostname (check the `/etc/hosts` file);
- The path of the `$INFA_HOME` is the same on all nodes. 
- The script uses the env variable `$INFA_HOME` value defined on the node that runs the script itself.

### SCRIPTS LANGUAGE
The script has been written and tested with [Bash](https://www.gnu.org/software/bash/) version 4.2.46.

## INSTALLATION AND EXECUTION
### INSTALL
To install the script, you need to copy this files on the servers:
- `start` and `stop`;
- `setEnv`;
- `nodeslist.txt`;

On the remote server you need to copy the scipt `startLocalNode`. You can copy the file into the home folder of the user.

The user that runs the scripts should be the one who runs the Informatica services.

There are no specific package dependencies or desired paths.

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
- `setEnv`: contains the declarations of three environment variables: `INFA_DEFAULT_DOMAIN`, `INFA_DEFAULT_DOMAIN_USER`, `INFA_DEFAULT_DOMAIN_PASSWORD`.
    
    > NOTE: For more information, check the link [Environment Variables for Command Line Programs](https://docs.informatica.com/data-quality-and-governance/data-quality/10-5-3/command-reference/environment-variables-for-command-line-programs.html). 

- `nodeslist.txt`: used by the `start` script to know the ordered list of the nodes.
- `startLocalNode`: you need to copy this script on each Informatica node.

### HOW TO READ THE OUTPUT
Based on the eventual problems, the script ends with a different exit code:
- `0` - Exit with success. 
- `99` - Exit with some issue in the part of the nodes checks.
- `98` - Exit with some issue in the part of the services checks (so only for the script `start`). In the log file, you will find details of services in a "NOT_ALIVE" state. The possible state of services are:
-- ENABLED and ALIVE: ok
-- ENABLED and NOT_ALIVE: ko

Below is an example of output in case of exit code `0`:
```sh
All the services are ENABLED and ALIVE.
SERVICE_NAME                             NODE_NAME                                                    STATUS                         HOST_PORT
                                         node01_pwc-01                                                ALIVE                          pwc-01:6006
                                         node01_pwc-01                                                ALIVE                          pwc-01:6006
MRS_DQ                                   node01_pwc-01                                                ALIVE                          pwc-01:6017
_AdminConsole                            node01_pwc-01                                                ALIVE                          pwc-01:6008
CMS_DQ                                   node01_pwc-01                                                ALIVE                          pwc-01:6020
PWC_IS                                   node01_pwc-01                                                ALIVE                          pwc-01:6022
ANALYST_DQ                               node01_pwc-01                                                ALIVE                          pwc-01:8085
MRS_MON                                  node01_pwc-01                                                ALIVE                          pwc-01:6029
PWC_RS                                   node01_pwc-01                                                ALIVE                          pwc-01:6021
DIS_DQ                                   node01_pwc-01                                                ALIVE                          pwc-01:6024
```

Below is an example of output in case of exit code `2`:
```sh
The test of the service ran more than 11 time(s).
The services in the NOT_ALIVE state are:
SERVICE_NAME                             NODE_NAME                                                    STATUS                         HOST_PORT
PWC_IS                                                                                                NOT_ALIVE
PWC_RS                                                                                                NOT_ALIVE
```

## CONFIGURATION FILES
### FILE 'nodeslist.txt'
This file contains the list of nodes of the Informatica domain.

It is essential to:
- Write nodes in the desired starting order;
- Report the list by writing one node per line;
- Insert, on the same line, the node name and the related hostname separated by a semicolon (`;`).

Below is an example of the file content:

```sh
node01;hostname01.domain
node02;hostname02.domain
node03;hostname03.domain
```

To obtain a list of node name, you can use the following command:

```sh
$ infacmd.bat getNodeName -o c:\nodeslist.txt
```

## CONTACT
Lorenzo Lombardi - [llombardi@informatica.com](mailto:llombardi@informatica.com)
