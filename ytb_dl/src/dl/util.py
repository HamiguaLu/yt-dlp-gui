import glob
import os
#from langdetect import detect
#import requests
import shutil
from pathlib import Path
import json
import re
#from PIL import Image
from subprocess import PIPE, run
import subprocess
#import win32api
import sys
import unittest
import time
import datetime
from urllib.parse import unquote
import urllib
import urllib.parse
#import pandas
import re
import uuid
from PySide2.QtCore import QDate, QTime, QDateTime
import datetime, time

import validators

SETTING_FILE = 'dld.pref'


def send_log_to_mail(to, subject, content):
    return
    para = {'to':to,'subject':subject,'content':content}
    url = 'https://autopostsocial.com/mail.php?{}'.format(urllib.parse.urlencode(para))
    print(url)
    r = requests.get(url)
    if r.status_code != 200:
        print('send mail failed with:' + str(r.status_code))
        return False
    return True


def set_scheduler(settings):
    print('not implemented!!!')
    os.system(
        r'SchTasks /Create /SC DAILY /TN "My Task" /TR "C:mytask.bat" /ST 09:00')

    # https://stackoverflow.com/questions/26160900/is-there-a-way-to-add-a-task-to-the-windows-task-scheduler-via-python-3
    # https://docs.microsoft.com/en-us/windows/win32/taskschd/schtasks


def validate_mail(email):
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    return EMAIL_REGEX.match(email)


def is_url_valid(url):
    return validators.url(url)

########setting manage



def save_global_settings(global_settings):
    with open(SETTING_FILE, 'w+', encoding='utf8') as file:
        json.dump(global_settings, file, ensure_ascii=False,
                  indent=4, sort_keys=True)
        file.close()


def mk_default_download_folder():
    data_folder = os.getenv('LOCALAPPDATA') 
    data_folder = os.path.join(data_folder,'social_autopost_data')
    Path(data_folder).mkdir(parents=True, exist_ok=True)
    return data_folder
    

def load_global_settings():
    settings = {}
    if os.path.isfile(SETTING_FILE):
        with open(SETTING_FILE, 'r', encoding='utf8') as file:
            settings = json.load(file)
            file.close()
            return settings

    settings['usr_folder'] = mk_default_download_folder()
    
    save_global_settings(settings)

    return settings


def get_download_dir():
    settings = load_global_settings()
    download_dir = settings['usr_folder']
    if os.access(download_dir, os.W_OK):
        return download_dir
    return None


########post data manage


# https://stackoverflow.com/questions/26160900/is-there-a-way-to-add-a-task-to-the-windows-task-scheduler-via-python-3
# https://docs.microsoft.com/en-us/windows/win32/taskschd/schtasks
#https://stackoverflow.com/questions/4438020/how-to-start-a-python-file-while-windows-starts
import getpass
#


def add_to_startup(file_path=""):
    USER_NAME = getpass.getuser()
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)


def qttime2seconds(qt_datetime):
    dt = qt_datetime.toPython()
    s = time.mktime(dt.timetuple())
    return s
    
    
def seconds2qttime(seconds):
    print(seconds)
    dt = datetime.datetime.fromtimestamp(seconds)
    return QDateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute,00)
    
    
    
    
    
    

