# Informatica Automation Examples

A collection of Python and Bash automation scripts for Informatica products, including PowerCenter, Enterprise Data Catalog (EDC), Axon, Data Quality, and Informatica Intelligent Data Management Cloud (IDMC).

## 📋 Overview

This repository contains practical examples and automation tools for common Informatica administration and data governance tasks. All scripts are designed to be educational resources demonstrating integration with Informatica REST APIs, ODBC connections, and multi-database platforms.

**Author:** Lorenzo Lombardi
**LinkedIn:** [linkedin.com/in/lorenzolombardi](https://www.linkedin.com/in/lorenzolombardi/)
**GitHub:** [github.com/thrama](https://github.com/thrama)

## 🚀 Projects Overview

### Enterprise Data Catalog (EDC)

| Project                                             | Description                                         | Status         | Language |
| --------------------------------------------------- | --------------------------------------------------- | -------------- | -------- |
| [edc-automation](./edc-automation/)                 | Automated creation of EDC connections and resources | ✅ Complete    | Python   |
| [edc-bulk-export](./edc-bulk-export/)               | Bulk export of EDC resources and metadata           | 🚧 In Progress | Python   |
| [edc-bulk-delete](./edc-bulk-delete/)               | Bulk deletion of EDC resources with safety checks   | 🚧 In Progress | Python   |
| [edc-profiles](./edc-profiles/)                     | Management of EDC user profiles and groups          | 🚧 In Progress | Python   |
| [edclineage-bulk-export](./edclineage-bulk-export/) | Export lineage information from EDC catalog         | 🚧 In Progress | Python   |

### Axon Data Governance

| Project                                 | Description                          | Status      | Language |
| --------------------------------------- | ------------------------------------ | ----------- | -------- |
| [axon-bulk-export](./axon-bulk-export/) | Export Axon facets and relationships | ✅ Complete | Python   |

### Infrastructure & Monitoring

| Project                                         | Description                                | Status         | Language |
| ----------------------------------------------- | ------------------------------------------ | -------------- | -------- |
| [monitoring](./monitoring/)                     | Health monitoring for Informatica services | 🚧 In Progress | Bash     |
| [metadex-resource-run](./metadex-resource-run/) | Automated execution of EDC scanners        | 🚧 In Progress | Bash     |
| [scripts-start-stop](./scripts-start-stop/)     | Service management scripts                 | 🚧 In Progress | Bash     |

### Utilities

| Project         | Description                                           | Status         | Language    |
| --------------- | ----------------------------------------------------- | -------------- | ----------- |
| [misc](./misc/) | Miscellaneous utilities (backups, connectivity tests) | 🚧 In Progress | Python/Bash |

## ⚙️ Technology Stack

- **Python 3.x** - Primary automation language
- **Bash** - System scripts and service management
- **REST APIs** - Informatica EDC, Axon, IDMC APIs
- **ODBC** - Multi-database connectivity
- **Supported Databases**: DB2, Oracle, SQL Server, Teradata, Hive, MongoDB

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager
- ODBC drivers for target databases (if using database connectivity features)
- Informatica EDC/Axon environment access

### Common Python Dependencies

Most projects require these libraries:

```bash
pip install requests pyexcel pyexcel-xls pyexcel-xlsx
```

Specific requirements are documented in each project's README.md file.

## 🔐 Security Best Practices

**IMPORTANT:** These scripts contain generic placeholder configurations. Before deploying to production:

1. **Never hardcode credentials** - Use environment variables or secure credential stores
2. **Use HTTPS** - Always use encrypted connections for API calls
3. **Implement access controls** - Restrict script execution to authorized users
4. **Audit logging** - Enable comprehensive logging for all operations
5. **Regular updates** - Keep dependencies updated to address security vulnerabilities

See individual project SECURITY.md files for detailed security guidelines.

## 📚 Documentation

Each project directory contains:

- **README.md** - Detailed usage instructions and examples
- **SECURITY.md** - Security considerations and best practices
- **requirements.txt** - Python dependencies (where applicable)

## 🤝 Contributing

While this is a personal portfolio repository, suggestions and feedback are welcome through GitHub Issues.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

These scripts are provided as **educational examples** and should be thoroughly tested and adapted for your specific environment before production use. Always follow your organization's security policies and best practices.

## 📧 Contact

**Lorenzo Lombardi**

- LinkedIn: [linkedin.com/in/lorenzolombardi](https://www.linkedin.com/in/lorenzolombardi/)
- GitHub: [github.com/thrama](https://github.com/thrama)

---

**Note:** All examples use generic configurations and placeholder values. Replace with your actual environment settings before use.
