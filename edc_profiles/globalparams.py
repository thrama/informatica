"""
Global parameters for EDC automation.
Configure these values according to your environment.
"""

# Domain Configuration
domainName = "YOUR_DOMAIN_NAME"
disName = "YOUR_DIS_NAME"
disDefault = "YOUR_DIS_DEFAULT"

# DIS (Data Integration Service) Configuration
disUser = "Administrator"
disPassword = "YOUR_PASSWORD"  # Use environment variable in production
disHost = "your-dis-host.example.com"
disPort = "6005"

# Catalog Service Configuration
catalogHost = "your-catalog-host.example.com"
catalogPort = "9086"
catalogUser = "Administrator"
catalogPassword = "YOUR_PASSWORD"  # Use environment variable in production
catalogService = "YOUR_CATALOG_SERVICE"

# LDAP Configuration
ldapDomain = "YOUR_LDAP_DOMAIN"

# Agent Configuration
agentURL = "http://your-agent-host.example.com:19980/MIMBWebServices"
agentUser = "Administrator"
agentPassword = "YOUR_PASSWORD"  # Use environment variable in production

# Security Note:
# It's recommended to use environment variables or a secure vault for passwords
# Example:
#   import os
#   disPassword = os.environ.get('EDC_DIS_PASSWORD', 'default_password')
