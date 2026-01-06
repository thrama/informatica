import time
from datetime import datetime

datenow = datetime.now().date()  # current date in date format
now = datetime.now()  # current date in timestamp format
start_time = time.time()  # current time in miliseconds
current_time = now.strftime("%H%M%S")  # current time in HH:MM:SS format
# current date in datababse format (yyyy-mm-dd hh:mm:ss)
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
dt_zip = now.strftime("%Y%m%d")
toDate = str(dt_string)  # date as string

nowIso = now.replace(microsecond=0).isoformat()
toDateEdc = str(nowIso)
