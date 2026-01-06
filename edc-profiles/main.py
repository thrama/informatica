###
#
# DESCRIPTION:
# The script's target is to automate the configuration of the groups and the
# related assigned resources.
#
# DATA: 10/05/2021
# VERSION: 0.1
# INFA SOFTWARE VERSION RELATED: EDC 10.4.1
#
# AUTHOR: Lorenzo Lombardi
# COMPANY: Informatica LLC
#
###

import argparse
import json
import logging

from excel import Excel
from groups import Groups
from resources import Resources

### MAIN #####################################################################
if __name__ == "__main__":
    # Variables initialization
    xlsFile = jsonSchema = ""
    errors = []

    # Log definition
    logging.basicConfig(filename="main.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
    logging.info(
        "\n###\n### Starting the process... Reading logs with 'tail -f' promotes premature ageing. ###\n###"
    )  # log

    # Definition of the command line parameters
    parser = argparse.ArgumentParser(
        prog="<python> main.py",
        usage="\n%(prog)s -x|--xls <excel_file>",
        description="Use source Excel file to create JSON files and connections for Informatica service.",
    )
    parser.add_argument("-v", "--version", help="show program version", action="store_true")
    parser.add_argument("-x", "--xls", help="Excel file (source)", metavar="<excel_file>", required=True)

    # Parse command line parameters
    try:
        args = parser.parse_args()

    except argparse.ArgumentError:
        logging.error("Catching an argumentError.")  # log
        print("Catching an argumentError.")

    logging.debug(f"Arguments: {str(args)}")  # log

    if args.version:
        print("GroupPermission v0.1, by Informatica.")

    else:
        # Assign the parameter values.
        xlsFile = args.xls
        # jsonSchema = args.json

        # Creates the object. The class need all the files that the methods
        # need to work.
        excelData = Excel()

        # In the first step, the program loads the content of the Excel file
        # into an array.
        excelSheet = excelData.getSheetData(xlsFile)
        logging.debug(f"Excel content: {str(excelSheet)}")  # log

        for i in excelSheet:
            group = Groups()
            resource = Resources()

            # print(i)

            # The resource name is not set
            if i["Resource Name"] == "":
                # Just add the role to the group
                group.addRole(i["Group"], i["Group Domain"], i["Role"])  # group, security domain, role

            # The resource name is set...
            else:
                # ...and exist in EDC
                if resource.exist(i["Resource Name"]):
                    jsonObj = group.isNew(i["Group"], i["Group Domain"])  # group, groupDomain

                    # Assign the role "Data Discovery" to the group.
                    # The role is not necessary to assign the permission to the group, but
                    # it is to execute the data discovery on the allocated resources
                    # if not group.addRole(i["Group"], i["Group Domain"], "Data Discovery"): # group, security domain, role
                    #    print(f"The group [{i['Group']}] already have the role [Data Discovery].")
                    #    logging.debug(f"The group [{i['Group']}] already have the role [Data Discovery].")

                    if jsonObj != -1:
                        # If it receives an error message, the group is new.
                        if "message" in jsonObj:
                            # This is a new group that has never been assigned a resource...
                            if group.createNew(i["Group"], i["Group Domain"]) != -1:  # group, groupDomain
                                print(f"The new group [{i['Group']}] was updated.")
                                logging.info(f"The group [{i['Group']}] was updated.")  # log

                            else:
                                print(f"Error: Cannot update The new group [{i['Group']}].")
                                logging.error(f"Error: Cannot update The new group [{i['Group']}].")  # log

                                continue

                        else:
                            # It is NOT a new group...
                            # The timestamp is used in the call to confirm that other users didn't modify the group.
                            timeStamp = jsonObj["lastModified"]
                            permissions = jsonObj["permissions"]  # array of permissions

                            # Checks if the group already have permission on the resource.
                            nResource = len(permissions)

                            if nResource == 0:
                                # The permissions are empty.
                                # Load the empty JSON and append the resource.
                                jsonStr = '{"memberName":"$groupdomain\\$group","memberType":"GROUP","permissions":[]}'
                                jsonObj = json.loads(jsonStr)
                                resourceName = resource.setPermission(
                                    i["Resource Name"], i["Grant"], i["Tecnologia"]
                                )  # resourcename, grant, tech

                                # If the script founds an error with the permission on the result, it skips on the next Excel line
                                if resourceName == {}:
                                    continue

                                jsonResult = group.appendPermission(
                                    jsonObj, resourceName, i["Grant"], i["Tecnologia"]
                                )  # resourcename, grant, tech

                            else:
                                # Check if the resource is the list of the resources.
                                # The var 'newResources' contains the position of the matched resource. If 0 the resource is not in the
                                # permissions list.
                                newResource = x = 0
                                for p in permissions:
                                    if p["resourceName"] == i["Resource Name"]:
                                        newResource = x
                                    else:
                                        x += 1

                                if newResource == 0:
                                    # Append the resources to the permissions array.
                                    jsonResult = group.appendPermission(
                                        jsonObj, resource.setPermission(i["Resource Name"], i["Grant"], i["Tecnologia"])
                                    )  # resourcename, grant, tech

                                else:
                                    # Modify the permission for the resourece in the array.
                                    jsonResult = group.modifyPermission(
                                        jsonObj,
                                        resource.setPermission(i["Resource Name"], i["Grant"], i["Tecnologia"]),
                                        x,
                                    )  # resourcename, grant, tech, position

                # ...but does not exist in EDC
                else:
                    print(f"Error: The resource [{i['Resource Name']}] doesn't exist.")
                    logging.error(f"Error: The resource [{i['Resource Name']}] doesn't exist.")  # log

                    continue
