# EDC Automation

Automated creation and management of Informatica Enterprise Data Catalog (EDC) connections and resources.

## 📋 Overview

This project automates the setup of EDC connections and resources for multiple database technologies using Excel-based configuration files. It streamlines the process of onboarding new data sources into EDC by:

- Creating EDC connections via `infacmd` command-line tool
- Generating ODBC configuration files for database connectivity
- Creating EDC resources via REST API
- Producing JSON templates for manual import when API calls fail

## 🎯 Features

### Supported Database Technologies

| Technology           | Connections | Resources | ODBC Config |
| -------------------- | ----------- | --------- | ----------- |
| IBM DB2 z/OS         | ✅          | ✅        | ❌          |
| Microsoft SQL Server | ✅          | ✅        | ✅          |
| Oracle Database      | ✅          | ✅        | ❌          |
| Teradata             | ✅          | ✅        | ✅          |
| Apache Hive          | ✅          | ✅        | ❌          |
| MongoDB              | ⏳          | ⏳        | ❌          |

### Key Capabilities

- **Bulk Operations**: Process multiple connections/resources from a single Excel file
- **Error Handling**: Graceful degradation - generates JSON files for failed API calls
- **ODBC Generation**: Automatic ODBC configuration file creation for SQL Server and Teradata
- **Validation**: Connection name length validation (32 character ODBC limit)
- **Logging**: Comprehensive logging for auditing and troubleshooting

## 📦 Prerequisites

### Software Requirements

- **Python 3.7+**
- **Informatica EDC** 10.4.1 or higher
- **ODBC Drivers** for target databases (if using ODBC connectivity)

### Python Dependencies

```bash
pip install pyexcel pyexcel-xls pyexcel-xlsx requests
```

See `requirements.txt` for specific versions.

### Environment Setup

1. Informatica EDC must be installed and configured
2. Set `INFA_HOME` environment variable:
   ```bash
   export INFA_HOME=/opt/informatica/edc/10.5.0
   ```
3. Ensure `infacmd.sh` is accessible in `$INFA_HOME/isp/bin/`

## 🚀 Installation

1. Clone or download this project:

   ```bash
   git clone https://github.com/thrama/informatica-automation-examples.git
   cd informatica-automation-examples/edc-automation
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment parameters:
   - Edit `globalparams.py` with your EDC environment details
   - Update `config.py` if needed (paths, folder names, etc.)

## ⚙️ Configuration

### Configuration Files

#### `globalparams.py`

Contains environment-specific parameters:

- Domain and DIS configuration
- Catalog Service connection details
- LDAP domain settings
- MIMB Agent configuration

**IMPORTANT:** Update all placeholder values before use. Never commit real credentials to version control.

#### `config.py`

Contains general script configuration:

- `infaHome`: Informatica installation directory
- `resultFolder`: Output directory for generated files
- Template file paths for ODBC and JSON

### Excel Input Format

The script expects Excel files with specific column layouts depending on the operation:

- **Connections**: Connection name, credentials, host, port, database, etc.
- **Resources**: Resource name, connection reference, profiling options, etc.

Refer to the template Excel files in the `xlsxFile/` directory (if available) for exact column mappings.

## 📖 Usage

### Command Line Syntax

```bash
python main.py -t <technology> -x <excel_file> [-c | -r]
```

### Parameters

| Parameter           | Description         | Required | Values                                       |
| ------------------- | ------------------- | -------- | -------------------------------------------- |
| `-t, --tech`        | Database technology | Yes      | db2, hive, mongodb, oracle, sqlsrv, teradata |
| `-x, --xls`         | Excel input file    | Yes      | Path to .xlsx file                           |
| `-c, --connections` | Create connections  | Yes\*    | Flag (no value)                              |
| `-r, --resources`   | Create resources    | Yes\*    | Flag (no value)                              |
| `-v, --version`     | Show version        | No       | Flag (no value)                              |

\*Either `-c` or `-r` must be specified (mutually exclusive)

### Examples

#### Create SQL Server Connections

```bash
python main.py -t sqlsrv -x input/sqlserver_connections.xlsx -c
```

This will:

1. Create EDC connections via `infacmd.sh`
2. Generate ODBC configuration files in `resultFile/` directory
3. Log all operations to `main.log`

**Next step:** Manually merge ODBC files into `$INFA_HOME/ODBC7.1/odbc.ini`

#### Create Oracle Resources

```bash
python main.py -t oracle -x input/oracle_resources.xlsx -r
```

This will:

1. Attempt to create resources via EDC REST API
2. Generate JSON files for any failed API calls
3. Save JSON files in `resultFile/` directory for manual import

#### Create DB2 Connections and Resources (Sequential)

```bash
# Step 1: Create connections
python main.py -t db2 -x input/db2_config.xlsx -c

