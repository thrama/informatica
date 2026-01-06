#!/bin/bash
###
# DATA: 09/07/2024
# VERSION: 1.0
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama
#
# DESCRIPTION:
# Informatica service health monitoring script with email notifications.
# Monitors domain and service status, sends alerts on failures.
#
# Features:
# - Checks Informatica domain status
# - Monitors individual service health
# - Sends email notifications for failures
# - Environment-aware (dev/prod)
###

# Uncomment the line below if running this script as a cron job
# source /home/informatica/.bash_profile

# Determine environment type (dev or prod)
# Uses ENV_TYPE environment variable, defaults to "prod"
envType="${ENV_TYPE:-prod}"

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

# Email sender address
fromEmail="noreply@example.com"

# Email recipients (can be multiple)
toEmails=("alert@example.com" "ops@example.com")

# SMTP server configuration
smtpServer="smtp.example.com"
smtpPort="25"

# Email subject varies by environment
if [ "$envType" == "dev" ]; then
    emailSubject="Informatica EDC Service Alert | DEV Environment"
else
    emailSubject="Informatica EDC Service Alert | PROD Environment"
fi

# Flag to track if notification should be sent
sendNotification=0


# =============================================================================
# FUNCTIONS
# =============================================================================

send_email() {
    """
    Send email notification using mailx command.

    Args:
        $1: Email subject
        $2: Email body
    """
    local subject="$1"
    local body="$2"

    for toEmail in "${toEmails[@]}"; do
        echo -e "$body" | /usr/bin/mail \
            -S smtp="$smtpServer:$smtpPort" \
            -r "$fromEmail" \
            -s "$subject" \
            "$toEmail"
    done
}


# =============================================================================
# MAIN MONITORING LOGIC
# =============================================================================

# Ping the Informatica domain
output=$(infacmd.sh isp PingDomain -Format CSV) || {
    echo "ERROR: Command 'infacmd.sh isp PingDomain' failed"
    exit 1
}

total_line_count=$(echo "$output" | wc -l)

# Check if domain is completely down
if [[ "$total_line_count" -eq 1 ]] && [[ "$output" =~ "NOT_ALIVE" ]]; then
    sendNotification=1
    emailBody="CRITICAL: Informatica domain $INFA_DEFAULT_DOMAIN is DOWN."

else
    # Check individual services
    not_alive_rows=""
    row_count=0

    while IFS= read -r line; do
        ((row_count++))

        # Skip header row
        if [ "$row_count" -eq 1 ]; then
            continue
        fi

        # Check if service is not ALIVE
        if [[ ! "$line" =~ ",ALIVE," ]]; then
            service_name=$(echo "$line" | cut -d',' -f1)
            not_alive_rows+="$service_name\n"
        fi
    done <<< "$output"

    # Send notification if any services are down
    if [ -n "$not_alive_rows" ]; then
        sendNotification=1
        emailBody="WARNING: The following Informatica services are NOT in ALIVE state:\n\n$not_alive_rows\n\nPlease investigate immediately."
    fi
fi


# =============================================================================
# NOTIFICATION SENDING
# =============================================================================

# Uncomment the line below to force notification sending (for testing)
# sendNotification=1

if [ "$sendNotification" -eq 1 ]; then
    send_email "$emailSubject" "$emailBody"
    printf "Notification sent:\n  Subject: '%s'\n  Body: '%s'\n" "$emailSubject" "$emailBody"

    # Log to syslog
    logger -t "infa-monitor" "$emailSubject - $emailBody"
fi

exit 0
