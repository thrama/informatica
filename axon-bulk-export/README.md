# Axon Bulk Export

Automated export of data from Informatica Axon Data Governance using REST APIs and PostgreSQL database queries.

## 📋 Overview

This project automates the bulk export of Axon facets, relationships, and metadata into CSV files. It supports both facets with and without relationships, and can export system resource mappings from EDC.

## 🎯 Features

- **Facet Export**: Export facets with and without relationships
- **System Resources**: Export EDC-Axon system resource mappings
- **Parallel Processing**: Uses Python multiprocessing for faster exports
- **Database Logging**: Tracks export execution in PostgreSQL
- **Automatic Archiving**: Creates timestamped ZIP files of exported data
- **Environment-Based Configuration**: Secure credential management via .env files

## 📦 Prerequisites

### Software Requirements

- **Python 3.6.8+**
- **Informatica Axon** (tested with 7.x)
- **PostgreSQL** (for execution logging)

### Python Dependencies

```bash
pip install -r requirements.txt
```

Key libraries:

- requests - REST API calls
- pandas - Data manipulation
- psycopg2-binary - PostgreSQL connectivity
- python-dotenv - Environment variable management
- beautifulsoup4 - HTML/XML parsing
- lxml - XML processing

## 🚀 Installation

1. Clone or download this project:

   ```bash
   cd informatica-automation-examples/axon-bulk-export
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your Axon credentials
   ```

4. (Optional) Create executable with PyInstaller:
   ```bash
   pyinstaller -D --noconfirm --distpath bin/ runAxon.py
   ```

## ⚙️ Configuration

### Environment Variables (.env)

Create a `.env` file in the project root with the following variables:

```bash
# Axon Frontend Credentials
AXON_FE_USER=your_username
AXON_FE_PWD=your_password
AXON_FE_URL=https://axon.example.com:8080

# PostgreSQL Database (for logging)
AXON_PS_HOST=postgres.example.com
AXON_PS_PORT=5432
AXON_PS_DB=axon_logs
AXON_PS_USER=postgres_user
AXON_PS_PWD=postgres_password
```

**IMPORTANT:** Never commit the `.env` file with real credentials.

### Configuration Files

#### `props/paramsAxon.py`

Contains runtime parameters:

- API endpoints
- Export paths
- Page limits for facets and relationships
- Character filters for data cleaning

#### `db/database.py`

PostgreSQL connection and logging functions.

## 📖 Usage

### Basic Usage

```bash
python runAxon.py
```

The script runs without command-line parameters and uses configuration from `.env` file.

### Using Executable (if built with PyInstaller)

```bash
./bin/runAxon/runAxon
```

### Output Files

The script generates:

1. **CSV Exports** (in `../AXON/` directory during processing):

   - Facets without relationships
   - Facets with relationships
   - System resource mappings

2. **ZIP Archive** (in `../../out/` directory):

   - `AXON_YYYYMMDD_HHMMSS.zip` - Contains all CSV files

3. **Log File**:
   - `runAxon.log` - Detailed execution log

## 🔧 Script Components

### Main Scripts

| Script                   | Purpose                                              |
| ------------------------ | ---------------------------------------------------- |
| `runAxon.py`             | Main orchestrator - coordinates all export processes |
| `getFacetsNoRel.py`      | Export facets without relationships                  |
| `getFacetsWithRel.py`    | Export facets with relationships                     |
| `getSystemRelEdc.py`     | Export EDC-Axon system mappings                      |
| `facetOptionsNoRel.py`   | Configuration for no-relation facets                 |
| `facetOptionsWithRel.py` | Configuration for relation facets                    |

### Support Modules

| Module                    | Purpose                      |
| ------------------------- | ---------------------------- |
| `props/paramsAxon.py`     | Configuration parameters     |
| `props/utils.py`          | Utility functions            |
| `props/response_code.txt` | HTTP response code reference |
| `db/database.py`          | Database logging functions   |
| `db/init.py`              | Database initialization      |

## 🔄 Workflow

1. **Authentication**

   - Connects to Axon API
   - Generates bearer token
   - Logs authentication status to database

2. **Parallel Export** (using multiprocessing)

   - Process 1: Export facets without relationships
   - Process 2: Export facets with relationships
   - Process 3: Export system resources

3. **Archiving**

   - Collects all CSV files
   - Creates timestamped ZIP archive
   - Cleans up temporary files

4. **Cleanup**
   - Removes temporary CSV directory
   - Closes database connections

## 🔐 Security Best Practices

See [SECURITY.md](../edc-automation/SECURITY.md) for detailed security guidelines.

**Critical Reminders:**

- ⚠️ Never commit `.env` file with real credentials
- ⚠️ Use environment variables for all sensitive data
- ⚠️ Enable SSL verification in production (currently disabled for demo)
- ⚠️ Restrict file permissions on configuration files
- ⚠️ Use dedicated service accounts with minimal permissions

## 🐛 Troubleshooting

### Common Issues

#### Authentication Failure

```
No Response from server, error code: 401
```

**Solution:** Check credentials in `.env` file, verify Axon URL is accessible

#### Database Connection Error

```
psycopg2.OperationalError: could not connect to server
```

**Solution:** Verify PostgreSQL connection parameters in `.env`

#### SSL Verification Warnings

```
InsecureRequestWarning: Unverified HTTPS request
```

**Note:** Disable SSL verification in demo mode. In production environement  remove `verify=False` from requests.

### Debug Mode

Check the log file for detailed information:

```bash
tail -f runAxon.log
```

## 📁 Project Structure

```
axon-bulk-export/
├── runAxon.py                    # Main entry point
├── getFacetsNoRel.py             # Export facets without relations
├── getFacetsWithRel.py           # Export facets with relations
├── getSystemRelEdc.py            # Export EDC system mappings
├── facetOptionsNoRel.py          # No-relation facet config
├── facetOptionsWithRel.py        # With-relation facet config
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .env.example                  # Example environment config
├── props/
│   ├── paramsAxon.py            # Runtime parameters
│   ├── utils.py                 # Utility functions
│   └── response_code.txt        # HTTP codes reference
├── db/
│   ├── database.py              # Database functions
│   └── init.py                  # Database initialization
└── out/                         # Output directory (auto-created)
    └── AXON_*.zip              # Exported ZIP files
```

## 📚 Additional Resources

- [Informatica Axon Documentation](https://docs.informatica.com/data-governance/axon-data-governance.html)
- [Axon REST API Reference](https://docs.informatica.com/data-governance/axon-data-governance/current-version/rest-api-reference.html)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for details.

## 🤝 Contributing

This is a personal portfolio project, but suggestions and feedback are welcome through GitHub Issues.

## 📧 Contact

**Lorenzo Lombardi**

- LinkedIn: [linkedin.com/in/lorenzolombardi](https://www.linkedin.com/in/lorenzolombardi/)
- GitHub: [github.com/thrama](https://github.com/thrama)
