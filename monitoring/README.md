# Informatica Domain Monitor Script

This script monitors the status of an Informatica domain, nodes, and services by pinging them using the `infacmd.sh isp PingDomain` command. It checks for any services that are not 'ALIVE' and sends a notification email if necessary.

## Prerequisites

- The Informatica Command Line Utilities (`infacmd.sh`) must be installed and accessible in the system's PATH.
- The environment variables INFA_DEFAULT_DOMAIN, INFA_DEFAULT_DOMAIN_USER, and INFA_DEFAULT_DOMAIN_PASSWORD need to be declared. If not, the command `infacmd.sh` will fail.
- The `mail` command-line utility should be installed for sending email notifications.

## Usage

1. Update the following variables in the script according to your environment:

   - `infaDomain`: The name of the Informatica domain to monitor.
   - `fromEmail`: The email address of the sender for notification emails.
   - `toEmail`: The email address of the recipient for notification emails.
   - `smtpServer`: The SMTP server address for sending email notifications.
   - `smtpPort`: The SMTP server port for sending email notifications.
   
2. Run the script:
   ```bash
   ./infa_monitor.sh
   ```

> **Note:** the script must executed with the user that ran the the Informatica domain.

INFA_DEFAULT_DOMAIN
INFA_DEFAULT_DOMAIN_USER
INFA_DEFAULT_DOMAIN_PASSWORD

## Ouptut
The output of the script is an email notification that notifies the users about two monitored cases:

1. An **error** if the Informatica Domain is down.
2. A **warning** if one or more services are not 'ALIVE'.

In the second case, the email will list the services that are in a state different from 'ALIVE'.

## Script Flow
The script runs the `infacmd.sh isp PingDomain` command to retrieve the status of the Informatica domain, nodes, and services.

1. It parses the output of the command and checks if any services are not 'ALIVE'.
2. If there are non-'ALIVE' services, the script constructs an email with the details of the affected services and sends it to the specified recipient.
3. If the Informatica domain itself is down, a separate email is sent to notify about the domain outage.
4. The script uses the `mail` command-line utility to send email notifications. Make sure it is properly configured on your system.

## Proposed Evolutions
- Modify the script to insert a distinction between core and non-core services.
- If the script reports an error, insert intelligent management of the following checks and notifications. For example, the script doesn't send further notifications for an hour.