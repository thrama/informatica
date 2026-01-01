# Setup Guide - Informatica EDC Automation

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: Version 3.6 or higher
- **Informatica EDC**: Version 10.4.1 or higher
- **Access**: EDC Administrator credentials and API access

### Environment Variables

Ensure the following environment variable is set:

```bash
export INFA_HOME=/path/to/informatica/edc/installation
```

## Installation Steps

### 1. Clone Repository

```bash
git clone <repository-url>
cd informatica-edc-automation
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# For .xlsm file support, you may need:
pip install xlrd==1.2.0
```

### 4. Configure Global Parameters

#### Copy Template

```bash
cp globalparams.py.example globalparams.py
```

#### Edit Configuration

Edit `globalparams.py` with your environment-specific values:

```python
# Domain Configuration
domainName="YOUR_EDC_DOMAIN"
domainUser="YOUR_ADMIN_USER"
domainPassword="YOUR_PASSWORD"

# Data Integration Service
disName="YOUR_DIS_NAME"
disHost="your-dis-hostname.domain.com"
disPort="6005"

# Catalog Service
catalogHost="your-catalog-hostname.domain.com"
catalogPort="9086"
catalogUser="YOUR_CATALOG_USER"
catalogPassword="YOUR_PASSWORD"

# LDAP Domain (for Windows Authentication)
ldapDomain="YOUR_DOMAIN"
```

#### Secure the Configuration File

```bash
# On Linux/macOS
chmod 600 globalparams.py

# Verify it's not tracked by Git
git status  # Should not show globalparams.py
```

### 5. Create Directory Structure

```bash
# Create necessary directories
mkdir -p odbcFile
mkdir -p jsonFile
mkdir -p xlsxFile
mkdir -p resultFile
```

### 6. Add ODBC Templates

Place your ODBC template files in the `odbcFile/` directory:

- `Template_ODBC_SQLSrv_sections.txt`
- `Template_ODBC_SQLSrv_heads.txt`
- `Template_ODBC_Teradata_sections.txt`
- `Template_ODBC_Teradata_heads.txt`

### 7. Add JSON Templates

Place your JSON template files in the `jsonFile/` directory:

- `Template_DB2zos.json`
- `Template_SQLServer.json`
- `Template_Teradata.json`
- `Template_Hive.json`
- `Template_Oracle.json`

## Configuration Files

### globalparams.py Parameters

| Parameter         | Description                   | Example                   |
| ----------------- | ----------------------------- | ------------------------- |
| `domainName`      | EDC Domain name               | `DMN_EDC_PROD`            |
| `domainUser`      | Domain admin username         | `Administrator`           |
| `domainPassword`  | Domain admin password         | `SecurePass123`           |
| `disName`         | Data Integration Service name | `DIS_EDC_PROD`            |
| `disHost`         | DIS hostname                  | `edc-dis.company.com`     |
| `disPort`         | DIS port                      | `6005`                    |
| `catalogHost`     | Catalog Service hostname      | `edc-catalog.company.com` |
| `catalogPort`     | Catalog Service port          | `9086`                    |
| `catalogUser`     | Catalog admin username        | `Administrator`           |
| `catalogPassword` | Catalog admin password        | `SecurePass123`           |
| `ldapDomain`      | Windows domain for NTLM auth  | `CORPORATE`               |

### config.py Parameters

| Parameter      | Description                | Default      |
| -------------- | -------------------------- | ------------ |
| `infaHome`     | Informatica home directory | `$INFA_HOME` |
| `resultFolder` | Output directory           | `resultFile` |
| `sheetName`    | Excel sheet to process     | `Sheet1`     |

## Preparing Excel Input Files

### Connection Excel Format

Your Excel file should have the following structure (example for SQL Server):

| Column | Description            | Example                 |
| ------ | ---------------------- | ----------------------- |
| 0      | Technology             | `SQLSRV`                |
| 1      | Resource Name          | `SQL_HR_Database`       |
| 2      | Connection Name        | `SQL_HR_CONN`           |
| 3      | DSN (alternative name) | `HR_DSN`                |
| 4      | Reserved               |                         |
| 5      | Username               | `sql_reader`            |
| 6      | Password               | `password123`           |
| 7      | Reserved               |                         |
| 8      | Hostname               | `sqlserver.company.com` |
| 9      | Reserved               |                         |
| 10     | Port                   | `1433`                  |
| 11     | Database               | `HR_Production`         |

**Note**: Column indices may vary by technology. Refer to your specific template.

### Resource Excel Format

Similar structure but may include additional fields depending on the technology.

## Testing the Installation

### Verify Installation

```bash
# Check Python version
python --version

# Verify dependencies
pip list | grep -E "pyexcel|requests"

# Verify Informatica CLI
$INFA_HOME/isp/bin/infacmd.sh isp help
```

### Run a Test

```bash
# Test with a small Excel file
python main.py -t sqlsrv -x test_data.xlsx -c --version

# Check logs
tail -f main.log
```

## Troubleshooting

### Common Issues

#### 1. Module Not Found Error

```bash
# Solution: Install missing module
pip install <module-name>
```

#### 2. INFA_HOME Not Set

```bash
# Solution: Export environment variable
export INFA_HOME=/path/to/informatica
```

#### 3. Permission Denied on infacmd.sh

```bash
# Solution: Check file permissions
chmod +x $INFA_HOME/isp/bin/infacmd.sh
```

#### 4. ODBC DSN Name Too Long

```
Error: SecureConnectionName [VeryLongConnectionName] is longer than 32 characters
```

**Solution**: Provide a shorter DSN name in column 3 of the Excel file.

#### 5. REST API Connection Error

```
Error: RestAPI error [Connection refused]
```

**Solution**:

- Verify `catalogHost` and `catalogPort` in `globalparams.py`
- Check network connectivity to catalog service
- Verify credentials

#### 6. xlrd Version Issue (.xlsm files)

```bash
# Solution: Downgrade xlrd
pip uninstall xlrd
pip install xlrd==1.2.0
```

## Behind Corporate Proxy

If you're behind a corporate proxy:

### Set Proxy Environment Variables

```bash
export http_proxy=http://proxy.company.com:port
export https_proxy=http://proxy.company.com:port
export no_proxy=localhost,127.0.0.1,.company.com
```

### Configure pip for Proxy

```bash
pip install --proxy http://proxy.company.com:port package-name
```

## Next Steps

After successful installation:

1. **Prepare Input Files**: Create Excel files with connection/resource data
2. **Test with Small Dataset**: Run with 2-3 connections first
3. **Review Logs**: Check `main.log` for any warnings
4. **Validate ODBC**: Review generated ODBC configuration files
5. **Verify in EDC**: Check that connections/resources appear in EDC UI

## Getting Help

- **Logs**: Check `main.log` for detailed error messages
- **Documentation**: Refer to [README.md](README.md) for usage examples
- **Security**: Review [SECURITY.md](SECURITY.md) for credential management

## Maintenance

### Regular Tasks

- **Backup Configuration**: Keep backups of `globalparams.py`
- **Update Dependencies**: `pip list --outdated` to check for updates
- **Rotate Credentials**: Update passwords in `globalparams.py` regularly
- **Clean Logs**: Archive or delete old log files periodically

### Before Major Changes

```bash
# Backup current configuration
cp globalparams.py globalparams.py.backup

# Test in development environment first
# Create separate configuration for testing
```

---

For additional support or questions, refer to the project documentation or contact the maintainer.
