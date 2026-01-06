# Security Guidelines

## 🔐 Security Best Practices for EDC Automation

This document outlines critical security considerations when deploying EDC automation scripts in production environments.

## ⚠️ Critical Security Warnings

### 1. Credential Management

**NEVER** commit files containing real credentials to version control:

❌ **BAD - Hardcoded Credentials**

```python
domainPassword = "MyRealPassword123!"  # DO NOT DO THIS
catalogPassword = "SecretPass2024"     # DO NOT DO THIS
```

✅ **GOOD - Environment Variables**

```python
import os
domainPassword = os.getenv('INFA_DOMAIN_PASSWORD')
catalogPassword = os.getenv('INFA_CATALOG_PASSWORD')
```

✅ **GOOD - Secure Credential Store**

```python
from credentialstore import get_credential
domainPassword = get_credential('informatica', 'domain_password')
```

### 2. SSL/TLS Configuration

**Current Implementation (INSECURE):**

```python
response = requests.post(url)
```

**Production Implementation (SECURE):**

```python
response = requests.post(
    url,
    verify=True,  # Enable SSL verification
    # OR specify custom CA bundle:
    verify='/path/to/ca-bundle.crt'
)
```

### 3. File Permissions

Protect configuration files containing sensitive data:

```bash
# Restrict access to configuration files
chmod 600 globalparams.py
chmod 600 config.py

# Ensure output directory has proper permissions
chmod 700 resultFile/

# Set ownership
chown informatica:informatica *.py
```

### 4. LDAP Domain Configuration

Replace generic LDAP domain with your actual domain, but never commit it:

```python
# Use environment variable
ldapDomain = os.getenv('LDAP_DOMAIN', 'CORP')

# Or configuration management system
ldapDomain = config_manager.get('ldap_domain')
```

## 🛡️ Production Deployment Checklist

### Pre-Deployment

- [ ] Remove or replace all hardcoded credentials
- [ ] Update SSL verification to `verify=True`
- [ ] Configure credential storage solution (HashiCorp Vault, AWS Secrets Manager, etc.)
- [ ] Set appropriate file permissions (600 for sensitive files)
- [ ] Add `globalparams.py` to `.gitignore`
- [ ] Review and update LDAP domain configuration
- [ ] Test with non-production credentials first

### Infrastructure

- [ ] Deploy scripts on secure, access-controlled servers
- [ ] Implement network segmentation (separate management networks)
- [ ] Enable firewall rules (allow only necessary EDC ports)
- [ ] Use secure file transfer methods (SFTP, not FTP)
- [ ] Implement log rotation and retention policies
- [ ] Configure monitoring and alerting

### Access Control

- [ ] Create dedicated service account for automation
- [ ] Apply principle of least privilege (minimal required permissions)
- [ ] Disable interactive login for service accounts
- [ ] Implement multi-factor authentication where possible
- [ ] Regular access reviews and audits
- [ ] Separate development and production credentials

### Operational Security

- [ ] Enable comprehensive audit logging
- [ ] Implement log centralization (SIEM integration)
- [ ] Regular vulnerability scanning
- [ ] Dependency version management (security patches)
- [ ] Incident response plan documented
- [ ] Regular security training for team

## 🔑 Recommended Credential Management Approaches

### Option 1: Environment Variables

**Setup:**

```bash
# Create .env file (add to .gitignore!)
cat > .env <<EOF
INFA_DOMAIN_PASSWORD=YourSecurePassword
INFA_CATALOG_PASSWORD=YourSecurePassword
LDAP_DOMAIN=YOURDOMAIN
EOF

# Load environment variables
source .env
```

**Usage in Python:**

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

domainPassword = os.getenv('INFA_DOMAIN_PASSWORD')
catalogPassword = os.getenv('INFA_CATALOG_PASSWORD')
ldapDomain = os.getenv('LDAP_DOMAIN')
```

### Option 2: HashiCorp Vault

```python
import hvac

# Initialize Vault client
client = hvac.Client(url='https://vault.example.com:8200')
client.token = os.getenv('VAULT_TOKEN')

# Retrieve secrets
secrets = client.secrets.kv.v2.read_secret_version(path='informatica/prod')
domainPassword = secrets['data']['data']['domain_password']
catalogPassword = secrets['data']['data']['catalog_password']
```

### Option 3: AWS Secrets Manager

```python
import boto3
import json

# Create Secrets Manager client
session = boto3.session.Session()
client = session.client(service_name='secretsmanager')

# Retrieve secret
secret_value = client.get_secret_value(SecretId='informatica/credentials')
secrets = json.loads(secret_value['SecretString'])

domainPassword = secrets['domain_password']
catalogPassword = secrets['catalog_password']
```

## 📝 Logging Security

### Secure Logging Practices

```python
import logging

