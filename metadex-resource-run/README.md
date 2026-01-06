# EDC Advanced Scanners - Sequential Execution Script

## Description

This Bash script automates the sequential execution of Informatica Enterprise Data Catalog (EDC) Advanced Scanners. It supports multiple scanner types including Oracle Stored Procedures and Power BI scanners, with comprehensive job monitoring and logging capabilities.

## Features

- **Sequential Execution**: Runs multiple scanners in a defined order
- **Job Monitoring**: Tracks job status until completion (success or failure)
- **Configurable Timeouts**: Adjustable wait times and check intervals
- **Flexible Configuration**: Environment-based configuration via `.env` file
- **Detailed Logging**: Comprehensive logs for troubleshooting
- **Failure Handling**: Optional stop-on-failure behavior
- **Multiple Scanner Groups**: Support for different scanner categories

## Requirements

- **EDC Version**: Informatica EDC 10.4.x or later with Advanced Scanners Application
- **Operating System**: Linux (tested on RHEL/CentOS 7+, Ubuntu 18.04+)
- **Bash Version**: 4.0 or later
- **Permissions**:
  - Read/execute access to EDC Advanced Scanners CLI
  - Write access to log directory
  - EDC user account with scanner execution privileges

## Installation

1. Clone or copy the script to your preferred location:

   ```bash
   mkdir -p /opt/scripts/edc-scanners
   cp run_edc_scanners.sh /opt/scripts/edc-scanners/
   chmod +x /opt/scripts/edc-scanners/run_edc_scanners.sh
   ```

2. Create your environment configuration:

   ```bash
   cp .env.example .env
   ```

3. Edit `.env` with your specific configuration (see Configuration section)

## Configuration

Copy `.env.example` to `.env` and configure the following variables:

### Required Variables

| Variable        | Description                           | Example                                                                               |
| --------------- | ------------------------------------- | ------------------------------------------------------------------------------------- |
| `SCANNERS_HOME` | Path to Advanced Scanners Application | `/opt/informatica/edc/10.5.1/services/CatalogService/AdvancedScannersApplication/app` |
| `EDC_SERVER`    | EDC Catalog Service URL               | `https://edc-server.example.com:9085`                                                 |
| `EDC_USER`      | EDC service account username          | `edc_scanner_user`                                                                    |
| `EDC_PASSWORD`  | EDC service account password          | `your_secure_password`                                                                |

### Optional Variables

| Variable                 | Default                   | Description                               |
| ------------------------ | ------------------------- | ----------------------------------------- |
| `EDC_AUTH_TYPE`          | `Native`                  | Authentication type (Native, LDAP, SAML)  |
| `LOG_DIR`                | `/var/log/edc-scanners`   | Log files directory                       |
| `MAX_JOB_WAIT_TIME`      | `21600`                   | Maximum wait time per job (seconds)       |
| `STATUS_CHECK_INTERVAL`  | `30`                      | Status check frequency (seconds)          |
| `STOP_ON_FAILURE`        | `true`                    | Stop execution on first failure           |
| `ORACLE_SP_SCANNER_BASE` | `DataHubStoredProcedures` | Base path for Oracle SP scanners          |
| `POWERBI_SCANNER_BASE`   | `Power_Bi`                | Base path for Power BI scanners           |
| `ORACLE_SP_SCANNERS`     | -                         | Comma-separated list of Oracle scanners   |
| `POWERBI_SCANNERS`       | -                         | Comma-separated list of Power BI scanners |

### Example Configuration

```bash
# .env
SCANNERS_HOME=/opt/informatica/edc/10.5.1/services/CatalogService/AdvancedScannersApplication/app
EDC_SERVER=https://edc.example.com:9085
EDC_AUTH_TYPE=Native
EDC_USER=scanner_service
EDC_PASSWORD=SecurePassword123

LOG_DIR=/var/log/edc-scanners
STOP_ON_FAILURE=true

ORACLE_SP_SCANNER_BASE=DataHubStoredProcedures
ORACLE_SP_SCANNERS=Schema1_DB1,Schema2_DB1,Schema3_Packages

POWERBI_SCANNER_BASE=Power_Bi
POWERBI_SCANNERS=PowerBI_Workspace1,PowerBI_Workspace2
```

