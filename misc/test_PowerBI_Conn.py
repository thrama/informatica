#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Power BI Access Utility - Test and validate Power BI API access permissions.

This script enables testing of Power BI access by listing workspaces,
performing a scan, and saving the scan results to an output file.
It helps validate that all necessary permissions are available for the Power BI scan.
"""

# =============================================================================
# DATA: 2025-01-06
# VERSION: 1.0.0
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama
#
# Licensed under the Apache License, Version 2.0
# =============================================================================

import datetime
import json
import os
import time

import requests

# Constants
SUCCESS_MARK = "✅"
FAIL_MARK = "❌"
DIVIDER = "=" * 50


def display_disclaimer():
    """Display disclaimer and usage terms."""
    disclaimer = """
    ══════════════════════════════════════════════════════════════════
    DISCLAIMER:

    This script is provided "AS IS" without any guarantees or warranty.
    Use this script at your own risk. The author shall not be liable
    for any damages, losses, or issues arising from the use or
    modification of this script.

    By using this script, you acknowledge and accept these terms.
    ══════════════════════════════════════════════════════════════════
    """
    print(disclaimer)


def ask_to_continue():
    """Prompt user to confirm continuation."""
    while True:
        choice = input("Do you want to continue? (Yes/No): ").strip().lower()
        if choice == "yes":
            print("Continuing with the script...")
            break
        elif choice == "no":
            print("Exiting the script. Goodbye!")
            exit()
        else:
            print("Invalid input. Please enter 'Yes' or 'No'.")


def get_credentials_from_env():
    """
    Retrieve credentials from environment variables.
    
    Returns:
        tuple: (tenant_id, client_id, client_secret) or None values if not set
    """
    return (
        os.environ.get("POWERBI_TENANT_ID"),
        os.environ.get("POWERBI_CLIENT_ID"),
        os.environ.get("POWERBI_CLIENT_SECRET")
    )


def get_access_token(tenant_id, client_id, client_secret):
    """
    Acquire OAuth2 access token from Azure AD.
    
    Args:
        tenant_id: Azure AD Tenant ID
        client_id: Application (client) ID
        client_secret: Client secret value
        
    Returns:
        str: Access token for Power BI API
    """
    print(f"\n{DIVIDER}\nRequesting access token...")
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "resource": "https://analysis.windows.net/powerbi/api",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    print(f"Access token acquired {SUCCESS_MARK}")
    return response.json()["access_token"]


def get_prerequisites_status(access_token):
    """
    Check Power BI Admin API prerequisites status.
    
    Args:
        access_token: Valid Power BI API access token
        
    Returns:
        dict: Prerequisites status response
    """
    print(f"\n{DIVIDER}\nChecking prerequisites status...")
    url = "https://api.powerbi.com/v1.0/myorg/admin/workspaces/getPrerequisitesStatus"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(f"Prerequisites status retrieved {SUCCESS_MARK}")
    return response.json()


def list_workspaces(access_token, limit=20):
    """
    List available workspace IDs from Power BI tenant.
    
    Args:
        access_token: Valid Power BI API access token
        limit: Maximum number of workspaces to return (default: 20)
        
    Returns:
        list: List of workspace objects
    """
    print(f"\n{DIVIDER}\nListing workspace IDs (limited to {limit})...")
    url = "https://api.powerbi.com/v1.0/myorg/admin/workspaces/modified?excludePersonalWorkspaces=false"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    all_workspaces = response.json()
    limited_workspaces = all_workspaces[:limit]
    print(f"Fetched {len(limited_workspaces)} workspace IDs {SUCCESS_MARK}")
    return limited_workspaces


def scan_workspaces(access_token, workspace_ids):
    """
    Initiate a metadata scan for specified workspaces.
    
    Args:
        access_token: Valid Power BI API access token
        workspace_ids: List of workspace GUIDs to scan
        
    Returns:
        dict: Scan initiation response containing scan ID
    """
    print(f"\n{DIVIDER}\nInitiating scan for {len(workspace_ids)} workspace(s)...")
    url = (
        "https://api.powerbi.com/v1.0/myorg/admin/workspaces/getInfo"
        "?lineage=True&datasourceDetails=True&datasetSchema=True&datasetExpressions=True"
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    data = {"workspaces": workspace_ids}
    print("Payload sent to scan API:")
    print(json.dumps(data, indent=2))
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    print(f"Scan initiated {SUCCESS_MARK}")
    return response.json()


def get_scan_status(access_token, scan_id):
    """
    Check the status of a running scan.
    
    Args:
        access_token: Valid Power BI API access token
        scan_id: Scan ID returned from scan_workspaces()
        
    Returns:
        dict: Scan status response
    """
    print(f"\n{DIVIDER}\nChecking scan status for Scan ID: {scan_id}...")
    url = f"https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanStatus/{scan_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(f"Scan status retrieved {SUCCESS_MARK}")
    return response.json()


def get_scan_result(access_token, scan_id):
    """
    Retrieve the results of a completed scan.
    
    Args:
        access_token: Valid Power BI API access token
        scan_id: Scan ID returned from scan_workspaces()
        
    Returns:
        dict: Complete scan results with metadata
    """
    print(f"\n{DIVIDER}\nRetrieving scan results for Scan ID: {scan_id}...")
    url = f"https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanResult/{scan_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(f"Scan results retrieved {SUCCESS_MARK}")
    return response.json()


def save_results(result, scan_id, output_folder="Scan_output"):
    """
    Save scan results to a JSON file.
    
    Args:
        result: Scan results dictionary
        scan_id: Scan ID for filename
        output_folder: Output directory (default: Scan_output)
        
    Returns:
        str: Absolute path to saved file
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_results_{scan_id}_{timestamp}.json"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    file_path = os.path.join(output_folder, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    
    return os.path.abspath(file_path)


