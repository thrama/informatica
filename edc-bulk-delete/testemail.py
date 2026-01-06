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
resource = "Pippo"
status = "Running"

emailText = f"Si comunica che la risorsa {resource} e' stata skippata dal processo perche' rimasta troppo tempo in stato {status}. Verificare la causa. \r\nNOTA: Verificare il corretto completamento del run e, al termine, la corretta impostazione del flag 'SaveSourceData' a 'true'. Modificarne il valore manualmente se necessario."
emailSub = "EDC - processo di cancellazione automatica sample dei dati - segnalazione errore"
sendMail(emailSub, emailText)