## Usage

### Basic Execution

```bash
# Using default .env in script directory
./run_edc_scanners.sh

# Specify custom environment file
./run_edc_scanners.sh --env-file /path/to/custom.env

# Show help
./run_edc_scanners.sh --help
```

### Scheduled Execution (Cron)

```bash
# Run daily at 2:00 AM
0 2 * * * /opt/scripts/edc-scanners/run_edc_scanners.sh >> /var/log/edc-scanners/cron.log 2>&1
```

## Output

### Log Files

The script generates the following log files in `LOG_DIR`:

- `scanner_run_YYYYMMDD_HHMMSS.log` - Main execution log
- `{scanner_name}_YYYYMMDD_HHMMSS.log` - Individual scanner output logs

### Exit Codes

| Code | Description                            |
| ---- | -------------------------------------- |
| `0`  | All scanners completed successfully    |
| `1`  | One or more scanners failed            |
| `2`  | Timeout waiting for scanner completion |

### Sample Output

```
=====================================
[2025-01-06 02:00:00] EDC Scanners Execution - Started
=====================================
[2025-01-06 02:00:00] Configuration:
[2025-01-06 02:00:00]   EDC Server: https://edc.example.com:9085
[2025-01-06 02:00:00]   Auth Type: Native
[2025-01-06 02:00:00]   Log Directory: /var/log/edc-scanners
[2025-01-06 02:00:00]   Stop on Failure: true
=====================================
[2025-01-06 02:00:01] Oracle Stored Procedures Scanners Execution
=====================================
[2025-01-06 02:00:01] Starting scanner: Schema1_DB1
[2025-01-06 02:00:01]   Path: DataHubStoredProcedures/Schema1_DB1
[2025-01-06 02:00:03] Schema1_DB1 submitted (ProcessingID: 138456789)
[2025-01-06 02:00:08] Monitoring job status for Schema1_DB1 (ProcessingID: 138456789)...
[2025-01-06 02:00:08] Schema1_DB1 - Status: RUNNING (check 0/720)
[2025-01-06 03:15:38] Schema1_DB1 completed successfully
...
=====================================
[2025-01-06 08:45:00] Execution Summary
=====================================
  Schema1_DB1:                   SUCCESS
  Schema2_DB1:                   SUCCESS
  Schema3_Packages:              SUCCESS
  PowerBI_Workspace1:            SUCCESS
-------------------------------------
[2025-01-06 08:45:00] Total: 4 succeeded, 0 failed
=====================================
```

## Troubleshooting

### Common Issues

1. **Scanner CLI not found**

   - Verify `SCANNERS_HOME` path is correct
   - Check file permissions on `scanners-cli.sh`

2. **Authentication failures**

   - Verify credentials in `.env` file
   - Check EDC_AUTH_TYPE matches your environment
   - Ensure service account has required permissions

3. **Timeout errors**

   - Increase `MAX_JOB_WAIT_TIME` for long-running scanners
   - Check EDC server performance and connectivity

4. **Scanner submission fails**
   - Verify scanner configuration exists in EDC workspace
   - Check scanner path is correct (case-sensitive)

### Debug Mode

For additional debugging, run with bash debug flags:

```bash
bash -x ./run_edc_scanners.sh
```

## Security Considerations

- Store credentials in `.env` file with restricted permissions (`chmod 600 .env`)
- Never commit `.env` file to version control
- Use a dedicated service account with minimal required permissions
- Consider using credential management tools (HashiCorp Vault, AWS Secrets Manager)

## License

Apache License 2.0

## Author

- **Lorenzo Lombardi**
- LinkedIn: [linkedin.com/in/lorenzolombardi](https://www.linkedin.com/in/lorenzolombardi/)
- GitHub: [github.com/thrama](https://github.com/thrama)
