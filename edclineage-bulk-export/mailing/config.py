# GENERAL CONFS
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


from dotenv import load_dotenv, find_dotenv

from props.paramsEdc import emailReceivers
from props.utils import os, dt_zip

basedir = os.getcwd()
load_dotenv(find_dotenv())


def sendSuccessEmail():
    try:
        smtp_server = os.getenv('STMP_HOST')

        port = os.getenv('STMP_PORT')  # For starttls
        sender_email = os.getenv('STMP_USER')
        password = os.getenv('STMP_PWD')

        receiver_email = emailReceivers

        msg = MIMEMultipart()

        msg['From'] = sender_email
        msg['To'] = ", ".join(emailReceivers)
        msg['Subject'] = "SUBJECT OF THE EMAIL"

        body = "TEXT YOU WANT TO SEND"

        msg.attach(MIMEText(body, 'plain'))

        filename = dt_zip+'.log'
        attachment = open(os.path.join(basedir+'/'+filename), "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)

        msg.attach(part)

        # Try to log in to server and send email
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Email sent")

    except Exception as e:
        # Print any error messages to stdout
        print('Email not sent')
        print(e)
    finally:
        server.quit()



