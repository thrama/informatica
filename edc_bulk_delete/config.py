import os

# GENERAL CONFS
#infaHome = "/informatica/edc/10.4.1"
infaHome = os.environ.get('INFA_HOME')
resultFolder = "resultFile"
sheetName = "Sheet1"
sleepTime = 5  # seconds
maxParallelJobs = 3

# EMAIL CONFS
smtpHost = "smtp.intesasanpaolo.com:25"
sender = "01mail11319@intesasanpaolo.com"
smtpAuth = "login"
smtpAuthUser = "01mail11319"
smtpAuthPassword = "SrkjNv_A1v4UJ"
to = "llombardi@informatica.com,supporto_informatica@intesasanpaolo.com,supportodatadiscovery@accenture.com"
#to = "llombardi@informatica.com"
