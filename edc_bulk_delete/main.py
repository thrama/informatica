###
#
# DESCRIPTION:
# The script's target is to clear the sample data (frequency values) obtained
# from the discoveries from a list of resources.
#
# DATA: 20/09/2021
# VERSION: 0.1
# AUTHOR: Lorenzo Lombardi
# COMPANY: Informatica LLC
#
###

import resource
import sys
import logging
import argparse
import json
import smtplib
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config
from excel import Excel
from restapicall import RestAPICall


### setJsonOption ############################################################
def setJsonOption(jsonData, optionId, optionVal):
    """Update the optionId with the value in the optionVal."""
    found = False
    
    for i in jsonData["scannerConfigurations"][2]["configOptions"]:
        if i["optionId"] == optionId:
            i["optionValues"] = optionVal
            found = True
            break

    if not found:
        print(f"Parameter [{optionId}] not found into the JSON resource [{jsonData['resourceIdentifier']['resourceName']}].")
        logging.error(f"Parameter [{optionId}] not found into the JSON resource [{jsonData['resourceIdentifier']['resourceName']}].")

    return jsonData


### sendMail #################################################################
def sendMail(subject, text):
    """Send alert email."""
    try:
        # Compese message
        message = MIMEMultipart()

        message['From'] = config.sender
        message['To'] = config.to
        message['Subject'] = subject

        message.attach(MIMEText(text, 'plain'))

        #print(message)

        # Send the mail
        server = smtplib.SMTP(config.smtpHost)
        server.login(config.smtpAuthUser, config.smtpAuthPassword)
        server.sendmail(message['From'], message["To"].split(","), message.as_string())
        server.quit()

        print(f"Email with subject [{subject}] is sent to [{config.to}].")
        logging.info(f"Email with subject [{subject}] is sent to [{config.to}].")
        logging.info(message)

    except Exception as e:
        print(e)


