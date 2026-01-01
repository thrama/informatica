# Informatica EDC Automation Framework

> Python automation framework for Informatica Enterprise Data Catalog (EDC) connections and resources management

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Project Overview

This project demonstrates enterprise-level automation for Informatica's Enterprise Data Catalog, streamlining the creation and management of data connections and catalog resources across multiple database technologies.

**Key Achievement**: Reduced manual configuration time by ~80% for EDC deployments through automated connection and resource provisioning.

## 💼 Professional Context

Developed as part of Data Governance initiatives to accelerate EDC deployment and configuration. This framework enables rapid onboarding of data sources into the catalog while maintaining consistency and reducing human error.

## 🚀 Technical Highlights

### Architecture & Design Patterns

- **Object-Oriented Design**: Modular class structure for maintainability
- **Strategy Pattern**: Technology-specific handlers (DB2, Oracle, SQL Server, Teradata, Hive)
- **Template Method Pattern**: Reusable ODBC and JSON configuration generation
- **Error Handling**: Comprehensive logging and exception management

### Technology Stack

- **Python 3.x**: Core language
- **REST API Integration**: Informatica EDC API interaction
- **Excel Processing**: Automated data ingestion via `pyexcel`
- **ODBC Configuration**: Template-based configuration file generation
- **JSON Schema**: Dynamic resource definition creation

### Supported Database Technologies

- IBM DB2 z/OS
- Microsoft SQL Server
- Oracle Database
- Teradata
- Apache Hive
- MongoDB (framework ready)

## 🏗️ Architecture

```
┌─────────────────┐
│   Excel Input   │
│  (Data Source)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   main.py       │
│  (Orchestrator) │
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
         ▼                 ▼
┌─────────────┐   ┌──────────────┐
│ Connections │   │  Resources   │
│   Module    │   │    Module    │
└──────┬──────┘   └──────┬───────┘
       │                 │
       ▼                 ▼
┌─────────────┐   ┌──────────────┐
│ ODBC Config │   │  REST API    │
│ Generation  │   │   Calls      │
└─────────────┘   └──────────────┘
```

## 🔧 Core Capabilities

### 1. Connection Automation

- Automated creation of EDC connections via `infacmd` CLI
- Dynamic ODBC configuration file generation
- Support for Windows Authentication (NTLM)
- DSN name validation and normalization (32-char limit)

### 2. Resource Automation

- REST API-based resource provisioning
- Fallback JSON file generation for manual import
- Template-driven configuration
- Comprehensive error handling and status reporting

### 3. Configuration Management

- Environment-specific parameter externalization
- Template-based ODBC and JSON generation
- Secure credential handling guidelines

## 💡 Key Features

- **Bulk Processing**: Process multiple connections/resources from single Excel file
- **Technology Agnostic**: Extensible framework for adding new database types
- **Idempotent Operations**: Safe to re-run without side effects
- **Audit Trail**: Comprehensive logging of all operations
- **Error Recovery**: Automatic fallback to JSON file generation on API failure

## 📊 Skills Demonstrated

### Technical Skills

- **Python Development**: OOP, error handling, file I/O, API integration
- **Data Governance**: EDC architecture, metadata management
- **Database Technologies**: Multi-platform database connectivity
- **REST API**: HTTP methods, authentication, status code handling
- **ODBC**: Configuration, DSN management, driver specifics
- **DevOps**: Configuration management, logging, error handling

### Informatica Expertise

- Enterprise Data Catalog (EDC) architecture
- Informatica command-line tools (`infacmd`)
- EDC REST API
- Connection and resource management
- ODBC integration

### Software Engineering

- Modular design and code organization
- Template Method and Strategy patterns
- Exception handling and logging
- Configuration externalization
- Documentation best practices

## 🔒 Security Considerations

- **Credential Management**: Externalized configuration with `.gitignore` protection
- **Template System**: Example configuration files prevent credential exposure
- **Best Practices**: Documented in `SECURITY.md`

## 📈 Performance & Impact

**Efficiency Gains:**

- Manual connection creation: ~5-10 minutes per connection
- Automated approach: ~30 seconds per connection
- **Time savings: 90%+ for bulk operations**

**Quality Improvements:**

- Eliminated configuration errors from manual entry
- Consistent ODBC configuration across environments
- Standardized resource definitions

## 🛠️ Usage Examples

### Create Connections

```bash
python main.py -t sqlsrv -x data/connections.xlsx -c
```

### Create Resources

```bash
python main.py -t oracle -x data/resources.xlsx -r
```

## 📚 Documentation

- **[README.md](README.md)**: Complete installation and usage guide
- **[SECURITY.md](SECURITY.md)**: Security best practices and configuration
- **[ANONIMIZZAZIONE_RIEPILOGO.md](ANONIMIZZAZIONE_RIEPILOGO.md)**: Anonymization details

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

- Enterprise data catalog implementation
- Python automation and scripting
- REST API integration
- Multi-database connectivity
- Configuration management
- Error handling and logging
- Technical documentation

## 📞 Author

**Lorenzo Lombardi**
Principal Data Architect @ NTT Data Italia

_Specializing in Data Governance and Informatica Enterprise Solutions_

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

_This is a portfolio project demonstrating enterprise automation capabilities. All sensitive information has been removed for public sharing._
