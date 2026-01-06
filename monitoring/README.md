# Informatica Service Monitoring

Bash script for monitoring Informatica domain and service health with email alerting.

## 📋 Overview

This script monitors the status of Informatica services and sends email notifications when services or the domain are down.

## 🎯 Features

- **Domain Health Check**: Monitors overall Informatica domain status
- **Service Monitoring**: Checks individual service health
- **Email Alerts**: Sends notifications for failures
- **Environment-Aware**: Supports dev/prod environment configurations
- **Cron Compatible**: Designed for scheduled execution

## 📦 Prerequisites

- Informatica EDC installed and configured
- `infacmd.sh` accessible in `$INFA_HOME/isp/bin/`
- `mailx` command available for sending emails
- SMTP server accessible

## ⚙️ Configuration

Edit the script to configure:

```bash
# Email configuration
fromEmail="noreply@example.com"
toEmails=("alert@example.com" "ops@example.com")
smtpServer="smtp.example.com"
smtpPort="25"

# Environment type
export ENV_TYPE="prod"  # or "dev"
```

## 📖 Usage

### Manual Execution

```bash
./infa_monitor.sh
```

### Cron Schedule

Run every 5 minutes:

```bash
*/5 * * * * /path/to/monitoring/infa_monitor.sh
```

For cron execution, uncomment the line that sources `.bash_profile`.

## 📧 Email Notifications

The script sends emails when:

- **Domain Down**: Entire Informatica domain is not alive
- **Service Down**: One or more services are not in ALIVE state

## 🔐 Security

- Use dedicated service account for monitoring
- Restrict script permissions: `chmod 750 infa_monitor.sh`
- Secure email credentials if SMTP requires authentication

## 📄 License

Apache License 2.0 - see [LICENSE](../LICENSE)

## 📧 Contact

**Lorenzo Lombardi**

- LinkedIn: [linkedin.com/in/lorenzolombardi](https://www.linkedin.com/in/lorenzolombardi/)
- GitHub: [github.com/thrama](https://github.com/thrama)