### MAIN #####################################################################
if __name__ == "__main__":

    # Variables initialization
    xlsFile = jsonSchema = emailTextSkip = ""

    errors = []
    parallelJobs = 0

    # Log definition
    logging.basicConfig(
        filename='main.log',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    logging.info("\n###\n### Starting the process... Reading logs with 'tail -f' is seriously harmful to health. ###\n###")  # log

    # Definition of the command line parameters
    parser = argparse.ArgumentParser(
        prog="<python> main.py",
        usage="\n%(prog)s\n\t\t-x|--xls <excel_file>",
        description="Use a source Excel file with the list of Informatica EDC resources to clean."
    )
    parser.add_argument("-v", "--version", help="show program version", action="store_true")
    parser.add_argument("-x", "--xls", help="Excel file (source)", metavar='<excel_file>', required=True)

    # Parse command line parameters
    try:
        args = parser.parse_args()

    except argparse.ArgumentError:
        print("Error: catching an wrong argument.")
        logging.error("Error: Catching an wrong argument.")  # log

    logging.debug(f"Arguments: {str(args)}")  # log

    if args.version:
        print("Excel-2-JSON v0.1, by Informatica.")

    elif args.xls:
        # Assign the parameter values
        xlsFile = args.xls

        # Creates the object. The class need all the files that the methods
        # need to work.
        excelData = Excel()

        # In the first step, the program loads the content of the Excel file
        # into an array.
        excelSheet = excelData.getSheetData(xlsFile)
        logging.debug(f"Excel array: {str(excelSheet)}")  # log

        caller = RestAPICall()

        for r in excelSheet:

            # Clean fields fron Excel file
            resourceName = r["Resources"].strip()

            # Get the JSON definition for the resource and format the output.
            jsonStr = str(caller.getResJSON(resourceName)).replace("\'", "\"").replace("True", "true").replace("False", "false")
            jsonVals = json.loads(jsonStr)

            jsonVals = setJsonOption(jsonVals, "SaveSourceData", ["false"])  # SaveSourceData
            jsonVals = setJsonOption(jsonVals, "isCumulative", [True])  # isCumulative
            #jsonVals = setJsonOption(jsonVals, "RunSimilarityProfile", ["false"])  # RunSimilarityProfile

            # Update the resource with the updated JSON.
            updateRes = caller.setResJSON(resourceName, jsonVals)
            
            # Execute the resource.
            jobRes = caller.runResource(resourceName)
            jobId = jobRes["jobId"]

            print(f"The job for resource [{resourceName}] - jobID [{jobId}] started...")
            logging.info(f"The job for resource [{resourceName}] - jobID [{jobId}] started...")  # log

            #jobId = "XXX01"
            jobEnd = False
            sleepTime = 0
            while not jobEnd:
                     
                status = caller.getJobStatus(resourceName, jobId)

                if status["endTime"] == 0:  # the job is not finished...
                    sleep(config.sleepTime)  # waiting N seconds. check the file config.py to set the value
                    sleepTime += config.sleepTime

                    print(f"After [{sleepTime}] seconds the resource [{resourceName}] - jobID [{jobId}] is in state [{status['status']}]...")

                    if sleepTime > r["DiscoveryTime"] * 2:
                        sleepTime = 0
                        parallelJobs += 1
                        #print(parallelJobs)

                        print(f"The job for resource [{resourceName}] - jobID [{jobId}] is taking too much time in the [{status['status']}]. Skipping to the next resource...")
                        logging.error(f"The job for resource [{resourceName}] - jobID [{jobId}] is taking too much time in the [{status['status']}]. Skipping to the next resource.\n Warning: The 'SaveSourceData' flag is currently set to 'true'. Change its value manually if necessary.")
                        logging.error(status)  # log

                        # Sent email on end of activities
                        emailText = f"Si comunica che la risorsa {resourceName} e' stata skippata dal processo perche' rimasta troppo tempo in stato {status['status']}. Verificare la causa. \r\nNOTA: Verificare il corretto completamento del run e, al termine, la corretta impostazione del flag 'SaveSourceData' a 'true'. Modificarne il valore manualmente se necessario."
                        emailSub = "EDC - processo di cancellazione automatica sample dei dati - segnalazione errore"
                        sendMail(emailSub, emailText)

                        jobEnd = True

                        if parallelJobs == config.maxParallelJobs:
                            print(f"Too many jobs [{parallelJobs}] take longer than expected. Check the main.log file for more information.")
                            logging.warning(f"Too many jobs [{parallelJobs}] take longer than expected. Check the main.log file for more information.")

                            # Sent email when the sctipt ends with maxParallelJobs error
                            emailText = "Il processo di cancellazione e' terminato per il superamento del numero massimo delivery contemporanee. \r\nSi chiede di verificare il file 'main.log' per identificare eventuali problematiche."
                            emailSub = "EDC - processo di cancellazione automatica sample dei dati - fine processo con errore"
                            sendMail(emailSub, emailText)

                            sys.exit()

                else:  # the job is finished...

                    # Completed with a succcess status
                    if status["status"] == "Completed":
                        print(f"The job for resource [{resourceName}] - jobID [{jobId}] completed with success.")
                        logging.info(f"The job for resource [{resourceName}] - jobID [{jobId}] completed with success.")  # log

                        jsonVals = setJsonOption(jsonVals, "SaveSourceData", ["true"])  # SaveSourceData

                        # Update the resource with the updated JSON.
                        updateRes = caller.setResJSON(resourceName, jsonVals)

                    # Completed with a failed status
                    elif status["status"] == "Failed":
                        print(f"The job for resource [{resourceName}] - jobID [{jobId}] failed.")
                        logging.error(f"The job for resource [{resourceName}] - jobID [{jobId}] failed.")  # log

                        emailText = f"Si comunica che la risorsa {resourceName} e' fallita."

                        # Print the error on the screen
                        for item in status["resourceTaskStatusList"]:
                            if item['status'] == "Failed":
                                print(f"{item['taskTypeLabel']} status [{item['status']}]: {item['logLocation']}")
                                logging.debug(f"{item['taskTypeLabel']} status [{item['status']}]: {item['logLocation']}")  # log

                                emailText = emailText + f"\r\n\t{item['taskTypeLabel']} status [{item['status']}]: {item['logLocation']}"

                            else:
                                print(f"{item['taskTypeLabel']} status [{item['status']}]")
                                logging.debug(f"{item['taskTypeLabel']} status [{item['status']}]")  # log

                        # Sent email when the run fails
                        emailSub = "EDC - processo di cancellazione automatica sample dei dati - segnalazione errore"
                        sendMail(emailSub, emailText)

                    else:
                        print(f"The Job for the resource [{resourceName}] - jobID [{jobId}] ended with state [{status['status']}].")

                    jobEnd = True

        # Sent email on end of activities
        emailText = "Il processo di cancellazione e' terminato. Si chiede di verificare il file 'main.log' per identificare eventuali problematiche."
        emailSub = "EDC - processo di cancellazione automatica sample dei dati - fine processo"
        sendMail(emailSub, emailText)

    else:
        print("Nothing to do.")
