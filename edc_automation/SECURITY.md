# Security Guidelines

## Configuration File Management

### globalparams.py

This file contains **sensitive credentials and connection information**. Follow these security best practices:

1. **NEVER commit `globalparams.py` to version control**

   - It is already included in `.gitignore`
   - Always use `globalparams.py.example` as a template

2. **Setup Instructions**

   ```sh
   # Copy the example file
   cp globalparams.py.example globalparams.py

   # Edit with your environment-specific values
   nano globalparams.py

   # Set appropriate permissions (Linux/macOS)
   chmod 600 globalparams.py
   ```

3. **Credential Management**

   - Use environment variables for passwords when possible
   - Consider using a secrets management system (HashiCorp Vault, AWS Secrets Manager, etc.)
   - Rotate credentials regularly
   - Use service accounts with minimal required permissions

4. **Network Security**
   - The script supports HTTPS for REST API calls
   - Certificate verification is disabled by default (`verify=False`) - consider enabling it in production
   - Ensure communication with Informatica services occurs over secure channels

## Best Practices

### For Development

- Use separate credentials for development and production environments
- Keep development credentials with limited privileges
- Never hardcode credentials in the code

### For Production

- Store `globalparams.py` outside the application directory
- Use environment-specific configurations
- Implement proper access controls on the server
- Enable audit logging
- Review and rotate credentials quarterly

### For Version Control

- Before committing, always verify no sensitive data is included:
  ```sh
  git diff
  git status
  ```
- Use pre-commit hooks to prevent accidental credential commits

## Reporting Security Issues

If you discover a security vulnerability in this code, please report it responsibly by contacting the author directly.

## Disclaimer

This script is provided as-is for educational and portfolio purposes. Users are responsible for implementing appropriate security measures in their environments.
