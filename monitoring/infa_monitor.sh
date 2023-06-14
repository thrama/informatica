#!/bin/bash

#. setEnv

#
# Check the README.md file before run.
# Last update: 07/06/2023
#

infaDomain=DMN_GEN_DEV
sendNotification=0

# configurations for the notification email
fromEmail="adadev-noreply@generali.com"
toEmail="lorenzo11.lombardi@nttdata.com"
smtpServer="smtpapp.corp.generali.net"
smtpPort="25"


########## MONITOR ##########

# run the command that pings all nodes and services in a domain to displays the status of the domain, nodes, and services
# doc link: https://docs.informatica.com/data-quality-and-governance/informatica-data-quality/10-5-1/command-reference/infacmd-isp-command-reference/pingdomain.html
output=$(infacmd.sh isp PingDomain -dn $infaDomain -un Administrator -pd N0des#2020#Dei# -Format CSV)


if [ "$?" -eq 0 ]; then
    # the Informatica domain replied to the command, so it checks for service issues

    not_alive_rows=""
    row_count=0

    # parse the output from the command "infacmd.sh isp PingDomain"
    while IFS= read -r line; do
        ((row_count++))

        # skup the headers' line
        if [ "$row_count" -eq 1 ]; then
            continue
        fi

        # check if there are any rows that did not contain "ALIVE"
        if [[ ! "$line" =~ "ALIVE" ]]; then
            not_alive_rows+="$line\n"
        fi

    done <<< "$output"

    # debug: display the rows that do not containes alive
    echo -e "$not_alive_rows"

    if [ -n "$not_alive_rows" ]; then
         # some services is down...
        sendNotification=1

        emailSubject="Warning: service(s) not 'ALIVE' checked"
        emailBody="It seems that the following service are not ALIVE:\n\n$not_alive_rows"

    fi

else
    # the Informatica Domain is down...
    sendNotification=1

    emailSubject="Error: Informatica Domain is down!"
    emailBody="It seems that the Informatica domain $infaDomain is down."

fi

########## NOTIFICATION ##########

# check if it needs to send a notification
if [ "$sendNotification" -eq 1 ]; then

    # send the email...
    echo -e "$emailBody" | /usr/bin/mail -S smtp="$smtpServer:$smtpPort" -r "$fromEmail" -s "$emailSubject" "$toEmail"

fi
