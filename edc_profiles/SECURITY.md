# Security Guidelines

## Overview

This document outlines security best practices for deploying and using the EDC Group Permission Automation tool in production environments.

## 🔐 Critical Security Requirements

### 1. Never Commit Credentials

**❌ NEVER DO THIS:**

```python
# In globalparams.py
catalogPassword = "MyRealPassword123"  # BAD!
```

**✅ DO THIS INSTEAD:**

```python
# In globalparams.py
import os
catalogPassword = os.environ.get('EDC_CATALOG_PASSWORD')
```

### 2. Use .gitignore Properly

Ensure these files are in your `.gitignore`:

```
globalparams.py
*.env
.env.*
*.log
config.ini
secrets.yaml
```

### 3. Protect Configuration Files

Set appropriate file permissions:

```bash
chmod 600 globalparams.py  # Read/write for owner only
chmod 600 .env             # Read/write for owner only
```

## 🛡️ Production Deployment Best Practices

### Option 1: Environment Variables (Recommended)

#### Linux/macOS Setup

```bash
# Add to ~/.bashrc or ~/.zshrc
export EDC_CATALOG_USER="Administrator"
export EDC_CATALOG_PASSWORD="your-secure-password"
export EDC_DIS_PASSWORD="your-dis-password"
export EDC_AGENT_PASSWORD="your-agent-password"
```

#### Windows Setup

```powershell
# PowerShell
$env:EDC_CATALOG_USER = "Administrator"
$env:EDC_CATALOG_PASSWORD = "your-secure-password"

# Or use System Properties > Environment Variables
```

#### Updated globalparams.py

```python
import os
import sys

# Catalog credentials
catalogUser = os.environ.get('EDC_CATALOG_USER')
catalogPassword = os.environ.get('EDC_CATALOG_PASSWORD')

# DIS credentials
disPassword = os.environ.get('EDC_DIS_PASSWORD')

# Agent credentials
agentPassword = os.environ.get('EDC_AGENT_PASSWORD')

# Validate that all required variables are set
required_vars = ['EDC_CATALOG_USER', 'EDC_CATALOG_PASSWORD', 'EDC_DIS_PASSWORD']
missing_vars = [var for var in required_vars if not os.environ.get(var)]

if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)
```

### Option 2: .env File with python-dotenv

#### Install python-dotenv

```bash
pip install python-dotenv
```

#### Create .env file

```bash
# .env (add to .gitignore!)
EDC_CATALOG_USER=Administrator
EDC_CATALOG_PASSWORD=your-secure-password
EDC_DIS_PASSWORD=your-dis-password
EDC_AGENT_PASSWORD=your-agent-password
EDC_CATALOG_HOST=edc-catalog.example.com
EDC_CATALOG_PORT=9086
```

#### Updated globalparams.py

```python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuration
catalogUser = os.getenv('EDC_CATALOG_USER')
catalogPassword = os.getenv('EDC_CATALOG_PASSWORD')
catalogHost = os.getenv('EDC_CATALOG_HOST')
catalogPort = os.getenv('EDC_CATALOG_PORT')
```

### Option 3: HashiCorp Vault (Enterprise)

For large enterprises, consider using a secrets management system:

```python
import hvac

# Initialize Vault client
client = hvac.Client(url='https://vault.example.com')
client.token = os.environ.get('VAULT_TOKEN')

# Retrieve secrets
secrets = client.secrets.kv.v2.read_secret_version(path='edc/credentials')
catalogPassword = secrets['data']['data']['catalog_password']
```

### Option 4: AWS Secrets Manager

For AWS deployments:

```python
import boto3
import json

def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')

    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])
    return secret

# Usage
edc_secrets = get_secret('edc/production/credentials')
catalogPassword = edc_secrets['catalog_password']
```

## 🔒 Network Security

### 1. Use HTTPS/TLS

Always use HTTPS for API communications:

```python
# In resources.py and groups.py
response = requests.get(
    url,
    headers=headers,
    verify=True,  # Enable certificate verification
    auth=HTTPBasicAuth(user, password)
)
```

