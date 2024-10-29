#!/bin/bash

# This bash script is used to monitor the status of Informatica services in a domain. It sends email notifications if any services 
# or the Informatica domain itself are down. If you want to run this script from the crontab, uncomment the line that sources .bash_profile.

# If you are running this script as a cron job, the environment might not be fully set up. In such cases, uncomment the line below.
# This line sources the '.bash_profile' from your home directory, ensuring that the environment variables and settings 
# that the script relies on are properly loaded. If your '.bash_profile' or equivalent file is in a different location, adjust the path accordingly.
source /home/infadei/.bash_profile


# Specify email configurations. Adjust the email addresses and SMTP server details as necessary.
#fromEmail="adadev-noreply@generali.com"  # Dev
fromEmail="ada-noreply@generali.com"  # Prod
toEmails=("mgs.CSC.PH@msg-global.com" "ada.support@nttdata.com")
#toEmails=("lorenzo11.lombardi@emeal.nttdata.com" "giuseppe.belviso@emeal.nttdata.com")
smtpServer="smtpapp.corp.generali.net"
smtpPort="25"

# By default, we don't want to send a notification unless an issue is found.
sendNotification=0

# Use the 'infacmd.sh isp PingDomain' command to ping all nodes and services in the Informatica domain and get their statuses.
output=$(infacmd.sh isp PingDomain -Format CSV) || { echo "Command failed"; exit 1; }
#printf "output: %s\n" "$output"  #debug

# Count the total number of lines in the output
total_line_count=$(echo "$output" | wc -l)
#printf "total_line_count: %s\n" "$total_line_count"  #debug

# Check if the output has exactly one line and it contains "NOT_ALIVE"
if [[ "$total_line_count" -eq 1 ]] && [[ "$output" =~ "NOT_ALIVE" ]]; then
    #printf "Domain DOWN\n"  #debug

    # If the Informatica domain is down, we prepare to send a notification about that.
    sendNotification=1
    emailSubject="Service ITCF-APP-0214 | ADA Informatica Service Unavailability"
    emailBody="Informatica domain $INFA_DEFAULT_DOMAIN is down." 
else
    #printf "Domain UP\n"  #debug

    not_alive_rows=""
    row_count=0

    # Parse the output line by line.
    while IFS= read -r line; do
        ((row_count++))

        #printf "line_1: %s\n" "$line"  #debug

        # Skip the first row (header line).
        if [ "$row_count" -eq 1 ]; then
            continue
        fi

        # If a line doesn't contain "ALIVE", then a service is NOT_ALIVE or DISABLED. We add this service's name to the list of not-alive services.
        if [[ ! "$line" =~ ",ALIVE," ]]; then
            printf "line_2: %s\n" "$line"  #debug
            not_alive_rows+="$(echo "$line" | cut -d',' -f1)\n"
        fi

    done <<< "$output"

    #printf "not_alive_rows: %s\n" "$not_alive_rows"  #debug

    # If there are any not-alive services, we prepare to send a notification.
    if [ -n "$not_alive_rows" ]; then
        sendNotification=1
        emailSubject="Service ITCF-APP-0214 | ADA Informatica Service Unavailability"
        emailBody="Following services are not in state ALIVE:\n$not_alive_rows"
    fi
fi

# If you need to test the sending of emails, uncomment the line below.
#sendNotification=1

# If a notification needs to be sent (either a service or the domain is down), send it.
if [ "$sendNotification" -eq 1 ]; then
    for toEmail in "${toEmails[@]}"; do
        # Command to send an email.
        echo -e "$emailBody" | /usr/bin/mail -S smtp="$smtpServer:$smtpPort" -r "$fromEmail" -s "$emailSubject" "$toEmail"
    done

    # For debugging, just print what the email subject and body would be.
    printf "If a notification were to be sent, the email subject would be: '%s', and the email body would be: '%s'\n" "$emailSubject" "$emailBody"  # debug
fi