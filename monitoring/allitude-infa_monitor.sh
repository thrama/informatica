#!/bin/bash

# This bash script monitors the status of Informatica services in a domain. It sends email notifications if any services 
# or the Informatica domain itself are down. If you want to run this script from the crontab, uncomment the line that sources .bash_profile.

# Uncomment the line below if running this script as a cron job to ensure environment variables are loaded.
source /home/infadei/.bash_profile

# Legge il tipo di ambiente (dev o prod) da una variabile di sistema chiamata ENV_TYPE.
# Se ENV_TYPE non è definita, usa "prod" come valore predefinito.
envType="${ENV_TYPE:-prod}"

# Email configurations
fromEmail="noreply@allitude.it"  # Prod
toEmails=("alert@alitude.it")
smtpServer="smtp.server.com"
smtpPort="25"

sendNotification=0

# Configurazione email in base al tipo di ambiente
if [ "$envType" == "dev" ]; then
    emailSubject="Service EDC | DEV environment"
else
    emailSubject="Service EDC | PROD environment"
fi

# Function to send email notification
send_email() {
    local subject="$1"
    local body="$2"
    for toEmail in "${toEmails[@]}"; do
        echo -e "$body" | /usr/bin/mail -S smtp="$smtpServer:$smtpPort" -r "$fromEmail" -s "$subject" "$toEmail"
    done
}

# Ping the Informatica domain
output=$(infacmd.sh isp PingDomain -Format CSV) || { echo "Command 'infacmd.sh isp PingDomain' failed"; exit 1; }

total_line_count=$(echo "$output" | wc -l)

if [[ "$total_line_count" -eq 1 ]] && [[ "$output" =~ "NOT_ALIVE" ]]; then
    sendNotification=1
    emailBody="Informatica domain $INFA_DEFAULT_DOMAIN is down."
else
    not_alive_rows=""
    row_count=0

    while IFS= read -r line; do
        ((row_count++))
        if [ "$row_count" -eq 1 ]; then
            continue
        fi
        if [[ ! "$line" =~ ",ALIVE," ]]; then
            not_alive_rows+="$(echo "$line" | cut -d',' -f1)\n"
        fi
    done <<< "$output"

    if [ -n "$not_alive_rows" ]; then
        sendNotification=1
        emailBody="Following services are not in state ALIVE:\n$not_alive_rows"
    fi
fi

# Uncomment the line below to force a notification for testing purposes.
#sendNotification=1

if [ "$sendNotification" -eq 1 ]; then
    send_email "$emailSubject" "$emailBody"
    printf "Notification sent: Subject='%s', Body='%s'\n" "$emailSubject" "$emailBody"
fi
