import subprocess
import datetime
import re
import pytz
import time
import os

date_format='%m/%d/%Y %H:%M:%S %Z'
def print_time():
    date = datetime.datetime.now(tz=pytz.utc)
    date = date.astimezone(pytz.timezone('US/Pacific'))
    print(date.strftime(date_format))

def print_ping():
    ping_response = subprocess.Popen(["ping", "-c1", "ftx.com"], stdout=subprocess.PIPE).stdout.read()
    print(re.search(r'time=(\d+)',ping_response.decode(), re.MULTILINE).group(1) +' ms')

def clear_sceen():
    os.system('cls' if os.name == 'nt' else 'clear')
