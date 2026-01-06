# Scripts Start & Stop

Service management scripts for Informatica components.

## 📋 Overview

Collection of start/stop scripts for various Informatica services and components.

## 🎯 Components Covered

- **Informatica Domain** - Domain service management
- **Axon** - Axon Data Governance services
- **Advanced Scanner** - EDC scanner services
- **DDM** - Data Domain Manager services

## 📦 Prerequisites

- Informatica installation
- Appropriate service permissions
- Bash shell

## ⚙️ Usage

Each component has dedicated start/stop scripts:

```bash
# Start a service
./{component}/start.sh

# Stop a service
./{component}/stop.sh

# Check status
./{component}/status.sh
```

## 🔐 Security

- Run scripts with appropriate service account
- Restrict permissions: `chmod 750 *.sh`
- Verify environment before execution

## 📄 License

Apache License 2.0

## 📧 Contact

**Lorenzo Lombardi**

- LinkedIn: [linkedin.com/in/lorenzolombardi](https://www.linkedin.com/in/lorenzolombardi/)
- GitHub: [github.com/thrama](https://github.com/thrama)
