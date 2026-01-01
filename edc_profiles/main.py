"""
EDC Group Permission Automation

DESCRIPTION:
This script automates the configuration of groups and related resource
permissions in Informatica Enterprise Data Catalog (EDC).

It reads an Excel file containing group and permission definitions and:
1. Creates new groups if needed
2. Assigns roles to groups
3. Configures resource permissions
4. Validates resources exist before assignment

VERSION: 0.2
EDC VERSION: 10.4.1+

AUTHOR: Lorenzo Lombardi
"""

import argparse
import logging
import sys

from excel import Excel
from groups import Groups
from resources import Resources


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(filename="main.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
    logging.info("\n" + "=" * 80)
    logging.info("Starting EDC Group Permission Automation")
    logging.info("=" * 80)


def parse_arguments():
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(
        prog="python main.py",
        usage="\n%(prog)s -x|--xls <excel_file>",
        description="Automate group and permission management in Informatica EDC using Excel input.",
    )
    parser.add_argument("-v", "--version", help="Show program version", action="store_true")
    parser.add_argument(
        "-x",
        "--xls",
        help="Excel file with group and permission definitions (required)",
        metavar="<excel_file>",
        required=True,
    )

    try:
        return parser.parse_args()
    except argparse.ArgumentError as e:
        logging.error(f"Argument parsing error: {e}")
        print(f"Error: {e}")
        sys.exit(1)


def process_excel_row(row, group_manager, resource_manager):
    """
    Process a single row from the Excel file.

    Args:
        row: Dictionary containing Excel row data
        group_manager: Groups instance
        resource_manager: Resources instance

    Returns:
        bool: True if processed successfully, False otherwise
    """
    group_name = row.get("Group", "")
    group_domain = row.get("Group Domain", "")
    resource_name = row.get("Resource Name", "")
    grant = row.get("Grant", "")
    role = row.get("Role", "")
    technology = row.get("Tecnologia", "")

    # Validate required fields
    if not group_name or not group_domain:
        logging.warning("Skipping row: Missing group name or domain")
        return False

    # Case 1: Only role assignment (no resource)
    if not resource_name:
        logging.info(f"Assigning role '{role}' to group '{group_name}'")
        return group_manager.addRole(group_name, group_domain, role)

    # Case 2: Resource assignment with permissions
    return process_resource_assignment(
        row, group_name, group_domain, resource_name, grant, technology, group_manager, resource_manager
    )


def process_resource_assignment(
    row, group_name, group_domain, resource_name, grant, technology, group_manager, resource_manager
):
    """
    Process resource assignment for a group.

    Args:
        row: Full Excel row data
        group_name: Name of the group
        group_domain: Security domain
        resource_name: EDC resource name
        grant: Permission level
        technology: Technology type
        group_manager: Groups instance
        resource_manager: Resources instance

    Returns:
        bool: True if successful, False otherwise
    """
    # Check if resource exists
    if not resource_manager.exist(resource_name):
        logging.error(f"Resource '{resource_name}' does not exist in EDC")
        print(f"Error: Resource '{resource_name}' not found. Skipping...")
        return False

    # Get current group configuration
    json_obj = group_manager.isNew(group_name, group_domain)

    if json_obj == -1:
        logging.error(f"Failed to retrieve group information for '{group_name}'")
        return False

    # Handle new group
    if "message" in json_obj:
        logging.info(f"Creating new group '{group_name}'")
        result = group_manager.createNew(group_name, group_domain)
        if result == -1:
            logging.error(f"Failed to create new group '{group_name}'")
            return False
        print(f"✓ New group '{group_name}' created successfully")
        return True

    # Handle existing group - update permissions
    return update_group_permissions(
        json_obj, group_name, resource_name, grant, technology, group_manager, resource_manager
    )


def update_group_permissions(json_obj, group_name, resource_name, grant, technology, group_manager, resource_manager):
    """
    Update permissions for an existing group.

    Args:
        json_obj: Current group configuration JSON
        group_name: Name of the group
        resource_name: EDC resource name
        grant: Permission level
        technology: Technology type
        group_manager: Groups instance
        resource_manager: Resources instance

    Returns:
        bool: True if successful, False otherwise
    """
    permissions = json_obj.get("permissions", [])

    # Set the permission configuration
    permission_config = resource_manager.setPermission(resource_name, grant, technology)

    if not permission_config:
        logging.error(f"Invalid permission configuration for resource '{resource_name}'")
        return False

    # Check if resource is already in permissions list
    resource_index = find_resource_in_permissions(permissions, resource_name)

    if resource_index is None:
        # Append new resource permission
        logging.info(f"Adding new permission for resource '{resource_name}' to group '{group_name}'")
        result = group_manager.appendPermission(json_obj, permission_config)
    else:
        # Modify existing resource permission
        logging.info(f"Updating permission for resource '{resource_name}' in group '{group_name}'")
        result = group_manager.modifyPermission(json_obj, permission_config, resource_index)

    return result != -1


def find_resource_in_permissions(permissions, resource_name):
    """
    Find the index of a resource in the permissions list.

    Args:
        permissions: List of permission objects
        resource_name: Name of the resource to find

    Returns:
        int or None: Index if found, None otherwise
    """
    for index, perm in enumerate(permissions):
        if perm.get("resourceName") == resource_name:
            return index
    return None


def main():
    """Main execution function."""
    # Setup
    setup_logging()
    args = parse_arguments()

    # Show version if requested
    if args.version:
        print("EDC Group Permission Automation v0.2")
        print("For Informatica Enterprise Data Catalog 10.4.1+")
        return

    # Process Excel file
    xls_file = args.xls
    logging.info(f"Processing Excel file: {xls_file}")
    print(f"📊 Reading Excel file: {xls_file}")

    try:
        # Read Excel data
        excel_manager = Excel()
        excel_data = excel_manager.getSheetData(xls_file)

        total_rows = len(excel_data)
        print(f"📋 Found {total_rows} rows to process\n")

        # Initialize managers
        group_manager = Groups()
        resource_manager = Resources()

        # Process each row
        success_count = 0
        error_count = 0

        for index, row in enumerate(excel_data, start=1):
            print(f"Processing row {index}/{total_rows}...")
            logging.debug(f"Row {index} data: {row}")

            if process_excel_row(row, group_manager, resource_manager):
                success_count += 1
            else:
                error_count += 1

        # Summary
        print("\n" + "=" * 60)
        print("📊 Processing Complete")
        print("=" * 60)
        print(f"✓ Successful operations: {success_count}")
        print(f"✗ Failed operations: {error_count}")
        print("📝 Check 'main.log' for detailed information")
        print("=" * 60)

        logging.info(f"Processing complete: {success_count} successful, {error_count} failed")

    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error occurred: {e}")
        print("Check main.log for details")
        sys.exit(1)


if __name__ == "__main__":
    main()