# Step 2: Create resources
python main.py -t db2 -x input/db2_config.xlsx -r
```

## 📂 Output Files

### Generated Files

The script creates output files in the `resultFile/` directory:

#### ODBC Configuration Files

- `sqlsrv_odbc_heads.txt` - SQL Server DSN list
- `sqlsrv_odbc_sections.txt` - SQL Server connection parameters
- `teradata_odbc_heads.txt` - Teradata DSN list
- `teradata_odbc_sections.txt` - Teradata connection parameters

**Usage:** Append these files to `$INFA_HOME/ODBC7.1/odbc.ini`

#### JSON Resource Files

- `{TECHNOLOGY}_{RESOURCE_NAME}.json` - Resource definition for manual import

**Usage:** Import via EDC Catalog Administrator UI or REST API

### Log Files

- `main.log` - Detailed execution log with DEBUG level information

## 🔧 Troubleshooting

### Common Issues

#### Connection Creation Fails

```
Error: Command failed with exit code 1
```

**Causes:**

- EDC services not running
- Invalid credentials in `globalparams.py`
- Connection name already exists
- Network connectivity issues

**Solution:** Check EDC service status, verify credentials, check logs

#### Resource API Call Returns 500

```
Error: General internal server error
```

**Causes:**

- Resource name conflicts with existing resource
- Invalid JSON structure
- Missing required fields
- Connection doesn't exist

**Solution:** Review generated JSON file, verify connection exists, check EDC logs

#### ODBC DSN Name Too Long

```
Warning: ODBC DSN name exceeds 32 characters
```

**Solution:** Provide alternative DSN in column 3 of Excel file (max 32 chars)

### Debug Mode

For verbose output, check `main.log` which contains DEBUG level logging:

```bash
tail -f main.log
```

## 🔐 Security Best Practices

See [SECURITY.md](./SECURITY.md) for detailed security guidelines.

**Critical Reminders:**

- ⚠️ Never commit `globalparams.py` with real credentials
- ⚠️ Use environment variables for sensitive data in production
- ⚠️ Enable SSL/TLS for all API connections
- ⚠️ Restrict file permissions on configuration files
- ⚠️ Implement credential rotation policies

## 📁 Project Structure

```
edc-automation/
├── main.py                  # Main entry point
├── config.py                # General configuration
├── globalparams.py          # Environment-specific parameters
├── excel.py                 # Excel file parser
├── connections.py           # Connection creation logic
├── resources.py             # Resource creation logic
├── restapicall.py           # REST API client
├── odbc.py                  # ODBC file generator
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── SECURITY.md              # Security guidelines
├── odbcFile/                # ODBC template files
│   ├── Template_ODBC_SQLSrv_*.txt
│   └── Template_ODBC_Teradata_*.txt
├── jsonFile/                # JSON template files
│   ├── Template_DB2zos.json
│   ├── Template_SQLServer.json
│   ├── Template_Teradata.json
│   ├── Template_Hive.json
│   └── Template_Oracle.json
└── resultFile/              # Output directory (auto-created)
```

## 📚 Additional Resources

- [Informatica EDC Documentation](https://docs.informatica.com/data-catalog/enterprise-data-catalog.html)
- [infacmd Command Reference](https://docs.informatica.com/data-catalog/enterprise-data-catalog/10-4-1/command-reference/infacmd-isp-command-reference.html)
- [EDC REST API Reference](https://docs.informatica.com/data-catalog/enterprise-data-catalog/10-4-1/rest-api-reference.html)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for details.

## 🤝 Contributing

This is a personal portfolio project, but suggestions and feedback are welcome through GitHub Issues.

## 📧 Contact

**Lorenzo Lombardi**

- LinkedIn: [linkedin.com/in/lorenzolombardi](https://www.linkedin.com/in/lorenzolombardi/)
- GitHub: [github.com/thrama](https://github.com/thrama)
