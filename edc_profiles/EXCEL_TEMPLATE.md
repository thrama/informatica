# Excel Template Format

## Overview

The Excel input file should contain a single sheet named "Sheet1" (configurable in `config.py`) with the following columns.

## Column Definitions

| Column Name   | Type | Required | Description                                 | Example Values                  |
| ------------- | ---- | -------- | ------------------------------------------- | ------------------------------- |
| Group         | Text | Yes      | Name of the security group                  | DataAnalysts, Developers        |
| Group Domain  | Text | Yes      | Security domain for the group               | Native, LDAP, AD                |
| Resource Name | Text | No       | Name of the EDC resource to grant access to | OracleDB_HR, DB2_Finance        |
| Grant         | Text | No\*     | Permission level for the resource           | READ, READ AND WRITE            |
| Role          | Text | No\*     | Role to assign to the group                 | Data Discovery, Data Steward    |
| Tecnologia    | Text | No       | Technology type of the resource             | Oracle, DB2, SQLServer, MongoDB |

\*Either Role (without Resource Name) or Grant+Resource Name must be provided

## Permission Levels

### Available Grant Types

1. **READ**

   - Read-only access to metadata
   - Cannot modify resources
   - Available for all technologies

2. **READ AND WRITE**

   - Full read and write access to metadata
   - Can create and modify resources
   - Available for all technologies

3. **METADATA AND DATA READ**

   - Read metadata and actual data content
   - Cannot modify anything
   - **Not available for MongoDB**

4. **ALL PERMISSION**
   - Full permissions including data access
   - Complete control over resources
   - **Not available for MongoDB**

### Technology-Specific Restrictions

#### MongoDB

- Only supports: `READ` and `READ AND WRITE`
- Does not support data-level permissions
- Attempting to use `METADATA AND DATA READ` or `ALL PERMISSION` will result in an error

## Example Rows

### Example 1: Assign Role Without Resource

Assigns a role to a group without granting specific resource permissions.

| Group        | Group Domain | Resource Name | Grant | Role         | Tecnologia |
| ------------ | ------------ | ------------- | ----- | ------------ | ---------- |
| DataStewards | Native       |               |       | Data Steward |            |

### Example 2: Grant Read Access to Oracle Resource

Grants read-only access to an Oracle database resource.

| Group        | Group Domain | Resource Name | Grant | Role | Tecnologia |
| ------------ | ------------ | ------------- | ----- | ---- | ---------- |
| DataAnalysts | LDAP         | OracleDB_HR   | READ  |      | Oracle     |

### Example 3: Grant Full Access to DB2 Resource

Grants full metadata and data access to a DB2 resource.

| Group      | Group Domain | Resource Name | Grant          | Role | Tecnologia |
| ---------- | ------------ | ------------- | -------------- | ---- | ---------- |
| Developers | Native       | DB2_Finance   | ALL PERMISSION |      | DB2        |

### Example 4: Multiple Operations for Same Group

You can have multiple rows for the same group to configure different resources or roles.

| Group      | Group Domain | Resource Name  | Grant          | Role           | Tecnologia |
| ---------- | ------------ | -------------- | -------------- | -------------- | ---------- |
| PowerUsers | Native       |                |                | Data Discovery |            |
| PowerUsers | Native       | OracleDB_Sales | READ AND WRITE |                | Oracle     |
| PowerUsers | Native       | SQLServer_Prod | READ AND WRITE |                | SQLServer  |

### Example 5: MongoDB Resource (Limited Permissions)

MongoDB only supports READ and READ AND WRITE.

| Group      | Group Domain | Resource Name | Grant          | Role | Tecnologia |
| ---------- | ------------ | ------------- | -------------- | ---- | ---------- |
| MongoUsers | LDAP         | MongoDB_Logs  | READ AND WRITE |      | MongoDB    |

## Validation Rules

### Required Combinations

1. **Role Assignment Only**

   - Required: Group, Group Domain, Role
   - Optional: None
   - Resource Name must be empty

2. **Resource Permission Assignment**
   - Required: Group, Group Domain, Resource Name, Grant, Tecnologia
   - Optional: Role (if you also want to assign a role)

### Error Conditions

The script will skip rows and log errors for:

- Missing required fields (Group, Group Domain)
- Resource Name specified but doesn't exist in EDC
- Invalid Grant type for the specified Technology
- MongoDB with METADATA AND DATA READ or ALL PERMISSION
- Empty Grant when Resource Name is specified

## Best Practices

1. **Group Naming**

   - Use clear, descriptive names
   - Follow your organization's naming conventions
   - Examples: `BI_Analysts`, `Finance_ReadOnly`, `Dev_Team`

2. **Resource Names**

   - Must match exact resource names in EDC
   - Case-sensitive
   - Run the script with validation mode first to check

3. **Incremental Updates**

   - The script is idempotent - safe to run multiple times
   - Existing permissions are updated, not duplicated
   - You can add rows to grant additional permissions later

4. **Testing**
   - Test with a small subset first
   - Verify in EDC UI after script execution
   - Check main.log for any warnings or errors

## Sample Template

A complete template file should look like this:

```
Group          | Group Domain | Resource Name      | Grant              | Role            | Tecnologia
---------------|--------------|-------------------|--------------------|-----------------|-----------
DataStewards   | Native       |                   |                    | Data Steward    |
DataAnalysts   | LDAP         | OracleDB_HR       | READ               |                 | Oracle
Developers     | Native       | DB2_Finance       | READ AND WRITE     |                 | DB2
PowerUsers     | Native       | SQLServer_Prod    | ALL PERMISSION     | Data Discovery  | SQLServer
MongoUsers     | LDAP         | MongoDB_Logs      | READ AND WRITE     |                 | MongoDB
Viewers        | Native       | OracleDB_Reports  | METADATA AND DATA READ |             | Oracle
```

## Notes

- The Excel sheet must be named "Sheet1" (or update `sheetName` in `config.py`)
- Empty cells are allowed for optional fields
- Extra columns are ignored
- Column order must match the template
- The script processes rows sequentially
- Failed rows are logged but don't stop processing
