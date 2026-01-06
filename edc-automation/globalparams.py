###
# DATA: 08/07/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama
#
# DESCRIPTION:
# Global parameters for Informatica EDC environment configuration.
#
# SECURITY NOTICE:
# This file contains placeholder values for demonstration purposes only.
# In production environments:
# - Store credentials in environment variables or secure credential stores
# - Use encrypted connections (HTTPS/SSL)
# - Implement proper access controls
# - Never commit real credentials to version control
###

# =============================================================================
# INFORMATICA DOMAIN CONFIGURATION
# =============================================================================

# Domain name (typically named with environment suffix like _DEV, _PROD)
domainName = "Domain_EDC_DEV"

# Domain administrator credentials
# SECURITY: Use environment variables instead: os.getenv('INFA_DOMAIN_USER')
domainUser = "Administrator"
domainPassword = "ChangeMe123!"  # Replace with actual credential management

# =============================================================================
# DATA INTEGRATION SERVICE (DIS) CONFIGURATION
# =============================================================================

# Data Integration Service name
disName = "DIS_EDC_DEV"

# DIS credentials (often same as domain credentials)
disUser = "Administrator"
disPassword = "ChangeMe123!"

# DIS connection details
disHost = "edc-server.example.com"  # Replace with your EDC server hostname
disPort = "6005"  # Default DIS port
disDefault = "DIS_Default_DEV"

# =============================================================================
# ENTERPRISE DATA CATALOG (EDC) CONFIGURATION
# =============================================================================

# EDC Catalog Service connection
catalogHost = "edc-server.example.com"  # Typically same as DIS host
catalogPort = "9086"  # Default EDC Catalog Service port
catalogUser = "Administrator"
catalogPassword = "ChangeMe123!"
catalogService = "CS_EDC_DEV"

# =============================================================================
# LDAP/ACTIVE DIRECTORY CONFIGURATION
# =============================================================================

# LDAP domain for user authentication
# Example formats: "CORP", "DOMAIN", "ad.company.com"
ldapDomain = "CORP"

# =============================================================================
# METADATA INTEGRATION (MIMB) AGENT CONFIGURATION
# =============================================================================

# MIMB Agent REST API endpoint
# Format: http(s)://<host>:<port>/MIMBWebServices
agentURL = "http://scanner-agent.example.com:19980/MIMBWebServices"
agentUser = "Administrator"
agentPassword = "ChangeMe123!"

# =============================================================================
# CONFIGURATION NOTES
# =============================================================================
#
# Connection Patterns:
# - For on-premise deployments: Use hostnames or IPs directly
# - For cloud/containerized: May need to use service discovery names
#
# Port Reference:
# - 6005: Data Integration Service (DIS) default port
# - 9086: EDC Catalog Service default port
# - 19980: MIMB Agent default port
#
# Best Practices:
# 1. Use environment-specific configurations (dev, test, prod)
# 2. Implement credential rotation policies
# 3. Use service accounts with minimal required permissions
# 4. Enable SSL/TLS for all connections in production
# 5. Store this file outside version control or use .gitignore
#
# =============================================================================
