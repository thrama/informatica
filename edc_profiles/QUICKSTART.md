# Quick Start Guide

Get up and running with EDC Group Permission Automation in 5 minutes!

## Prerequisites

- Python 3.6 or higher
- Informatica EDC 10.4.1 or higher
- Access to EDC with appropriate permissions
- Excel file with group/permission definitions

## Installation

### Step 1: Clone or Download

```bash
# Clone from GitHub
git clone https://github.com/yourusername/edc-group-automation.git
cd edc-group-automation

# Or download and extract ZIP
unzip edc-group-automation.zip
cd edc-group-automation
```

### Step 2: Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy configuration template
cp globalparams.py.example globalparams.py

# Edit with your EDC connection details
nano globalparams.py  # or use your preferred editor
```

Update these values in `globalparams.py`:

```python
# Domain Configuration
domainName = "YOUR_DOMAIN_NAME"
disName = "YOUR_DIS_NAME"

# Catalog Service
catalogHost = "your-catalog-host.example.com"
catalogPort = "9086"
catalogUser = "Administrator"
catalogPassword = "YOUR_PASSWORD"  # See security notes below

# DIS Configuration
disHost = "your-dis-host.example.com"
disPassword = "YOUR_PASSWORD"

# Agent Configuration
agentURL = "http://your-agent-host.example.com:19980/MIMBWebServices"
agentPassword = "YOUR_PASSWORD"
```

### Step 4: Set Environment Variable

```bash
# Linux/macOS
export INFA_HOME=/path/to/informatica/edc

# Windows (PowerShell)
$env:INFA_HOME = "C:\path\to\informatica\edc"
```

### Step 5: Prepare Excel File

Create an Excel file with these columns:

| Group        | Group Domain | Resource Name | Grant | Role | Tecnologia |
| ------------ | ------------ | ------------- | ----- | ---- | ---------- |
| DataAnalysts | Native       | OracleDB_HR   | READ  |      | Oracle     |

See [EXCEL_TEMPLATE.md](EXCEL_TEMPLATE.md) for detailed format.

### Step 6: Run the Script

```bash
python main.py --xls your_permissions_file.xlsx
```

## Example Usage

### Simple Example

```bash
# Assign permissions from Excel file
python main.py -x permissions.xlsx
```

### What Happens

1. ✓ Script reads Excel file
2. ✓ Validates resources exist in EDC
3. ✓ Creates groups if needed
4. ✓ Assigns permissions to resources
5. ✓ Logs all operations to main.log

### Expected Output

```
📊 Reading Excel file: permissions.xlsx
📋 Found 5 rows to process

Processing row 1/5...
✓ Successfully added permissions for resource [OracleDB_HR] in group [DataAnalysts].

Processing row 2/5...
✓ New group [Developers] created successfully

...

============================================================
📊 Processing Complete
============================================================
✓ Successful operations: 5
✗ Failed operations: 0
📝 Check 'main.log' for detailed information
============================================================
```

## Common Tasks

### Task 1: Assign Role to Group

Excel row:

```
Group: DataStewards
Group Domain: Native
Resource Name: (empty)
Grant: (empty)
Role: Data Steward
Tecnologia: (empty)
```

### Task 2: Grant Read Access

Excel row:

```
Group: Analysts
Group Domain: LDAP
Resource Name: OracleDB_Sales
Grant: READ
Role: (empty)
Tecnologia: Oracle
```

### Task 3: Grant Full Permissions

Excel row:

```
Group: Developers
Group Domain: Native
Resource Name: DB2_Dev
Grant: ALL PERMISSION
Role: (empty)
Tecnologia: DB2
```

## Troubleshooting

### Issue: Import Error

**Problem:** `ModuleNotFoundError: No module named 'pyexcel'`

**Solution:**

```bash
pip install -r requirements.txt
```

### Issue: Connection Error

**Problem:** Cannot connect to EDC

**Solution:**

1. Check `globalparams.py` settings
2. Verify network connectivity:
   ```bash
   ping your-catalog-host.example.com
   telnet your-catalog-host.example.com 9086
   ```
3. Check firewall rules

### Issue: Permission Denied

**Problem:** Authentication fails

**Solution:**

1. Verify credentials in `globalparams.py`
2. Check user has required EDC permissions
3. Try logging into EDC UI with same credentials

### Issue: Resource Not Found

**Problem:** `Error: Resource 'XYZ' does not exist`

**Solution:**

1. Verify resource name spelling (case-sensitive)
2. Check resource exists in EDC UI
3. Confirm you have access to view the resource

## Security Best Practices

### ⚠️ Important: Never Commit Credentials!

**Instead of hardcoding passwords:**

```bash
# Set environment variables
export EDC_CATALOG_PASSWORD="your-password"
export EDC_DIS_PASSWORD="your-password"
export EDC_AGENT_PASSWORD="your-password"
```

**Update globalparams.py:**

```python
import os
catalogPassword = os.environ.get('EDC_CATALOG_PASSWORD')
disPassword = os.environ.get('EDC_DIS_PASSWORD')
agentPassword = os.environ.get('EDC_AGENT_PASSWORD')
```

See [SECURITY.md](SECURITY.md) for complete security guidelines.

## Next Steps

1. **Review Logs:** Check `main.log` for detailed operation logs
2. **Verify in EDC:** Login to EDC UI and verify permissions
3. **Automate:** Add to cron job or CI/CD pipeline for regular updates
4. **Learn More:** Read full documentation in [README.md](README.md)

## Getting Help

- 📖 **Full Documentation:** [README.md](README.md)
- 🔐 **Security Guide:** [SECURITY.md](SECURITY.md)
- 📋 **Excel Format:** [EXCEL_TEMPLATE.md](EXCEL_TEMPLATE.md)
- 🐛 **Report Issues:** GitHub Issues
- 💬 **Questions:** GitHub Discussions

## Validation Checklist

Before running in production:

- [ ] `globalparams.py` configured with correct values
- [ ] `INFA_HOME` environment variable set
- [ ] Dependencies installed (`requirements.txt`)
- [ ] Excel file format validated
- [ ] Resources exist in EDC
- [ ] Credentials are secure (not hardcoded)
- [ ] Test run completed successfully
- [ ] Logs reviewed for errors

---

**Ready to go!** 🚀

Run: `python main.py -x your_file.xlsx`