### 2. Certificate Verification

**For Production:**

```python
# Use proper certificate verification
verify=True
# Or specify certificate bundle
verify='/path/to/ca-bundle.crt'
```

**For Development Only:**

```python
# Only in dev environments
verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

### 3. Firewall Rules

Ensure proper firewall configuration:

- Allow HTTPS (443) to EDC Catalog
- Allow port 6005 for DIS connections
- Restrict source IPs where possible
- Use VPN for remote access

## 👤 Access Control

### 1. Principle of Least Privilege

Create dedicated service accounts with minimal permissions:

```python
# Instead of using Administrator
catalogUser = "edc_automation_svc"
```

### 2. Role-Based Access

- Create specific roles for automation
- Limit scope to required operations
- Regular permission audits

### 3. Audit Logging

Enhanced logging for security events:

```python
import logging

# Configure security logging
security_logger = logging.getLogger('security')
handler = logging.FileHandler('security.log')
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - USER:%(user)s - ACTION:%(action)s'
))
security_logger.addHandler(handler)

# Log security events
security_logger.info('Permission granted', extra={
    'user': current_user,
    'action': 'grant_resource_access',
    'resource': resource_name,
    'group': group_name
})
```

## 🔍 Security Monitoring

### 1. Log Review

Regularly review logs for:

- Failed authentication attempts
- Unauthorized access attempts
- Unusual permission changes
- Error patterns

```bash
# Example log analysis
grep "Error: RestAPI error" main.log
grep "Failed to" main.log
grep "Permission denied" main.log
```

### 2. Alerts

Set up alerts for:

- Multiple failed login attempts
- Modifications to critical resources
- Unexpected script executions

## 🔄 Password Management

### 1. Password Rotation

Implement regular password rotation:

```bash
# Rotate every 90 days
# Update in your secrets management system
# Never hardcode in scripts
```

### 2. Strong Password Policy

- Minimum 16 characters
- Mix of uppercase, lowercase, numbers, symbols
- No dictionary words
- Use password manager

### 3. Encrypted Storage

If you must store passwords in files:

```python
from cryptography.fernet import Fernet

# Generate key (do this once, store securely)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt password
encrypted_password = cipher.encrypt(b"my-secret-password")

# Decrypt when needed
decrypted_password = cipher.decrypt(encrypted_password).decode()
```

## 📋 Security Checklist

Before deploying to production:

- [ ] All credentials stored in environment variables or secrets manager
- [ ] `globalparams.py` added to `.gitignore`
- [ ] No hardcoded passwords in any files
- [ ] HTTPS/TLS enabled with certificate verification
- [ ] Service account created with minimal permissions
- [ ] File permissions set correctly (600 for config files)
- [ ] Logging configured for security events
- [ ] Regular password rotation schedule established
- [ ] Backup and recovery procedures documented
- [ ] Security review completed
- [ ] Penetration testing performed (if required)

## 🚨 Incident Response

If credentials are compromised:

1. **Immediate Actions:**

   - Revoke compromised credentials
   - Reset all related passwords
   - Review access logs
   - Identify affected resources

2. **Investigation:**

   - Determine scope of compromise
   - Review recent activities
   - Check for unauthorized changes

3. **Remediation:**
   - Rotate all credentials
   - Update secrets in secure storage
   - Review and update security policies
   - Document lessons learned

## 📞 Security Contacts

- **Security Team:** security@yourcompany.com
- **Incident Response:** incident-response@yourcompany.com
- **IT Support:** itsupport@yourcompany.com

## 🔗 Additional Resources

- [OWASP Security Guidelines](https://owasp.org/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [Informatica EDC Security Guide](https://docs.informatica.com/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## 📝 Compliance

### GDPR Considerations

- Ensure personal data in logs is pseudonymized
- Implement data retention policies
- Provide audit trails

### SOC 2 / ISO 27001

- Document all security controls
- Regular security assessments
- Access control reviews
- Change management procedures

---

**Remember:** Security is not a one-time task but an ongoing process. Regularly review and update your security practices.
