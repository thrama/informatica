#!/bin/sh -x

# This script is used to automatically start the Infa service.
# It sources the content of the .bash_profile file and sets the necessary environment variables.
# The script then starts the Infa service using the specified user and logs the output to a log file.

sleep 30

# Define the log file path
LOG_FILE="/informatica/infadei/10.5.5/autostart.log"

# Source the .bash_profile to set environment variables
source /home/infadei/.bash_profile

# Define the user to run the Infa service
USER=infadei

# Log the start time and action to the log file
echo -n $(date "+%Y-%m-%d %H:%M:%S") $"Starting Infa: " >> $LOG_FILE

# Print the action to the console
echo -n $"Starting Infa: "

# Check if the INFA_HOME environment variable is set
if [ -z "$INFA_HOME" ]; then
    # If not, log the error message to the log file and exit the script
    echo "INFA_HOME non è definito. Assicurati che /home/infadei/.bash_profile sia configurato correttamente." >> $LOG_FILE
    exit 1
fi

# Start the Infa service as the specified user and redirect both stdout and stderr to the log file
su $USER -c "$INFA_HOME/tomcat/bin/infaservice.sh startup" >> $LOG_FILE 2>&1
