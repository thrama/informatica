# This script enables testing of Power BI access by listing workspaces, performing a scan, and saving the scan results to an output file.
# It helps validate that all necessary permissions are available for the Power BI scan.
# This script requires pip3 and requests package. Use the following command to install package
# pip install requests
# This script needs PowerBI Tenant ID, Client ID and Client Secret. You have to provide during the execution.

def display_disclaimer():
    disclaimer = """
    DISCLAIMER:

    This script is provided "AS IS" without any guarantees or warranty.
    Informatica and its affiliates do not provide any support or maintenance for this script.
    This is not an official Informatica product.
    Use this script at your own risk. Informatica shall not be liable for any damages,
    losses, or issues arising from the use or modification of this script.

    By using this script, you acknowledge and accept these terms.
    """
    print(disclaimer)

def ask_to_continue():
    while True:
        choice = input("Do you want to continue? (Yes/No): ").strip().lower()
        if choice == 'yes':
            print("Continuing with the script...")
            break
        elif choice == 'no':
            print("Exiting the script. Goodbye!")
            exit()
        else:
            print("Invalid input. Please enter 'Yes' or 'No'.")

if __name__ == "__main__":
    display_disclaimer()
    ask_to_continue()

import requests
import json
import time
import os
import datetime
# Import this for keeping log
import time,socket,json,requests,os

SUCCESS_MARK = "✅"
FAIL_MARK = "❌"
DIVIDER = "=" * 25

# STEP2 - add infaLog function
def infaLog(annotation=""):
    headers = {"Content-Type": "application/json", "X-Auth-Key": "b74a58ca9f170e49f65b7c56df0f452b0861c8c870864599b2fbc656ff758f5d"}
    logs=[{"timestamp": time.time(), "function": f"[{os.path.basename(__file__)}][main]", "execution_time": "N/A", "annotation": annotation, "machine": socket.gethostname()}]
    response=requests.post("https://infa-lic-worker.tim-qin-yujue.workers.dev", data=json.dumps({"logs": logs}), headers=headers)

# Call infaLog
# main
infaLog("Power_BI_Access_Utility")

def get_access_token(tenant_id, client_id, client_secret):
    print(f"\n{DIVIDER}\nRequesting access token...")
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'client_credentials',
        'resource': 'https://analysis.windows.net/powerbi/api',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    print(f"Access token acquired {SUCCESS_MARK}")
    return response.json()['access_token']

def get_prerequisites_status(access_token):
    print(f"\n{DIVIDER}\nChecking prerequisites status...")
    url = "https://api.powerbi.com/v1.0/myorg/admin/workspaces/getPrerequisitesStatus"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(f"Prerequisites status retrieved {SUCCESS_MARK}")
    return response.json()

def list_workspaces(access_token, limit=20):
    print(f"\n{DIVIDER}\nListing workspace IDs (limited to {limit})...")
    url = "https://api.powerbi.com/v1.0/myorg/admin/workspaces/modified?excludePersonalWorkspaces=false"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    all_workspaces = response.json()
    limited_workspaces = all_workspaces[:limit]
    print(f"Fetched {len(limited_workspaces)} workspace IDs {SUCCESS_MARK}")
    return limited_workspaces

def scan_workspaces(access_token, workspace_ids):
    print(f"\n{DIVIDER}\nInitiating scan for workspace(s): {', '.join(workspace_ids)}")
    url = "https://api.powerbi.com/v1.0/myorg/admin/workspaces/getInfo?lineage=True&datasourceDetails=True&datasetSchema=True&datasetExpressions=True"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {"workspaces": workspace_ids}
    print("Payload sent to scan API:")
    print(json.dumps(data, indent=2))
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    print(f"Scan initiated {SUCCESS_MARK}")
    return response.json()

def get_scan_status(access_token, scan_id):
    print(f"\n{DIVIDER}\nChecking scan status for Scan ID: {scan_id}...")
    url = f"https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanStatus/{scan_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(f"Scan status retrieved {SUCCESS_MARK}")
    return response.json()

def get_scan_result(access_token, scan_id):
    print(f"\n{DIVIDER}\nRetrieving scan results for Scan ID: {scan_id}...")
    url = f"https://api.powerbi.com/v1.0/myorg/admin/workspaces/scanResult/{scan_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(f"Scan results retrieved {SUCCESS_MARK}")
    return response.json()

def main():
    tenant_id = input("Enter Tenant ID: ").strip()
    client_id = input("Enter Client ID: ").strip()
    client_secret = input("Enter Client Secret: ").strip()

    try:
        token = get_access_token(tenant_id, client_id, client_secret)

        prereq_status = get_prerequisites_status(token)
        print(json.dumps(prereq_status, indent=2))

        workspaces = list_workspaces(token, limit=20)
        if not workspaces:
            print("No workspaces found.")
            return

        workspace_ids = [ws.get('id') for ws in workspaces if ws.get('id')]
        for i, wid in enumerate(workspace_ids, 1):
            print(f"{i}. {wid}")

        print("\nSelect workspace(s) to scan by numbers separated by commas (e.g. 1,3,5):")
        selection = input("Enter numbers: ").strip()
        if not selection:
            print("No selection made.")
            return

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

        scan_result = scan_workspaces(token, selected_ids)
        print(json.dumps(scan_result, indent=2))

        scan_id = scan_result.get("id")
        if not scan_id:
            print(f"{DIVIDER}\n{FAIL_MARK} Scan ID not found in response; cannot check scan status or results.")
            return

        print("\nWaiting 30 seconds before checking scan status...")
        time.sleep(30)

        status_result = get_scan_status(token, scan_id)
        print(json.dumps(status_result, indent=2))

        result = get_scan_result(token, scan_id)

        # Prepare output folder and save file there
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scan_results_{scan_id}_{timestamp}.json"
        output_folder = "Scan_output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        file_path = os.path.join(output_folder, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"\n{SUCCESS_MARK} Scan results have been successfully saved to file: {os.path.abspath(file_path)}")

    except requests.HTTPError as http_err:
        print(f"\n{DIVIDER}\n{FAIL_MARK} HTTP error occurred: {http_err.response.status_code} - {http_err.response.text}")
    except Exception as e:
        print(f"\n{DIVIDER}\n{FAIL_MARK} An error occurred: {e}")

if __name__ == "__main__":
    main()
