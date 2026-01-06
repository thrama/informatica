# EDC Lineage Bulk Export

Export data lineage information from Informatica Enterprise Data Catalog.

## 📋 Overview

Automated export of EDC lineage relationships, data domain mappings, and source-to-target dependencies into CSV format with automatic ZIP archiving.

## 🎯 Features

- **Lineage Export**: Export complete data lineage relationships
- **Source-to-Target Mapping**: Column-level lineage tracking
- **Data Domain Integration**: Lineage filtered by data domains
- **CSV Output**: Structured CSV files for analysis
- **ZIP Archiving**: Automatic timestamped ZIP archives
- **PostgreSQL Logging**: Execution tracking and audit trail
- **Email Notifications**: Optional success/failure notifications
- **Environment Filtering**: Filter lineage by custom environment facets

## 📦 Prerequisites

### Software Requirements

- **Python 3.6+**
- **Informatica EDC** (tested with 10.4.1+)
- **PostgreSQL** (for execution logging)

### Python Dependencies

```bash
pip install -r requirements.txt
```

Key libraries:
- requests - REST API calls
- pandas - Data manipulation
- beautifulsoup4 - HTML/XML parsing
- psycopg2 - PostgreSQL connectivity
- python-dotenv - Environment variable management

## 🚀 Installation

1. Clone or download this project:
   ```bash
   cd informatica-automation-examples/edclineage-bulk-export
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your EDC credentials
   ```

## ⚙️ Configuration

### Environment Variables (.env)

Create a `.env` file in the project root:

```bash
# EDC Credentials
EDC_FE_USER=your_username
EDC_FE_PWD=your_password
EDC_FE_URL=https://edc.example.com:9085

# PostgreSQL Database (for logging)
EDC_PS_HOST=postgres.example.com
EDC_PS_PORT=5432
EDC_PS_DB=edc_logs
EDC_PS_USER=postgres_user
EDC_PS_PWD=postgres_password

# Lineage environment filter (optional)
EDC_ENV_FLTR=%7B!tag%3Dcustom_facet%7D...
```

**IMPORTANT:** Never commit the `.env` file with real credentials.

### Lineage Filtering

The script supports filtering lineage by:
- **Data Domain**: `DD_for_Lineage` (configurable in paramsEdc.py)
- **Basic Query**: `*_Totale` (filters by naming pattern)
- **Environment**: Custom facet filter via `EDC_ENV_FLTR`

## 📖 Usage

### Basic Usage

```bash
python runEdcLineage.py
```

The script runs without command-line parameters and uses configuration from `.env`.

### Output Files

The script generates:

1. **CSV Export** (in `EDC/` directory during processing):
   - Lineage relationships
   - Column-level dependencies
   - Data domain associations

2. **ZIP Archive** (in `../../out/` directory):
   - `LINEAGE_EDC_YYYYMMDD_HHMMSS.zip` - Contains all lineage CSV files

3. **Log File**:
   - `runEdcLineage.log` - Detailed execution log

## 🔧 Script Components

### Main Scripts

| Script | Purpose |
|--------|---------|
| `runEdcLineage.py` | Main orchestrator |
| `getLineages.py` | Extract lineage relationships |

### Support Modules

| Module | Purpose |
|--------|---------|
| `props/paramsEdc.py` | Configuration parameters |
| `props/utils.py` | Utility functions |
| `props/response_code.txt` | HTTP response code reference |
| `db/` | Database logging functions |
| `mailing/` | Email notification templates |

## 🔄 Workflow

1. **Initialization**
   - Load environment variables
   - Configure logging

2. **Authentication**
   - Connect to EDC REST API
   - Authenticate with credentials

3. **Lineage Export**
   - Query lineage relationships
   - Process data domains
   - Extract column-level dependencies
   - Save to CSV files

4. **Archiving**
   - Collect all CSV files
   - Create timestamped ZIP archive
   - Optionally clean up temporary files

5. **Notification** (optional)
   - Send email notification
   - Log execution status to database

## 🔐 Security Best Practices

See [SECURITY.md](../edc-automation/SECURITY.md) for detailed security guidelines.

**Critical Reminders:**
- ⚠️ Never commit `.env` file with real credentials
- ⚠️ Use environment variables for all sensitive data
- ⚠️ Restrict file permissions on configuration files
- ⚠️ Use dedicated service accounts with minimal permissions

## 🐛 Troubleshooting

### Common Issues

#### Authentication Failure
```
401 Unauthorized
```
**Solution:** Verify credentials in `.env` file, check EDC URL

#### Database Connection Error
```
psycopg2.OperationalError: could not connect to server
```
**Solution:** Verify PostgreSQL connection parameters in `.env`

#### Empty Lineage Export
```
No lineage found
```
**Solution:**
- Verify data domain name (`lineageDomain` in paramsEdc.py)
- Check basic query filter
- Verify environment facet filter (`EDC_ENV_FLTR`)

### Debug Mode

Check the log file for detailed information:
```bash
tail -f runEdcLineage.log
```

## 📁 Project Structure

```
edclineage-bulk-export/
├── runEdcLineage.py             # Main entry point
├── getLineages.py               # Lineage extraction logic
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment config
├── README.md                    # This file
├── props/
│   ├── paramsEdc.py            # Configuration parameters
│   ├── utils.py                # Utility functions
│   ├── requirements.txt        # Legacy requirements file
│   └── response_code.txt       # HTTP codes reference
├── db/                         # Database logging
├── mailing/                    # Email templates
└── out/                        # Output directory (auto-created)
    └── LINEAGE_EDC_*.zip      # Exported ZIP files
```

## 📚 Additional Resources

- [Informatica EDC Documentation](https://docs.informatica.com/data-catalog/enterprise-data-catalog.html)
- [EDC REST API Reference](https://docs.informatica.com/data-catalog/enterprise-data-catalog/current-version/rest-api-reference.html)
- [EDC Lineage Guide](https://docs.informatica.com/data-catalog/enterprise-data-catalog/current-version/lineage.html)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for details.

## 🤝 Contributing

This is a personal portfolio project, but suggestions and feedback are welcome through GitHub Issues.

## 📧 Contact

**Lorenzo Lombardi**
- LinkedIn: [linkedin.com/in/lorenzolombardi](https://www.linkedin.com/in/lorenzolombardi/)
- GitHub: [github.com/thrama](https://github.com/thrama)
