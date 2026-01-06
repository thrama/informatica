import os

# GENERAL CONFS
# infaHome = "/informatica/edc/10.4.1"
infaHome = os.environ.get("INFA_HOME")
resultFolder = "resultFile"
sheetName = "Sheet1"
sleepTime = 5  # seconds
maxParallelJobs = 3

# EMAIL CONFS
smtpHost = "smtp.example.com:25"
sender = "noreply@example.com"
smtpAuth = "login"
smtpAuthUser = "ChangeMe123!"
smtpAuthPassword = "ChangeMe456!"
to = "alert@example.com"
