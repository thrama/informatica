# START/STOP INFORMATICA SERVICES - DDM

## ABOUT THE PROJECT

Bash scripts to start and stop Informatica DDM server:

- `stop` -> stop the DDM server;
- `start` -> start the DDM server.

The use case is related to the patching install where it is necessary to automatically stop and restart the Informatica products.

## PREREQUISITES

Some prerequisites:

- The script can start and stop only the DDM instance on the server on which it runs.
- The script need to run as `root` user. This is why it run the SystemD command to start and stop the server:
  ```sh
  systemd start infaddm
  ```
  and
  ```sh
  systemd stop infaddm
  ```

### SCRIPTS LANGUAGE

The script has been written and tested with [Bash](https://www.gnu.org/software/bash/) version 4.2.46.

## INSTALLATION AND EXECUTION

### INSTALL

To install the script, you need to copy the `start` and `stop` files on the server.

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

- `ddm_start-<timestamp>.log`: the start script log the information on this file.
- `ddm_stop-<timestamp>.log`: the stop script log the information on this file.

### HOW TO READ THE OUTPUT

Based on the eventual problems, the script ends with a different exit code:

- `0` - Exit with success.
- `1` - Exit with some issue.

## CONTACT

Lorenzo Lombardi - [llombardi@informatica.com](mailto:llombardi@informatica.com)
