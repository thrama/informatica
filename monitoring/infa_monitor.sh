#!/bin/bash

#. setEnv

#
# Check the README.md file before run.
# Last update: 19/12/2022
#


########## MONITOR ##########

# run the command that pings all nodes and services in a domain to displays the status of the domain, nodes, and services
# doc link: https://docs.informatica.com/data-quality-and-governance/informatica-data-quality/10-5-1/command-reference/infacmd-isp-command-reference/pingdomain.html
output=$(infacmd.sh isp PingDomain -dn DMN_GEN_DEV -un Administrator -pd N0des#2020#Dei# -Format CSV)

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

# display the rows that do not containes alive
echo -e "$not_alive_rows"


########## NOTIFICATION ##########

# Verifica se la variabile non_alive_rows non è vuota
if [ -n "$not_alive_rows" ]; then
    # configuration for the notification email
    from_email="adadev-noreply@generali.com"
    to_email="lorenzo11.lombardi@nttdata.com"
    smtp_server="smtpapp.corp.generali.net"
    smtp_port="25"
    email_subject="Warning: service not 'ALIVE' checked"
    email_body="It seems that the followinf service are not ALIVE:\n\n$non_alive_rows"

    # send the email...
    echo -e "$email_body" | /usr/bin/mail -S smtp="$smtp_server:$smtp_port" -r "$from_email" -s "$email_subject" "$to_email"

fi