# Configure logging to exclude sensitive data
logging.basicConfig(
    filename='main.log',
    level=logging.INFO,  # Avoid DEBUG in production
    format='%(asctime)s %(levelname)s %(message)s'
)

# NEVER log passwords or sensitive data
logging.info(f"Creating connection: {connectionName}")  # OK
logging.info(f"Password: {password}")  # NEVER DO THIS
```

### Log File Protection

```bash
# Set restrictive permissions on log files
chmod 640 main.log
chown informatica:informatica main.log

# Implement log rotation
cat > /etc/logrotate.d/edc-automation <<EOF
/path/to/edc-automation/main.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
    create 0640 informatica informatica
}
EOF
```

## 🌐 Network Security

### Firewall Configuration

Allow only required EDC ports:

```bash
# Data Integration Service (DIS)
iptables -A INPUT -p tcp --dport 6005 -s trusted_ip -j ACCEPT

# EDC Catalog Service
iptables -A INPUT -p tcp --dport 9086 -s trusted_ip -j ACCEPT

# MIMB Agent
iptables -A INPUT -p tcp --dport 19980 -s trusted_ip -j ACCEPT

# Block all other incoming
iptables -A INPUT -j DROP
```

### HTTPS/SSL Configuration

Always use HTTPS for API connections:

```python
# Ensure URL uses HTTPS
url = f"https://{catalogHost}:{catalogPort}/access/1/catalog/resources"

# Verify SSL certificate
response = requests.post(url, verify=True, ...)

# For custom CA certificates
response = requests.post(url, verify='/etc/ssl/certs/ca-bundle.crt', ...)
```

## 🔄 Credential Rotation

Implement regular credential rotation:

```bash
#!/bin/bash
# Example credential rotation script

# 1. Generate new password
NEW_PASSWORD=$(openssl rand -base64 32)

# 2. Update in Informatica
infacmd.sh isp UpdateUser \
    -UserName Administrator \
    -Password $NEW_PASSWORD

# 3. Update in credential store
vault kv put secret/informatica/prod \
    domain_password="$NEW_PASSWORD"

# 4. Restart services (if needed)
systemctl restart informatica-services
```

## 📊 Security Monitoring

### Key Metrics to Monitor

- Failed login attempts
- Unauthorized API calls
- File permission changes
- Unusual connection patterns
- Resource creation/deletion activities

### Example Monitoring Script

```bash
#!/bin/bash
# Monitor for suspicious activity

# Check for failed login attempts
grep "Unauthorized" main.log | \
    awk '{print $1, $2}' | \
    sort | uniq -c | \
    awk '$1 > 5 {print "Alert: " $1 " failed attempts at " $2 " " $3}'

# Alert on sensitive file changes
inotifywait -m -e modify globalparams.py | \
    while read; do
        echo "ALERT: globalparams.py was modified" | \
        mail -s "Security Alert" security@example.com
    done
```

## 🚨 Incident Response

### If Credentials are Compromised

1. **Immediate Actions:**

   ```bash
   # Disable compromised account
   infacmd.sh isp DisableUser -UserName Administrator

   # Revoke API tokens
   # Check for unauthorized resources/connections
   infacmd.sh isp ListConnections
   ```

2. **Investigation:**

   - Review access logs
   - Identify affected systems
   - Determine blast radius

3. **Remediation:**

   - Rotate all credentials
   - Remove unauthorized resources
   - Update access controls
   - Patch vulnerabilities

4. **Post-Incident:**
   - Document incident
   - Update security procedures
   - Conduct lessons learned

## 📚 Compliance Considerations

### Data Protection Regulations

- **GDPR**: Ensure proper handling of European personal data
- **HIPAA**: Protect healthcare-related information
- **PCI-DSS**: Secure payment card data
- **SOX**: Maintain audit trails for financial data

### Audit Requirements

Maintain logs that capture:

- Who executed the script
- When it was executed
- What actions were performed
- Success/failure status
- Any errors or exceptions

## 🔍 Security Testing

### Regular Security Assessments

```bash
# Check for hardcoded credentials
grep -r "password.*=" *.py | grep -v "getenv\|get_credential"

# Scan for security vulnerabilities
pip install safety
safety check

# Check file permissions
find . -type f -name "*.py" -perm /go+w

# Scan for secrets in git history
git secrets --scan-history
```

## 📞 Security Contact

For security concerns or to report vulnerabilities:

- **LinkedIn:** [linkedin.com/in/lorenzolombardi](https://www.linkedin.com/in/lorenzolombardi/)
- **GitHub Issues:** [github.com/thrama/informatica-automation-examples/issues](https://github.com/thrama/informatica-automation-examples/issues) (for non-sensitive issues)

**For sensitive security issues, please contact directly via LinkedIn.**
