import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


### sendMail #################################################################
def sendMail(subject, text):
    """Send alert email."""

    try:
        # Compese message
        message = MIMEMultipart()

        message["From"] = config.sender
        message["To"] = config.to
        message["Subject"] = subject

        message.attach(MIMEText(text, "plain"))

        print(message)

        # Send the mail
        server = smtplib.SMTP(config.smtpHost)
        server.login(config.smtpAuthUser, config.smtpAuthPassword)
        server.sendmail(message["From"], message["To"].split(","), message.as_string())
        server.quit()

    except Exception as e:
        print(e)


### MAIN #####################################################################
resource = "TestResource"
status = "Running"

emailText = f"The resource {resource} has been skipped from the process because it remained too long in the {status} state. Please verify the cause. \r\nNOTE: Verify the correct completion of the run and, at the end, the correct setting of the 'SaveSourceData' flag to 'true'. Change its value manually if necessary."
emailSub = "EDC - Automatic sample data deletion process - error notification"
sendMail(emailSub, emailText)