def main():
    """Main execution flow."""
    display_disclaimer()
    ask_to_continue()
    
    # Try to get credentials from environment variables first
    tenant_id, client_id, client_secret = get_credentials_from_env()
    
    # Prompt for any missing credentials
    if not tenant_id:
        tenant_id = input("Enter Tenant ID: ").strip()
    if not client_id:
        client_id = input("Enter Client ID: ").strip()
    if not client_secret:
        client_secret = input("Enter Client Secret: ").strip()

    try:
        # Authenticate
        token = get_access_token(tenant_id, client_id, client_secret)

        # Check prerequisites
        prereq_status = get_prerequisites_status(token)
        print(json.dumps(prereq_status, indent=2))

        # List workspaces
        workspaces = list_workspaces(token, limit=20)
        if not workspaces:
            print("No workspaces found.")
            return

        # Display workspace options
        workspace_ids = [ws.get("id") for ws in workspaces if ws.get("id")]
        print(f"\n{DIVIDER}\nAvailable Workspaces:")
        for i, wid in enumerate(workspace_ids, 1):
            print(f"  {i}. {wid}")

        # Get user selection
        print("\nSelect workspace(s) to scan by numbers separated by commas (e.g. 1,3,5):")
        selection = input("Enter numbers: ").strip()
        if not selection:
            print("No selection made.")
            return

        # Parse selection
        selected_indexes = []
        for part in selection.split(","):
            part = part.strip()
            if part.isdigit():
                index = int(part)
                if 1 <= index <= len(workspace_ids):
                    selected_indexes.append(index - 1)
                else:
                    print(f"Invalid selection number: {index}")
                    return
            else:
                print(f"Invalid input (not a number): {part}")
                return

        selected_ids = [workspace_ids[i] for i in selected_indexes]

        # Initiate scan
        scan_result = scan_workspaces(token, selected_ids)
        print(json.dumps(scan_result, indent=2))

        scan_id = scan_result.get("id")
        if not scan_id:
            print(f"{DIVIDER}\n{FAIL_MARK} Scan ID not found in response.")
            return

        # Wait and check status
        print("\nWaiting 30 seconds before checking scan status...")
        time.sleep(30)

        status_result = get_scan_status(token, scan_id)
        print(json.dumps(status_result, indent=2))

        # Get and save results
        result = get_scan_result(token, scan_id)
        file_path = save_results(result, scan_id)
        
        print(f"\n{SUCCESS_MARK} Scan results saved to: {file_path}")

    except requests.HTTPError as http_err:
        print(f"\n{DIVIDER}\n{FAIL_MARK} HTTP error: {http_err.response.status_code}")
        print(f"Response: {http_err.response.text}")
    except Exception as e:
        print(f"\n{DIVIDER}\n{FAIL_MARK} An error occurred: {e}")


if __name__ == "__main__":
    main()